import sqlite3
from flask import g, current_app
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()

class User(UserMixin):
    def __init__(self, id, username, customer_id, hashed_password):
        self.id = id
        self.username = username
        self.customer_id = customer_id
        self.hashed_password = hashed_password

    @staticmethod
    def get_db():
        if 'db' not in g:
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        return g.db

    @staticmethod
    def validate(username, password):
        db = User.get_db()
        user = db.execute(
            'SELECT id, username, customer_id, hashed_password FROM Users WHERE username = ?',
            [username.lower()]
        ).fetchone()

        if user is None:
            return None

        if bcrypt.check_password_hash(user['hashed_password'], password):
            return User(user['id'], user['username'], user['customer_id'], user['hashed_password'])
        
        return None

    @staticmethod
    def get(user_id):
        db = User.get_db()
        user = db.execute(
            'SELECT id, username, customer_id, hashed_password FROM Users WHERE id = ?',
            [user_id]
        ).fetchone()
        
        if user:
            return User(user['id'], user['username'], user['customer_id'], user['hashed_password'])
        return None