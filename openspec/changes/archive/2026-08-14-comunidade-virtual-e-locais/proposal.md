## Why

**PRD de origem:** PRD-08 — Comunidades Virtuais e dados do território. Primeira fatia dele
e décima sexta da esteira, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-08-01` (Admin cria a Comunidade Virtual), `RF-08-02` (vínculo
do Guerreiro(a) atribuído pela comunidade da aula agendada), `RF-08-04` (hierarquia de
locais cadastrada por Admin), `RN-08-01` (comunidade só por Admin e nasce vazia),
`RN-08-02` (exatamente uma comunidade, atribuída pela aula) e a primeira metade de
`RN-08-18` (o local nasce de cadastro do Admin).

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
- O **vínculo de comunidade passa a ser entidade com histórico**, o `VinculoJogador` do
  PRD-08 §8, atribuído pela comunidade da aula agendada em que o Guerreiro(a) se cadastra
  (`RF-08-02`, `RN-08-02`).

### Por que a solicitação de local não entra aqui

`RF-08-22` a `RF-08-24` pareciam caber nesta fatia, e não cabem. `RF-08-23` manda o
**Mestre da trilha** — ou um Admin — avaliar a solicitação, e a `SolicitacaoDeLocal` do
PRD-08 §8 chega à trilha pelo atributo **desafio de origem**. A jornada §5.3 diz o mesmo: a
solicitação nasce depois que o Guerreiro(a) aceita um desafio de coleta e descobre que falta
o local.

Sem `DesafioDeColeta`, que é de fatia seguinte, não há como escopar qual Mestre avalia sem
inventar regra transitória. Os três requisitos vão para a fatia do desafio, onde o vínculo
que os sustenta existe.

Fica registrado, para aquela fatia, um achado desta: a solicitação de local **não é a quinta
natureza da `fila-de-avaliacao`**. Aquela capacidade tem o requisito "Nenhuma solicitação
cria cadastro, persona ou acesso", válido "inclusive quando aprovadas"; `RN-08-18` manda o
oposto — a aprovação **cria o local**. Some-se que o avaliador pode ser o Mestre da trilha, e
não só um Admin, e que nada no PRD-08 estende à solicitação de local o prazo de 7 dias das
quatro naturezas.

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

O que é do PRD-08 mas de outra fatia:

| Fica para                                | Porque                                                   |
| ---------------------------------------- | -------------------------------------------------------- |
| `RF-08-22`, `RF-08-23`, `RF-08-24`       | solicitação de local: precisa do desafio de origem        |
| `RF-08-05`, `RF-08-06`                   | catálogo de tipos de coleta e desafio                     |
| `RF-08-07` a `RF-08-13`, `RF-08-21`      | série, registro, invalidação e auditoria                  |
| `RF-08-16`, `RF-08-19`, `RF-08-20`       | painel e exportação: exigem série                         |
| `RF-08-17`, `RF-08-18`                   | consulta das séries pelo Guerreiro(a) e pelo responsável  |
| `RF-08-25` a `RF-08-27`                  | etiqueta ODS herdada pelo desafio de coleta               |
| `RF-08-03`                               | transferência, fora do Ciclo 01 (invariante 4)            |

As duas pendências do PRD-08 §14 **não alcançam este recorte**: a autenticação do sensor
trava `RF-08-14`, e o critério de agregação mínima dentro do bairro trava `RF-08-16` e
`RF-08-19`. Nenhum dos três está aqui.

## Capabilities

### New Capabilities

- `comunidade-virtual`: a criação da comunidade por Admin, o nascimento vazio, a
  granularidade máxima declarada, e o vínculo do Guerreiro(a) como entidade com histórico,
  atribuído pela comunidade da aula agendada e único vigente por Guerreiro(a).
- `local-do-territorio`: a hierarquia de seis níveis com local pai dentro da mesma
  comunidade, e o cadastro do local por Admin como a única origem de local nesta entrega.

### Modified Capabilities

- `persona-e-credencial`: o vínculo de comunidade do Guerreiro(a) deixa de ser atributo da
  `Persona` e passa a ser o `VinculoJogador`, com início, fim e histórico. O requisito
  vigente já diz "nem com mais de uma **vigente**", e continua valendo palavra por palavra —
  o que muda é onde o vínculo mora e de onde ele vem (`RN-01-05`, `RF-08-02`).

## Impact

- `backend/src/nucleo/`: módulo novo `comunidades/` — a comunidade, o `VinculoJogador` e as
  rotas de Admin. Módulo novo `locais/` — a hierarquia e o cadastro por Admin.
- `backend/src/nucleo/personas/`: a `ComunidadeVirtual` sai de `modelo.py` para o módulo
  novo, e `Persona.comunidade_virtual_id` cede lugar ao `VinculoJogador`. O
  `CheckConstraint` que hoje garante `RN-01-05` na tabela muda de forma junto. Migração do
  Alembic, com cuidado para preservar os vínculos já gravados.
- `backend/src/nucleo/aulas/`: a comunidade da aula passa a ser a origem declarada do
  vínculo (`RF-08-02`).
- `backend/src/nucleo/principal.py`: registra os dois roteadores novos.
- `backend/tests/`: as rotas novas, a recusa do segundo vínculo vigente, a recusa do local
  pai de nível errado ou de outra comunidade, e a comunidade recém-criada que responde sem
  nenhum local.
- `docs/prds/index.md`: o PRD-01 passa à situação **implementado**, sexto valor do
  vocabulário da coluna, por decisão do fundador.
- `docs/`: nada mais. O **rótulo de ciclo** fica como parâmetro de operação, sem registro
  normativo — decisão do fundador, que encerra a questão aberta deixada pela fatia anterior.

## Questões que ficam para o `design.md`

1. **Como o `VinculoJogador` substitui `Persona.comunidade_virtual_id` sem perder a garantia
   de `RN-01-05`.** Hoje a regra é um `CheckConstraint` de tabela. Com o vínculo em entidade
   própria, "exatamente um vigente" vira índice parcial único, regra de aplicação, ou os
   dois — e a migração precisa converter os vínculos existentes sem janela em que a
   invariante não valha.
2. **Onde a hierarquia se valida.** Os seis níveis são ordenados, e o local pai tem de ser do
   nível imediatamente acima, dentro da mesma comunidade.
3. **O que a granularidade máxima da comunidade governa** no cadastro de local, já que ela é
   atributo declarado na criação e `RF-08-06` só a exige do desafio, que não entra aqui.
