import requests
import pandas as pd

type_cache = {}
role_cache = {}

TYPE_CHART = {
    "Normal": {"weak": ["Fighting"], "resist": [], "immune": ["Ghost"]},
    "Fire": {
        "weak": ["Water", "Ground", "Rock"],
        "resist": ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"],
        "immune": [],
    },
    "Water": {
        "weak": ["Electric", "Grass"],
        "resist": ["Fire", "Water", "Ice", "Steel"],
        "immune": [],
    },
    "Electric": {
        "weak": ["Ground"],
        "resist": ["Electric", "Flying", "Steel"],
        "immune": [],
    },
    "Grass": {
        "weak": ["Fire", "Ice", "Poison", "Flying", "Bug"],
        "resist": ["Water", "Electric", "Grass", "Ground"],
        "immune": [],
    },
    "Ice": {
        "weak": ["Fire", "Fighting", "Rock", "Steel"],
        "resist": ["Ice"],
        "immune": [],
    },
    "Fighting": {
        "weak": ["Flying", "Psychic", "Fairy"],
        "resist": ["Bug", "Rock", "Dark"],
        "immune": [],
    },
    "Poison": {
        "weak": ["Ground", "Psychic"],
        "resist": ["Grass", "Fighting", "Poison", "Bug", "Fairy"],
        "immune": [],
    },
    "Ground": {
        "weak": ["Water", "Grass", "Ice"],
        "resist": ["Poison", "Rock"],
        "immune": ["Electric"],
    },
    "Flying": {
        "weak": ["Electric", "Ice", "Rock"],
        "resist": ["Grass", "Fighting", "Bug"],
        "immune": ["Ground"],
    },
    "Psychic": {
        "weak": ["Bug", "Ghost", "Dark"],
        "resist": ["Fighting", "Psychic"],
        "immune": [],
    },
    "Bug": {
        "weak": ["Fire", "Flying", "Rock"],
        "resist": ["Grass", "Fighting", "Ground"],
        "immune": [],
    },
    "Rock": {
        "weak": ["Water", "Grass", "Fighting", "Ground", "Steel"],
        "resist": ["Normal", "Fire", "Poison", "Flying"],
        "immune": [],
    },
    "Ghost": {
        "weak": ["Ghost", "Dark"],
        "resist": ["Poison", "Bug"],
        "immune": ["Normal", "Fighting"],
    },
    "Dragon": {
        "weak": ["Ice", "Dragon", "Fairy"],
        "resist": ["Fire", "Water", "Electric", "Grass"],
        # Os tipos que causam dano super efetivo (2x) ao tipo 't'
        "immune": [],
    },
    "Dark": {
        "weak": ["Fighting", "Bug", "Fairy"],
        "resist": ["Ghost", "Dark"],
        "immune": ["Psychic"],
    },
    "Steel": {
        "weak": ["Fire", "Fighting", "Ground"],
        "resist": [
            "Normal",
            "Grass",
            "Ice",
            "Flying",
            "Psychic",
            "Bug",
            "Rock",
            "Dragon",
            "Steel",
            "Fairy",
        ],
        "immune": ["Poison"],
    },
    "Fairy": {
        "weak": ["Poison", "Steel"],
        "resist": ["Fighting", "Bug", "Dark"],
        "immune": ["Dragon"],
    },
}


def get_weaknesses(pokemon_types):
    weaknesses = set()
    for t in pokemon_types:
        entry = TYPE_CHART.get(t, {})
        weaknesses.update(entry.get("weak", []))
    return weaknesses


def get_resistances(pokemon_types):
    resistances = set()
    for t in pokemon_types:
        entry = TYPE_CHART.get(t, {})
        resistances.update(entry.get("resist", []))
    return resistances


def compatibility_score(p1, p2):
    types1 = get_pokemon_types(p1)
    types2 = get_pokemon_types(p2)
    p1_weaknesses = get_weaknesses(types1)

    p2_resistances = get_resistances(types2)

    coverage_bonus = 0.0
    if p1_weaknesses:
        coverage_bonus = len(p1_weaknesses & p2_resistances) / len(p1_weaknesses)

    role1 = get_pokemon_role(p1)
    role2 = get_pokemon_role(p2)
    role_bonus = 1.0 if role1 != role2 else 0.4

    type_overlap = len(set(types1) & set(types2))
    type_diversity = 1.0 - (type_overlap / max(len(types1), 1))

    score = 0.4 * coverage_bonus + 0.4 * role_bonus + 0.2 * type_diversity
    return round(score, 4)


def get_pokemon_types(name: str):
    global type_cache
    name = name.lower().replace(" ", "-").replace("’", "").replace(".", "")
    if name in type_cache:
        return type_cache[name]
    if name in type_cache:
        return type_cache[name]

    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        types = [t["type"]["name"].capitalize() for t in data["types"]]
        type_cache[name] = types
        return types
    except Exception as e:
        print(f"Erro ao buscar {name}: {e}")
        type_cache[name] = []
        return []


def get_pokemon_role(name: str) -> str:
    global role_cache
    name = name.lower().replace(" ", "-").replace("’", "").replace(".", "")
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
        hp, atk, defense, sp_atk, sp_def, speed = (
            stats.get("hp", 0),
            stats.get("attack", 0),
            stats.get("defense", 0),
            stats.get("special-attack", 0),
            stats.get("special-defense", 0),
            stats.get("speed", 0),
        )

        # --- Heurísticas simples:
        if (atk >= 120 or sp_atk >= 120) and speed >= 90:
            role_cache[name] = "sweeper"
        elif (defense >= 120 or sp_def >= 120) and hp >= 100:
            role_cache[name] = "wall"
        elif speed >= 100 and max(atk, sp_atk) < 110:
            role_cache[name] = "pivot"
        elif hp >= 130 and max(defense, sp_def) < 100:
            role_cache[name] = "cleric"
        else:
            role_cache[name] = "flex"
    except Exception as e:
        print(f"Erro ao buscar função de {name}: {e}")
        role_cache[name] = "unknown"
    return role_cache[name]
