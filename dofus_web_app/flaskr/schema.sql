DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id_dofus INT,
    item_name TEXT,
    item_image TEXT,
    item_type TEXT,
    item_level INT,
    item_description TEXT,
    item_stats TEXT
);

CREATE TABLE IF NOT EXISTS item_ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INT,
    ingredients_name TEXT,
    ingredients_quantity INT,
    ingredients_image TEXT,
    FOREIGN KEY (item_id) REFERENCES items (id)
);