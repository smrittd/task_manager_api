from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from jwt.exceptions import InvalidTokenError


from app.database import get_db
from app.core.security import SECRET_KEY,ALGORITHM
from app.crud.user import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exceptions = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload =  jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get('sub')
        if email is None:
            raise credentials_exceptions
        
    except InvalidTokenError:
        raise credentials_exceptions
    

    user = await get_user_by_email(db, email = email)
    if user is None:
        raise credentials_exceptions
    
    return user