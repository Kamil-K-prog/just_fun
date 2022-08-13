from typing import Optional, Union, Literal, Dict
import os


class BaseAppConfig(object):
    """Базовый конфиг (сам по себе не может быть применён)"""
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
    DB_ARGS: Dict[str, str] = {}

    # Указывает, как должны быть загружены связанные объекты ORM моделей и
    # их элементы. При изменении этого атрибута не требуется миграция БД.
    # Статья "Eager VS Lazy Loading in SQLAlchemy" https://clck.ru/sKobQ
    ORM_MODEL_RELATIONSHIP_LAZY_PARAM: (  # 'select' - это lazy-load
        Union[Literal['select'], Literal['joined']]) = 'joined'  # eager-load

    # Аргументы при создании движка SQLAlchemy
    ORM_ENGINE_ARGS: Dict[str, object] = {'echo': False}

    # Аргументы, передаваемые в специальный атрибут __table_args__ ORM-моделей
    DB_TABLE_ARGS: Dict[str, str] = {}

    # Аргументы запросов с оператором PRAGMA (при отсутствии запросов не будет)
    # Сюда только доверенный ввод, т.к. название вставляется в запрос f-строкой
    DB_PRAGMA_ARGS: Dict[str, str] = {}

    # флаг, показювающий отправлять ли письма
    IS_SENDING_EMAILS: bool = False
    # адрес/хостнейм почтового сервера
    EMAIL_HOST: str = 'www.uc.osu.ru'
    # порт почтового сервера
    EMAIL_PORT: int = 0
    # адрес почтового ящика, с которого приложение будет рассылать письма
    EMAIL_FROM: str = 'just_fun@gmail.com'

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


class MySqlAppConfig(BaseAppConfig):
    """Конфиг приложения, использующего MySQL в качестве СУБД"""
    DB_DIALECT = 'mysql+mysqldb'
    DB_USERNAME = 'root'
    # DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_PASSWORD = '1Q2w3e4r'
    DB_HOST = 'localhost'
    DB_PORT = 3306
    DB_NAME = 'labor_protection_monitoring'

    # InnoDB - одна из подсистем низкого уровня в СУБД MySQL, поддерживающая
    # механизмы транзакций и внешних ключей, сохраняющая тем самым ссылочную
    # целостность БД. Опция mysql_charset ставит кодировку символов БД на UTF-8
    DB_TABLE_ARGS = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}


class SqliteAppConfig(BaseAppConfig):
    """Конфиг приложения, использующего sqlite в качестве СУБД"""
    DB_DIALECT = 'sqlite'
    DB_NAME = os.path.join('database', 'labor_protection_monitoring.sqlite')
    DB_ARGS = {'check_same_thread': 'False'}

    # Таким образом сохраняется ссылочная целостность при мутабельных ID
    # При этих аргументах sqlite должна быть скомпилирована без следующих опций
    # SQLITE_OMIT_FOREIGN_KEY или SQLITE_OMIT_TRIGGER
    # Версия sqlite должна быть 3.6.19 или новее
    # https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#sqlite-foreign-keys
    DB_PRAGMA_ARGS = {'foreign_keys': 'ON'}


class ProductionAppConfig(BaseAppConfig):
    """Конфигурация для продакшена"""
    IS_SENDING_EMAILS = True
    APP_DEBUG = False


class DevelopmentAppConfig(BaseAppConfig):
    """Конфигурация для разработки на локальной машине"""
    IS_SENDING_EMAILS = False
    APP_DEBUG = True


class AppConfig(MySqlAppConfig, DevelopmentAppConfig):
    """Текущий конфиг. Для настройки можно изменять опции наследования"""
