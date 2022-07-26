from flask import Blueprint, Response, redirect, abort
from flask_login import login_required

from ...db import db_sessionmaker
from ...db.__all_models import User, Passport, PassportStatus
from ...db.db_utils import get_current_yekt_datetime
from .middleware import is_admin
from .mail_sender import send_mail


blueprint = Blueprint('golden_mark', __name__, template_folder='templates')


@blueprint.route('/admin_gold_confirm/<int:pass_id>/', methods=['GET', 'POST'])
@login_required
@is_admin
def admin_golden_badge_confirm(pass_id: int) -> Response:
    """Подтверждение выдачи золотого знака"""

    with db_sessionmaker.create_session() as db_sess:
        pass_obj: Passport = db_sess.query(Passport).get(pass_id)

        if pass_obj is None:
            abort(404, description='Паспорт с таким id не найден')

        pass_obj.golden_badge_verdict = True
        pass_obj.golden_badge_verification_date = get_current_yekt_datetime()

        # если сам паспорт ещё не подтверждён, подтверждаем
        pass_obj.passport_status_id = db_sess.query(PassportStatus).filter_by(
            name='Принят').first().id

        db_sess.commit()

        passport_owner: User = pass_obj.user
        send_mail(
            passport_owner.login, passport_owner.email,
            'You have been given a golden badge',
            'Congratulations to your organization')

    return redirect('/admin_bids')


@blueprint.route('/admin_gold_decline/<int:pass_id>/', methods=['GET', 'POST'])
@login_required
@is_admin
def admin_golden_badge_decline(pass_id: int) -> Response:
    """Отказ в выдаче золотого знака"""
    with db_sessionmaker.create_session() as db_sess:
        pass_obj: Passport = db_sess.query(Passport).get(pass_id)

        if pass_obj is None:
            abort(404, description='Паспорт с таким id не найден')

        pass_obj.golden_badge_verdict = False
        pass_obj.golden_badge_verification_date = None
        pass_obj.golden_badge_application_date = None

        db_sess.commit()

        passport_owner: User = pass_obj.user
        send_mail(
            passport_owner.login, passport_owner.email,
            'Gold badge application rejected',
            'Contact the administrator for clarification')

    return redirect('/admin_bids')
