import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import random


caminho_arquivo = 'model.pkm'

# Carrega o CSV
df = pd.read_csv('pkm.csv')

# Lista de todos pokémons únicos
todos_pokemons = pd.unique(df[['pokemon1', 'pokemon2']].values.ravel())

# Codificadores para nomes de pokémon
le = LabelEncoder()
le.fit(todos_pokemons)

# Codifica os pokémons
df['pokemon1_id'] = le.transform(df['pokemon1'])
df['pokemon2_id'] = le.transform(df['pokemon2'])

# Vamos gerar amostras de times e o próximo pokémon
# Suponha que cada linha representa uma interação útil entre dois pokémon

# Construção de dataset de treino com times
def gerar_amostras(df, n_amostras=10000):
    times = []
    alvos = []

    for _ in range(n_amostras):
        # Seleciona aleatoriamente 6 pares para formar um time (6 pokémon no total)
        amostra = df.sample(6)

        pokemons_ids = list(pd.concat([amostra['pokemon1_id'], amostra['pokemon2_id']]).unique())

        if len(pokemons_ids) < 6:
            continue

        random.shuffle(pokemons_ids)
        time = pokemons_ids[:5]
        alvo = pokemons_ids[5]

        # Preenche o time com -1 se tiver menos de 5 (por segurança)
        time += [-1] * (5 - len(time))
        times.append(time)
        alvos.append(alvo)

    return np.array(times), np.array(alvos)

X, y = gerar_amostras(df)

# Modelo de classificação

clf = None
if os.path.exists(caminho_arquivo):
    # Arquivo existe: carrega o modelo
    with open(caminho_arquivo, 'rb') as f:
        clf = pickle.load(f)
    print("Modelo carregado com sucesso!")
else:
    # Arquivo não existe: treina e salva um novo
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    
    with open(caminho_arquivo, 'wb') as f:
        pickle.dump(clf, f)
    print("Modelo treinado e salvo!")

# Função para sugerir próximo pokémon
def sugerir_pokemon(time, modelo, codificador):
    # time: lista de até 5 nomes de pokémon
    time_ids = [codificador.transform([p])[0] for p in time]
    time_ids += [-1] * (5 - len(time_ids))  # Preenche se for menos que 5

    pred_id = modelo.predict([time_ids])[0]
    return codificador.inverse_transform([pred_id])[0]

# Exemplo de uso
time_exemplo = ['Garchomp', 'Rotom-Wash', 'Scizor']
sugestao = sugerir_pokemon(time_exemplo, clf, le)
print(f"Sugestão de Pokémon para o time: {sugestao}")


#.mode csv
#.headers on
#.output pkm.csv
#SELECT 
#  mon.name AS pokemon1,
#  mon.usage AS uso_pokemon1, 
#  mon.viability_ceiling AS viability_ceiling_pokemon1,
#  mon2.name AS pokemon2, 
#  mon2.usage AS uso_pokemon2, 
#  mon2.viability_ceiling AS viability_ceiling_pokemon2
#FROM mon
#JOIN team t ON t.mon = mon.name
#JOIN mon mon2 ON t.mate = mon2.name;
#.output stdout