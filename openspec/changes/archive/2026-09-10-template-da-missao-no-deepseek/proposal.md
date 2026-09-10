# Template da missão no DeepSeek

Origem: **PRD-09** (fatia 12, `Template da missão por IA` — `RF-09-85`, `RF-09-86`,
`RF-09-91`). A fatia está `implementado` e **não está no ar**: a chamada ao Gemini volta `429`
por falta de crédito. Esta change aplica ao código a decisão que o documento 03 §1.12 já
registra desde 2026-09-10 — o modelo é escolhido por funcionalidade, e o que é só texto vai
para o DeepSeek. Não abre fatia nova: linha sem número no bloco do PRD-09.

## Why

O Gemini deixou de ter _free tier_ para conta nova e passou a exigir crédito pré-pago:

```json
{"code": 429, "message": "Your prepayment credits are depleted.", "status": "RESOURCE_EXHAUSTED"}
```

O template da missão é a única das três portas de IA que manda **só texto**, e por isso é a que
a decisão já autoriza a mover. `producoes` e `assistente` seguem no Gemini, porque leem imagem
e áudio, que o DeepSeek não faz — a visão dele é experimental e limitada a 384 tokens por
imagem, insuficiente para transcrever manuscrito de criança.

Três defeitos de diagnóstico apareceram no caminho e entram junto, porque a próxima falha de
provedor — qualquer provedor — vai passar exatamente por eles:

1. **O corpo da resposta é descartado no erro de HTTP.** O `raise_for_status` levanta com a
   linha de status, e a `HTTPStatusError` não carrega o corpo. O Google vinha dizendo, por
   extenso, "modelo indisponível para contas novas, use gemini-3.6-flash" e depois "créditos
   esgotados"; o adaptador jogou as duas frases fora, e cada uma custou uma rodada de
   investigação.
2. **A credencial vaza no log.** O Gemini a recebe na _query string_, e a URL inteira entra na
   mensagem da exceção, que o `logger.warning(..., exc_info=True)` despeja no Cloud Logging em
   texto claro. O DeepSeek usa `Authorization: Bearer`, o que resolve o caso dele — mas o
   `producoes` e o `assistente` seguem no Gemini e seguem vazando.
3. **`%` no DSN derruba o Job de migração.** O `alembic/env.py` passa a URL por
   `config.set_main_option`, que interpola com `configparser`: qualquer `%` levanta `invalid
   interpolation syntax`. O DSN de produção hoje não tem `%`, então não é defeito ativo — mas o
   README já avisa que `/` e `+` quebram a análise do DSN, e este é o terceiro caractere da
   lista, não documentado. Entra por decisão do fundador (2026-09-10).

## What Changes

- `template_de_missao/nuvem.py` fala com `https://api.deepseek.com/chat/completions`, no
  formato compatível com OpenAI, autenticando por `Authorization: Bearer`. Usa
  `response_format={"type": "json_object"}`, que o DeepSeek oferece e o Gemini não tinha — a
  resposta deixa de vir embrulhada em cerca de código.
- `CG_DEEPSEEK_CHAVE_DE_API` e `CG_DEEPSEEK_MODELO` na configuração; a chave vem do Secret
  Manager (`cg-deepseek-api-key`), o modelo do deploy, no critério já aplicado ao Gemini.
- **O corpo da resposta entra no log** nos três adaptadores, truncado, quando o erro é de HTTP.
- **A credencial nunca entra no log**: o adaptador do Gemini passa a mandar a chave no
  cabeçalho `x-goog-api-key`, e a URL deixa de conter segredo.
- `alembic/env.py` escapa `%` ao declarar a URL.
- Nenhuma mudança de rota, de contrato ou de comportamento visível.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

Nenhuma. `template-da-missao` especifica que o Mestre envia o tópico e recebe estrutura e
lacunas, e que a indisponibilidade vira aviso em linguagem simples — tudo segue valendo palavra
por palavra. Trocar o provedor de um adaptador não é comportamento: `skip_specs: true`.

## Impact

| Área | O que muda |
| --- | --- |
| `backend/src/nucleo/configuracao.py` | as duas variáveis do DeepSeek |
| `backend/src/nucleo/template_de_missao/{nuvem,fabrica}.py` | o adaptador passa a ser o DeepSeek |
| `backend/src/nucleo/{producoes,assistente}/nuvem.py` | corpo no log, chave no cabeçalho |
| `backend/alembic/env.py` | escape de `%` |
| `.github/workflows/backend-deploy.yml` | `CG_DEEPSEEK_MODELO` em `--set-env-vars` |
| `backend/README.md` | variáveis, provisionamento e a tabela de causas |

Fora do repositório, a cargo do fundador: acrescentar
`CG_DEEPSEEK_CHAVE_DE_API=cg-deepseek-api-key:latest` ao `GCP_SECRETOS_CG`. O segredo já
existe.
