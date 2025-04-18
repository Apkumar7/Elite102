CREATE DATABASE IF NOT EXISTS bank_system;
USE bank_system;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    pin VARCHAR(10) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Accounts table
CREATE TABLE IF NOT EXISTS accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    balance DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Insert sample users
INSERT INTO users (name, pin, is_admin) VALUES ('AdminUser', '1234', TRUE);
INSERT INTO users (name, pin, is_admin) VALUES ('John Doe', '1111', FALSE);

-- Insert sample accounts
INSERT INTO accounts (user_id, balance) VALUES (1, 1000.00), (2, 250.50);
