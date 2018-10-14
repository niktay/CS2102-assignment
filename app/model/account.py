from logging import getLogger

import psycopg2
from flask_login import UserMixin
from model.model import Model
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

logger = getLogger(__name__)


class Account(UserMixin, Model):

    def __init__(self, *args, **kwargs):
        super().__init__()

        if args:
            logger.debug(f'Intializing Account with args:\n{args}')

            try:
                self.username = args[0]
                self.id = self.username  # flask-login expects id
                self.is_admin = args[1]
                self.date_of_birth = args[2]
                self.email = args[3]
                self.contact = args[4]
                self.password = args[5]
                self.name = args[6]
                self.confirm_password = None

            except IndexError as e:
                logger.error('Insufficient metadata to initialize Account:')
                logger.error(e)

            except Exception as e:
                logger.critical('Account failed to initialize')

            logger.debug(f'Account initialzed:\n{self}')

        elif kwargs:
            try:
                logger.debug(f'Intializing Account with kwargs:\n{kwargs}')
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

                logger.debug(f'Account initialzed: \n{self}')

            except TypeError as e:
                logger.error(e)

            except Exception as e:
                logger.critical('Account failed to initialize')

        else:
            logger.warning('Account initialized with no metadata')
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
            logger.info(f'Toggling admin status for username: {self.username}')

            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE account SET is_admin = NOT is_admin WHERE username = "
                f"'{self.username}';",
            )
            self.conn.commit()

            logger.info(f'Admin status toggled successfully')

            return True

        except psycopg2.Error as e:
            logger.warning('Failed to toggle admin status')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning('Failed to toggle admin status')
            logger.critical(e)

        return False

    @classmethod
    def load(cls, username):
        if not username:
            return None

        try:
            logger.info(f'Loading account {username} for database')
            account = cls()
            cursor = account.conn.cursor()
            cursor.execute(
                f"SELECT * FROM Account WHERE username = '{username}';",
            )
            account_found = cursor.fetchone()

            if not account_found:
                logger.info(f'Account {username} not found')
                return None

            logger.info(f'Account {username} found')
            return cls(*account_found)

        except psycopg2.Error as e:
            logger.warning('Failed to load account from database')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning('Failed to load account from database')
            logger.critical(e)

    def authenticate(self):
        if not self._auth_validate():
            logger.warning(f'Insufficient parameters to authenticate user')
            return False

        try:
            logger.info(f'Attemping to authenticate account {self.username}')

            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT pass FROM Account "
                f"WHERE username = '{self.username}';",
            )
            stored_account = cursor.fetchone()

            if not stored_account:
                logger.info(f'Account {self.username} not found')
                return False

            return check_password_hash(stored_account[0], self.password)

        except psycopg2.Error as e:
            logger.warning('Failed to authenticate account')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning('Failed to authenticate account')
            logger.critical(e)

    def save(self):
        if (
            not self.password or not self.confirm_password or
            self.password != self.confirm_password
        ):
            logger.warning('Password field(s) empty mismatched')
            logger.warning('Account not created')
            return

        if not self._save_validate():
            logger.warning('Insufficient fields provided to create account')
            logger.warning('Account not created')
            return
        try:
            self.password = generate_password_hash(self.password)

            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Account (name, username, dob, email, contact, "
                f"pass, is_admin) VALUES ('{self.name}', '{self.username}', "
                f"'{self.date_of_birth}', '{self.email}', '{self.contact}', "
                f"'{self.password}', '{self.is_admin}');",
            )
            self.conn.commit()

            logger.info(f'Account {self.username} created')

        except psycopg2.Error as e:
            logger.warning(f'Failed to create account {self.username}')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning(f'Failed to create account {self.username}')
            logger.critical(e)

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
