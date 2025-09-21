from pydantic import BaseModel, EmailStr
from datetime import datetime



# --- User Schemas ---

# This is the schema for data you expect when CREATING a user.
# The user provides an email and a password.
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# This is the schema for data you send back when READING a user.
# Notice: NO password here. Never send the password hash back.
class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

# --- Workout Schemas ---

class WorkoutCreate(BaseModel):
    name: str

class WorkoutRead(BaseModel):
    id: int
    name: str
    timestamp: datetime
    user_id: int

    class Config:
        from_attributes = True

'''Notes:
We are using Pydantic's BaseModel to define schemas for user and workout data. This is not for the database itself, but for data validation and serialization in our API.
- UserCreate schema is used when a new user is being created. It includes email and password fields.
- UserRead schema is used when user data is being sent back to the client. It includes
  id and email fields, but excludes the password for security reasons.
  - WorkoutCreate schema is used when a new workout is being created. It includes the name of the workout.
  - WorkoutRead schema is used when workout data is being sent back to the client. 
  The config class with from_attributes = True allows Pydantic to read data directly from SQLAlchemy model instances. Pydantic normally expects dictionaries,
  but this setting makes it compatible with ORM models.
  - eventhough we are not using pydantic models to create the database tables, they aer used to read data from database.
  
  Flow:
  1. Client sends a request to create a user with UserCreate schema.
  2. fastAPI then receives JSOn and validates the pydantic model
  3. pydantic model is converted to SQLAlchemy model and saved to database
  4. when reading user data, SQLAlchemy model is converted to pydantic model and sent back to client.
  '''

class LoginRequest(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str