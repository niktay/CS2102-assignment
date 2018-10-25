import random
from datetime import date
from random import randint


def generate_account(username, name, surnamelist):
    surname = random.choice(surnamelist)
    contact = randint(80000000, 99999999)
    dob = date(
        randint(1971, 2000),
        randint(1, 12),
        randint(1, 28),
    ).isoformat()
    with open('output_account_query.sql', 'a+') as output_account_query:
        output_account_query.write(
            f'INSERT INTO account(username, is_admin, dob, email, '
            f"contact, pass, name) VALUES('{username}', 'False', "
            f"'{dob}', '{username}@gmail.com', '{contact}', "
            f"'{username}pw', '{name} {surname}');\n",
        )


def generate_driver(license_number, username):
    drive_since = date(
        randint(2008, 2018),
        randint(1, 12),
        randint(1, 28),
    ).isoformat()
    with open('output_driver_query.sql', 'a+') as output_driver_query:
        output_driver_query.write(
            f'INSERT INTO driver(license_number, username, driving_since) '
            f"VALUES('{license_number}', '{username}', "
            f"'{drive_since}');\n",
        )


def generate_data(namelist, surnamelist):
    for name in namelist:
        random_number = randint(1, 101)
        username = f'{name.lower()}{random_number}'
        random_alphabet = random.choice([chr(i) for i in range(65, 91)])
        random_7_digits = randint(8000000, 9099999)
        license_number = f'S{random_7_digits}{random_alphabet}'
        generate_account(username, name, surnamelist)
        if randint(1, 10) <= 5:
            generate_driver(license_number, username)


with open('name_input.txt', 'r') as name_inputfile:
    namelist = name_inputfile.read().splitlines()

with open('surname_input.txt', 'r') as surname_inputfile:
    surnamelist = surname_inputfile.read().splitlines()

if __name__ == '__main__':
    generate_data(namelist, surnamelist)
