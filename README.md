# Loan Default Prediction API

This is a FastAPI-based endpoint for predicting loan default risk.

## Features

- Accepts loan application data as input.
- Predicts whether the loan will default (1) or not (0).

## Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the FastAPI server: `uvicorn app.main:app --reload`.

## API Endpoint

- **POST `/predict/`**: Accepts loan application data and returns a prediction.

## Example Request

```json
{
  "features": [0.5, 0.3, 0.2, 0.1, 0.4]
}
```
