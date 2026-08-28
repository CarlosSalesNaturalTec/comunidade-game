## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta, e já está pronto:

- `POST /aportes` (Form, com `comprovante` opcional), `GET /vitrine/necessidades`,
  `GET /tipos-de-recurso`, `POST /aulas` com `recursos_declarados` e `GET /aulas` já existem e
  não mudam — `openspec/specs/aporte/spec.md`, `necessidade-de-recurso`, `aula-e-presenca`.
- A confirmação automática da aula pelo aporte já é regra do núcleo (`aporte` — "O aporte que
  fecha a diferença confirma a aula pendente de lastro"). A App 03 só relê.
- `Atividade` vive em `trilhas/modelo.py`, com `missao_id` **não nulo**, e o crédito do Resultado
  passa por `conferir_posse_da_trilha` e por `creditar_pontuacao_do_resultado(..., trilha=...)`.
- `PontoRegular` aceita **exatamente uma** referência — trilha ou poder.

## Goals / Non-Goals

**Goals:** abrir a atividade fora de trilha sem afrouxar a atividade de trilha; ligar o circuito
recurso → falta → necessidade → aporte → confirmação pela App 03, sem que a aplicação calcule
nada de economia.

**Non-Goals:** rota de gestão para necessidades; listagem de aportes registrados; atividade
prevista no agendamento (`RF-02-30`); absorção pela App 03, que é ato do Mestre na App 09.

## Decisions

1. **A atividade avulsa reaproveita `Atividade`**, com `missao_id` **nulo** e uma coluna
   `poder_id` nova. O PRD-02 §8 é explícito em não criar entidade nova, e `Resultado` já aponta
   `atividade_id` — entidade separada duplicaria o lançamento inteiro. _Descartado:_ `AtividadeAvulsa`
   própria.
2. **A âncora é garantida no banco**, por `CheckConstraint` que exige `missao_id` **ou**
   `poder_id`, nunca os dois nem nenhum — a mesma forma da regra que `creditar_ponto_regular` já
   aplica em código. _Descartado:_ só validar na regra, que deixa a garantia fora do esquema.
3. **Módulo novo `backend/src/nucleo/atividades/`** (regra e rotas) para `POST /v1/atividades`,
   em vez de estender `trilhas/rotas.py`: a posse é outra (Admin, não Mestre autor) e a
   capacidade é outra. O modelo continua em `trilhas/modelo.py`, onde `Atividade` já mora.
4. **O desvio do lançamento é por ausência de missão**, não por sinalizador novo:
   `registrar_resultado` que receba atividade sem missão pula `conferir_posse_da_trilha`, exige
   Admin e chama a pontuação com o poder da atividade. `creditar_pontuacao_do_resultado` passa a
   receber **trilha ou poder**; com poder, credita o ponto regular e não chama `avaliar_niveis`
   nem o badge de valores e causas, que são percurso de trilha. _Descartado:_ campo `avulsa` na
   `Atividade`, que seria estado derivável de `missao_id`.
5. **A App 03 lê as necessidades pela rota pública** `GET /vitrine/necessidades`, sob a chave da
   aplicação que ela já envia: a saída é a mesma que a spec fixa para as duas rotas existentes,
   não traz pessoa e alcança todas as comunidades — que é o alcance do Admin. _Descartado:_ rota
   de gestão nova, que duplicaria a derivação sem acrescentar campo.
6. **`RF-02-67` é releitura, não estado local.** Depois do `POST /aportes` bem-sucedido, a área
   Recursos relê as necessidades e a agenda e apresenta o que voltou. A aplicação nunca marca
   aula como confirmada por conta própria.
7. **Área nova por assunto, no padrão do `App.tsx`**: `recursos/` (aporte e necessidades) e
   `atividades/` (cadastro da avulsa), cada uma com `api.ts`, tela e teste, e a declaração de
   recursos entrando no `FormularioDeAgendamento` que já existe.
8. **Nenhum custo novo entra no livro-razão por esta fatia**: o aporte já é a porta de crédito e
   a reserva e a baixa da aula já são lançamentos do núcleo.

## Risks / Trade-offs

- `missao_id` nulo afrouxa, no esquema, a garantia de que a atividade de trilha pertence a uma
  missão → o `CheckConstraint` da decisão 2 e a recusa de `trilhas.regra.criar_atividade`, que
  segue exigindo a missão, guardam os dois lados.
- Quem só realiza atividade avulsa acumula ponto regular no poder e **não sobe nível** → é o que
  o documento 11 §6 determina; nível é percurso de trilha, e a fatia não o altera.
- A área Recursos lê necessidades de **todas** as comunidades, sem filtro → é o alcance do Admin
  hoje; filtro por comunidade só se a rota ganhar o parâmetro, e aí é fatia própria.

## Migration Plan

Uma revisão Alembic: `atividade.missao_id` passa a admitir nulo, entra `atividade.poder_id` com
chave estrangeira para `poder` e entra o `CheckConstraint` da decisão 2. Não há dado a
retroceder — toda `Atividade` existente tem missão e satisfaz a restrição. O _rollback_ exige
que nenhuma atividade avulsa tenha sido cadastrada.
