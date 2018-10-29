import datetime
from datetime import datetime as dt
from logging import getLogger

import psycopg2

from app.model.car import Car
from app.model.database import connection_required


logger = getLogger(__name__)


class Advertisement(object):

    def __init__(
        self, start_timestamp=None, origin=None, destination=None,
        license_number=None,
    ):

        self.start_timestamp = start_timestamp
        self.origin = origin
        self.destination = destination
        self.license_number = license_number

        logger.debug(self)

    @classmethod
    def init_using_form(cls, **kwargs):
        for _type in (type(v) for v in kwargs.values()):
            if _type != list:
                raise TypeError('Not all values in kwargs are of type `list`')

        kwargs = {k: v[0] for k, v in kwargs.items() if v[0]}
        logger.debug(f'Extracted from kwargs: {kwargs}')

        date = kwargs.get('date', None)
        time = kwargs.get('time', None)

        if date and time:
            start_timestamp = dt.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')
        else:
            start_timestamp = kwargs.get('start-timestamp', None)

        origin = kwargs.get('origin', None)
        destination = kwargs.get('destination', None)
        license_number = kwargs.get('license-number', None)

        advertisement = cls(
            start_timestamp=start_timestamp, origin=origin,
            destination=destination,
            license_number=license_number,
        )

        logger.debug(
            'Instantiated Advertisement using form:\n'
            f'{advertisement}',
        )

        return advertisement

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

    @connection_required
    def car(self, conn=None):
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT c.license_plate, c.brand, c.model, c.license_number, "
                f"a.origin, a.destination FROM Advertisement a "
                f"INNER JOIN Driver d ON d.license_number = a.license_number "
                f"INNER JOIN Car c ON c.license_number = a.license_number "
                f"WHERE a.license_number = '{self.license_number}' "
                f"and a.start_timestamp = '{self.start_timestamp}';",
            )

            car_found = cursor.fetchone()

            if not car_found:
                return None

            car_details = {
                'license_plate': car_found[0],
                'brand': car_found[1],
                'model': car_found[2],
                'license_number': car_found[3],
            }

            car = Car(**car_details)
            logger.debug(car)

            return car
        except Exception as e:
            logger.warning('Failed to load advertisements')
            logger.critical(e)

    @connection_required
    def save(self, conn=None):
        required_parameters = [
            self.start_timestamp, self.origin,
            self.destination, self.license_number, ]
        if not all(required_parameters):
            logger.warning(
                'Insufficient fields provided to insert '
                'advertisement',
            )
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Advertisement (start_timestamp, license_number,"
                f"origin, destination) VALUES ('{self.start_timestamp}', "
                f"'{self.license_number}', '{self.origin}', "
                f"'{self.destination}');",
            )
            logger.debug(self)
            conn.commit()

            return True

        except psycopg2.IntegrityError:
            logger.warning(
                'Unable to save, (start_timestamp, license_number)'
                'already exists',
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
            logger.debug(conn)
            raise

    @classmethod
    @connection_required
    def fetch(cls, license_number=None, conn=None):
        try:
            cursor = conn.cursor()

            if license_number:
                cursor.execute(
                    "SELECT start_timestamp, license_number, "
                    "origin, destination FROM advertisement "
                    f"WHERE license_number='{license_number}'",
                )
            else:
                cursor.execute(
                    'SELECT start_timestamp, license_number, '
                    'origin, destination FROM advertisement;',
                )

            results = cursor.fetchall()

            advertisements = []
            for result in results:
                advertisement_details = {
                    'start_timestamp': result[0],
                    'license_number': result[1],
                    'origin': result[2],
                    'destination': result[3],
                }
                advertisements.append(cls(**advertisement_details))

            return advertisements

        except AttributeError:
            logger.error(
                'Unable to fetch advertisements, '
                'did you pass in a connection?',
            )
            logger.debug(conn)
            raise

        except psycopg2.InterfaceError:
            logger.error(
                'Unable to fetch advertisements, '
                'is connection open?',
            )
            logger.debug(conn)
            raise

        except psycopg2.OperationalError:
            logger.error(
                'Unable to fetch advertisements, '
                'is database running?',
            )
            logger.debug(conn)
            raise

    def __str__(self):
        output = f"""
--------------------------------------------------------------------------------
                               Advertisement
--------------------------------------------------------------------------------
start_timestamp: {self.start_timestamp}
license_number: {self.license_number}
origin: {self.origin}
destination: {self.destination}
--------------------------------------------------------------------------------
"""
        return output
