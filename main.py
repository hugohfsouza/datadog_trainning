from fastapi import FastAPI, HTTPException, Depends, Request
from typing import List
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from ddtrace import tracer, patch_all

from models import Person, PersonModel, Base, engine, get_db

patch_all(sqlalchemy=True, pymysql=True)

app = FastAPI()

# Datadog tracing middleware
@app.middleware("http")
async def trace_requests(request: Request, call_next):
    with tracer.trace("fastapi.request", resource=request.url.path):
        response = await call_next(request)
        return response

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# CRUD Endpoints
@app.post("/people/", response_model=Person)
def create_person(person: Person, db: Session = Depends(get_db)):
    if db.query(PersonModel).filter(PersonModel.id == person.id).first():
        raise HTTPException(status_code=400, detail="Person already exists")
    db_person = PersonModel(id=person.id, name=person.name, age=person.age)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@app.get("/people/", response_model=List[Person])
def list_people(db: Session = Depends(get_db)):
    return db.query(PersonModel).all()

@app.get("/people/{person_id}", response_model=Person)
def read_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@app.put("/people/{person_id}", response_model=Person)
def update_person(person_id: int, person: Person, db: Session = Depends(get_db)):
    db_person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    if person_id != person.id:
        raise HTTPException(status_code=400, detail="ID mismatch")
    db_person.name = person.name
    db_person.age = person.age
    db.commit()
    db.refresh(db_person)
    return db_person

@app.delete("/people/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    db.delete(person)
    db.commit()
    return {"detail": "Person deleted"}

# Serve frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
