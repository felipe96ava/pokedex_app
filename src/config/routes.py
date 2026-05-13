import flet as ft

from src.views.home_view import tela_inicio
from src.views.buscar_view import tela_buscar
from src.views.favoritos_view import tela_favoritos
from src.views.perfil_view import tela_perfil
from src.views.config_view import tela_config


ROTAS = ["/", "/buscar", "/favoritos", "/perfil", "/config"]


def resolver_rota(page: ft.Page, nav_bar: ft.NavigationBar):
    """Decide qual tela renderizar com base em page.route."""

    if page.route in ROTAS:
        nav_bar.selected_index = ROTAS.index(page.route)

    if page.route == "/":
        conteudo = tela_inicio()
    elif page.route == "/buscar":
        conteudo = tela_buscar(page)
    elif page.route == "/favoritos":
        conteudo = tela_favoritos(page)
    elif page.route == "/perfil":
        conteudo = tela_perfil()
    elif page.route == "/config":
        conteudo = tela_config(page)
    else:
        conteudo = ft.Text("Página não encontrada")

    page.views.clear()
    page.views.append(
        ft.View(
            route=page.route,
            controls=[conteudo],
            navigation_bar=nav_bar,
        )
    )
