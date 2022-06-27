from sqlalchemy import Column, Integer, Text, ForeignKey, Date, Boolean
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class GoldenMarkApplication(SqlAlchemyBase):
    __tablename__ = 'golden_mark_applications'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    passport_id = Column(Integer, ForeignKey('passports.id'))  # кто подал заявку
    application_date = Column(Text, nullable=False)  # дата подачи
    application_verdict = Column(Boolean, default=0)  # вердикт

    passport = orm.relation('Passport')
