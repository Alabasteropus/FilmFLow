# src/services/auth_service.py
from src import db
from src.models.user import User
import bcrypt

def register_user(username, password):
    if User.query.filter_by(username=username).first():
        raise ValueError("Username already exists.")
    
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return True
    return False

def get_user(username):
    return User.query.filter_by(username=username).first()
