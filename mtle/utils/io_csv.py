from __future__ import annotations
from pathlib import Path
import pandas as pd

def load_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path, index_col=False)

def save_csv(df: pd.DataFrame, path: str | Path, index: bool = False) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index)

class Checkpointer:
    def __init__(self, out_path: str | Path, every: int = 20):
        self.out_path = Path(out_path)
        self.every = every
        self._counter = 0

    def step(self, df: pd.DataFrame):
        self._counter += 1
        if self._counter % self.every == 0:
            save_csv(df, self.out_path)
