# Chave do Gemini em produção

Origem: **PRD-09** (fatia 12, `Template da missão por IA` — `RF-09-85` a `RF-09-91`),
**PRD-04** (fatia 10, `Assistente de trilhas no encontro` — `RF-04-36` a `RF-04-40`) e
**PRD-05** (fatia 7, `Produção da missão, devolutiva e retomada` — `RF-05-74` a `RF-05-77`). As
três já estão `implementado` no `openspec/cronograma-de-fatias.md`: esta change **não abre
fatia nova** e não altera requisito nenhum — provisiona em produção a credencial de que as três
dependem. Entra no cronograma como linha sem número no bloco do PRD-09, no precedente de
`2026-08-20-implantacao-da-app-03-e-do-nucleo` e
`2026-09-01-esteira-de-deploy-das-apps-07-e-08`.

## Why

As três funcionalidades de IA do Ciclo 01 estão no ar e nenhuma responde. Em produção,
`CG_TEMPLATE_DE_MISSAO_GEMINI_CHAVE_DE_API` nunca foi provisionada e mantém o valor padrão
vazio; o adaptador de nuvem devolve `None` sem chegar a chamar o Gemini, e cada tela mostra o
aviso de indisponibilidade que `RF-09-91`, `RN-04-21` e `RN-05-35` prevêem para quando o modelo
falha. O comportamento está correto — o que falta é a credencial.

Provisionar exige três correções de acompanhamento, decididas pelo fundador em 2026-09-10:

1. **O nome mente.** `template_de_missao_gemini_chave_de_api` nasceu na fatia 12 do PRD-09, mas
   `producoes/fabrica.py` e `assistente/fabrica.py` leem a mesma variável. Quem mantiver o
   mapeamento `GCP_SECRETOS_CG` não tem como saber que três funcionalidades dependem dela.
2. **O modelo não é segredo** e está no Secret Manager por arrasto. Trocar de modelo deveria
   ser uma linha do workflow, como já é `CG_AMBIENTE`.
3. **Toda causa produz a mesma tela.** Chave vazia, modelo inexistente, `403` por restrição da
   chave e resposta fora do formato caem todas no mesmo `except Exception` e no mesmo aviso.
   Sem tabela de diagnóstico, o fundador provisiona e não tem como saber se funcionou.

## What Changes

- **BREAKING (implantação):** `CG_TEMPLATE_DE_MISSAO_GEMINI_CHAVE_DE_API` passa a
  `CG_GEMINI_CHAVE_DE_API` e `CG_TEMPLATE_DE_MISSAO_GEMINI_MODELO` a `CG_GEMINI_MODELO`. Quebra
  só o ambiente que já declarasse os nomes antigos — nenhum declara, e é por isso que a change
  existe. O mapeamento em `GCP_SECRETOS_CG` nasce já com o nome novo.
- `CG_GEMINI_MODELO` sai do Secret Manager e entra em `--set-env-vars` do `backend-deploy.yml`,
  ao lado de `CG_AMBIENTE`, no serviço e no Job de migração. Mantém o padrão `gemini-2.5-flash`
  do código. A chave continua no Secret Manager, mapeada por `GCP_SECRETOS_CG`.
- `backend/README.md` ganha as duas variáveis na lista de ambiente, o passo do Secret Manager
  no provisionamento e um bloco de diagnóstico com tabela de causas, no mesmo padrão da tabela
  de `chave_invalida` que já existe.
- Nenhuma mudança de comportamento: nem rota, nem contrato, nem aviso, nem modelo de dados.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

Nenhuma. `template-da-missao`, `producao-da-missao` e `consulta-ao-assistente` já especificam o
aviso de indisponibilidade e seguem valendo palavra por palavra: a change troca nome de
variável de configuração, move um parâmetro de segredo para variável de ambiente e escreve
documentação de operação. Comportamento não muda, logo spec não muda — `skip_specs: true` no
`.openspec.yaml`.

## Impact

| Área | O que muda |
| --- | --- |
| `backend/src/nucleo/configuracao.py` | os dois campos renomeados, com o comentário refeito |
| `backend/src/nucleo/{template_de_missao,producoes,assistente}/fabrica.py` | as três chamadas passam a ler os campos novos |
| `.github/workflows/backend-deploy.yml` | `CG_GEMINI_MODELO` em `--set-env-vars`, nas duas etapas |
| `backend/README.md` | variáveis, provisionamento e tabela de causas |
| `openspec/cronograma-de-fatias.md` | linha sem número no bloco do PRD-09 |

Fora do repositório, a cargo do fundador no console do GCP: criar a API Key restrita à
Generative Language API, criar o segredo no Secret Manager e acrescentar o mapeamento
`<segredo>:CG_GEMINI_CHAVE_DE_API` ao segredo de repositório `GCP_SECRETOS_CG`. IAM não muda —
`nucleo-runtime` já tem `roles/secretmanager.secretAccessor` no projeto.

Sem dependência de outra change. Não toca `docs/`: não há decisão nova a gravar em
documento-fonte nem no documento 09 — o documento 03 §1.12 já decidiu Gemini para todo o Ciclo
01, e esta change apenas o aplica.
