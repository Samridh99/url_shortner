# URL Shortener API

This is a basic URL shortener API built with FastAPI and PostgreSQL.

## Setup and Running

1. Install the required packages:
pip install fastapi uvicorn psycopg2-binary sqlalchemy


2. Set up a PostgreSQL database and update the `SQLALCHEMY_DATABASE_URL` in `main.py` with your database credentials.

3. Run the application:
python main.py


   The API will be available at `http://localhost:8000`.

## API Endpoints

- POST /shorten: Accept a long URL, return a shortened URL
  - Request body: `{"url": "https://example.com"}`
  - Response: `{"short_url": "http://localhost:8000/abc123"}`

- GET /{short_code}: Redirect to the original URL
  - Response: `{"url": "https://example.com"}`

## Project Structure

- `main.py`: Contains the FastAPI application, database models, and API endpoints.
- `README.md`: This file, containing project documentation.

## Notes

- This is a basic implementation and doesn't include error handling for invalid URLs or duplicate short codes.
- In a production environment, you would want to add more robust error handling, logging, and possibly rate limiting.