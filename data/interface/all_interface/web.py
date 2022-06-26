from flask import Blueprint, session, jsonify, render_template, redirect, request
from ...interface.flask_wtf_forms import PassportForm
from .middleware import is_admin, is_user
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from data.db import db_sessionmaker
from ...db.__all_models import User, Passport, Video, Photo
from werkzeug.utils import secure_filename
import os

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
    return render_template('back/admin_edit_form.html', user=user,
                           title='РЎС‚СЂР°РЅРёС†Р° СЂРµРґР°РєС‚РёСЂРѕРІР°РЅРёСЏ')


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

    sess = db_sessionmaker.create_session()
    organizations = sess.query(Passport).filter_by(user_id=user.id).all()
    form = PassportForm()
    if form.validate_on_submit():
        print('POST\n')
        passport = Passport(
            user_id=user.id,
            name_of_the_legal_entity=form.opf.data,
            organization_full_name=form.full_name.data,
            organization_short_name=form.short_name.data,
            date_of_data_collection=form.information_date.data,
            boss_full_name_n_position=form.boss_fio.data + ' ' + form.boss_place.data,
            phone_number=form.company_phone.data,
            email_oficcial=form.company_email.data,
            address_for_contact=form.location.data,
            fact_address=form.address_fact.data,
            legal_address=form.address_yur.data,
            INN=form.inn.data,
            OKTMO=form.oktmo.data,
            main_activity_OKVED=form.main_activity_okved.data,
            male_workers_count=form.workers_male_count.data,
            female_workers_count=form.workers_female_count.data,
            workers_protector_FIO_n_position=form.protector_fio.data,
            workers_protector_phone_number=form.protector_phone.data,
            workers_protector_email=form.protector_email.data
        )
        if form.video_url.data:
            vid = Video(
                user_id=user.id,
                link=form.video_url.data
            )
            sess.add(vid)
        if form.photo.data:
            phot = form.photo.data
            filename = secure_filename(phot.filename)
            phot.save(
                '/load', filename
            )

            photo = Photo(user_id=user.id, path=f'/load/{filename}')
            sess.add(photo)

        sess.add(passport)
        sess.commit()
    return render_template('back/passport_form.html', user=user, title='Личный кабинет', organizations=organizations,
                           form=form)


@blueprint.route('/passport_form', methods=['GET', 'POST'])
@login_required
@is_user
def Passport_Form():
    user = current_user
    return render_template('back/passport_form.html', user=user, title='Организации')


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


@blueprint.route('/passport_change/<id>', methods=['GET', 'POST'])
@login_required
@is_user
def Passport_Change(id):
    form = PassportForm()
    user = current_user
    if form.validate_on_submit():
        print('POST\n')
        sess = db_sessionmaker.create_session()

        passp = sess.query(Passport).filter(Passport.id == id).first()

        passp.name_of_the_legal_entity = form.opf.data
        passp.organization_full_name = form.full_name.data
        passp.organization_short_name = form.short_name.data
        passp.date_of_data_collection = form.information_date.data
        passp.boss_full_name_n_position = form.boss_fio.data + ' ' + form.boss_place.data
        passp.phone_number = form.company_phone.data
        passp.email_oficcial = form.company_email.data
        passp.address_for_contact = form.location.data
        passp.fact_address = form.address_fact.data
        passp.legal_address = form.address_yur.data
        passp.INN = form.inn.data
        passp.OKTMO = form.oktmo.data
        passp.main_activity_OKVED = form.main_activity_okved.data
        passp.male_workers_count = form.workers_male_count.data
        passp.female_workers_count = form.workers_female_count.data
        passp.workers_protector_FIO_n_position = form.protector_fio.data
        passp.workers_protector_phone_number = form.protector_phone.data
        passp.workers_protector_email = form.protector_email.data

        if form.video_url.data:
            vid = Video(
                user_id=user.id,
                link=form.video_url.data
            )
            sess.add(vid)
        if form.photo.data:
            phot = form.photo.data
            filename = secure_filename(phot.filename)
            phot.save(
                '/photos', filename
            )

            photo = Photo(user_id=user.id, path=f'/photos/{filename}')
            sess.add(photo)
        sess.commit()
        return redirect('/account')
    return render_template('back/passport_edit.html', form=form, user=user)
