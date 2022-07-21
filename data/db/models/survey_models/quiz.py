from sqlalchemy import Column, Integer, Text
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase
from config import AppConfig


LAZY = AppConfig.ORM_MODEL_RELATIONSHIP_LAZY_PARAM


class Quiz(SqlAlchemyBase, SerializerMixin):
    ("""Сущность универсальной формы опросника """
     """для сбора информации об охране труда в организациях""")
    __tablename__ = 'quiz'

    serialize_only = ('id', 'title')

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    title = Column(Text, nullable=False)  # Название квиза

    # Связи one-to-many:
    fields = orm.relationship('Field', back_populates='quiz', lazy=LAZY)
    processes = orm.relationship('Process', back_populates='quiz', lazy=LAZY)
