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
optional_bio VARCHAR(255),
PRIMARY KEY (license_number),
FOREIGN KEY (username) REFERENCES account (username)
);

CREATE TABLE advertisement
(
start_timestamp TIMESTAMP NOT NULL,
license_number VARCHAR(64) NOT NULL,
origin VARCHAR(255) NOT NULL,
destination VARCHAR(255) NOT NULL,
active BOOLEAN NOT NULL,
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
bid_id SERIAL NOT NULL,
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

CREATE OR REPLACE FUNCTION get_highest_bid(c_license_number VARCHAR(64), c_start_timestamp TIMESTAMP)
RETURNS INTEGER AS
$$
DECLARE
	highest_bid INTEGER;
BEGIN
	SELECT max(price) INTO highest_bid
	FROM (
		SELECT price
		FROM bid
		WHERE bid.license_number=c_license_number and bid.start_timestamp=c_start_timestamp
	) AS advertisement_bids;
	IF highest_bid IS NULL THEN
		highest_bid := 0;
	END IF;
	RETURN highest_bid;
END
$$ LANGUAGE plpgsql;

INSERT INTO account (username, is_admin, dob, email, contact, pass, name) VALUES ('admin', true, '1990-12-12', 'admin@zooom.com', '91234567', 'pbkdf2:sha256:50000$2H9J5Im2$e34488586e65fe584fd660eac998c06180d9f0ade7164071a3c50caeaf5c0c93', 'System Administratior');
