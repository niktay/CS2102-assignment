from datetime import datetime as dt

import psycopg2
import pytest
from werkzeug.security import generate_password_hash

from app.model import Car


# Car.__init__()

def test_init_all_parameters():
    test_attributes = {
        'license_number': 'S1234567A',
        'license_plate': 'SKV6201B',
        'brand': 'Toyota',
        'model': 'Camry',
    }

    test_car = Car(**test_attributes)

    assert test_car.license_number == test_attributes['license_number']
    assert test_car.license_plate == test_attributes['license_plate']
    assert test_car.brand == test_attributes['brand']
    assert test_car.model == test_attributes['model']


def test_init_no_parameters():
    test_attributes = {}

    test_car = Car(**test_attributes)

    assert test_car.license_number is None
    assert test_car.license_plate is None
    assert test_car.brand is None
    assert test_car.model is None


# Car.init_using_form()

def test_init_using_form_all_attributes():
    test_request_form = {
        'license-number': ['S1234567A'],
        'license-plate': ['SKV6201B'],
        'brand': ['Toyota'],
        'model': ['Camry'],
    }

    test_car = Car.init_using_form(**test_request_form)

    assert test_car.license_number == test_request_form['license-number'][0]
    assert test_car.license_plate == test_request_form['license-plate'][0]
    assert test_car.brand == test_request_form['brand'][0]
    assert test_car.model == test_request_form['model'][0]


def test_init_using_form_partial_attributes():
    test_request_form = {
        'license-number': ['S1234567A'],
        'license-plate': ['SKV6201B'],
    }

    test_car = Car.init_using_form(**test_request_form)

    assert test_car.license_number == test_request_form['license-number'][0]
    assert test_car.license_plate == test_request_form['license-plate'][0]
    assert test_car.brand is None
    assert test_car.model is None


def test_init_using_form_no_attributes():
    test_request_form = {
        'license-number': [''],
        'license-plate': [''],
        'brand': [''],
        'model': [''],
    }

    test_car = Car.init_using_form(**test_request_form)

    assert test_car.license_number is None
    assert test_car.license_plate is None
    assert test_car.brand is None
    assert test_car.model is None


def test_init_using_form_attribute_type_invalid():
    test_request_form = {
        'license-number': 123456789,
        'license-plate': 'SKV6201B',
    }

    with pytest.raises(TypeError):
        Car.init_using_form(**test_request_form)


# Car.save()

