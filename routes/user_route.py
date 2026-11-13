from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
import time

from schemas.user_schema import UserResponse, UserCreate
from services import user_service
from connection import get_db

user_router = APIRouter(tags=['User'])

@user_router.get('')
async def get_users(db: Session = Depends(get_db)) -> list[UserResponse] | None:
    users = await user_service.get_users(db)

    return users

@user_router.post('/signup',
                  response_model=UserResponse,
                  status_code=status.HTTP_201_CREATED)
async def sign_up(user_in: UserCreate, db: Session = Depends(get_db)) -> UserCreate | None:
    user = await user_service.create_user(user_in, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='이미 사용 중인 아이디 또는 이메일입니다.'
        )

    return user

@user_router.get('/{email}')
async def get_user(email: str, db: Session = Depends(get_db)) -> UserResponse | None:
    user = await user_service.get_user(email, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='존재하지 않는 이메일입니다.'
        )

    return user
