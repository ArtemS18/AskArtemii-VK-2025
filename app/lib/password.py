from bcrypt import hashpw, gensalt, checkpw

def hash_password(password: str) -> str:
    hashed = hashpw(password.encode('utf-8'), gensalt())
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return checkpw(password.encode('utf-8'), hashed.encode('utf-8'))