from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase
from config import AppConfig


LAZY = AppConfig.ORM_MODEL_RELATIONSHIP_LAZY_PARAM


class Field(SqlAlchemyBase):
    """Поле универсальной формы для сбора информации"""
    __tablename__ = 'field'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    quiz_id = Column(Integer, ForeignKey('quiz.id'))

    title = Column(Text)
    field_type_id = Column(Integer, ForeignKey('field_type.id'))

    # Связи many-to-one:
    quiz = orm.relationship('Quiz', lazy='select')
    field_type = orm.relationship(
        'FieldType', back_populates='fields', lazy=LAZY)

    # Связи one-to-many
    answers = orm.relationship('Answer', lazy='select')
