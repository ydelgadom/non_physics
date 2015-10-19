BEGIN;

CREATE SCHEMA winedb;

CREATE TABLE winedb.users(
    userid UUID PRIMARY KEY,
    real_name VARCHAR NOT NULL,
    username VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    created TIMESTAMP NOT NULL
);

CREATE TABLE winedb.wines (
    wineid UUID PRIMARY KEY,
    userid UUID REFERENCES winedb.users,
    name VARCHAR NOT NULL,
    typed VARCHAR NOT NULL,
    pics JSON NOT NULL,
    general_info JSON NOT NULL,
    fruit_family JSON NOT NULL,
    fruit_quality JSON NOT NULL,
    non_fruit_quality JSON NOT NULL,
    structure JSON NOT NULL,
    notes VARCHAR NOT NULL,
    created TIMESTAMP NOT NULL
);

COMMIT;