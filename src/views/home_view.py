import flet as ft

def tela_inicio():
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        padding=30,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[
                ft.Icon(ft.Icons.CATCHING_POKEMON, size=80, color=ft.Colors.RED),
                ft.Text("PokéDex SENAI", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Use a aba Buscar para encontrar um Pokémon pelo nome ou número, "
                    "e salve seus favoritos.",
                    text_align=ft.TextAlign.CENTER,
                    size=14,
                    color=ft.Colors.GREY,
                ),
            ],
        ),
    )
