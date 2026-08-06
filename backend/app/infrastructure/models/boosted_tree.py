import joblib
from pathlib import Path
import boto3

from config.settings import settings

class BoostedTree:
    def __init__ (self):
        current_dir = Path(__file__).resolve().parent
        path = current_dir / "boosted_tree.joblib"

        s3 = boto3.client("s3",
                            aws_access_key_id=settings.AWS_ACCESS_KEY,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        s3.download_file(
            "boosted-tree-joblib-893410593768-us-east-1-an",
            "boosted_tree.joblib",
            path
        )

        # Load the saved model back into memory
        self.tree = joblib.load(path)

    def predict (self, input):
        return self.tree.predict(input)

    def predict_proba(self, input):
        return self.tree.predict_proba(input)