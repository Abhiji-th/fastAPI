from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
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

class UpdatePatient(BaseModel):
    id: Optional[Annotated[str, Field(..., description="Unique ID of the patient", examples=["P001"])]] = None
    name: Optional[Annotated[str, Field(..., description="Name of the patient", )]] = None
    age: Optional[Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient", )]] = None
    gender: Optional[Annotated[Literal["Male", "Female"], Field(..., description="Gender of the patient", )]] = None
    city: Optional[Annotated[str, Field(..., description="City where the patient resides", )]] = None
    height: Optional[Annotated[float, Field(..., gt=0, description="Height of the patient in Mtrs", )]] = None
    weight: Optional[Annotated[float, Field(..., gt=0, description="Weight of the patient in Kgs", )]] = None

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

@app.get('/sort')
def sort(sort_by: str = Query(...), order_by: str=Query(...)):
    
    data = load_data()

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Not valid sort field")
    
    if order_by not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')    
    

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=(order_by=="desc"))

    return sorted_data

@app.put('/edit/{patient_id}')
def update(patient_id: str, patient: UpdatePatient):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=400, detail="Patiend doesnt exist")
    
    existing = data[patient_id]

    new = patient.model_dump(exclude_unset=True);

    for key, value in new.items():
        existing[key] = value

    existing['id'] = patient_id
    pydantic_obj = Patient(**existing)

    data[patient_id] = pydantic_obj.model_dump(exclude=["id"]) 

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Updated'})
        
@app.delete('/delete/{patient_id}')
def delete(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=400, detail="Not found")
    
    del data[patient_id]

    save_data(data)

    return {"msg": "Deleted"}
