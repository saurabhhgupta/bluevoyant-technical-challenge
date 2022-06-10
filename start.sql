CREATE DATABASE saurabh_bluevoyant;

CREATE USER 'bluevoyant'@'localhost' IDENTIFIED BY 'saurabh-is-hired';
CREATE USER 'bluevoyant'@'%' IDENTIFIED BY 'saurabh-is-hired';
GRANT ALL PRIVILEGES ON saurabh_bluevoyant.* TO 'bluevoyant'@'localhost';
GRANT ALL PRIVILEGES ON saurabh_bluevoyant.* TO 'bluevoyant'@'%';

USE saurabh_bluevoyant;

CREATE TABLE marvel(
    id int NOT NULL,
    name varchar(1000) NOT NULL,
    description varchar(5000) NOT NULL,
    thumbnail varchar(5000) NOT NULL
);
