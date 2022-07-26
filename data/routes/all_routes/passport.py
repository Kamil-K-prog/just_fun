from typing import Dict, Set, Tuple
import datetime

import sqlalchemy
import flask_wtf
from flask import Blueprint, Response, render_template, redirect, abort
from flask_login import (
    login_required,
    current_user,
)

from ...db import db_sessionmaker, db_utils
from ...db.__all_models import User, Passport, PassportStatus, Video, File, \
    Location, EvalMarkSout, EvalMarkProfrisks, Process, Answer, PassportLog
from ...routes.flask_wtf_forms import PassportForm
from .middleware import is_admin, is_user
from .mail_sender import send_mail


blueprint = Blueprint('passport', __name__, template_folder='templates')


def _get_passport_normal_column_names() -> Set[str]:
    ("""Возвращает названия числовых, текстовых, булевых и датированных """
     """колонок таблицы passport, которые не заполняются автоматически и """
     """которые не являются внешними ключами на другие таблицы а БД""")
    NORMAL_TYPES = (int, str, bool, datetime.date)
    # получаем сет названий всех числовых, строковых и булевых колонок
    passport_normal_column_names = set(  # и колонок с датами
        db_utils._get_column_names_with_types(Passport, NORMAL_TYPES))
    # удаляем названия всех внешних ключей
    passport_normal_column_names -= set(
        db_utils._get_column_names_of_foreign_keys(Passport))

    # удаляем те названия колонок которые должны сами
    # заполниться автоматически (не обязательно сразу)
    passport_normal_column_names -= {
        'id',  # авто (первичный ключ)
        'date_of_application_submission',  # авто (текущее время)
        'date_of_application_editing',  # авто (текущее время)
        'golden_badge_verdict',  # авто (булевое значение)
        # заявка на Золотой знак не могла быть подана
        'golden_badge_application_date',
        # собственно, подтверждена тоже не могла быть
        'golden_badge_verification_date'}

    return passport_normal_column_names


PASSPORT_NORMAL_COLUMN_NAMES: Set[str] = _get_passport_normal_column_names()


def _get_foreign_key_kwarg(
        db_session: sqlalchemy.orm.Session,
        flask_wtf_form: flask_wtf.FlaskForm,
        db_model: sqlalchemy.orm.decl_api.DeclarativeMeta,
        db_name_field: str,
        form_field_name: str,
        kwarg_name: str) -> Dict[str, int]:
    """Возвращает словарь с именованым аргументом и id для записи в бд"""
    value = getattr(flask_wtf_form, form_field_name).data.title()
    entity = db_session.query(db_model).filter_by(
        **{db_name_field: value}).first()

    if entity is None:
        return {}
    return {kwarg_name: entity.id}


def _get_required_foreign_keys_kwargs(
    db_session: sqlalchemy.orm.Session,
        flask_wtf_form: flask_wtf.FlaskForm) -> Tuple[Dict[str, int]]:
    ("""Возвращает словари с названиями и значениями обязательных """
     """внешних ключей таблицы passport(значения берёт из формы) """
     """для подачи этой информации в ORM-модель/объект ORM-модели Passport"""
     """(для создания/редактирования паспорта организации)""")
    # получаем нужный аргумент location
    location_kwarg: Dict[str, int] = _get_foreign_key_kwarg(
        db_session, flask_wtf_form, Location,
        db_name_field='name',
        form_field_name='location',
        kwarg_name='location_id')

    # получаем нужный аргумент с отметкой проведения СОУТ
    sout_check_kwarg: Dict[str, int] = _get_foreign_key_kwarg(
        db_session, flask_wtf_form, EvalMarkSout,
        db_name_field='title',
        form_field_name='sout_check',
        kwarg_name='sout_check_eval_mark_id')

    # получаем нужный аргумент с отметкой проведения оценки профрисков
    profrisks_check_kwarg: Dict[str, int] = _get_foreign_key_kwarg(
        db_session, flask_wtf_form, EvalMarkProfrisks,
        db_name_field='title',
        form_field_name='profrisks_check',
        kwarg_name='profrisks_check_eval_mark_id')

    return (location_kwarg, sout_check_kwarg, profrisks_check_kwarg)


