from fastapi.responses import JSONResponse
from fastapi import APIRouter

from schemas.user import User

from utils.jwt_manager import create_token


user_router = APIRouter()


@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'arnol@mail.com' and user.password == '1234':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

