from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import numpy as np


app = FastAPI(
    title="GetAround Pricing API",
    description="Pricing API using an XGBoost model optimized with GridSearchCV.",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)


# =============================
# LOAD MODEL
# =============================
model = joblib.load("model.joblib")


# =============================
# SCHEMAS
# =============================
class PredictionRequest(BaseModel):
    input: list[list[float]]

class PredictionResponse(BaseModel):
    prediction: list[float]


# =============================
# ROUTES
# =============================
@app.get("/")
def root():
    return {"message": "API running. Go to /docs for full Swagger UI"}


@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest):
    X = np.array(data.input)
    preds = model.predict(X)
    return {"prediction": preds.tolist()}


# =============================
# CUSTOM OPENAPI ROUTE
# =============================
@app.get("/openapi.json", include_in_schema=False)
async def openapi_json():
    return get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
        description=app.description
    )


# =============================
# DEFINITIVE SWAGGER UI ROUTE
# =============================
@app.get("/docs", include_in_schema=False)
async def swagger_docs():
    html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Swagger UI</title>
        <link href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" rel="stylesheet" />
      </head>
      <body>
        <div id="swagger-ui"></div>

        <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
        <script>
          window.onload = function() {
            SwaggerUIBundle({
              url: '/openapi.json',
              dom_id: '#swagger-ui'
            });
          };
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)