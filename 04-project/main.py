from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "API is working"}

@app.get("/clients")
def get_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()

@app.post("/clients")
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
