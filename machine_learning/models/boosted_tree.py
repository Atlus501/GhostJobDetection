from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

import asyncio
import pandas as pd
import joblib
import mlflow
import logging
from pathlib import Path

from artifacts.boosted_tree_config import default_tree
from config.mlflow import mlflow_config
from data_gen.ghost_job import GhostJobDB


def get_curr_dir():
    path = Path(__file__).resolve().parent
    return path

"""
Sets up the mlflow
"""
def setup_mlflow(version, user_id=1, session_id=1):
    # Specify the tracking URI for the MLflow server.
    mlflow.set_tracking_uri("sqlite:///mlflow.db")

    # Specify the experiment you just created for your LLM application or AI agent.
    mlflow.set_experiment(mlflow_config.application)

    mlflow.sklearn.autolog(
        log_models=True,
        log_datasets=True,
        log_post_training_metrics=True,
        registered_model_name="GhostJobClassifier",
    )

"""
Attempts to read model artifacts to load the boosted tree.
Otherwise, return a default graident boosting classifier tree
"""
def load_model(version):
    try:
        path = get_curr_dir().parent / "artifacts" / f"boosted_tree{version}.joblib"
        tree = joblib.load(path)
        print("loading existing joblib file")
        return tree
    except FileNotFoundError as e:
        print("file not found. Returning default tree")
        return GradientBoostingClassifier(**default_tree.model_dump())

"""
Loads data from a file
"""
async def load_data(heuristic=True, file="heuristic.csv"):
    if heuristic:
        try:
            path = get_curr_dir().parent / "data" / file
            df = pd.read_csv(path)
            print("using heuristcal data")
            return df
        except FileNotFoundError as e: 
            raise FileNotFoundError(str(e))

    print("Fetching data from pymonogo")

    db = GhostJobDB()
    entries = await db.load()

    if not entries:
        raise ValueError("No records found in MongoDB collection!")

    df = pd.DataFrame(entries)

    if "_id" in df.columns:
        df.drop(columns=["_id"])

    return df

"""
evaluates a model based on its accuracy, precision, and recall
"""
def evaluate_model(tree, X_test, y_test):
    y_pred = tree.predict(X_test)
    scores = {"accuracy" : accuracy_score(y_test, y_pred),
                "precision" : precision_score(y_test, y_pred),
                "recall" : recall_score(y_test, y_pred)}

    return scores

    
"""
Saves a model into the joblib file
"""
def save_model(tree, version):
    path = get_curr_dir().parent / "artifacts" / f"boosted_tree{version}.joblib"
    joblib.dump(tree, path)


"""
Function that loads the model and then trains it 
"""
async def train_model(version="1.0.0", target="ghost_job", dataset_type="heuristic"):
    tree = load_model(version)

    df = await load_data(heuristic=(dataset_type == "heuristic"))

    X = df.drop(target, axis=1)
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    setup_mlflow(version)

    with mlflow.start_run() as run:
        tree.fit(X_train, y_train)
        scores = evaluate_model(tree, X_test, y_test)

        #logging metrics using mlflow
        mlflow.set_tags(
            {
                "model" : "GhostJobClassifier",
                "version" : version,
                "datatype" : dataset_type,
            }
        )
        mlflow.log_metrics(scores)

        print("evluation scores ", scores)

    save_model(tree, version)

if __name__ == "__main__":
    version="v1"
    log_path = Path(__file__).resolve().parent.parent / "logs" / f"boosted_tree{version}.log"
    logging.basicConfig(level=logging.INFO, filename=log_path)

    asyncio.run(train_model(version=version))