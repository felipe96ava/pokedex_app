import flet as ft

from src.config.routes import ROTAS


def criar_nav_bar(page: ft.Page):
    """Monta a NavigationBar do app e liga o evento de troca de aba."""

    async def ao_mudar_aba(e):
        indice = e.control.selected_index
        await page.push_route(ROTAS[indice])

    return ft.NavigationBar(
        selected_index=0,
        on_change=ao_mudar_aba,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Início",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SEARCH,
                label="Buscar",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.STAR,
                label="Favoritos",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON_OUTLINED,
                selected_icon=ft.Icons.PERSON,
                label="Perfil",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Config",
            ),
        ],
    )
