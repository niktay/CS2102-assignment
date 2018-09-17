CREATE TABLE Account
(
 account_id SERIAL PRIMARY KEY,
 first_name VARCHAR(64) NOT NULL,
 last_name VARCHAR(64) NOT NULL,
 is_admin BOOLEAN NOT NULL,
 email VARCHAR(64) NOT NULL
);

INSERT INTO Account VALUES (DEFAULT, 'XIE XIN', 'CHEN', false, 'xiexin2011@gmail.com');
INSERT INTO Account VALUES (DEFAULT, 'MARY', 'TAN', false, 'mt1993@gmail.com');
INSERT INTO Account VALUES (DEFAULT, 'SUSASSANE', 'LIM', false, 'suzzlim99@gmail.com');
INSERT INTO Account VALUES (DEFAULT, 'FABIAN', 'KOH', false, 'fabiancool@gmail.com');
INSERT INTO Account VALUES (DEFAULT, 'JASMINE', 'JEE', true, 'jasjee91@gmail.com');
