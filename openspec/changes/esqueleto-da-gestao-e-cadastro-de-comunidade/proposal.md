## Why

O PRD-02 (App 03 — frontend de gestão) é a entrega nº 4 do documento 99 §9 e está liberado
desde a nº 1. É a primeira aplicação a existir: o PRD-02 §2 declara que nenhuma outra abre sem
ela, porque é onde o Admin cria a Comunidade Virtual e agenda a aula que habilita o App 01.

Esta é a primeira fatia de código fora de `backend/`. Ela abre a pasta da aplicação com a
esteira de CI dela, materializa os tokens que o documento 15 §12 manda nascer junto da
primeira pasta de aplicação, e entrega **um cadastro de ponta a ponta** — o de Comunidade
Virtual (`RF-02-11`), o menor recorte completo do PRD-02 e a raiz de todo vínculo da
plataforma (documento 03, princípio 10).

Origem: **PRD-02**, com `RF-02-11`. Atende também, do lado da entrada, `RF-01-09`, `RF-01-10`
e `RN-01-34` do PRD-01, e consome `RF-08-30` do PRD-08.

## What Changes

- **App 03 nasce** em `apps/app-03-gestao/`, com a esteira de CI da pasta — `biome
  format --check`, `biome check` e `vitest run` bloqueando o merge, disparada só pelo caminho
  dela.
- **`comum/` nasce** na raiz com o arquivo de tokens em CSS, nas camadas semântica e de tema
  do documento 15 §12, no temperamento Operação (documento 15 §6).
- **Entrada do adulto na App 03**: login social do Google, com a recusa de quem não tem
  cadastro orientando à vitrine (`RF-01-09`, `RF-01-10`).
- **Cadastro de Comunidade Virtual de ponta a ponta** (`RF-02-11`): a lista, o formulário de
  nome, localização e granularidade máxima, a criação e as recusas.
- **Recusa por papel visível na tela**: quem não é Admin lê a recusa em vez de um erro cru
  (`RN-08-01`).
- **BREAKING**: o núcleo passa a responder a **qualquer origem**, sem cookie credenciado
  (documento 03, princípio 2). Sem isso nenhum navegador alcança a API a partir de um
  frontend em endereço próprio. É mudança de comportamento do backend, não do contrato de
  dados: nenhuma rota, corpo ou código de resposta muda.
- **`openspec/config.yaml` deixa de contradizer o documento 03**: o contexto entregue aos
  agentes ainda diz que as ferramentas de frontend seguem pendentes e que não há pasta de
  topo além das cinco da árvore antiga.

## Capabilities

### New Capabilities

- `aplicacao-de-gestao`: a App 03 — como o adulto entra nela, como a sessão e o papel
  governam o que ele alcança, e o cadastro de Comunidade Virtual de ponta a ponta.

### Modified Capabilities

- `convencoes-da-api`: o contrato ganha de que origem a chamada é aceita. Hoje a capacidade
  define onde a rota vive, a forma do erro, a paginação, o fuso e onde o contrato é publicado
  — e silencia sobre origem, o que só não doeu enquanto nenhum navegador chamou de fora.

## Impact

**Pastas novas**, cada uma com a esteira que o `CLAUDE.md` exige:

- `apps/app-03-gestao/` — React com TypeScript sobre Vite (documento 03 §1)
- `comum/` — tokens compartilhados pelas oito aplicações (documento 03 §1.2)
- `.github/workflows/` — o workflow das pastas de JavaScript

**Backend**: `backend/src/nucleo/principal.py` ganha o middleware de origem. Nenhuma rota
muda.

**Rotas consumidas**, todas já implementadas e testadas: `POST /v1/sessoes/social`,
`GET /v1/eu`, `DELETE /v1/sessoes/atual`, `GET /v1/comunidades` e `POST /v1/comunidades`.

**Fora da esteira de código**: a implantação precisa de um _client ID_ do OAuth do Google —
o mesmo que o núcleo já confere em `google_client_id` — e da chave de aplicação da App 03,
por ambiente (documento 03, princípio 2).

**Fora do escopo**, como o PRD-02 §3.2 já exclui: autoria de trilha, missão e quiz, que é da
App 09; lançamento das atividades do próprio Mestre; telas de coleta do Guerreiro(a) e
conversa de onboarding. Fora do escopo **desta fatia**, sem exclusão nova: os demais cadastros
do PRD-02 §6.1, as filas de avaliação, o painel do dia, o Quiz ao Vivo e a publicação da
aplicação em endereço próprio.
