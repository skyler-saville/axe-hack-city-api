# routers/authentication_router.py
from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# Create an APIRouter instance
router = APIRouter()

# Fake user database
fake_users_db: Dict[str, Dict[str, Optional[str]]] = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    """User model for API responses."""

    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    """User model with hashed password for database."""

    hashed_password: str


def fake_hash_password(password: str) -> str:
    """Fake password hashing function."""
    return "fakehashed" + password


def get_user(
    db: Dict[str, Dict[str, Optional[str]]], username: str
) -> Optional[UserInDB]:
    """Retrieve a user from the database."""
    user_dict = db.get(username)
    if user_dict:
        return UserInDB(**user_dict)
    return None


def fake_decode_token(token: str) -> Optional[UserInDB]:
    """Fake token decoder."""
    return get_user(fake_users_db, token)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """Get the current user based on the provided token."""
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get the current active user."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    """Login endpoint to obtain access tokens."""
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if hashed_password != user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)) -> User:
    """Retrieve the current user's information."""
    return current_user
