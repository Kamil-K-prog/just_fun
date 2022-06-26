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
    return render_template('back/admin.html', user=user, title='РџР°СЃРїРѕСЂС‚Р°')


@blueprint.route('/admin_bids', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_Bids():
    user = current_user
    return render_template('back/admin_bids.html', user=user, title='РЎР±РѕСЂ РёРЅС„РѕСЂРјР°С†РёРё')


@blueprint.route('/admin_forms', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_Forms():
    user = current_user
    return render_template('back/admin_forms.html', user=user, title='Р—РѕР»РѕС‚С‹Рµ Р·РЅР°РєРё')


@blueprint.route('/admin_edit_form', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_Edit_Form():
    user = current_user
    return render_template('back/admin_edit_form.html', user=user, title='РЎС‚СЂР°РЅРёС†Р° СЂРµРґР°РєС‚РёСЂРѕРІР°РЅРёСЏ')


@blueprint.route('/passport_view', methods=['GET', 'POST'])
@login_required
def Passport_View():
    user = current_user
    return render_template('back/passport_view.html', user=user, title='РџР°СЃРїРѕСЂС‚')


@blueprint.route('/account', methods=['GET', 'POST'])
@login_required
@is_user
def account():
    user = current_user
    return render_template('back/passport_form.html', user=user, title='Р›РёС‡РЅС‹Р№ РєР°Р±РёРЅРµС‚')

@blueprint.route('/passport_form', methods=['GET', 'POST'])
@login_required
@is_user
def Passport_Form():
    user = current_user
    return render_template('back/passport_form.html', user=user, title='РћСЂРіР°РЅРёР·Р°С†РёРё')

@blueprint.route('/form_collection_of_information', methods=['GET', 'POST'])
@login_required
@is_user
def Form_Collection_of_Information():
    user = current_user
    return render_template('back/form_collection_of_information.html', user=user, title='РЎР±РѕСЂ РёРЅС„РѕСЂРјР°С†РёРё')

@blueprint.route('/golden_badge', methods=['GET', 'POST'])
@login_required
@is_user
def Golden_Badge():
    user = current_user
    return render_template('back/golden_badge.html', user=user, title='Р—РѕР»РѕС‚РѕР№ Р·РЅР°Рє')