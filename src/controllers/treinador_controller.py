from src.services import db_service

def obter_nome():
    return db_service.obter_nome_treinador()


def salvar_nome(nome: str):
    nome_limpo = (nome or "").strip()
    if not nome_limpo:
        return False
    db_service.salvar_nome_treinador(nome_limpo)
    return True


def tem_nome_definido():
    return obter_nome() is not None
