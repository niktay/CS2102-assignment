from logging import getLogger

import psycopg2
from model.model import Model


logger = getLogger(__name__)


class Advertisement(Model):

    def __init__(self, *args, **kwargs):
        super().__init__()

        kwargs = {k: v[0] for k, v in kwargs.items()}

        self.start_timestamp = kwargs.get('date-and-time', None)
        self.origin = kwargs.get('origin', None)
        self.destination = kwargs.get('destination', None)

        if(args):
            self.license_number = args[0]

    def _validate(self):
        return any([
            self.start_timestamp, self.origin, self.destination,
            self.license_number,
        ])

    def save(self):
        if not self._validate():
            logger.warning(
                'Insufficient fields provided to insert advertisement',
            )
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Advertisement (start_timestamp, license_number,"
                f"origin, destination)"
                f"VALUES ('{self.start_timestamp}', '{self.license_number}',"
                f"'{self.origin}', '{self.destination}');",
            )
            self.conn.commit()
            return True

        except psycopg2.Error as e:
            logger.warning('Failed to update advertisement')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning('Failed to update advertisement')
            logger.critical(e)

        return False

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

    @classmethod
    def get_all(cls):
        results = []

        advert = Advertisement()
        try:
            cursor = advert.conn.cursor()
            cursor.execute(
                'SELECT * FROM Advertisement NATURAL JOIN Driver;',
            )

            results = cursor.fetchall()

            print(results)

            return results
        except Exception as e:
            logger.warning('Failed to load advertisements')
            logger.critical(e)

    @classmethod
    def get_advert(cls, start_timestamp, license_number):
        advert = Advertisement()
        try:
            cursor = advert.conn.cursor()
            cursor.execute(
                "SELECT a.start_timestamp, a.origin, a.destination, "
                f"c.license_plate, c.brand, c.model "
                f"FROM Advertisement a "
                f"INNER JOIN Driver d ON d.license_number = a.license_number "
                f"INNER JOIN Car c ON c.license_number = a.license_number "
                f"WHERE a.license_number = '{license_number}' "
                f"and a.start_timestamp = '{start_timestamp}';",
            )

            result = cursor.fetchone()

            return result
        except Exception as e:
            logger.warning('Failed to load advertisements')
            logger.critical(e)

    @classmethod
    def get_mine(cls, license_number):
        results = []

        advert = Advertisement()
        try:
            cursor = advert.conn.cursor()
            cursor.execute(
                "SELECT * FROM Advertisement  NATURAL JOIN Driver"
                f"WHERE license_number = '{license_number}';",
            )

            results = cursor.fetchall()

            return results
        except Exception as e:
            logger.warning(
                'Failed to load advertisements from {license_number}',
            )
            logger.critical(e)
