import datetime
from logging import getLogger

import psycopg2
from model.model import Model


logger = getLogger(__name__)


class Driver(Model):

    def __init__(self, *args, **kwargs):
        super().__init__()

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

    def save(self):
        if not self._validate():
            logger.warning('Insufficient fields provided to create driver')
            logger.warning('Driver not created')
            return False

        try:
            today = datetime.datetime.now()
            self.driving_since = today.strftime('%Y-%m-%d')

            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Driver (license_number, username,"
                f"driving_since, optional_bio)"
                f"VALUES ('{self.license_number}', '{self.username}', "
                f"'{self.driving_since}', '{self.optional_bio}');",
            )
            self.conn.commit()

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

    def update(self):
        print(self)
        if not self._validate():
            logger.warning('Insufficient fields provided to update driver')
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE Driver SET optional_bio = '{self.optional_bio}' "
                f"WHERE license_number = '{self.license_number}';",
            )

            self.conn.commit()

            logger.info(f'Driver details for {self.license_number} updated')
            return True

        except psycopg2.Error as e:
            logger.warning('Failed to update driver {self.license_number}')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning('Failed to update driver {self.license_number}')
            logger.critical(e)

    def get_license_number(self):
        return self.license_number

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
    def get_driver(cls, username):
        if not username:
            return None

        driver = cls()
        try:
            cursor = driver.conn.cursor()
            cursor.execute(
                f"SELECT * FROM Driver WHERE username = '{username}';",
            )

            driver_found = list(cursor.fetchone())

            return driver_found

        except psycopg2.Error as e:
            logger.warning('Failed to get driver {username}')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning('Failed to get driver {username}')
            logger.critical(e)
