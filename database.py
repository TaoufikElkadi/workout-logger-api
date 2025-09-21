from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
# The database URL tells SQLAlchemy where our database is.

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# The engine is the main entry point to the database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# A SessionLocal class is a "factory" for creating new database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base will be used by our models to inherit from.
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db # This provides the database session to the endpoint.
    finally:
        db.close() # This closes the session after the endpoint is don


'''Notes:
- SQLAlchemy uses the database URL to connect to the database.
- The engine is the starting point for any SQLAlchemy application. Which manages the connection pool to the database.
- SessionLocal is a factory for new Session objects, which are used to interact with the database
- Base is a base class for our ORM models, so Alemvic can generate migrations based on them.
- The get_db function is a dependency that provides a database session to FastAPI endpoints, ensuring that the session is properly opened and closed.
- '''