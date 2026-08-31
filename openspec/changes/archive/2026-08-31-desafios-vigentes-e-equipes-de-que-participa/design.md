## Context

Fatia de **leitura pura** sobre entidades já de pé. `Atividade`, `Resultado`,
`DesbloqueioDaMissao`, `InscricaoNaTrilha`, `Equipe` e `IntegranteDaEquipe` existem; a
derivação do percurso já está firmada em `openspec/specs/area-do-guerreiro` (o percurso nasce
na leitura, sem tabela de estado por missão), e o contrato de saída restrito a avatar e nick já
está firmado em `openspec/specs/equipe`. Nada de esquema muda.

Motivação e recorte: ver `proposal.md`. As duas decisões de produto desta fatia — o que é
"vigente" no `RF-05-19` e a troca do `RN-05-23` pelo `RN-05-12` no cronograma — foram do
fundador e estão registradas lá.

## Goals / Non-Goals

**Goals:**

- Derivar "em aberto" na leitura, sem campo, tabela nem migração nova.
- Reaproveitar os contratos de saída que já existem, em vez de abrir contrato paralelo.

**Non-Goals:**

- Janela de datas de qualquer espécie sobre a `Atividade`.
- Qualquer escrita: nem de equipe, nem de resultado, nem de ponto.

## Decisions

**1. "Em aberto" é derivado na leitura, no mesmo molde de `derivar_percurso`.**
A consulta parte das inscrições do Guerreiro(a), pega as missões com `DesbloqueioDaMissao`
aprovado, toma as atividades dessas missões e subtrai aquelas que já têm `Resultado` dele.
Sem estado persistido, a lista nunca fica dessincronizada do percurso.
_Alternativas descartadas:_ campo de vigência na `Atividade` (decisão nova de produto — foi ao
fundador e foi recusada); janela pela data da aula (deixaria a atividade on-line sem critério).

**2. A atividade avulsa fica de fora.**
A avulsa ancora em **poder**, não em missão, e não tem percurso de onde derivar "desbloqueada".
O critério que o fundador fixou é missão desbloqueada em trilha inscrita; incluir a avulsa
exigiria um critério de vigência que o PRD não dá.
_Alternativa descartada:_ listar toda avulsa do poder das trilhas inscritas — seria regra nova.

**3. Cada rota nasce no módulo que já é dono da entidade.**
`GET /v1/eu/desafios` em `trilhas/` (onde vivem inscrição, percurso e atividade);
`GET /v1/eu/equipes` em `equipes/`. A regra fica em `regra.py`, a rota em `rotas.py`, como nas
fatias anteriores.
_Alternativa descartada:_ módulo `desafios/` novo — a fatia não tem entidade própria.

**4. `GET /v1/eu/equipes` estende a saída de equipe que já existe.**
Reaproveita `saida_da_equipe` — que já restringe o integrante a avatar e nick — e acrescenta
dois campos: o **papel da persona em sessão** naquela equipe, lido do vínculo dela e não
adivinhado da lista de integrantes, e as **atividades da equipe**. A programação do encontro
sai no mesmo formato que `GET /v1/equipes/{id}/missao` já serve, com a corrente marcada.
_Alternativa descartada:_ o cliente montar a lista chamando `/eu/trilhas/{id}/equipe` por
trilha — não alcança a equipe da aula e multiplica chamada no celular modesto.

**5. As atividades de uma equipe são as que o modelo já vincula a ela.**
Equipe da aula: as atividades daquela aula (`Atividade.aula_id`), de trilha publicada — a
programação do encontro, já definida. Equipe da trilha: as atividades das missões daquela
trilha publicada.
_Alternativa descartada:_ filtrar por modalidade "em equipe" — o PRD não pede o filtro, e
inventá-lo seria regra nova.

**6. Um bloco só na navegação, com duas abas dentro.**
A `AreaDoGuerreiro` ganha o bloco **"Desafios e equipes"**, com as duas telas em abas, no molde
que a `Carteira` já usa. O aparelho de referência é o celular modesto do ponto de apoio
(PRD-05 §10): quatro botões de bloco cabem, seis não.
_Alternativa descartada:_ dois blocos novos na navegação de topo.

## Risks / Trade-offs

- **A leitura dos desafios percorre inscrições, desbloqueios, atividades e resultados** →
  volume do Ciclo 01 é pequeno (uma turma por comunidade) e a consulta parte sempre de um só
  Guerreiro(a); nenhuma pré-agregação se justifica agora.
- **Atividade de missão desbloqueada segue "em aberto" até o Mestre lançar o resultado**, ainda
  que a criança já a tenha feito → é o que o `RF-05-18` já resolve na tela do progresso
  ("aguardando lançamento"); aqui a lista apenas não some sozinha, e a fatia 7 acrescenta a
  entrega da produção.
