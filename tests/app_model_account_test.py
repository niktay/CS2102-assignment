import datetime
from datetime import datetime as dt

import psycopg2
import pytest
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.model import Account


# Account.__init__()

def test_init_all_parameters():
    test_attributes = {
        'name': 'Test Case',
        'username': 'tester',
        'date_of_birth': dt(1990, 12, 12).date(),
        'email': 'tester@test.comm',
        'contact': '91234567',
        'is_admin': True,
        'password': '12345678',
        'confirm_password': '12345678',
    }

    test_account = Account(**test_attributes)

    assert test_account.name == test_attributes['name']
    assert test_account.username == test_attributes['username']
    assert test_account.id == test_account.username
    assert test_account.date_of_birth == test_attributes['date_of_birth']
    assert test_account.email == test_attributes['email']
    assert test_account.contact == test_attributes['contact']
    assert test_account.is_admin == test_attributes['is_admin']
    assert test_account.password == test_attributes['password']


def test_init_all_parameters_mismatched_password():
    test_attributes = {
        'name': 'Test Case',
        'username': 'tester',
        'date_of_birth': dt(1990, 12, 12).date(),
        'email': 'tester@test.comm',
        'contact': '91234567',
        'is_admin': True,
        'password': '12345678',
        'confirm_password': 'abcdefgh',
    }

    test_account = Account(**test_attributes)

    assert test_account.name == test_attributes['name']
    assert test_account.username == test_attributes['username']
    assert test_account.id == test_account.username
    assert test_account.date_of_birth == test_attributes['date_of_birth']
    assert test_account.email == test_attributes['email']
    assert test_account.contact == test_attributes['contact']
    assert test_account.is_admin == test_attributes['is_admin']
    assert test_account.password is None


# Account.date_of_birth

def test_date_of_birth_setter_date():
    test_date_of_birth = dt(1990, 12, 12).date()

    test_account = Account()
    test_account.date_of_birth = test_date_of_birth

    assert type(test_account.date_of_birth) == datetime.date


def test_date_of_birth_setter_datetime():
    test_date_of_birth = dt(1990, 12, 12)

    test_account = Account()
    test_account.date_of_birth = test_date_of_birth

    assert type(test_account.date_of_birth) == datetime.date


def test_date_of_birth_setter_str_yyyy_mm_dd():
    test_date_of_birth = '1990-12-12'

    test_account = Account()
    test_account.date_of_birth = test_date_of_birth

    assert type(test_account.date_of_birth) == datetime.date


def test_date_of_birth_setter_str_dd_mm_yyyy():
    test_date_of_birth = '24-12-1990'

    test_account = Account()

    with pytest.raises(ValueError):
        test_account.date_of_birth = test_date_of_birth


def test_date_of_birth_setter_str_mm_dd_yyyy():
    test_date_of_birth = '12-24-1990'

    test_account = Account()

    with pytest.raises(ValueError):
        test_account.date_of_birth = test_date_of_birth


def test_date_of_birth_setter_str_garbage():
    test_date_of_birth = 'asdf12345!@#$%'

    test_account = Account()

    with pytest.raises(ValueError):
        test_account.date_of_birth = test_date_of_birth


def test_date_of_birth_setter_wrong_type():
    test_date_of_birth = []

    test_account = Account()

    with pytest.raises(TypeError):
        test_account.date_of_birth = test_date_of_birth


# Account.is_admin

def test_is_admin_setter_bool():
    test_is_admin = True

    test_account = Account()
    test_account.is_admin = test_is_admin

    assert test_account.is_admin == test_is_admin


def test_is_admin_setter_none():
    test_is_admin = None

    test_account = Account()
    test_account.is_admin = test_is_admin

    assert test_account.is_admin == test_is_admin


def test_is_admin_setter_str_allowed_string():
    test_is_admin = 'FALSE'

    test_account = Account()
    test_account.is_admin = test_is_admin

    assert test_account.is_admin is False


def test_is_admin_setter_str_invalid_string():
    test_is_admin = 'asdf1234'

    test_account = Account()

    with pytest.raises(ValueError):
        test_account.is_admin = test_is_admin


