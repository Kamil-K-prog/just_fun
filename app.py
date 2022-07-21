import os
from flask import Flask
from config import AppConfig
from data.db import db_sessionmaker
from data.routes.all_routes import auth
# from data.routes import routes_manager  # заглушено на время интеграции с бд
from flask import render_template


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
    
    # заглушено на время интеграции с бд
    # routes_manager.global_routes_init(app)
    app.run(host='127.0.0.1', port=8080, debug=True)
