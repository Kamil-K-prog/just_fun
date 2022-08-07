from typing import List
import os
import urllib.request
from urllib.error import URLError

from flask import Blueprint, Response, render_template, request, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from ...db import db_sessionmaker
from ...db.__all_models import User, Passport, Video, File
from .middleware import is_user
from config import AppConfig


blueprint = Blueprint('file_save', __name__, template_folder='templates')


# Доступные расширения файлов (MIME-типы)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename: str) -> bool:
    ("""Возвращает булевое значение, показывающее является ли название """
     """файла допустимым""")
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def is_hex_str(string: str) -> bool:
    """Проверяет является ли строка шестнадцатеричной"""
    HEX_ALPHABET = '01234567890abcdef'
    for symbol in string.lower():
        if symbol not in HEX_ALPHABET:
            return False
    return True


def check_web_page_status(url: str, http_status: int = 200) -> bool:
    """Проверяет статус ответа сервера на определённый url"""
    try:
        with urllib.request.urlopen(url) as http_response:
            return http_response.status == http_status
    except URLError:
        return False


def is_valid_rutube_url(url: str) -> bool:
    """Проверяет является ли url на видео rutube валидным"""
    url_list = url.split('/', maxsplit=5)

    if len(url_list) < 5:
        return False

    if not url_list[-1]:
        url_list.pop()

    video_id_str = url_list.pop()
    if len(video_id_str) != 32 or not is_hex_str(video_id_str) or (
            url_list[0] not in ('https:', 'http:')) or (
                url_list[1:] != ['', 'rutube.ru', 'video']):
        return False

    return check_web_page_status(url=url, http_status=200)


def _render_response(
        user_obj: User,
        videos_list: List[Video],
        files_list=List[File],
        sent_msg: str = ''):
    return render_template(
        'back/passport_upload.html',
        user=user_obj,
        title='Загрузка файлов',
        videos=videos_list,
        files=files_list,
        sent_msg=sent_msg)


@blueprint.route('/passport_upload/<int:pass_id>/', methods=['GET', 'POST'])
@login_required
@is_user
def passport_upload(pass_id: int) -> Response:
    user: User = current_user

    with db_sessionmaker.create_session() as db_sess:

        passport: Passport = db_sess.query(Passport).get(pass_id)

        if passport is None:
            abort(404, description='Паспорт с таким id не найден')

        if user.role_id != 2 and user.id != passport.user_id:
            abort(403, description='Вам запрещено совершать это действие')

        videos = passport.videos
        files = passport.files

        if request.method == 'POST':

            file = request.files['file']
            video_url: str = request.form['video_url'].strip()

            if not file or not allowed_file(file.filename):
                return _render_response(
                    user, videos, files,
                    'Файлы не прикреплены или недопустимы в целях безопасности'
                )

            if not is_valid_rutube_url(video_url):
                return _render_response(
                    user, videos, files,
                    'Неправильная ссылка на видео rutube')

            filename = secure_filename(file.filename)
            os.makedirs(AppConfig.UPLOAD_FOLDER, exist_ok=True)
            file.save(os.path.join(AppConfig.UPLOAD_FOLDER, filename))
            db_sess.add(File(passport_id=pass_id, filename=filename))
            db_sess.add(Video(passport_id=pass_id, link=video_url))
            db_sess.commit()

            return _render_response(
                user, videos, files,
                'Файлы и видео успешно отправлены и сохранены')

        return _render_response(user, videos, files)