def test_is_admin_setter_invalid_type():
    test_is_admin = []

    test_account = Account()

    with pytest.raises(TypeError):
        test_account.is_admin = test_is_admin


# Account.init_using_form()

def test_init_using_form_all_attributes():
    test_request_form = {
        'full-name': ['Test Case'],
        'username': ['tester'],
        'date-of-birth': [dt(1990, 12, 12).date()],
        'email': ['tester@test.comm'],
        'contact': ['91234567'],
        'password': ['12345678'],
        'confirm-password': ['12345678'],
    }

    test_account = Account.init_using_form(**test_request_form)

    assert test_account.name == test_request_form['full-name'][0]
    assert test_account.username == test_request_form['username'][0]
    assert test_account.id == test_account.username
    assert test_account.date_of_birth == test_request_form['date-of-birth'][0]
    assert test_account.email == test_request_form['email'][0]
    assert test_account.contact == test_request_form['contact'][0]
    assert test_account.is_admin is None
    assert test_account.password == test_request_form['password'][0]


def test_init_using_form_all_attributes_empty():
    test_request_form = {
        'full-name': [''],
        'username': [''],
        'date-of-birth': [''],
        'email': [''],
        'contact': [''],
        'password': [''],
        'confirm-password': [''],
    }

    test_account = Account.init_using_form(**test_request_form)

    assert test_account.name is None
    assert test_account.username is None
    assert test_account.id == test_account.username
    assert test_account.date_of_birth is None
    assert test_account.email is None
    assert test_account.contact is None
    assert test_account.is_admin is None
    assert test_account.password is None


def test_init_using_form_partial_attributes():
    test_request_form = {
        'username': ['tester'],
        'password': ['12345678'],
    }

    test_account = Account.init_using_form(**test_request_form)

    assert test_account.name is None
    assert test_account.username == test_request_form['username'][0]
    assert test_account.id == test_account.username
    assert test_account.date_of_birth is None
    assert test_account.email is None
    assert test_account.contact is None
    assert test_account.is_admin is None
    assert test_account.password == test_request_form['password'][0]


def test_init_using_form_no_attributes():
    test_request_form = {}

    test_account = Account.init_using_form(**test_request_form)

    assert test_account.name is None
    assert test_account.username is None
    assert test_account.id == test_account.username
    assert test_account.date_of_birth is None
    assert test_account.email is None
    assert test_account.contact is None
    assert test_account.is_admin is None
    assert test_account.password is None


def test_init_using_form_attribute_type_invalid():
    test_request_form = {
        'username': 'tester',
        'contact': 91234567,
    }

    with pytest.raises(TypeError):
        Account.init_using_form(**test_request_form)


# Account.toggle_admin_status()

def test_toggle_admin_status_false_to_true(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = False
    password = generate_password_hash('12345678')

    cursor = mock_db.cursor()
    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{password}', '{is_admin}');",
    )

    test_account = Account(username=username)
    test_account.toggle_admin_status(conn=mock_db)

    cursor.execute(
        f"SELECT is_admin FROM account WHERE username='{username}';",
    )

    assert cursor.fetchone()[0] is True


def test_toggle_admin_status_true_to_false(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = True
    password = generate_password_hash('12345678')

    cursor = mock_db.cursor()
    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{password}', '{is_admin}');",
    )

    test_account = Account(username=username)
    test_account.toggle_admin_status(conn=mock_db)

    cursor.execute(
        f"SELECT is_admin FROM account WHERE username='{username}';",
    )
    assert cursor.fetchone()[0] is False


def test_toggle_admin_status_conn_closed(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = True
    password = generate_password_hash('12345678')

    cursor = mock_db.cursor()
    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{password}', '{is_admin}');",
    )

    test_account = Account(username=username)

    mock_db.close()

    with pytest.raises(psycopg2.InterfaceError):
        test_account.toggle_admin_status(conn=mock_db)


def test_toggle_admin_status_conn_fail(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = True
    password = generate_password_hash('12345678')

    cursor = mock_db.cursor()
    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{password}', '{is_admin}');",
    )

    test_account = Account(username=username)

    # When we don't pass in conn it will attempt to connect to the prod db,
    # this simulates a failed connection.

    with pytest.raises(psycopg2.OperationalError):
        test_account.toggle_admin_status()


