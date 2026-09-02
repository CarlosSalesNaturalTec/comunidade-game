## Why

O Apoiador acompanha hoje só o que nasce dele — o desafio que propôs, o aporte que declarou, a
missão que cobriu. O que os Guerreiros, as Guerreiras e os Mestres produzem passa longe da
App 08, e o único jeito de saber que o apoio virou alguma coisa é abrir a vitrine e procurar. A
**fatia 7 do PRD-14** — `openspec/cronograma-de-fatias.md`, bloco do PRD-14 — entrega o
acompanhamento: os mesmos dados do painel público dentro da aplicação e o favorito, que é
leitura e nada mais.

PRD de origem: **PRD-14 — Área do Apoiador (App 08)**.
Recorte da fatia: `RF-14-48` a `RF-14-55`, `RN-14-23` a `RN-14-25`; entidade `Favorito`
(PRD-14 §8).
Depende da leitura pública já entregue pelo núcleo (`leitura-publica-da-vitrine`).

## What Changes

- Nasce a entidade **`Favorito`** — Apoiador, alvo (Guerreiro(a) ou Mestre) e data de inclusão
  (PRD-14 §8) —, com as três rotas do PRD-14 §9: `GET`, `POST` e `DELETE` em
  `/v1/eu/favoritos`, todas restritas ao Apoiador em sessão.
- O favorito de Guerreiro(a) se faz **pelo nick exato** que a família cedeu. A rota não lista,
  não sugere e não completa nick nenhum, e **nick inexistente e nick sem divulgação autorizada
  devolvem o mesmo 404** (`RF-14-49`, `RF-14-50`, `RF-14-51`, `RN-14-23`).
- O favorito de Mestre se faz pela persona dele (`RF-14-52`).
- A leitura do favorito traz as **novidades dos últimos 30 dias**, derivadas — nunca
  armazenadas (PRD-14 §8) — dos fatos que as entidades já datam (`RF-14-53`, `RN-14-25`).
- Favoritar é **leitura**: não abre canal, não avisa a criança, não amplia o que o Apoiador
  enxerga, e o destaque existe só dentro da aplicação — sem e-mail (`RF-14-54`, `RN-14-24`,
  `RN-14-27`). Remover é ato do Apoiador, a qualquer tempo (`RF-14-55`).
- A App 08 ganha a área **Acompanhamento**, com os mesmos dados do painel público, sem recorte
  adicional (`RF-14-48`), e a gestão dos favoritos.

### O quinto fato da novidade fica para o PRD-10

`RF-14-53` e `RN-14-25` definem cinco fatos em destaque: criação original publicada, badge
novo, nível novo, **resultado de batalha** e trilha nova publicada pelo Mestre. Quatro são
deriváveis hoje. O resultado de batalha é do PRD-10, que não tem entidade nenhuma no núcleo e
é o nº 11 na ordem do documento 99 §9 — depois do PRD-14. Decisão do fundador, 2026-09-02:
**os quatro entram agora e o quinto entra com o PRD-10**, anotado na linha da fatia 7 e no
bloco do PRD-10 do cronograma.

### O Mestre é guardado agora, a descoberta vem com o PRD-03

`RF-14-52` favorita o Mestre "a partir da página pública dele", e essa página é
`GET /v1/vitrine/mestres` — rota do PRD-03 §9, adiada pela change
`2026-08-14-leitura-publica-vitrine-e-jogos` e ainda sem fatia. Decisão do fundador,
2026-09-02: a entidade e as rotas **já aceitam alvo Mestre**, e a tela lista os que foram
favoritados; o caminho de chegar até ele — a página pública — vem com o PRD-03. Esta change
**não** antecipa rota de outro PRD.

## Fora do escopo

O que o PRD-14 §3.2 já exclui, e que esta fatia toca de perto: qualquer canal de mensagem,
telefone ou e-mail de Guerreiro(a), família ou Mestre; qualquer dado de criança além de avatar
e nick de quem tem divulgação autorizada; notificação por e-mail (`RN-14-27`).

Ficam de fora por não serem desta fatia: a rota pública de Mestres e o restante do painel
público da App 06 (PRD-03); o resultado de batalha (PRD-10); e as propostas, avisos e o canal
fechado (`RF-14-56` a `RF-14-59`, fatia 8).

## Capabilities

### New Capabilities

- `favorito-do-apoiador`: o que o favorito é e o que ele nunca é — o alvo, a busca por nick
  exato com recusa indistinta, a novidade derivada dos últimos 30 dias, a remoção e as
  salvaguardas que impedem o favorito de virar canal (`RF-14-49` a `RF-14-55`, `RN-14-23` a
  `RN-14-25`).

### Modified Capabilities

- `area-do-apoiador`: a App 08 ganha a área de acompanhamento — os mesmos dados do painel
  público, sem recorte adicional, e a gestão dos favoritos com as salvaguardas de exibição
  (`RF-14-48` a `RF-14-55`).

## Impact

- **Backend** (`backend/src/nucleo/`): módulo novo `favoritos/` com modelo, regra e rotas, e a
  migração Alembic aditiva da tabela. Lê `vitrine.publico`,
  `consentimentos.regra.condicao_de_autorizacao_vigente`, `pontuacao.modelo` (`Nivel`,
  `Badge`), `criacoes_originais.modelo` e `trilhas.modelo` — nenhum deles é alterado.
- **App 08** (`apps/app-08-apoiador/`): área e telas novas, com o cliente das rotas públicas de
  vitrine e das rotas de favorito.
- **API**: três rotas novas sob `/v1`; nenhum contrato existente muda.
- **Documentação**: a linha da fatia 7 no `openspec/cronograma-de-fatias.md` e a anotação do
  quinto fato no bloco do PRD-10. Nenhuma decisão de produto nova, logo nada muda em `docs/`.
