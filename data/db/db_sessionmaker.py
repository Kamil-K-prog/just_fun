from typing import Optional

import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy.engine import Engine, URL as EngineURL


from .sqlalchemy_base_maker import SqlAlchemyBase


class DatabaseInitError(Exception):
    ("""Класс исключения, сообщающего об ошибке инициализации соединения БД """
     """и всех необходимых объектов для работы с БД""")


_factory: Optional[type] = None  # Для реализации "Фабричного метода"


def create_session() -> orm.Session:
    """Возвращает объект ORM-сессии SQLAlchemy"""
    global _factory

    if _factory is None:
        raise DatabaseInitError(
            'Перед созданием сессии БД необходимо произвести '
            'инициализацию соединения БД с помощью функции создания'
            'экземпляра класса DatabaseGlobalInitializer')

    return _factory()


def _get_sqlalchemy_exception_code(
        sqlalchemy_exc: sqlalchemy.exc.SQLAlchemyError) -> Optional[int]:
    """Возвращает None или код ошибки СУБД по исключению SQLAlchemy"""
    # Формат строки, хранящейся в первом аргументе исключения SQLAlchemy:
    # (Название класса исключения бэкенда БД) (Код, "Сообщение с ошибкой")

    if not (hasattr(sqlalchemy_exc, 'args') and sqlalchemy_exc.args):
        return None
    url_temp_list = sqlalchemy_exc.args[0].split('(', maxsplit=2)

    if len(url_temp_list) < 3:
        return None
    url_temp_list = url_temp_list[2].split(',', maxsplit=1)

    if not (url_temp_list and url_temp_list[0].isdigit()):
        return None
    return int(url_temp_list[0])


