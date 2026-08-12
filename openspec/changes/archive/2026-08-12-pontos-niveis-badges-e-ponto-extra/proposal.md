## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Sexta fatia, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-01-20` (parcial — a parte de resultado), `RF-01-21` (parcial),
`RF-01-56`, `RF-01-57`, `RF-01-58`, `RN-01-38`, `RN-01-39`, `RN-01-40`.

A quinta fatia entregou a cadeia trilha → missão → atividade — a definição do que se faz —, mas
não a **realização**: o registro de que um Guerreiro(a) fez aquilo. A própria proposta daquela
fatia já apontou a lacuna, ao adiar "a parte de resultado" de `RF-01-20` para "a fatia seguinte,
que credita ponto" — esta. Sem `Resultado`, `RF-01-21` ("pontos... derivados das realizações")
não tem de onde derivar. Esta fatia entrega os dois juntos: o `Resultado` (documento 11 §4, "
resultado lançado pela gestão") e o **motor de pontuação** do documento 11 §5 que o lê — pontos
regulares por trilha ou poder, o percurso de nível que não depende de território nem de autoria,
os badges que nascem só do que já existe no núcleo, e as duas contas do ponto extra.

## What Changes

- Nasce o **Resultado**, o registro de que um Guerreiro(a) realizou uma atividade: quem, qual
  atividade, quando, o que produziu (contra a `producao_esperada` já declarada na atividade) e o
  desfecho lançado pela gestão — realizada, realizada com mérito ou mérito extra por auxílio aos
  colegas (documento 11 §4). É o objeto que faltava para fechar `RF-01-20` (`RF-01-20`).
- Nasce o **Ponto regular**, por trilha ou poder, creditado a partir de `Resultado` contra a
  tabela de fontes do documento 11 §5 — nunca debitado (`RF-01-21`, `RN-01-38`).
- Nasce o **Nível**, por trilha ou poder, com os critérios verificáveis do documento 11 §6 que
  **não dependem de outro PRD**: nível 1 (inscrito e primeira atividade realizada), nível 2
  (1/3 das missões obrigatórias desbloqueadas) e nível 4 (todas as obrigatórias desbloqueadas e
  ao menos um mérito extra por auxílio). Nível conquistado nunca regride (`RF-01-21`).
- Nascem os **Badges** que o núcleo já consegue verificar sozinho a partir de Resultado: de
  nível (um por nível alcançado) e de valores/causas (atividade de natureza "valores e temas
  transversais"). Badge é por trilha ou por poder, nunca global (`RF-01-21`).
- Nasce o **Ponto extra em duas contas**: acumulado, que só cresce, e saldo disponível, que só
  o Guerreiro(a) tem e nunca fica negativo. Nesta fatia as duas contas **só recebem crédito**;
  o débito por troca é de outra fatia (`RF-01-56`, `RF-01-57`, `RF-01-58`, `RN-01-39`,
  `RN-01-40`).
- O lançamento de pontos é sempre autoria de quem lança — Mestre ou automático do sistema —,
  reaproveitando o mixin de autoria já existente (`RN-01-13`, já em vigor desde a fundação).

**Nenhuma rota nova sob `/v1`.** Como a quinta fatia, esta entrega **entidade e regra de
crédito**, não rota — nem de lançamento manual, nem de leitura pública. A leitura pelos jogos
(`RF-01-22`) não é endpoint próprio: o documento 11 §8.4 declara que o jogo lê o mesmo *card*
público da vitrine (`GET /v1/vitrine/guerreiros/{nick}`), e essa rota está travada — como
`RF-01-33`/`RF-01-34` já estavam na fatia anterior — pela pendência "Números da proteção das
rotas públicas" do documento 09. `RF-01-22` fica então para a fatia que construir a vitrine,
depois que o fundador decidir os números.

### O que esta fatia não tem, e não é omissão

**Nível 3 e nível 5 ficam de fora.** O nível 3 exige série de coleta ativa — entidade do PRD-08,
entrega nº 2 do documento 99 §9, que ainda não existe no núcleo. O nível 5 exige culminância
validada pelo Mestre autor — entidade do PRD-09, que também ainda não existe. Os critérios 1, 2
e 4 nascem aqui; 3 e 5 nascem quando as entidades de que dependem existirem.

**Badge de território e badge de autoria ficam de fora**, pela mesma razão: dependem de série de
coleta (PRD-08) e de criação original validada em culminância (PRD-09).

**Badge de conquista Guardião do Acervo fica de fora.** Ele nasce do "badge de conduta" lançado
pelo Mestre/gestão uma vez por ciclo, ou do item apresentado "por encontro presencial" (documento
11 §5) — nenhum dos dois é Resultado de uma atividade de trilha, e o segundo depende de um
encontro identificável, que só existe com `Aula/Agenda`, da fatia da operação da aula.

**O débito do saldo disponível fica de fora.** Ele só acontece na troca por recompensa avulsa, e
a `Troca` é entidade do PRD-07 (`RF-01-60`), entrega nº 3 do documento 99 §9 — a fatia anterior
já tinha registrado essa dependência. Aqui a conta nasce e recebe crédito; a rota que debita
chega com o livro-razão.

**Nenhuma rota de lançamento manual.** Quem lança o `Resultado` — realizada, com mérito, ou o
mérito extra por auxílio aos colegas — é o Mestre ou a gestão, pelas rotas de gestão do PRD-09 e
do PRD-02: o PRD-01 §9 não declara rota própria de lançamento aqui, só a entidade e a regra de
crédito, como a quinta fatia entregou entidade sem rota de autoria.

**Pontuação negativa fica de fora.** O prazo de guarda do registro de infração é pendência
declarada no PRD-01 §14 e precisa ser decidida no documento-fonte antes de virar código.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação, cadência de
coleta e valoração de aporte (a régua em si já é do documento 11, aplicada aqui, não inventada);
captura da imagem, conversa de cadastro e geração do descritor no aparelho; exclusão do
_template_; telemetria da Batalha de Laser e personalização por IA.

O que é do PRD-01 mas de outra fatia, por dependência declarada ou por pendência aberta:

| Fica para                           | Porque                                                            |
| ------------------------------------ | ------------------------------------------------------------------ |
| Nível 3 e badge de território        | dependem de série de coleta, do PRD-08                            |
| Nível 5 e badge de autoria           | dependem de culminância validada, do PRD-09                       |
| `RF-01-59`, débito de `RF-01-56`     | dependem de `Troca` e do catálogo avulso, do PRD-07 (`RF-01-60`)   |
| `RF-01-22`                            | rota pública (mesmo *card* da vitrine), travada pela pendência "Números da proteção das rotas públicas" |
| `RF-01-20`, partes de equipe e presença; `RF-01-32`, `RF-01-36` a `RF-01-39` | pendem de `Aula/Agenda`, da fatia da operação da aula |
| `RF-01-40` a `RF-01-45`              | a etiqueta ODS propaga para coleta (PRD-08) e desafio extra        |
| `RF-01-49` a `RF-01-53`, `RF-01-55`  | documento 09, "Números da proteção das rotas públicas"            |
| `RF-01-23` a `RF-01-26`, `RF-01-29`, `RF-01-46`, `RF-01-47` | território, ledger, fila de avaliação e auditoria |

## Capabilities

### New Capabilities

- `resultado-de-atividade`: o registro de que um Guerreiro(a) realizou uma atividade, com o
  desfecho lançado pela gestão — realizada, com mérito ou mérito extra por auxílio aos colegas.
- `pontos-niveis-e-badges`: o ponto regular creditado a partir do resultado, o percurso de nível
  1, 2 e 4 por trilha ou poder, e os badges que o núcleo verifica sozinho.
- `ponto-extra`: as duas contas do ponto extra — acumulado, que só cresce, e saldo disponível,
  que nunca fica negativo — recebendo crédito a partir do mesmo resultado.

### Modified Capabilities

Nenhuma. `atividade-de-trilha` já entrega a definição do que se faz; `resultado-de-atividade`
referencia essa definição por chave estrangeira, sem mudar nenhum requisito dela.

## Impact

- `backend/src/nucleo/`: módulos novos `resultados/` (o `Resultado` e seu desfecho),
  `pontuacao/` (ponto regular, nível, badge) e `ponto_extra/` (as duas contas), lendo
  `atividade` e `trilha` já existentes.
- `backend/alembic/`: migração para as novas entidades de resultado, ponto, nível, badge e ponto
  extra.
- Nenhuma rota nova sob `/v1` — nem de lançamento nem de leitura pública. O lançamento é das
  aplicações de gestão (PRD-02, PRD-09); a leitura pública é da fatia da vitrine, depois da
  pendência de números resolvida.
- `docs/`: nenhuma decisão nova nesta fatia — a régua de pontos, níveis e badges já está no
  documento 11 §§5–7 e é aplicada, não criada. `docs/prds/index.md` recebe a situação atualizada
  se ela mudar ao fim da implementação.
