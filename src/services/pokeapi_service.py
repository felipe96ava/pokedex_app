"""Camada de comunicação com a PokéAPI (https://pokeapi.co).

O service NUNCA conhece UI. Ele só faz request HTTP, trata erros e
devolve dados estruturados (model Pokemon ou None).
"""
import httpx

from src.config.settings import POKEAPI_URL, TIMEOUT_API
from src.models.pokemon import Pokemon


async def buscar_pokemon(nome_ou_id: str):
    """Busca um Pokémon pelo nome ou número. Retorna None se não achar."""

    url = f"{POKEAPI_URL}/pokemon/{nome_ou_id.lower().strip()}"

    async with httpx.AsyncClient() as client:
        try:
            resposta = await client.get(url, timeout=TIMEOUT_API)
            resposta.raise_for_status()
            dados = resposta.json()
        except (httpx.HTTPError, httpx.TimeoutException):
            return None

    sprite = dados["sprites"]["front_default"]
    if not sprite:
        # Alguns Pokémon não têm sprite "default"; usa fallback
        sprite = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"

    return Pokemon(
        id=dados["id"],
        nome=dados["name"].capitalize(),
        sprite_url=sprite,
        tipos=[t["type"]["name"] for t in dados["types"]],
        altura_m=dados["height"] / 10,   # API retorna em decímetros
        peso_kg=dados["weight"] / 10,    # API retorna em hectogramas
    )
