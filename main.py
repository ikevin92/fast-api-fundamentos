# Python
from typing import Optional
from enum import Enum
# Pydantic
from pydantic import BaseModel, Field
# FastApi
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

# Models


class HairColor(Enum):
    white = "white"
    black = "black"
    browm = "browm"
    yelow = "yelow"
    blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str
    state: str
    country: str

    class Config:
        schema_extra = {
            "example": {
                "city": "San Francisco",
                "state": "California",
                "country": "USA"
            }
        }


class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        title="First Name",
        example="John",
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        title="Last Name",
        example="Connor"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=29
    )
    hair_color: Optional[HairColor] = Field(
        default=None,
        example=HairColor.blonde
    )
    is_married: Optional[bool] = Field(default=None, example=False)

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Kevin",
    #             "last_name": "Echeverri",
    #             "age": 29,
    #             "hair_color": "black",
    #             "is_married": False,
    #         }
    #     }


class Person(PersonBase):
    password: str = Field(..., min_length=8)


class PersonOut(PersonBase):
    pass


@app.get("/")
def home():
    return {"Hello": "World"}


# Request and Response Body
@app.post("/person/new", response_model=PersonOut)
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        description="This is the person name. It's between 1 and 50 characters long.",
        example="John",
    ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's a number and required",
        example=30
    ),
):
    return {
        name: age
    }


# Validaciones: Path Parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person Id",
        description="This is the person id. It's a number and required",
        example=23
    )
):
    return {person_id: "It exist!"}


# Validaciones: Requets Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person Id",
        description="This is the person id. It's a number and required",
        example=23
    ),
    person: Person = Body(
        ...,
        title="Person",
        description="This is the person. It's a Object and required"
    ),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results

# https://pydantic-docs.helpmanual.io/usage/types/#pydantic-types