class DatabaseGlobalInitializer(object):
    _AppConfigClass: type = ...
    _engine_url: EngineURL = ...
    _engine: Engine = ...

    _is_creating_db: bool = True
    _mysql_1049_error_fixer_already_worked: bool = False

    def __init__(self, AppConfigClass: type, create_db: bool = True) -> None:
        ("""Совершает глобальную инициализацию соедидения с БД. """
         """Если таковая уже проводилась, то ничего не делает. """
         """Если таблицы в соответствии с ORM-моделями не созданы, создает."""
         """Использует паттерн проектирования "Фабричный метод". """
         """Принимает класс конфигурации приложения. \n"""
         """ВАЖНО: у этого класса извне вызывайте только инициализатор!""")

        global _factory

        if _factory:  # если всё уже инициализировано, выходим
            return None

        self._AppConfigClass: type = AppConfigClass

        self._is_creating_db: bool = create_db

        # создаём URL для нового объект движка
        self._create_engine_url_from_config()

        # создаём объект движка SQLAlchemy
        self._create_engine()

        # продолжаем в "приватной" функции принудит. инициализации
        self._force_global_init()

    def _create_engine_url_from_config(self) -> None:
        """Создает URL по конфигурации для начала работы движка SQLAlchemy"""
        self._engine_url: EngineURL = EngineURL.create(
            drivername=self._AppConfigClass.DB_DIALECT,
            username=self._AppConfigClass.DB_USERNAME,
            password=self._AppConfigClass.DB_PASSWORD,
            host=self._AppConfigClass.DB_HOST,
            port=self._AppConfigClass.DB_PORT,
            database=self._AppConfigClass.DB_NAME,
            query=self._AppConfigClass.DB_ARGS)

    def _force_global_init(self) -> None:
        ("""Принудительная глобальная инициализация соедидения с БД, то есть"""
         """ даже если таковая уже проводилась""")

        # ставим класс-фабрику ORM-сессий
        self._set_sessionmaker()
        # создаём таблицы по ORM-моделям, если ещё не созданы
        self._create_all_models()

    def _create_engine(self) -> None:
        """Создаёт движок SQLAlchemy по URL и классу конфигурации приложения"""
        try:
            self._engine: Engine = sqlalchemy.create_engine(
                self._engine_url, **self._AppConfigClass.ORM_ENGINE_ARGS)
        except (TypeError, ValueError) as exc:
            raise DatabaseInitError(
                'В аргументах класса конфигурации приложения, '
                'отвечающих за соединение с базой данных, '
                'указаны неправильные данные'
            ) from exc
        except sqlalchemy.exc.NoSuchModuleError as sa_exc:
            raise DatabaseInitError(
                'Указан неправильный диалект базы данных '
                'в классе конфигурации приложения'
            ) from sa_exc

    def _set_sessionmaker(self) -> None:
        """Перезаписывает класс, реализующий "Фабричный метод". """
        global _factory

        _factory = orm.sessionmaker(bind=self._engine)

    def _create_all_models(self) -> None:
        ("""Создаёт таблицы по ORM-моделям из модуля __all_models, при """
         """возникновении ошибок делегирует поведение специальной для """
         """определённого диалекта SQLAlchemy функции""")

        # импортирем все ORM-модели, чтобы создать по ним таблицы в БД
        __import__('data.db.__all_models')

        try:
            SqlAlchemyBase.metadata.create_all(self._engine)
        except sqlalchemy.exc.SQLAlchemyError as sa_exc:

            # Если опция выполнения фичи включена и если мы используем MySQL
            if self._is_creating_db and self._is_mysql():
                # и если проблема в том, что БД езё не создана
                # то можно её создать и попробовать инициализацию снова
                self._mysql_create_db_if_not_exists_and_retry_init(sa_exc)
                return None

            raise DatabaseInitError(
                'Ошибка создания таблиц базы данных. '
                'Следовательно, прочая работа с базой данных тоже невозможна. '
                'Проверьте конфигурацию приложения. Например,учётные данные БД'
            ) from sa_exc

    def _is_mysql(self) -> bool:
        """Проверяет является ли MySQL диалектом данного движка SQLAlchemy"""
        return self._engine.dialect.name == 'mysql'

    def _mysql_create_db_if_not_exists_and_retry_init(
            self, sa_exc: sqlalchemy.exc.SQLAlchemyError):
        ("""Проверяет по исключению - ошибка из-за отсутствия БД или нет. """
         """Если это так, и при этом в классе конфигурации приложения """
         """указано название БД, то создаёт движок для сервера и создаёт """
         """новую БД после чего ещё раз проделывает инициализацию. """)
        if self._mysql_1049_error_fixer_already_worked or \
                not self._is_creating_db:
            # Эта функция изменяет внешние объекты только единожды,
            # чтобы не попасть в бесконечный цикл лишней работы.
            # Если функция уже отработала, то при след. вызове бездействует
            return None

        # Функция продолжит работу только если диалект движка - mysql и
        # исключение было поднято из-за запроса отсутствующей базы данных
        if not self._mysql_is_db_missing(sa_exc):
            return None  # иначе, естественно, функция ничего не будет делать

        # Если в конфиге не указано название БД, то, увы, ничего не получится
        db_name = self._AppConfigClass.DB_NAME
        if not db_name:
            raise DatabaseInitError(
                'Если при создании объекта глобального инициализатора БД '
                'create_db == True, то в классе конфигурации приложения '
                'обязательно должно быть указано название базы данных')

        # создаём новый URL, используя старый, но уже для движка сервера
        mysql_server_engine_url = self._engine.url._replace(database=None)

        # создаём объект движка SQLAlchemy сервера MySQL
        mysql_server_engine = sqlalchemy.create_engine(mysql_server_engine_url)

        try:  # создаём БД по названию из конфига (только доверенный ввод)
            mysql_server_engine.execute(
                f'CREATE DATABASE IF NOT EXISTS {db_name}')
        except sqlalchemy.exc.ProgrammingError as sa_prog_exc:
            raise DatabaseInitError(
                'Неправильное для MySQL название базы данных. Проверьте'
            ) from sa_prog_exc

        # ставим флаг, что отработали
        self._mysql_1049_error_fixer_already_worked = True

        # теперь можно попробовать сделать ещё попытку продолжить инициализацию
        self._force_global_init()

    def _mysql_is_db_missing(
            self, sa_exc: sqlalchemy.exc.SQLAlchemyError) -> bool:
        ("""Возвращает истину, если движок с диалектом MySQL и если данное """
         """исключение было поднято из-за отстутствия запрашиваемой БД""")

        if not self._is_mysql():
            return False

        sa_exc_code = _get_sqlalchemy_exception_code(sa_exc)
        # (MySQLdb.OperationalError) (1049, "Unknown database '{db_name}'")
        return sa_exc_code == 1049
