from flask import Blueprint, jsonify, request
from app.services import user_service, book_service, library_service
from app.extensions import jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
from werkzeug.exceptions import BadRequest, Forbidden
from sqlalchemy.exc import IntegrityError

routesBP = Blueprint('routes', __name__, url_prefix="/")


## /Users
@routesBP.route('/Users', methods=['GET'])
def getUsers():
    users = user_service.getUsers()
    return jsonify(users), 200

@routesBP.route('/Users', methods=['POST'])
def create_user():
    try:
        data = request.json
        users = data.get('users', [])
        usersCreated = []
        for user in users:
            name = user.get('name')
            email = user.get('email')
            password = user.get('password')
            is_teacher = user.get('is_teacher')
            if 'name' not in user or 'email' not in user or 'password' not in user or 'is_teacher' not in user:
                raise BadRequest
            userCreated = user_service.createUser(name, email, password, is_teacher)
            usersCreated.append(userCreated)
        return jsonify(users), 200
    except BadRequest:
        return jsonify({"message": "Invalid input"}), 400
    except IntegrityError:
        return jsonify({"message": "Email already exists"}), 409

@routesBP.route('/Users', methods=['DELETE'])
def reset_users():
    library_service.deleteUsers()
    return jsonify({'message': 'Table reset'}), 200

## /Books
@routesBP.route('/Books', methods=['GET'])
def getBooks():
    books = book_service.getBooks()
    return jsonify(books), 200

@routesBP.route('/Books', methods=['POST'])
@jwt_required()
def create_book():
    try:
        email = get_jwt_identity()
        if library_service.check_if_teacher(email) is False:
            raise Forbidden
        data = request.json
        books = data.get('books', [])
        booksCreated = []
        for book in books:
            name = book.get('name')
            category = book.get('category')
            author = book.get('author')
            if 'name' not in book or 'category' not in book or 'author' not in book:
                raise BadRequest
            bookCreated = book_service.createBook(name, category, author)
            booksCreated.append(bookCreated)
        return jsonify(booksCreated), 200
    except BadRequest:
        return jsonify({"message": "Invalid input"}), 400
    except Forbidden:
        return jsonify({"message": "You do not have permission for this action"}), 403


# /User
@routesBP.route('/User', methods=['DELETE'])
@jwt_required()
def delete_user():
    try:
        userEmail = get_jwt_identity()
        user_service.deleteUser(userEmail)
        return jsonify({'message': 'User deleted'}), 200
    except TypeError:
        return jsonify({"message": "user not found"}), 404

@routesBP.route('/User', methods=['PUT'])
@jwt_required()
def change_user():
    try:
        userEmail = get_jwt_identity()
        data = request.json
        name = data.get('name')
        if 'name' not in data:
            raise BadRequest
        user = user_service.updateUser(userEmail, name)
        return jsonify(user), 200
    except BadRequest:
        return jsonify({"message": "Invalid input"}), 400

@routesBP.route('/User', methods=['POST'])
@jwt_required()
def make_payment():
    try:
        userEmail = get_jwt_identity()
        data = request.json
        payment = data.get('payment')
        if 'payment' not in data:
            raise BadRequest
        message = library_service.payBalance(userEmail, payment)
        return jsonify({"message": message}), 200
    except BadRequest:
        return jsonify({"message": "Invalid input"}), 400

@routesBP.route('/User/Book/<int:bookId>', methods=['POST'])
@jwt_required()
def rentBook(bookId):
    try:
        userEmail = get_jwt_identity()
        book = library_service.rentBook(bookId, userEmail)
        return jsonify(book), 200
    except ValueError:
        return jsonify({"message": "Book already issued to another user"}), 401
    except TypeError:
        return jsonify({"message": "book was not found"}), 404

@routesBP.route('/User/Book/<int:bookId>', methods=['DELETE'])
@jwt_required()
def returnBook(bookId):
    try:
        userEmail = get_jwt_identity()
        library_service.returnBook(bookId, userEmail)
        return jsonify({"message": "Book returned"}), 200
    except ValueError:
        return jsonify({"message": "Book was already not issued to user"}), 401
    except TypeError:
        return jsonify({"message": "book was not found"}), 404

@routesBP.route('/User', methods=['GET'])
@jwt_required()
def passTime():
    try:
        email = get_jwt_identity()
        if library_service.check_if_teacher(email) is False:
            raise Forbidden
        time = request.args['time']
        library_service.passTime(time)
        return jsonify({"message": f"Time passed by {time}"}), 200
    except KeyError:
        return jsonify({"message": "No query parameter given"}), 400
    except Forbidden:
        return jsonify({"message": "You do not have permission to do this action"}), 403
        


## /Book
@routesBP.route('/Book/<int:bookId>', methods=['DELETE'])
@jwt_required()
def delete_book(bookId):
    try:
        email = get_jwt_identity()
        if library_service.check_if_teacher(email) is False:
            raise Forbidden
        book_service.deleteBook(bookId)
        return jsonify({'message': 'Book deleted'}), 200
    except TypeError:
        return jsonify({"message": "book was not found"}), 404
    except Forbidden:
        return jsonify({"message": "You do not havae permission for this action"}), 403

@routesBP.route('/Book/<int:bookId>', methods=['PUT'])
@jwt_required()
def change_book(bookId):
    try:
        email = get_jwt_identity()
        if library_service.check_if_teacher(email) is False:
            raise Forbidden
        data = request.json
        name = data.get('name')
        category = data.get('category')
        author = data.get('author')
        if 'name' not in data or 'category' not in data or 'author' not in data:
            raise BadRequest
        book = book_service.updateBook(bookId, name, category, author)
        return jsonify(book), 200
    except BadRequest:
        return jsonify({"message": "invalid input"}), 400
    except TypeError:
        return jsonify({"message": "book not found"}), 404
    except Forbidden:
        return jsonify({"message": "You do not have permission for this action "}), 403


## Login, logout, and check token
@routesBP.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password') 
        if 'email' not in data or 'password' not in data:
            raise BadRequest
        user = user_service.getUser(email)
        if library_service.checkUserPassword(user.password, password):
            access_token = create_access_token(identity=user.email, expires_delta=timedelta(minutes=10))
            return jsonify({'message': f"Hello {user.name}, you are logged in!", 'token': access_token}), 200
        else:
            return jsonify({"message": "Incorrect password"}), 400
    except BadRequest:
        return jsonify({"message": "invalid input"}), 400
    except TypeError:
        return jsonify({"message": "user not found"}), 404


@routesBP.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    library_service.addToken(jti)
    return jsonify({"message": "Logged out!"}), 200

@jwt.token_in_blocklist_loader
def check_token(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = library_service.getToken(jti)
    return token is not None

    