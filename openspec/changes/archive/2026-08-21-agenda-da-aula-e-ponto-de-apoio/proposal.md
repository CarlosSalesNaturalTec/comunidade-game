## Why

**Origem: PRD-02**, com `RF-02-12`, `RF-02-13`, `RF-02-14` e `RF-02-95`, e `RF-02-30` em parte;
e **PRD-07**, com `RF-07-47`. Do núcleo, atende `RF-01-28`, `RF-01-32` e `RF-01-18`.

O PRD-02 §2 diz por que a App 03 existe: é onde o Admin *cria a Comunidade Virtual e agenda a
aula que habilita o App 01*. A primeira fatia entregou a primeira metade. Esta entrega a
segunda, e com ela a App 01 (PRD-04, nº 6 do documento 99 §9) passa a ter de onde saber em que
comunidade opera.

O que falta não é regra — é superfície. Dez fatias do PRD-07 foram construídas em volta da
`Aula`: reserva, pendente de lastro, cancelamento que libera, confirmação pelo aporte que fecha
a diferença. **Nenhuma tela agenda uma aula, e nenhuma rota lê uma.** A derivação das aulas
vigentes já está especificada em `openspec/specs/aula-e-presenca/spec.md` e implementada como
regra (`aulas_vigentes`), exercitada só por teste de unidade: não há rota que a exponha, então
o App 01 não tem como abrir.

O mesmo vale para o ponto de apoio, que a aula exige: `RF-07-47` está implementado na escrita e
não tem nem leitura nem tela — o Admin não consegue cadastrar o espaço sem o qual não agenda.

## What Changes

- **`GET /pontos-de-apoio`**: a gestão lê os pontos de apoio, paginado e filtrado por
  comunidade (`RF-07-47`, `RF-01-28`, `RF-01-18`).
- **`GET /aulas`**: a gestão lê a agenda, paginada e filtrada por comunidade e por período,
  com a situação de cada aula (`RF-02-12`, `RF-01-28`, `RF-01-18`).
- **`GET /aulas/vigentes`**: rota **pública** — chave de aplicação sim, credencial de persona
  não —, que expõe a derivação já especificada e já implementada. **Nenhum comportamento novo:
  a regra `aulas_vigentes` não muda** (`RF-02-14`, `RF-02-13`, `RF-01-32`).
- **Cadastro de ponto de apoio na App 03**: lista e formulário de nome e comunidade, com as
  recusas por papel e por campo em falta (`RF-07-47`).
- **Agenda de aulas na App 03**: lista com situação, formulário de comunidade, data, horário
  inicial, horário final e ponto de apoio, e o **cancelamento com motivo** (`RF-02-12`,
  `RF-02-95`, `RF-02-30` em parte).

Nenhuma rota de escrita muda. `POST /pontos-de-apoio`, `PUT /pontos-de-apoio/{id}/responsavel`,
`POST /aulas` e `POST /aulas/{id}/cancelamento` já existem e ficam como estão.

### O que fica para depois — e por quê

Nada disto é exclusão nova: o PRD-02 §3.1 mantém tudo em escopo, e a fatia apenas não alcança.

| Adiado                                     | Trava                                                            |
| ------------------------------------------ | ---------------------------------------------------------------- |
| Recursos declarados e reserva (`RF-02-31`) | pede `GET /tipos-de-recurso`, que não existe — fatia seguinte    |
| Atividade prevista (`RF-02-30`)            | `Atividade` é autoria do Mestre na App 09 (PRD-02 §3.2)          |
| Designar responsável do acervo (`RF-07-49`)| pede rota que liste adultos cadastrados, que não existe          |

A aula agendada sem recursos declarados **nasce confirmada** — é o comportamento que
`openspec/specs/aula-e-presenca/spec.md` já fixa, não uma simplificação desta fatia.

### Pergunta ao fundador, antes do `/opsx:apply`

**A `Aula` do núcleo não tem modalidade, e o ponto de apoio dela é obrigatório.** O PRD-02 §8
lista *modalidade* entre os atributos de `Aula/Agenda` e o `RF-02-30` fala em *"aula on-line ou
presencial"*, mas a capacidade `aula-e-presenca` exige ponto de apoio em toda aula — e aula
on-line com espaço físico obrigatório é contradição. Ela não trava esta fatia, que agenda a
aula presencial, mas precisa de decisão antes que alguém a resolva por suposição. Vai ao
documento 09 como pendência, não como campo novo.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aula-e-presenca`: a agenda e as aulas vigentes ganham **superfície de leitura**. Hoje a
  capacidade define como a aula é agendada, cancelada e como as vigentes se derivam — e
  silencia sobre quem as lê e sob que credencial, o que só não doeu enquanto nenhuma aplicação
  precisava lê-las.
- `ponto-de-apoio`: a gestão passa a **ler** os pontos de apoio da comunidade. A capacidade
  hoje só define o cadastro e a designação do responsável.
- `aplicacao-de-gestao`: a App 03 ganha o **segundo e o terceiro cadastros** — ponto de apoio e
  agenda de aulas —, com o cancelamento da aula.

## Impact

**Backend** — só adição, nenhuma migração:

- `backend/src/nucleo/aulas/rotas.py` — `GET /aulas` e `GET /aulas/vigentes`
- `backend/src/nucleo/pontos_de_apoio/rotas.py` — `GET /pontos-de-apoio`
- `backend/src/nucleo/aulas/regra.py` — `aulas_vigentes` é consumida, não alterada

**App 03** — `apps/app-03-gestao/`: duas áreas novas, consumindo a camada de `comum/react/`. O
campo de data e horário com fuso não tem componente na camada comum; se a fatia precisar criá-lo,
ele nasce em `comum/react/` para as oito aplicações, como manda o documento 15 §12.

**Documentação** — `docs/09-topicos-em-aberto-e-sugestoes.md` §1 recebe a pendência da
modalidade da aula. Nenhum PRD muda, nenhuma decisão nova é tomada por esta change.
