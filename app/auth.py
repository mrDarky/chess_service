from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
import hashlib

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _prepare_password(password: str) -> str:
    """
    Pre-hash password with SHA-256 to ensure it's always within bcrypt's 72-byte limit.
    This allows passwords of any length while maintaining security.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    Supports both legacy hashes (without SHA-256 pre-hashing) and new hashes (with SHA-256 pre-hashing).
    """
    # First try with SHA-256 pre-hashing (new method)
    prepared_password = _prepare_password(plain_password)
    if pwd_context.verify(prepared_password, hashed_password):
        return True
    
    # Fallback to direct verification for backward compatibility with existing hashes
    # This handles passwords that were hashed before the SHA-256 pre-hashing was added
    try:
        if pwd_context.verify(plain_password, hashed_password):
            return True
    except ValueError:
        # If the password is too long for bcrypt, the ValueError is expected
        # and we can safely ignore it since we already tried with pre-hashing above
        pass
    
    return False

def get_password_hash(password: str) -> str:
    """Hash a password"""
    prepared_password = _prepare_password(password)
    return pwd_context.hash(prepared_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(db, username: str, password: str):
    """Authenticate a user"""
    cursor = await db.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = await cursor.fetchone()
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user
