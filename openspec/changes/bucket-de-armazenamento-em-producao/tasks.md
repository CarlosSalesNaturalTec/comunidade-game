# Tarefas — bucket de armazenamento em produção

Recorte em `proposal.md`; decisões em `design.md`. Nenhum requisito muda: as tarefas fazem
existir o destino que `RF-09-19`, `RF-07-49` e as demais capacidades de envio já supõem.

## 1. Esteira

- [ ] 1.1 Em `.github/workflows/backend-deploy.yml`, declarar
  `CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE=comunidade-game-armazenamento` em `--set-env-vars`, ao
  lado de `CG_AMBIENTE` e `CG_GEMINI_MODELO`, nas **duas** etapas — Job de migração e serviço
  —, com o valor em `env:` no topo do workflow (design — decisão 1).

## 2. Falha cedo

- [ ] 2.1 Fazer o arranque recusar, com mensagem nomeando a variável e o ambiente, quando
  `ambiente == "producao"` e o bucket não foi declarado. A validação fica junto da configuração
  ou da construção da porta, antes de qualquer requisição. Não estender às portas de IA, onde a
  indisponibilidade é requisito (`RF-09-91`, `RN-04-21`, `RN-05-35`) — design, decisão 2 e
  Non-Goals.

## 3. Testes

- [ ] 3.1 Em `backend/tests/test_armazenamento_porta.py` (novo), cobrir o adaptador de nuvem,
  que hoje não tem teste nenhum: bucket declarado constrói a porta; bucket vazio em produção
  recusa com a mensagem esperada, e não com `IndexError`; fora de produção a porta é a de
  disco, sem exigir credencial (design — decisão 2).

## 4. Documentação

- [ ] 4.1 Em `backend/README.md`: remover a frase que afirma o fallback para disco local, que é
  falsa — em produção não há fallback; acrescentar `CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE` à
  lista de variáveis dizendo que sem ela o serviço não sobe; incluir no provisionamento a
  criação do bucket `comunidade-game-armazenamento` em `southamerica-east1` e a concessão de
  acesso a objeto à `nucleo-runtime` **no bucket**, não no projeto (design — decisão 3).
- [ ] 4.2 Registrar a change em `openspec/cronograma-de-fatias.md`: linha sem número no bloco
  do PRD-09, com o slug. Nada muda em `docs/`, no documento 99 nem na `nav` do `mkdocs.yml` — a
  change não toma decisão nova nem altera requisito.
