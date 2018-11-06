import datetime
from datetime import datetime as dt
from logging import getLogger

import psycopg2

from app.model.bid import Bid
from app.model.database import connection_required


logger = getLogger(__name__)


class Ride(object):

    def __init__(self, bid_id=None, confirmed_timestamp=None):
        bid_id = bid_id
        confirmed_timestamp = confirmed_timestamp

    @property
    def confirmed_timestamp(self):
        return self._confirmed_timestamp

    @confirmed_timestamp.setter
    def confirmed_timestamp(self, confirmed_timestamp):
        if confirmed_timestamp is None:
            self._confirmed_timestamp = None
        elif type(confirmed_timestamp) == datetime.datetime:
            self._confirmed_timestamp = confirmed_timestamp
        elif type(confirmed_timestamp) == str:
            try:
                self._confirmed_timestamp = dt.strptime(
                    confirmed_timestamp,
                    '%Y-%m-%d %H:%M:%S',
                )
            except ValueError:
                logger.debug(confirmed_timestamp)
                logger.error(
                    'confirmed_timestamp string not in '
                    'YYYY-MM-DD HH:MM:SS',
                )
                raise
        else:
            logger.debug(type(confirmed_timestamp))
            raise TypeError(
                'confirmed_timestamp can only be assigned types: str, '
                'datetime.datetime',
            )

    @classmethod
    @connection_required
    def fetch(cls, username=None, past=False, upcoming=False, conn=None):
        try:
            cursor = conn.cursor()

            if upcoming:
                cursor.execute(
                    "SELECT DISTINCT bid.start_timestamp, bid.license_number, "
                    "bid.price FROM bid, ride WHERE bid.bid_id = ride.bid_id "
                    "and bid.start_timestamp >= now() and "
                    f"bid.username='{username}';",
                )
            elif past:
                cursor.execute(
                    "SELECT DISTINCT bid.start_timestamp, bid.license_number, "
                    "bid.price FROM bid, ride WHERE bid.bid_id = ride.bid_id "
                    "and bid.start_timestamp < now() and "
                    f"bid.username='{username}';",
                )
            else:
                cursor.execute(
                    "SELECT DISTINCT bid.start_timestamp, bid.license_number, "
                    "bid.price FROM bid, ride WHERE bid.bid_id = ride.bid_id "
                    f"and bid.username='{username}';",
                )

            bids_found = cursor.fetchall()
            logger.debug(bids_found)

            bids_for_upcoming_rides = []
            for bid in bids_found:
                bid = Bid(
                    start_timestamp=bid[0],
                    license_number=bid[1],
                    price=bid[2],
                )
                bids_for_upcoming_rides.append(bid)

            return bids_for_upcoming_rides

        except AttributeError:
            logger.error('Unable to confirm, did you pass in a connection?')
            logger.debug(conn)
            raise

        except psycopg2.InterfaceError:
            logger.error('Unable to confirm, is connection open?')
            logger.debug(conn)
            raise

        except psycopg2.OperationalError:
            logger.error('Unable to confirm, is database running?')
            raise

    @classmethod
    @connection_required
    def confirm(cls, bid, conn=None):
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ride (bid_id, confirmed_timestamp) VALUES ("
                f"'{bid.bid_id}', '{dt.now()}');",
            )

            conn.commit()

            return True

        except psycopg2.IntegrityError:
            logger.warning('Unable to confirm, bid_id does not exist')
            raise

        except AttributeError:
            logger.error('Unable to confirm, did you pass in a connection?')
            logger.debug(conn)
            raise

        except psycopg2.InterfaceError:
            logger.error('Unable to confirm, is connection open?')
            logger.debug(conn)
            raise

        except psycopg2.OperationalError:
            logger.error('Unable to confirm, is database running?')
            raise

    @classmethod
    @connection_required
    def total_by_month(cls, conn=None):
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT myMon, COUNT(*) FROM(SELECT "
                "to_char(bid.start_timestamp, 'Mon') as myMon from ride, bid "
                "WHERE ride.bid_id=bid.bid_id AND extract(year from "
                "bid.start_timestamp) = extract(year from NOW())) as foo "
                "GROUP BY myMon;",
            )

            ride_per_month = cursor.fetchall()
            ride_count = {
                'Jan': 0,
                'Feb': 0,
                'Mar': 0,
                'Apr': 0,
                'May': 0,
                'Jun': 0,
                'Jul': 0,
                'Aug': 0,
                'Sep': 0,
                'Oct': 0,
                'Nov': 0,
                'Dec': 0,
            }
            for month, ride in ride_per_month:
                ride_count[month] = int(ride)

            logger.debug(ride_count)

            return ride_count

        except AttributeError:
            logger.error(
                'Unable to make advertisement inactive, '
                'did you pass in a connection?',
            )
            logger.debug(conn)
            raise

        except psycopg2.InterfaceError:
            logger.error(
                'Unable to make advertisement inactive, '
                'is connection open?',
            )
            logger.debug(conn)
            raise

        except psycopg2.OperationalError:
            logger.error(
                'Unable to make advertisement inactive, '
                'is database running?',
            )
            raise
