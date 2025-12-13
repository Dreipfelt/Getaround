import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from xgboost import XGBRegressor


# ============================================================
# 1. LOAD DATA
# ============================================================

DATA_URL = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv"

print("Loading dataset...")
df = pd.read_csv(DATA_URL, encoding="latin")

TARGET = "rental_price_per_day"

X = df.drop(columns=[TARGET])
y = df[TARGET]

num_cols = X.select_dtypes(include="number").columns.tolist()
cat_cols = X.select_dtypes(exclude="number").columns.tolist()

print(f"Numeric features: {num_cols}")
print(f"Categorical features: {cat_cols}")


# ============================================================
# 2. PREPROCESSING PIPELINE
# ============================================================

numeric_transformer = Pipeline(steps=[
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, num_cols),
        ("cat", categorical_transformer, cat_cols)
    ]
)


# ============================================================
# 3. BASE MODEL (for GridSearch)
# ============================================================

base_model = XGBRegressor(
    objective="reg:squarederror",
    random_state=42
)

pipe = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("model", base_model)
])


# ============================================================
# 4. GRID SEARCH (mini-grid)
# ============================================================

param_grid = {
    "model__n_estimators": [200, 300],
    "model__max_depth": [4, 6],
    "model__learning_rate": [0.05, 0.1],
    "model__subsample": [0.8],
    "model__colsample_bytree": [0.8]
}

print("Starting GridSearchCV...")
grid = GridSearchCV(
    estimator=pipe,
    param_grid=param_grid,
    scoring="r2",
    cv=3,
    n_jobs=-1,
    verbose=1
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

grid.fit(X_train, y_train)

print("Best parameters found:")
print(grid.best_params_)

print("Best cross-validation R2 score:")
print(grid.best_score_)


# ============================================================
# 5. SAVE BEST MODEL
# ============================================================

best_model = grid.best_estimator_
joblib.dump(best_model, "model.joblib")

print("Model successfully saved to model.joblib")