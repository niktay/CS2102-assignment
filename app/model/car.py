from model.model import Model


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
                "INSERT INTO Car (license_number, license_plate,"
                f"brand, model)"
                f"VALUES ('{self.license_number}', '{self.license_plate}', "
                f"'{self.brand}', '{self.model}');",
            )
            self.conn.commit()
            return True
        except Exception as e:
            # TODO(Glenice): Error handling/logging
            print(e)
        return False

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