@blueprint.route(
    '/admin_passport_confirm/<int:pass_id>/', methods=['GET', 'POST'])
@login_required
@is_admin
def admin_passport_confirm_form(pass_id: int) -> Response:
    """Подтверждение паспорта"""

    with db_sessionmaker.create_session() as db_sess:
        pass_obj: Passport = db_sess.query(Passport).get(pass_id)

        if pass_obj is None:
            abort(404, description='Паспорт с таким id не найден')

        pass_obj.passport_status_id = db_sess.query(PassportStatus).filter_by(
            name='Принят').first().id
        user: User = pass_obj.user

        db_sess.commit()

        send_mail(
            user=user.login, mail_to=user.email,
            subject='Your organization\'s passport has been verified',
            text='You can use the information collection service')

    return redirect('/admin')


@blueprint.route(
    '/admin_passport_decline/<int:pass_id>/', methods=['GET', 'POST'])
@login_required
@is_admin
def admin_passport_decline_form(pass_id: int) -> Response:
    """Отказ в подтверждении паспорта"""

    with db_sessionmaker.create_session() as db_sess:
        pass_obj: Passport = db_sess.query(Passport).get(pass_id)

        if pass_obj is None:
            abort(404, description='Паспорт с таким id не найден')

        pass_obj.passport_status_id = db_sess.query(PassportStatus).filter_by(
            name='Отклонен').first().id
        user: User = pass_obj.user

        # удаление заявки на золотой знак
        pass_obj.golden_badge_application_date = None
        pass_obj.golden_badge_verification_date = None
        pass_obj.golden_badge_verdict = False

        db_sess.commit()

        send_mail(
            user=user.login, mail_to=user.email,
            subject='Your organization\'s passport has been rejected',
            text='Contact the administrator for clarification')

    return redirect('/admin')


@blueprint.route(
    '/passport_view/<int:pass_id>/', methods=['GET', 'POST'])
@login_required
def passport_view(pass_id: int) -> Response:
    """Просмотр паспорта"""
    user: User = current_user

    db_sess = db_sessionmaker.create_session()
    pass_obj: Passport = db_sess.query(Passport).get(pass_id)

    if pass_obj is None:
        abort(404, description='Паспорт с таким id не найден')

    # защита от просмотра чужого паспорта:
    if user.role_id != 2 and user.id != pass_obj.user_id:
        # если юзер - не админ и если это не его паспорт
        abort(403, description='Вам запрещено совершать это действие')

    passport_dict = pass_obj.to_dict()
    passport_dict['passport_status'] = pass_obj.status.name.title()
    passport_dict['location'] = pass_obj.location.name.title()
    passport_dict['sout_check'] = (
        pass_obj.sout_check_eval_mark.title.title())
    passport_dict['profrisks_check'] = (
        pass_obj.profrisks_check_eval_mark.title.title())

    return render_template(
        'back/passport_view.html',
        user=current_user,
        title='Паспорт',
        passport=passport_dict)


@blueprint.route('/passport_create/', methods=['GET', 'POST'])
@login_required
@is_user
def passport_create() -> Response:
    """Создание паспорта"""
    user: User = current_user
    form = PassportForm()

    with db_sessionmaker.create_session() as db_sess:
        if form.validate_on_submit():

            (  # получаем именованые аргументы обязательных внешних ключей
                location_kwarg,
                sout_check_kwarg,
                profrisks_check_kwarg
            ) = _get_required_foreign_keys_kwargs(db_sess, form)

            passport = Passport(
                user_id=user.id,  # проставляем вшешние ключи
                **location_kwarg,
                **sout_check_kwarg,
                **profrisks_check_kwarg,

                **{colname: getattr(form, colname).data  # проставляем значения
                    for colname in PASSPORT_NORMAL_COLUMN_NAMES})

            db_sess.add(passport)
            db_sess.commit()

            send_mail(
                user=user.login, mail_to=user.email,
                subject='Passport application',
                text='You have received an application for a passport')

            return redirect(f'/passport_upload/{passport.id}/')

    return render_template(
        'back/passport_create_or_edit.html',
        user=user,
        title='Организации',
        form=form)


