CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    created_at TEXT,
    wrong_coords INTEGER DEFAULT 0,
    password_hash TEXT
);

CREATE TABLE spots (
    id INTEGER PRIMARY KEY,
    name TEXT,
    lat REAL,
    lon REAL,
    description TEXT,
    category TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER,
    spot_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (spot_id) REFERENCES spots(id) ON DELETE CASCADE
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    spot_id INTEGER,
    image BLOB,
    FOREIGN KEY (spot_id) REFERENCES spots(id) ON DELETE CASCADE
);

CREATE INDEX idx_user_spots ON spots(user_id);
CREATE INDEX idx_spot_category ON spots(category);
CREATE INDEX idx_spot_name ON spots(name);
CREATE INDEX idx_comments_spot ON comments(spot_id);
CREATE INDEX idx_images_spot ON images(spot_id);
CREATE INDEX idx_users_username ON users(username);