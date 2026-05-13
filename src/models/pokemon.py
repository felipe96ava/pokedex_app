from dataclasses import dataclass

@dataclass
class Pokemon:
    id: int
    nome: str
    sprite_url: str
    tipos: list[str]
    altura_m: float
    peso_kg: float
