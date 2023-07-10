from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from .auth import login_required
from bs4 import BeautifulSoup


bp = Blueprint('profile', __name__)


@bp.route('/profile')
@login_required
def user_profile():
    return render_template('user/profile.html')
