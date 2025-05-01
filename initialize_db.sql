-- I had an error initially because I forgot to set AUTO_INCREMENT for id
DROP DATABASE IF EXISTS bank_user_info;
CREATE DATABASE bank_user_info;
USE bank_user_info;

CREATE TABLE user_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45),
    date VARCHAR(10),
    SSN VARCHAR(9),
    number VARCHAR(10),
    PIN VARCHAR(6) UNIQUE,
    balance INT
);
