import datetime
from logging import getLogger

import psycopg2

from app.model.database import connection_required


logger = getLogger(__name__)


class Driver(object):

    def __init__(self, *args, **kwargs):
        kwargs = {k: v[0] for k, v in kwargs.items()}

        self.license_number = kwargs.get('license-number', None)
        self.username = kwargs.get('username', None)
        self.optional_bio = kwargs.get('optional-bio', None)
        self.driving_since = kwargs.get('driving-since', None)

        if args:
            self.username = args[0]

        logger.debug(f'Driver initialized"\n{self}')

    def _validate(self):
        return any([
            self.license_number, self.username, self.driving_since,
        ])

    @connection_required()
    def save(self, conn=None):
        if not self._validate():
            logger.warning('Insufficient fields provided to create driver')
            logger.warning('Driver not created')
            return False

        try:
            today = datetime.datetime.now()
            self.driving_since = today.strftime('%Y-%m-%d')

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Driver (license_number, username,"
                f"driving_since, optional_bio)"
                f"VALUES ('{self.license_number}', '{self.username}', "
                f"'{self.driving_since}', '{self.optional_bio}');",
            )
            conn.commit()

            logger.info(f'Driver {self.username} created')

            return True

        except psycopg2.Error as e:
            logger.warning(f'Failed to create driver {self.username}')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning(f'Failed to create driver {self.username}')
            logger.critical(e)

    def get(self):
        return [
            self.license_number, self.username,
            self.optional_bio, self.driving_since,
        ]

    @connection_required()
    def update(self, conn=None):
        if not self._validate():
            logger.warning('Insufficient fields provided to update driver')
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Driver "
                f"SET optional_bio = '{self.optional_bio}' "
                f"WHERE license_number = '{self.license_number}';",
            )

            conn.commit()

            logger.info(f'Driver details for {self.license_number} updated')
            return True

        except psycopg2.Error as e:
            logger.warning('Failed to update driver {self.license_number}')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning('Failed to update driver {self.license_number}')
            logger.critical(e)

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

    @classmethod
    @connection_required()
    def get_driver(cls, username, conn=None):
        if not username:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT license_number, username, "
                f"driving_since, optional_bio "
                f"FROM Driver WHERE username = '{username}';",
            )

            results = cursor.fetchone()

            if results is None:
                return None

            driver_found = list(results)

            return driver_found

        except psycopg2.Error as e:
            logger.warning(f'Failed to get driver {username}')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning(f'Failed to get driver {username}')
            logger.critical(e)
