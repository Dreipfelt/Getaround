# GetAround – Delay Analysis & Pricing API

This project was built as part of the CDSD certification.  
It analyses rental delays on GetAround vehicles and provides:

- An interactive **Streamlit dashboard** for delay analysis & buffer simulation.
- A **FastAPI pricing API** using a model optimised with GridSearchCV.
- A clean, reproducible ML pipeline and documented repository structure.

---

## 🚀 Features

### **1. Delay Analysis Dashboard (Streamlit)**
- Computes core KPIs: late ratio, mean delay, distribution, percentiles.
- Supports simulation of mandatory buffer times between rentals.
- Includes dashboards for:
  - **All rentals**
  - **Connect-only rentals**
  - **Mobile-only rentals**

### **2. Pricing Model**
- Trained using:
  - XGBoost Regressor
  - GridSearchCV hyperparameter tuning
  - Full preprocessing pipeline (numerical scaling + categorical OHE)
- Exported into `model.joblib` for deployment.

### **3. Deployed FastAPI**
- Endpoints:
  - `GET /` → Health check
  - `POST /predict` → Predict rental price
  - `GET /docs` → Swagger UI
- Ready for HuggingFace Docker Spaces.

---

## 📁 Repository Structure

```text
Project_GetAround/
├── api/
│   ├── main.py                       # FastAPI pricing API
│   └── model.joblib                  # Trained ML model
│
├── dashboard/
│   └── app.py                        # Streamlit delay analysis dashboard
│
├── notebooks/
│   ├── 01_delay_analysis_eda.ipynb   # Delay KPIs + buffer simulation
│   └── 02_pricing_modeling.ipynb     # Pricing model training
│
├── data/
│   └── buffer_simulation_summary.csv # Generated dataset from dashboard
│
├── requirements.txt                  # Project dependencies
├── README.md
└── .gitignore
