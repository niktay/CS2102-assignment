import random
from datetime import date
from random import randint


def generate_account(namelist, surnamelist):
    account_queries = []
    accounts = []

    for name in namelist:
        random_number = randint(1, 101)
        username = f'{name.lower()}{random_number}'
        surname = random.choice(surnamelist)
        contact = randint(80000000, 99999999)
        dob = date(
            randint(1971, 2000),
            randint(1, 12),
            randint(1, 28),
        ).isoformat()

        account_queries.append(
            f'INSERT INTO account(username, is_admin, dob, '
            f"email, contact, pass, name) VALUES('{username}', 'False', "
            f"'{dob}', '{username}@gmail.com', '{contact}', "
            f"'{username}pw', '{name} {surname}');",
        )
        account = {
            'username': username,
            'is_admin': 'False',
            'dob': dob,
            'email': f'{username}@gmail.com',
            'contact': contact,
            'pass': f'{username}pw',
            'name': f'{name} {surname}',
        }
        accounts.append(account)
    with open('output_account_query.sql', 'w') as output_account_query:
        output_account_query.write('\n'.join(account_queries))

    return accounts


def generate_driver(account_dicts):
    driver_queries = []
    drivers = []

    driverlist = random.sample(account_dicts, 50)
    for driver in driverlist:
        username = driver.get('username')
        random_alphabet = random.choice([chr(i) for i in range(65, 91)])
        random_7_digits = randint(8000000, 9099999)
        license_number = f'S{random_7_digits}{random_alphabet}'
        drive_since = date(
            randint(2008, 2018),
            randint(1, 12),
            randint(1, 28),
        ).isoformat()

        driver_queries.append(
            f'INSERT INTO driver(license_number, username, '
            f"driving_since) VALUES('{license_number}', '{username}', "
            f"'{drive_since}');",
        )
        driver = {
            'license_number': license_number,
            'username': username,
            'drive_since': drive_since,
        }
        drivers.append(driver)

    with open('output_driver_query.sql', 'w') as output_driver_query:
        output_driver_query.write('\n'.join(driver_queries))

    return drivers


def generate_data(namelist, surnamelist):
    account_dicts = generate_account(namelist, surnamelist)
    generate_driver(account_dicts)


with open('name_input.txt', 'r') as name_inputfile:
    namelist = name_inputfile.read().splitlines()

with open('surname_input.txt', 'r') as surname_inputfile:
    surnamelist = surname_inputfile.read().splitlines()

if __name__ == '__main__':
    generate_data(namelist, surnamelist)
