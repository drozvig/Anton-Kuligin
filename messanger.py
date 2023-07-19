from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session




app = FastAPI(
    title="SlavaRossii"
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Message_ALL(BaseModel):
    text_message : str
    author: str

messanger = []


@app.post(("/"))
def messege(message : Message_ALL, db: Session = Depends(get_db)):
    message_model = models.Message()
    message_model.text_message = message.text_message
    message_model.author = message.author

    db.add(message_model)
    db.commit()


@app.get(("/"))
def messege_all(db: Session = Depends(get_db)):
    return db.query(models.Message).all()
