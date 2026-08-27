## 1. Núcleo — modelo e migração

- [ ] 1.1 Estender `criacoes_originais/modelo.py`: `equipe_id` e `producao` opcionais,
      `guerreiro_id`, `tipo` (os cinco valores), `motivo_da_devolucao` e as colunas de mídia,
      com a restrição de exatamente um entre equipe e Guerreiro(a) e os dois índices únicos
      parciais (design — decisões 2, 3, 4, 6). Verificar por `uv run pytest
      tests/test_criacao_original.py -x` com a suíte vigente ainda verde.
- [ ] 1.2 Criar a revisão Alembic da tabela `criacao_original` na ordem do plano de migração,
      com `tipo` preenchido como texto nas linhas existentes. Verificar aplicando e revertendo a
      revisão contra o banco de teste.

## 2. Núcleo — regra da entrega e da decisão

- [ ] 2.1 `RF-05-40`, `RF-09-30`: reescrever `entregar_criacao_original` para seguir a
      modalidade da culminância, recusar trilha sem culminância com 409, recusar entrega em
      desacordo com a modalidade com 422 e exigir a produção conforme o tipo.
- [ ] 2.2 `RF-05-42`: fazer a nova entrega antes da validação substituir a produção e devolver a
      situação a "entregue", e recusar com 409 a entrega depois de validada (design — decisão 3).
- [ ] 2.3 `RF-05-42`, `RF-09-34`: exigir e gravar o motivo na devolução, recusando com 422 a
      devolução sem motivo, sem alterar a autoria (`RN-05-13`, `RN-09-04`).
- [ ] 2.4 `RF-09-31`: acrescentar o caminho individual em
      `pontuacao.regra.creditar_pontuacao_da_criacao_original` — mesmos 50 pontos, nível 5 e
      badge de autoria ao Guerreiro(a) que entregou (design — decisão 5).

## 3. Núcleo — rotas

- [ ] 3.1 `RF-05-40`, `RF-05-41`: criar `criacoes_originais/rotas.py` com
      `POST /v1/culminancias/{id}/criacoes`, resolvendo a trilha pela culminância, sob
      `Operacao.suas_criacoes` (design — decisão 1); registrar o roteador em `principal.py`.
- [ ] 3.2 `RF-05-40`: acrescentar `POST /v1/criacoes/{id}/arquivo` e `PATCH
      /v1/criacoes/{id}/arquivo`, espelhando a sessão retomável de `conteudos/rotas.py`
      (design — decisão 4).
- [ ] 3.3 `RF-05-43`, `RF-05-44`: expor `GET /v1/eu/portfolio` com trilha, data da validação,
      autoria e situação de exposição derivada da condição de autorização compartilhada com a
      vitrine (design — decisão 7), alcançando apenas as criações do Guerreiro(a) em sessão
      (`RN-05-21`).
- [ ] 3.4 `RF-09-31`, `RF-09-32`, `RF-09-34`: expor a fila das criações entregues das trilhas do
      Mestre autor, com a produção e a autoria, e as rotas de validar e devolver com motivo, sob
      a posse estrita da trilha.
- [ ] 3.5 `RF-09-33`, `RN-09-19`: estender `condicao_de_autorizacao_vigente` em
      `vitrine/rotas.py` ao autor individual, para que criação individual sem autorização não
      apareça em rota pública.

## 4. App 05 — Área do Guerreiro(a)

- [ ] 4.1 `RF-05-39`: tela da culminância com descrição, critério de validação e modalidade
      escritos pelo Mestre autor, e o aviso de culminância não declarada sem oferecer entrega.
- [ ] 4.2 `RF-05-40`, `RF-05-41`: tela de entrega nos cinco tipos, com progresso do envio de
      mídia e o papel de cada integrante na modalidade de equipe, consultando a equipe
      homologada sem oferecer formá-la (`RN-05-12`).
- [ ] 4.3 `RF-05-42`: exibir a criação devolvida com o motivo em linguagem simples, a autoria
      intacta e o caminho de reenvio.
- [ ] 4.4 `RF-05-43`, `RF-05-44`: tela do portfólio com trilha, data e autoria de cada criação
      validada, marcando o que é público e o que depende de autorização do responsável, sem
      oferecer alterá-la (`RN-05-14`).
- [ ] 4.5 Acrescentar as chamadas de criação original e portfólio ao cliente de API da App 05.

## 5. App 09 — Área do Mestre

- [ ] 5.1 `RF-09-31`, `RF-09-32`: tela da fila das criações a validar, com trilha, critério
      declarado, produção e autoria — cada integrante com o papel, na modalidade de equipe.
- [ ] 5.2 `RF-09-31`, `RF-09-34`: validar, confirmando autoria creditada e badge liberado, e
      devolver exigindo o motivo, sem oferecer editar a produção nem reatribuir a autoria
      (`RN-09-04`).
- [ ] 5.3 `RF-09-33`: informar na criação validada que ela só vai à vitrine com autorização de
      todos os creditados, sem oferecer conceder nem revogar (`RN-09-19`).
- [ ] 5.4 Acrescentar as chamadas da fila, da validação e da devolução ao cliente de API da
      App 09.

## 6. Testes

- [ ] 6.1 Estender `backend/tests/test_criacao_original.py` com os cenários da entrega
      individual e de equipe, da recusa por trilha sem culminância (409), da recusa por
      modalidade em desacordo (422), da substituição antes da validação, da recusa depois de
      validada (409) e do motivo obrigatório na devolução (`RF-05-40`, `RF-05-42`, `RF-09-30`,
      `RF-09-34`).
- [ ] 6.2 Cobrir o crédito da modalidade individual — 50 pontos, nível 5 e badge de autoria ao
      Guerreiro(a) que entregou — e confirmar que o crédito de equipe segue integral a cada
      integrante, sem rateio (`RF-09-31`).
- [ ] 6.3 Cobrir as rotas novas: entrega sob a culminância, envio de mídia, portfólio com a
      situação de exposição e ausência de criação de terceiro, fila do Mestre autor sem alcançar
      trilha de outro Mestre, validar e devolver (`RF-05-40`, `RF-05-43`, `RF-05-44`,
      `RF-09-31`, `RF-09-32`, `RN-05-21`).
- [ ] 6.4 Cobrir na vitrine que a criação individual credita quem entregou e não aparece sem
      autorização vigente (`RF-09-33`, `RN-09-19`).
- [ ] 6.5 Testes das telas da App 05 — culminância, entrega nos cinco tipos com papel de
      integrante, devolução com motivo e reenvio, portfólio com as duas situações de exposição
      (`RF-05-39` a `RF-05-44`).
- [ ] 6.6 Testes das telas da App 09 — fila com critério e papéis, validação, devolução recusada
      sem motivo e o aviso da autorização de divulgação (`RF-09-31` a `RF-09-34`).

## 7. Documentação

- [ ] 7.1 Acrescentar uma linha à tabela de fatias do PRD-05 em `docs/prds/index.md`, marcando
      esta fatia. Nenhuma decisão nova foi tomada: a modalidade da culminância (`RF-09-30`), a
      entrega em mídia e o motivo da devolução já estão nos PRDs e no documento 02 §4, e nada
      muda no documento 09, no documento 99 nem na `nav` do `mkdocs.yml`.
