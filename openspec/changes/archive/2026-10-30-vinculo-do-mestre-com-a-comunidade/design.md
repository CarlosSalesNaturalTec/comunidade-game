# Design

## Context

Ver `proposal.md` — Why. O estado que molda o desenho, em três fatos:

- `VinculoJogador` tem coluna `guerreiro_id`, índice parcial único por Guerreiro(a) e
  `abrir_vinculo` que recusa papel diverso (`RN-08-02`). É do Guerreiro(a), e a spec
  `comunidade-virtual` já o descreve assim.
- `Persona.vinculo_vigente` casa `VinculoJogador.guerreiro_id == Persona.id`. Para Mestre
  resolve **sempre** `None` — dez pontos de leitura o consultam.
- `Aula` não guarda Mestre algum. O PRD-02 §8 lista o campo; o PRD-01 §8, não — divergência
  que o `docs/09` §1 registrou duas vezes e que esta change resolve a favor do PRD-02.

As specs de `patrimonio`, `necessidade-de-recurso`, `responsavel-e-vinculo`, `area-do-mestre`
e `aula-e-presenca` **já dizem "as comunidades a que está vinculado"**, no plural. O desenho
não as altera: dá a elas a entidade que faltava.

## Goals / Non-Goals

**Goals:**

- O Mestre passa a ter comunidade, sem que o Guerreiro(a) perca a dele.
- Os dez pontos passam a ler o conjunto de comunidades por um caminho só.
- A suíte deixa de provar um estado que o núcleo recusa criar.

**Non-Goals:**

- Encerrar vínculo de Mestre — não existe no Ciclo 01, e nenhuma rota o fará.
- Mexer no vínculo do Guerreiro(a), no histórico dele ou na transferência (`RF-08-03`).
- A fila do encontro na App 01 — é a fatia 31 do PRD-04, change própria.
- Retroagir sobre aulas já agendadas: as da fase de testes foram canceladas.

## Decisions

### 1. Duas tabelas, não uma derivada

`MestreDaAula` (aula × mestre, N:N) guarda **quem ministra**; o vínculo do Mestre com a
comunidade é tabela própria, **sem `data_fim`**.

**Alternativa descartada:** só `MestreDaAula`, derivando as comunidades por `DISTINCT` nas
aulas do Mestre. Com "nunca encerra" seria preciso contar **aula cancelada** — senão o
cancelamento da última aula revogaria o acesso —, e aí o Mestre leria o acervo por causa de
uma aula que não aconteceu. O vínculo explícito torna "nunca encerra" literal e poupa um
`JOIN` em cada um dos oito pontos de leitura.

### 2. Entidade separada, não reuso do `VinculoJogador`

**Alternativa descartada:** tirar a recusa de `abrir_vinculo` e deixar o Mestre usar a mesma
tabela. Custa zero linha nos dez pontos, mas: `contar_guerreiros_vinculados` — a
**vitalidade da comunidade** do documento 11 §§8.2 e 8.3, que vai à vitrine (`RF-03-02`,
`RF-03-16`) — conta `VinculoJogador` **sem filtrar papel**, e cada Mestre viraria +1
Guerreiro(a) em público, sem erro e sem teste que pegue; o índice único por `guerreiro_id`
travaria o Mestre em uma comunidade só, contra o plural que as specs já escrevem; e o nome
da tabela passaria a mentir. Com entidade separada, a vitalidade não é tocada.

### 3. Um só ponto de escopo, no lugar de três cópias

`escopo_de_comunidade_da_leitura` existe idêntica em `aulas/regra.py` e
`pontos_de_apoio/regra.py`, e `patrimonio.listar_acervo` traz a mesma lógica embutida — as
duas primeiras declarando, no docstring, que são "no molde de `listar_acervo`". As três
passam a uma função única em `comunidades/regra.py`, ao lado de
`filtrar_personas_por_comunidade`, devolvendo **conjunto de ids** em vez de um id: Admin
declara a comunidade e recebe o conjunto de um; Mestre recebe as dele; conjunto vazio
significa lista vazia, nunca erro, como já significava `None`.

Os oito pontos trocam `== alvo` por `.in_(alvos)`; `necessidades` já recebe
`comunidade_ids` como conjunto e quase não muda. As duas guardas de escrita — cancelamento
de aula (`RF-01-72`) e confirmação da entrega (`RF-07-13`) — passam de igualdade a
pertinência, e os enunciados delas seguem valendo sem alteração.

### 4. O seletor de Mestres não filtra por comunidade

Ovo e galinha: é o agendamento que dá comunidade ao Mestre, então filtrar os candidatos por
comunidade deixaria o primeiro agendamento de cada comunidade sem Mestre algum a escolher.
`GET /v1/mestres` já existe e já é consumido pela App 03 — nenhuma rota nova.

### 5. A fixture de teste passa a abrir o vínculo pela entidade própria

`criar_vinculo_jogador(mestre, comunidade)` aparece **63 vezes em 24 arquivos** e grava
`VinculoJogador` com `guerreiro_id` de um Mestre, por fora de `abrir_vinculo`. Nasce uma
fixture para o vínculo do Mestre, e as 63 chamadas passam a ela. Troca mecânica, mas é o
maior volume da change — e é ela que faz a suíte voltar a provar o que o núcleo faz.

## Risks / Trade-offs

- **O agendamento vira BREAKING** — `POST /v1/aulas` passa a recusar corpo sem Mestre. →
  Mitigado pela fase de testes: as aulas existentes foram canceladas, e não há consumidor
  externo. Sem retroação, por decisão do fundador.
- **63 chamadas de fixture a migrar** — erro de troca aparece como teste verde pelo motivo
  errado. → A recusa de Mestre em `abrir_vinculo` permanece, e o modelo do vínculo do
  Guerreiro(a) segue recusando papel diverso: chamada esquecida falha, não passa.
- **A fila de pendências já é O(n·m)** e passa a varrer N comunidades. → No Ciclo 01 a
  ordem de grandeza é de dezenas; não se otimiza aqui, mas a consulta de Guerreiros e
  Guerreiras passa a ser uma só por comunidade, não uma por recompensa.
- **Dois Mestres na mesma aula lendo o painel do dia** encontram o mesmo encontro, o que é
  desejado; mas um Mestre com duas aulas vigentes em comunidades distintas agora alcança o
  caso de desempate, antes só do Admin. → Resolvido na spec de `painel-do-dia`, pelo
  precedente de `RF-01-32` e `RF-01-18`.

## Migration Plan

1. Revisão Alembic cria as duas tabelas **vazias**. Sem backfill, sem dado a preservar.
2. O teste de paridade entre `alembic upgrade head` e `Base.metadata` cobre as duas — é o
   mesmo laço que a correção `2026-09-10-migracao-das-tabelas-de-recompensa-de-marco`
   instituiu, e que o `conftest` sozinho não pega, por montar o schema com `create_all`.
3. Sem rollback de dado: `downgrade` apaga tabelas que nasceram vazias.
4. Depois do merge, o Admin agenda a primeira aula com Mestres — é esse ato, e nenhum
   script, que vincula os Mestres já cadastrados.

## Open Questions

Nenhuma. As quatro travas do recorte — encerramento, obrigatoriedade, retroação e quantos
Mestres por aula — foram decididas pelo fundador em 2026-10-30 e estão no `docs/09` §1.
