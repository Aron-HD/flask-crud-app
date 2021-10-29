from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@dataclass
class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, autoincrement=True)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    age = db.Column(db.Integer())
    role = db.Column(db.String(80))

    # def __init__(self, user_id, name, surname, age, role):
    #     self.user_id = user_id
    #     self.name = name
    #     self.surname = surname
    #     self.age = age
    #     self.role = role

    def __repr__(self):
        return f"{self.name} {self.surname}"
