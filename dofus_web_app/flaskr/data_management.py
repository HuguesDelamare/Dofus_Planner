from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for, current_app
)
from dofus_web_app.flaskr.db import get_db
import json
import os

#
bp = Blueprint('data_m', __name__,)


@bp.route('/insert-data', methods=['POST'])
def insert_data_from_json():
    json_path = os.path.join('..', 'items.json')
    # Reading the json file
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        print(data)
