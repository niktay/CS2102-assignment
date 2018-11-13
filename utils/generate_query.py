import random
from datetime import date
from random import randint


def generate_account(names, surnames):
    account_queries = []
    accounts = []

    for name in names:
        random_number = randint(1, 101)
        username = f'{name.lower()}{random_number}'
        surname = random.choice(surnames)
        contact = randint(80000000, 99999999)
        dob = date(
            randint(1971, 2000),
            randint(1, 12),
            randint(1, 28),
        ).isoformat()

        account_queries.append(
            f"INSERT INTO account(username, is_admin, dob, "
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


def generate_driver(accounts):
    driver_queries = []
    drivers = []

    driverlist = random.sample(accounts, 50)
    for driver in driverlist:
        username = driver.get('username')
        random_alphabet = random.choice([chr(i) for i in range(65, 91)])
        random_7_digits = random_digits(7)
        license_number = f'S{random_7_digits}{random_alphabet}'
        drive_since = date(
            randint(2008, 2018),
            randint(1, 12),
            randint(1, 28),
        ).isoformat()

        driver_queries.append(
            f"INSERT INTO driver(license_number, username, "
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


def generate_car(drivers, brands, models):
    car_queries = []
    cars = []

    for driver in drivers:
        random_alphabet = random.choice([chr(i) for i in range(65, 91)])
        random_4_digits = random_digits(4)
        license_plate = (
            f'SG{random_alphabet}{random_4_digits}{random_alphabet}'
        )
        brand = random.choice(brands)
        model = random.choice(models)
        license_number = driver.get('license_number', None)

        car_queries.append(
            f"INSERT INTO car(license_plate, brand, model, license_number) "
            f"VALUES('{license_plate}', '{brand}', '{model}', "
            f"'{license_number}');",
        )
        car = {
            'license_plate': license_plate,
            'brand': brand,
            'model': model,
            'license_number': license_number,
        }
        cars.append(car)

    with open('output_car_query.sql', 'w') as output_car_query:
        output_car_query.write('\n'.join(car_queries))

    return cars


def random_digits(number_of_digits):
    range_start = 10**(number_of_digits-1)
    range_end = 10**(number_of_digits)-1
    return randint(range_start, range_end)


def generate_data(**kwargs):
    names = kwargs.get('names', None)
    surnames = kwargs.get('surnames', None)
    accounts = generate_account(names, surnames)

    drivers = generate_driver(accounts)

    brands = kwargs.get('brands', None)
    models = kwargs.get('models', None)
    generate_car(drivers, brands, models)


with open('name_input.txt', 'r') as name_inputfile:
    names = name_inputfile.read().splitlines()

with open('surname_input.txt', 'r') as surname_inputfile:
    surnames = surname_inputfile.read().splitlines()

with open('carbrand_input.txt', 'r') as carbrand_inputfile:
    brands = carbrand_inputfile.read().splitlines()

with open('carmodel_input.txt', 'r') as carmodel_inputfile:
    models = carmodel_inputfile.read().splitlines()


if __name__ == '__main__':
    kwargs = {
        'names': names,
        'surnames': surnames,
        'brands': brands,
        'models': models,
    }

    generate_data(**kwargs)
