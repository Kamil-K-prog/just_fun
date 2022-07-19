from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import get_current_yekt_datetime


class Process(SqlAlchemyBase):
    __tablename__ = 'process'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    passport_id = Column(Integer, ForeignKey('passport.id'))

    quiz_id = Column(Integer, ForeignKey('quiz.id'))

    date = Column(Date, nullable=False, default=get_current_yekt_datetime)

    # Связи many-to-one:
    passport = orm.relationship('Passport', lazy='select')

    quiz = orm.relationship('Quiz', lazy='select')

    # Связи one-to-many:
    answers = orm.relationship('Answer', lazy='select')
