from sqlalchemy import Column, Integer, Text, ForeignKey, Date, Boolean
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class Answer(SqlAlchemyBase):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    process_id = Column(Integer, ForeignKey('processes.id'))  # к какому процессу относится
    field_id = Column(Integer, ForeignKey('fields.id'))  # Какое именно поле заполнено
    user_answer = Column(Text)  # Чем заполнено поле

    field = orm.relation('Field')
    process = orm.relation('Process')
