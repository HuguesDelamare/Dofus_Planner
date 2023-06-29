from flask import Blueprint, render_template

# Create a Blueprint object for your views
bp = Blueprint('views', __name__)


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/craft')
def craft():
    return render_template('craft.html')


@bp.route('/workbench')
def workbench():
    return render_template('workbench.html')
