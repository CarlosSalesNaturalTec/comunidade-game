## Why

Fatia **8 do PRD-05** (`openspec/cronograma-de-fatias.md`), a última do PRD-05 no Ciclo 01.
Atende `RF-05-20` e `RF-05-21`.

A trava anotada na fatia — a entidade `DesafioExtra` — caiu: ela nasceu na fatia 1 do PRD-14, o
Mestre já valida (fatia 15 do PRD-09) e o Admin já aprova, publica e encerra (fatia 15 do
PRD-02). O desafio extra hoje percorre o caminho inteiro **até publicar e não chega a ninguém**:
quem propõe vê o que propôs, o Mestre vê o que tem a validar, o Admin vê o que tem a aprovar — e
o Guerreiro(a), para quem o desafio existe, não vê nada. Esta fatia fecha a ponta.

## What Changes

- **O Guerreiro(a) lê os desafios extras vigentes que lhe são elegíveis** (`RF-05-20`):
  publicados, com a vigência correndo hoje, das trilhas em que ele está **inscrito**, e nas duas
  modalidades — o **aberto**, que alcança todos os inscritos na trilha, e o **direcionado**,
  que alcança só o dono do nick que o proponente digitou. O direcionado a nick que não está
  inscrito naquela trilha não aparece (decisão do fundador de 2026-09-02).
- **Cada desafio extra exibe a recompensa oferecida, a quantidade disponível e o período de
  vigência** (`RF-05-21`), junto do critério de atribuição, dos pontos extras que vale, do
  formato e da trilha (e da missão, quando houver) a que se prende.
- **O esgotado continua na lista, marcado** (decisão do fundador de 2026-09-02): desafio
  publicado, dentro da vigência, cuja quantidade restante chegou a zero segue visível dizendo
  que as recompensas acabaram — a §5.2 do PRD-05 não admite que o que já não dá para fazer
  desapareça sem motivo.
- **BREAKING** — `GET /v1/eu/desafios` passa a devolver **um objeto com dois conjuntos**,
  `semanais` e `extras`, no lugar da lista de atividades. É o contrato que a §9 do PRD-05
  declara para essa rota ("Desafios semanais **e extras** vigentes e elegíveis"); a fatia 6
  entregou só a primeira metade. O único consumidor é a App 05, atualizada nesta mesma change.
- **A App 05 mostra os desafios extras na aba Desafios**, abaixo dos semanais e apartados
  deles, em linguagem da criança. Leitura apenas: nenhuma ação de concluir, disputar ou trocar
  nasce daqui.
- **Nenhuma leitura identifica pessoa**: o Guerreiro(a) recebe o que o desafio oferece e nada
  do proponente além do que a proposta declara, e nunca o nick do destinatário de um
  direcionado alheio (`RN-05-21`, `RN-14-20`). Pontos extras seguem computados isoladamente,
  sem alimentar nível (`RN-05-18`).

**Fora do escopo**, como o PRD-05 §3.2 e o cronograma já excluem: **concluir** o desafio extra e
**receber** a recompensa — o ato de registrar a conclusão é do PRD-09, em fatia ainda sem
número; o **acervo do Guerreiro(a)**, o **canal de sugestões** e o **apoio escolar por
assistente de voz**, todos do Ciclo 02.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `area-do-guerreiro`: `GET /v1/eu/desafios` passa a servir também os desafios extras vigentes
  e elegíveis, com a elegibilidade das duas modalidades; a App 05 ganha a exibição deles com
  recompensa, quantidade e vigência.
- `desafio-extra`: a leitura do desafio publicado alcança o Guerreiro(a) elegível — quem vê,
  o que a resposta traz e o que ela nunca traz.

## Impact

- `backend/src/nucleo/desafios_extras/regra.py` — a derivação dos desafios extras elegíveis ao
  Guerreiro(a) em sessão.
- `backend/src/nucleo/trilhas/rotas.py` — `GET /v1/eu/desafios` passa a devolver `semanais` e
  `extras`.
- `apps/app-05-guerreiro/src/api/desafiosEEquipes.ts` e `src/desafios/` — o novo formato da
  resposta e a exibição dos extras.
- Sem migração: nenhuma coluna nova, nenhuma entidade nova.
- Documentação no mesmo PR: `openspec/cronograma-de-fatias.md` (a situação da fatia 8 e o slug),
  `docs/prds/index.md` (a situação do PRD-05, que fecha o Ciclo 01) e
  `docs/09-topicos-em-aberto-e-sugestoes.md` §1 (as duas decisões do fundador de 2026-09-02).
