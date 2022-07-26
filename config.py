class AppConfig:
    DB_DIRNAME = 'database'
    DB_FILENAME = 'safemonitoring.sqlite'

    # Указывает, как должны быть загружены
    # связанные объекты ORM моделей и их элементы.
    # При изменении не требует миграции бд.
    # Статья "Eager VS Lazy Loading in SQLAlchemy" https://clck.ru/sKobQ
    # ORM_MODEL_RELATIONSHIP_LAZY_PARAM = 'select' # lazy-load
    ORM_MODEL_RELATIONSHIP_LAZY_PARAM = 'joined'  # eager-load

    IS_SENDING_EMAILS = False  # флаг, показювающий отправлять ли письма
    EMAIL_HOST = 'www.uc.osu.ru'  # адрес почтового сервера
    # адрес почтового ящика, с которого приложение будет рассылать письма
    EMAIL_FROM = 'just_fun@gmail.com'

    # название директории и файлами, загруженными пользователями системы
    UPLOAD_FOLDER = 'upload/'

    # Секретный ключ WSGI приложения Flask
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = '50eafa001ed07f3c92e0acb7da6d8c3c'
