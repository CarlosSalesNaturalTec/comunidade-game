# Proposal

## Why

É a **fatia 13 do PRD-05** (`openspec/cronograma-de-fatias.md`), e ela atende identificadores
**novos** — `RF-05-91` a `RF-05-93`, `RN-05-51`, `RN-05-52` e `RF-04-76` —, criados na revisão
do PRD-05 e do PRD-04 que entra nesta change, aplicando a decisão do fundador de 2026-11-03
(documento 09 §1, documentos 02 §4 e 11 §2.2).

O desafio prático se cumpre hoje por **declaração nua**: `POST /v1/eu/missoes/{id}/desbloqueio`
manda `respostas: null` e nada mais chega ao núcleo. A fatia 26 fez o Mestre autor declarar a
forma de comprovação aceita, o critério de aceite e o título curto (`RF-09-129` a `RF-09-131`),
e **nenhuma tela os apresenta à criança** nem recebe o que eles pedem: o Guerreiro(a) não sabe o
que entregar e o Mestre não tem o que julgar. Sem esta fatia, a bancada do julgamento
(fatia 27 do PRD-09) segue sem produção à vista e a linha do portfólio (fatia 12 do PRD-03)
segue sem item — as duas dependem dela.

## What Changes

- **O Guerreiro(a) entrega a comprovação na forma que o Mestre autor aceitou**, no mesmo ato em
  que declara que cumpriu: o corpo da submissão passa a carregar a comprovação, e a mídia entra
  por sessão de envio retomável, como a criação original já faz. (`RF-05-91`)
- **A tela do desafio prático apresenta o critério de aceite** junto do enunciado, e **avisa a
  criança** de que aquela mídia fica guardada e pode ir à vitrine — é requisito, não texto de
  enfeite, e é o que dá sentido ao critério. (`RF-05-92`)
- **A comprovação passa a ser exigida para declarar que cumpriu**, com a alternativa de
  **entregar ao Mestre no encontro**: escolhida, a declaração é gravada **sem mídia** e marcada
  como entrega presencial, e NEVER SHALL fazer perder a missão. Estende ao desbloqueio a
  alternativa que o PRD-05 §11 e o `RF-05-78` já garantem a quem recusa foto ou áudio — decisão
  do fundador de 2026-11-04. (`RN-05-51`)
- **Entrega nova antes do julgamento substitui a anterior**, em vez de criar segundo registro;
  julgado que não passou, a linha do desbloqueio é apagada e a comprovação vai com ela, como
  `RN-05-20` já determina. (`RN-05-52`)
- **O Guerreiro(a) reencontra a comprovação que entregou**, e o Mestre autor a alcança: nasce a
  rota de leitura dos bytes, no molde de `GET /v1/criacoes/{id}/arquivo`. Quem grava entrega
  também quem lê — decisão do fundador de 2026-11-04, pela lição do defeito _write-only_ que a
  fatia do núcleo acabou de corrigir na criação original. (`RF-05-93`)
- **A App 01 entrega a comprovação na mesma tela**, pelo componente comum que as duas
  aplicações já consomem — `comum/trilha/DesafioDeDesbloqueio.tsx`, com `submissaoLigada` hoje
  verdadeiro nas duas. (`RF-04-76`)
- Migração Alembic: colunas de comprovação em `desbloqueio_da_missao`, anuláveis.
- Revisão do **PRD-05** (§§6.2, 7, 8, 9, 11 e 15) e do **PRD-04** (§§6, 15) com os
  identificadores novos.

**Fora do escopo** — é fatia das outras, e está nomeado para não ser suposto: os **dois
vereditos**, o motivo em linguagem simples e os **5 pontos regulares** (fatia 27 do PRD-09); a
**linha do portfólio** com nick e título e a abertura da mídia em público (fatia 12 do PRD-03);
a **declaração** dos três campos pelo Mestre, que a fatia 26 já entregou. Segue valendo o que o
PRD-05 §3.2 já exclui, em especial o **acervo do Guerreiro(a)** (`RF-05-47` a `RF-05-49`), que é
Ciclo 02.

## Capabilities

### New Capabilities

Nenhuma. A fatia amplia capacidades existentes.

### Modified Capabilities

- `desbloqueio-da-missao`: a submissão do desafio prático deixa de ser declaração nua e passa a
  carregar a comprovação na forma aceita, com a exigência dela, a alternativa de entrega
  presencial, a substituição antes do julgamento e a leitura dos bytes.
- `area-do-guerreiro`: a tela do desafio prático na App 05 passa a apresentar o critério de
  aceite, a avisar da mídia guardada e a receber a comprovação, com o envio retomável.
- `aplicacao-da-aula-presencial`: a mesma tela na App 01, pelo componente comum.

## Impact

- **Núcleo**: `trilhas/` — `modelo.py` (colunas de comprovação em `DesbloqueioDaMissao`),
  `regra.py` (`submeter_desafio_de_desbloqueio`, abrir/confirmar/ler o envio),
  `rotas.py` (entrada da submissão e as três rotas do arquivo).
- **Contratos**: `POST /v1/eu/missoes/{id}/desbloqueio` passa a exigir a comprovação no prático
  — **BREAKING** para quem submete prático com o corpo de hoje, e os dois clientes são as Apps
  01 e 05, que entram na mesma change. Nascem `POST` e `PATCH` de
  `/v1/eu/missoes/{id}/desbloqueio/comprovacao`, que são do Guerreiro(a), e
  `GET /v1/missoes/{id}/desbloqueios/{id_do_guerreiro}/comprovacao`, que serve também o Mestre
  autor e por isso não cabe em `/eu/`.
- **Dados**: migração Alembic, colunas anuláveis em `desbloqueio_da_missao`. **Sem _backfill_**:
  o desbloqueio prático gravado antes desta change segue valendo sem comprovação, como a
  fatia 26 fixou para os três campos do Mestre.
- **Aplicações**: `comum/trilha` e as **Apps 05 e 01 juntas**, pelo precedente das fatias 10,
  11 e 12 do PRD-05. A App 09 não muda — a bancada é a fatia 27.
- **PRD-05 e PRD-04**: identificadores novos a partir de `RF-05-91`, `RN-05-51` e `RF-04-76`,
  livres hoje. A §14 do PRD-05 não tem pendência que trave esta fatia.
- **LGPD**: a comprovação é mídia de criança que pode ir a público. A tabela do PRD-05 §11 ganha
  a linha dela, com a finalidade, a base legal e a retenção; a divulgação pública segue
  dependendo da adesão em duas etapas, que a fatia 12 do PRD-03 consome. O aviso do `RF-05-92` é
  o "aviso visível" que o §11 já exige de toda tela que coleta dado.
- **Documentação**: a decisão já está nos documentos 02 §4, 11 §§2.2, 5 e 8.2, 99 §6 e 09 §1 —
  esta change não a reescreve. Revisa o **PRD-05** e o **PRD-04** e fecha a linha 13 do bloco do
  PRD-05 no cronograma. O doc 99 §8 não muda: o PRD-05 já depende do PRD-01 e do PRD-09.
