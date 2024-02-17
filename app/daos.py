from app.models import User, Book
from app.extensions import db

class UserDAO:

    def __init__(self, model):
        self.model = model

    def getUsers(self):
        users = db.session.query(self.model).all()
        return users

    def getUser(self, email):
        user = db.session.query(self.model).filter_by(email = email).one_or_none()
        return user
    
    def createUser(self, name, email, password, is_teacher):
        user = User(name=name, email=email, password=password, is_teacher = is_teacher)
        db.session.add(user)
        db.session.commit()
        return user
    
    def deleteUser(self, email):
        user = self.getUser(email)
        if user is None:
            return None
        db.session.delete(user)
        db.session.commit()
    
    def deleteUsers(self):
        User.query.delete()
        db.session.commit()
    
    def updateUser(self):
        db.session.commit()
    
    def updateBalance(self, userEmail, days, time):
        time = float(time)
        user = self.getUser(userEmail)
        if user.is_teacher is True and days > 7:
            if time == days:
                user.balance = user.balance + (time - 7) 
            else:
                user.balance = user.balance + time
        elif user.is_teacher is False and days > 5:
            if time == days:
                user.balance = user.balance + ((time - 7) * 2.5)
            else:
                user.balance = user.balance + (time * 2.5)
        db.session.commit()
    
    def payBalance(self, userEmail, payment):
        user = self.getUser(userEmail)
        if user.balance == 0.0:
            return "No balance due to pay"
        elif user.balance < payment:
            return f"Payment exceeds balance, your balance is {user.balance}"
        user.balance = user.balance - payment
        db.session.commit()
        return f"Payment completed, your new balance is {user.balance}"
    
    def deleteUsers(self):
        User.query.delete()
        db.session.commit()


class BookDAO:

    def __init__(self, model):
        self.model = model

    def getBooks(self):
        books = db.session.query(self.model).all()
        return books

    def rentBook(self, bookId, userEmail):
        book = self.getBook(bookId)
        if book is None:
            raise TypeError
        if book.userEmail is not None:
            raise ValueError
        book.userEmail = userEmail
        db.session.commit()
        return book

    def getBook(self, bookId):
        book = db.session.query(self.model).filter_by(bookId = bookId).one_or_none()
        return book
    
    def createBook(self, name, category, author):
        book = Book(name=name, category=category, author=author)
        db.session.add(book)
        db.session.commit()
        return book
    
    def deleteBook(self, bookId):
        book = self.getBook(bookId)
        if book is None:
            raise TypeError
        db.session.delete(book)
        db.session.commit()
    
    def deleteUsers(self):
        User.query.delete()
        db.session.commit()
    
    def passTime(self, time):
        db.session.query(self.model).filter(self.model.userEmail != None).update({self.model.rentCounter: self.model.rentCounter + time})
        db.session.commit()
    
    def updateBook(self):
        db.session.commit()
    
    def getRentedBooks(self):
        return db.session.query(self.model).filter(self.model.userEmail != None).all()

user_dao = UserDAO(User)
book_dao = BookDAO(Book)