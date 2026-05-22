# create a personal notebook tracker API
from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app import models, schemas
# add a vocabulary, and category feature.

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/posts", response_model= schemas.note_response)
def Create_note(data: schemas.Note_create, response: Response, db: Session = Depends(get_db)):
    user = models.Personal_Note(
        Title = data.Title,
        Topic = data.Topic,
        Category = data.Category,
        Vocabulary = data.Vocabulary,
        Note = data.Note,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    response.headers["X-Message"] = "Note successfully created!"
    
    return user

@app.get("/posts/{post_id}", response_model = schemas.note_response)
def get_note(post_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Personal_Note).filter(models.Personal_Note.Id == post_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Post not found!")
    return user
    
# look for its category
@app.get("/post/{post_category}", response_model = list[schemas.note_response])
def get_category(post_category:str, db: Session = Depends(get_db)):
    user = db.query(models.Personal_Note).filter(models.Personal_Note.Category == post_category).all()
    if not user:
        raise HTTPException(status_code=404, detail = "Category not found.")
    return user

