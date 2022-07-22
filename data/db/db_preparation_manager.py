from . import db_sessionmaker
from .__all_models import Role, PassportStatus, FieldType, EvalMarkProfrisks, \
    EvalMarkSout, Location


LOCATIONS = ('Оренбург', 'Тюмень',  'Орск', 'Сорочинск', 'Бугуруслан', 'Гай')
EVAL_MARK_CONTENTS = ('Да', 'Нет', 'Частично')  # метки качества соблюдения
PREPARATION_DATA = [  # Константа с обязательными записями БД (см. prepare_db)
    # Роли пользователей
    {'model': Role, 'name_field': 'name', 'contents': ('User', 'Admin')},
    # Статусы паспортов организаций
    {'model': PassportStatus, 'name_field': 'name',
     'contents': ('Принят', 'На рассмотрении', 'Отклонен')},
    # Типы полей в универсальной форме опросника
    {'model': FieldType, 'name_field': 'name', 'contents': (
        'Свободное текстовое поле', 'Текстовое поле с вариантами ответов',
        'Дата', 'Число', 'Загрузка файла')},
    # Метки качества и наличия оценки профессиональных рисков
    {'model': EvalMarkProfrisks, 'name_field': 'title',
        'contents': EVAL_MARK_CONTENTS},
    # Метки качества и наличия специальной оценки условий труда (СОУТ)
    {'model': EvalMarkSout, 'name_field': 'title',
        'contents': EVAL_MARK_CONTENTS},
    {'model': Location, 'name_field': 'name', 'contents': LOCATIONS}
]


def prepare_db() -> None:
    ("""Производит обязательные для корректной работы web-приложения записи """
     """в базу данных, если на данный момент таковых в ней нет""")

    with db_sessionmaker.create_session() as db_sess:
        for essential_dict in PREPARATION_DATA:
            model = essential_dict['model']  # класс ORM-модели
            name_field = essential_dict['name_field']  # название поля названия

            for model_obj_id, obj_name_value in enumerate(
                    essential_dict['contents'], start=1):
                # очередной обязательный для работы приложения объект модели
                model_obj = db_sess.query(model).get(model_obj_id)

                if model_obj is None:  # если ещё не создан, создаём
                    model_obj = model(
                        id=model_obj_id, **{name_field: obj_name_value})

                    db_sess.add(model_obj)

        db_sess.commit()
