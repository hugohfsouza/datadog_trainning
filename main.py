from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

class Person(BaseModel):
    id: int
    name: str
    age: int

# In-memory 'database'
people_db: Dict[int, Person] = {}

@app.post("/people/", response_model=Person)
async def create_person(person: Person):
    if person.id in people_db:
        raise HTTPException(status_code=400, detail="Person already exists")
    people_db[person.id] = person
    return person

# Endpoint to retrieve all people
@app.get("/people/", response_model=List[Person])
async def list_people():
    return list(people_db.values())

@app.get("/people/{person_id}", response_model=Person)
async def read_person(person_id: int):
    person = people_db.get(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@app.put("/people/{person_id}", response_model=Person)
async def update_person(person_id: int, person: Person):
    if person_id != person.id:
        raise HTTPException(status_code=400, detail="ID mismatch")
    if person_id not in people_db:
        raise HTTPException(status_code=404, detail="Person not found")
    people_db[person_id] = person
    return person

@app.delete("/people/{person_id}")
async def delete_person(person_id: int):
    if person_id not in people_db:
        raise HTTPException(status_code=404, detail="Person not found")
    del people_db[person_id]
    return {"detail": "Person deleted"}

