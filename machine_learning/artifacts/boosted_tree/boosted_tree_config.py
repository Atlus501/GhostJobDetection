from pydantic import BaseModel

"""
Default configrations for a boosted tree
"""
class BoostedTreeConfig(BaseModel):
    loss: str = "log_loss"
    learning_rate: float = 0.1
    n_estimators: int = 100
    min_samples_split: int = 4
    min_samples_leaf: int = 4
    max_depth: int = 3

default_tree = BoostedTreeConfig()