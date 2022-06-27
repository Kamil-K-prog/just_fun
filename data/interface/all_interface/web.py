from flask import Blueprint, session, jsonify, render_template, redirect
from flask import request as req
from requests import request
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
from werkzeug.utils import secure_filename
import os
from ...db.__all_models import User, Passport, PassportStatus, GoldenMarkApplication, Quiz, Video, Photo, Field
from ..flask_wtf_forms import AdminAddForm, GetFilesForm

blueprint = Blueprint('web', __name__, template_folder='templates')
login_manager = LoginManager()

UPLOAD_FOLDER = 'upload/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# доступные расширения файлов, типа mime-типы =)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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


@blueprint.route('/pasport_docs_download/<pas_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def AdminDownloadDock(pas_id):
    user = current_user
    db_sess = db_sessionmaker.create_session()
    vedeos = db_sess.query(Video).filter_by(pass_id=pas_id).all()
    photos = db_sess.query(Photo).filter_by(pass_id=pas_id).all()

    return render_template('back/admin_downloads.html',
                           user=user,
                           title='Сбор информации',
                           videos=vedeos,
                           photos=photos)


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


@blueprint.route('/admin_passport_confirm/<pass_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_PasswordConfirm_Form(pass_id):
    user = current_user
    db_sess = db_sessionmaker.create_session()
    pass_obj = db_sess.query(Passport).filter_by(id=pass_id).first()
    pass_obj.passport_status = db_sess.query(PassportStatus).filter_by(
        name='Принят').first().id
    db_sess.add(pass_obj)
    db_sess.commit()
    return redirect('/admin')


@blueprint.route('/admin_passport_decline/<pass_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_PassDecline_Form(pass_id):
    user = current_user
    db_sess = db_sessionmaker.create_session()
    pass_obj = db_sess.query(Passport).filter_by(id=pass_id).first()
    pass_obj.passport_status = db_sess.query(PassportStatus).filter_by(
        name='Отклонен').first().id
    db_sess.add(pass_obj)
    db_sess.commit()
    return redirect('/admin')


@blueprint.route('/admin_gold_confirm/<pass_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_GoldConfirm_Form(pass_id):
    user = current_user
    db_sess = db_sessionmaker.create_session()
    pass_obj = db_sess.query(Passport).filter_by(id=pass_id).first()
    gd_app = db_sess.query(GoldenMarkApplication).filter_by(
        passport_id=pass_id).first()
    pass_obj.golden_mark = True
    gd_app.application_verdict = True
    db_sess.add(pass_obj)
    db_sess.add(gd_app)
    db_sess.commit()
    return redirect('/admin_bids')


@blueprint.route('/admin_gold_decline/<pass_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def Admin_GoldDecline_Form(pass_id):
    user = current_user
    db_sess = db_sessionmaker.create_session()
    pass_obj = db_sess.query(Passport).filter_by(id=pass_id).first()
    gd_app = db_sess.query(GoldenMarkApplication).filter_by(
        passport_id=pass_id).first()
    pass_obj.golden_mark = False
    gd_app.application_verdict = False
    db_sess.add(pass_obj)
    db_sess.add(gd_app)
    db_sess.commit()
    return redirect('/admin_bids')


@blueprint.route('/passport_view/<pas_id>', methods=['GET', 'POST'])
@login_required
def Passport_View(pas_id):
    user = current_user
    db_sess = db_sessionmaker.create_session()
    pas = db_sess.query(Passport).filter_by(id=pas_id).first()
    pass_di = {
        'id':
        pas.id,
        'user_id':
        pas.user_id,
        'name_of_the_legal_entity':
        pas.name_of_the_legal_entity,
        'organization_full_name':
        pas.organization_full_name,
        'organization_short_name':
        pas.organization_short_name,
        'legal_address':
        pas.legal_address,
        'fact_address':
        pas.fact_address,
        'boss_full_name_n_position':
        pas.boss_full_name_n_position,
        'INN':
        pas.INN,
        'OKTMO':
        pas.OKTMO,
        'main_activity_OKVED':
        pas.main_activity_OKVED,
        'male_workers_count':
        pas.male_workers_count,
        'female_workers_count':
        pas.female_workers_count,
        'phone_number':
        pas.phone_number,
        'email_oficcial':
        pas.email_oficcial,
        'workers_protector_FIO_n_position':
        pas.workers_protector_FIO_n_position,
        'workers_protector_phone_number':
        pas.workers_protector_phone_number,
        'workers_protector_email':
        pas.workers_protector_email,
        'golden_mark':
        pas.golden_mark,
        'golden_mark_date':
        pas.golden_mark_date,
        'passport_status':
        db_sess.query(PassportStatus).filter_by(
            id=pas.passport_status).first().name,
        'date_of_application_submission':
        pas.date_of_application_submission
    }
    return render_template('back/passport_view.html',
                           user=user,
                           title='Паспорт',
                           passport=pass_di)


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


@blueprint.route('/passport_create', methods=['GET', 'POST'])
@login_required
@is_user
def Passport_Create():
    user = current_user
    form = PassportForm()
    sess = db_sessionmaker.create_session()
    if form.validate_on_submit():
        passport = Passport(
            user_id=user.id,
            name_of_the_legal_entity=form.opf.data,
            organization_full_name=form.full_name.data,
            organization_short_name=form.short_name.data,
            date_of_data_collection=form.information_date.data,
            boss_full_name_n_position=form.boss_fio.data + ' ' +
            form.boss_place.data,
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
            workers_protector_email=form.protector_email.data)
        sess.add(passport)
        sess.commit()
        return redirect(f'/passpoort_upload/{passport.id}')
    return render_template('back/passport_create.html',
                           user=user,
                           title='Организации',
                           form=form)


@blueprint.route('/passpoort_upload/<pas_id>')
@login_required
@is_user
def Passport_Downdoads(pas_id):
    user = current_user
    db_sess = db_sessionmaker.create_session()
    videos = db_sess.query(Video).filter_by(pass_id=pas_id).all()
    photos = db_sess.query(Photo).filter_by(pass_id=pas_id).all()

    if req.method == 'POST':
        file = req.files['file']
        v_url = file = req.files['video_url']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(UPLOAD_FOLDER + filename)
            p = Photo(pass_id=pas_id, filename=filename)
            v = Video(pass_id=pas_id, link=v_url)
            db_sess.add(p)
            db_sess.add(v)
            db_sess.commit()
            # тут можно срендерить шаблон с сообщением об успешной отправке
        return redirect(f'/passport_upload/{pas_id}')

    return render_template('back/passport_upload.html',
                           user=user,
                           title='Загрузка файлов',
                           videos=videos, photos=photos)


@blueprint.route('/form_collection_of_information', methods=['GET', 'POST'])
@login_required
@is_user
def Form_Collection_of_Information():
    user = current_user
    return render_template('back/form_collection_of_information.html',
                           user=user,
                           title='Сбор информации')


@blueprint.route('/golden_badge', methods=['GET', 'POST'])
@login_required
@is_user
def Golden_Badge():
    user = current_user
    return render_template('back/golden_badge.html',
                           user=user,
                           title='Р—РѕР»РѕС‚РѕР№ Р·РЅР°Рє')


@blueprint.route('/passport_change/<id>', methods=['GET', 'POST'])
@login_required
@is_user
def Passport_Change(id):
    form = PassportForm()
    user = current_user
    sess = db_sessionmaker.create_session()
    passp = sess.query(Passport).filter(Passport.id == id).first()

    form.opf.data = passp.name_of_the_legal_entity[:]
    form.full_name.data = passp.organization_full_name[:]
    form.short_name.data = passp.organization_short_name[:]
    form.information_date.data = passp.date_of_data_collection[:]
    form.boss_fio.data = passp.boss_full_name_n_position[:]
    form.boss_place.data = passp.boss_full_name_n_position[:]
    form.company_phone.data = passp.phone_number[:]
    form.company_email.data = passp.email_oficcial[:]
    form.location.data = passp.address_for_contact[:]
    form.address_fact.data = passp.fact_address[:]
    form.address_yur.data = passp.legal_address[:]
    form.inn.data = passp.INN[:]
    form.oktmo.data = passp.OKTMO[:]
    form.main_activity_okved.data = passp.main_activity_OKVED[:]
    form.workers_male_count.data = passp.male_workers_count
    form.workers_female_count.data = passp.female_workers_count
    form.protector_fio.data = passp.workers_protector_FIO_n_position[:]
    form.protector_phone.data = passp.workers_protector_phone_number[:]
    form.protector_email.data = passp.workers_protector_email[:]

    if form.validate_on_submit():

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

        sess.add(passp)
        sess.commit()
        return redirect('/account')
    return render_template('back/passport_edit.html', form=form, user=user)

    return render_template('back/golden_badge.html',
                           user=user,
                           title='Золотой знак')


@blueprint.route('/passport_delete/<id>')
@login_required
@is_user
def delete(id):
    sess = db_sessionmaker.create_session()
    i = sess.query(Passport).filter(Passport.id == id).first()
    sess.delete(i)
    sess.commit()
    return redirect('/account')