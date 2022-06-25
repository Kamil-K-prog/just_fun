from sqlalchemy import Column, Integer, Text, ForeignKey, Date, Boolean
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class Quiz(SqlAlchemyBase):
    __tablename__ = 'quizes'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    title = Column(Text)  # название
    data = Column(Text)  # данные
    organizer = Column(Text)  # организатор

