from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import versatile_represent, versatile_convert_to_str
from config import AppConfig


LAZY = AppConfig.ORM_MODEL_RELATIONSHIP_LAZY_PARAM


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Сущность пользователя системы"""
    __tablename__ = 'user'
    __table_args__ = AppConfig.DB_TABLE_ARGS

    serialize_only = (
        'id', 'login', 'email', 'role_id')

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    email = Column(Text, unique=True, nullable=False)
    login = Column(Text, unique=True, nullable=False)
    passwd_hash = Column(Text, nullable=False)

    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)

    # Связи many-to-one:
    role = orm.relationship('Role', back_populates='users', lazy=LAZY)

    # Связи one-to-many:
    passports = orm.relationship('Passport', back_populates='user', lazy=LAZY)

    def set_password(self, new_password: str) -> None:
        self.passwd_hash = generate_password_hash(new_password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.passwd_hash, password)

    __repr__ = versatile_represent

    __str__ = versatile_convert_to_str
