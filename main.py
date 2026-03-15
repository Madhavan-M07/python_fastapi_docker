from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, Worlddddfefdeescdcd!"}

@app.get("/greet")
def greet():
    return {"message": "Hello, FastAPI!. I love you"}

@app.get('/greet/{name}')
def greet_name(name: str, age: Optional[int] = None):
    if age is None:
        return {"message": f"Hello, {name}!. I love you"}
    else:
        return {"message": f"Hello, {name}!. I love you and you are {age} years old."}
    


class Student(BaseModel):
    name: str
    age:int
    roll:int

@app.post('/student')
def create_student(student: Student):
    return {"message": f"Student {student.name} created successfully with age {student.age} and roll number {student.roll}."}


