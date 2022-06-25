from flask import Blueprint, session, jsonify, render_template, redirect
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

blueprint = Blueprint('lobby', __name__, template_folder='templates')


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    user = current_user
    return render_template('front/index.html', user=user)