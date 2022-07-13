from flask import Blueprint, session, jsonify, render_template, redirect
from flask import request as req
from requests import request
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
from ...db.__all_models import User, Passport, Video, Photo

blueprint = Blueprint('file_save', __name__, template_folder='templates')
login_manager = LoginManager()

UPLOAD_FOLDER = 'upload/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# доступные расширения файлов, типа mime-типы =)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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

