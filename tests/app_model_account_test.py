import pytest

from app.model import Account


# Account.__init__()
def test_init_all_parameters():
    test_attributes = {
        'name': 'Test Case',
        'username': 'tester',
        'date_of_birth': '1990-12-12',
        'email': 'tester@test.comm',
        'contact': '91234567',
        'is_admin': 'True',
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
        'date_of_birth': '1990-12-12',
        'email': 'tester@test.comm',
        'contact': '91234567',
        'is_admin': 'True',
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

# Account.init_using_form()


def test_init_using_form_all_attributes():
    test_request_form = {
        'full-name': ['Test Case'],
        'username': ['tester'],
        'date-of-birth': ['1990-12-12'],
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
    date_of_birth = '1990-12-12'
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = 'False'
    password = '12345678'

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
    date_of_birth = '1990-12-12'
    email = 'tester@test.com'
    contact = '91234567'
    is_admin = 'True'
    password = '12345678'

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
