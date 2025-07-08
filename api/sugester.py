import sys
import numpy as np
import joblib
from .utils import *

df = get_dataframe()
print("Got dataframe")

all_pokemon = sorted(set(df["pokemon1"]).union(df["pokemon2"]))
print("Sorted")
mlb = get_binarizer(all_pokemon)

model = get_model(df, mlb, all_pokemon)
print("Model learned")

joblib.dump(model, "model.pkm")
joblib.dump(mlb, "binarizer.pkm")
print("Dumped Model")

move_df = pd.read_csv("moves_by_pkm.csv")

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def get_moves(pokemon_name):
    filtered = move_df[move_df["mon"].str.lower() == pokemon_name.lower()]
    return filtered["move"].unique().tolist()


def recomendar_pokemon(time, top_k=10, num_suggestions=5):
    time_set = frozenset(time)
    time_vec = mlb.transform([time_set])[0]
    candidates = [p for p in all_pokemon if p not in time]
    candidate_indices = [all_pokemon.index(p) for p in candidates]
    X_test = np.hstack(
        [
            np.repeat([time_vec], len(candidates), axis=0),
            np.array(candidate_indices).reshape(-1, 1),
        ]
    )
    scores = model.predict(X_test)
    top_indices = np.argsort(scores)[-top_k:][::-1]
    top_scores = scores[top_indices]
    probs = softmax(top_scores)
    chosen_indices = np.random.choice(
        top_indices, size=num_suggestions, replace=False, p=probs
    )
    return [(candidates[i], scores[i]) for i in chosen_indices]


if __name__ == "__main__":
    time = sys.argv[1:]
    recomendacoes = recomendar_pokemon(time)
    for poke, score in recomendacoes:
        print(f"Recommended: {poke} with estimated score: {score:.2f}")

    joblib.dump(model, "model.pkm")
    joblib.dump(mlb, "binarizer.pkm")