def test_toggle_admin_status_conn_none(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = True
    password = generate_password_hash('12345678')

    cursor = mock_db.cursor()
    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{password}', '{is_admin}');",
    )

    test_account = Account(username=username)

    with pytest.raises(AttributeError):
        test_account.toggle_admin_status(conn=None)


# Account.load()

def test_load_valid_username(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = False
    password = generate_password_hash('12345678')

    cursor = mock_db.cursor()
    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{password}', '{is_admin}');",
    )

    test_account = Account.load(username, conn=mock_db)

    assert test_account.name == name
    assert test_account.username == username
    assert test_account.date_of_birth == date_of_birth
    assert test_account.email == email
    assert test_account.contact == contact
    assert test_account.is_admin == is_admin
    assert test_account.password is None


def test_load_none_username(mock_db):
    username = None
    test_account = Account.load(username, conn=mock_db)

    assert test_account is None


def test_load_username_not_found(mock_db):
    username = 'tester1'
    test_account = Account.load(username, conn=mock_db)

    assert test_account is None


def test_load_username_wrong_type(mock_db):
    username = []
    test_account = Account.load(username, conn=mock_db)

    assert test_account is None


def test_load_conn_closed(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = False
    password = generate_password_hash('12345678')

    cursor = mock_db.cursor()
    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{password}', '{is_admin}');",
    )

    mock_db.close()

    with pytest.raises(psycopg2.InterfaceError):
        Account.load(username, conn=mock_db)


def test_load_conn_fail(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = False
    password = generate_password_hash('12345678')

    cursor = mock_db.cursor()
    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{password}', '{is_admin}');",
    )

    mock_db.close()

    # When we don't pass in conn it will attempt to connect to the prod db,
    # this simulates a failed connection.
    with pytest.raises(psycopg2.OperationalError):
        Account.load(username)


def test_load_conn_none(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = False
    password = generate_password_hash('12345678')

    cursor = mock_db.cursor()
    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{password}', '{is_admin}');",
    )

    with pytest.raises(AttributeError):
        Account.load(username, conn=None)


# Account.authenticate()

def test_authenticate_valid_username_valid_password(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = False
    password = '12345678'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{generate_password_hash(password)}', "
        f"'{is_admin}');",
    )

    test_account = Account(username=username, password=password)

    assert test_account.authenticate(conn=mock_db) is True


def test_authenticate_valid_username_invalid_password(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = False
    password = '12345678'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{generate_password_hash(password)}', "
        f"'{is_admin}');",
    )

    test_password = '87654321'
    test_account = Account(username=username, password=test_password)

    assert test_account.authenticate(conn=mock_db) is False


def test_authenticate_invalid_username_valid_password(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = False
    password = '12345678'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{generate_password_hash(password)}', "
        f"'{is_admin}');",
    )

    test_username = 'tester1'
    test_account = Account(username=test_username, password=password)

    assert test_account.authenticate(conn=mock_db) is False


def test_authenticate_invalid_username_invalid_password(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = False
    password = '12345678'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{generate_password_hash(password)}', "
        f"'{is_admin}');",
    )

    test_username = 'tester1'
    test_password = '87654321'
    test_account = Account(username=test_username, password=test_password)

    assert test_account.authenticate(conn=mock_db) is False


def test_authenticate_insufficient_parameters(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = False
    password = '12345678'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{generate_password_hash(password)}', "
        f"'{is_admin}');",
    )

    test_account = Account(username=username)

    with pytest.raises(TypeError):
        test_account.authenticate(conn=mock_db)


def test_authenticate_conn_close(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = False
    password = '12345678'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{generate_password_hash(password)}', "
        f"'{is_admin}');",
    )

    test_account = Account(username=username, password=password)

    mock_db.close()

    with pytest.raises(psycopg2.InterfaceError):
        test_account.authenticate(conn=mock_db)


