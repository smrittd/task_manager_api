from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import Token, UserCreate, UserResponse
from app.crud.user import get_user_by_email, create_user
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, verify_password
router = APIRouter(tags=["Users"], prefix="/users")



@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):


    db_user = await get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    
    return await create_user(db=db, user=user)



@router.post('/login', response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email=form_data.username)


    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate":'bearer'}
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
