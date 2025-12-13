📘 GetAround – Delay Analysis, Pricing Optimization & API Deployment
🎯 Project Overview

This project reproduces a real case study from GetAround, a leading peer-to-peer car-sharing platform.
It includes:

Delay analysis to understand late checkouts and their operational impact

Machine Learning pricing optimization (XGBoost optimized with GridSearchCV)

Deployment of a prediction API using FastAPI

Interactive dashboard deployed online with Streamlit

Hosting on Hugging Face Spaces

This work is delivered as part of a Data Science certification.

🚗 1. Delay Analysis (Streamlit Dashboard)

Late checkouts create operational friction, especially when two rentals are close together.
The dashboard analyzes:

Distribution of delays

Differences between Connect and Non-Connect rentals

Impact of different buffer thresholds (15, 30, 45, 60 min…)

Number of rentals potentially lost vs. operational gain

▶️ Run locally
streamlit run app.py

🤖 2. Pricing Optimization (Machine Learning)
Dataset

Pricing dataset available at:

https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv

Target

rental_price_per_day

Features

Numerical: mileage, engine_power…

Categorical: model_key, fuel, paint_color, car_type…

Binary: gps, air_conditioning, automatic, etc.

Model

A Pipeline combines:

StandardScaler (numeric)

OneHotEncoder (categorical)

XGBoostRegressor

Hyperparameter tuning with GridSearchCV

This approach provides the best R² score among tested models
(RandomForest, GradientBoosting, LinearRegression).

▶️ Train model
python train_model.py


This script:

Loads the pricing dataset

Builds preprocessing pipelines

Runs GridSearchCV

Saves the final model as model.joblib

🔌 3. Prediction API (FastAPI)

The deployed API loads model.joblib and exposes:

POST /predict

Input:

{
  "input": [
    [7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8]
  ]
}


Output:

{
  "prediction": [56.4]
}

GET /

Simple health check.

GET /docs

Custom Swagger UI (forced manually to ensure compatibility).

Designed to be fully compatible with Hugging Face Spaces.

▶️ Run API locally
uvicorn api:app --reload

🌐 4. Deployment on Hugging Face Spaces

Two Spaces are recommended:

A. Streamlit Dashboard (Space type: Streamlit)

Files required:

app.py
requirements.txt
data/


Deployment is automatic.

B. FastAPI Prediction API (Space type: Docker or FastAPI template)

Files required:

api.py
model.joblib
requirements.txt


Hugging Face exposes the API automatically at:

https://<username>.hf.space/predict
https://<username>.hf.space/docs

📂 5. Repository Structure
Project_GetAround/
│
├── app.py                   # Streamlit dashboard
├── api.py                   # FastAPI model API
├── train_model.py           # ML training script with GridSearchCV
├── model.joblib             # Final trained model
├── requirements.txt
│
├── data/
│   ├── get_around_delay_analysis.xlsx
│   └── get_around_pricing_project.csv
│
├── notebooks/
│   ├── delay_analysis.ipynb
│   └── pricing_model.ipynb
│
└── README.md

✔️ 6. Key Results

Significant share of rentals have delays → potential operational friction

Minimum buffer time can reduce customer dissatisfaction at the cost of some revenue

Optimized XGBoost model achieves strong R² performance for pricing

API and dashboard fully deployed and functional

🏁 Conclusion

This project combines:

Exploratory Data Analysis

Machine Learning

Model optimization

API development

Frontend dashboarding

Deployment in production

It demonstrates a full end-to-end Data Science workflow, ready for real-world usage.