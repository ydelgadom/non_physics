CREATE DATABASE winesdb;

CREATE TABLE winesdb.users(
    userid VARCHAR(36) PRIMARY KEY,
    real_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(32) NOT NULL,
    created TIMESTAMP NOT NULL
);

CREATE TABLE winesdb.wines (
    wineid VARCHAR(36) PRIMARY KEY,
    userid VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL,
    typed VARCHAR(20) NOT NULL,
    pics BLOB NOT NULL,
    general_info BLOB NOT NULL,
    sight BLOB NOT NULL,
    nose BLOB NOT NULL,
    taste BLOB NOT NULL,
    notes VARCHAR(255) NOT NULL,
    created TIMESTAMP NOT NULL
);
