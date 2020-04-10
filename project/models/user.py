from project import db
from flask import jsonify

class UserModel(db.Model):
    __table_name__ = 'Users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(50))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def user_exist(self):
        temp = UserModel.query.filter_by(username=self.username).first()
        if temp is not None:
            return True
        else:
            return False

    def verify_user(self,password):
        if self.password == password:
            return True
        else:
            return False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

