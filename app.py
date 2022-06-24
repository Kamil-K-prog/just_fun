import os
from flask import Flask
from config import AppConfig
from data.db import db_sessionmaker
from data.rest import rest_api_manager
from data.interface import interface_manager

app = Flask(__name__)
app.config.from_object(AppConfig)

if __name__ == '__main__':
    db_path = os.path.join(
        app.config['DB_DIRNAME'],
        app.config['DB_FILENAME'])
    db_sessionmaker.global_init(db_path)
    rest_api_manager.global_api_init(app)
    interface_manager.global_interface_init(app)
    app.run(host='127.0.0.1', port=8080, debug=True)
