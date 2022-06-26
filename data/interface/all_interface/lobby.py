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
    if hasattr(user, 'role_id'):
        if user.role_id == 1:
            return redirect('/account')
        elif user.role_id == 2:
            return redirect('/admin')
    return render_template('front/index.html', user=user)