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
license_num VARCHAR(64) NOT NULL,
username VARCHAR(64) NOT NULL UNIQUE,
driving_since DATE NOT NULL,
PRIMARY KEY (license_num),
FOREIGN KEY (username) REFERENCES account (username)
);

CREATE TABLE advertisement
(
start_date_time TIMESTAMP NOT NULL,
license_num VARCHAR(64) NOT NULL,
origin VARCHAR(255) NOT NULL,
destination VARCHAR(255) NOT NULL,
PRIMARY KEY (start_date_time, license_num),
FOREIGN KEY (license_num) REFERENCES driver (license_num),
CONSTRAINT origin_dest_different CHECK (origin != destination)
);

CREATE TABLE car
(
license_plate VARCHAR(10) NOT NULL,
brand VARCHAR(64) NOT NULL,
model VARCHAR(64) NOT NULL,
license_num VARCHAR(64) NOT NULL,
PRIMARY KEY (license_plate),
FOREIGN KEY (license_num) REFERENCES driver (license_num)
);

CREATE TABLE bid
(
bid_id INTEGER NOT NULL,
price DECIMAL(19,4) NOT NULL,
username VARCHAR(64) NOT NULL,
start_date_time TIMESTAMP NOT NULL,
license_num VARCHAR(64) NOT NULL,
PRIMARY KEY (bid_id),
FOREIGN KEY (username) REFERENCES account (username),
FOREIGN KEY (start_date_time, license_num) REFERENCES advertisement
(start_date_time, license_num),
CONSTRAINT price_not_negative CHECK (price > 0)
);

CREATE TABLE ride
(
bid_id INTEGER NOT NULL,
won_date_time TIMESTAMP NOT NULL,
PRIMARY KEY (bid_id, won_date_time),
FOREIGN KEY (bid_id) REFERENCES bid (bid_id)
);
