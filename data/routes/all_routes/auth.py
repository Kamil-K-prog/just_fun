from flask import Blueprint, Response, render_template, redirect
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
)
from data.db import db_sessionmaker

from ...db.__all_models import User
from ...db.__all_models import Role

from ..flask_wtf_forms import LoginForm, RegisterForm   # формы FlaskWTF


def register_login_manager(app):
    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id: int):
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return None

        with db_sessionmaker.create_session() as db_sess:
            return db_sess.query(User).get(user_id)


blueprint = Blueprint('auth', __name__, template_folder='templates')


@blueprint.route('/login/', methods=['GET', 'POST'])
def login() -> Response:
    user = current_user
    if not user.is_anonymous:
        if hasattr(user, 'role_id'):
            if user.role_id == 1:
                return redirect('/account')
            elif user.role_id == 2:
                return redirect('/admin')
        return redirect("/")

    form = LoginForm()
    form_name = 'front/LoginForm.html'

    if form.validate_on_submit():
        with db_sessionmaker.create_session() as db_sess:
            error_mes = None
            user = db_sess.query(User).filter_by(
                login=form.login.data.strip()).first()
            if user is None:
                error_mes = 'Неправильный логин'
            elif not user.check_password(form.password.data.strip()):
                error_mes = 'Неправильный пароль'
            if error_mes:
                return render_template(form_name, form=form, message=error_mes)
            login_user(user, remember=form.remember_me.data)
            if hasattr(user, 'role_id'):
                if user.role_id == 1:
                    return redirect('/account')
                elif user.role_id == 2:
                    return redirect('/admin')
            return redirect('/')

    return render_template(form_name, form=form)


@blueprint.route('/register/', methods=['GET', 'POST'])
def register() -> Response:
    user = current_user
    if not user.is_anonymous:
        if hasattr(user, 'role_id'):
            if user.role_id == 1:
                return redirect('/account')
            elif user.role_id == 2:
                return redirect("/")

    form = RegisterForm()
    form_name = 'front/RegisterForm.html'
    err_mes = None

    if form.validate_on_submit():

        with db_sessionmaker.create_session() as db_sess:
            user = db_sess.query(User).filter_by(
                login=form.login.data.strip()).first()
            if user is not None:
                err_mes = 'Пользователь с таким логином уже существует!'
            user = db_sess.query(User).filter_by(
                email=form.email.data.strip()).first()
            if user is not None:
                err_mes = 'Пользователь с такой почтой уже существует!'
            if err_mes:
                return render_template(form_name, form=form, message=err_mes)
            user = User(
                login=form.login.data.strip(),
                passwd_hash='',
                email=form.email.data.strip(),
                role_id=db_sess.query(
                    Role).filter_by(name='User').first().id)
            user.set_password(form.password.data.strip())
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')

    return render_template(form_name, form=form)


@blueprint.route('/logout/', methods=['GET', 'POST'])
def logout() -> Response:
    logout_user()
    return redirect('/')
