import joblib
from pathlib import Path

class BoostedTree:
    def __init__ (self):
        current_dir = Path(__file__).resolve().parent
        path = current_dir / "boosted_tree.joblib"

        # Load the saved model back into memory
        self.tree = joblib.load(path)

    def predict (self, input):
        return self.tree.predict(input)

    def predict_proba(self, input):
        return self.tree.predict_proba(input)