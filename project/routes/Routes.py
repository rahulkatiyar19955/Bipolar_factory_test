from flask import request, jsonify
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, fresh_jwt_required
from flask_jwt_extended import get_jwt_identity, create_access_token, create_refresh_token
from project import app, db, jwt_obj
from project.models.user import UserModel
from project.models.books import BooksModel


@app.route('/')
def index():
    return "hello"


@app.before_first_request
def init_database():
    db.create_all()


@app.route('/login', methods=['POST'])
def login():
    data_received = request.get_json()
    user = UserModel.find_by_username(data_received['username'])
    if user is not None:
        if user.verify_user(data_received['password']):
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            return jsonify({'message': 'Login Successful',
                            'access_token': access_token,
                            'refresh_token': refresh_token})
    return "Login Unsuccessful"


@app.route('/reauthenticate', methods=['POST'])
@jwt_refresh_token_required
def reauthenticate():
    return ''


@app.route('/register', methods=['POST'])
def create_user():
    data_received = request.get_json()
    new_user = UserModel(data_received['username'], data_received['password'])
    new_user.save_to_db()
    return "creating " + " " + data_received['username'] + " " + data_received['password']


@app.route('/favourite_book', methods=['POST'])
@jwt_required
def adding_book():
    data_received = request.get_json()
    title = data_received['title']
    amazon_url = data_received['amazon_url']
    author = data_received['author']
    genre = data_received['genre']
    # add check if it is already exist or not
    try:
        new_book = BooksModel(title, amazon_url, author, genre)
        new_book.save_to_db()
    except:
        return "error occured"

    return "added: " + title


@app.route('/favourite_book', methods=['GET'])
@jwt_required
def list_book():
    # data_received = request.get_json()
    books = BooksModel.query.all()
    list_of_books = []
    for book in books:
        temp_book = {}
        temp_book['title'] = book.title
        temp_book['amazon_url'] = book.amazon_url
        temp_book['author'] = book.author
        temp_book['genre'] = book.genre
        list_of_books.append(temp_book)
    return jsonify({'list_of_books': list_of_books})


@app.route('/favourite_book', methods=['PUT'])
@fresh_jwt_required
def update_book():
    return "update_book"


@app.route('/favourite_book', methods=['DELETE'])
@fresh_jwt_required
def delete_book():
    return "delete_book"
