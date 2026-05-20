
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app import models, auth, schemas

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ----------------------------------------------------
# Database Session Dependency
# ----------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------------------------------
# REGISTER ENDPOINT
# ----------------------------------------------------
@app.post("/register", response_model=schemas.RegisterResponse)
def register_user(data: schemas.RegisterCreate, db: Session = Depends(get_db)):

    # Check if the user already exists
    existing_user = db.query(models.Authentication).filter(
        models.Authentication.Account == data.Account
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password
    hashed_pw = auth.hash_password(data.Password)

    # Create new user record
    user = models.Authentication(
        Account=data.Account,
        Password=hashed_pw
    )

    db.add(user)
    db.commit()            # <-- MUST be commit()
    db.refresh(user)       # <-- Refresh to return the inserted user

    return user

# -------------------------
# LOGIN
# -------------------------
@app.post("/login")
def login(account: str, password: str, db: Session = Depends(get_db)):

    # Find the user (Model uses capitalized Account)
    user = db.query(models.Authentication).filter(
        models.Authentication.Account == account
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify hashed password (Model uses capitalized Password)
    if not auth.verify_password(password, user.Password):
        raise HTTPException(status_code=400, detail="Wrong password")

    return {
        "message": f"Welcome {user.Account}, login successful!"
    }
