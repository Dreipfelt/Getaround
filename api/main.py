from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import joblib
import numpy as np
import uvicorn

app = FastAPI(title="Getaround Pricing API")

# Charger le modèle entraîné (pipeline complet)
model = joblib.load("model.joblib")

@app.get("/")
def read_root():
    return {"message": "Getaround Pricing API - use POST /predict"}

@app.post("/predict")
def predict(input: dict):
    """
    Input JSON attendu :
    {
      "input": [[mileage, engine_power, car_type, fuel, paint_color], ...]
    }
    """
    # 1. Extraire les données brutes
    raw = input["input"]  # liste de listes

    # 2. Créer un DataFrame avec les VRAIES colonnes d'entraînement
    import pandas as pd
    columns = ["mileage", "engine_power", "car_type", "fuel", "paint_color"]
    X = pd.DataFrame(raw, columns=columns)

    # 3. Prédire avec le pipeline complet (preprocessor + regressor)
    preds = model.predict(X)

    # 4. Retourner les prédictions arrondies
    return {"prediction": [int(round(p)) for p in preds]}
