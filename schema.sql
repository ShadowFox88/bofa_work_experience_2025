CREATE TABLE IF NOT EXISTS users (
    id text NOT NULL PRIMARY KEY,
    password text NOT NULL,
    balance float NOT NULL DEFAULT 0,
    currency char(3) NOT NULL
);

-- logs