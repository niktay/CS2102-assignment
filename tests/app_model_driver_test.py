import datetime
from datetime import datetime as dt

import psycopg2
import pytest
from werkzeug.security import generate_password_hash

from app.model import Driver


# Driver.__init__()

def test_init_all_parameters():
    test_attributes = {
        'license_number': 'S1234567A',
        'username': 'tester',
        'driving_since': dt(1990, 12, 12).date(),
        'optional_bio': 'asdf',
    }

    test_driver = Driver(**test_attributes)

    assert test_driver.license_number == test_attributes['license_number']
    assert test_driver.username == test_attributes['username']
    assert test_driver.driving_since == test_attributes['driving_since']
    assert test_driver.optional_bio == test_attributes['optional_bio']


def test_init_without_bio():
    test_attributes = {
        'license_number': 'S1234567A',
        'username': 'tester',
        'driving_since': dt(1990, 12, 12).date(),
    }

    test_driver = Driver(**test_attributes)

    assert test_driver.license_number == test_attributes['license_number']
    assert test_driver.username == test_attributes['username']
    assert test_driver.driving_since == test_attributes['driving_since']
    assert test_driver.optional_bio is None


# Driver.driving_since

def test_driving_since_setter_date():
    test_driving_since = dt(1990, 12, 12).date()

    test_driver = Driver()
    test_driver.driving_since = test_driving_since

    assert type(test_driver.driving_since) == datetime.date


def test_driving_since_setter_datetime():
    test_driving_since = dt(1990, 12, 12)

    test_driver = Driver()
    test_driver.driving_since = test_driving_since

    assert type(test_driver.driving_since) == datetime.date


def test_driving_since_setter_str_yyyy_mm_dd():
    test_driving_since = '1990-12-12'

    test_driver = Driver()
    test_driver.driving_since = test_driving_since

    assert type(test_driver.driving_since) == datetime.date


def test_driving_since_setter_str_dd_mm_yyyy():
    test_driving_since = '24-12-1990'

    test_driver = Driver()

    with pytest.raises(ValueError):
        test_driver.driving_since = test_driving_since


def test_driving_since_setter_str_mm_dd_yyyy():
    test_driving_since = '12-24-1990'

    test_driver = Driver()

    with pytest.raises(ValueError):
        test_driver.driving_since = test_driving_since


def test_driving_since_setter_str_garbage():
    test_driving_since = 'asdf12345!@#$%'

    test_driver = Driver()

    with pytest.raises(ValueError):
        test_driver.driving_since = test_driving_since


def test_driving_since_setter_wrong_type():
    test_driving_since = []

    test_driver = Driver()

    with pytest.raises(TypeError):
        test_driver.driving_since = test_driving_since


# Driver.init_using_form()

def test_init_using_form_all_attributes():
    test_request_form = {
        'license-number': ['S1234567A'],
        'username': ['tester'],
        'driving-since': [dt(1990, 12, 12).date()],
        'optional-bio': ['asdf'],
    }

    test_driver = Driver.init_using_form(**test_request_form)

    assert test_driver.license_number == test_request_form['license-number'][0]
    assert test_driver.username == test_request_form['username'][0]
    assert test_driver.driving_since == test_request_form['driving-since'][0]
    assert test_driver.optional_bio == test_request_form['optional-bio'][0]


def test_init_using_form_all_attributes_empty():
    test_request_form = {
        'license-number': [''],
        'username': [''],
        'driving-since': [''],
        'optional-bio': [''],
    }

    test_driver = Driver.init_using_form(**test_request_form)

    assert test_driver.license_number is None
    assert test_driver.username is None
    assert test_driver.driving_since is None
    assert test_driver.optional_bio is None


def test_init_using_form_partial_attributes():
    test_request_form = {
        'username': ['tester'],
        'optional-bio': ['asdf'],
    }

    test_driver = Driver.init_using_form(**test_request_form)

    assert test_driver.license_number is None
    assert test_driver.username == test_request_form['username'][0]
    assert test_driver.driving_since is None
    assert test_driver.optional_bio == test_request_form['optional-bio'][0]


def test_init_using_form_no_attributes():
    test_request_form = {}

    test_driver = Driver.init_using_form(**test_request_form)

    assert test_driver.license_number is None
    assert test_driver.username is None
    assert test_driver.driving_since is None
    assert test_driver.optional_bio is None


def test_init_using_form_attribute_type_invalid():
    test_request_form = {
        'license-number': 123456789,
        'username': 'tester',
    }

    with pytest.raises(TypeError):
        Driver.init_using_form(**test_request_form)


