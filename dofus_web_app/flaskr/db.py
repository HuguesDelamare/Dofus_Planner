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


def perform_search(query):
    db = get_db()
    cursor = db.execute("SELECT * FROM items WHERE item_name = ?", (query,))
    results = [dict(row) for row in cursor.fetchall()]
    return results


def get_item_by_id(item_id):
    db = get_db()
    cursor = db.execute("""
        SELECT items.*, item_ingredients.ingredients_name, item_ingredients.ingredients_quantity, item_ingredients.ingredients_image
        FROM items
        LEFT JOIN item_ingredients ON items.item_id_dofus = item_ingredients.item_id
        WHERE items.item_id_dofus = ?
    """, (item_id,))

    item_rows = cursor.fetchall()
    if not item_rows:
        return None
    item = {
        'id': item_rows[0]['item_id_dofus'],
        'name': item_rows[0]['item_name'],
        'image': item_rows[0]['item_image'],
        'type': item_rows[0]['item_type'],
        'level': item_rows[0]['item_level'],
        'description': item_rows[0]['item_description'],
        'stats': item_rows[0]['item_stats'],
        'recipe': []
    }
    for row in item_rows:
        if row['ingredients_name'] is not None:
            item['recipe'].append({
                'name': row['ingredients_name'],
                'quantity': row['ingredients_quantity'],
                'image': row['ingredients_image']
            })

    return item


def add_item(item):
    db = get_db()
    # Insert the item into the items table
    stats_str = ', '.join(item['stats'])
    db.execute(
        'INSERT INTO items (item_id_dofus, item_name, item_image, item_type, item_level, item_description, item_stats) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (item['id'], item['name'], item['image'], item['type'], item['level'], item['description'], stats_str)
    )
    db.commit()

    recipe = item.get('recipe')
    if recipe and isinstance(recipe, list):
        # Insert the recipe ingredients into the item_ingredients table
        for ingredient in recipe:
            db.execute(
                'INSERT INTO item_ingredients (item_id, ingredients_name, ingredients_quantity, ingredients_image) VALUES (?, ?, ?, ?)',
                (item['id'], ingredient.get('name'), ingredient.get('quantity'), ingredient.get('image'))
            )
        db.commit()
    else:
        # Handle the case when recipe data is invalid
        print("Invalid recipe data for item: {}".format(item['id']), "error")


def item_exists(item_id):
    db = get_db()
    cursor = db.execute("SELECT COUNT(*) FROM items WHERE item_id_dofus = ?", (item_id,))
    count = cursor.fetchone()[0]
    if count == 0:
        print("Item does not exist in the database")
    else:
        print("Item already exists in the database")
    return count > 0
