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


@blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
@is_admin
def Passports():
    user = current_user
    return render_template('back/html/back/admin.html', user=user, title='Паспорта')


@blueprint.route('/admin_bids', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_Bids():
    user = current_user
    return render_template('back/html/back/admin_bids.html', user=user, title='Сбор информации')


@blueprint.route('/admin_forms', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_Forms():
    user = current_user
    return render_template('back/html/back/admin_forms.html', user=user, title='Золотые знаки')


@blueprint.route('/admin_edit_form', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_Edit_Form():
    user = current_user
    return render_template('back/html/back/admin_edit_form.html', user=user, title='Страница редактирования')


@blueprint.route('/passport_view', methods=['GET', 'POST'])
@login_required
def Passport_View():
    user = current_user
    return render_template('back/html/back/passport_view.html', user=user, title='Паспорт')


@blueprint.route('/account', methods=['GET', 'POST'])
@login_required
@login_required
@is_user
def account():
    user = current_user
    return render_template('back/passport_form.html', user=user, title='Личный кабинет')

@blueprint.route('/passport_form', methods=['GET', 'POST'])
@login_required
@is_user
def Passport_Form():
    user = current_user
    return render_template('back/html/back/passport_form.html', user=user, title='Организации')

@blueprint.route('/form_collection_of_information', methods=['GET', 'POST'])
@login_required
@is_user
def Form_Collection_of_Information():
    user = current_user
    return render_template('back/html/back/form_collection_of_information.html', user=user, title='Сбор информации')

@blueprint.route('/golden_badge', methods=['GET', 'POST'])
@login_required
@is_user
def Golden_Badge():
    user = current_user
    return render_template('back/html/back/golden_badge.html', user=user, title='Золотой знак')

