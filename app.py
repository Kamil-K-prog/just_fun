import os
from flask import Flask
from config import AppConfig
from data.db import db_sessionmaker, db_preparation_manager
from data.routes.all_routes import auth
from data.routes import routes_manager
from data.errorhandling_http import register_errorhandlers


app = Flask(__name__)
app.config.from_object(AppConfig)


if __name__ == '__main__':
    db_path = os.path.join(
        app.config['DB_DIRNAME'],
        app.config['DB_FILENAME'])

    db_sessionmaker.global_init(db_path)
    db_preparation_manager.prepare_db()
    auth.register_login_manager(app)
    app.register_blueprint(auth.blueprint)
    routes_manager.global_routes_init(app)
    register_errorhandlers(app)
    app.run(host='127.0.0.1', port=8080, debug=True)
