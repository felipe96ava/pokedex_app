"""Tela de Busca.

Fluxo: usuário digita nome/número → clica Buscar → controller chama o
service da API → exibimos o card ou mensagem de erro.
"""
import flet as ft

from src.components.pokemon_card import pokemon_card
from src.controllers import pokemon_controller, favoritos_controller
from src.utils.keyboard import fechar_teclado


def tela_buscar(page: ft.Page):
    campo_busca = ft.TextField(
        label="Nome ou número do Pokémon",
        hint_text="Ex: pikachu, charizard, 25",
        width=320,
        autofocus=True,
    )

    area_resultado = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    def aviso(mensagem: str, cor=ft.Colors.GREY):
        area_resultado.controls = [
            ft.Icon(ft.Icons.INFO_OUTLINE, size=40, color=cor),
            ft.Text(mensagem, color=cor),
        ]

    def ao_favoritar(pokemon):
        agora_favorito = favoritos_controller.alternar_favorito(pokemon)
        msg = "Adicionado aos favoritos!" if agora_favorito else "Removido dos favoritos."
        page.show_dialog(ft.SnackBar(content=ft.Text(msg)))
        # Reconstrói o card pra atualizar o ícone do coração
        area_resultado.controls = [
            pokemon_card(
                pokemon,
                eh_favorito=agora_favorito,
                on_favoritar=ao_favoritar,
            )
        ]
        page.update()

    async def ao_clicar_buscar(e):
        fechar_teclado(page)

        termo = campo_busca.value or ""
        if not termo.strip():
            aviso("Digite algo para buscar.", cor=ft.Colors.ORANGE)
            return

        aviso("Buscando...", cor=ft.Colors.BLUE)

        pokemon = await pokemon_controller.buscar(termo)

        if pokemon is None:
            aviso(f'Pokémon "{termo}" não encontrado.', cor=ft.Colors.RED)
            return

        area_resultado.controls = [
            pokemon_card(
                pokemon,
                eh_favorito=favoritos_controller.eh_favorito(pokemon.id),
                on_favoritar=ao_favoritar,
            )
        ]

    botao_buscar = ft.ElevatedButton(
        "Buscar Pokemon",
        icon=ft.Icons.SEARCH,
        on_click=ao_clicar_buscar,
    )

    # Enter no teclado também dispara a busca
    campo_busca.on_submit = ao_clicar_buscar

    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Text("Buscar Pokémon", size=42, weight=ft.FontWeight.BOLD),
                ft.Column(
                    controls=[campo_busca, botao_buscar],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                area_resultado,
            ],
        ),
    )