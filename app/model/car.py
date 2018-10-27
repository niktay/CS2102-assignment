from logging import getLogger

import psycopg2

from app.model.database import connection_required


logger = getLogger(__name__)


class Car(object):

    def __init__(
        self, license_number=None, license_plate=None, brand=None,
        model=None,
    ):

        self.license_number = license_number
        self.license_plate = license_plate
        self.brand = brand
        self.model = model

    @classmethod
    def init_using_form(cls, **kwargs):
        for _type in (type(v) for v in kwargs.values()):
            if _type != list:
                raise TypeError('Not all values in kwargs are of type `list`')

        kwargs = {k: v[0] for k, v in kwargs.items() if v[0]}
        logger.debug(f'Extracted from kwargs: {kwargs}')

        license_number = kwargs.get('license-number', None)
        license_plate = kwargs.get('license-plate', None)
        brand = kwargs.get('brand', None)
        model = kwargs.get('model', None)

        car = cls(
            license_number=license_number, license_plate=license_plate,
            brand=brand, model=model,
        )
        logger.debug(f'Instantiated Car using form:\n{car}')

        return car

    @connection_required
    def save(self, conn=None):
        required_parameters = [
            self.license_number, self.license_plate,
            self.brand, self.model, ]
        if not all(required_parameters):
            logger.warning('Insufficient fields provided to add car')
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO car (license_number, license_plate,"
                f"brand, model)"
                f"VALUES ('{self.license_number}', '{self.license_plate}', "
                f"'{self.brand}', '{self.model}');",
            )
            conn.commit()

            return True

        except psycopg2.IntegrityError:
            logger.warning('Unable to save, license plate already exists')
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
    def update(self, conn=None):
        required_parameters = [
            self.license_number, self.license_plate,
            self.brand, self.model, ]
        if not all(required_parameters):
            logger.warning('Insufficient fields provided to update car')
            return False

        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM car WHERE license_plate = "
                f"'{self.license_plate}';",
            )
            conn.commit()

            if cursor.fetchone() is None:
                return False

            cursor.execute(
                f"UPDATE car SET brand = '{self.brand}', model = "
                f"'{self.model}' WHERE license_plate = "
                f"'{self.license_plate}';",
            )

            conn.commit()

            return True

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
    def load(cls, license_number=None, license_plate=None, conn=None):
        # Check if either license_number or license_plate is set (XOR)
        if not bool(license_number) != bool(license_plate):
            logger.warning('load called with invalid parameters')
            logger.debug(license_number)
            logger.debug(license_plate)
            return None

        try:
            cursor = conn.cursor()

            if license_number:
                cursor.execute(
                    "SELECT license_plate, license_number, brand, model FROM "
                    f"car WHERE license_number = '{license_number}';",
                )
            else:
                cursor.execute(
                    "SELECT license_plate, license_number, brand, model FROM "
                    f"car WHERE license_plate = '{license_plate}';",
                )

            car_found = cursor.fetchone()

            if not car_found:
                return None

            car_details = {
                'license_plate': car_found[0],
                'license_number': car_found[1],
                'brand': car_found[2],
                'model': car_found[3],
            }

            loaded_car = cls(**car_details)
            logger.debug(f'Loaded Car:\n{loaded_car}')

            return loaded_car

        except AttributeError:
            logger.error('Unable to load car, did you pass in a connection?')
            logger.debug(conn)
            raise

        except psycopg2.InterfaceError:
            logger.error('Unable to load car, is connection open?')
            logger.debug(conn)
            raise

        except psycopg2.OperationalError:
            logger.error('Unable to load car, is database running?')
            raise

    def __str__(self):
        output = f"""
--------------------------------------------------------------------------------
                               Car
--------------------------------------------------------------------------------
license_plate: {self.license_plate}
license_number: {self.license_number}
brand: {self.brand}
model: {self.model}
--------------------------------------------------------------------------------
"""
        return output
