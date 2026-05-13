import flet as ft

from src.config.routes import resolver_rota
from src.components.nav_bar import criar_nav_bar
from src.components.treinador_dialog import abrir_dialog_treinador
from src.controllers import treinador_controller
from src.services.db_service import inicializar_banco
from src.utils.keyboard import setup_teclado


def main(page: ft.Page):
    page.title = "PokéDex SENAI"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Garante que as tabelas (favoritos, treinador) existem no SQLite
    inicializar_banco()

    # Inicializa o controle de teclado virtual (ver src/utils/keyboard.py)
    setup_teclado(page)

    nav_bar = criar_nav_bar(page)

    def ao_mudar_rota(e):
        resolver_rota(page, nav_bar)

    page.on_route_change = ao_mudar_rota
    ao_mudar_rota(None)

    # Primeira vez no app: pergunta o nome do treinador.
    if not treinador_controller.tem_nome_definido():
        abrir_dialog_treinador(page, primeira_vez=True)


ft.run(main)