from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

def load_data():
    with open("patients.json", 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Unique ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal["Male", "Female"], Field(..., description="Gender of the patient")]
    city: Annotated[str, Field(..., description="City where the patient resides")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in Mtrs")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in Kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'        

@app.get('/')
def view():
    data = load_data()
    return data

@app.post('/')
def create(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    data[patient.id] = patient.model_dump(exclude=["id"])

    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient added successfully"})


        