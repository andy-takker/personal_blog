from typing import NoReturn, Union

from flask_login import UserMixin
from sqlalchemy import Column, String, Integer
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager
from app.mixins import BaseMixin, TimestampMixin


class User(BaseMixin, UserMixin, TimestampMixin, db.Model):
    """Авторизованный пользователь админ панели"""
    __tablename__ = "user"

    name = Column(String, nullable=False, index=True)
    login = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def set_password(self, password: str) -> NoReturn:
        self.password_hash = generate_password_hash(password)


@login_manager.user_loader
def load_user(user_id: Union[int, str]):
    return User.query.get(user_id)


# class Post(BaseMixin, TimestampMixin, db.Model):
#     __tablename__ = 'post'
#
#     title = Column(String, nullable=False)
#     text = Column(String, nullable=False)
#     author_id = Column(Integer)

