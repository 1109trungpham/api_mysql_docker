from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
from pydantic import BaseModel

DATABASE_URL =  "mysql+pymysql://root:rootpass@mysql/db_name"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    score = Column(Integer, nullable=False)

class UserCreate(BaseModel):
    name: str
    score: int

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI is connected to MySQL"}

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, score=user.score)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User {user.name} with score {user.score} created"}


# Mở terminal chạy lệnh sau để thêm dữ liệu
# curl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d '{"name": "Linh", "score": 0}'

