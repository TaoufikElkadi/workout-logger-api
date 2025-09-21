from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
import models, schemas, hashing
import os
from database import get_db, engine

from jose import JWTError, jwt
from datetime import datetime, timedelta

# CONSTANTS FOR JWT

SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# tells FastAPI what URL to check for the token.
# doesn't create the endpoint, just tells the dependency where to look. it says to look for the token in the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    # define the exception to raise if credentials are invalid
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # decode the jwt to get the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # extract the user id from the payload
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        # get the user from the database
    user = db.query(models.user).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# WE give the route and the pydantic model to validate the function input and output. We use Depends to get a database session
@app.post('/users/', response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # hash the password before storing it
    hashed_pass = hashing.hash_password(user.password)
    # create the new user instance
    new_user = models.User(email=user.email, hashed_password=hashed_pass)
        # add and commit the new user to the database
    db.add(new_user)
    # save the changes
    db.commit()
    # gets new ID from database and updates the new_user instance
    db.refresh(new_user)

    return new_user

@app.post('/login', response_model = schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # get user from database
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not hashing.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # set the token to expire in 30 minutes
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # define the payload of the token with user id and expiry time
    to_encode = {"sub":str(user.id), "exp": expire}

    # create the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # return the token
    return {"access_token": encoded_jwt, "token_type": "bearer"}
   
# the dependency get_current_user will be executed first and use teh request's bearer token to get the current user
@app.get("users/me", response_model=schemas.UserRead)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user