import pandas as pd

from schemas.model import Predictors

"""
Class for predicting ghost jobs
"""
class GhostJobPredictor:
    """
    Constructor that adds the model
    """
    def __init__(self, model):
        self.model = model

    """
    Predicts the target class and probability that a class is a ghost job
    """
    def predict(self, predictors : Predictors):
        df = pd.DataFrame([predictors.model_dump()]) 

        prediction = self.model.predict(df)[0]
        probability = float(max(self.model.predict_proba(df)[0]))

        return prediction, probability