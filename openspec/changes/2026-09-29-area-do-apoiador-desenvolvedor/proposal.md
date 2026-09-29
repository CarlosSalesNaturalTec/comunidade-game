# Proposal

Origem: **PRD-03 — App 06: Vitrine pública**, **fatia 8** do
`openspec/cronograma-de-fatias.md` ("Área do Apoiador Desenvolvedor").

Atende `RF-03-67` a `RF-03-77`, `RN-03-29` a `RN-03-32` e `RN-03-35`.

## Why

A porta de quem quer construir sobre a API não existe. O núcleo já aceita a solicitação de
chave (`POST /v1/solicitacoes-de-chave`) e a apresentação da URL (`POST /v1/chaves/{id}/url`),
mas nenhuma tela leva a elas, e a rota que falta — `POST /v1/assistente-do-desenvolvedor` — é
o que faz o visitante entender a plataforma antes de pedir a chave. Sem esta fatia, o
desenvolvedor de terceiro chega à vitrine e não encontra caminho nenhum, e o `RF-03-67` a
`RF-03-77` ficam inteiros em aberto — é a última fatia do PRD-03.

## What Changes

- **Rota nova no núcleo**: `POST /v1/assistente-do-desenvolvedor`, pública e sem credencial de
  persona, sobre o adaptador Gemini que `backend/src/nucleo/assistente/` já traz (`RF-03-70`,
  `RN-03-31`). Nada é gravado: a consulta do Desenvolvedor não cria `ConsultaAoAssistente`
  nem qualquer outra linha (PRD-03 §8).
- **Corpus montado pela esteira**: a documentação de `docs/`, o README da raiz e o contrato
  OpenAPI do núcleo viram um artefato de blocos gerado a cada implantação, sem requisição a
  terceiro no momento da resposta (documento 03 §8, decisão do fundador de 2026-09-26).
- **Seção nova na App 06** — a Área do Apoiador Desenvolvedor, em endereço próprio, reunindo
  as quatro coisas do `RF-03-67`: assistente de chat, link da documentação MkDocs, link do
  repositório e formulário de solicitação de chave. Leva também a tela de apresentar a URL
  (`RF-03-77`), os dois prazos (`RF-03-75`) e a declaração sobre a chave (`RF-03-76`).
- **Freio por origem sobre a rota do assistente** (decisão do fundador de 2026-09-29): a
  superfície entra no freio do `RN-03-08`, ao contrário do formulário de chave, que segue sem
  ele (`RN-03-35`).
- **Três decisões novas** do fundador, de 2026-09-29, descidas pelo fluxo da hierarquia de
  autoridade antes do código — documento 03 §8, documento 09 §1 e depois o PRD-03: o
  **recorte do corpus por pergunta com teto**, o **freio por origem** na rota do assistente e a
  **abertura como texto fixo da aplicação**.

Fora do escopo, como o PRD-03 §3.2 já exclui: emitir chave, avaliar a solicitação e a tela da
fila — atos de Admin na App 03 (`RN-03-32`) —, e qualquer autenticação de visitante.

## Capabilities

### New Capabilities

- `assistente-do-desenvolvedor`: a consulta pública ao assistente da Área do Apoiador
  Desenvolvedor — corpus fechado montado pela esteira, recorte por pergunta com teto, recusa
  declarada fora do corpus, pergunta de múltipla escolha ao fim de toda mensagem, nenhum dado
  do visitante pedido ou guardado, e a indisponibilidade que não derruba a área.

### Modified Capabilities

- `aplicacao-da-vitrine`: a Área do Apoiador Desenvolvedor como seção da vitrine — as quatro
  partes do `RF-03-67`, os prazos de 7 e 30 dias, a declaração de que a API não responde sem
  chave e de que a chave não amplia direito, o formulário de chave sem espera crescente e a
  área utilizável com o assistente fora do ar.
- `protecao-das-rotas-publicas`: a consulta ao assistente do Desenvolvedor passa a ser
  superfície do freio por origem, contada em separado das demais.

## Impact

- **Núcleo** (`backend/`): módulo novo sob `src/nucleo/assistente/` para o assistente do
  Desenvolvedor — porta, adaptadores local e Gemini, regra e rota —, o leitor do artefato de
  corpus e a inclusão da rota nas superfícies do freio por origem. Nenhuma entidade nova e
  nenhuma migração.
- **Esteira** (`.github/workflows/backend-deploy.yml` e o script que ela chama): passo novo
  que monta o artefato de corpus a partir de `docs/`, do `README.md` da raiz e do OpenAPI
  gerado pelo próprio núcleo.
- **App 06** (`apps/app-06-vitrine/`): pasta nova da área, com a tela, o chat, o formulário de
  chave e a tela de apresentação da URL; novos caminhos em `navegacao/caminhos.ts` e as
  chamadas em `api/solicitacoes.ts`.
- **Documentação**, no mesmo PR: documento 03 §8 e documento 09 §1 com as três decisões novas,
  o PRD-03 com o que elas mudam, `docs/prds/index.md` e a linha da fatia 8 no
  `openspec/cronograma-de-fatias.md`.
