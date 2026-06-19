import flet as ft

from src.controllers import favoritos_controller
from src.services import db_service


def tela_favoritos(page: ft.Page):
    container = ft.Container(expand=True, padding=20)

    def renderizar():
        favoritos = favoritos_controller.listar()

        if not favoritos:
            container.content = ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.STAR_BORDER, size=60, color=ft.Colors.GREY),
                    ft.Text("Você ainda não tem favoritos.", size=18),
                    ft.Text(
                        "Vá em Buscar e marque o coração de um Pokémon.",
                        color=ft.Colors.GREY,
                    ),
                ],
            )
            page.update()
            return

        cards = []
        for fav in favoritos:
            def gerar_handler(fav_id):
                # Capturamos o id em closure pra cada botão
                def handler(e):
                    db_service.remover_favorito(fav_id)
                    renderizar()
                return handler

            card = ft.Card(
                content=ft.Container(
                    padding=12,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=4,
                        controls=[
                            ft.Image(src=fav["sprite_url"], width=200, height=200),
                            ft.Text(
                                fav["nome"],
                                weight=ft.FontWeight.BOLD,
                                size=14,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                f"#{fav['id']:03d}",
                                color=ft.Colors.GREY,
                                size=12,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color=ft.Colors.RED,
                                tooltip="Remover dos favoritos",
                                on_click=gerar_handler(fav["id"]),
                            ),
                        ],
                    ),
                ),
            )
            cards.append(card)

        container.content = ft.Column(
            expand=True,
            spacing=10,
            controls=[
                ft.Text(
                    f"Meus Favoritos ({len(favoritos)})",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.GridView(
                    expand=True,
                    runs_count=2,
                    spacing=10,
                    run_spacing=10,
                    child_aspect_ratio=0.75,
                    controls=cards,
                ),
            ],
        )
        page.update()

    renderizar()
    return container
