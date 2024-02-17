from app.daos import user_dao, book_dao
from app.extensions  import db, bcrypt
from app.models import BlockListToken

class UserService:
    def getUsers(self):
        queryUsers = user_dao.getUsers()
        users = []
        for qUser in queryUsers:
            users.append({
                'name': qUser.name,
                'email': qUser.email,
                'password': qUser.password,
                'is teacher?': qUser.is_teacher,
                'balance': qUser.balance,
                'books': [{'id': book.bookId, 'name': book.name, 'category': book.category, 'days rented': book.rentCounter, 'author': book.author} for book in qUser.books]
            })
        return users
    
    def getUser(self, email):
        user = user_dao.getUser(email)
        if user is None:
            raise TypeError
        return user
    
    def createUser(self, name, email, password, is_teacher):
        hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
        user = user_dao.createUser(name, email, hashedPassword, is_teacher)
        return {
            'name': user.name,
            'email': user.email,
            'books': user.books,
            'balance': user.balance,
            'is teacher?': user.is_teacher
        }
    
    def deleteUser(self, email):
        user_dao.deleteUser(email)
    
    def updateUser(self, email, name):
        user = user_dao.getUser(email)
        if user is None:
            raise TypeError
        user.name = name
        user_dao.updateUser()
        return {
            'name': user.name,
            'email': user.email,
            'balance': user.balance,
            'is teacher': user.is_teacher
        }
    
    def deleteUsers(self):
        user_dao.deleteUsers()

    

class BookService:
    def getBooks(self):
        queryBooks = book_dao.getBooks()
        books = []
        for qBook in queryBooks:
            books.append({
                'name': qBook.name,
                'category': qBook.category,
                'author': qBook.author,
                'days rented': qBook.rentCounter,
                'user': qBook.userEmail
            })
        return books
    
    def getBook(self, bookId):
        book = book_dao.getUser(bookId)
        if book is None:
            raise TypeError
        return {
            'bookId': book.bookId,
            'name': book.name,
            'category': book.category,
            'author': book.author,
            'days rented': book.rentCounter,
            'user': book.userEmail
        }
    
    def createBook(self, name, category, author):
        book = book_dao.createBook(name, category, author)
        return {
            'bookId': book.bookId,
            'name': book.name,
            'category': book.category,
            'author': book.author,
            'days rented': book.rentCounter,
            'user': book.userEmail
        }
    
    def deleteBook(self, bookId):
        book_dao.deleteBook(bookId)
    
    def updateBook(self, bookId, name, category, author):
        book = book_dao.getBook(bookId)
        if book is None:
            raise TypeError
        book.name = name
        book.category = category
        book.author = author
        book_dao.updateBook()
        return {
            'bookId': book.bookId,
            'name': book.name,
            'category': book.category,
            'days rented': book.rentCounter,
            'author': book.author
        }
    
    def deleteUsers(self):
        user_dao.deleteUsers()


    
class LibraryService:

    def rentBook(self, bookId, userEmail):
        book = book_dao.rentBook(bookId, userEmail)
        return {
            'name': book.name,
            'category': book.category,
            'author': book.author,
            'days rented': book.rentCounter,
            'userEmail': book.userEmail
        }
    
    def returnBook(self, bookId, userEmail):
        user = user_dao.getUser(userEmail)
        book = book_dao.getBook(bookId)
        if book is None:
            raise TypeError
        if book in user.books:
            book.rentCounter = 0
            user.books.remove(book)
            user_dao.updateUser()
        else:
            raise ValueError
            
    
    def passTime(self, time):
        book_dao.passTime(time)
        self.calculateBalance(time)
        
    
    def calculateBalance(self, time):
        rented_books = book_dao.getRentedBooks()
        for book in rented_books:
            user_dao.updateBalance(book.userEmail, book.rentCounter, time)

    def check_if_teacher(self, email):
        user = user_dao.getUser(email)
        return user.is_teacher
    
    def payBalance(self, userEmail, payment):
        return user_dao.payBalance(userEmail, payment)
    
    def getToken(self, jti):
        return BlockListToken.query.filter_by(token=jti).one_or_none()
    
    def addToken(self, jti):
        token = BlockListToken(token=jti)
        db.session.add(token)
        db.session.commit()
    
    def checkUserPassword(self, inputPassword, userPassword):
        return bcrypt.check_password_hash(inputPassword, userPassword)
    
    def deleteUsers(self):
        user_dao.deleteUsers()



user_service = UserService()
book_service = BookService()
library_service = LibraryService()