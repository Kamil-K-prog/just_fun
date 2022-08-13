from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import versatile_represent, versatile_convert_to_str
from config import AppConfig


LAZY = AppConfig.ORM_MODEL_RELATIONSHIP_LAZY_PARAM


class Answer(SqlAlchemyBase, SerializerMixin):
    """Ответ в форме паспорта организации"""
    __tablename__ = 'answer'
    __table_args__ = AppConfig.DB_TABLE_ARGS

    serialize_only = ('id', 'process_id', 'field_id', 'user_answer')

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # к какому процессу относится
    process_id = Column(Integer, ForeignKey('process.id'), nullable=False)

    # Какое именно поле заполнено
    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)

    user_answer = Column(Text, nullable=False)  # Чем заполнено поле

    # Связи many-to-one:
    field = orm.relationship('Field', back_populates='answers', lazy=LAZY)
    process = orm.relationship('Process', back_populates='answers', lazy=LAZY)

    __repr__ = versatile_represent

    __str__ = versatile_convert_to_str
