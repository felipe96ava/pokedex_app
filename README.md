# PokéDex SENAI

App didático em Flet que consome a [PokéAPI](https://pokeapi.co) e salva
favoritos em banco SQLite local. Foi pensado como **projeto de 3-4 aulas**
para a turma de Dispositivos Móveis.

## Estrutura

```
pokedex_app/
├── main.py                          # Entrypoint
├── requirements.txt
├── README.md
└── src/
    ├── config/
    │   ├── settings.py              # URL da API, caminho do banco
    │   └── routes.py                # Mapeamento de rotas
    ├── components/
    │   ├── nav_bar.py               # NavigationBar
    │   └── pokemon_card.py          # Card visual reutilizável
    ├── controllers/
    │   ├── pokemon_controller.py    # Regras: validar busca
    │   └── favoritos_controller.py  # Regras: favoritar/listar
    ├── models/
    │   └── pokemon.py               # dataclass Pokemon
    ├── services/
    │   ├── pokeapi_service.py       # HTTP / consumo da API
    │   └── db_service.py            # SQL / acesso ao SQLite
    ├── utils/
    │   └── formatters.py            # Cores por tipo
    └── views/
        ├── home_view.py
        ├── buscar_view.py
        ├── favoritos_view.py
        ├── perfil_view.py
        └── config_view.py
```

## Como rodar

```bash
pip install -r requirements.txt
python main.py
```

---

## Plano de Aulas (3-4 aulas)

### 🧱 Aula 1 — Estrutura ampliada + consumo de API

**Objetivos:** apresentar as novas pastas (`models`, `services`, `utils`) e
fazer a primeira requisição HTTP funcionar.

1. Revisitar a estrutura do projeto anterior (NavigationBar + rotas).
2. Apresentar o conceito de **camadas**: a UI não fala direto com a API.
3. Implementar:
   - `src/models/pokemon.py` — explicar `@dataclass`.
   - `src/config/settings.py` — falar sobre evitar valores "mágicos".
   - `src/services/pokeapi_service.py` — apresentar `httpx` e `async/await`.
4. Testar o service no terminal antes de plugar na UI:
   ```python
   import asyncio
   from src.services.pokeapi_service import buscar_pokemon
   print(asyncio.run(buscar_pokemon("pikachu")))
   ```

**Exercício em sala:** modificar o service pra também retornar a lista de
habilidades (`abilities`) do Pokémon.

---

### 🔌 Aula 2 — Plugar a busca na UI + componente reutilizável

**Objetivos:** ligar a API à interface e introduzir componentes próprios.

1. Implementar `src/utils/formatters.py` (cor por tipo).
2. Implementar `src/components/pokemon_card.py` — explicar por que componentes
   visuais ficam separados das views.
3. Implementar `src/controllers/pokemon_controller.py` — papel do controller
   como "mediador" entre view e service.
4. Atualizar `src/views/buscar_view.py` — campo de texto, botão, exibição do
   card, tratamento de erro ("não encontrado", "campo vazio").

**Exercício em sala:** adicionar um indicador de loading (`ft.ProgressRing`)
enquanto a API está sendo consultada.

---

### 💾 Aula 3 — Banco de dados SQLite

**Objetivos:** introduzir persistência local.

1. Implementar `src/services/db_service.py`:
   - `inicializar_banco()` — `CREATE TABLE IF NOT EXISTS`.
   - `adicionar_favorito` / `remover_favorito` / `listar_favoritos` / `eh_favorito`.
2. Chamar `inicializar_banco()` no `main.py`.
3. Implementar `src/controllers/favoritos_controller.py` com `alternar_favorito`.
4. Conectar o botão de coração no `pokemon_card.py` ao controller.
5. Implementar `src/views/favoritos_view.py` — listar do banco.

**Exercício em sala:** adicionar uma coluna `data_favoritado` (TIMESTAMP) na
tabela e mostrar quando o Pokémon foi salvo.

---

### 🎨 Aula 4 — Polimento + apresentação (opcional)

**Objetivos:** UX e revisão geral.

1. Tela de Perfil com contador de favoritos.
2. Tela de Configurações com alternância de tema (`ft.Switch` + `page.theme_mode`).
3. Tratamento de erros: o que mostrar quando o usuário está offline?
4. Apresentação dos projetos.

**Desafios pra puxar:**
- Adicionar paginação na busca (offset + limit).
- Permitir nota pessoal de cada favorito (ALTER TABLE).
- Exportar favoritos pra um JSON.

---

## Conceitos cobertos pelo projeto

| Conceito | Onde aparece |
|---|---|
| Estrutura modular | Todas as pastas |
| `@dataclass` | `models/pokemon.py` |
| Consumo de API REST | `services/pokeapi_service.py` |
| `async`/`await` com `httpx` | `services/pokeapi_service.py` |
| SQLite + DDL/DML | `services/db_service.py` |
| Tratamento de exceções | `pokeapi_service.py` (HTTPError, Timeout) |
| Componentes reutilizáveis | `components/pokemon_card.py` |
| Separação UI ↔ regra ↔ dados | controllers ↔ services |
| Closures em handlers | `favoritos_view.py` (`gerar_handler`) |
| Estado e re-renderização | `page.go(page.route)` |

## Convenções (mantém o padrão da turma)

- Flet 0.28+, `ft.run(main)`, sem `page.update()` manual.
- Sem `lambda` em handlers — sempre funções nomeadas.
- Imports absolutos (`from src.services...`), nunca relativos.
