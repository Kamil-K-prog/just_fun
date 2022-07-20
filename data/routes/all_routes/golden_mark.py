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
from ...db.__all_models import User, Passport, PassportStatus, GoldenBadge

blueprint = Blueprint('golden_mark', __name__, template_folder='templates')
login_manager = LoginManager()


@blueprint.route('/admin_gold_confirm/<pass_id>', methods=['GET', 'POST'])  # подтверждение выдачи золотого знака
@login_required
@is_admin
def Admin_GoldConfirm_Form(pass_id):
    db_sess = db_sessionmaker.create_session()
    pass_obj = db_sess.query(Passport).filter_by(id=pass_id).first()
    gd_app = db_sess.query(GoldenBadge).filter_by(
        passport_id=pass_id).first()
    pass_obj.golden_mark = True
    pass_obj.golden
    gd_app.application_verdict = True
    user = db_sess.query(User).filter_by(id=pass_obj.user_id).first()
    db_sess.add(pass_obj)
    db_sess.add(gd_app)
    db_sess.commit()
    send_mail(user.login, user.email, 'You have been given a golden badge',
          'Congratulations to your organization')
    return redirect('/admin_bids')


@blueprint.route('/admin_gold_decline/<pass_id>', methods=['GET', 'POST'])  # отказ в выдаче золотого знака
@login_required
@is_admin
def Admin_GoldDecline_Form(pass_id):
    db_sess = db_sessionmaker.create_session()
    pass_obj = db_sess.query(Passport).filter_by(id=pass_id).first()
    gd_app = db_sess.query(GoldenBadge).filter_by(
        passport_id=pass_id).first()
    pass_obj.golden_mark = False
    gd_app.application_verdict = False
    user = db_sess.query(User).filter_by(id=pass_obj.user_id).first()
    db_sess.add(pass_obj)
    db_sess.add(gd_app)
    db_sess.commit()
    send_mail(user.login, user.email, 'Gold badge application rejected',
          'Contact the administrator for clarification')
    return redirect('/admin_bids')