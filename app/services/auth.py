import bcrypt

def hash_password(password: str) -> str:
    # 1. Convert plain text password to bytes
    password_bytes = password.encode('utf-8')
    
    # 2. Generate a random salt
    salt = bcrypt.gensalt()
    
    # 3. Hash the password and convert the resulting bytes back into a string
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_password_bytes.decode('utf-8')