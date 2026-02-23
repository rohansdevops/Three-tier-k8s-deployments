import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20), unique=True)
    password = Column(String(255))

Base.metadata.create_all(bind=engine)

@app.post("/signup")
def signup(user: dict):
    db = SessionLocal()
    existing = db.query(User).filter(User.phone == user["phone"]).first()
    if existing:
        return {"message": "User already exists"}

    new_user = User(**user)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/login")
def login(data: dict):
    db = SessionLocal()
    try:
        phone =  data.get("phone")
        password = data.get("password")
        user = db.query(User).filter(User.phone ==phone).first()

        if not user:
            return {"message": "User not found. Please sign up."}

        if user.password == password:
            return {"message": "Hello, you have successfully logged in."}

        return {"message": "Invalid password"}
    except Exception as e:
        print(f"Error occured: {e}")
        return {"message": "Internal Database Error"}, 500
    finally:
        db.close()