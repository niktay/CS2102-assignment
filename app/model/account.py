from logging import getLogger

import psycopg2
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.model.database import connection_required

logger = getLogger(__name__)


class Account(UserMixin, object):

    def __init__(
        self, username=None, is_admin=None, date_of_birth=None,
        email=None, contact=None, password=None, name=None,
        confirm_password=None,
    ):

        self.username = username
        self.id = username
        self.is_admin = is_admin
        self.date_of_birth = date_of_birth
        self.email = email
        self.contact = contact
        self.password = password
        self.name = name

        if confirm_password and self.password != confirm_password:
            self.password = None
            logger.debug('Password mismatch, password set to `None`')
            logger.debug(f'Password: {self.password}')
            logger.debug(f'Confirm password: {confirm_password}')

    @classmethod
    def init_using_form(cls, **kwargs):
        for _type in (type(v) for v in kwargs.values()):
            if _type != list:
                raise TypeError('Not all values in kwargs are of type `list`')

        kwargs = {k: v[0] for k, v in kwargs.items() if v[0]}
        logger.debug(f'Extracted from kwargs: {kwargs}')

        username = kwargs.get('username', None)
        date_of_birth = kwargs.get('date-of-birth', None)
        email = kwargs.get('email', None)
        contact = kwargs.get('contact', None)
        password = kwargs.get('password', None)
        confirm_password = kwargs.get('confirm-password', None)
        name = kwargs.get('full-name', None)

        account = cls(
            username=username, date_of_birth=date_of_birth,
            email=email, contact=contact, password=password,
            confirm_password=confirm_password, name=name,
        )
        logger.debug(f'Instantiated Account using form:\n{account}')

        return account

    @connection_required
    def toggle_admin_status(self, conn=None):
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
    @connection_required
    def load(cls, username, conn=None):
        if not username:
            logger.debug(f'Username is empty: {username}')
            return None

        try:
            cursor = conn.cursor()
            logger.debug(f'cursor: {cursor}')

            statement = "SELECT username, is_admin, dob, email, contact, pass,"
            statement += f" name FROM Account WHERE username = '{username}';"
            logger.debug(f'Query: {statement}')
            cursor.execute(statement)

            account_found = cursor.fetchone()
            logger.debug(f'Query result: {account_found}')

            if not account_found:
                return None

            account_details = {
                'username': account_found[0],
                'is_admin': account_found[1],
                'date_of_birth': account_found[2],
                'email': account_found[3],
                'contact': account_found[4],
                'name': account_found[6],
            }

            loaded_account = cls(**account_details)
            logger.debug(f'Loaded Account:\n{loaded_account}')

            return loaded_account

        except psycopg2.Error as e:
            logger.warning('Failed to load Account from database')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning('Failed to load Account from database')
            logger.critical(e)

    @connection_required
    def authenticate(self, conn=None):
        required_parameters = [self.username, self.password]

        if not all(required_parameters):
            logger.warning(f'Insufficient parameters to authenticate Account')
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

        except psycopg2.Error as e:
            logger.warning('Failed to authenticate Account')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning('Failed to authenticate Account')
            logger.critical(e)

    @connection_required
    def save(self, conn=None):
        required_parameters = [
            self.name, self.username, self.date_of_birth,
            self.email, self.contact, self.password,
        ]
        if not all(required_parameters):
            logger.warning('Insufficient fields provided to create Account')
            return False

        try:
            self.password = generate_password_hash(self.password)

            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Account (name, username, dob, email, contact, "
                f"pass, is_admin) VALUES ('{self.name}', '{self.username}', "
                f"'{self.date_of_birth}', '{self.email}', '{self.contact}', "
                f"'{self.password}', 'False');",
            )
            self.conn.commit()

        except psycopg2.Error as e:
            logger.warning(f'Failed to create Account {self.username}')
            logger.debug(e.diag.message_detail)

        except Exception as e:
            logger.warning(f'Failed to create Account {self.username}')
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
