import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# ==============================
# 1. DATABASE CONFIG
# ==============================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ==============================
# 2. FASTAPI APP
# ==============================

# app = FastAPI()

app = FastAPI(
    root_path="/api",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# ==============================
# 3. CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# 4. ROOT ROUTE (VERY IMPORTANT)
# ==============================

@app.get("/")
def root():
    return {"status": "Backend is running"}

# ==============================
# 5. HEALTH CHECK FOR ALB
# ==============================

@app.get("/api/")
def health_check():
    return {"status": "Backend healthy", "database": "Connected to RDS"}

# ==============================
# 6. MODEL
# ==============================

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20), unique=True)
    password = Column(String(255))

Base.metadata.create_all(bind=engine)

# ==============================
# 7. SIGNUP
# ==============================

@app.post("/api/signup")
def signup(user: dict):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.phone == user["phone"]).first()
        if existing:
            return {"message": "User already exists"}

        new_user = User(**user)
        db.add(new_user)
        db.commit()
        return {"message": "User registered successfully"}
    finally:
        db.close()

# ==============================
# 8. LOGIN
# ==============================

@app.post("/api/login")
def login(data: dict):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.phone == data.get("phone")).first()

        if not user:
            return {"message": "User not found"}

        if user.password == data.get("password"):
            return {"message": "Login successful"}

        return {"message": "Invalid password"}
    finally:
        db.close()
