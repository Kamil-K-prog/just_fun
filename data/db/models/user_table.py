from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    serialize_only = (
        'id', 'login', 'email', 'role_id')

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    email = Column(Text, unique=True, nullable=False)
    login = Column(Text, unique=True, nullable=False)
    passwd_hash = Column(Text, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), default=1)

    photo = orm.relation('Photo', back_populates='user')
    video = orm.relation('Video', back_populates='user')
    role = orm.relation('Role')
    passport = orm.relation('Passport', back_populates='user')

    def set_password(self, new_password: str):
        self.passwd_hash = generate_password_hash(new_password)

    def check_password(self, password):
        return check_password_hash(self.passwd_hash, password)
