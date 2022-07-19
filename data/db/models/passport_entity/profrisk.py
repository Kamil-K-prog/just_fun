from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase


class Profrisk(SqlAlchemyBase):
    ("""Управление профессиональными рисками """
     """в организации""")
    __tablename__ = 'profrisk'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    passport_id = Column(
        Integer, ForeignKey('passport.id'),
        nullable=False, unique=True)

    # Проведена оценка профрисков в области охраны труда
    # 1 - да
    # 2 - нет
    # 3 - частично
    profrisks_check = Column(
        Integer, nullable=False)
    # Дата проведения последней оценки профрисков
    last_check_date = Column(Date, nullable=False)

    passport = orm.relationship('Passport', lazy='select')
