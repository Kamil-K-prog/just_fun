# from flask import Flask

from config import AppConfig
from data.db import db_sessionmaker, db_preparation_manager
# from data.routes.all_routes import auth
# from data.routes import routes_manager
# from data import errorhandling_http


if __name__ == '__main__':
    # app = Flask(__name__)
    # app.config.from_object(AppConfig)

    db_sessionmaker.DatabaseGlobalInitializer(AppConfig)
    db_preparation_manager.prepare_db()

    # auth.register_login_manager(app)
    # app.register_blueprint(auth.blueprint)

    # routes_manager.global_routes_init(app)

    # errorhandling_http.register_errorhandlers(app)

    # app.run(
    #     host=app.config['APP_HOST'],
    #     port=app.config['APP_PORT'],
    #     debug=app.config['APP_DEBUG'])
