import os
import sqlite3
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MultiLabelBinarizer
from .pkm_utils import compatibility_score


def get_dataframe() -> pd.DataFrame:
    if os.path.exists("pkm.csv"):
        return pd.read_csv("pkm.csv")
    else:
        conn = sqlite3.connect("gen9vgc2025regg-0.sqlite")
        df = pd.read_sql(
            """
                    SELECT 
                    mon.name AS pokemon1,
                    mon2.name AS pokemon2, 
                    t.usage AS compatibility, 
                    mon2.viability_ceiling AS viability_ceiling_pokemon2
                    FROM mon
                    JOIN team t ON t.mon = mon.name
                    JOIN mon mon2 ON t.mate = mon2.name;
                    """,
            conn,
        )
        return df.to_csv("pkm.csv", index=False)


def get_model(
    df: pd.DataFrame, mlb: MultiLabelBinarizer, all_pokemon: list
) -> RandomForestRegressor:
    model = None
    if os.path.exists("model.pkm"):
        model = joblib.load("model.pkm")
    else:
        df["computed_compatibility"] = df.apply(lambda row: compatibility_score(row["pokemon1"], row["pokemon2"]), axis=1
        )
        print("Applied score")

        df["score"] = (
            df["computed_compatibility"]
            * df["compatibility"]
            * (df["viability_ceiling_pokemon2"] / 100)
        )
        print("Calculated score")
        
        examples = make_examples(df)
        X_team = mlb.fit_transform([e["team"] for e in examples])
        X_candidate = [all_pokemon.index(e["candidate"]) for e in examples]
        X = np.hstack([X_team, np.array(X_candidate).reshape(-1, 1)])
        y = np.array([e["score"] for e in examples])
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
    return model


def make_examples(df: pd.DataFrame) -> list:
    examples = []
    for p1 in df["pokemon1"].unique():
        subset = df[df["pokemon1"] == p1]
        for _, row in subset.iterrows():
            examples.append(
                {
                    "team": frozenset([p1]),
                    "candidate": row["pokemon2"],
                    "score": row["score"],
                }
            )
    return examples


def get_binarizer(all_pokemon: list) -> MultiLabelBinarizer:
    if os.path.exists("binarizer.pkm"):
        return joblib.load("binarizer.pkm")
    else:
        return MultiLabelBinarizer(classes=all_pokemon)
