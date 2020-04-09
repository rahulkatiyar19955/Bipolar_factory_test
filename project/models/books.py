from project import db


class BooksModel(db.Model):
    __table_name__ = 'Books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    amazon_url = db.Column(db.String(1250))
    author = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    user_id = db.Column(db.Integer)

    def __init__(self,title,amazon_url,author,genre):
        self.title= title
        self.amazon_url = amazon_url
        self.author = author
        self.genre = genre

    @classmethod
    def find_by_name(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
