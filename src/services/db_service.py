"""Camada de acesso ao banco SQLite.

Aqui ficam TODAS as queries do app. Quem importa esse módulo (controllers)
não sabe nem precisa saber que tem SQL por trás — se um dia a gente trocar
SQLite por outro banco, só esse arquivo muda.
"""
import sqlite3

from src.config.settings import DB_PATH


def _conexao():
    """Abre uma conexão nova com o banco. Função privada (prefixo _)."""
    return sqlite3.connect(DB_PATH)


def inicializar_banco():
    """Cria as tabelas caso ainda não existam. Roda no startup."""
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS favoritos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            sprite_url TEXT NOT NULL
        )
        """
    )
    # Tabela de treinador: guardamos sempre uma única linha (id=1) com o nome.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS treinador (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def salvar_nome_treinador(nome: str):
    """Cria ou atualiza o nome do treinador (sempre na linha id=1)."""
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO treinador (id, nome) VALUES (1, ?)",
        (nome,),
    )
    conn.commit()
    conn.close()


def obter_nome_treinador():
    """Retorna o nome do treinador, ou None se ainda não foi definido."""
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM treinador WHERE id = 1")
    linha = cursor.fetchone()
    conn.close()
    return linha[0] if linha else None


def adicionar_favorito(pokemon_id: int, nome: str, sprite_url: str):
    """Insere um Pokémon na tabela de favoritos (ignora se já existe)."""
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO favoritos (id, nome, sprite_url) VALUES (?, ?, ?)",
        (pokemon_id, nome, sprite_url),
    )
    conn.commit()
    conn.close()


def remover_favorito(pokemon_id: int):
    """Remove um Pokémon dos favoritos pelo ID."""
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favoritos WHERE id = ?", (pokemon_id,))
    conn.commit()
    conn.close()


def listar_favoritos():
    """Retorna todos os favoritos ordenados por nome."""
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, sprite_url FROM favoritos ORDER BY nome")
    linhas = cursor.fetchall()
    conn.close()
    return [
        {"id": linha[0], "nome": linha[1], "sprite_url": linha[2]}
        for linha in linhas
    ]


def eh_favorito(pokemon_id: int):
    """Verifica se um Pokémon já está nos favoritos."""
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM favoritos WHERE id = ?", (pokemon_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None
