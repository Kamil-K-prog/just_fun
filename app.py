import os
from flask import Flask
from config import AppConfig
from data.db import db_sessionmaker
from data.interface.all_interface import auth
from data.interface import interface_manager
from data.db.models.user_table import User

app = Flask(__name__)
app.config.from_object(AppConfig)

if __name__ == '__main__':
    db_path = os.path.join(
        app.config['DB_DIRNAME'],
        app.config['DB_FILENAME'])
    db_sessionmaker.global_init(db_path)

    auth.register_login_manager(app)
    app.register_blueprint(auth.blueprint)
    interface_manager.global_interface_init(app)
    app.run(host='127.0.0.1', port=8080, debug=True)