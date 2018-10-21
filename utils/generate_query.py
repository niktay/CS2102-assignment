from random import randint


def generate_account(namelist, surnamelist):
    for name in namelist:
        for x in range(1):
            random_surname = randint(0, 19)
            random_number = randint(1, 101)
            random_year = randint(1971, 2000)
            random_month = randint(1, 13)
            random_day = randint(1, 30)
            random_contact = randint(80000000, 99999999)
        surname = ''.join(surnamelist[random_surname])
        username = name.lower() + str(random_number)
        year = str(random_year)
        if random_month < 10:
            month = '0' + str(random_month)
        else:
            month = str(random_month)
        if random_day < 10:
            day = '0' + str(random_day)
        else:
            day = str(random_day)
        dob = year + '-' + month + '-' + day
        contact = str(random_contact)
        print(
            f'INSERT INTO account(username, is_admin, dob, email, '
            f"contact, pass, name) VALUES('{username}', 'False', "
            f"'{dob}', '{username}@gmail.com', '{contact}', "
            f"'{username}pw', '{name} {surname}');",
        )
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
