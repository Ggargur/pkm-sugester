import sys
import numpy as np
import joblib
import utils

df = utils.get_dataframe()

# Improve score function
df["score"] = df["compatibility"] * (df["viability_ceiling_pokemon2"] / 100)

all_pokemon = sorted(set(df["pokemon1"]).union(df["pokemon2"]))
mlb = utils.get_binarizer(all_pokemon)

model = utils.get_model(df, mlb, all_pokemon)


def recomendar_pokemon(time, top_k=5):
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
    return [(candidates[i], scores[i]) for i in top_indices]


if __name__ == "__main__":
    time = sys.argv[1:]
    recomendacoes = recomendar_pokemon(time)
    for poke, score in recomendacoes:
        print(f"Recommended: {poke} with estimated score: {score:.2f}")

    joblib.dump(model, "model.pkm")
    joblib.dump(mlb, "binarizer.pkm")