@blueprint.route('/passport_change/<int:pass_id>/', methods=['GET', 'POST'])
@login_required
@is_user
def passport_change(pass_id: int) -> Response:
    """Изменение паспорта"""
    form = PassportForm()
    user: User = current_user

    with db_sessionmaker.create_session() as db_sess:

        passport: Passport = db_sess.query(Passport).get(pass_id)

        if passport is None:
            abort(404, description='Паспорт с таким id не найден')

        # защита от редактирования чужого паспорта
        if user.role_id != 2 and user.id != passport.user_id:
            abort(403, description='Вам запрещено совершать это действие')

        if form.validate_on_submit():
            # ПЕРЕНОС ДАННЫХ ИЗ ФОРМЫ В СУЩЕСТВУЮЩИЙ ПАСПОРТ

            # проставляем внешние ключи
            for foreign_key_dict in (
                    _get_required_foreign_keys_kwargs(db_sess, form)):
                if foreign_key_dict:
                    fk_key, fk_value = tuple(foreign_key_dict.items())[0]
                    setattr(passport, fk_key, fk_value)

            # проставляем значения обычных полей
            for pass_colname in PASSPORT_NORMAL_COLUMN_NAMES:
                setattr(
                    passport, pass_colname,
                    getattr(form, pass_colname).data)

            # ПРОЧИЕ МАНИПУЛЯЦИИ С ОБЪЕКТОМ ORM-МОДЕЛИ ПАСПОРТА

            # сброс статуса паспорта
            passport.passport_status_id = db_sess.query(
                PassportStatus).filter_by(name='На рассмотрении').first().id

            # удаление заявки на золотой знак
            passport.golden_badge_application_date = None
            passport.golden_badge_verification_date = None
            passport.golden_badge_verdict = False

            db_sess.commit()

            return redirect('/account')

        # ПОЛУЧЕНИЕ ДАННЫХ ИЗ ПАСПОРТА В ФОРМУ

        # проставляем значения из связанных таблиц
        form.location.data = passport.location.name
        form.sout_check.data = passport.sout_check_eval_mark.title
        form.profrisks_check.data = passport.profrisks_check_eval_mark.title

        # проставляем значения обычных полей
        for pass_colname in PASSPORT_NORMAL_COLUMN_NAMES:
            getattr(form, pass_colname).data = getattr(passport, pass_colname)

    return render_template(
        'back/passport_create_or_edit.html', form=form, user=user, is_editing=True)


@blueprint.route(
    '/delete_organization/<int:passport_id>/', methods=['GET', 'POST'])
@blueprint.route(
    '/passport_delete/<int:passport_id>/', methods=["GET", "POST"])
@login_required
@is_user
def passport_delete(passport_id: int) -> Response:
    """Удаление всех записей в бд, отвечающих за данный паспорт"""
    response = redirect('/account')
    user: User = current_user

    with db_sessionmaker.create_session() as db_sess:
        passport: Passport = db_sess.query(Passport).get(passport_id)

        if passport is None:
            abort(404, description='Паспорт с таким id не найден')

        # защита от удаления чужого паспорта:
        if user.role_id != 2 and user.id != passport.user_id:
            # если юзер - не админ и если это не его паспорт
            abort(403, description='Вам запрещено совершать это действие')

        # удаление всех ссылок на видео
        db_sess.query(Video).filter_by(passport_id=passport.id).delete()

        # удаление всех файлов
        db_sess.query(File).filter_by(passport_id=passport.id).delete()

        # удаляем все ответы в опросах данной организации
        for process in (
            db_sess
            .query(Process)
            .filter_by(passport_id=passport.id)
                .all()):
            db_sess.query(Answer).filter_by(process_id=process.id).delete()

        # удаляем все процессы опроса данной организации
        db_sess.query(Process).filter_by(passport_id=passport.id).delete()

        # удаляем все прикреплённые к данному паспорту логи
        db_sess.query(PassportLog).filter_by(passport_id=passport_id).delete()

        db_sess.delete(passport)  # удаление паспорта

        db_sess.commit()

    return response
