from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model.predict import predict
from schema.userInput import UserInput
from schema.response import Response

app = FastAPI()
        
@app.post('/predict', response_model=Response)
def predict_premiun(data: UserInput):

    try:
        prediction = predict(data)
    except Exception as e:
        return JSONResponse(status_code=500, content={"Error": str(e)})
    
    return prediction