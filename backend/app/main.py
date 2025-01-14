from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import numpy as np
import pandas as pd
from .utils import load_model
from .logging_config import setup_logging
import pickle
import statsmodels.api as sm
from sklearn.tree import DecisionTreeClassifier
import os


# Initialize logging
setup_logging()

# Load the pre-trained model
model = load_model()

# Initialize FastAPI app
app = FastAPI()

# Get the absolute path to the static directory
static_dir = os.path.join(os.path.dirname(__file__), "static")

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Set up Jinja2 templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# Define the input model
class LoanApplication(BaseModel):
    features: List[float]

# Root endpoint to serve the index.html file
#@app.get("/")
#async def root():
#with open("static/index.html", "r") as file:
#return HTMLResponse(content=file.read())

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request})


# Prediction endpoint
@app.post("/predict")
async def predict(loan_application: LoanApplication):
    X = loan_application.features  
    try:
        # Validate input data
        if len(X) != 6:
            raise HTTPException(status_code=400, detail="Invalid input data")
        # Convert input features to a pandas DataFrame
        columns = ["interest_rate", "remaining term", "salary", "outstanding_balance", "age", "loan_amount"]
        df = pd.DataFrame([X], columns=columns)
        
        # Transform the input data
        scaler = pickle.load(open("../models/StandardScaler.pkl", "rb"))
        df[columns] = scaler.transform(df[columns])
        
        # Load the trained model
        trained_model = pickle.load(open("../models/DecisionTree.pkl", "rb"))
        
        # Get the feature names from the trained model
        feature_names = trained_model.feature_names_in_
        
        # Create a new DataFrame with the correct feature names in the correct order
        new_df = pd.DataFrame(index=[0])
        new_df[feature_names] = 0  # Initialize all features to 0
        new_df['const'] = 1  # Set the constant feature
        new_df['interest_rate'] = df['interest_rate'].values[0]
        new_df['remaining term'] = df['remaining term'].values[0]
        new_df['salary'] = df['salary'].values[0]
        new_df['outstanding_balance'] = df['outstanding_balance'].values[0]
        new_df['age'] = df['age'].values[0]
        new_df['loan_amount'] = df['loan_amount'].values[0]
        new_df['number_of_defaults'] = 0  # Set the number_of_defaults feature
        
        # Use the trained model to make predictions
        try:
            y_pred = trained_model.predict(new_df[feature_names])
            confidence = trained_model.predict_proba(new_df[feature_names])[0][int(y_pred[0])] * 100  # Convert to percentage
        
        # Return the prediction result with confidence level
            return {
                "prediction": int(y_pred[0]),
                "confidence": confidence
            }
        except Exception as e:
            return {
                "error": str(e),
                "message": "An error occurred while making the prediction."
            }
            
    except Exception as e:
        # Log the error
        print(f"Error: {str(e)}")
        
        # Raise a HTTP exception with a more informative error message
        raise HTTPException(status_code=400, detail=str(e))