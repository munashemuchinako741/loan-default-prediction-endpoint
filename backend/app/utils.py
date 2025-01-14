import pickle
from pathlib import Path

def load_model():
    """
    Load the pre-trained machine learning model.
    """
    model_path = Path("../models/DecisionTree.pkl")
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model