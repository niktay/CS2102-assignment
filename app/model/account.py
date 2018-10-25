import datetime
from datetime import datetime as dt
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

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth):
        if date_of_birth is None:
            self._date_of_birth = None
        elif type(date_of_birth) == datetime.date:
            self._date_of_birth = date_of_birth
        elif type(date_of_birth) == datetime.datetime:
            self._date_of_birth = date_of_birth.date()
        elif type(date_of_birth) == str:
            try:
                self._date_of_birth = dt.strptime(
                    date_of_birth,
                    '%Y-%m-%d',
                ).date()
            except ValueError:
                logger.debug(date_of_birth)
                logger.error('date_of_birth string not in YYYY-MM-DD')
                raise
        else:
            logger.debug(type(date_of_birth))
            raise TypeError(
                'date_of_birth can only be assigned types: str, '
                'datetime.datetime, datetime.datetime.date',
            )

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, is_admin):
        if type(is_admin) == bool:
            self._is_admin = is_admin
        elif is_admin is None:
            self._is_admin = None
        elif type(is_admin) == str:
            allowed_str = ['True', 'TRUE', 'true', 'False', 'FALSE', 'false']

            if is_admin not in allowed_str:
                logger.debug(is_admin)
                raise ValueError(f'is_admin not in: {allowed_str}')

            self._is_admin = (is_admin.lower() == 'true')
        else:
            logger.debug(type(is_admin))
            raise TypeError('is_admin can only be assigned types: bool, str')

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
            logger.debug(conn)

            cursor = conn.cursor()
            cursor.execute(
                "UPDATE account SET is_admin = NOT is_admin WHERE username = "
                f"'{self.username}';",
            )
            conn.commit()

            logger.info(f'Admin status toggled successfully')

        except AttributeError:
            logger.error(
                'Unable to toggle admin status, '
                'did you pass in a connection?',
            )
            logger.debug(conn)
            raise

        except psycopg2.InterfaceError:
            logger.error('Unable to toggle admin status, is connection open?')
            logger.debug(conn)
            raise

        except psycopg2.OperationalError:
            logger.error('Unable to toggle admin status, is database running?')
            raise

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

        except AttributeError:
            logger.error('Unable to load user, did you pass in a connection?')
            logger.debug(conn)
            raise

        except psycopg2.InterfaceError:
            logger.error('Unable to load user, is connection open?')
            logger.debug(conn)
            raise

        except psycopg2.OperationalError:
            logger.error('Unable to load user, is database running?')
            raise

    @connection_required
    def authenticate(self, conn=None):
        required_parameters = [self.username, self.password]

        if not all(required_parameters):
            logger.debug(
                f'username: {self.username}\npassword: '
                f'{self.password}',
            )
            raise TypeError(
                'authenticate requires both username and password '
                'to be set',
            )

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT pass FROM Account "
                f"WHERE username = '{self.username}';",
            )
            stored_account = cursor.fetchone()
            logger.debug(f'Query Result: {stored_account}')

            if not stored_account:
                return False

            logger.debug(
                f'comparing {generate_password_hash(self.password)} '
                f'with {stored_account[0]}',
            )
            return check_password_hash(stored_account[0], self.password)

        except AttributeError:
            logger.error(
                'Unable to authenticate, '
                'did you pass in a connection?',
            )
            logger.debug(conn)
            raise

        except psycopg2.InterfaceError:
            logger.error('Unable to authenticate, is connection open?')
            logger.debug(conn)
            raise

        except psycopg2.OperationalError:
            logger.error('Unable to authenticate, is database running?')
            raise

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

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Account (name, username, dob, email, contact, "
                f"pass, is_admin) VALUES ('{self.name}', '{self.username}', "
                f"'{self.date_of_birth}', '{self.email}', '{self.contact}', "
                f"'{self.password}', 'False');",
            )
            conn.commit()

            return True

        except psycopg2.IntegrityError:
            logger.warning('Unable to save, username already exists')
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
