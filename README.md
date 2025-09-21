# Workout Logger API

A FastAPI backend for user registration, authentication, and workout logging.

## Features

- **User Registration:** Create new accounts with email and password.
- **User Login:** Authenticate and receive a JWT token.
- **JWT Authentication:** Secure endpoints using JWT tokens.
- **User Profile:** Retrieve current user info.
- **PostgreSQL Database:** Stores users and workouts (extendable).

## Tech Stack

- FastAPI
- SQLAlchemy
- Alembic (for migrations)
- PostgreSQL
- JWT (via python-jose)

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/workout-logger-api.git
   cd workout-logger-api
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Create a `.env` file:
     ```
     DATABASE_URL=postgresql://user:password@localhost/dbname
     SECRET_KEY=your_secret_key
     ```
   - Add `.env` to `.gitignore`.

5. **Run database migrations (if using Alembic):**
   ```sh
   alembic upgrade head
   ```

6. **Start the API server:**
   ```sh
   uvicorn main:app --reload
   ```

## API Endpoints

- `POST /users/` — Register a new user
- `POST /login` — Login and get JWT token
- `GET /users/me` — Get current user info (requires JWT)


## License

MIT
