# App 03 — Frontend de gestão

Aplicação de gestão do Comunidade Game (PRD-02): entrada do adulto por login social e o
cadastro de Comunidade Virtual. React com TypeScript sobre Vite (documento 03 §1).

## Comandos

- `npm run dev` — ambiente de desenvolvimento
- `npm run build` — build de produção (saída estática)
- `npm run test` — suíte Vitest
- `npm run format` / `npm run check` — Biome, na esteira de `.github/workflows/`

## Variáveis de ambiente

- `VITE_CHAVE_DE_APLICACAO` — chave desta aplicação, por ambiente (documento 03 §1, princípio
  2). **Pública por construção**: assada no _bundle_ estático no momento do build, qualquer
  visitante a lê no JavaScript servido. Coerente com o princípio 2 — a chave identifica a
  aplicação e sustenta a cota de leitura; quem protege a pessoa é a credencial da persona, que
  nunca sai do `sessionStorage`. Em produção, vem do segredo do repositório
  `APP03_CHAVE_DE_APLICACAO`, semeado pelo `python -m nucleo.cli` do backend.
- `VITE_GOOGLE_CLIENT_ID` — _client ID_ do OAuth do Google, o mesmo que o núcleo confere em
  `google_client_id`.
- `VITE_URL_DO_NUCLEO` — endereço do Backend API. Em produção, `https://api.comunidadegame.org`.

## Implantação

Publicada pelo `.github/workflows/app-03-deploy.yml` em `gestao.comunidadegame.org`, via
Firebase Hosting — alvo `app-03` de `firebase.json`. Provisionamento e ordem da primeira
execução em `backend/README.md`.

## Conferência à mão de acessibilidade (2026-08-20)

**Regra da conferência.** Ela roda sobre build com `VITE_GOOGLE_CLIENT_ID` vazio. Sem client
ID a tela de entrada não carrega o provedor externo de identidade, e navegador automatizado
acionando endpoint de identidade é a forma exata do que sistemas antiabuso classificam como
bot. Contraste, alvo de toque, foco e desenho da fonte se medem igual sem o botão do Google.

O que o Vitest não prova — contraste, alvo de toque em pixel e o desenho das duas famílias —,
conferido uma vez nas três telas, na largura de um celular (390 px), claro e escuro (design —
Decisions). Resultado:

| O que foi medido                                       | Piso do documento 15 §5 | Medido                                                    |
| -------------------------------------------------------- | ------------------------ | ---------------------------------------------------------- |
| Contraste do título e do corpo sobre o fundo             | 4,5:1                    | 16,88:1 (título), 10,72:1 claro / 8,62:1 escuro (corpo)     |
| Contraste do `Aviso` de erro sobre o fundo                | 4,5:1                    | 5,43:1 claro / 6,87:1 escuro                                |
| Contraste do rótulo do `Botao` primário sobre o fundo     | 4,5:1                    | 7,51:1 claro / 5,96:1 escuro                                |
| Alvo de toque dos três botões (`Sair`, `Criar`, `Cancelar`) | 48 px                   | 48,0 px de altura, nos três                                 |
| Contorno de foco do `Botao`, alcançado por Tab            | 2 px, `marca-500`/`marca-400` | 2 px sólido, `#f25c05` no claro e `#ff7a2e` no escuro — exato |
| Família do título e do corpo                              | Archivo / Atkinson Hyperlegible Next | Aplicadas nas três telas, sem substituição pela família de reserva |

Conferido com Chromium (o mesmo motor do ambiente), viewport 390×1400, nas três telas —
entrada, comunidades com erro de carregamento e formulário com erro de campo —, em claro e
escuro. Nenhum ponto abaixo do piso.
