import os
from flask import Flask
from config import AppConfig
from data.db import db_sessionmaker
from data.interface.all_interface import auth
from data.interface import interface_manager
from flask import render_template
from data.db.models.user_table import User

app = Flask(__name__)
app.config.from_object(AppConfig)
app.config['UPLOAD_FOLDER'] = "/upload"


if __name__ == '__main__':
    db_path = os.path.join(
        app.config['DB_DIRNAME'],
        app.config['DB_FILENAME'])
    app.config['UPLOAD_FOLDER'] = "/upload/"
    db_sessionmaker.global_init(db_path)
    auth.register_login_manager(app)
    app.register_blueprint(auth.blueprint)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(401)
    def page_not_found(e):
        return render_template('403.html'), 401

    interface_manager.global_interface_init(app)
    app.run(host='127.0.0.1', port=8080, debug=True)