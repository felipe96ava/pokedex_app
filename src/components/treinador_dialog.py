import flet as ft

from src.controllers import treinador_controller

def abrir_dialog_treinador(
    page: ft.Page,
    primeira_vez: bool = False,
    ao_salvar=None,
):
    nome_atual = treinador_controller.obter_nome() or ""

    campo_nome = ft.TextField(
        label="Nome do Treinador",
        hint_text="Ex: Ash, Misty, Brock...",
        value=nome_atual,
        autofocus=True,
        max_length=30,
    )

    def salvar(e):
        if not treinador_controller.salvar_nome(campo_nome.value):
            campo_nome.error_text = "Digite um nome válido."
            page.update()
            return

        page.pop_dialog()
        page.show_dialog(
            ft.SnackBar(content=ft.Text("Nome do treinador salvo!"))
        )
        if ao_salvar:
            ao_salvar()

    def cancelar(e):
        page.pop_dialog()

    acoes = [ft.TextButton("Salvar", on_click=salvar)]
    if not primeira_vez:
        acoes.insert(0, ft.TextButton("Cancelar", on_click=cancelar))

    titulo = "Bem-vindo, Treinador!" if primeira_vez else "Alterar nome do treinador"
    subtitulo = (
        "Antes de começar, como podemos te chamar?"
        if primeira_vez
        else "Escolha um novo nome de treinador."
    )

    dialog = ft.AlertDialog(
        modal=primeira_vez,
        title=ft.Text(titulo),
        content=ft.Column(
            tight=True,
            controls=[
                ft.Text(subtitulo, color=ft.Colors.GREY),
                campo_nome,
            ],
        ),
        actions=acoes,
    )

    page.show_dialog(dialog)
