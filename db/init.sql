CREATE TABLE account
(
username VARCHAR(64) NOT NULL,
is_admin BOOLEAN NOT NULL,
dob DATE NOT NULL,
email VARCHAR(320) NOT NULL,
contact VARCHAR(15) NOT NULL,
pass VARCHAR(255) NOT NULL,
name VARCHAR(255) NOT NULL,
PRIMARY KEY (username),
CONSTRAINT username_not_empty CHECK(LENGTH(username) > 0)
);

CREATE TABLE driver
(
license_number VARCHAR(64) NOT NULL,
username VARCHAR(64) NOT NULL UNIQUE,
driving_since DATE NOT NULL,
PRIMARY KEY (license_number),
FOREIGN KEY (username) REFERENCES account (username)
);

CREATE TABLE advertisement
(
start_timestamp TIMESTAMP NOT NULL,
license_number VARCHAR(64) NOT NULL,
origin VARCHAR(255) NOT NULL,
destination VARCHAR(255) NOT NULL,
PRIMARY KEY (start_timestamp, license_number),
FOREIGN KEY (license_number) REFERENCES driver (license_number),
CONSTRAINT origin_destination_different CHECK (origin != destination)
);

CREATE TABLE car
(
license_plate VARCHAR(10) NOT NULL,
brand VARCHAR(64) NOT NULL,
model VARCHAR(64) NOT NULL,
license_number VARCHAR(64) NOT NULL,
PRIMARY KEY (license_plate),
FOREIGN KEY (license_number) REFERENCES driver (license_number)
);

CREATE TABLE bid
(
bid_id INTEGER NOT NULL,
price DECIMAL(19,4) NOT NULL,
username VARCHAR(64) NOT NULL,
start_timestamp TIMESTAMP NOT NULL,
license_number VARCHAR(64) NOT NULL,
PRIMARY KEY (bid_id),
FOREIGN KEY (username) REFERENCES account (username),
FOREIGN KEY (start_timestamp, license_number) REFERENCES advertisement
(start_timestamp, license_number),
CONSTRAINT price_not_negative CHECK (price > 0)
);

CREATE TABLE ride
(
bid_id INTEGER NOT NULL,
confirmed_timestamp TIMESTAMP NOT NULL,
PRIMARY KEY (bid_id, confirmed_timestamp),
FOREIGN KEY (bid_id) REFERENCES bid (bid_id)
);
