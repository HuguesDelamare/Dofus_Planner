from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for, current_app
)
from dofus_web_app.flaskr.db import get_db
import json
import os

bp = Blueprint('data_m', __name__)

@bp.route('/insert-data', methods=['POST'])
def insert_data_from_json():
    json_path = os.path.join('.', 'items.json')
    # Reading the JSON file
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)
        for page in json_data:
            for item in json_data[page]:
                stats_str = ', '.join(item['stats'])

                # Inserting the data into the 'items' table
                db = get_db()
                db.execute(
                    'INSERT INTO items (item_id_dofus, item_name, item_image, item_type, item_level, item_description, item_stats) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (item['id'], item['name'], item['image'], item['type'], item['level'], item['description'], stats_str)
                )

                # Commit the changes to retrieve the last inserted row ID
                db.commit()
                item_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]

                # Inserting the data into the 'item_ingredients' table
                recipe = item.get('recipe')  # Get the 'recipe' attribute
                if recipe and isinstance(recipe, list):
                    for ingredient in recipe:
                        db.execute(
                            'INSERT INTO item_ingredients (item_id, ingredients_name, ingredients_quantity, ingredients_image) VALUES (?, ?, ?, ?)',
                            (item_id, ingredient.get('name'), ingredient.get('quantity'), ingredient.get('image'))
                        )
                else:
                    flash("Invalid recipe data for item: {}".format(item['id']), "error")
            print("Page" + page + "inserted.")
            db.commit()
    return redirect(url_for('index'))
