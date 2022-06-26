from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


# таблица для "Управление профрисками"

class Profrisk(SqlAlchemyBase):
    __tablename__ = 'profrisks'

    passport_id = Column(Integer, ForeignKey('passports.id'), primary_key=True, nullable=False, autoincrement=True,
                         unique=True)  # id организации
    profrisks_check = Column(Integer,
                             nullable=False)  # Проведена оценка профессиональных рисков в области охраны труда
    # да / нет / частично
    last_check_date = Column(Date, nullable=False)  #Дата проведения последней оценки профессиональных рисков

    passport = orm.relation('Passport')
