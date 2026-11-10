# Tasks

## 1. Núcleo

- [ ] 1.1 `trilhas/modelo.py`: `Missao.materiais` (`ARRAY(Text)`, não nula, padrão `[]`) e a
      migração Alembic com `server_default '{}'`, sem _backfill_ (`RF-09-140`, `RN-09-61`,
      design — decisão 1)
- [ ] 1.2 `trilhas/regra.py`: `_conferir_materiais_da_missao` (tira os espaços das pontas,
      recusa item vazio e lista nula com 422 no campo `materiais`), usada por `criar_missao` e
      `corrigir_missao`; `duplicar_trilha` copia os materiais (`RF-09-140`, `RN-09-61`,
      `RF-09-13`, design — decisões 2, 3 e 7)
- [ ] 1.3 `trilhas/rotas.py`: `materiais` em `CriarMissaoEntrada`, `CorrigirMissaoEntrada`
      (docstring dos campos atualizada) e `MissaoSaida`, com `_saida_da_missao` preenchendo
      (`RF-09-140`, design — decisão 4)
- [ ] 1.4 `equipes/rotas.py`: `missao_materiais` no item da programação do encontro
      (`RF-04-79`, design — decisão 5)

## 2. App 09

- [ ] 2.1 `trilhas/api.ts`: `materiais` no tipo da missão e nos corpos de `criarMissao` e
      `corrigirMissao` (`RF-09-140`)
- [ ] 2.2 `FormularioDeMissao.tsx`: campo "Materiais necessários para a aula", com acrescentar,
      remover, dica de exemplos, abertura com o gravado na correção e envio só quando mudou;
      `ListaDeMissoes.tsx` mostra os materiais na linha, sem rótulo quando vazia (`RF-09-140`,
      `RN-09-61`, design — decisão 6)

## 3. App 01

- [ ] 3.1 `api/programacao.ts` e `trilhas/TelaDaProgramacao.tsx`: `missao_materiais` no item e a
      lista "Materiais para a aula" junto da missão, antes do conteúdo, sem rótulo quando vazia
      (`RF-04-79`, `RF-04-35`)

## 4. Testes

- [ ] 4.1 `backend/tests/test_missao.py`: criação com materiais aparados, sem materiais (lista
      vazia) e com item vazio (422) (`RF-09-140`, `RN-09-61`)
- [ ] 4.2 `backend/tests/test_missao_corrigida.py`: correção só dos materiais em trilha
      publicada (substitui e mantém a situação), lista vazia apaga, nulo e item vazio dão 422,
      Admin recebe 403; publicação sem materiais confere só as travas antigas (`RF-09-140`,
      `RN-09-61`, `RN-09-56`)
- [ ] 4.3 `backend/tests/test_duplicacao_de_trilha.py` e `backend/tests/test_equipe_escolha.py`
      (ou o arquivo que já cobre `GET /v1/equipes/{id}/missao`): a cópia traz os materiais; a
      programação devolve `missao_materiais` (`RF-09-13`, `RF-04-79`)
- [ ] 4.4 `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`: acrescentar e mandar na criação,
      abrir com o gravado e remover na correção, item em branco não entra, linha sem rótulo
      quando vazia (`RF-09-140`)
- [ ] 4.5 `apps/app-01-aula-presencial/src/trilhas/trilhas.test.tsx`: programação com e sem
      materiais (`RF-04-79`)

## 5. Documentação

- [ ] 5.1 Documento 11 §2.2: linha **Materiais** na tabela "Toda missão declara"; documento 09
      §1: a decisão de 2026-11-10 em "Já decididos", com o pré-requisito da trilha registrado
      como descartado
- [ ] 5.2 PRD-09: `RF-09-140` em §6.1, `RN-09-61` em §7, `materiais` em `Missao` (§8), o campo
      nas linhas de `POST /v1/trilhas/{id}/missoes` e `PATCH /v1/missoes/{id}` (§9) e a linha
      de §15; PRD-04: `RF-04-79` em §6, a linha de `GET /v1/equipes/{id}/missao` (§9) e a de
      §15. `docs/prds/index.md`, doc 99 e `mkdocs.yml` não mudam
- [ ] 5.3 `openspec/cronograma-de-fatias.md`: fatia 30 do PRD-09 como implementada
