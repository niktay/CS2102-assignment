from model.model import Model


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
            # TODO(Danny) Throw some error/log
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
        except Exception as e:
            # TODO(Danny) Error handling/logging
            print(e)
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
