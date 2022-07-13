import imp
from flask import Blueprint, session, jsonify, render_template, redirect
from flask import request as req
from requests import request
from .mail_sender import send_mail
from ...routes.flask_wtf_forms import PassportForm
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


blueprint = Blueprint('admin_interface', __name__, template_folder='templates')
login_manager = LoginManager()

@blueprint.route('/admin', methods=['GET', 'POST']
                 )  # главная страница администратора. Управление паспортами
@login_required
@is_admin
def Passports():
    user = current_user
    db_sess = db_sessionmaker.create_session()
    m = db_sess.query(Passport).all()
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
    return render_template('back/admin.html',
                           user=user,
                           title='Паспорта',
                           passports=passports_list)


@blueprint.route('/admin_bids', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_Bids():
    user = current_user
    db_sess = db_sessionmaker.create_session()
    m = db_sess.query(GoldenMarkApplication).all()
    appl_list = []
    for ap in m:
        appl_list.append({
            'id':
            ap.passport_id,
            'organization_short_name':
            db_sess.query(Passport).filter_by(
                id=ap.passport_id).first().organization_short_name,
            'date':
            ap.application_date,
            'status':
            ap.application_verdict
        })
    return render_template('back/admin_bids.html',
                           user=user,
                           title='Сбор информации',
                           apples=appl_list)

@blueprint.route('/admin_forms', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_Forms():
    form = AdminAddForm()
    user = current_user
    db_sess = db_sessionmaker.create_session()
    q_list = []
    qs = db_sess.query(Quiz).all()
    for i in qs:
        q_list.append({'name': i.title, 'id': i.id})
    if form.validate_on_submit():
        err_mes = None
        if db_sess.query(Quiz).filter_by(title=form.name.data).first():
            err_mes = 'Форма с таким названием уже существует'
        if err_mes:
            return render_template('back/admin_forms.html',
                                   user=user,
                                   form=form,
                                   title='Золотые знаки',
                                   message=err_mes,
                                   quizes=q_list)
        else:
            q = Quiz(title=form.name.data)
            db_sess.add(q)
            db_sess.commit()
            return redirect('/admin_forms')
    return render_template('back/admin_forms.html',
                           user=user,
                           form=form,
                           title='Золотые знаки',
                           quizes=q_list)


@blueprint.route('/admin_delete_form/<qz_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_Del_Form(qz_id):
    user = current_user
    db_sess = db_sessionmaker.create_session()
    db_sess.query(Quiz).filter_by(id=qz_id).delete()
    db_sess.commit()
    return redirect('/admin_forms')


@blueprint.route('/admin_edit_form/<qz_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_Edit_Form(qz_id):
    user = current_user
    form = AdminAddForm()
    db_sess = db_sessionmaker.create_session()
    fields = db_sess.query(Field).filter_by(quiz_id=qz_id)
    if form.validate_on_submit():
        type = req.form.get("type_field")
        f = Field(title=form.name.data, type=type, quiz_id=qz_id)
        db_sess.add(f)
        db_sess.commit()
        return redirect(f'/admin_edit_form/{qz_id}')

    return render_template('back/admin_edit_form.html',
                           user=user,
                           title='Страница редактирования',
                           fields=fields,
                           qz_id=qz_id,
                           form=form)


@blueprint.route('/admin_field_del/<f_id>/<qz_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_Del_Field(f_id, qz_id):
    user = current_user
    db_sess = db_sessionmaker.create_session()
    db_sess.query(Field).filter_by(id=f_id).delete()
    db_sess.commit()
    return redirect(f'/admin_edit_form/{qz_id}')
