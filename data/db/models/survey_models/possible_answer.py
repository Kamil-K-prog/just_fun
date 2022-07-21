from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase


class PossibleAnswer(SqlAlchemyBase, SerializerMixin):
    ("""Возможный вариант ответа на определённое поле универсальной """
     """формы опроса""")
    __tablename__ = 'possible_answer'

    serialize_only = ('id', 'possible_answer', 'field_id')

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)

    possible_answer = Column(Text, nullable=False)

    # Связи many-to-one:
    field = orm.relationship(
        'Field', back_populates='possible_answers', lazy='select')
