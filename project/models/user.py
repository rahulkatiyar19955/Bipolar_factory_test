# import database object
from project import db


# class for user model
# this class inherit db model
class UserModel(db.Model):
    __table_name__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # this is a class method, so no class object is needed to call this function
    # this is used to find the user record with the given username
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # this function is used to tell whether a user with the given username exist in the database or not
    def user_exist(self):
        temp = UserModel.query.filter_by(username=self.username).first()
        if temp is not None:
            return True
        else:
            return False

    # this function will verify the user with the password in the database with the password given.
    def verify_user(self, password):
        if self.password == password:
            return True
        else:
            return False

    # this is used to add the object and commit the change in the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # this is used to delete the object and commit the change in the database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()