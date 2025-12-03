import bcrypt
from src.database import db

current_user = None


import bcrypt
from src.database import db, DatabaseConnectionError

current_user = None

def login_user(email: str, password: str) -> dict:
    global current_user
    
    try:
        user = db.execute_one("SELECT * FROM Users WHERE email = %s", (email,))
        if not user:
            raise ValueError("Invalid email or password")
        
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            raise ValueError("Invalid email or password")
        
        current_user = user
        return user
        
    except DatabaseConnectionError:
        raise  # Re-raise database connection errors
    except Exception as e:
        if "invalid" in str(e).lower():
            raise ValueError("Invalid email or password")
        raise ValueError(f"Login failed: {str(e)}")

def get_current_user():
    global current_user
    if current_user:
        # Validate user still exists in database
        try:
            user = db.execute_one("SELECT * FROM Users WHERE user_id = %s", (current_user['user_id'],))
            if not user:
                current_user = None
        except DatabaseConnectionError:
            pass  # Keep current session during connection issues
    return current_user


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

def logout_user():
    global current_user
    current_user = None