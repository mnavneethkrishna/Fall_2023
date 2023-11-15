from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import re

app = FastAPI()

engine = create_engine("sqlite:///phonebook.db", echo=True)
Base = declarative_base()

class PhoneBook(Base):
    __tablename__ = "phonebook"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    phone_number = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class Person(BaseModel):
    full_name: str
    phone_number: str

    @validator("full_name")
    def validate_full_name(cls, value):
        person_name_regex = re.compile(
            "^[A-Za-z]\\w{3,}|" +
            "^[a-z]+$|^[A-Z]+$|" +
            "[A-Za-z]\\w{3,}\\s[A-Za-z]\\w{2,}|" +
            "[A-Za-z]\\w{3,},\\s[A-Za-z]\\w{2,}|" +
            "[A-Za-z]\\w{3,},\\s[A-Za-z]\\w{2,}\\s[A-Za-z]\\w{3,}|" +
            "[A-Za-z]\\w{3,}\\s[A-Za-z]'[A-Za-z]\\w{3,}|" +
            "[A-Za-z]'[A-Za-z]\\w{2,},\\s[A-Za-z]\\w{3,}\\s[A-Za-z].+|" +
            "[A-Za-z]\\w{3,}\\s[A-Za-z]\\w|" +
            "[A-Za-z]\\w{3,}\\s[A-Za-z]'[A-Za-z]\\w{3,}-[A-Za-z]\\w{3,}$"
        )
        if not person_name_regex.match(value):
            raise ValueError("Invalid full name")
        return value

    @validator("phone_number")
    def validate_phone_number(cls, value):
        # Regular expression for acceptable phone numbers
        if not re.match(
            r"^\+?(\d{1,4}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,10}([-.\s]?\d{1,10})?$", value
        ):
            raise ValueError("Invalid phone number")
        return value

def log_operation(operation, person_name=None, http_code=None, message=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {operation} - {person_name} - HTTP Code: {http_code} - Message: {message}\n"
    with open("audit.log", "a") as log_file:
        log_file.write(log_entry)

def add_person_to_db(person):
    session = Session()
    existing_person = session.query(PhoneBook).filter_by(phone_number=person.phone_number).first()

    if existing_person:
        session.close()
        log_operation("add", person.full_name, http_code=400, message="Person already exists in the database")
        raise HTTPException(status_code=400, detail="Person already exists in the database")

    new_person = PhoneBook(full_name=person.full_name, phone_number=person.phone_number)
    session.add(new_person)
    session.commit()
    session.close()

    log_operation("add", person.full_name, http_code=200, message="Person added successfully")
    return {"message": "Person added successfully"}

def delete_person_by_name_from_db(full_name):
    session = Session()
    person = session.query(PhoneBook).filter_by(full_name=full_name).first()

    if not person:
        session.close()
        log_operation("delete", full_name, http_code=404, message="Person not found in the database")
        raise HTTPException(status_code=404, detail="Person not found in the database")

    session.delete(person)
    session.commit()
    session.close()

    log_operation("delete", full_name, http_code=200, message="Person deleted successfully")
    return {"message": "Person deleted successfully"}

def delete_person_by_number_from_db(phone_number):
    session = Session()
    person = session.query(PhoneBook).filter_by(phone_number=phone_number).first()

    if not person:
        session.close()
        log_operation("delete", person.full_name, http_code=404, message="Person not found in the database")
        raise HTTPException(status_code=404, detail="Person not found in the database")

    session.delete(person)
    session.commit()
    session.close()

    log_operation("delete", person.full_name, http_code=200, message="Person deleted successfully")
    return {"message": "Person deleted successfully"}

@app.get("/PhoneBook/list")
def list_phonebook():
    session = Session()
    phonebook = session.query(PhoneBook).all()
    session.close()
    log_operation("list", http_code=200, message="Phonebook listed successfully")
    return phonebook

@app.post("/PhoneBook/add")
def add_person(person: Person):
    return add_person_to_db(person)

@app.put("/PhoneBook/deleteByName")
def delete_by_name(full_name: str):
    return delete_person_by_name_from_db(full_name)

@app.put("/PhoneBook/deleteByNumber")
def delete_by_number(phone_number: str):
    return delete_person_by_number_from_db(phone_number)
