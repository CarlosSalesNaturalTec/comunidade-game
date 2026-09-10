# Tarefas — template da missão no DeepSeek

Recorte em `proposal.md`; decisões em `design.md`. Nenhum requisito muda: as tarefas fazem
`RF-09-85`, `RF-09-86` e `RF-09-91` voltarem a funcionar em produção, com o provedor que o
documento 03 §1.12 destina ao texto.

## 1. Configuração e esteira

- [x] 1.1 Em `backend/src/nucleo/configuracao.py`, acrescentar `deepseek_chave_de_api` (padrão
  vazio, vem do Secret Manager) e `deepseek_modelo` (padrão `deepseek-v4-flash`), no bloco e no
  padrão de comentário das do Gemini (design — decisão 1).
- [x] 1.2 Em `.github/workflows/backend-deploy.yml`, declarar `CG_DEEPSEEK_MODELO` em
  `--set-env-vars`, nas duas etapas, com o valor em `env:` — nome de modelo não é segredo.

## 2. Adaptador do template da missão

- [x] 2.1 Em `template_de_missao/nuvem.py`, falar com
  `https://api.deepseek.com/chat/completions` no formato de _chat completions_: `messages`,
  `response_format={"type": "json_object"}`, `Authorization: Bearer` e o modelo da
  configuração. Manter o `_INSTRUCAO`, o `_extrair_json`, o `_validar_estrutura` e o contrato
  da porta — muda quem responde, não o que a porta devolve (`RF-09-85`, `RF-09-86`; design —
  decisões 1 e 2).
- [x] 2.2 Em `template_de_missao/fabrica.py`, ler `deepseek_chave_de_api` e `deepseek_modelo`,
  e refazer o _docstring_: esta porta deixa de compartilhar credencial com as outras duas.

## 3. Diagnóstico dos três adaptadores

- [x] 3.1 Nos três `nuvem.py`, distinguir `httpx.HTTPStatusError` das demais exceções e
  registrar o `status_code` e um recorte do corpo da resposta, que é onde o provedor explica a
  causa. Manter o retorno `None` em todos os caminhos — a indisponibilidade não pode virar
  exceção (`RF-09-91`, `RN-04-21`, `RN-05-35`; design — decisão 3).
- [x] 3.2 Em `producoes/nuvem.py` e `assistente/nuvem.py`, mandar a chave do Gemini no
  cabeçalho `x-goog-api-key` em vez de `?key=` na URL, para que nenhuma mensagem de exceção
  carregue credencial ao log (design — decisão 4).

## 4. Escape de `%` na migração

- [x] 4.1 Em `backend/alembic/env.py`, escapar `%` ao declarar a URL em `set_main_option`:
  `configparser` a interpola, e qualquer `%` no DSN levanta `invalid interpolation syntax` e
  derruba o Job de migração (design — decisão 5; decisão do fundador, 2026-09-10).

## 5. Testes

- [x] 5.1 Em `backend/tests/test_template_de_missao_porta.py`, refazer os cenários para o
  DeepSeek: sem chave devolve `None` e registra; erro de transporte, demora e formato recusado
  seguem devolvendo `None` com a linha esperada; resposta válida devolve a estrutura. Somar a
  asserção de que a requisição leva `Authorization: Bearer` e **não** leva a chave na URL, e de
  que o corpo do erro de HTTP aparece no log (design — decisões 3 e 4).
- [x] 5.2 Em `test_producao_da_missao_porta.py` e `test_assistente_porta.py`, cobrir o
  cabeçalho `x-goog-api-key`, a ausência da chave na URL e o corpo do erro no log.
- [x] 5.3 Em `backend/tests/test_portas_do_gemini.py`, ajustar a escolha das fábricas: o
  template da missão passa a ler a dupla do DeepSeek, e as outras duas seguem na do Gemini.
- [x] 5.4 Em `backend/tests/test_migracoes.py`, cobrir que um DSN com `%` sobe as migrações sem
  `invalid interpolation syntax`.

## 6. Documentação

- [x] 6.1 Em `backend/README.md`: acrescentar `CG_DEEPSEEK_CHAVE_DE_API` e `CG_DEEPSEEK_MODELO`
  à lista de variáveis, dizendo qual porta cada dupla serve; incluir `cg-deepseek-api-key` no
  passo 3 do provisionamento; atualizar a tabela de causas com a linha do DeepSeek e com o fato
  de o corpo da resposta passar a aparecer no log.
- [x] 6.2 Registrar a change em `openspec/cronograma-de-fatias.md`: linha sem número no bloco
  do PRD-09, com o slug. Nada muda em `docs/` — a decisão já foi gravada no documento 03 §1.12
  e no documento 09 pelo PR anterior, e esta change apenas a aplica ao código.
