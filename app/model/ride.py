import datetime
from datetime import datetime as dt
from logging import getLogger

import psycopg2

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
