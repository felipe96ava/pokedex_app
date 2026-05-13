"""Utilitários para controle de teclado virtual no Flet.

NOTA TÉCNICA:
    O Flet ainda não expõe método nativo para dispensar o teclado virtual.
    Issue: https://github.com/flet-dev/flet/issues/4827

    Usamos setattr/getattr direto no objeto `page` porque a API
    de page.session muda entre versões do Flet — atributo Python é estável.
"""
import flet as ft


_ATRIBUTO_SINK = "_pokedex_focus_sink"


def setup_teclado(page: ft.Page):
    """Inicializa o controle de teclado. Chamar uma vez no startup."""
    if getattr(page, _ATRIBUTO_SINK, None) is not None:
        return

    sink = ft.TextField(
        read_only=True,
        width=0,
        height=0,
        border=ft.InputBorder.NONE,
    )
    page.overlay.append(sink)
    setattr(page, _ATRIBUTO_SINK, sink)


def fechar_teclado(page: ft.Page):
    """Fecha o teclado virtual."""
    sink = getattr(page, _ATRIBUTO_SINK, None)
    if sink is not None:
        sink.focus()