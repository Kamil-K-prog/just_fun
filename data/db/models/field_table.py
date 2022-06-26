from sqlalchemy import Column, Integer, Text, ForeignKey, Date, Boolean
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class Field(SqlAlchemyBase):
    __tablename__ = 'fields'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    title = Column(Text)  # Название
    type = Column(Text)  # Тип
    quiz_id = Column(Integer, ForeignKey('quizes.id'))
    