from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
)

from sqlalchemy.orm import declarative_base, relationship

# This Base class will be used by our models to inherit from. Factory function that creates a special base class for db models. purpose is to act as central regisgry for all table definitions
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    workouts = relationship("Workout", back_populates="owner")

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="workouts")

'''Notes:
These are the models in our database, defined using SQLAlchemy's ORM system.
- We have two models: User and Workout.
- The User model has fields for id, email, and hashed_password. The email field is unique and indexed for fast lookups.
- The Workout model has fields for id, name, timestamp, and user_id. The timestamp field defaults to the current time when a workout is created.
- There is a one-to-many relationship between User and Workout, meaning one user can have many workouts.
- The relationship is established using SQLAlchemy's relationship function, allowing easy access to a user's workouts and the owner of a workout.
'''
