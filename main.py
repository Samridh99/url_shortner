from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import string
import random

# Database setup
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/dbname"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# URL model
class URL(Base):
  __tablename__ = "urls"

  id = Column(Integer, primary_key=True, index=True)
  original_url = Column(String, index=True)
  short_code = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic model for request validation
class URLBase(BaseModel):
  url: str

# Dependency to get the database session
def get_db():
  db = SessionLocal()
  try:
      yield db
  finally:
      db.close()

# Generate a random short code
def generate_short_code():
  characters = string.ascii_letters + string.digits
  return ''.join(random.choice(characters) for _ in range(6))

# POST /shorten endpoint
@app.post("/shorten")
def shorten_url(url_base: URLBase, db: Session = Depends(get_db)):
  short_code = generate_short_code()
  db_url = URL(original_url=url_base.url, short_code=short_code)
  db.add(db_url)
  db.commit()
  db.refresh(db_url)
  return {"short_url": f"http://localhost:8000/{short_code}"}

# GET /{short_code} endpoint
@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
  db_url = db.query(URL).filter(URL.short_code == short_code).first()
  if db_url is None:
      raise HTTPException(status_code=404, detail="URL not found")
  return {"url": db_url.original_url}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)