"""Controller que orquestra a busca de Pokémon.

Recebe input da UI (view), valida, delega ao service, devolve o resultado.
"""
from src.models.pokemon import Pokemon
from src.services import pokeapi_service


async def buscar(termo: str):
    if not termo or not termo.strip():
        return None
    return await pokeapi_service.buscar_pokemon(termo)
