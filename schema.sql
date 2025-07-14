CREATE TABLE IF NOT EXISTS users (
    id text NOT NULL PRIMARY KEY,
    password text NOT NULL,
    balance float NOT NULL,
    currency char(3) NOT NULL,
);

CREATE TABLE IF NOT EXISTS fx (
    currency char(3) NOT NULL,
    value float NOT NULL -- what 1 usd is equal to
);