from src.models.pokemon import Pokemon
from src.services import db_service


def alternar_favorito(pokemon: Pokemon):
    if db_service.eh_favorito(pokemon.id):
        db_service.remover_favorito(pokemon.id)
        return False

    db_service.adicionar_favorito(pokemon.id, pokemon.nome, pokemon.sprite_url)
    return True


def listar():
    return db_service.listar_favoritos()


def eh_favorito(pokemon_id: int):
    return db_service.eh_favorito(pokemon_id)
