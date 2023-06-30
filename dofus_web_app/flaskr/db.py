import sqlite3
from flask import current_app, g


def init_app(app):
    app.teardown_appcontext(close_db)


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# Function to fetch search suggestions from the database
def get_suggestions(query):
    db = get_db()
    # SQL query to fetch suggestions based on the user's query
    cursor = db.execute("SELECT item_name FROM items WHERE LOWER(item_name) LIKE ? LIMIT 10", ('%' + query + '%',))
    # Extract the item names from the query result
    suggestions = [row['item_name'] for row in cursor.fetchall()]
    return suggestions


def perform_search(query):
    db = get_db()
    # Perform a database query to fetch the search results based on the query
    cursor = db.execute("SELECT * FROM items WHERE item_name = ?", (query,))
    results = [dict(row) for row in cursor.fetchall()]
    return results


def get_recipe_by_id(item_id):
    db = get_db()
    cursor = db.execute("SELECT * FROM item_ingredients WHERE item_id = ?", (item_id,))
    results = [dict(row) for row in cursor.fetchall()]
    return results
