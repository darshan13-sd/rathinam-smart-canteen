from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.models import User, Canteen, get_db
from backend.app.schemas import UserLogin, UserCreate, TokenResponse, UserResponse
from backend.app.auth import hash_password, verify_password, create_access_token, get_current_user, require_auth

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    token = create_access_token(user.id, user.role, user.username)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/register", response_model=TokenResponse)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        (User.username == payload.username) | (User.email == payload.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role or "STUDENT",
        phone=payload.phone,
        department=payload.department,
        roll_number=payload.roll_number,
        canteen_id=payload.canteen_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.id, user.role, user.username)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(require_auth)):
    return current_user

@router.get("/demo-users")
def get_demo_users(db: Session = Depends(get_db)):
    """Returns quick switcher login credentials for easy demo & evaluation"""
    users = db.query(User).all()
    res = []
    for u in users:
        canteen_name = None
        if u.canteen_id:
            c = db.query(Canteen).filter(Canteen.id == u.canteen_id).first()
            if c:
                canteen_name = c.name
        res.append({
            "id": u.id,
            "username": u.username,
            "password": "password123" if u.username != "admin" else "admin123",
            "full_name": u.full_name,
            "role": u.role,
            "department": u.department,
            "canteen_name": canteen_name,
            "canteen_id": u.canteen_id
        })
    return res