def test_save_car_valid(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    car = Car(
        license_plate=license_plate, license_number=license_number,
        brand=brand, model=model,
    )

    assert car.save(conn=mock_db) is True

    cursor.execute(
        "SELECT license_plate, license_number, brand, model FROM car WHERE "
        f"license_plate='{license_plate}';",
    )

    test_car = cursor.fetchone()

    assert test_car

    test_car_details = {
        'license_plate': test_car[0],
        'license_number': test_car[1],
        'brand': test_car[2],
        'model': test_car[3],
    }

    test_car = Car(**test_car_details)

    assert test_car.license_plate == license_plate
    assert test_car.license_number == license_number
    assert test_car.brand == brand
    assert test_car.model == model


def test_save_car_invalid_license_plate(mock_db):
    name = 'Test Case'
    username = 'tester'
    dob = dt(1990, 12, 12).date()
    email = 'tester@gmail.com'
    contact = '12345678'
    password = '12345678'
    is_admin = False
    license_number = 'S1234567A'

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

    cursor = mock_db.cursor()

    cursor.execute(
        "INSERT INTO account (name, username, dob, email, contact, pass, "
        f"is_admin) VALUES ('{name}', '{username}', '{dob}', '{email}', "
        f"'{contact}', '{generate_password_hash(password)}', '{is_admin}'); ",
    )

    car = Car(
        license_plate=license_plate, license_number=license_number,
        brand=brand, model=model,
    )

    with pytest.raises(psycopg2.IntegrityError):
        car.save(conn=mock_db)


def test_save_car_duplicate(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    car = Car(
        license_plate=license_plate, license_number=license_number,
        brand=brand, model=model,
    )

    assert car.save(conn=mock_db) is True

    with pytest.raises(psycopg2.IntegrityError):
        car.save(conn=mock_db)


def test_save_car_insufficient_fields(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    car = Car(license_number=license_number, brand=brand, model=model)

    assert car.save(conn=mock_db) is False

    cursor.execute(
        "SELECT license_plate, license_number, brand, model FROM car WHERE "
        f"license_plate='{license_plate}';",
    )

    test_car = cursor.fetchone()

    assert not test_car


def test_save_car_conn_close(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    car = Car(
        license_plate=license_plate, license_number=license_number,
        brand=brand, model=model,
    )

    mock_db.close()
    with pytest.raises(psycopg2.InterfaceError):
        car.save(conn=mock_db)


def test_save_car_conn_fail(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    car = Car(
        license_plate=license_plate, license_number=license_number,
        brand=brand, model=model,
    )

    # When we don't pass in conn it will attempt to connect to the prod db,
    # this simulates a failed connection.

    with pytest.raises(psycopg2.OperationalError):
        car.save()


def test_save_car_conn_none(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    car = Car(
        license_plate=license_plate, license_number=license_number,
        brand=brand, model=model,
    )

    with pytest.raises(AttributeError):
        car.save(conn=None)


# Car.update()

def test_update_valid(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    cursor.execute(
        "INSERT INTO car (license_plate, license_number, brand, model) VALUES "
        f"('{license_plate}', '{license_number}', '{brand}', '{model}');",
    )

    new_brand = 'Cherry'
    new_model = 'QQ'

    new_car = Car(
        license_plate=license_plate,
        license_number=license_number, brand=new_brand,
        model=new_model,
    )

    assert new_car.update(conn=mock_db) is True

    cursor.execute(
        "SELECT license_plate, license_number, brand, model FROM car WHERE "
        f"license_plate='{license_plate}';",
    )

    test_car = cursor.fetchone()

    assert test_car

    test_car_details = {
        'license_plate': test_car[0],
        'license_number': test_car[1],
        'brand': test_car[2],
        'model': test_car[3],
    }

    test_car = Car(**test_car_details)

    assert test_car.license_plate == license_plate
    assert test_car.license_number == license_number
    assert test_car.brand == new_brand
    assert test_car.model == new_model


def test_update_invalid_license_plate(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    cursor.execute(
        "INSERT INTO car (license_plate, license_number, brand, model) VALUES "
        f"('{license_plate}', '{license_number}', '{brand}', '{model}');",
    )

    new_brand = 'Cherry'
    new_model = 'QQ'

    new_car = Car(
        license_plate='asdf',
        license_number=license_number, brand=new_brand,
        model=new_model,
    )

    assert new_car.update(conn=mock_db) is False


def test_update_conn_closed(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    cursor.execute(
        "INSERT INTO car (license_plate, license_number, brand, model) VALUES "
        f"('{license_plate}', '{license_number}', '{brand}', '{model}');",
    )

    new_brand = 'Cherry'
    new_model = 'QQ'

    new_car = Car(
        license_plate=license_plate,
        license_number=license_number, brand=new_brand,
        model=new_model,
    )

    mock_db.close()

    with pytest.raises(psycopg2.InterfaceError):
        new_car.update(conn=mock_db)


def test_update_conn_fail(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    cursor.execute(
        "INSERT INTO car (license_plate, license_number, brand, model) VALUES "
        f"('{license_plate}', '{license_number}', '{brand}', '{model}');",
    )

    new_brand = 'Cherry'
    new_model = 'QQ'

    new_car = Car(
        license_plate=license_plate,
        license_number=license_number, brand=new_brand,
        model=new_model,
    )

    # When we don't pass in conn it will attempt to connect to the prod db,
    # this simulates a failed connection.

    with pytest.raises(psycopg2.OperationalError):
        new_car.update()


def test_update_conn_none(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    cursor.execute(
        "INSERT INTO car (license_plate, license_number, brand, model) VALUES "
        f"('{license_plate}', '{license_number}', '{brand}', '{model}');",
    )

    new_brand = 'Cherry'
    new_model = 'QQ'

    new_car = Car(
        license_plate=license_plate,
        license_number=license_number, brand=new_brand,
        model=new_model,
    )

    with pytest.raises(AttributeError):
        new_car.update(conn=None)


# Car.load()
def test_load_valid_license_plate(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    cursor.execute(
        "INSERT INTO car (license_plate, license_number, brand, model) VALUES "
        f"('{license_plate}', '{license_number}', '{brand}', '{model}');",
    )

    test_car = Car.load(license_plate=license_plate, conn=mock_db)

    assert test_car.license_plate == license_plate
    assert test_car.license_number == license_number
    assert test_car.brand == brand
    assert test_car.model == model


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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    cursor.execute(
        "INSERT INTO car (license_plate, license_number, brand, model) VALUES "
        f"('{license_plate}', '{license_number}', '{brand}', '{model}');",
    )

    test_car = Car.load(license_number=license_number, conn=mock_db)

    assert test_car.license_plate == license_plate
    assert test_car.license_number == license_number
    assert test_car.brand == brand
    assert test_car.model == model


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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    cursor.execute(
        "INSERT INTO car (license_plate, license_number, brand, model) VALUES "
        f"('{license_plate}', '{license_number}', '{brand}', '{model}');",
    )

    assert Car.load(conn=mock_db) is None


def test_load_license_number_and_license_plate(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    cursor.execute(
        "INSERT INTO car (license_plate, license_number, brand, model) VALUES "
        f"('{license_plate}', '{license_number}', '{brand}', '{model}');",
    )

    assert(
        Car.load(
            license_plate=license_plate,
            license_number=license_number, conn=mock_db,
        ) is None
    )


def test_load_invalid_car(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    cursor.execute(
        "INSERT INTO car (license_plate, license_number, brand, model) VALUES "
        f"('{license_plate}', '{license_number}', '{brand}', '{model}');",
    )

    assert Car.load(license_plate='asdf', conn=mock_db) is None


def test_load_conn_close(mock_db):
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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    cursor.execute(
        "INSERT INTO car (license_plate, license_number, brand, model) VALUES "
        f"('{license_plate}', '{license_number}', '{brand}', '{model}');",
    )

    mock_db.close()

    with pytest.raises(psycopg2.InterfaceError):
        Car.load(license_plate=license_plate, conn=mock_db) is None


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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    cursor.execute(
        "INSERT INTO car (license_plate, license_number, brand, model) VALUES "
        f"('{license_plate}', '{license_number}', '{brand}', '{model}');",
    )

    # When we don't pass in conn it will attempt to connect to the prod db,
    # this simulates a failed connection.

    with pytest.raises(psycopg2.OperationalError):
        Car.load(license_plate=license_plate) is None


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

    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

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

    cursor.execute(
        "INSERT INTO car (license_plate, license_number, brand, model) VALUES "
        f"('{license_plate}', '{license_number}', '{brand}', '{model}');",
    )

    with pytest.raises(AttributeError):
        Car.load(license_plate=license_plate, conn=None) is None


# Car.__str__

def test_str():
    license_number = 'S1234567A'
    license_plate = 'SKV6201B'
    brand = 'Toyota'
    model = 'Camry'

    car = Car(
        license_plate=license_plate, license_number=license_number,
        brand=brand, model=model,
    )

    test_str = f"""
--------------------------------------------------------------------------------
                               Car
--------------------------------------------------------------------------------
license_plate: {license_plate}
license_number: {license_number}
brand: {brand}
model: {model}
--------------------------------------------------------------------------------
"""
    assert car.__str__() == test_str
