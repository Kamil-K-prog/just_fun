from flask import Blueprint, session, jsonify, render_template, redirect
from .middleware import is_admin, is_user
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from data.db import db_sessionmaker
from ...db.__all_models import User

blueprint = Blueprint('web', __name__, template_folder='templates')
login_manager = LoginManager()


@blueprint.route('/account', methods=['GET', 'POST'])
@login_required
@is_user
def account():
    user = current_user
    return render_template('back/passport_form.html', user=user, title='Личный кабинет')


@blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
@is_admin
def admin():
    user = current_user
    return render_template('back/admin.html', user=user, title='Админка')

