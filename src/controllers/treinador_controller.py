"""Controller do treinador.

Cuida das regras de negócio relacionadas ao nome do treinador.
"""
from src.services import db_service


def obter_nome():
    """Retorna o nome do treinador salvo (ou None se nunca foi definido)."""
    return db_service.obter_nome_treinador()


def salvar_nome(nome: str):
    """Salva o nome do treinador. Retorna False se o nome for vazio/inválido."""
    nome_limpo = (nome or "").strip()
    if not nome_limpo:
        return False
    db_service.salvar_nome_treinador(nome_limpo)
    return True


def tem_nome_definido():
    """Indica se o app já tem um nome de treinador configurado."""
    return obter_nome() is not None
