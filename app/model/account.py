from flask_login import UserMixin
from model.model import Model
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


class Account(UserMixin, Model):

    def __init__(self, *args, **kwargs):
        super().__init__()

        if args:
            self.username = args[0]
            self.id = self.username  # flask-login expects id
            self.is_admin = args[1]
            self.date_of_birth = args[2]
            self.email = args[3]
            self.contact = args[4]
            self.password = args[5]
            self.name = args[6]
            self.confirm_password = None
        elif kwargs:
            kwargs = {k: v[0] for k, v in kwargs.items()}

            self.name = kwargs.get('full-name', None)
            self.username = kwargs.get('username', None)
            self.id = self.username  # flask-login expects id
            self.date_of_birth = kwargs.get('date-of-birth', None)
            self.email = kwargs.get('email', None)
            self.contact = kwargs.get('contact', None)
            self.is_admin = kwargs.get('is-admin', False)
            self.password = kwargs.get('password', None)
            self.confirm_password = kwargs.get('confirm-password', None)
        else:
            pass

    def _auth_validate(self):
        return any([self.username, self.password])

    def _save_validate(self):
        return any([
            self.name, self.username, self.date_of_birth, self.email,
            self.contact, self.password,
        ])

    def toggle_admin_status(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE account SET is_admin = NOT is_admin WHERE username = "
                f"'{self.username}';",
            )
            self.conn.commit()

            return True

        except Exception as e:
            # TODO(Nik): Error handling/logging
            print(e)

        return False

    @classmethod
    def load(cls, username):
        if not username:
            return None

        try:
            account = cls()
            cursor = account.conn.cursor()
            cursor.execute(
                f"SELECT * FROM Account WHERE username = '{username}';",
            )
            account_found = cursor.fetchone()

            if not account_found:
                return None

            return cls(*account_found)

        except Exception as e:
            # TODO(Nik): Error handling/logging
            print(e)

        return None

    def authenticate(self):
        if not self._auth_validate():
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT pass FROM Account "
                f"WHERE username = '{self.username}';",
            )
            stored_account = cursor.fetchone()

            if not stored_account:
                return False

            return check_password_hash(stored_account[0], self.password)

        except Exception as e:
            # TODO(Nik): Error handling/logging
            print(e)

        return False

    def save(self):
        if (
            not self.password or not self.confirm_password or
            self.password != self.confirm_password
        ):
            # TODO(Nik): Throw some error/log
            return

        if not self._save_validate():
            # TODO(Nik): Throw some error/log
            return
        try:
            cursor = self.conn.cursor()
            self.password = generate_password_hash(self.password)
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
