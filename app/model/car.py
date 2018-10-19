from logging import getLogger

import psycopg2
from model.model import Model


logger = getLogger(__name__)


class Car(Model):
    def __init__(self, **kwargs):
        super().__init__()

        kwargs = {k: v[0] for k, v in kwargs.items()}

        self.license_number = kwargs.get('license-number', None)
        self.license_plate = kwargs.get('license-plate', None)
        self.brand = kwargs.get('brand', None)
        self.model = kwargs.get('model', None)

    def _validate(self):
        return any([
            self.license_number, self.license_plate,
            self.brand, self.model,
        ])

    def save(self):
        if not self._validate():
            # TODO(Glenice): Throw some error/log
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO car (license_number, license_plate,"
                f"brand, model)"
                f"VALUES ('{self.license_number}', '{self.license_plate}', "
                f"'{self.brand}', '{self.model}');",
            )
            self.conn.commit()
            return self

        except Exception as e:
            # TODO(Glenice): Error handling/logging
            print(e)
        return False

    def update(self):
        if not self._validate():
            # TODO(Glenice): Throw some error/log
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE car SET "
                f"brand = '{self.brand}',"
                f"model = '{self.model}' "
                f"WHERE license_plate = '{self.license_plate}'",
            )

            self.conn.commit()

            logger.info(f'Car details for {self.license_plate} updated')
            return True

        except psycopg2.Error as e:
            logger.warning('Failed to update car {self.license_plate}')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning('Failed to update car {self.license_plate}')
            logger.critical(e)

    def get(self):
        return [
            self.license_number, self.license_plate,
            self.brand, self.model,
        ]

    def __str__(self):
        output = f"""
--------------------------------------------------------------------------------
                               Car
--------------------------------------------------------------------------------
license_number: {self.license_number}
license_plate: {self.license_plate}
brand: {self.brand}
model: {self.model}
--------------------------------------------------------------------------------
"""
        return output

    @classmethod
    def get_car(cls, license_number):
        car = cls()

        try:
            cursor = car.conn.cursor()
            cursor.execute(
                'SELECT license_plate, brand, model FROM Car'
                f" WHERE license_number = '{license_number}';",
            )
            car_found = list(cursor.fetchone())

            return car_found
        except Exception as e:
            # TODO(Glenice): Error handling/logging
            print(e)
