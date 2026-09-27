# Proposal

Fatia 22 do **PRD-09 — Área do Mestre (App 09)**, conforme
`openspec/cronograma-de-fatias.md`. Atende `RF-09-122`, declarado no PRD-09 pela fatia 24 do
PRD-02. **Só tela**: nenhuma rota, requisito, entidade, `Operacao` ou migração nova.

## Why

A fatia 24 do PRD-02 criou `GET /v1/responsaveis` no núcleo **já autorizada ao Mestre**, com o
recorte dele implementado e coberto por teste: os responsáveis com vínculo vigente a
Guerreiro(a) das comunidades em que atua, somados aos que ele próprio cadastrou. Faltou a
tela — decisão do fundador de 2026-09-26, que separou a regra da apresentação para não inchar
aquela fatia.

Sem ela, a Área do Mestre tem o mesmo buraco que a gestão tinha: a tela abre direto no
cadastro, e responsável cadastrado fica inalcançável. Pior no Mestre, que cadastra
**presencialmente no encontro** — é justamente quem interrompe o cadastro antes do vínculo, e
é para ele que o ramo por autoria do recorte foi criado. O ramo existe no núcleo e não tem
quem o consuma.

## What Changes

- A área **Responsáveis** da App 09 passa a **abrir na lista** dos responsáveis que o Mestre
  alcança, com o nome e os vinculados por nick e grau de parentesco.
- O cadastro de responsável, que hoje é a primeira coisa da tela, passa a ficar atrás de um
  botão, no padrão que a App 03 já usa.
- A partir de um responsável da lista, o Mestre **retoma** o vínculo e adiciona outro
  Guerreiro(a), sem cadastrar ninguém.
- Responsável sem vínculo aparece sinalizado — é o cadastro interrompido no encontro.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `area-do-mestre`: requisito novo — a App 09 apresenta os responsáveis que o Mestre alcança e
  retoma o vínculo de um deles.

## Impact

- `apps/app-09-mestre/src/responsaveis/api.ts` — o cliente da rota que já existe.
- `apps/app-09-mestre/src/responsaveis/TelaDeResponsaveis.tsx` — passa a abrir na lista.
- `apps/app-09-mestre/src/responsaveis/` — a lista nova.
- `apps/app-09-mestre/src/responsaveis/responsaveis.test.tsx` — cobertura.
- Backend: **nenhum**. A rota, o recorte e a cobertura dele já estão em `main`.
- Documentação MkDocs: **nenhuma**. `RF-09-122` já foi declarado no PRD-09, a decisão já está
  no documento 09 §1 e no documento 02 §1, e o documento 99 §8 já registra o PRD-09 dependendo
  do PRD-02 — tudo pela fatia 24 do PRD-02. Fecha a fatia 22 no
  `openspec/cronograma-de-fatias.md`.

## Fora do escopo

- **Mudar o recorte do Mestre**: ele é do núcleo, está decidido e coberto por teste. A tela
  apresenta o que a rota serve, sem filtrar por conta própria.
- **Sinalizar se o responsável tem credencial criada**: a fatia 24 do PRD-02 deixou de fora, e
  a rota não serve esse dado.
- **Editar, encerrar vínculo ou descadastrar responsável**: sem requisito no PRD-09 e sem rota.
- **Extrair a lista para `comum/`**: as duas aplicações apresentam recortes diferentes da mesma
  rota; a decisão de não compartilhar componente segue a da fatia 21.
