import flet as ft

from src.controllers import favoritos_controller, treinador_controller


def tela_perfil():
    total_favoritos = len(favoritos_controller.listar())
    nome_treinador = treinador_controller.obter_nome() or "Treinador SENAI"

    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        padding=30,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            controls=[
                ft.CircleAvatar(
                    content=ft.Icon(ft.Icons.PERSON, size=50),
                    radius=50,
                ),
                ft.Text(nome_treinador, size=22, weight=ft.FontWeight.BOLD),
                ft.Text("aluno@senai.br", color=ft.Colors.GREY),
                ft.Divider(),
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER),
                        ft.Text(f"{total_favoritos} Pokémon favoritados"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        ),
    )
