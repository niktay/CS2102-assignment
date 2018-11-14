import random
from datetime import date
from datetime import time
from operator import itemgetter
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


def generate_advertisement(drivers, towns):
    advertisement_queries = []
    advertisements = []

    for driver in drivers:
        ad_date = date(
            2018,
            randint(1, 12),
            randint(1, 28),
        ).isoformat()
        ad_time = time(
            randint(0, 23),
            randint(0, 59),
            randint(0, 59),
            0,
        ).isoformat()
        start_timestamp = f'{ad_date} {ad_time}'

        license_number = driver.get('license_number', None)

        origin_town = random.choice(towns)
        destination_town = random.choice(towns)
        while origin_town == destination_town:
            destination_town = random.choice(towns)

        origin = random_address(origin_town)
        destination = random_address(destination_town)

        active = random.choice(['True', 'False'])

        advertisement_queries.append(
            f"INSERT INTO advertisement(start_timestamp, license_number, "
            f"origin, destination, active) VALUES('{start_timestamp}', "
            f"'{license_number}', '{origin}', '{destination}', '{active}');",
        )
        advertisement = {
            'start_timestamp': start_timestamp,
            'license_number': license_number,
            'origin': origin,
            'destination': destination,
            'active': active,
        }
        advertisements.append(advertisement)

    with open('output_ad_query.sql', 'w') as output_ad_query:
        output_ad_query.write('\n'.join(advertisement_queries))

    return advertisements


def generate_bid(accounts, advertisements):
    bid_queries = []
    bids = []
    counter = 1

    active_ad = [d for d in advertisements if d['active'] == 'True']

    sorted_active_ad = sorted(active_ad, key=itemgetter('start_timestamp'))

    for ad in sorted_active_ad:
        price = random_digits(2)
        account = random.choice(accounts)
        username = account.get('username', None)
        start_timestamp = ad.get('start_timestamp', None)
        license_number = ad.get('license_number', None)

        bid_queries.append(
            f"INSERT INTO bid(bid_id, price, username, start_timestamp, "
            f"license_number) VALUES('{counter}', '{price}', '{username}', "
            f"'{start_timestamp}', '{license_number}');",
        )
        bid = {
            'bid_id': counter,
            'price': price,
            'username': username,
            'start_timestamp': start_timestamp,
            'license_number': license_number,
        }
        bids.append(bid)
        counter = counter + 1

    with open('output_bid_query.sql', 'w') as output_bid_query:
        output_bid_query.write('\n'.join(bid_queries))

    return bids


def generate_ride(bids):
    ride_queries = []
    rides = []

    for bid in bids:
        bid_id = bid.get('bid_id', None)
        confirmed_timestamp = bid.get('start_timestamp', None)

        ride_queries.append(
            f"INSERT INTO ride(bid_id, confirmed_timestamp) VALUES"
            f"('{bid_id}', '{confirmed_timestamp}');",
        )
        ride = {
            'bid_id': bid_id,
            'confirmed_timestamp': confirmed_timestamp,
        }
        rides.append(ride)

    with open('output_ride_query.sql', 'w') as output_ride_query:
        output_ride_query.write('\n'.join(ride_queries))

    return rides


def random_digits(number_of_digits):
    range_start = 10**(number_of_digits-1)
    range_end = 10**(number_of_digits)-1
    return randint(range_start, range_end)


def random_address(town):
    street_suffix = ['Street', 'Avenue', 'Drive']
    random_3_digits = random_digits(3)
    random_2_digits = random_digits(2)
    random_street_suffix = random.choice(street_suffix)

    address = (
        f'Block {random_3_digits} {town} '
        f'{random_street_suffix} {random_2_digits}'
    )
    return address


def generate_data(**kwargs):
    names = kwargs.get('names', None)
    surnames = kwargs.get('surnames', None)
    accounts = generate_account(names, surnames)

    drivers = generate_driver(accounts)

    brands = kwargs.get('brands', None)
    models = kwargs.get('models', None)
    generate_car(drivers, brands, models)

    towns = kwargs.get('towns', None)
    advertisements = generate_advertisement(drivers, towns)

    bids = generate_bid(accounts, advertisements)

    generate_ride(bids)


with open('name_input.txt', 'r') as name_inputfile:
    names = name_inputfile.read().splitlines()

with open('surname_input.txt', 'r') as surname_inputfile:
    surnames = surname_inputfile.read().splitlines()

with open('carbrand_input.txt', 'r') as carbrand_inputfile:
    brands = carbrand_inputfile.read().splitlines()

with open('carmodel_input.txt', 'r') as carmodel_inputfile:
    models = carmodel_inputfile.read().splitlines()

with open('town_input.txt', 'r') as town_inputfile:
    towns = town_inputfile.read().splitlines()


if __name__ == '__main__':
    kwargs = {
        'names': names,
        'surnames': surnames,
        'brands': brands,
        'models': models,
        'towns': towns,
    }

    generate_data(**kwargs)
