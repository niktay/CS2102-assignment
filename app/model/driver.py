from model.model import Model


class Driver(Model):

    def __init__(self, **kwargs):
        super().__init__()

        kwargs = {k: v[0] for k, v in kwargs.items()}

        self.license_number = kwargs.get('license-number', None)
        self.username = kwargs.get('username', None)
        self.driving_since = kwargs.get('driving-since', None)
        self.optional_bio = kwargs.get('optional-bio', None)

    def save(self):
        if not self._validate():
            # TODO(Glenice): Throw some error/log
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Driver (license_number, username,"
                f"driving_since, optional_bio)"
                f"VALUES ('{self.license_number}', '{self.username}', "
                f"'{self.driving_since}', '{self.optional_bio}');",
            )
            self.conn.commit()
        except Exception as e:
            # TODO(Glenice): Error handling/logging
            print(e)

    def __str__(self):
        output = f"""
--------------------------------------------------------------------------------
                               Account
--------------------------------------------------------------------------------
license_number: {self.license_number}
username: {self.username}
driving_since: {self.driving_since}
--------------------------------------------------------------------------------
"""
        return output
