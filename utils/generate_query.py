import random
from datetime import date
from random import randint


def generate_account(namelist, surnamelist):
    for name in namelist:
        surname = random.choice(surnamelist)
        random_number = randint(1, 101)
        contact = randint(80000000, 99999999)
        username = f'{name.lower()}{random_number}'
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


with open('name_input.txt', 'r') as name_inputfile:
    namelist = name_inputfile.read().splitlines()

with open('surname_input.txt', 'r') as surname_inputfile:
    surnamelist = surname_inputfile.read().splitlines()

if __name__ == '__main__':
    generate_account(namelist, surnamelist)
