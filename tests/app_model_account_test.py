from app.model import Account


def test_init_valid_kwargs():
    test_request_form = {
        'full-name': ['Test Case'],
        'username': ['tester'],
        'date-of-birth': ['1990-12-12'],
        'email': ['tester@test.comm'],
        'contact': ['91234567'],
        'password': ['12345678'],
        'confirm-password': ['12345678'],
    }

    test_account = Account(**test_request_form)

    assert test_account.name == test_request_form['full-name'][0]
    assert test_account.username == test_request_form['username'][0]
    assert test_account.date_of_birth == test_request_form['date-of-birth'][0]
    assert test_account.email == test_request_form['email'][0]
    assert test_account.contact == test_request_form['contact'][0]
    assert test_account.password == test_request_form['password'][0]
    assert(test_account.confirm_password ==
           test_request_form['confirm-password'][0])
