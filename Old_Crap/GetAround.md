## 🧭 **Plan Global du Projet Getaround**

### 🎯 Objectifs principaux :

1. **Analyse des retards** (Data analysis & dashboard)
2. **Modèle de prédiction de prix** (Machine Learning + API)
3. **Mise en ligne :** un tableau de bord + une API avec documentation

---

## 🛠️ Outils à utiliser

| Partie du projet     | Outils recommandés                                                              |
| -------------------- | ------------------------------------------------------------------------------- |
| Analyse de données   | `pandas`, `matplotlib`, `seaborn`, `numpy`                                      |
| Dashboard Web        | `Streamlit` (simple et parfait pour débutants)                                  |
| Machine Learning     | `scikit-learn`, `pandas`                                                        |
| API & Documentation  | `FastAPI` (simple), `Uvicorn` (serveur), `Swagger` (auto-documentation)         |
| Mise en ligne        | `Hugging Face Spaces` pour Streamlit + FastAPI ou `Render`, `Railway`, `Vercel` |
| Versioning & partage | `Git`, `GitHub`                                                                 |

---

## 📁 Organisation de ton projet

```
getaround-project/
│
├── data/
│   ├── getaround_delay_analysis.csv
│   └── getaround_pricing_optimization.csv
│
├── notebooks/
│   └── analyse_retards.ipynb
│
├── app/
│   ├── dashboard.py         # ton app Streamlit
│   ├── api.py               # ton API FastAPI
│   └── model.pkl            # modèle de ML entraîné
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ✅ Étape 1 : Analyse des retards & dashboard (Data Analysis)

### 📌 Objectif : répondre aux questions du chef produit

#### 1.1 Charger et comprendre les données

* Fichier : `getaround_delay_analysis.csv`
* Utilise un notebook Jupyter (`notebooks/analyse_retards.ipynb`)

```python
import pandas as pd

df = pd.read_csv('data/getaround_delay_analysis.csv')
df.head()
df.info()
df.describe()
```

#### 1.2 Analyser les cas de retard

* Crée une colonne `delay_in_minutes = actual_end_time - scheduled_end_time`
* Identifie les retards critiques (si une autre location commence juste après)

#### 1.3 Répondre aux questions :

* Combien de locations ont été affectées par des retards ?
* Quelle est la proportion de voitures connectées affectées ?
* Quel pourcentage du chiffre d’affaires cela représente ?

Utilise des visualisations :

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.histplot(df['delay_in_minutes'])
```

#### 1.4 Crée ton dashboard Streamlit (`dashboard.py`)

```python
import streamlit as st
import pandas as pd

st.title("Analyse des retards - Getaround")
df = pd.read_csv("data/getaround_delay_analysis.csv")
st.dataframe(df.head())
# Affiche des graphes, KPIs, sliders pour seuils, etc.
```

#### 1.5 Héberge ton app :

* Crée un compte Hugging Face
* Héberge avec un dépôt Streamlit : [https://huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)

---

## ✅ Étape 2 : Modèle de prédiction de prix (Machine Learning)

### 2.1 Charger et comprendre les données

* Fichier : `getaround_pricing_optimization.csv`

### 2.2 Prétraitement

* Supprimer les colonnes inutiles
* Gérer les valeurs manquantes
* Normaliser si besoin

### 2.3 Entraîner un modèle simple

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

X = df.drop("rental_price_per_day", axis=1)
y = df["rental_price_per_day"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestRegressor()
model.fit(X_train, y_train)

joblib.dump(model, "app/model.pkl")
```

---

## ✅ Étape 3 : API avec /predict et /docs (FastAPI)

### 3.1 Crée l’API (`api.py`)

```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model = joblib.load("model.pkl")

class InputData(BaseModel):
    input: list

@app.post("/predict")
def predict(data: InputData):
    inputs = np.array(data.input)
    preds = model.predict(inputs).tolist()
    return {"prediction": preds}

@app.get("/docs")
def documentation():
    return {
        "title": "API de prédiction des prix",
        "endpoints": {
            "/predict": {
                "method": "POST",
                "input": [[...features]],
                "output": "[prix estimé]"
            }
        }
    }
```

### 3.2 Teste localement

```bash
uvicorn app.api:app --reload
```

### 3.3 Héberge ton API (Hugging Face Spaces + `FastAPI`)

* Regarde cet exemple : [https://huggingface.co/spaces/yuntian-deng/fastapi-template](https://huggingface.co/spaces/yuntian-deng/fastapi-template)

---

## ✅ Étape 4 : README + GitHub

Crée un fichier `README.md` :

````md
# Getaround - Projet Data Science

## 📊 Objectifs
- Analyser les retards de retour
- Construire un modèle de prédiction des prix
- Fournir une API en ligne et un tableau de bord

## 🔗 Liens
- Dashboard Streamlit : [URL Hugging Face]
- API FastAPI : [URL API Hugging Face]
- Documentation API : [URL]/docs

## 🚀 Installation
```bash
git clone ...
pip install -r requirements.txt
````

```

---

## ✅ Étape 5 : Bonus

Tu peux ajouter :
- Un système de logs dans l’API
- Un formulaire interactif dans Streamlit
- Une fonctionnalité de téléchargement CSV de résultats

---

## ⏱️ Temps estimé

| Étape                            | Durée estimée       |
|----------------------------------|---------------------|
| Analyse des données              | 3-4h                |
| Construction du dashboard        | 2h                  |
| Machine learning + test          | 3h                  |
| Création de l’API FastAPI        | 2h                  |
| Mise en ligne (Hugging Face)     | 1h                  |
| README et finalisation           | 1h                  |
| **Total estimé**                 | **12-15 heures**    |

---

## 🧡 Tu peux le faire !

C’est un **très bon projet pour apprendre** à faire une analyse complète de données **de A à Z**, avec de la mise en production.

Si tu veux, je peux t’aider à chaque étape : analyser ton CSV, coder le modèle, déployer l’API, etc. Tu veux qu’on commence par l’analyse de données ensemble ? 😊
```
