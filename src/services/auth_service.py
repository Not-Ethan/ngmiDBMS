import bcrypt
from src.database import db

current_user = None

def register_user(email: str, full_name: str, password: str) -> int:
    existing = db.execute_one("SELECT user_id FROM Users WHERE email = %s", (email,))
    if existing:
        raise ValueError("User already exists")
    
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    result = db.execute_one(
        "INSERT INTO Users (email, full_name, password_hash) VALUES (%s, %s, %s) RETURNING user_id",
        (email, full_name, password_hash)
    )
    return result['user_id']

def login_user(email: str, password: str) -> dict:
    global current_user
    
    user = db.execute_one("SELECT * FROM Users WHERE email = %s", (email,))
    if not user:
        raise ValueError("User not found")
    
    if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        raise ValueError("Invalid password")
    
    current_user = user
    return user

def get_current_user():
    return current_user

def logout_user():
    global current_user
    current_user = None