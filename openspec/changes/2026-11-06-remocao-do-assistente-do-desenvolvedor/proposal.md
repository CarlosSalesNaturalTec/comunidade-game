# Proposal

**PRD de origem:** PRD-03 — Vitrine pública (App 06). **Fatia:** nenhuma numerada — linha "—"
nova no bloco do PRD-03 do `openspec/cronograma-de-fatias.md`, como as demais correções por
decisão do fundador. **Desfaz** parte da fatia 8 (`2026-09-29-area-do-apoiador-desenvolvedor`).

**Identificadores:** retira `RF-03-68`, `RF-03-69`, `RF-03-70`, `RF-03-71`, `RF-03-72`,
`RF-03-81`, `RN-03-30`, `RN-03-31`, `RN-03-38` e `RN-03-39`; **muda o enunciado** do
`RF-03-67`; preserva `RF-03-73` a `RF-03-77`, `RN-03-29`, `RN-03-32` e `RN-03-35`.

## Why

Duas decisões do fundador de 2026-11-06:

1. **Sai o assistente de chat da Área do Apoiador Desenvolvedor** ("Converse com o
   assistente") — remoção completa: tela da App 06, rota do núcleo, corpus montado na esteira e
   superfície do freio. Acaba o custo de modelo pago numa rota aberta sem login.
2. **A seção "Documentação e código" ganha o link da documentação da API em Swagger**, a
   interface que o núcleo já publica fora de `/v1`, aberta e sem chave (documento 09,
   "Documentação da API em OpenAPI"). É ela que passa a responder "como a API funciona" a quem
   chega sem chave.

Decisão nova desce pelo fluxo antes do código: documento 03 §8 → documento 09 → PRD-03 →
change.

## What Changes

- **Documentação (antes do código):** documento 03 §8, linha "Acesso das aplicações de
  terceiros" do documento 09 com a decisão de 2026-11-06, PRD-03 (enunciado do `RF-03-67`,
  retirada dos `RF`/`RN` acima e as §§3, 4, 5.8, 8, 9, 11, 12, 13 e 15 que citam o
  assistente), menções de uma frase no documento 08 e nos PRDs 11 e 12, `README.md` da raiz, e a
  linha nova do cronograma.
- **App 06:** a Área do Apoiador Desenvolvedor passa a reunir **quatro coisas** — link da
  documentação (MkDocs), **link da documentação da API (Swagger)**, formulário de chave e link
  do repositório. Saem o chat, a mensagem de abertura e a consulta ao núcleo; sai a linha
  "Conversa com o assistente do Desenvolvedor" da área detalhada de coleta; textos da seção de
  abertura e da área deixam de citar o assistente.
- **Núcleo — BREAKING:** sai `POST /v1/assistente-do-desenvolvedor` (passa a 404), com a porta,
  os adaptadores local e Gemini, a regra e a configuração do assistente do Desenvolvedor; sai o
  módulo `corpus_do_desenvolvedor` e a superfície `assistente_do_desenvolvedor` do freio por
  origem. O assistente de trilhas e o adaptador Gemini compartilhado ficam.
- **Esteira e imagem:** sai o passo "Montar o corpus do assistente do Desenvolvedor" de
  `backend-deploy.yml`, o `COPY` do corpus no `Dockerfile` e a entrada no `.gitignore`.
- **Semeadura do institucional:** o rascunho semeado de "Construir sobre a plataforma" deixa
  de prometer o assistente.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: a área reúne documentação, Swagger, formulário e repositório; saem
  os requisitos do chat (abertura, múltipla escolha, conversa não guardada, assistente fora do
  ar); a área detalhada deixa de citar a conversa.
- `assistente-do-desenvolvedor`: todos os requisitos são retirados — a capacidade deixa de
  existir.
- `protecao-das-rotas-publicas`: a consulta ao assistente deixa de ser superfície do freio por
  origem; a solicitação de chave segue sem freio.

## Impact

- **API:** `POST /v1/assistente-do-desenvolvedor` deixa de existir. Consumidor conhecido: só a
  App 06, que sai junto. O schema OpenAPI perde a rota.
- **Código:** `backend/src/nucleo/assistente/desenvolvedor/`,
  `backend/src/nucleo/corpus_do_desenvolvedor/`, `principal.py`, `configuracao.py`,
  `protecao/freio.py`, `conteudo_institucional/semeadura.py`, três arquivos de teste e o
  `conftest.py`; na App 06, `desenvolvedor/`, `api/desenvolvedor.ts`, `coleta/AreaDetalhada.tsx`,
  `descoberta/enderecos.ts` e dois testes.
- **Esteira:** `.github/workflows/backend-deploy.yml`, `backend/Dockerfile`, `.gitignore`.
- **Configuração:** a App 06 já declara `VITE_URL_DO_NUCLEO`; o link do Swagger deriva dela,
  sem variável nova.
- **Custo:** cessa o consumo de Gemini pela Área do Desenvolvedor.
