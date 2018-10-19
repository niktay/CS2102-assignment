from random import randint


def generate_account(namelist):
    i = 0
    with open("output_account_query.sql", "w") as output_account_query:
        while i < len(namelist):
            name = ("".join(namelist[i])).title()
            surnamelist = [
                "Smith", "Hill", "Lee", "Brown", "Taylor", "Jones", "Wood",
                "White", "Fox", "Gray", "Hunt", "Bell", "Scott", "Cook",
                "Owen", "Ross", "West", "Lane", "Green", "Shaw",
            ]
            for x in range(1):
                random_surname = randint(0, 19)
                random_number = randint(1, 101)
                random_year = randint(1971, 2000)
                random_month = randint(1, 13)
                random_day = randint(1, 30)
                random_contact = randint(80000000, 99999999)
            surname = "".join(surnamelist[random_surname])
            username = name.lower() + str(random_number)
            year = str(random_year)
            if random_month < 10:
                month = "0" + str(random_month)
            else:
                month = str(random_month)
            if random_day < 10:
                day = "0" + str(random_day)
            else:
                day = str(random_day)
            dob = year + "-" + month + "-" + day
            contact = str(random_contact)
            print(
                "INSERT INTO account(username, is_admin, dob, email, "
                + "contact, pass, name) VALUES('" +
                username + "', 'False', '"
                + dob + "', '" + username + "@gmail.com', '" + contact
                + "', '" + username + "pw', '" + name + " " + surname + "');",
            )
            output_account_query.write(
                "INSERT INTO account(username, "
                + "is_admin, dob, email, contact, pass, name) VALUES('"
                + username + "', 'False', '" + dob + "', '" + username
                + "@gmail.com', '" + contact + "', '" + username + "pw', '"
                + name + " " + surname + "');\n",
            )
            i += 1


with open('name_input.txt', 'r') as inputfile:
    namelist = inputfile.read().splitlines()

generate_account(namelist)
