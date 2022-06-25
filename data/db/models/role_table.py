from sqlalchemy import Column, Integer, Text
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase

class Role(SqlAlchemyBase):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = Column(Text, unique=True, nullable=False)

    user = orm.relation('User', back_populates='role')