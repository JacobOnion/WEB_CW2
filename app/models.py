from app import db
from werkzeug.security import generate_password_hash, check_password_hash

AttemptsTable = db.Table("attempts",
                        db.Column("puzzleId", db.Integer, db.ForeignKey('puzzle_table.puzzleId'), primary_key=True),
                        db.Column("userId", db.Integer, db.ForeignKey('user_table.userId'), primary_key=True),
                        db.Column("score", db.Integer)
                        )

class Puzzle(db.Model):
    __tablename__ = "puzzle_table"
    puzzleId = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    puzzleLetters = db.Column(db.String)
    #puzzleAnswers = db.Column(db.String)
    users = db.relationship('User', secondary = AttemptsTable, back_populates = "puzzles")

class User(db.Model):
    __tablename__ = "user_table"
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String)
    password_hash = db.Column(db.String)
    puzzles = db.relationship('Puzzle', secondary = AttemptsTable, back_populates = "users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Word(db.Model):
    __tablename__ = "word_table"
    wordId = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    word = db.Column(db.String)
