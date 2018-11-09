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
        start_timestamp = kwargs.get('datetime', None)
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

        logger.debug(f'Attempting to save:\n{self}')
        if not all(required_parameters):
            logger.warning('Insufficient fields provided to create Bid')
            return False

        try:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO bid (price, username, start_timestamp, "
                f"license_number) SELECT '{self.price}', "
                f"'{self.username}', '{self.start_timestamp}', "
                f"'{self.license_number}' "
                f"WHERE {self.price} > get_highest_bid('{self.license_number}'"
                f", '{self.start_timestamp}');",
            )

            conn.commit()
            logger.debug(self)

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
    def get_highest(cls, advertisement=None, conn=None):
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT bid_id, price, username, start_timestamp, "
                "license_number FROM bid WHERE bid_id = (SELECT bid_id FROM "
                f"bid WHERE license_number='{advertisement.license_number}' "
                f"AND start_timestamp='{advertisement.start_timestamp}' "
                "ORDER BY price DESC LIMIT 1);",
            )
            logger.debug(advertisement)
            bid_found = cursor.fetchone()
            logger.debug(bid_found)

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

    @classmethod
    @connection_required
    def dump_hourly(cls, conn=None):
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT bid.price, extract(hour from bid.start_timestamp) FROM"
                " bid,ride WHERE bid.bid_id=ride.bid_id GROUP BY extract(hour "
                "from bid.start_timestamp), bid.price;",
            )
            bid_data = cursor.fetchall()

            logger.debug(bid_data)

            bid_information = []
            for bid, bid_hour in bid_data:
                bid_information.append((int(bid_hour), int(bid)))

            logger.debug(bid_information)
            return bid_information

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

    @classmethod
    def dump_hourly_jinja(cls):
        hourly_data = cls.dump_hourly()

        formatted_data = []
        for hour, bid in hourly_data:
            formatted_data.append(f'{{ x:{hour}, y:{bid} }}')
        logger.debug(formatted_data)
        return ', '.join(formatted_data)

    def __str__(self):
        output = f"""
--------------------------------------------------------------------------------
                               Bid
--------------------------------------------------------------------------------
license_number: {self.license_number}
username: {self.username}
start_timestamp: {self.start_timestamp}
price: {self.price}
--------------------------------------------------------------------------------
"""
        return output
