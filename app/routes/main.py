from flask import Blueprint, redirect, url_for
from flask_login import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return redirect(url_for('auth.login')) 