from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
import hashlib

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)

    def set_password(self, password):
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.hashed_password == hashlib.sha256(password.encode()).hexdigest()