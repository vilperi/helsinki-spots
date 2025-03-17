CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE spots (
    id INTEGER PRIMARY KEY,
    name TEXT,
    lat REAL,
    lon REAL,
    category TEXT
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    spot_id INTEGER REFERENCES spots
);