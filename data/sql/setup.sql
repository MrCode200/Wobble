CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    xp INTEGER DEFAULT 0,
    lvl INTEGER DEFAULT 1
);
