# Tasks

## 1. Núcleo

- [x] 1.1 `resultados/modelo.py` e migração Alembic: colunas `comprovante_tipo`,
      `comprovante_referencia`, `comprovante_tamanho`, `comprovante_tipo_do_arquivo`;
      `producao` anulável; preenchimento `comprovante_tipo='texto'` nas linhas existentes e
      `NOT NULL` em seguida (`RF-09-149`, `RN-09-64`, design — decisão 1).
- [x] 1.2 `resultados/regra.py`: `registrar_resultado` recebe o comprovante — texto/link no
      corpo, mídia por `envio_id` conferido no armazenamento (posse pela referência, teto e
      tipo reais, referência não reusada); `producao` em texto vale como comprovante em texto,
      e os dois juntos → 422 (`RF-09-149`, `RN-09-64`, design — decisões 2 e 3).
- [x] 1.3 `resultados/regra.py`: `abrir_envio_do_comprovante` — posse da atividade, lista
      fechada, teto de `teto_do_tipo_de_producao`, referência
      `resultados/envios/{persona_id}/{envio_id}` (`RF-09-149`, design — decisão 2).
- [x] 1.4 `trilhas/regra.py`: `situacao_do_pratico(missao, guerreiro)` com `exige_julgamento`,
      e `julgar_pratico_no_lancamento` — julga a pendente, ou grava/reabre a declaração em
      nome do Guerreiro(a) com o comprovante (forma aceita, inscrição, legado sem forma) e
      julga; 422 para julgamento ausente quando exigido e presente quando não cabe
      (`RF-09-150`, `RN-09-65`, `RN-09-66`, `RN-09-52` a `RN-09-55`, design — decisões 4 e 5).
- [x] 1.5 `lancar_resultados_da_atividade` chama `julgar_pratico_no_lancamento` por
      participante, na mesma transação (`RF-09-150`, design — decisão 4).
- [x] 1.6 Rotas: `ParticipanteDoLancamentoCorpo` com `comprovante` e `julgamento_do_pratico`,
      `producao` opcional; `entregar_na_aprovacao` quando cumpriu; nascem
      `POST /v1/atividades/{id}/lancamentos/comprovantes`,
      `GET /v1/missoes/{id}/desbloqueios/{id_do_guerreiro}`, `GET /v1/aulas/{id}/resultados`
      (nick, sem nome civil) e `GET /v1/resultados/{id}/comprovante` (`RF-09-149` a
      `RF-09-151`, `RN-09-18`, design — decisão 6).
- [x] 1.7 Testes em `backend/tests/` (arquivos de resultado e de desbloqueio prático):
      comprovante nas seis formas, texto simples legado, envio não concluído, de outra
      persona, reusado, 413/422 de teto e tipo; julgamento exigido ausente, presente sem
      prático, pendente julgado com a entrega do Guerreiro(a), declaração em nome nova e
      reaberta, forma diferente recusada, legado sem forma, não inscrito, motivo faltando
      desfazendo o Resultado, 5 pontos uma vez; leituras com recorte do Mestre autor, Admin,
      403 e 404.

## 2. App 09

- [x] 2.1 `turmas/api.ts`: tipos e chamadas do comprovante, do envio prévio (reusando o envio
      retomável de `trilhas/api.ts`), da situação do prático, dos resultados da aula e dos bytes
      do comprovante (`RF-09-149` a `RF-09-151`).
- [x] 2.2 `turmas/TelaDaAula.tsx`: seção **Lançar resultado de uma atividade** vira formulário
      — _select_ da atividade, nick, forma e corpo ou arquivo do comprovante, momento,
      desfecho, um por envio; julgamento com critério, forma aceita e entrega do Guerreiro(a)
      quando exigido, e o aviso de que o comprovante vira a comprovação; aviso de coleta; lista
      **Lançados nesta aula** (`RF-09-43`, `RF-09-44`, `RF-09-148` a `RF-09-151`, `RN-09-16`,
      `RN-09-18`, `RN-09-65`, `RN-09-66`).
- [x] 2.3 Remover `TelaDeLancamento.tsx`, a prop `aoAbrirLancamento` e a navegação até ela em
      `App.tsx`/`TelaDeMinhasTurmas.tsx` (`RF-09-148`, design — decisão 7).
- [x] 2.4 `turmas/turmas.test.tsx`: lançamento com texto e com foto, nick não encontrado, sem
      atividade, sem comprovante, julgamento exibido e ausente conforme a situação, aviso da
      declaração em nome, recusa do núcleo em linguagem simples, lista dos lançados com
      atualização após o envio e abertura do arquivo.

## 3. Documentação

- [x] 3.1 Documento 09 §1: linha da decisão de 2026-11-27 em "Já decididos", com a revisão do
      `RF-09-74`. Documento 11 §4: a produção do Resultado é o comprovante, em seis formas.
      PRD-09: `RF-09-148` a `RF-09-151`, `RN-09-64` a `RN-09-66`, `RF-09-74` revisto, §9 com
      as rotas novas, §13 com a decisão, §15 com a rastreabilidade. Documento 99 §8 se a
      relação mudar. Cronograma: fatia 41 do PRD-09 marcada como implementada com o slug.
