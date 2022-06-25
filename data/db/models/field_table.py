from sqlalchemy import Column, Integer, Text, ForeignKey, Date, Boolean
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class Field(SqlAlchemyBase):
    __tablename__ = 'fields'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    title = Column(Text)  # Название
    data = Column(Text)  # Содержение
    type = Column(Text)  # Тип

    answer = orm.relation('Answer', back_populates='field')