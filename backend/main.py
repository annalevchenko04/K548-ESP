import os
import crud
import models
import schemas
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, List
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost:3000",
    "https://quickchart.io"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SENDGRIDAPIKEY = os.environ.get("SENDGRID_API_KEY")
REFRESH_TOKEN_EXPIRE_DAYS = 10


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/user/{username}", response_model=schemas.UserResponse, tags=["Users"])
async def get_user_by_username(username: str, db: db_dependency):
    db_user = crud.get_user(db=db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/user/id/{userid}/", response_model=schemas.UserResponse, tags=["Users"])
async def get_user_by_id(userid: int, db: db_dependency):
    db_user = crud.get_user_by_id(db=db, userid=userid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def register_user(user: schemas.UserCreate, db: db_dependency):
    db_user = crud.get_user(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db=db, user=user)


def authenticate_user(username: str, password: str, db: db_dependency):
    user = crud.get_user(db=db, username=username)

    db_user = db.query(models.User).filter(models.User.username == username).first()

    # If user is not found, return None
    if not db_user:
        return False
    if not user or not pwd_context.verify(password, db_user.hashed_password):
        return False
    return user


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/token", tags=["Users"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})
    token_data = {"id": user.id, "username": user.username, "role": user.role}
    access_token = create_token(data=token_data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is invalid")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Token is invalid")


@app.get("/verify-token/{token}", tags=["Users"])
async def verify_user_token(token: str, db: Session = Depends(get_db)):
    payload = verify_token(token=token)
    username = payload.get("username")
    user = crud.get_user(db, username=username)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Token is valid", "access_token": token}


@app.post("/refresh-token", tags=["Users"])
async def refresh_access_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        username: str = payload.get("username")
        role: str = payload.get("role")
        if user_id is None or username is None or role is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid refresh token")
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        access_token = create_token(
            {"id": user.id, "username": user.username, "role": user.role},
            timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

        return {"access_token": access_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid refresh token")


@app.get("/users", response_model=List[schemas.UserResponse], tags=["Users"])
async def list_users(db: db_dependency):
    users = crud.get_users(db=db)
    return users


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        username: str = payload.get("username")
        role: str = payload.get("role")
        if user_id is None or username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


@app.get("/user/profile", response_model=schemas.UserResponse, tags=["Users"])
async def get_user_profile(current_user: models.User = Depends(get_current_user)):
    return current_user


# Update a user
@app.put("/user/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
async def update_user(user_id: int, user: schemas.UserCreate, db: db_dependency):
    db_user = crud.update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Delete a user
@app.delete("/user/{user_id}", response_model=dict, tags=["Users"])
async def delete_user(user_id: int, db: db_dependency):
    result = crud.delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


