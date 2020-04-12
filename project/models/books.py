# import database object
from project import db


# class model for book database
class BooksModel(db.Model):
    __table_name__ = 'Books'  # table name in the database
    id = db.Column(db.Integer, primary_key=True)  # id is a primary key
    title = db.Column(db.String(100))
    amazon_url = db.Column(db.String(1250))
    author = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    user_id = db.Column(db.Integer)

    # initialise the book object
    def __init__(self, title, amazon_url, author, genre, user_id):
        self.title = title
        self.amazon_url = amazon_url
        self.author = author
        self.genre = genre
        self.user_id = user_id

    # this is a class method, so no class object is needed to call this function
    # this is used to find the first record(book) which matches with the given title
    @classmethod
    def find_by_name(cls, title):
        return cls.query.filter_by(title=title).first()

    # this is a class method, so no class object is needed to call this function
    # this is used to find the first record(book) which matches with the given book id
    @classmethod
    def find_by_book_id(cls, book_id):
        return cls.query.filter_by(id=book_id).first()

    # this is a class method, so no class object is needed to call this function
    # this is used to delete the first record(book) which matches with the given book_id and user_id
    @classmethod
    def delete_by_book_user_id(cls, book_id, user_id):
        return cls.query.filter_by(id=book_id, user_id=user_id).delete()

    # this is a class method, so no class object is needed to call this function
    # this will give all the books of the user with the given user ID
    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    # this is used to add the object and commit the change in the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # this is used to delete the object and commit the change in the database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
