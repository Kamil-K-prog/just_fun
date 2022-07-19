from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase


class GoldenMarkApplication(SqlAlchemyBase):
    """Статус 'Золотого знака' организации"""
    __tablename__ = 'golden_mark_application'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    passport_id = Column(
        Integer, ForeignKey('passport.id'),
        nullable=False, unique=True)

    application_date = Column(Date, nullable=False)  # дата подачи
    # вердикт
    application_verdict = Column(Boolean, nullable=False, default=False)

    passport = orm.relationship('Passport', lazy='select')
