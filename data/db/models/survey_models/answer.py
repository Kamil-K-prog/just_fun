from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase
from config import AppConfig


LAZY = AppConfig.ORM_MODEL_RELATIONSHIP_LAZY_PARAM


class Answer(SqlAlchemyBase):
    """Ответ в форме паспорта организации"""
    __tablename__ = 'answer'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # к какому процессу относится
    process_id = Column(Integer, ForeignKey('process.id'))

    # Какое именно поле заполнено
    field_id = Column(Integer, ForeignKey('field.id'))

    user_answer = Column(Text)  # Чем заполнено поле

    field = orm.relationship('Field', back_populates='answers', lazy=LAZY)
    process = orm.relationship('Process', back_populates='answers', lazy=LAZY)
