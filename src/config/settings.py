"""Configurações centralizadas do app.

Tudo que pode mudar entre ambientes (URL, caminho do banco) vem pra cá,
pra evitar valores 'mágicos' espalhados pelo código.
"""

POKEAPI_URL = "https://pokeapi.co/api/v2"
DB_PATH = "pokedex.db"
TIMEOUT_API = 10.0  # segundos
