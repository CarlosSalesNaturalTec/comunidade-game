## Why

**PRD de origem:** PRD-08 — Comunidades Virtuais e dados do território. Primeira fatia dele
e décima sexta da esteira, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-08-01` (Admin cria a Comunidade Virtual), `RF-08-02` (vínculo
do Guerreiro(a) atribuído pela comunidade da aula agendada), `RF-08-04` (hierarquia de
locais), `RF-08-22` (Guerreiro(a) solicita local ausente), `RF-08-23` (Mestre da trilha ou
Admin aprova ou recusa com motivo), `RF-08-24` (alerta das solicitações em aberto),
`RN-08-01` (comunidade só por Admin e nasce vazia), `RN-08-02` (exatamente uma comunidade,
atribuída pela aula) e `RN-08-18` (local nasce de cadastro do Admin ou de solicitação
aprovada; o pedido em si não cria local).

**O PRD-01 fechou.** As quinze fatias anteriores cobriram 59 dos 66 `RF-01-nn` e 45 dos 51
`RN-01-nn`. Os que restam não são recorte do PRD-01: `RF-01-24`, `RF-01-58` e `RF-01-60`
esperam o livro-razão (PRD-07); `RF-01-66`, `RN-01-08`, `RN-01-09`, `RN-01-26` e `RN-01-47`
esperam o território; `RF-01-41` espera o desafio de coleta e o desafio extra; `RF-01-44`
vale a partir do Ciclo 02 e se prende ao fluxo de publicação, que a spec `trilha-e-missao`
atribui ao PRD-09; `RF-01-31` é pendência declarada no próprio PRD-01 §14. As fatias
anteriores já vinham nomeando esses restos uma a uma.

Por isso entra o PRD-08, que o documento 99 §9 põe em segundo lugar, liberado a partir do
PRD-01. E o núcleo já deixou o encaixe pronto: `ComunidadeVirtual` existe hoje como entidade
sem nenhuma rota, com o registro explícito de que "criação, hierarquia de locais e
transferência são comportamento do PRD-08".

Esta fatia abre essa superfície e para antes da medição. Ela é o piso de tudo o que vem
depois no PRD-08: sem local cadastrado não há série, porque `RF-08-07` exige que o
Guerreiro(a) selecione "um local cadastrado da sua comunidade".

## What Changes

- A **Comunidade Virtual ganha rota**: um Admin a cria com nome, localização e granularidade
  máxima, e ela nasce vazia — sem locais, sem séries, sem Guerreiros e Guerreiras
  (`RF-08-01`, `RN-08-01`).
- Nasce a **hierarquia de locais** em seis níveis — comunidade, bairro, rua, condomínio,
  bloco e quadra —, cadastrada por Admin, cada local apontando para o local pai
  (`RF-08-04`).
- Nasce a **solicitação de local**: o Guerreiro(a) pede a inclusão do que falta, o Mestre da
  trilha ou um Admin aprova — e é a aprovação que **cria o local** — ou recusa com motivo.
  Os dois enxergam as solicitações em aberto (`RF-08-22`, `RF-08-23`, `RF-08-24`,
  `RN-08-18`).
- O **vínculo de comunidade passa a ser entidade com histórico**, o `VinculoJogador` do
  PRD-08 §8, atribuído pela comunidade da aula agendada em que o Guerreiro(a) se cadastra
  (`RF-08-02`, `RN-08-02`).

### A solicitação de local não é a quinta natureza da fila

`RF-08-22` fala em "fila de aprovação", mas a capacidade `fila-de-avaliacao` não a comporta,
e o motivo é de regra, não de arrumação. Aquela capacidade tem o requisito **"Nenhuma
solicitação cria cadastro, persona ou acesso"**, válido "inclusive quando aprovadas" — nas
quatro naturezas, o que a aprovação produz depende de ato posterior de um Admin. Aqui é o
contrário: `RN-08-18` manda a **aprovação criar o local**. Somam-se duas diferenças menores:
o avaliador pode ser o **Mestre da trilha**, e não só um Admin, e nada no PRD-08 estende à
solicitação de local o prazo de 7 dias que a fila aplica às suas quatro naturezas.

A solicitação de local nasce, portanto, na capacidade nova. O que ela reaproveita da fila é
mecânico — o mesmo ciclo de situação, avaliador, parecer e data —, e onde esse
reaproveitamento se dá no código é assunto do `design.md`, não da spec.

### Por que o histórico do vínculo nasce sem rota que o mova

O invariante 4 do documento 99 §6 é explícito: **no Ciclo 01 não há troca de comunidade**, e
`RF-08-03` está marcado "fora do Ciclo 01". Mas o PRD-08 §3.1 pede o vínculo "com histórico
de transferências **no modelo**", e o §8 nomeia o `VinculoJogador` com data de início, data
de fim e admin responsável.

O modelo entra inteiro; a rota de transferência não entra. É o mesmo precedente do avatar e
do nick na capacidade `persona-e-credencial`: o atributo nasce onde a regra o exige, e a
rota que o move é de outra entrega.

### Fora do escopo

O que o PRD-08 §3.2 já exclui: importação de fontes públicas de dados; georreferenciamento
por coordenada de GPS; interface das telas de coleta; escolha do banco de séries temporais.

O que é do PRD-08 mas de outra fatia — tudo o que depende de medição:

| Fica para                                  | Porque                                       |
| ------------------------------------------ | -------------------------------------------- |
| `RF-08-05` a `RF-08-13`, `RF-08-21`        | catálogo, desafio, série, registro e auditoria |
| `RF-08-16`, `RF-08-19`, `RF-08-20`         | painel e exportação: exigem série             |
| `RF-08-17`, `RF-08-18`                     | consulta das séries pelo Guerreiro(a) e pelo responsável |
| `RF-08-25`, `RF-08-26`, `RF-08-27`         | etiqueta ODS herdada pelo desafio de coleta   |
| `RF-08-03`                                 | transferência, fora do Ciclo 01 (invariante 4) |

As duas pendências do PRD-08 §14 **não alcançam este recorte**: a autenticação do sensor
trava `RF-08-14`, e o critério de agregação mínima dentro do bairro trava `RF-08-16` e
`RF-08-19`. Nenhum dos três está aqui.

## Capabilities

### New Capabilities

- `comunidade-virtual`: a criação da comunidade por Admin, o nascimento vazio, a
  granularidade máxima declarada, e o vínculo do Guerreiro(a) como entidade com histórico,
  atribuído pela comunidade da aula agendada e único vigente por Guerreiro(a).
- `local-do-territorio`: a hierarquia de seis níveis com local pai, o cadastro por Admin, a
  solicitação do Guerreiro(a), a avaliação pelo Mestre da trilha ou por Admin que cria o
  local ao aprovar e exige motivo ao recusar, e a consulta das solicitações em aberto que
  alimenta o alerta das duas aplicações.

### Modified Capabilities

- `persona-e-credencial`: o vínculo de comunidade do Guerreiro(a) deixa de ser atributo da
  `Persona` e passa a ser o `VinculoJogador`, com início, fim e histórico. O requisito
  vigente já diz "nem com mais de uma **vigente**", e continua valendo palavra por palavra —
  o que muda é onde o vínculo mora e de onde ele vem (`RN-01-05`, `RF-08-02`).

## Impact

- `backend/src/nucleo/`: módulo novo `comunidades/` — a comunidade, o `VinculoJogador` e as
  rotas de Admin. Módulo novo `locais/` — a hierarquia, a solicitação e a avaliação.
- `backend/src/nucleo/personas/`: a `ComunidadeVirtual` sai de `modelo.py` para o módulo
  novo, e `Persona.comunidade_virtual_id` cede lugar ao `VinculoJogador`. O
  `CheckConstraint` que hoje garante `RN-01-05` na tabela muda de forma junto. Migração do
  Alembic, com cuidado para preservar os vínculos já gravados.
- `backend/src/nucleo/aulas/`: a comunidade da aula passa a ser a origem declarada do
  vínculo (`RF-08-02`).
- `backend/src/nucleo/principal.py`: registra os dois roteadores novos.
- `backend/tests/`: as rotas novas, a recusa do segundo vínculo vigente, a recusa do nível
  fora da hierarquia e o teste de que o pedido de local **não** cria local antes da
  aprovação (`RN-08-18`).
- `docs/prds/index.md`: o PRD-01 muda de situação, por decisão do fundador. Ver a questão
  abaixo sobre o vocabulário da coluna.
- `docs/`: nada mais. O **rótulo de ciclo** fica como parâmetro de operação, sem registro
  normativo — decisão do fundador, que encerra a questão aberta deixada pela fatia anterior.

## Questões que ficam para o `design.md`

1. **Como o `VinculoJogador` substitui `Persona.comunidade_virtual_id` sem perder a garantia
   de `RN-01-05`.** Hoje a regra é um `CheckConstraint` de tabela. Com o vínculo em entidade
   própria, "exatamente um vigente" vira índice parcial único, regra de aplicação, ou os
   dois — e a migração precisa converter os vínculos existentes sem janela em que a
   invariante não valha.
2. **Onde a hierarquia se valida.** Os seis níveis são ordenados, e o local pai tem de ser do
   nível imediatamente acima, dentro da mesma comunidade. Isso é `CheckConstraint`,
   validação de aplicação ou tabela de níveis.
3. **O que a granularidade máxima da comunidade governa** no cadastro de local, já que ela é
   atributo declarado na criação e `RF-08-06` só a exige do desafio, que não entra aqui.
4. **Quanto do ciclo da `fila-de-avaliacao` se reaproveita** no código — o mixin `EmAvaliacao`
   existe e serve —, sem que a solicitação de local vire a quinta natureza da capacidade.

## Questão aberta para o fundador

O índice dos PRDs registra situação com cinco valores — **não iniciado**, **em elicitação**,
**em redação**, **em revisão** e **aprovado** —, e todos descrevem o ciclo de **redação** do
documento, que termina em "aprovado". Não há valor que signifique "o código saiu".

Registrar o fechamento do PRD-01 pede, portanto, uma escolha de vocabulário:

| Opção                                        | Efeito                                                     |
| -------------------------------------------- | ---------------------------------------------------------- |
| **implementado** como sexto valor da lista   | Uma linha na tabela e uma no vocabulário; mistura dois eixos — redação e execução — na mesma coluna |
| Coluna nova **Código**, com a esteira do §9  | Separa os eixos; mexe na largura da tabela e duplica o que o documento 99 §9 já ordena |

A primeira é a menor edição e é a que esta change carrega, salvo indicação contrária.
Confirme antes do `/opsx:apply`.
