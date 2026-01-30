from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model = joblib.load('models/pricing_model.pkl')

class PredictRequest(BaseModel):
    input: list[list[float]]

@app.post("/predict")
def predict(request: PredictRequest):
    predictions = model.predict(request.input)
    return {"prediction": predictions.tolist()}

# Documentation automatique sur /docs