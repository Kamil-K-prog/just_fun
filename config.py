import os


class AppConfig:
    DB_DIRNAME = 'database'
    DB_FILENAME = '!!!название бд!!!.sqlite'
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
    ('50eafa001ed07f3c92e0acb7da6d8c3c')
