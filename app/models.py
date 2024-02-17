from app.extensions import db

class User(db.Model):
    email = db.Column(db.String(255), primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_teacher = db.Column(db.Boolean)
    balance = db.Column(db.Float, default=0.0)
    books = db.relationship('Book', backref='user')

class Book(db.Model):
    bookId = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rentCounter = db.Column(db.Integer, default=0)
    userEmail = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=True)

class BlockListToken(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    token = db.Column(db.String(255), nullable=False)