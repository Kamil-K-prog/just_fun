from flask import Blueprint, Response, render_template, redirect, abort
from flask_login import login_required, current_user

from ...db import db_sessionmaker
from ...db.db_utils import get_current_yekt_datetime
from ...db.__all_models import User, Passport
from ..flask_wtf_forms import GoldenBadgeApplicationForm
from .middleware import is_user


blueprint = Blueprint('user_interface', __name__, template_folder='templates')


@blueprint.route('/account/', methods=['GET', 'POST'])
@login_required
@is_user
def account() -> Response:
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
        'back/passport_form.html',
        user=user,
        title='Личный кабинет',
        organizations=passports_list)


@blueprint.route('/golden_badge/', methods=['GET', 'POST'])
@login_required
@is_user
def golden_badge() -> Response:
    user: User = current_user

    with db_sessionmaker.create_session() as db_sess:

        form = GoldenBadgeApplicationForm()
        if form.validate_on_submit():
            passport: Passport = db_sess.query(
                Passport).get(form.organization_id.data)

            if passport is None:
                return redirect('/golden_badge/')

            passport.golden_badge_application_date = (
                get_current_yekt_datetime())
            passport.golden_badge_verdict = False
            passport.golden_badge_verification_date = None
            db_sess.commit()

            return redirect('/golden_badge/')

    return render_template(
        'back/golden_badge.html',
        user=user,
        title='Золотой знак',
        form=form,
        passports=(
            pass_obj for pass_obj in user.passports
            if pass_obj.golden_badge_application_date is not None))


@blueprint.route(
    '/delete_application/<int:passport_id>/', methods=['GET', 'POST'])
@login_required
@is_user
def delete_application(passport_id: int) -> Response():
    user: User = current_user

    with db_sessionmaker.create_session() as db_sess:
        passport: Passport = db_sess.query(Passport).get(passport_id)

        if passport is None:
            abort(404, description='Паспорт с таким id не найден')

        # защита от удаления чужой заявки на статус "Золотой знак"
        if user.role_id != 2 and user.id != passport.user_id:
            abort(403, description='Вам запрещено совершать это действие')

        passport.golden_badge_application_date = None
        passport.golden_badge_verdict = False
        passport.golden_badge_verification_date = None

        db_sess.commit()

    return redirect('/golden_badge')
