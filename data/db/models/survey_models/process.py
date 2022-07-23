from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import get_current_yekt_datetime, versatile_represent, \
    versatile_convert_to_str


class Process(SqlAlchemyBase, SerializerMixin):
    ("""Сущность процесса заполненния универсальной """
     """формы опроса конкретной организацией""")
    __tablename__ = 'process'

    serialize_only = ('id', 'passport_id', 'quiz_id', 'date')

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    passport_id = Column(Integer, ForeignKey('passport.id'), nullable=False)

    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)

    date = Column(Date, nullable=False, default=get_current_yekt_datetime)

    # Связи many-to-one:
    passport = orm.relationship('Passport', lazy='select')

    quiz = orm.relationship('Quiz', lazy='select')

    # Связи one-to-many:
    answers = orm.relationship('Answer', lazy='select')

    __repr__ = versatile_represent

    __str__ = versatile_convert_to_str
