# ZOOOM Car Pooling App
[![Build Status](https://semaphoreci.com/api/v1/projects/8e061085-0cc3-4231-aa8b-7f5b2c60bdaa/2290277/badge.svg)](https://semaphoreci.com/niktay-24/cs2102-assignment) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/dfaa5ebb355a4d0e8239caed877cc255)](https://www.codacy.com?utm_source=github.com&utm_medium=referral&utm_content=niktay/CS2102-assignment&utm_campaign=Badge_Coverage) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/dfaa5ebb355a4d0e8239caed877cc255)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=niktay/CS2102-assignment&amp;utm_campaign=Badge_Grade)

## How to run

1. Install [Docker](https://docs.docker.com/install/), and [docker-compose](https://docs.docker.com/compose/install/#install-compose)
2. Clone repository and enter folder
```
git clone https://github.com/niktay/CS2102-assignment.git
```
4. If volumes folder exists in the director, `rm -r volumes/` to remove previous db records.
5. Run `docker-compose build`
6. Run `docker-compose up` to launch flask server and postgres server.
7. Navigate to `127.0.0.1` in your browser to check if flask is active.

## Usage
The application comes preloaded with an admin account with the following credentials

username: admin
password: 123

Admin interface can be accessed at `http://127.0.0.1/admin`
