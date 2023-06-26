DROP TABLE IF EXISTS user;


CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_dofus TEXT,
    name TEXT,
    image TEXT,
    type TEXT,
    level TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS item_stats (
    id INTEGER PRIMARY KEY,
    item_id INTEGER,
    stat TEXT,
    FOREIGN KEY (item_id) REFERENCES items (id)
);

CREATE TABLE IF NOT EXISTS item_ingredients (
    id INTEGER PRIMARY KEY ,
    item_id INTEGER,
    name TEXT,
    quantity TEXT,
    image TEXT,
    FOREIGN KEY (item_id) REFERENCES items (id)
);
