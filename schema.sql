CREATE TABLE IF NOT EXISTS users (
    id text NOT NULL PRIMARY KEY,
    password text NOT NULL,
    balance float NOT NULL DEFAULT 0,
    currency char(3) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    id text NOT NULL,
    transaction_type text NOT NULL,
    amount float NOT NULL,
    currency char(3) NOT NULL,
    recipient_id text,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);