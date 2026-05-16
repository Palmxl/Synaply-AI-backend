from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.user import (
    UserCreate,
    UserLogin,
)

from app.services.auth_service import (
    register_user,
    login_user,
)

router = APIRouter()


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(user, db)


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    return login_user(user, db)