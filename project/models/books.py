from project import db


class BooksModel(db.Model):
    __table_name__ = 'Books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    amazon_url = db.Column(db.String(1250))
    author = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    user_id = db.Column(db.Integer)

    def __init__(self, title, amazon_url, author, genre, user_id):
        self.title = title
        self.amazon_url = amazon_url
        self.author = author
        self.genre = genre
        self.user_id = user_id

    @classmethod
    def find_by_name(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_book_id(cls, book_id):
        return cls.query.filter_by(id=book_id).first()

    @classmethod
    def delete_by_book_user_id(cls, book_id, user_id):
        return cls.query.filter_by(id=book_id, user_id=user_id).delete()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