# Driver.save()

def test_save_driver_valid(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    driver = Driver(
        license_number=license_number, username=username,
        driving_since=driving_since, optional_bio=optional_bio,
    )

    assert driver.save(conn=mock_db) is True

    cursor.execute(
        "SELECT license_number, username, driving_since, optional_bio FROM "
        f"driver WHERE license_number='{license_number}';",
    )

    test_driver = cursor.fetchone()

    assert test_driver

    test_driver_details = {
        'license_number': test_driver[0],
        'username': test_driver[1],
        'driving_since': test_driver[2],
        'optional_bio': test_driver[3],
    }

    test_driver = Driver(**test_driver_details)

    assert test_driver.license_number == license_number
    assert test_driver.username == username
    assert test_driver.driving_since == driving_since
    assert test_driver.optional_bio == optional_bio


def test_save_driver_invalid_username(mock_db):
    username = 'tester'
    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    driver = Driver(
        license_number=license_number, username=username,
        driving_since=driving_since, optional_bio=optional_bio,
    )

    with pytest.raises(psycopg2.IntegrityError):
        driver.save(conn=mock_db)


def test_save_driver_duplicate(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    driver = Driver(
        license_number=license_number, username=username,
        driving_since=driving_since, optional_bio=optional_bio,
    )

    assert driver.save(conn=mock_db) is True

    with pytest.raises(psycopg2.IntegrityError):
        driver.save(conn=mock_db)


def test_save_driver_insufficient_fields(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    driver = Driver(
        username=username, driving_since=driving_since,
        optional_bio=optional_bio,
    )

    assert driver.save(conn=mock_db) is False

    cursor.execute(
        "SELECT license_number, username, driving_since, optional_bio FROM "
        f"driver WHERE license_number='{license_number}';",
    )

    test_driver = cursor.fetchone()

    assert not test_driver


def test_save_driver_conn_close(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    driver = Driver(
        license_number=license_number, username=username,
        driving_since=driving_since, optional_bio=optional_bio,
    )

    mock_db.close()

    with pytest.raises(psycopg2.InterfaceError):
        driver.save(conn=mock_db)


def test_save_driver_conn_fail(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    driver = Driver(
        license_number=license_number, username=username,
        driving_since=driving_since, optional_bio=optional_bio,
    )

    # When we don't pass in conn it will attempt to connect to the prod db,
    # this simulates a failed connection.

    with pytest.raises(psycopg2.OperationalError):
        driver.save()


def test_save_driver_conn_none(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    driver = Driver(
        license_number=license_number, username=username,
        driving_since=driving_since, optional_bio=optional_bio,
    )

    with pytest.raises(AttributeError):
        driver.save(conn=None)


# Driver.update_bio()

def test_update_bio_valid(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    cursor.execute(
        "INSERT INTO driver (license_number, username, driving_since, "
        f"optional_bio) VALUES ('{license_number}', '{username}', "
        f"'{driving_since}', '{optional_bio}'); ",
    )

    new_bio = 'ghij'
    test_driver = Driver(
        license_number=license_number, username=username,
        driving_since=driving_since,
        optional_bio=new_bio,
    )

    assert test_driver.update_bio(conn=mock_db) is True

    cursor.execute(
        "SELECT optional_bio FROM driver WHERE "
        f"license_number='{license_number}';",
    )

    test_new_bio = cursor.fetchone()

    assert test_new_bio[0] == new_bio


def test_update_bio_conn_closed(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    cursor.execute(
        "INSERT INTO driver (license_number, username, driving_since, "
        f"optional_bio) VALUES ('{license_number}', '{username}', "
        f"'{driving_since}', '{optional_bio}'); ",
    )

    new_bio = 'ghij'
    test_driver = Driver(
        license_number=license_number, username=username,
        driving_since=driving_since,
        optional_bio=new_bio,
    )

    mock_db.close()

    with pytest.raises(psycopg2.InterfaceError):
        test_driver.update_bio(conn=mock_db)


def test_update_bio_conn_fail(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    cursor.execute(
        "INSERT INTO driver (license_number, username, driving_since, "
        f"optional_bio) VALUES ('{license_number}', '{username}', "
        f"'{driving_since}', '{optional_bio}'); ",
    )

    new_bio = 'ghij'
    test_driver = Driver(
        license_number=license_number, username=username,
        driving_since=driving_since,
        optional_bio=new_bio,
    )

    # When we don't pass in conn it will attempt to connect to the prod db,
    # this simulates a failed connection.

    with pytest.raises(psycopg2.OperationalError):
        test_driver.update_bio()


def test_update_bio_conn_none(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    cursor.execute(
        "INSERT INTO driver (license_number, username, driving_since, "
        f"optional_bio) VALUES ('{license_number}', '{username}', "
        f"'{driving_since}', '{optional_bio}'); ",
    )

    new_bio = 'ghij'
    test_driver = Driver(
        license_number=license_number, username=username,
        driving_since=driving_since,
        optional_bio=new_bio,
    )

    with pytest.raises(AttributeError):
        test_driver.update_bio(conn=None)


# Driver.load()

def test_load_valid_username(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    cursor.execute(
        "INSERT INTO driver (license_number, username, driving_since, "
        f"optional_bio) VALUES ('{license_number}', '{username}', "
        f"'{driving_since}', '{optional_bio}'); ",
    )

    test_driver = Driver.load(username=username, conn=mock_db)

    assert test_driver.license_number == license_number
    assert test_driver.username == username
    assert test_driver.driving_since == driving_since
    assert test_driver.optional_bio == optional_bio


def test_load_valid_license_number(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    cursor.execute(
        "INSERT INTO driver (license_number, username, driving_since, "
        f"optional_bio) VALUES ('{license_number}', '{username}', "
        f"'{driving_since}', '{optional_bio}'); ",
    )

    test_driver = Driver.load(license_number=license_number, conn=mock_db)

    assert test_driver.license_number == license_number
    assert test_driver.username == username
    assert test_driver.driving_since == driving_since
    assert test_driver.optional_bio == optional_bio


def test_load_no_parameters(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    cursor.execute(
        "INSERT INTO driver (license_number, username, driving_since, "
        f"optional_bio) VALUES ('{license_number}', '{username}', "
        f"'{driving_since}', '{optional_bio}'); ",
    )

    assert Driver.load(conn=mock_db) is None


def test_load_license_number_and_username(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    cursor.execute(
        "INSERT INTO driver (license_number, username, driving_since, "
        f"optional_bio) VALUES ('{license_number}', '{username}', "
        f"'{driving_since}', '{optional_bio}'); ",
    )

    assert(
        Driver.load(
            license_number=license_number, username=username,
            conn=mock_db,
        ) is None
    )


def test_load_invalid_driver(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    cursor.execute(
        "INSERT INTO driver (license_number, username, driving_since, "
        f"optional_bio) VALUES ('{license_number}', '{username}', "
        f"'{driving_since}', '{optional_bio}'); ",
    )

    assert Driver.load(license_number='asdf', conn=mock_db) is None


def test_load_conn_closed(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    cursor.execute(
        "INSERT INTO driver (license_number, username, driving_since, "
        f"optional_bio) VALUES ('{license_number}', '{username}', "
        f"'{driving_since}', '{optional_bio}'); ",
    )

    mock_db.close()

    with pytest.raises(psycopg2.InterfaceError):
        Driver.load(license_number=license_number, conn=mock_db)


def test_load_conn_fail(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    cursor.execute(
        "INSERT INTO driver (license_number, username, driving_since, "
        f"optional_bio) VALUES ('{license_number}', '{username}', "
        f"'{driving_since}', '{optional_bio}'); ",
    )

    # When we don't pass in conn it will attempt to connect to the prod db,
    # this simulates a failed connection.

    with pytest.raises(psycopg2.OperationalError):
        Driver.load(license_number=license_number)


def test_load_conn_none(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False

    license_number = 'S1234567A'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    cursor.execute(
        "INSERT INTO driver (license_number, username, driving_since, "
        f"optional_bio) VALUES ('{license_number}', '{username}', "
        f"'{driving_since}', '{optional_bio}'); ",
    )

    with pytest.raises(AttributeError):
        Driver.load(license_number=license_number, conn=None)


# Driver.__str__

def test_str():
    license_number = 'S1234567A'
    username = 'tester'
    driving_since = dt(1990, 12, 12).date()
    optional_bio = 'asdf'

    driver = Driver(
        license_number=license_number, username=username,
        driving_since=driving_since, optional_bio=optional_bio,
    )

    test_str = f"""
--------------------------------------------------------------------------------
                               Driver
--------------------------------------------------------------------------------
license_number: {license_number}
username: {username}
driving_since: {driving_since}
optional_bio: {optional_bio}
--------------------------------------------------------------------------------
"""
    assert driver.__str__() == test_str
