## 1. Modelo e migração

- [ ] 1.1 Tornar o índice único de `nick.valor` insensível a caixa em
      `backend/src/nucleo/personas/modelo.py` e acrescentar a coluna `nick` a
      `SolicitacaoDeParticipacao` em `backend/src/nucleo/fila/modelo.py`, com a migração
      Alembic correspondente (`RN-01-30`, `RF-01-25`); verificar que `alembic upgrade head`
      sobe limpo e que gravar "Zeferina" e "zeferina" passa a colidir

## 2. Nick do adulto na persona

- [ ] 2.1 Em `backend/src/nucleo/personas/regra.py`, estender a unicidade e a exigência de nick
      ao Mestre — nick opcional para Apoiador e Mestre, obrigatório só para Guerreiro(a) — e
      garantir que a recusa por nick em uso responde 422 no campo `nick` sem revelar de quem é
      nem de que papel (`RF-01-19`, `RN-01-22`, `RN-01-30`, `RN-14-10`)
- [ ] 2.2 Expor no mesmo módulo a função de conferência de disponibilidade restrita a nicks de
      adulto, incluindo os nicks reservados por solicitação pendente, e a geração de sugestões
      de variação que também só olham adulto (`RF-14-13`, `RN-01-22`, `RN-14-23`)

## 3. Reserva do nick na fila

- [ ] 3.1 Em `backend/src/nucleo/fila/regra.py`, gravar o nick declarado no pré-cadastro de
      Apoiador, recusar nick indisponível, recusar nick declarado em solicitação de Mestre e
      derivar a reserva de `decidido_em is None and prazo >= agora`, sem coluna de vencimento
      nova (`RF-01-25`, `RN-01-28`, `RN-01-30`, `RF-14-13`)

## 4. Rotas

- [ ] 4.1 Criar `GET /v1/nicks/disponibilidade` em `backend/src/nucleo/personas/rotas.py`, com
      chave de aplicação e sem credencial de persona, devolvendo disponibilidade e sugestões
      (`RF-14-13`); verificar que nick de Guerreiro(a) sai como disponível
- [ ] 4.2 Criar `PUT /v1/eu/apoiador/identidade` e `PUT /v1/eu/mestre/identidade`, que definem
      ou trocam o nick da própria persona em sessão, com 403 para outro papel e para tentativa
      de alterar persona alheia (`RF-14-12`, `RN-14-10`, `RN-01-30`)
- [ ] 4.3 Conferir que a nova rota pública entra no freio por origem já vigente para consulta
      de nick (`RF-01-65`), sem número novo

## 5. Testes

- [ ] 5.1 Em `backend/tests/test_persona.py`, cobrir os cenários do delta de
      `persona-e-credencial`: Apoiador e Mestre criados sem nick, nick de Mestre colidindo com
      nick de Guerreiro(a) e com nick de Apoiador, colisão insensível a caixa, e a recusa que
      não revela o papel de quem tem o nick
- [ ] 5.2 Criar `backend/tests/test_identidade_do_adulto.py` cobrindo os cenários do delta de
      `identidade-do-adulto`: nick livre disponível, nick de Apoiador e de Mestre
      indisponíveis, **nick de Guerreiro(a) devolvido como disponível**, variações que não
      colidem com adulto, conferência disponível que ainda assim é recusada na gravação, e os
      403 da rota de identidade
- [ ] 5.3 Em `backend/tests/test_fila.py`, cobrir os cenários do delta de `fila-de-avaliacao`:
      nick gravado no pré-cadastro sem criar persona, nick de adulto em uso recusado, nick
      declarado em solicitação de Mestre recusado, nick reservado saindo como indisponível,
      segunda solicitação com o mesmo nick recusada, reserva vencida e solicitação recusada
      liberando o nick, e reserva que não impede o cadastro de um Guerreiro(a)

## 6. Documentação

- [ ] 6.1 Gravar as decisões novas nos documentos-fonte e nos PRDs, no mesmo PR: documento 02
      §1 (Mestre passa a ter nick e avatar; o nick do adulto é opcional; o Admin digita o nick
      na colisão e no cadastro direto de Apoiador), documento 11 §8.2 (o card do Mestre passa a
      exibir avatar e nick no lugar do nome, mantendo a prova pública na página individual),
      documento 09 (mover "Conferência do nick no pré-cadastro" para os já decididos e revisar
      as linhas "Quem escolhe o nick do Apoiador" e "Unicidade do nick"), PRD-01 (`RN-01-30`,
      §8 `Persona`/`Apoiador`/`SolicitacaoDeParticipacao`, §9 com as rotas novas), PRD-14
      (`RF-14-12`, `RF-14-13`), PRD-09 (nick e avatar do Mestre) e `docs/prds/index.md`
