from flask import Blueprint, session, jsonify, render_template, redirect
from flask import request as req
from requests import request
from .mail_sender import send_mail
from .middleware import is_admin, is_user
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from data.db import db_sessionmaker
from werkzeug.utils import secure_filename
import os
from ...db.__all_models import User, Passport, PassportStatus, GoldenMarkApplication, Quiz, Video, Photo, Field, Profrisk
from ..flask_wtf_forms import AdminAddForm, GetFilesForm, GoldenBadgeApplicationForm, WorkProtectionForm

blueprint = Blueprint('user_interface', __name__, template_folder='templates')
login_manager = LoginManager()


@blueprint.route('/account', methods=['GET', 'POST'])
@login_required
@is_user
def account():
    user = current_user
    db_sess = db_sessionmaker.create_session()
    m = db_sess.query(Passport).filter_by(user_id=user.id).all()
    passports_list = []
    for pas in m:
        passports_list.append({
            'id':
            pas.id,
            'organization_short_name':
            pas.organization_short_name,
            'date':
            pas.date_of_data_collection,
            'golden_mark':
            pas.golden_mark,
            'status':
            db_sess.query(PassportStatus).filter_by(
                id=pas.passport_status).first().name
        })
    return render_template('back/passport_form.html',
                           user=user,
                           title='Личный кабинет',
                           organizations=passports_list)


@blueprint.route('/golden_badge', methods=['GET', 'POST'])
@login_required
@is_user
def golden_badge():
    sess = db_sessionmaker.create_session()
    user = current_user

    applications = []
    passports = sess.query(Passport).filter(Passport.user_id == user.id).all()
    for passp in passports:
        for i in sess.query(GoldenMarkApplication).filter(GoldenMarkApplication.passport_id == passp.id).all():
            applications.append([passp, i])

    form = GoldenBadgeApplicationForm()
    if form.validate_on_submit():
        badge = GoldenMarkApplication(
            passport_id=form.organization_id.data,
            application_date=form.date_of_application.data
        )
        sess.add(badge)
        sess.commit()
        return redirect('/golden_badge')
    return render_template('back/golden_badge.html',
                           user=user,
                           title='Золотой знак',
                           form=form,
                           applications=applications)


@blueprint.route('/delete_organization/<id>', methods=['GET', 'POST'])
@login_required
@is_user
def delete_passport(id):
    sess = db_sessionmaker.create_session()
    i = sess.query(Passport).filter(Passport.id == id).first()
    sess.delete(i)
    sess.commit()
    return redirect('/account')


@blueprint.route('/delete_application/<id>', methods=['GET', 'POST'])
@login_required
@is_user
def delete_application(id):
    sess = db_sessionmaker.create_session()
    i = sess.query(GoldenMarkApplication).filter(GoldenMarkApplication.id == id).first()
    sess.delete(i)
    sess.commit()
    return redirect('/golden_badge')


@blueprint.route('/profrisk_information_collection', methods=['GET', 'POST'])
@login_required
@is_user
def profrisks_collection():
    user = current_user
    form = WorkProtectionForm()
    sess = db_sessionmaker.create_session()

    if form.validate_on_submit():
        check = 0

        if form.profrisks_check.data == 'Да':
            check = 1
        elif form.profrisks_check.data == 'Нет':
            check = 2
        elif form.profrisks_check.data == 'Частично':
            check = 3

        prf = Profrisk(
            passport_id=form.pasport_id.data,
            profrisks_check=check,
            last_check_date=form.last_check_date.data
        )
        sess.add(prf)
        sess.commit()
        return redirect('/profrisk_information_collection')
    return render_template('back/form_collection_of_information.html', user=user,
                           title='Сбор информации о профрисках', form=form)