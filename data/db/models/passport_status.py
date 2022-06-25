from sqlalchemy import Column, Integer, Text
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class PassportStatus(SqlAlchemyBase):
    __tablename__ = 'password_statuses'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = Column(Text, unique=True, nullable=False)

    passport = orm.relation('Passport', back_populates='status')