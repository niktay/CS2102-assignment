import datetime
from datetime import datetime as dt
from logging import getLogger

import psycopg2

from app.model.database import connection_required


logger = getLogger(__name__)


class Bid(object):

    def __init__(
        self, bid_id=None, price=None, username=None, start_timestamp=None,
        license_number=None,
    ):
        self.bid_id = bid_id
        self.price = price
        self.username = username
        self.start_timestamp = start_timestamp
        self.license_number = license_number

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        if price is None:
            self._price = None
        self._price = int(price)

    @property
    def start_timestamp(self):
        return self._start_timestamp

    @start_timestamp.setter
    def start_timestamp(self, start_timestamp):
        if start_timestamp is None:
            self._start_timestamp = None
        elif type(start_timestamp) == datetime.datetime:
            self._start_timestamp = start_timestamp
        elif type(start_timestamp) == str:
            try:
                self._start_timestamp = dt.strptime(
                    start_timestamp,
                    '%Y-%m-%d %H:%M:%S',
                )
            except ValueError:
                logger.debug(start_timestamp)
                logger.error(
                    'start_timestamp string not in '
                    'YYYY-MM-DD HH:MM:SS',
                )
                raise
        else:
            logger.debug(type(start_timestamp))
            raise TypeError(
                'start_timestamp can only be assigned types: str, '
                'datetime.datetime',
            )

    @classmethod
    def init_using_form(cls, **kwargs):
        for _type in (type(v) for v in kwargs.values()):
            if _type != list:
                raise TypeError('Not all values in kwargs are of type `list`')

        kwargs = {k: v[0] for k, v in kwargs.items() if v[0]}
        logger.debug(f'Extracted from kwargs: {kwargs}')

        bid_id = kwargs.get('bid-id', None)
        price = kwargs.get('price', None)
        username = kwargs.get('username', None)
        start_timestamp = kwargs.get('start-timestamp', None)
        license_number = kwargs.get('license-number', None)

        bid = cls(
            bid_id=bid_id, price=price, username=username,
            start_timestamp=start_timestamp, license_number=license_number,
        )
        logger.debug(f'Instantiated Bid using form:\n{bid}')

        return bid

    @connection_required
    def save(self, conn=None):
        required_parameters = [
            self.price, self.username, self.start_timestamp,
            self.license_number,
        ]

        if not all(required_parameters):
            logger.warning('Insufficient fields provided to create Bid')
            return False

        if self.price <= self.get_highest().price:
            logger.warning('Bid price too low')
            return False

        try:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO bid (price, username, start_timestamp, "
                f"license_number) VALUES ('{self.price}', '{self.username}', "
                f"'{self.start_timestamp}', '{self.license_number}');",
            )

            conn.commit()

            return True

        except psycopg2.IntegrityError:
            logger.warning(
                'Unable to save, corresponding advertisement '
                'not found',
            )
            raise

        except AttributeError:
            logger.error('Unable to save, did you pass in a connection?')
            logger.debug(conn)
            raise

        except psycopg2.InterfaceError:
            logger.error('Unable to save, is connection open?')
            logger.debug(conn)
            raise

        except psycopg2.OperationalError:
            logger.error('Unable to save, is database running?')
            raise

    @classmethod
    @connection_required
    def get_highest(cls, conn=None):
        try:
            cursor = conn.cursor()

            cursor.execute(
                'SELECT bid_id, price, username, start_timestamp, '
                'license_number FROM bid WHERE price = (SELECT '
                'max(price) FROM bid;);',
            )

            bid_found = cursor.fetchone()

            if bid_found is None:
                return None

            highest_bid_details = {
                'bid_id': bid_found[0],
                'price': bid_found[1],
                'username': bid_found[2],
                'start_timestamp': bid_found[3],
                'license_number': bid_found[4],
            }

            highest_bid = cls(**highest_bid_details)
            logger.debug(f'Loaded Bid:\n{highest_bid}')

            return highest_bid

        except AttributeError:
            logger.error('Unable to fetch bid, did you pass in a connection?')
            logger.debug(conn)
            raise

        except psycopg2.InterfaceError:
            logger.error('Unable to fetch bid, is connection open?')
            logger.debug(conn)
            raise

        except psycopg2.OperationalError:
            logger.error('Unable to fetch bid, is database running?')
            raise
