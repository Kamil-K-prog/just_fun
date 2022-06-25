from email.policy import default
import sqlalchemy as sa
from sqlalchemy import orm
from data.db.db_sessionmaker import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    serialize_only = (
        'id', 'login', 'email')

    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.Text, unique=True, nullable=False)
    email = sa.Column(sa.Text, unique=True, nullable=False)
    role_id = sa.Column(sa.Integer, nullable=False, default=1)
    passwd_hash = sa.Column(sa.Text, unique=False, nullable=False)

    def set_password(self, new_password: str):
        self.passwd_hash = generate_password_hash(new_password)

    def check_password(self, password):
        return check_password_hash(self.passwd_hash, password)
