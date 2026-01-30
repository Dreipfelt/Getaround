# GetAround — Delay Analysis & Pricing API

## Project Context

GetAround is a peer-to-peer car rental platform.

Two recurring operational challenges directly impact user satisfaction and revenue:

- **Late returns** cause friction for the next renter  
- **Pricing optimization** is essential to balance competitiveness and owner revenue

This project addresses both problems through:

- Delay analysis and buffer simulation  
- A machine learning pricing model  
- A production-ready API  
- A Streamlit dashboard for business insights  

---

## Project Objectives

### 1. Delay Analysis
- Understand late return patterns
- Measure their impact on subsequent rentals
- Simulate buffer policies between rentals

### 2. Pricing Optimization
- Train a regression model to predict daily rental prices
- Deploy the model via a FastAPI endpoint

### 3. Industrialization
- Deliver a dashboard for business exploration
- Serve predictions through a REST API

---

## Delay Analysis & Buffer Simulation

The delay dataset is analyzed to answer key business questions:

- How often are cars returned late?
- How large are the delays?
- Which check-in methods are most impacted?

A **buffer simulation** evaluates how introducing a minimum time gap between rentals reduces cascading delays while limiting revenue loss.

**Key output file:**
data/buffer_simulation_summary.csv

**Notebook:**
notebooks/01_delay_analysis_eda.ipynb


---

## Pricing Model

A supervised regression model predicts the daily rental price of a car.

### Target
- `rental_price_per_day`

### Features
- Mileage
- Engine power
- Fuel type
- Paint color
- Car type

### Model
- RandomForestRegressor
- Full preprocessing pipeline:
  - StandardScaler for numerical features
  - OneHotEncoder for categorical features

### Evaluation
- RMSE (train / test)
- R² score on test set (~0.73)

The trained pipeline is exported for API usage:

api/model.joblib

**Notebook:**
notebooks/02_pricing_modeling.ipynb


---

## Pricing API (FastAPI)

The pricing model is served through a REST API.

### Run locally

pip install -r requirements.txt

uvicorn api.main:app --reload

### API available at:
http://127.0.0.1:8000/

Swagger UI: http://127.0.0.1:8000/docs

## Endpoint: POST /predict

## Description: Predict the daily rental price of a car.

## Request body (JSON)
{
  "mileage": 45000,
  "engine_power": 110,
  "fuel": "diesel",
  "paint_color": "black",
  "car_type": "sedan"
}

## Response
{
  "rental_price_per_day": 132.28
}

## Dashboard (Streamlit)

A Streamlit dashboard provides:

- Delay distributions,

- Late return ratios,

- Impact of buffer policies.

## Run locally:
streamlit run dashboard/app.py

## Repository Structure
'''Project_GetAround/
├── api/
│   ├── main.py                 # FastAPI application (pricing prediction)
│   └── model.joblib            # Trained ML pricing pipeline
│
├── dashboard/
│   └── app.py                  # Streamlit dashboard (delay & buffer analysis)
│
├── notebooks/
│   ├── 01_delay_analysis_eda.ipynb
│   └── 02_pricing_modeling.ipynb
│
├── data/
│   └── buffer_simulation_summary.csv
│
├── requirements.txt
├── README.md
└── .gitignore'''

## Deployment (Hugging Face)

The pricing model is deployed as a public FastAPI service on Hugging Face Spaces.

Steps:
1. Create a Docker Space
2. Push the dedicated API repository
3. Access Swagger UI at `/docs`

## Conclusion
This project demonstrates:

- Business-oriented data analysis, 
- Robust machine learning pipelines,
- Clean deployment practices.

It illustrates how data science decisions can directly improve operational reliability and pricing strategy for a mobility platform like GetAround.
