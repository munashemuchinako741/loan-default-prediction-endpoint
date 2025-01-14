from pydantic import BaseModel

class LoanApplication(BaseModel):
    features: list[float]