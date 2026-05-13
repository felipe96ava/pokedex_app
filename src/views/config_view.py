import flet as ft

from src.components.treinador_dialog import abrir_dialog_treinador
from src.controllers import treinador_controller


def tela_config(page: ft.Page):
    tema_escuro = page.theme_mode == ft.ThemeMode.DARK

    def alternar_tema(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        )
        page.update()

    nome_atual_texto = ft.Text(
        treinador_controller.obter_nome() or "(não definido)",
        color=ft.Colors.GREY,
    )

    def ao_alterar_nome(e):
        def atualizar_label():
            nome_atual_texto.value = treinador_controller.obter_nome() or "(não definido)"
            page.update()

        abrir_dialog_treinador(page, primeira_vez=False, ao_salvar=atualizar_label)

    return ft.Container(
        expand=True,
        padding=30,
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Configurações", size=24, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.DARK_MODE),
                        ft.Text("Tema escuro"),
                        ft.Switch(value=tema_escuro, on_change=alternar_tema),
                    ],
                ),
                ft.Divider(),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.PERSON),
                                ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text("Nome do treinador"),
                                        nome_atual_texto,
                                    ],
                                ),
                            ],
                        ),
                        ft.TextButton(
                            "Alterar",
                            icon=ft.Icons.EDIT,
                            on_click=ao_alterar_nome,
                        ),
                    ],
                ),
                ft.Divider(),
                ft.Text("PokéDex SENAI · v1.0", color=ft.Colors.GREY, size=12),
            ],
        ),
    )
