# Identidade pública e comprobatórios

Origem: **PRD-14 — App 08: Área do Apoiador**, §§5.2, 5.9, 6.2, 8, 9 e 11. **Fatia 3** do
PRD-14 no `openspec/cronograma-de-fatias.md`.

Atende `RF-14-12` a `RF-14-20`, `RN-14-10`, `RN-14-11` e `RN-14-12`. Traz também o
`RF-02-101`, requisito novo do PRD-02 — decisão do fundador de 2026-09-01, sem a qual o
`RF-14-19` não fecha.

## Why

O Apoiador cadastrado entra na App 08 e não tem identidade: o nick só se define por uma rota
sem tela, o avatar não tem rota alguma — a coluna existe na `Persona` e nada a grava — e não há
por onde enviar a prova do apoio. Sem isso o card dele não chega à vitrine com o que o
documento 11 §8.2 define, e o piso de 10 moedas do avatar próprio, decidido no PRD-14, não vale
em lugar nenhum.

O `RF-14-19` fecha o ciclo do documento comprobatório em dois atos — o Apoiador envia, o Admin
anexa —, e **o segundo não tinha requisito em PRD algum**: o PRD-02 §6 só previa o artefato
declarado no cadastro (`RF-02-02` a `RF-02-04`). Sem o ato do Admin, o documento enviado ficaria
pendente para sempre.

## What Changes

### O núcleo grava o avatar do Apoiador, com o piso de moedas (PRD-14 §§5.2, 6.2)

- `PUT /v1/eu/apoiador/identidade` passa a aceitar o **avatar** ao lado do nick, como o PRD-01
  §9 já declara (`RF-14-12`, `RF-14-17`).
- O avatar próprio é liberado a partir de **10 moedas acumuladas em aportes homologados**;
  abaixo do piso a gravação é recusada com **409** e quanto falta, como o PRD-14 §9 prevê
  (`RF-14-14`, `RN-14-11`).
- O acumulado **não regride**: o piso se mede pela soma dos aportes homologados do Apoiador, não
  pelo Poder Sustentador, que o ressarcimento derruba (`RN-14-11`).
- Leitura nova `GET /v1/eu/apoiador/identidade` — nick, avatar, moedas acumuladas e quanto falta
  para o piso —, contraparte do `PUT` que já existe, para a tela dizer o que falta sem tentar
  gravar (`RF-14-15`, `RF-14-16`).
- O nick continua sob a unicidade e a conferência restrita a nicks de adulto que a capacidade
  `identidade-do-adulto` já governa (`RF-14-13`, `RN-14-10`).

### O documento comprobatório do Apoiador nasce pendente e só o Admin o publica (PRD-14 §§5.9, 6.2)

- `POST /v1/eu/apoiador/documentos` — o Apoiador declara currículo, portfólio, rede social,
  termo de doação ou comprovante, cada um com **endereço e rótulo**, como o documento 02 §1
  exige de Mestre e Apoiador. Anexo de arquivo segue fora do Ciclo 01 (`RF-14-18`).
- O documento enviado **nasce sem anexação** e não vai à vitrine; só o ato do Admin o publica
  (`RF-14-19`, `RN-14-12`).
- `POST /v1/apoiadores/{id}/artefatos/{artefato_id}/anexacao` — o ato do Admin, no molde do
  `POST /v1/consentimentos/{id}/anexo` que já existe. É o **`RF-02-101`**, requisito novo do
  PRD-02 §6.2 (`RF-14-19`, `RN-14-12`).
- `GET /v1/eu/apoiador/documentos` — o Apoiador lê o que enviou e **o que já está publicado**
  na página dele (`RF-14-20`).

### A App 08 ganha as duas telas (PRD-14 §§5.2, 5.9)

- **Identidade pública**: define ou troca nick e avatar, mostra o card na moldura comum do
  documento 11 §8.2 com o total em moedas e, abaixo do piso, o **avatar padrão do projeto** com
  quanto falta para trocá-lo — sem cobrar nem insistir (`RF-14-12` a `RF-14-17`, `RN-14-11`).
- **Comprobatórios**: envia o documento por endereço e rótulo, declara que ele só vai à página
  pública quando um Admin o anexar, e lista o que já está publicado (`RF-14-18` a `RF-14-20`,
  `RN-14-12`).

### Fora do escopo

- A **auditoria por amostragem** do avatar e do nick e a **despublicação com motivo**
  (`RN-14-10`) são atos da gestão na App 03, sem `RF` no PRD-14; aqui vale só a autoria do
  Apoiador e a unicidade do nick.
- A **fila da App 03** que lista os documentos pendentes e a **tela** que os anexa são da fatia
  16 do PRD-02 — esta fatia entrega o ato no núcleo, não a tela.
- O **card na vitrine** é do PRD-03, ainda não fatiado; a App 08 apresenta a prévia do card,
  não a página pública.
- Tudo o que o PRD-14 §3.2 já exclui: contato com Guerreiro(a), recibo fiscal e cadastro pela
  porta pública.

## Capabilities

### New Capabilities

- `prova-do-apoio`: como o Apoiador declara o comprobatório do próprio apoio, por que ele nasce
  pendente, o ato de Admin que o anexa ao cadastro e o publica, e a leitura que o Apoiador tem
  do que já está publicado.

### Modified Capabilities

- `identidade-do-adulto`: a identidade do Apoiador passa a levar o **avatar**, com o piso de 10
  moedas acumuladas em aportes homologados, o direito que não regride e a leitura de quanto
  falta.
- `area-do-apoiador`: a App 08 ganha a tela de identidade pública — com a prévia do card e o
  avatar padrão abaixo do piso — e a tela de envio de comprobatórios.

## Impact

- `backend/src/nucleo/personas/`: `avatar` no `PUT` da identidade do Apoiador e a leitura
  correspondente, as rotas do documento comprobatório e o ato de anexação; coluna nova de
  anexação em `ArtefatoComprobatorio`, com migração Alembic que preserva publicados os artefatos
  já declarados.
- `backend/src/nucleo/poder_sustentador/regra.py`: a derivação das **moedas acumuladas** do
  provedor, que não regride — vizinha do Poder Sustentador, que regride.
- `apps/app-08-apoiador/`: telas de identidade pública e de comprobatórios.
- `docs/02-conceito-do-jogo-e-gamificacao.md` §1 e `docs/09-topicos-em-aberto-e-sugestoes.md` §1
  (decisão nova), `docs/prds/prd-02-frontend-de-gestao.md` §§6.2, 9 e 15 (`RF-02-101`),
  `docs/prds/prd-14-area-do-apoiador.md` §9 e `docs/prds/prd-01-backend-api.md` §9 (as rotas de
  leitura e de anexação) e `openspec/cronograma-de-fatias.md`.
