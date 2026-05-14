import sqlite3

from src.config.settings import DB_PATH

def _conexao():
    return sqlite3.connect(DB_PATH)


def inicializar_banco():
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
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO treinador (id, nome) VALUES (1, ?)",
        (nome,),
    )
    conn.commit()
    conn.close()


def obter_nome_treinador():
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM treinador WHERE id = 1")
    linha = cursor.fetchone()
    conn.close()
    return linha[0] if linha else None


def adicionar_favorito(pokemon_id: int, nome: str, sprite_url: str):
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO favoritos (id, nome, sprite_url) VALUES (?, ?, ?)",
        (pokemon_id, nome, sprite_url),
    )
    conn.commit()
    conn.close()


def remover_favorito(pokemon_id: int):
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favoritos WHERE id = ?", (pokemon_id,))
    conn.commit()
    conn.close()


def listar_favoritos():
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
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM favoritos WHERE id = ?", (pokemon_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None
