import flet as ft

CORES_POR_TIPO = {
    "fire":     ft.Colors.RED_400,
    "water":    ft.Colors.BLUE_400,
    "grass":    ft.Colors.GREEN_400,
    "electric": ft.Colors.YELLOW_700,
    "psychic":  ft.Colors.PURPLE_300,
    "ice":      ft.Colors.CYAN_300,
    "dragon":   ft.Colors.INDIGO_400,
    "dark":     ft.Colors.BLACK87,
    "fairy":    ft.Colors.PINK_200,
    "ground":   ft.Colors.BROWN_400,
    "rock":     ft.Colors.BROWN_700,
    "fighting": ft.Colors.DEEP_ORANGE_400,
    "poison":   ft.Colors.PURPLE_400,
    "bug":      ft.Colors.LIGHT_GREEN_500,
    "ghost":    ft.Colors.DEEP_PURPLE_400,
    "steel":    ft.Colors.BLUE_GREY_400,
    "flying":   ft.Colors.LIGHT_BLUE_300,
    "normal":   ft.Colors.GREY_500,
}

def cor_do_tipo(tipo: str):
    return CORES_POR_TIPO.get(tipo.lower(), ft.Colors.GREY_500)
