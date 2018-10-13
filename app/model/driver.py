import datetime

from model.model import Model


class Driver(Model):

    def __init__(self, **kwargs):
        super().__init__()

        kwargs = {k: v[0] for k, v in kwargs.items()}

        self.license_number = kwargs.get('license-number', None)
        self.username = kwargs.get('username', None)
        self.optional_bio = kwargs.get('optional-bio', None)

        today = datetime.datetime.now()
        self.driving_since = today.strftime("%Y-%m-%d")

    def _validate(self):
        return any([
            self.license_number, self.username, self.driving_since,
        ])

    def save(self):
        if not self._validate():
            # TODO(Glenice): Throw some error/log
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Driver (license_number, username,"
                f"driving_since, optional_bio)"
                f"VALUES ('{self.license_number}', '{self.username}', "
                f"'{self.driving_since}', '{self.optional_bio}');",
            )
            self.conn.commit()
            return True
        except Exception as e:
            # TODO(Glenice): Error handling/logging
            print(e)
        return False

    def get(self):
        return [
            self.license_number, self.username,
            self.optional_bio, self.driving_since,
        ]

    def update(self):
        print(self)
        if not self._validate():
            # TODO(Glenice): Throw some error/log
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE Driver SET optional_bio = '{self.optional_bio}' "
                f"WHERE license_number = '{self.license_number}';",
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
                               Driver
--------------------------------------------------------------------------------
license_number: {self.license_number}
username: {self.username}
driving_since: {self.driving_since}
optional_bio: {self.optional_bio}
--------------------------------------------------------------------------------
"""
        return output
