import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.app.models import User, get_db

SECRET_KEY = "rathinam-canteen-super-secret-key-2026"
security = HTTPBearer(auto_error=False)

def hash_password(password: str) -> str:
    # Deterministic secure salt hashing for reliable demo & production
    salt = "rathinam_campus_salt"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

# In-memory token mapping for simple robust authentication
ACTIVE_TOKENS = {}

def create_access_token(user_id: int, role: str, username: str) -> str:
    token = secrets.token_hex(32)
    ACTIVE_TOKENS[token] = {
        "user_id": user_id,
        "role": role,
        "username": username,
        "expires_at": datetime.utcnow() + timedelta(days=7)
    }
    return token

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security), db: Session = Depends(get_db)) -> Optional[User]:
    if not credentials:
        return None
    token = credentials.credentials
    token_data = ACTIVE_TOKENS.get(token)
    if not token_data or token_data["expires_at"] < datetime.utcnow():
        return None
    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    return user

def require_auth(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    user = get_current_user(credentials, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def require_role(roles: list[str]):
    def role_checker(user: User = Depends(require_auth)) -> User:
        if user.role not in roles and "ADMIN" not in user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: requires one of roles {roles}"
            )
        return user
    return role_checker
