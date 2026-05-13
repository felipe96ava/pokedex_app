"""Componente visual reutilizável: cartão de Pokémon.

Recebe um Pokemon e devolve um Card pronto pra ser usado em qualquer view.
Aceita callbacks opcionais pro botão de favoritar.
"""
import flet as ft

from src.models.pokemon import Pokemon
from src.utils.formatters import cor_do_tipo


def pokemon_card(
    pokemon: Pokemon,
    eh_favorito: bool = False,
    on_favoritar=None,
):
    icone = ft.Icons.FAVORITE if eh_favorito else ft.Icons.FAVORITE_BORDER

    def click_favoritar(e):
        if on_favoritar:
            on_favoritar(pokemon)

    badges_tipos = [
        ft.Container(
            content=ft.Text(tipo.upper(), color=ft.Colors.WHITE, size=11, weight=ft.FontWeight.BOLD),
            bgcolor=cor_do_tipo(tipo),
            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
            border_radius=12,
        )
        for tipo in pokemon.tipos
    ]

    return ft.Card(
        elevation=4,
        content=ft.Container(
            width=260,
            padding=20,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(f"#{pokemon.id:03d}", color=ft.Colors.GREY),
                            ft.IconButton(
                                icon=icone,
                                icon_color=ft.Colors.RED,
                                on_click=click_favoritar,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Image(src=pokemon.sprite_url, width=140, height=140),
                    ft.Text(pokemon.nome, size=20, weight=ft.FontWeight.BOLD),
                    ft.Row(controls=badges_tipos, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(
                        controls=[
                            ft.Text(f"Altura: {pokemon.altura_m:.1f} m"),
                            ft.Text(f"Peso: {pokemon.peso_kg:.1f} kg"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                ],
            ),
        ),
    )
