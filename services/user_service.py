from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt

from schemas.user_schema import UserCreate, UserResponse
from models.user_model import User

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

async def get_users(db: Session) -> list[UserResponse] | None:
    userTable = db.query(User).all()

    if len(userTable) == 0:
        return None

    users = [UserResponse.model_validate(user) for user in userTable] # db모델->스키마 & 배열
    return users

async def create_user(user_in: UserCreate, db: Session) -> UserCreate | None:
    email = user_in.email.lower()

    exist = (
        db.query(User)
            .filter(or_(User.userid == user_in.userid, User.email == email))
            .first()
    )

    if exist:
        return None

    user = User(
        userid = user_in.userid,
        password = hash_password(user_in.password),
        email = email,
        name = user_in.name
    )
    db.add(user)

    try:
        db.commit()
    except IntegrityError: # 동시에 같은 값으로 가입한 경우
        db.rollback()
        return None

    db.refresh(user)
    return user

async def get_user(email: str, db: Session):
    exist = (
        db.query(User)
            .filter(User.email == email)
            .first()
    )

    if exist is None:
        return None

    userTable = UserResponse.model_validate(exist)
    return userTable
