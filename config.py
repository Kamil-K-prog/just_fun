from typing import Optional, Union, Literal
import os


class BaseAppConfig(object):
    # Название СУБД + название драйвера (его не всегда обязательно указывать)
    # Например, 'postgresql+psycopg2'
    DB_DIALECT: str = ''
    DB_USERNAME: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    # Название БД (не СУБД) или относительный путь к файлу БД
    # Сюда только доверенный ввод, т.к. название вставляется в запрос f-строкой
    DB_NAME: Optional[str] = None
    # Аргументы при подключении к БД (ключи и значения - строки)
    DB_ARGS: dict[str, str] = {}

    # Указывает, как должны быть загружены связанные объекты ORM моделей и
    # их элементы. При изменении этого атрибута не требуется миграция БД.
    # Статья "Eager VS Lazy Loading in SQLAlchemy" https://clck.ru/sKobQ
    ORM_MODEL_RELATIONSHIP_LAZY_PARAM: (  # 'select' - это lazy-load
        Union[Literal['select'], Literal['joined']]) = 'joined'  # eager-load

    # Аргументы при создании движка SQLAlchemy
    ORM_ENGINE_ARGS: dict[str, object] = {'echo': False}

    # флаг, показювающий отправлять ли письма
    IS_SENDING_EMAILS: bool = False
    # адрес/хостнейм почтового сервера
    EMAIL_HOST: str = ''
    # порт почтового сервера
    EMAIL_PORT: int = 0
    # адрес почтового ящика, с которого приложение будет рассылать письма
    EMAIL_FROM: str = ''

    # название директории с файлами, загруженными пользователями системы
    UPLOAD_FOLDER: str = 'upload'

    # хост, на котором будет поднято WEB-приложение
    APP_HOST: str = '127.0.0.1'
    # порт, который будет прослушивать WEB-приложение
    APP_PORT: int = 8080

    # включен ли режим отладки
    APP_DEBUG: bool = False

    # Секретный ключ WSGI приложения Flask
    # SECRET_KEY: Optional[str] = os.environ.get('SECRET_KEY')
    SECRET_KEY: Optional[str] = '50eafa001ed07f3c92e0acb7da6d8c3c'


class ProductionAppConfig(BaseAppConfig):
    DB_DIALECT = 'mysql+mysqldb'
    DB_USERNAME = 'root'
    # os.environ.get('DB_PASSWORD')
    DB_PASSWORD = '1Q2w3e4r'
    DB_HOST = 'localhost'
    DB_PORT = 3306
    DB_NAME = 'labor_protection_monitoring'

    IS_SENDING_EMAILS = False
    EMAIL_HOST = 'www.uc.osu.ru'
    EMAIL_FROM = 'just_fun@gmail.com'

    DEBUG = False


class DevelopmentAppConfig(BaseAppConfig):
    DB_DIALECT = 'sqlite'
    DB_NAME = os.path.join('database', 'labor_protection_monitoring.sqlite')
    DB_ARGS = {'check_same_thread': 'False'}

    IS_SENDING_EMAILS = False

    DEBUG = True


# Обязательная переменная-алиас для работы приложения. Должна быть равна
# соответствующему по ситуации классу конфигурации (только не BaseAppConfig)
AppConfig = ProductionAppConfig
