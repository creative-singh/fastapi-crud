from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ShoesBase(BaseModel):
  type: str
  name: str
  is_expensive: bool = False

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Get All Shoes
@app.get("/shoes/")
async def get_shoes(db: db_dependency):
  return db.query(models.Shoes).all()

# Create Shoes
@app.post("/shoes/")
async def create_shoes(shoes: ShoesBase, db: db_dependency):
  db_shoes = models.Shoes(
    type=shoes.type, 
    name=shoes.name, 
    is_expensive=shoes.is_expensive
  )
  db.add(db_shoes)
  db.commit()
  db.refresh(db_shoes)
  return db_shoes

# Get Shoes by ID
@app.get("/shoes/{id}")
async def get_shoes_by_id(id: int, db: db_dependency):
  db_shoes = db.query(models.Shoes).filter(models.Shoes.id == id).first()
  if not db_shoes: 
    raise HTTPException(status_code=404, detail="Shoes not found")
  return db_shoes

# Update Shoes by ID by Type
@app.put("/shoes/{id}")
async def update_shoes_by_id(id: int, type: str, db: db_dependency):
  db_shoes = db.query(models.Shoes).filter(models.Shoes.id == id).first()
  if not db_shoes:
    raise HTTPException(status_code=404, detail="Shoes not found")
  db_shoes.type = type
  db.commit()
  db.refresh(db_shoes)
  return db_shoes

# Delete Shoes by ID
@app.delete("/shoes/{id}")
async def delete_shoes_by_id(id: int, db: db_dependency):
  db_shoes = db.query(models.Shoes).filter(models.Shoes.id == id).first()
  if not db_shoes:
    raise HTTPException(status_code=404, detail="Shoes not found")
  db.delete(db_shoes)
  db.commit()
  return {"message": "Shoes deleted"}

