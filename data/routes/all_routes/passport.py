from flask import Blueprint, session, jsonify, render_template, redirect
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
from ...db.__all_models import User, Passport, PassportStatus, GoldenMarkApplication

blueprint = Blueprint('passport', __name__, template_folder='templates')
login_manager = LoginManager()


@blueprint.route('/admin_passport_confirm/<pass_id>', methods=['GET', 'POST'])  # подтверждение паспорта
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
    send_mail('Aleksey', 'begun.aleksey@mail.ru',
          'Your organization\'s passport has been verified',
          'You can use the information collection service')
    return redirect('/admin')


@blueprint.route('/admin_passport_decline/<pass_id>', methods=['GET', 'POST'])  # отказ в подтверждении паспорта
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
    send_mail('Aleksey', 'begun.aleksey@mail.ru',
          'Your organization\'s passport has been rejected',
          'Contact the administrator for clarification')
    return redirect('/admin')


@blueprint.route('/admin_gold_confirm/<pass_id>', methods=['GET', 'POST'])  # подтверждение выдачи золотого знака
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
    send_mail('Aleksey', 'begun.aleksey@mail.ru', 'You have been given a golden badge',
          'Congratulations to your organization')
    return redirect('/admin_bids')


@blueprint.route('/admin_gold_decline/<pass_id>', methods=['GET', 'POST'])  # отказ в выдаче золотого знака
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
    send_mail('Aleksey', 'begun.aleksey@mail.ru', 'Gold badge application rejected',
          'Contact the administrator for clarification')
    return redirect('/admin_bids')


@blueprint.route('/passport_view/<pas_id>', methods=['GET', 'POST'])  # просмотр паспорта
@login_required
def Passport_View(pas_id):
    user = current_user
    db_sess = db_sessionmaker.create_session()
    pas = db_sess.query(Passport).filter_by(id=pas_id).first()

    if user.role_id != 2:  # защита от просмотра чужого паспорта
        if user.id != pas.user_id:
            return redirect('/account')
    
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


@blueprint.route('/passport_create', methods=['GET', 'POST'])  # создание паспорта
@login_required
@is_user
def Passport_Create():
    user = current_user
    form = PassportForm()
    sess = db_sessionmaker.create_session()
    if form.validate_on_submit():
        print('POST\n')
        passport = Passport(
            user_id=user.id,
            name_of_the_legal_entity=form.opf.data,
            organization_full_name=form.full_name.data,
            organization_short_name=form.short_name.data,
            date_of_data_collection=form.information_date.data,
            boss_full_name_n_position=form.boss_fio.data + ' ' +  #TODO: убрать разделение этих полей
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
        send_mail('Aleksey', 'begun.aleksey@mail.ru', "Passport application",
          'You have received an application for a passport')
        return redirect(f'/passpoort_upload/{passport.id}')
    return render_template('back/passport_create.html',
                           user=user,
                           title='Организации',
                           form=form)


@blueprint.route('/passport_change/<id>', methods=['GET', 'POST'])  # изменение паспорта
@login_required
@is_user
def Passport_Change(id):
    form = PassportForm()
    user = current_user
    sess = db_sessionmaker.create_session()
    passp = sess.query(Passport).filter(Passport.id == id).first()

    if user.role_id != 2:  # защита от редактирования чужого паспорта
        if user.id != passp.user_id:
            return redirect('/account')

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


@blueprint.route('/passport_delete/<id>')  # Удаление паспорта
@login_required
@is_user
def delete(id):
    user = current_user
    sess = db_sessionmaker.create_session()
    passp = sess.query(Passport).filter(Passport.id == id).first()

    if user.role_id != 2:  # защита от удаления чужого паспорта
        if user.id != passp.user_id:
            return redirect('/account')

    sess.delete(passp)
    sess.commit()
    return redirect('/account')