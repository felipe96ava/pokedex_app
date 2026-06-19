from src.services import pokeapi_service


async def buscar(termo: str):
    if not termo or not termo.strip():
        return None
    return await pokeapi_service.buscar_pokemon(termo)
