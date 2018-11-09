import datetime
from datetime import datetime as dt
from logging import getLogger

import psycopg2

from app.model.database import connection_required


logger = getLogger(__name__)


class Driver(object):

    def __init__(
        self, license_number=None, username=None, driving_since=None,
        optional_bio=None,
    ):

        self.license_number = license_number
        self.username = username
        self.driving_since = driving_since
        self.optional_bio = optional_bio

    @property
    def driving_since(self):
        return self._driving_since

    @driving_since.setter
    def driving_since(self, driving_since):
        if driving_since is None:
            self._driving_since = None
        elif type(driving_since) == datetime.date:
            self._driving_since = driving_since
        elif type(driving_since) == datetime.datetime:
            self._driving_since = driving_since.date()
        elif type(driving_since) == str:
            try:
                self._driving_since = dt.strptime(
                    driving_since,
                    '%Y-%m-%d',
                ).date()
            except ValueError:
                logger.debug(driving_since)
                logger.error('driving_since string not in YYYY-MM-DD')
                raise
        else:
            logger.debug(type(driving_since))
            raise TypeError(
                'driving_since can only be assigned types: str, '
                'datetime.datetime, datetime.datetime.date',
            )

    @classmethod
    def init_using_form(cls, **kwargs):
        for _type in (type(v) for v in kwargs.values()):
            if _type != list:
                raise TypeError('Not all values in kwargs are of type `list`')

        kwargs = {k: v[0] for k, v in kwargs.items() if v[0]}
        logger.debug(f'Extracted from kwargs: {kwargs}')

        license_number = kwargs.get('license-number', None)
        username = kwargs.get('username', None)
        driving_since = kwargs.get('driving-since', None)
        optional_bio = kwargs.get('optional-bio', None)

        driver = cls(
            license_number=license_number, username=username,
            optional_bio=optional_bio, driving_since=driving_since,
        )
        logger.debug(f'Instantiated Driver using forrm:\n{driver}')

        return driver

    @connection_required
    def save(self, conn=None):
        required_parameters = [self.license_number, self.username, ]

        if not all(required_parameters):
            logger.warning('Insufficient fields provided to create Driver')
            return False

        try:
            self.driving_since = dt.now().date()

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Driver (license_number, username,"
                f"driving_since, optional_bio)"
                f"VALUES ('{self.license_number}', '{self.username}', "
                f"'{self.driving_since}', '{self.optional_bio}');",
            )
            conn.commit()

            return True

        except psycopg2.IntegrityError as e:
            if 'not present in table "account"' in e.diag.message_detail:
                logger.warning(
                    'Unable to save, provided username not in '
                    'account table',
                )
            else:
                logger.warning('Unable to save, license number already exists')
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

    @connection_required
    def update_bio(self, conn=None):
        required_parameters = [self.license_number, self.optional_bio]
        if not all(required_parameters):
            logger.warning('Insufficient fields provided to update bio')
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE Driver SET optional_bio = '{self.optional_bio}' "
                f"WHERE license_number = '{self.license_number}';",
            )

            conn.commit()

            return True

        except psycopg2.IntegrityError:
            logger.warning(
                'Unable to update bio, license number already '
                'exists',
            )
            raise

        except AttributeError:
            logger.error('Unable to update bio, did you pass in a connection?')
            logger.debug(conn)
            raise

        except psycopg2.InterfaceError:
            logger.error('Unable to update bio, is connection open?')
            logger.debug(conn)
            raise

        except psycopg2.OperationalError:
            logger.error('Unable to update bio, is database running?')
            raise

    @classmethod
    @connection_required
    def load(cls, username=None, license_number=None, conn=None):
        # Check if either username or license_number is set (XOR)
        if not bool(username) != bool(license_number):
            logger.warning('load called with invalid parameters')
            logger.debug(username)
            logger.debug(license_number)
            return None

        try:
            cursor = conn.cursor()

            if username:
                cursor.execute(
                    f"SELECT license_number, username, "
                    f"driving_since, optional_bio "
                    f"FROM Driver WHERE username = '{username}';",
                )
            else:
                cursor.execute(
                    f"SELECT license_number, username, "
                    f"driving_since, optional_bio "
                    f"FROM Driver WHERE license_number = '{license_number}';",
                )

            driver_found = cursor.fetchone()

            if not driver_found:
                return None

            driver_details = {
                'license_number': driver_found[0],
                'username': driver_found[1],
                'driving_since': driver_found[2],
                'optional_bio': driver_found[3],
            }

            loaded_driver = cls(**driver_details)
            logger.debug(f'Loaded Driver:\n{loaded_driver}')

            return loaded_driver

        except AttributeError:
            logger.error(
                'Unable to load driver, did you pass in a '
                'connection?',
            )
            logger.debug(conn)
            raise

        except psycopg2.InterfaceError:
            logger.error('Unable to load driver, is connection open?')
            logger.debug(conn)
            raise

        except psycopg2.OperationalError:
            logger.error('Unable to load driver, is database running?')
            raise

    @classmethod
    @connection_required
    def get_top_drivers(cls, conn=None):
        try:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT SUM(bid.price), driver.username FROM ride, bid, '
                'driver WHERE ride.bid_id = bid.bid_id AND '
                'bid.license_number = driver.license_number GROUP BY '
                'driver.username ORDER BY SUM(bid.price) DESC LIMIT 3',
            )

            top_drivers = cursor.fetchall()

            results = []
            for driver in top_drivers:
                results.append(driver[1])

            return results

        except AttributeError:
            logger.error(
                'Unable to load driver, did you pass in a '
                'connection?',
            )
            logger.debug(conn)
            raise

        except psycopg2.InterfaceError:
            logger.error('Unable to load driver, is connection open?')
            logger.debug(conn)
            raise

        except psycopg2.OperationalError:
            logger.error('Unable to load driver, is database running?')
            raise

    def __str__(self):
        output = f"""
--------------------------------------------------------------------------------
                               Driver
--------------------------------------------------------------------------------
license_number: {self.license_number}
username: {self.username}
driving_since: {self.driving_since}
optional_bio: {self.optional_bio}
--------------------------------------------------------------------------------
"""
        return output
