# Tarefas — chave do Gemini em produção

Recorte em `proposal.md`; decisões em `design.md`. Nenhum requisito muda: as tarefas atendem em
operação os `RF-09-91`, `RN-04-21` e `RN-05-35` já implementados — o aviso de indisponibilidade
deixa de ser o único desfecho possível em produção.

## 1. Configuração

- [x] 1.1 Em `backend/src/nucleo/configuracao.py`, renomear
  `template_de_missao_gemini_chave_de_api` para `gemini_chave_de_api` e
  `template_de_missao_gemini_modelo` para `gemini_modelo`, preservando os padrões (`""` e
  `"gemini-2.5-flash"`). Refazer o comentário do bloco: a dupla serve as três funcionalidades
  de IA do Ciclo 01, não só o template da missão (documento 03 §1.12; design — decisão 1).

## 2. Fábricas

- [x] 2.1 Apontar as três fábricas para os campos novos e corrigir o _docstring_ de cada uma,
  que hoje diz "a mesma chave e o mesmo modelo do `template_de_missao`" — passa a nomear a
  chave única do Gemini (design — decisão 1): `template_de_missao/fabrica.py`,
  `producoes/fabrica.py`, `assistente/fabrica.py`.

## 3. Log das causas mudas

- [x] 3.1 Em `template_de_missao/nuvem.py`, `producoes/nuvem.py` e `assistente/nuvem.py`,
  acrescentar `logger.warning` no ramo da chave ausente, antes do `try`, e na recusa de
  formato, onde o validador devolve `None` de dentro do `try`. Manter o `logger.warning` de
  exceção que já existe e o retorno `None` em todos os caminhos — a indisponibilidade não pode
  virar exceção (`RF-09-91`, `RN-04-21`, `RN-05-35`; design — decisão 3). As mensagens são as
  que a tabela do README traduz: chave ausente e resposta fora do formato esperado.

## 4. Esteira

- [x] 4.1 Em `.github/workflows/backend-deploy.yml`, declarar `CG_GEMINI_MODELO` em
  `--set-env-vars`, ao lado de `CG_AMBIENTE`, nas **duas** etapas — Job de migração e serviço
  —, com o valor em `env:` no topo do workflow (design — decisão 2).

## 5. Testes

- [x] 5.1 Cobrir os dois caminhos mudos do adaptador de nuvem em cada módulo — chave ausente
  e resposta fora do formato esperado devolvem `None` **e** emitem a linha de log esperada
  (`caplog`) — no _logger_ do módulo (design — decisão 3). Só `assistente` tem hoje arquivo
  de porta de nuvem; os outros dois não têm cobertura nenhuma do adaptador de produção:
  acrescentar os cenários a `test_assistente_porta.py`, criar
  `test_template_de_missao_porta.py` no molde dele e acrescentar um bloco de nuvem a
  `test_producao_da_missao_porta.py`.
- [x] 5.2 Cobrir a escolha da fábrica com os campos novos: em `ambiente="producao"` as três
  devolvem o adaptador de nuvem construído com `gemini_chave_de_api` e `gemini_modelo`; fora de
  produção, o adaptador local. Guarda a renomeação contra ponto de leitura esquecido (design —
  Risks).

## 6. Documentação

- [x] 6.1 Em `backend/README.md`: acrescentar `CG_GEMINI_CHAVE_DE_API` e `CG_GEMINI_MODELO` à
  lista de variáveis com valor padrão, dizendo que a dupla serve as três funcionalidades de IA
  e que sem a chave elas respondem o aviso de indisponibilidade; incluir a chave no passo 3 do
  provisionamento (Secret Manager e `GCP_SECRETOS_CG`), com a nota de restringir a API Key à
  Generative Language API; registrar que o modelo vai por `--set-env-vars`, não por segredo
  (design — decisões 1 e 2).
- [x] 6.2 Em `backend/README.md`, acrescentar a seção de diagnóstico "Quando a sugestão, a
  leitura ou a resposta do assistente não vêm", com o comando de leitura do log e a tabela
  sinal → causa do `design.md` — decisão 4, no mesmo padrão da tabela de `chave_invalida`.
- [x] 6.3 Registrar a change em `openspec/cronograma-de-fatias.md`: linha sem número no bloco
  do PRD-09, com o slug `chave-do-gemini-em-producao`. Nada muda em `docs/`, em
  `docs/prds/index.md`, no documento 99 nem na `nav` do `mkdocs.yml` — a change não toma
  decisão nova (o documento 03 §1.12 já decidiu Gemini), não altera requisito de PRD e não cria
  arquivo em `docs/`.
