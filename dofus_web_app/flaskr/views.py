from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from dofus_web_app.flaskr.db import perform_search, add_item, get_item_by_id
from scrap_dofus_app.classes.dofus_to_json_class import DofusItemScrapping
from .db import get_all_servers
from .auth import login_required
from .db import item_exists
import os
import json


bp = Blueprint('views', __name__)


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/breeding/packages')
def breeding_packages():
    # Get all server data from the database
    servers = get_all_servers()
    return render_template('server.html', servers=servers)


@bp.route('/breeding/<server>')
def breeding(server):
    # Handle the selected server and any additional logic, if needed
    # Then, redirect to the "Breeding.html" page
    return redirect(url_for('views.breeding_html', server=server))


@bp.route('/offers/breeding_packages.html')
def breeding_html():
    # Render the "Breeding.html" page
    return render_template('offers/breeding_packages.html')


@bp.route('/craft', methods=['GET', 'POST'])
@login_required
def craft():
    query = request.args.get('query', '')
    if query:
        search_results = perform_search(query)
    else:
        search_results = "No recipe available for this item."
    return render_template('craft.html', results=search_results)


@bp.route('/workbench')
def workbench():
    return render_template('workbench.html')


@bp.route('/suggest')
def suggest():
    query = request.args.get('query', '').lower()

    # Load the JSON data
    json_path = os.path.join('.', 'items.json')
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Filter and retrieve suggestions based on the query
    suggestions = []
    for item in json_data:
        item_name = item.get('name', '').lower()
        if query in item_name:
            suggestions.append({'name': item_name, 'id': item.get('id', '')})

    return jsonify({'suggestions': suggestions})


@bp.route('/search')
def search():
    item_id = request.args.get('id', '')

    # Redirect to the URL with the item ID
    if item_id:
        if item_exists(item_id):
            item = get_item_by_id(item_id)
        else:
            url = f'https://www.dofus.com/fr/mmorpg/encyclopedie/equipements/{item_id}'
            scrapping = DofusItemScrapping()
            item = scrapping.get_item_from_url(url)
            if item:
                add_item(item)
            else:
                flash("Item not found.", "error")
                return redirect(url_for('views.craft'))
    else:
        # Handle the case when item ID is not found
        flash("Item not found.", "error")
        return redirect(url_for('views.craft'))
    return item