def test_authenticate_conn_fail(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = False
    password = '12345678'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{generate_password_hash(password)}', "
        f"'{is_admin}');",
    )

    test_account = Account(username=username, password=password)

    # When we don't pass in conn it will attempt to connect to the prod db,
    # this simulates a failed connection.
    with pytest.raises(psycopg2.OperationalError):
        test_account.authenticate()


def test_authenticate_conn_none(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = False
    password = '12345678'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, "
        f"pass, is_admin) VALUES ('{name}', '{username}', '{date_of_birth}', "
        f"'{email}', '{contact}', '{generate_password_hash(password)}', "
        f"'{is_admin}');",
    )

    test_account = Account(username=username, password=password)

    with pytest.raises(AttributeError):
        test_account.authenticate(conn=None)


# Account.save()

def test_save_account_valid(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    password = '12345678'

    account = Account(
        name=name, username=username,
        date_of_birth=date_of_birth, email=email,
        contact=contact, password=password,
    )

    assert account.save(conn=mock_db) is True

    cursor = mock_db.cursor()

    cursor.execute(
        "SELECT name, username, dob, email, contact, is_admin, "
        f"pass FROM account WHERE username='{username}'",
    )

    test_account = cursor.fetchone()

    assert test_account

    test_account_details = {
        'name': test_account[0],
        'username': test_account[1],
        'date_of_birth': test_account[2],
        'email': test_account[3],
        'contact': test_account[4],
        'is_admin': test_account[5],
        'password': test_account[6],
    }

    test_account = Account(**test_account_details)

    assert test_account.name == name
    assert test_account.username == username
    assert test_account.date_of_birth == date_of_birth
    assert test_account.email == email
    assert test_account.contact == contact
    assert check_password_hash(test_account.password, password)


def test_save_account_duplicate(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    password = '12345678'

    account = Account(
        name=name, username=username,
        date_of_birth=date_of_birth, email=email,
        contact=contact, password=password,
    )

    assert account.save(conn=mock_db) is True
    with pytest.raises(psycopg2.IntegrityError):
        account.save(conn=mock_db)


def test_save_account_insufficient_fields(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    contact = '91234567'
    password = '12345678'

    account = Account(
        name=name, username=username,
        date_of_birth=date_of_birth, contact=contact,
        password=password,
    )

    assert account.save(conn=mock_db) is False

    cursor = mock_db.cursor()

    cursor.execute(
        "SELECT name, username, dob, email, contact, is_admin, "
        f"pass FROM account WHERE username='{username}'",
    )

    test_account = cursor.fetchone()

    assert not test_account


def test_save_account_conn_close(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    password = '12345678'

    account = Account(
        name=name, username=username,
        date_of_birth=date_of_birth, email=email,
        contact=contact, password=password,
    )

    mock_db.close()

    with pytest.raises(psycopg2.InterfaceError):
        account.save(conn=mock_db)


def test_save_account_conn_fail(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    password = '12345678'

    account = Account(
        name=name, username=username,
        date_of_birth=date_of_birth, email=email,
        contact=contact, password=password,
    )

    # When we don't pass in conn it will attempt to connect to the prod db,
    # this simulates a failed connection.

    with pytest.raises(psycopg2.OperationalError):
        account.save()


def test_save_account_conn_none(mock_db):
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    email = 'tester@test.com'
    contact = '91234567'
    password = '12345678'

    account = Account(
        name=name, username=username,
        date_of_birth=date_of_birth, email=email,
        contact=contact, password=password,
    )

    with pytest.raises(AttributeError):
        account.save(conn=None)


# Account.__str__

def test_str():
    name = 'Test Case'
    username = 'tester'
    date_of_birth = dt(1990, 12, 12).date()
    is_admin = True
    email = 'tester@test.com'
    contact = '91234567'
    password = '12345678'

    account = Account(
        name=name, username=username,
        date_of_birth=date_of_birth, is_admin=is_admin,
        email=email, contact=contact, password=password,
    )

    test_str = f"""
--------------------------------------------------------------------------------
                               Account
--------------------------------------------------------------------------------
name: {name}
username: {username}
date of birth: {date_of_birth}
email: {email}
contact: {contact}
password: {password}
admin: {is_admin}
--------------------------------------------------------------------------------
"""

    assert account.__str__() == test_str
