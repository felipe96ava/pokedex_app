import flet as ft

_ATRIBUTO_SINK = "_pokedex_focus_sink"


def setup_teclado(page: ft.Page):
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
    sink = getattr(page, _ATRIBUTO_SINK, None)
    if sink is not None:
        sink.focus()