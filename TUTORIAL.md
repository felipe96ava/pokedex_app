# Tutorial: Construindo a PokéDex SENAI do zero

Guia passo a passo para construir um app **Flet** que consome a [PokéAPI](https://pokeapi.co), salva favoritos em **SQLite** local, tem onboarding com nome de treinador e gera um **APK Android** instalável.

> Este tutorial complementa o `README.md` (que tem o plano de aulas resumido). Aqui o foco é a **construção** em si, em etapas incrementais — cada etapa entrega algo que já roda.

## Sumário

- [Parte 0 — Antes de começar](#parte-0--antes-de-começar)
- [Parte 1 — Setup do ambiente](#parte-1--setup-do-ambiente-etapas-12)
- [Parte 2 — Arquitetura em camadas](#parte-2--arquitetura-em-camadas-etapas-35)
- [Parte 3 — Consumindo a PokéAPI](#parte-3--consumindo-a-pokéapi-etapas-68)
- [Parte 4 — Primeira UI navegável](#parte-4--primeira-ui-navegável-etapas-911)
- [Parte 5 — Tela de busca funcional](#parte-5--tela-de-busca-funcional-etapas-1213)
- [Parte 6 — Persistência local com SQLite](#parte-6--persistência-local-com-sqlite-etapas-1416)
- [Parte 7 — Tela de favoritos responsiva](#parte-7--tela-de-favoritos-responsiva-etapa-17)
- [Parte 8 — Onboarding e personalização](#parte-8--onboarding-e-personalização-etapas-1819)
- [Parte 9 — Polimento de UX](#parte-9--polimento-de-ux-etapa-20)
- [Parte 10 — Gerando o APK Android](#parte-10--gerando-o-apk-android-etapas-2122)
- [Parte 11 — Conceitos, desafios e erros comuns](#parte-11--conceitos-desafios-e-erros-comuns)

---

## Parte 0 — Antes de começar

### O que você vai construir

Um app Android (e também desktop) que permite:

- Buscar Pokémon por nome ou número usando a PokéAPI pública.
- Ver detalhes (sprite, tipos coloridos, altura, peso).
- Favoritar Pokémon — fica salvo no celular mesmo sem internet.
- Lista de favoritos em grid 2 colunas com scroll infinito.
- Tela de Perfil com o nome do treinador e contador de favoritos.
- Configurações com tema escuro e alteração do nome do treinador.
- **Primeiro acesso**: pergunta o nome do treinador num diálogo modal.

### Conceitos que você vai aprender

| Conceito | Onde aparece |
|---|---|
| Framework Flet (UI em Python) | Tudo |
| Arquitetura em camadas (views → controllers → services) | Estrutura de pastas |
| `@dataclass` | `models/pokemon.py` |
| Requisições HTTP assíncronas com `httpx` | `services/pokeapi_service.py` |
| `async`/`await` | services e views |
| SQLite com `sqlite3` (módulo padrão do Python) | `services/db_service.py` |
| Componentes reutilizáveis | `components/pokemon_card.py` |
| Sistema de rotas | `config/routes.py` |
| `NavigationBar` mobile | `components/nav_bar.py` |
| `GridView` responsivo | `views/favoritos_view.py` |
| Diálogos modais e SnackBar | `components/treinador_dialog.py` |
| Build mobile (APK) com `flet build` | Parte 10 |

### Pré-requisitos

- **Python 3.10 ou superior** (recomendado 3.11 ou 3.12 — o 3.14 também funciona, mas tem aquele detalhe de encoding que veremos)
- **Editor de código** — VSCode, PyCharm, Cursor, ou similar
- **Conexão de internet** — pra baixar dependências e consumir a API
- **Sistema operacional** — Windows, macOS ou Linux funcionam pra desenvolvimento. Pra **build do APK Android**, ainda funciona em qualquer um — só precisa de Flutter + Android SDK (veremos na Parte 10).

### Tempo estimado

- Setup do ambiente: 30 min
- Construção do app: 6-10 horas (3-4 aulas)
- Build do APK na primeira vez: 15-25 min (próximas: 3-5 min)

---

## Parte 1 — Setup do ambiente (Etapas 1-2)

### Etapa 1 — Criar o projeto e o ambiente virtual

Abra o terminal (PowerShell no Windows, Terminal no Mac/Linux) e crie a pasta:

```powershell
mkdir pokedex_app
cd pokedex_app
```

Crie e ative o **ambiente virtual** (`venv`):

```powershell
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

> **Por que `venv`?** Pra isolar as dependências do projeto do Python global do sistema. Cada projeto tem suas próprias bibliotecas em versões próprias — sem `venv`, instalar uma versão diferente do Flet num projeto quebra os outros.

Quando estiver ativado, você verá `(.venv)` no início da linha do terminal.

### Etapa 2 — Instalar Flet e fazer o primeiro "Hello PokéDex"

Crie o arquivo `requirements.txt`:

```text
flet>=0.28.0
httpx>=0.27.0
```

Instale:

```powershell
pip install -r requirements.txt
```

Crie o `main.py` com um "olá mundo" do Flet:

```python
import flet as ft


def main(page: ft.Page):
    page.title = "PokéDex SENAI"
    page.add(ft.Text("Olá, PokéDex!", size=24, weight=ft.FontWeight.BOLD))


ft.run(main)
```

Rode:

```powershell
python main.py
```

Vai abrir uma janela com o texto. Se chegou aqui, ambiente OK.

> **Atenção (Windows)**: se aparecer erro de execução de scripts no PowerShell ao ativar o venv, rode uma vez como administrador:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

---

## Parte 2 — Arquitetura em camadas (Etapas 3-5)

### Etapa 3 — Criar a estrutura de pastas

Crie a árvore vazia (sem conteúdo ainda, só os arquivos `.py` vazios):

```
pokedex_app/
├── main.py
├── requirements.txt
└── src/
    ├── __init__.py
    ├── config/
    │   ├── __init__.py
    │   ├── settings.py
    │   └── routes.py
    ├── components/
    │   ├── __init__.py
    │   ├── nav_bar.py
    │   ├── pokemon_card.py
    │   └── treinador_dialog.py
    ├── controllers/
    │   ├── __init__.py
    │   ├── pokemon_controller.py
    │   ├── favoritos_controller.py
    │   └── treinador_controller.py
    ├── models/
    │   ├── __init__.py
    │   └── pokemon.py
    ├── services/
    │   ├── __init__.py
    │   ├── pokeapi_service.py
    │   └── db_service.py
    ├── utils/
    │   ├── __init__.py
    │   ├── formatters.py
    │   └── keyboard.py
    └── views/
        ├── __init__.py
        ├── home_view.py
        ├── buscar_view.py
        ├── favoritos_view.py
        ├── perfil_view.py
        └── config_view.py
```

> **Por que tantas pastas?** Cada pasta tem **uma responsabilidade**. Quando o projeto cresce, você sabe exatamente onde mexer:
> - `models/` — só estruturas de dados (formato de um Pokémon, p.ex.)
> - `services/` — quem **fala com o mundo externo** (API HTTP, banco de dados)
> - `controllers/` — **regras de negócio** (validações, decisão de favoritar/desfavoritar)
> - `views/` — telas (a parte que o usuário vê)
> - `components/` — **pedaços de UI reutilizáveis** entre várias views
> - `config/` — configurações centralizadas (URLs, caminhos, rotas)
> - `utils/` — funções utilitárias sem regra de negócio (cores, formatadores)
>
> Quando uma view precisa de dados, ela chama um controller. O controller chama um service. Nada de view falando direto com SQL ou HTTP. Isso se chama **arquitetura em camadas**.

Os arquivos `__init__.py` ficam vazios — só servem pra o Python tratar a pasta como um pacote.

### Etapa 4 — `config/settings.py`

```python
"""Configurações centralizadas do app."""

POKEAPI_URL = "https://pokeapi.co/api/v2"
DB_PATH = "pokedex.db"
TIMEOUT_API = 10.0
```

> **Por que assim?** Toda vez que você usa uma URL ou caminho diretamente no meio do código, ele vira um "valor mágico". Centralizando aqui, se um dia a PokéAPI mudar a URL, você muda só num lugar. O mesmo vale pro caminho do banco, timeouts, etc.

### Etapa 5 — `models/pokemon.py`

```python
"""Model que representa um Pokémon no app."""
from dataclasses import dataclass


@dataclass
class Pokemon:
    id: int
    nome: str
    sprite_url: str
    tipos: list[str]
    altura_m: float
    peso_kg: float
```

> **Por que `@dataclass`?** Sem ele, você teria que escrever `__init__`, `__repr__`, `__eq__` e outros métodos à mão. Com `@dataclass`, o Python gera tudo automaticamente a partir das anotações de tipo. Resultado: classe limpa, focada em **estrutura**, não em mecânica.

Pra testar, abra o terminal Python (`python` no terminal com venv ativo):

```python
>>> from src.models.pokemon import Pokemon
>>> p = Pokemon(id=25, nome="Pikachu", sprite_url="...", tipos=["electric"], altura_m=0.4, peso_kg=6.0)
>>> print(p)
Pokemon(id=25, nome='Pikachu', sprite_url='...', tipos=['electric'], altura_m=0.4, peso_kg=6.0)
```

---

## Parte 3 — Consumindo a PokéAPI (Etapas 6-8)

### Etapa 6 — `services/pokeapi_service.py`

Esse é quem fala HTTP com a PokéAPI. **Não tem nada de UI aqui** — só recebe um nome/número e devolve um `Pokemon` ou `None`.

```python
"""Camada de comunicação com a PokéAPI."""
import httpx

from src.config.config import POKEAPI_URL, TIMEOUT_API
from src.models.pokemon import Pokemon


async def buscar_pokemon(nome_ou_id: str):
    """Busca um Pokémon pelo nome ou número. Retorna None se não achar."""

    url = f"{POKEAPI_URL}/pokemon/{nome_ou_id.lower().strip()}"

    async with httpx.AsyncClient() as client:
        try:
            resposta = await client.get(url, timeout=TIMEOUT_API)
            resposta.raise_for_status()
            dados = resposta.json()
        except (httpx.HTTPError, httpx.TimeoutException):
            return None

    sprite = dados["sprites"]["front_default"]
    if not sprite:
        sprite = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"

    return Pokemon(
        id=dados["id"],
        nome=dados["name"].capitalize(),
        sprite_url=sprite,
        tipos=[t["type"]["name"] for t in dados["types"]],
        altura_m=dados["height"] / 10,
        peso_kg=dados["weight"] / 10,
    )
```

> **Por que `async`?** Requisições HTTP são lentas (esperam a rede). Se você fizesse sincronamente, a tela do app **congelaria** durante a espera. Com `async/await`, o Python pode fazer outras coisas enquanto espera a resposta.

> **Por que retornar `None`?** É um padrão simples pra dizer "não deu certo". A view (UI) recebe o `None` e decide o que mostrar pro usuário. Se você lançar exceção, a UI precisa de `try/except` em todo lugar — fica pior.

Antes de plugar na UI, **teste no terminal**. Crie um `teste_api.py` na raiz (depois pode apagar):

```python
import asyncio
from src.services.pokeapi_service import buscar_pokemon


async def teste():
    p = await buscar_pokemon("pikachu")
    print(p)


asyncio.run(teste())
```

Rode `python teste_api.py`. Deve imprimir os dados do Pikachu.

### Etapa 7 — `utils/formatters.py`

Mapeamento de tipo de Pokémon para uma cor. Como é só transformação, mora em `utils/`.

```python
"""Mapeia tipo de Pokémon para uma cor."""
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
```

### Etapa 8 — `controllers/pokemon_controller.py`

```python
"""Controller que orquestra a busca de Pokémon."""
from src.models.pokemon import Pokemon
from src.services import pokeapi_service


async def buscar(termo: str):
    if not termo or not termo.strip():
        return None
    return await pokeapi_service.buscar_pokemon(termo)
```

> **Por que um controller só pra isso?** Hoje ele só valida o termo. Amanhã ele pode: cachear resultados, normalizar abreviações ("char" → "charmander"), logar buscas, etc. **A view não vai precisar mudar** — só o controller. Isso é o ganho de separar camadas.

---

## Parte 4 — Primeira UI navegável (Etapas 9-11)

Nesta parte montamos o esqueleto navegável: 5 abas no rodapé, troca de telas, mas as telas são quase vazias por enquanto.

### Etapa 9 — `components/nav_bar.py`

```python
import flet as ft

from src.config.routes import ROTAS


def criar_nav_bar(page: ft.Page):
    """Monta a NavigationBar do app e liga o evento de troca de aba."""

    async def ao_mudar_aba(e):
        indice = e.control.selected_index
        await page.push_route(ROTAS[indice])

    return ft.NavigationBar(
        selected_index=0,
        on_change=ao_mudar_aba,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Início",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SEARCH,
                label="Buscar",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.STAR,
                label="Favoritos",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON_OUTLINED,
                selected_icon=ft.Icons.PERSON,
                label="Perfil",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Config",
            ),
        ],
    )
```

### Etapa 10 — Views "vazias"

Crie cada view inicialmente bem simples, só pra ter algo que renderiza.

`src/views/home_view.py`:

```python
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
```

`src/views/buscar_view.py` (placeholder, só com título):

```python
import flet as ft


def tela_buscar(page: ft.Page):
    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Text("Buscar Pokémon", size=24, weight=ft.FontWeight.BOLD),
    )
```

`src/views/favoritos_view.py`:

```python
import flet as ft


def tela_favoritos(page: ft.Page):
    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Text("Favoritos", size=24, weight=ft.FontWeight.BOLD),
    )
```

`src/views/perfil_view.py`:

```python
import flet as ft


def tela_perfil():
    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Text("Perfil", size=24, weight=ft.FontWeight.BOLD),
    )
```

`src/views/config_view.py`:

```python
import flet as ft


def tela_config(page: ft.Page):
    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Text("Configurações", size=24, weight=ft.FontWeight.BOLD),
    )
```

### Etapa 11 — Sistema de rotas + `main.py`

`src/config/routes.py`:

```python
import flet as ft

from src.views.home_view import tela_inicio
from src.views.buscar_view import tela_buscar
from src.views.favoritos_view import tela_favoritos
from src.views.perfil_view import tela_perfil
from src.views.config_view import tela_config


ROTAS = ["/", "/buscar", "/favoritos", "/perfil", "/config"]


def resolver_rota(page: ft.Page, nav_bar: ft.NavigationBar):
    """Decide qual tela renderizar com base em page.route."""

    if page.route in ROTAS:
        nav_bar.selected_index = ROTAS.index(page.route)

    if page.route == "/":
        conteudo = tela_inicio()
    elif page.route == "/buscar":
        conteudo = tela_buscar(page)
    elif page.route == "/favoritos":
        conteudo = tela_favoritos(page)
    elif page.route == "/perfil":
        conteudo = tela_perfil()
    elif page.route == "/config":
        conteudo = tela_config(page)
    else:
        conteudo = ft.Text("Página não encontrada")

    page.views.clear()
    page.views.append(
        ft.View(
            route=page.route,
            controls=[conteudo],
            navigation_bar=nav_bar,
        )
    )
```

Substitua o `main.py` (que estava com "Hello PokéDex") pelo esqueleto navegável:

```python
import flet as ft

from src.config.routes import resolver_rota
from src.components.nav_bar import criar_nav_bar


def main(page: ft.Page):
    page.title = "PokéDex SENAI"
    page.theme_mode = ft.ThemeMode.LIGHT

    nav_bar = criar_nav_bar(page)

    def ao_mudar_rota(e):
        resolver_rota(page, nav_bar)

    page.on_route_change = ao_mudar_rota
    ao_mudar_rota(None)


ft.run(main)
```

Rode `python main.py`. Você deve conseguir trocar entre as 5 abas. Cada tela mostra só o título por enquanto.

> **Por que `page.views.clear()` e `append`?** O Flet trabalha com uma pilha de `View`. Cada vez que a rota muda, apagamos tudo e empilhamos a view nova. Como sempre tem **uma** view ativa, simplifica muito.

---

## Parte 5 — Tela de busca funcional (Etapas 12-13)

### Etapa 12 — `components/pokemon_card.py`

Componente visual reutilizável: recebe um `Pokemon` e devolve um `Card` pronto.

```python
"""Componente visual reutilizável: cartão de Pokémon."""
import flet as ft

from src.models.pokemon import Pokemon
from src.utils.cores import cor_do_tipo


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
```

> **Por que componente separado?** O `pokemon_card` vai aparecer em DUAS telas (Buscar e Favoritos). Se você colar o código direto na view, duplica trabalho. Sempre que algo aparece em mais de um lugar, **vira componente**.

### Etapa 13 — Completar `views/buscar_view.py`

Agora a tela completa: campo de texto, botão, exibição do card, mensagens de aviso, fluxo `async`.

```python
"""Tela de Busca."""
import flet as ft

from src.components.pokemon_card import pokemon_card
from src.controllers import pokemon_controller


def tela_buscar(page: ft.Page):
    campo_busca = ft.TextField(
        label="Nome ou número do Pokémon",
        hint_text="Ex: pikachu, charizard, 25",
        width=250,
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

    async def ao_clicar_buscar(e):
        termo = campo_busca.value or ""
        if not termo.strip():
            aviso("Digite algo para buscar.", cor=ft.Colors.ORANGE)
            return

        aviso("Buscando...", cor=ft.Colors.BLUE)

        pokemon = await pokemon_controller.buscar(termo)

        if pokemon is None:
            aviso(f'Pokémon "{termo}" não encontrado.', cor=ft.Colors.RED)
            return

        area_resultado.controls = [pokemon_card(pokemon)]

    botao_buscar = ft.ElevatedButton(
        "Buscar",
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
                ft.Text("Buscar Pokémon", size=24, weight=ft.FontWeight.BOLD),
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
```

> **Atenção — alignment vs horizontal_alignment em Column**:
> - `alignment` controla o **eixo principal** (vertical em Column): onde os filhos ficam entre o topo e a base.
> - `horizontal_alignment` controla o **eixo cruzado** (horizontal em Column): se os filhos vão pra esquerda, centro ou direita.
> Em `Row` é o inverso (alignment = horizontal, vertical_alignment = vertical).

Rode `python main.py`, vá pra aba Buscar, digite "pikachu", clique. Deve aparecer o card. Sem internet ou termo inválido, mostra a mensagem de aviso.

---

## Parte 6 — Persistência local com SQLite (Etapas 14-16)

### Etapa 14 — `services/db_service.py`

```python
"""Camada de acesso ao banco SQLite."""
import sqlite3

from src.config.config import DB_PATH


def _conexao():
    """Abre uma conexão nova com o banco."""
    return sqlite3.connect(DB_PATH)


def inicializar_banco():
    """Cria as tabelas caso ainda não existam. Roda no startup."""
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS favoritos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            sprite_url TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def adicionar_favorito(pokemon_id: int, nome: str, sprite_url: str):
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO favoritos (id, nome, sprite_url) VALUES (?, ?, ?)",
        (pokemon_id, nome, sprite_url),
    )
    conn.commit()
    conn.close()


def remover_favorito(pokemon_id: int):
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favoritos WHERE id = ?", (pokemon_id,))
    conn.commit()
    conn.close()


def listar_favoritos():
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, sprite_url FROM favoritos ORDER BY nome")
    linhas = cursor.fetchall()
    conn.close()
    return [
        {"id": linha[0], "nome": linha[1], "sprite_url": linha[2]}
        for linha in linhas
    ]


def eh_favorito(pokemon_id: int):
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM favoritos WHERE id = ?", (pokemon_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None
```

> **Por que parâmetros com `?` no SQL?** É proteção contra **SQL Injection**. Nunca concatene strings do usuário direto no SQL (`f"... WHERE id = {pokemon_id}"`). O `sqlite3` escapa os valores corretamente quando você passa pelos `?`.

Chame `inicializar_banco()` no `main.py`, logo no início:

```python
import flet as ft

from src.config.routes import resolver_rota
from src.components.nav_bar import criar_nav_bar
from src.services.db_service import inicializar_banco


def main(page: ft.Page):
    page.title = "PokéDex SENAI"
    page.theme_mode = ft.ThemeMode.LIGHT

    inicializar_banco()

    nav_bar = criar_nav_bar(page)

    def ao_mudar_rota(e):
        resolver_rota(page, nav_bar)

    page.on_route_change = ao_mudar_rota
    ao_mudar_rota(None)


ft.run(main)
```

### Etapa 15 — `controllers/favoritos_controller.py`

```python
"""Controller que aplica as regras de negócio dos favoritos."""
from src.models.pokemon import Pokemon
from src.services import db_service


def alternar_favorito(pokemon: Pokemon):
    """Adiciona ou remove. Retorna True se ficou favoritado, False se foi removido."""
    if db_service.eh_favorito(pokemon.id):
        db_service.remover_favorito(pokemon.id)
        return False

    db_service.adicionar_favorito(pokemon.id, pokemon.nome, pokemon.sprite_url)
    return True


def listar():
    return db_service.listar_favoritos()


def eh_favorito(pokemon_id: int):
    return db_service.eh_favorito(pokemon_id)
```

### Etapa 16 — Ligar o coração na busca

Volte em `views/buscar_view.py` e adicione o callback de favoritar:

```python
"""Tela de Busca."""
import flet as ft

from src.components.pokemon_card import pokemon_card
from src.controllers import pokemon_controller, favoritos_controller


def tela_buscar(page: ft.Page):
    campo_busca = ft.TextField(
        label="Nome ou número do Pokémon",
        hint_text="Ex: pikachu, charizard, 25",
        width=250,
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
        "Buscar",
        icon=ft.Icons.SEARCH,
        on_click=ao_clicar_buscar,
    )

    campo_busca.on_submit = ao_clicar_buscar

    return ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Text("Buscar Pokémon", size=24, weight=ft.FontWeight.BOLD),
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
```

> **Atenção — o ícone não atualiza sozinho.** O `pokemon_card` é construído **uma vez**: o ícone do coração é decidido na hora de criar o card. Pra atualizar o ícone depois de favoritar, precisamos **reconstruir o card** com `eh_favorito` novo. Por isso o `ao_favoritar` chama `pokemon_card(...)` novamente e substitui em `area_resultado.controls`.

> **Por que não `page.go(page.route)` pra rerenderizar?** O Flet só dispara `on_route_change` quando a rota **muda de fato**. Se você chama `page.go(page.route)` (mesma rota), nada acontece. Reconstruir manualmente o controle é o caminho.

> **Sobre `page.show_dialog(SnackBar(...))`**: nas versões mais novas do Flet (>= 1.x previstas), o método será `page.open(...)`. Em Flet 0.85.x, `SnackBar` herda de `DialogControl`, então o mesmo `show_dialog` que mostra `AlertDialog` mostra `SnackBar` também. Se sua versão for mais nova e der `AttributeError: 'Page' object has no attribute 'open'`, troque pra `show_dialog`. Se der erro em `show_dialog`, troque pra `open`.

Teste: busque um Pokémon, clique no coração, o ícone deve mudar e o snackbar aparece.

---

## Parte 7 — Tela de favoritos responsiva (Etapa 17)

### Etapa 17 — `views/favoritos_view.py` com GridView

A tela precisa:
- Listar favoritos em **2 colunas** lado a lado (mobile-friendly).
- Ter **scroll infinito** (se o usuário tiver 100 favoritos, rola tranquilo).
- Atualizar a lista **na hora** quando remover um — sem trocar de aba.

```python
"""Tela de Favoritos."""
import flet as ft

from src.controllers import favoritos_controller
from src.services import db_service


def tela_favoritos(page: ft.Page):
    container = ft.Container(expand=True, padding=20)

    def renderizar():
        favoritos = favoritos_controller.listar()

        if not favoritos:
            container.content = ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.STAR_BORDER, size=60, color=ft.Colors.GREY),
                    ft.Text("Você ainda não tem favoritos.", size=18),
                    ft.Text(
                        "Vá em Buscar e marque o coração de um Pokémon.",
                        color=ft.Colors.GREY,
                    ),
                ],
            )
            page.update()
            return

        cards = []
        for fav in favoritos:
            def gerar_handler(fav_id):
                def handler(e):
                    db_service.remover_favorito(fav_id)
                    renderizar()
                return handler

            card = ft.Card(
                content=ft.Container(
                    padding=12,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=4,
                        controls=[
                            ft.Image(src=fav["sprite_url"], width=90, height=90),
                            ft.Text(
                                fav["nome"],
                                weight=ft.FontWeight.BOLD,
                                size=14,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                f"#{fav['id']:03d}",
                                color=ft.Colors.GREY,
                                size=12,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color=ft.Colors.RED,
                                tooltip="Remover dos favoritos",
                                on_click=gerar_handler(fav["id"]),
                            ),
                        ],
                    ),
                ),
            )
            cards.append(card)

        container.content = ft.Column(
            expand=True,
            spacing=10,
            controls=[
                ft.Text(
                    f"Meus Favoritos ({len(favoritos)})",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.GridView(
                    expand=True,
                    runs_count=2,
                    spacing=10,
                    run_spacing=10,
                    child_aspect_ratio=0.75,
                    controls=cards,
                ),
            ],
        )
        page.update()

    renderizar()
    return container
```

> **Por que `GridView` e não `Row(wrap=True)`?**
> - `GridView` garante **2 colunas** exatas (`runs_count=2`) independente do tamanho da tela.
> - Já tem **scroll infinito nativo** e renderiza só o que está visível (`build_controls_on_demand=True` por padrão).
> - `Row(wrap=True)` depende da largura disponível e não scrolla.

> **Por que `gerar_handler(fav_id)` com closure?** Se você fizer `on_click=lambda e: remover(fav["id"])` num laço, o `fav` é capturado por **referência** e na hora do clique todos os botões apontam pro último `fav` do loop. A "fábrica de handlers" `gerar_handler` cria um escopo novo pra cada `fav_id`, fixando o valor.

> **Por que `renderizar()` em vez de `page.go(page.route)`?** Já vimos: navegar pra mesma rota não rerenderiza. O padrão "função renderizar interna + chamada explícita" é mais previsível.

---

## Parte 8 — Onboarding e personalização (Etapas 18-19)

### Etapa 18 — Tabela `treinador` + controller

Adicione no `db_service.py` (junto com o que já existe):

```python
def inicializar_banco():
    """Cria as tabelas caso ainda não existam. Roda no startup."""
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS favoritos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            sprite_url TEXT NOT NULL
        )
        """
    )
    # Tabela de treinador: guardamos sempre uma única linha (id=1) com o nome.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS treinador (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def salvar_nome_treinador(nome: str):
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO treinador (id, nome) VALUES (1, ?)",
        (nome,),
    )
    conn.commit()
    conn.close()


def obter_nome_treinador():
    conn = _conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM treinador WHERE id = 1")
    linha = cursor.fetchone()
    conn.close()
    return linha[0] if linha else None
```

> **Por que `INSERT OR REPLACE` na linha id=1?** Como só existe **um** treinador no app, sempre gravamos na mesma linha. Simples e direto, sem precisar de "primeira inserção" vs "atualização" separadas.

Crie `controllers/treinador_controller.py`:

```python
"""Controller do treinador."""
from src.services import db_service


def obter_nome():
    return db_service.obter_nome_treinador()


def salvar_nome(nome: str):
    nome_limpo = (nome or "").strip()
    if not nome_limpo:
        return False
    db_service.salvar_nome_treinador(nome_limpo)
    return True


def tem_nome_definido():
    return obter_nome() is not None
```

### Etapa 19 — Diálogo reutilizável e integração

`src/components/treinador_dialog.py`:

```python
"""Diálogo reutilizável pra pedir/editar o nome do treinador."""
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
```

> **Por que `modal=True` só no primeiro acesso?** Pra **forçar** o usuário a digitar o nome. Diálogo modal não fecha clicando fora — só pelo botão Salvar. Depois (na edição via Configurações), modal é chato, então deixamos `modal=False`.

Atualize `main.py` pra abrir o diálogo no primeiro acesso:

```python
import flet as ft

from src.config.routes import resolver_rota
from src.components.nav_bar import criar_nav_bar
from src.components.treinador_dialog import abrir_dialog_treinador
from src.controllers import treinador_controller
from src.services.db_service import inicializar_banco


def main(page: ft.Page):
    page.title = "PokéDex SENAI"
    page.theme_mode = ft.ThemeMode.LIGHT

    inicializar_banco()

    nav_bar = criar_nav_bar(page)

    def ao_mudar_rota(e):
        resolver_rota(page, nav_bar)

    page.on_route_change = ao_mudar_rota
    ao_mudar_rota(None)

    if not treinador_controller.tem_nome_definido():
        abrir_dialog_treinador(page, primeira_vez=True)


ft.run(main)
```

Atualize `views/perfil_view.py` pra mostrar o nome real:

```python
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
```

---

## Parte 9 — Polimento de UX (Etapa 20)

### Etapa 20 — Configurações com tema escuro + alterar nome + teclado virtual

`views/config_view.py`:

```python
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
```

### Teclado virtual (mobile)

No celular, depois de buscar um Pokémon, o teclado virtual fica aberto cobrindo o resultado. Vamos fechar.

Crie `src/utils/keyboard.py`:

```python
"""Utilitários para controle de teclado virtual no Flet.

NOTA: O Flet ainda não expõe método nativo para dispensar o teclado virtual.
Truque: criar um TextField invisível e dar focus nele, o teclado fecha.
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
```

Chame `setup_teclado(page)` no `main.py`:

```python
import flet as ft

from src.config.routes import resolver_rota
from src.components.nav_bar import criar_nav_bar
from src.components.treinador_dialog import abrir_dialog_treinador
from src.controllers import treinador_controller
from src.services.db_service import inicializar_banco
from src.utils.keyboard import setup_teclado


def main(page: ft.Page):
    page.title = "PokéDex SENAI"
    page.theme_mode = ft.ThemeMode.LIGHT

    inicializar_banco()
    setup_teclado(page)

    nav_bar = criar_nav_bar(page)

    def ao_mudar_rota(e):
        resolver_rota(page, nav_bar)

    page.on_route_change = ao_mudar_rota
    ao_mudar_rota(None)

    if not treinador_controller.tem_nome_definido():
        abrir_dialog_treinador(page, primeira_vez=True)


ft.run(main)
```

E use no início do handler de busca, em `buscar_view.py`:

```python
from src.utils.keyboard import fechar_teclado

# ...

async def ao_clicar_buscar(e):
    fechar_teclado(page)
    # resto do código
```

Pronto. O app está completo do ponto de vista funcional. Agora bora gerar APK.

---

## Parte 10 — Gerando o APK Android (Etapas 21-22)

### Etapa 21 — Pré-requisitos do build

O `flet build apk` é uma camada sobre o **Flutter** que empacota seu app Python num APK Android. Pré-requisitos:

1. **Flutter SDK** — [instalar](https://docs.flutter.dev/get-started/install)
2. **Android SDK** — vem com o Android Studio (ou via `cmdline-tools`)
3. **JDK** — geralmente vem com o Android Studio. Pode usar OpenJDK 17.

Verifique tudo de uma vez:

```powershell
flutter doctor
```

Você quer ver, no mínimo:

```
[√] Flutter (Channel stable, ...)
[√] Android toolchain - develop for Android devices (Android SDK ...)
```

> **No Windows há um pré-requisito extra: Modo de Desenvolvedor**. O Flutter usa **symlinks** pra organizar plugins Android e isso exige permissão. Ative em **Configurações → Sistema → Para desenvolvedores** ou rode:
> ```powershell
> start ms-settings:developers
> ```
> Sem isso, o build falha com "Building with plugins requires symlink support".

### Etapa 22 — `pyproject.toml` e comando de build

O `flet build` usa `pyproject.toml` pra ler metadados do app. Crie na raiz:

```toml
[project]
name = "pokedex_app"
version = "1.0.0"
description = "PokéDex SENAI - app de busca e favoritos de Pokémon"
authors = [{ name = "SENAI" }]
requires-python = ">=3.10"
dependencies = [
    "flet>=0.28.0",
    "httpx>=0.27.0",
]

[tool.flet]
# Identidade do pacote no Android (precisa ser único e em letras minúsculas)
org = "br.senai"
product = "PokeDex SENAI"
company = "SENAI"
copyright = "Copyright (c) 2026 SENAI"

[tool.flet.app]
path = "."
exclude = [
    ".venv",
    ".idea",
    "__pycache__",
    "pokedex.db",
    "build",
    "*.pyc",
]
```

> **Por que `exclude`?** O `flet build` empacota a pasta inteira por padrão. Sem excluir, ele jogaria a `.venv` (centenas de MB) e seu `pokedex.db` local (com seus dados de teste) dentro do APK. Vai inflar o tamanho e bagunçar a primeira execução no celular.

Rode o build:

```powershell
# No Windows, force UTF-8 antes pra evitar problema de encoding:
$env:PYTHONIOENCODING="utf-8"
$env:PYTHONUTF8="1"

.venv\Scripts\flet build apk --yes --skip-flutter-doctor --no-rich-output
```

**Flags explicadas:**

- `apk` — alvo da build. Outros: `aab` (Google Play), `web`, `windows`, `macos`, `ipa`.
- `--yes` — confirma automaticamente todos os "Y/N" do processo.
- `--skip-flutter-doctor` — pula a verificação se você já rodou antes.
- `--no-rich-output` — **desliga emojis e formatação rica** no log. **Importante no Windows** com Python 3.13/3.14 — sem isso, dá `UnicodeEncodeError: 'charmap' codec can't encode character '\u2705'`.

> **Atenção — primeiro build é demorado**: 10–25 min porque baixa JDK, Android SDK, Gradle, plugins Flutter, etc. Próximos builds são bem mais rápidos (2–5 min) porque tudo fica em cache.

Quando terminar, o APK fica em:

```
build/apk/pokedex_app.apk      ← ~60-70 MB
build/apk/pokedex_app.apk.sha1
```

### Como instalar no celular

**Opção 1 — Cabo USB (mais profissional):**

1. No celular, ative **Opções do desenvolvedor**: toque 7x em *Configurações → Sobre → Número da versão*.
2. Habilite **Depuração USB**.
3. Conecte e rode:
   ```powershell
   adb install build\apk\pokedex_app.apk
   ```

**Opção 2 — Copiar e abrir:**

1. Mande o `.apk` pro celular (USB, Drive, e-mail, etc).
2. No celular, abra o arquivo. O Android pede pra liberar "instalar apps desconhecidos" pra quem está abrindo (Files, navegador). Confirme.
3. Instale.

### Otimização: APKs menores por arquitetura

Se quiser, dá pra gerar **três APKs separados**, cada um pra uma arquitetura de processador (ARM, ARM64, x86). Cada um pesa ~25-30 MB em vez de 70:

```powershell
.venv\Scripts\flet build apk --yes --skip-flutter-doctor --no-rich-output --split-per-abi
```

Pra distribuir em escala, prefira esse formato. Pra trabalho/teste, o APK único é mais simples.

### E pra iOS?

O Flet também tem `flet build ipa`, mas iOS exige **Mac com Xcode**. Sem Mac, suas alternativas são:

1. **GitHub Actions com runner `macos-latest`** — gratuito pra repos públicos, builda na nuvem da Microsoft.
2. **Mac na nuvem** (MacInCloud, MacStadium) — paga, mas pode usar por uma semana.
3. **Codemagic / Bitrise** — CI/CD especializado em mobile.

Pra distribuir oficialmente na App Store, ainda precisa de **Apple Developer Account paga** ($99/ano).

---

## Parte 11 — Conceitos, desafios e erros comuns

### Conceitos cobertos

| Conceito | Onde aparece | Etapa |
|---|---|---|
| Estrutura modular em camadas | Toda a árvore `src/` | 3 |
| `@dataclass` | `models/pokemon.py` | 5 |
| Consumo de API REST | `services/pokeapi_service.py` | 6 |
| `async`/`await` com `httpx` | services e views | 6, 13 |
| Tratamento de exceções HTTP | `services/pokeapi_service.py` | 6 |
| SQLite + DDL/DML + bind params | `services/db_service.py` | 14, 18 |
| Componentes reutilizáveis | `components/pokemon_card.py` | 12 |
| Separação UI → controller → service | controllers vs services | 8, 15, 18 |
| Closures em handlers de loop | `favoritos_view.py` (`gerar_handler`) | 17 |
| Reconstrução manual de controles | `buscar_view.py` e `favoritos_view.py` | 16, 17 |
| GridView responsivo | `favoritos_view.py` | 17 |
| Diálogos modais e SnackBar | `treinador_dialog.py` | 19 |
| Tema dinâmico | `config_view.py` | 20 |
| Build mobile (APK) | Parte 10 | 22 |

### Desafios pra puxar (ordem crescente de dificuldade)

1. **Loading visual**: enquanto a API responde, mostre `ft.ProgressRing`.
2. **Habilidades do Pokémon**: adicione `abilities: list[str]` no model e mostre no card.
3. **Data do favorito**: `ALTER TABLE favoritos ADD COLUMN data_favoritado TIMESTAMP` e mostre "favoritado há X dias".
4. **Filtro nos favoritos**: campo de busca pra filtrar a lista por nome.
5. **Detalhes ao tocar no card**: abrir uma tela nova com mais informações (estatísticas, movimentos, evolução).
6. **Compartilhar Pokémon**: botão "Compartilhar" que abre o intent do Android.
7. **Modo offline pra busca**: cachear resultados em uma terceira tabela.
8. **Exportar favoritos pra JSON**.

### Erros comuns e como resolver

| Erro | Causa | Solução |
|---|---|---|
| `ModuleNotFoundError: No module named 'src'` | Rodou `python src/main.py` em vez de `python main.py` na raiz | Sempre rodar da raiz, com venv ativo |
| `UnicodeEncodeError: 'charmap' codec can't encode character '\u2705'` | Console Windows em cp1252 não imprime emojis do Flet CLI | Use `--no-rich-output` + `$env:PYTHONUTF8="1"` |
| `AttributeError: 'Page' object has no attribute 'open'` | Versão do Flet (0.85.x) ainda não tem `page.open()` | Use `page.show_dialog(SnackBar(...))` — em 0.85.x, `SnackBar` herda de `DialogControl` |
| Coração não muda depois de clicar | `pokemon_card` foi construído uma vez só, o estado fica congelado | Reconstrua o card com `eh_favorito` novo e chame `page.update()` |
| `page.go(page.route)` "não faz nada" | Flet só dispara `on_route_change` quando a rota muda de fato | Refatore pra usar uma função `renderizar()` interna que repopula `container.content` e chama `page.update()` |
| `RuntimeWarning: coroutine 'FormFieldControl.focus' was never awaited` | Em versões novas do Flet, `focus()` é `async` | Use `await sink.focus()` e marque o handler como `async` |
| `Building with plugins requires symlink support` no `flet build apk` | Modo de Desenvolvedor do Windows desligado | Ative em Configurações → Para desenvolvedores |
| APK gigante (70+ MB) | Padrão é build "fat" com todas as arquiteturas | Use `--split-per-abi` |
| `ElevatedButton is deprecated` (warning) | Mudança de API no Flet 0.80+ | Use `ft.Button` no lugar de `ft.ElevatedButton` |
| Campo da Column "colado na esquerda" | `Column` não tem `horizontal_alignment` setado | Adicione `horizontal_alignment=ft.CrossAxisAlignment.CENTER` |

### Para fechar

Você construiu um app completo que cobre **toda a pirâmide de uma aplicação mobile real**:

- UI declarativa com componentes reutilizáveis.
- Comunicação com API externa (assíncrona, com tratamento de falhas).
- Persistência local (SQLite, queries parametrizadas).
- Onboarding e personalização.
- Build de produção para celular.

A arquitetura em camadas que usamos aqui escala. Se um dia você trocar SQLite por Firebase, só o `db_service.py` muda. Se trocar PokéAPI por outra, só o `pokeapi_service.py`. **As views e os controllers não precisam saber.**

Bom código.
