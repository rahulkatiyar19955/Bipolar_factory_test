from flask import request, jsonify
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, fresh_jwt_required
from flask_jwt_extended import get_jwt_identity, create_access_token, create_refresh_token
from project import app, db
from project.models.user import UserModel
from project.models.books import BooksModel


@app.route('/')
def index():
    return jsonify({'message': "The API is working : Root Endpoint"}), 200


@app.before_first_request
def init_database():
    db.create_all()


@app.route('/login', methods=['POST'])
def login():
    data_received = request.get_json()
    user = UserModel.find_by_username(data_received['username'])
    if user is not None:
        if user.verify_user(data_received['password']):
            user_json = dict()
            user_json['username'] = user.username
            user_json['id'] = user.id
            access_token = create_access_token(identity=user_json, fresh=True)
            refresh_token = create_refresh_token(identity=user_json)
            return jsonify({'message': 'Login Successful',
                            'access_token': access_token,
                            'refresh_token': refresh_token})
    return jsonify({'message': "Login Unsuccessful"}), 401


@app.route('/reauthenticate', methods=['POST'])
@jwt_refresh_token_required
def reauthenticate():
    curr_user = get_jwt_identity()
    access_token = create_access_token(identity=curr_user, fresh=False)
    return jsonify({'message': 'Successful Creating of access token',
                    'access_token': access_token}), 200


@app.route('/register', methods=['POST'])
def create_user():
    data_received = request.get_json()
    new_user = UserModel(data_received['username'], data_received['password'])
    if new_user.user_exist():
        return jsonify({'message': "Username already exist"}), 400
    new_user.save_to_db()
    return jsonify({'message': "Created Successfully",
                    "username":data_received['username']}), 200


@app.route('/favourite_book', methods=['POST'])
@jwt_required
def adding_book():
    data_received = request.get_json()
    title = data_received['title']
    amazon_url = data_received['amazon_url']
    author = data_received['author']
    genre = data_received['genre']
    curr_user = get_jwt_identity()
    new_book = BooksModel(title, amazon_url, author, genre, curr_user['id'])
    if BooksModel.find_by_name(title) is not None:
        return jsonify({'message': "Book with same title already exist"}), 400
    else:
        try:
            new_book.save_to_db()
        except:
            return jsonify({'message': "error occured"}), 400

    return jsonify({'message': "added successful",
                    "title":title}), 200


@app.route('/favourite_book', methods=['GET'])
@jwt_required
def list_book():
    curr_user = get_jwt_identity()
    books = BooksModel.find_by_user_id(curr_user['id'])
    list_of_books = []
    for book in books:
        temp_book = {}
        temp_book['book_id'] = book.id
        temp_book['title'] = book.title
        temp_book['amazon_url'] = book.amazon_url
        temp_book['author'] = book.author
        temp_book['genre'] = book.genre
        list_of_books.append(temp_book)
    return jsonify({'list_of_books': list_of_books}), 200


@app.route('/favourite_book', methods=['PUT'])
@fresh_jwt_required
def update_book():
    data_received = request.get_json()
    book_id = data_received['book_id']
    curr_user = get_jwt_identity()
    temp_book = BooksModel.find_by_book_id(book_id)
    if temp_book is not None and temp_book.user_id == curr_user['id']:
        temp_book.title = data_received['title']
        temp_book.amazon_url = data_received['amazon_url']
        temp_book.author = data_received['author']
        temp_book.genre = data_received['genre']
        temp_book.save_to_db()
        return jsonify({'message': "update book successful"}), 200
    else:
        return jsonify({'message': "Book with the Given Id is not found"}), 404


@app.route('/favourite_book', methods=['DELETE'])
@fresh_jwt_required
def delete_book():
    data_received = request.get_json()
    book_id = data_received['book_id']
    curr_user = get_jwt_identity()
    try:
        temp_book = BooksModel.find_by_book_id(book_id)
        if temp_book is not None and temp_book.user_id == curr_user['id']:
            BooksModel.delete_by_book_user_id(book_id, curr_user['id'])
            db.session.commit()
            return jsonify({'message': "deletion of book Successful"}), 200
        else:
            return jsonify({'message': "No book found with the given Book_Id"}), 404
    except:
        return jsonify({'message': "deletion of book Unsuccessful"}), 404
