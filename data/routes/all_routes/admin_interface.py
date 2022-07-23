from flask import Blueprint, Response, render_template, redirect, abort, \
    request
from flask_login import login_required, current_user

from ...db import db_sessionmaker
from ...db.__all_models import User, Quiz, Field, Passport
from ..flask_wtf_forms import AdminAddForm
from .middleware import is_admin


blueprint = Blueprint('admin_interface', __name__, template_folder='templates')


@blueprint.route('/admin/', methods=['GET', 'POST'])
@login_required
@is_admin
def passports() -> Response:
    """Главная страница администратора. Управление паспортами"""
    user: User = current_user

    user_passports = user.passports

    passports_list = [None] * len(user_passports)
    for index, pass_obj in enumerate(user_passports):
        passports_list[index] = {
            'id': pass_obj.id,
            'organization_short_name': pass_obj.organization_short_name,
            'date': pass_obj.date_of_application_editing,
            'golden_mark': pass_obj.golden_badge_verdict,
            'status': pass_obj.status.name}

    return render_template(
        'back/admin.html',
        user=user,
        title='Паспорта',
        passports=passports_list)


@blueprint.route('/admin_bids/', methods=['GET', 'POST'])
@login_required
@is_admin
def admin_bids() -> Response:
    user: User = current_user

    with db_sessionmaker.create_session() as db_sess:
        all_passports = db_sess.query(Passport).all()

        passports_list = [None] * len(all_passports)
        for index, pass_obj in enumerate(all_passports):
            passports_list[index] = {
                'id': pass_obj.id,
                'organization_short_name': pass_obj.organization_short_name,
                'date': pass_obj.golden_badge_application_date,
                'status': pass_obj.golden_badge_verdict}

    return render_template(
        'back/admin_bids.html',
        user=user,
        title='Сбор информации',
        apples=passports_list)


@blueprint.route('/admin_forms/', methods=['GET', 'POST'])
@login_required
@is_admin
def admin_forms() -> Response:
    user: User = current_user

    form = AdminAddForm()

    with db_sessionmaker.create_session() as db_sess:
        all_quizes = db_sess.query(Quiz).all()

        q_list = [None] * len(all_quizes)
        for index, _quiz in enumerate(all_quizes):
            q_list[index] = {'name': _quiz.title, 'id': _quiz.id}

        if form.validate_on_submit():
            if db_sess.query(Quiz).filter_by(title=form.name.data).first():
                return render_template(
                    'back/admin_forms.html',
                    user=user,
                    form=form,
                    title='Золотые знаки',
                    message='Форма с таким названием уже существует',
                    quizes=q_list)

            quiz = Quiz(title=form.name.data)
            db_sess.add(quiz)
            db_sess.commit()

            return redirect('/admin_forms')

    return render_template(
        'back/admin_forms.html',
        user=user,
        form=form,
        title='Золотые знаки',
        quizes=q_list)


@blueprint.route('/admin_delete_form/<int:quiz_id>/', methods=['GET', 'POST'])
@login_required
@is_admin
def admin_del_quiz(quiz_id: int) -> Response:
    with db_sessionmaker.create_session() as db_sess:
        db_sess.query(Quiz).filter_by(id=quiz_id).delete()
        db_sess.commit()

    return redirect('/admin_forms')


@blueprint.route('/admin_edit_form/<int:quiz_id>/', methods=['GET', 'POST'])
@login_required
@is_admin
def admin_edit_quiz(quiz_id: int) -> Response:
    user: User = current_user

    form = AdminAddForm()

    with db_sessionmaker.create_session() as db_sess:
        quiz: Quiz = db_sess.query(Quiz).get(quiz_id)

        if quiz is None:
            abort(404, description='Квиз с таким id не найден')

        fields = quiz.fields

        if form.validate_on_submit():
            field_type = request.form.get("type_field")
            f = Field(title=form.name.data, type=field_type, quiz_id=quiz_id)
            db_sess.add(f)
            db_sess.commit()
            return redirect(f'/admin_edit_form/{quiz_id}/')

    return render_template(
        'back/admin_edit_form.html',
        user=user,
        title='Страница редактирования',
        fields=fields,
        qz_id=quiz_id,
        form=form)


@blueprint.route(
    '/admin_field_del/<int:field_id>/<int:quiz_id>/', methods=['GET', 'POST'])
@login_required
@is_admin
def admin_del_field(field_id: int, quiz_id: int) -> Response:
    with db_sessionmaker.create_session() as db_sess:
        db_sess.query(Field).filter_by(id=field_id).delete()
        db_sess.commit()
    return redirect(f'/admin_edit_form/{quiz_id}/')
