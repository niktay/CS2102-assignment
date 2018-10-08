from model.model import Model


class Account(Model):

    def __init__(self, **kwargs):
        super().__init__()

        kwargs = {k: v[0] for k, v in kwargs.items()}

        self.name = kwargs.get('full-name', None)
        self.username = kwargs.get('username', None)
        self.date_of_birth = kwargs.get('date-of-birth', None)
        self.email = kwargs.get('email', None)
        self.contact = kwargs.get('contact', None)
        self.is_admin = kwargs.get('is_admin', False)

        password = kwargs.get('password', None)
        confirm_password = kwargs.get('confirm-password', None)

        if password and confirm_password and password == confirm_password:
            self.password = password
        else:
            self.password = None

    def _validate(self):
        return any([
            self.name, self.username, self.date_of_birth, self.email,
            self.contact, self.password,
        ])

    def save(self):
        if not self._validate():
            # TODO(Nik): Throw some error/log
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Account (name, username, dob, email, contact, "
                f"pass, is_admin) VALUES ('{self.name}', '{self.username}', "
                f"'{self.date_of_birth}', '{self.email}', '{self.contact}', "
                f"'{self.password}', '{self.is_admin}');",
            )
            self.conn.commit()
        except Exception as e:
            # TODO(Nik): Error handling/logging
            print(e)

    def __str__(self):
        output = f"""
--------------------------------------------------------------------------------
                               Account
--------------------------------------------------------------------------------
name: {self.name}
username: {self.username}
date of birth: {self.date_of_birth}
email: {self.email}
contact: {self.contact}
password: {self.password}
admin: {self.is_admin}
--------------------------------------------------------------------------------
"""
        return output
