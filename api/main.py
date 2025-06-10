from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from .sugester import recomendar_pokemon

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PokemonRequest(BaseModel):
    selected_pokemon: list[str]

pokemon_cache = None

async def load_pokemon_list():
    global pokemon_cache
    if pokemon_cache is None:
        print("🔄 Carregando lista de Pokémon da PokéAPI...")
        async with httpx.AsyncClient() as client:
            response = await client.get("https://pokeapi.co/api/v2/pokemon?limit=3000")
            pokemon_cache = response.json()["results"]
    return pokemon_cache


def capitalizar_nomes(nomes : list[str]) -> list[str]:
    return ['-'.join(p.capitalize() for p in nome.split('-')) for nome in nomes]

@app.post("/recommend")
async def recommend_pokemon(data: PokemonRequest):
    selected = set(p.lower() for p in data.selected_pokemon)
    full_list = await load_pokemon_list()

    async with httpx.AsyncClient() as client:
        response = await client.get("https://pokeapi.co/api/v2/pokemon?limit=3000")
        full_list = response.json()["results"]
    
    candidates = recomendar_pokemon(capitalizar_nomes(selected)) #["charmander"]
    candidate_names = set(name.lower() for name, _ in candidates)


    recomendados_info = [poke for poke in full_list if poke["name"] in candidate_names]

    results = []
    for poke in recomendados_info:
        async with httpx.AsyncClient() as client:
            name = poke["name"]
            poke_response = await client.get(poke["url"])
        data = poke_response.json()
        sprite_url = data["sprites"]["front_default"]
        results.append({"name": name, "image": sprite_url})

    return results