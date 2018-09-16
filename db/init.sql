CREATE TABLE Account
(
 account_id SERIAL PRIMARY KEY,
 first_name VARCHAR(64) NOT NULL ,
 last_name  VARCHAR(64) NOT NULL ,
 is_admin   BOOLEAN NOT NULL ,
 email      VARCHAR(64) NOT NULL ,
);

INSERT INTO Account VALUES ('XIE XIN', 'CHEN', 0, 'xiexin2011@gmail.com');
INSERT INTO Account VALUES ('MARY', 'TAN', 0, 'mt1993@gmail.com');
INSERT INTO Account VALUES ('SUSASSANE', 'LIM', 0, 'suzzlim99@gmail.com');
INSERT INTO Account VALUES ('FABIAN', 'KOH', 0, 'fabiancool@gmail.com');
INSERT INTO Account VALUES ('JASMINE', 'JEE', 1, 'jasjee91@gmail.com');
