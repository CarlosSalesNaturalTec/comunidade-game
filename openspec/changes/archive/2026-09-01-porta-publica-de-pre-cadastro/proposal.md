# Porta pública de pré-cadastro

Origem: **PRD-14 — App 08: Área do Apoiador**, §§3.1, 5.1, 6.1, 9 e 11. **Fatia 2** do PRD-14
no `openspec/cronograma-de-fatias.md`.

Atende `RF-14-01` a `RF-14-07`, `RN-14-01`, `RN-14-03`, `RN-14-05`, `RN-14-06`, `RN-14-39` e
`RN-14-40`.

## Why

Quem quer sustentar o projeto não tem por onde entrar. A App 08 nasceu na fatia 1 inteiramente
autenticada, e o cadastro do Apoiador é ato de Admin (`RN-14-01`): sem a porta pública, ninguém
de fora consegue nem declarar o aporte que já transferiu. O núcleo já espera esse pedido — a
rota pública `POST /v1/solicitacoes-de-participacao` guarda aporte declarado, comprovante e
nick, com freio por origem —, mas nenhuma tela o alcança.

## What Changes

### A App 08 ganha a porta pública, antes da entrada (PRD-14 §§5.1, 6.1)

- Quem chega sem sessão vê a porta pública: o que é a Área do Apoiador, o pré-cadastro e o
  caminho de entrada de quem já tem cadastro (`RF-14-01`).
- Identificação **sem documento**: nome ou razão social, e-mail, WhatsApp, nick pretendido e o
  **perfil declarado** — pessoa física ou jurídica (`RF-14-01`, `RN-14-03`, `RN-14-39`).
- Três formas de declarar o aporte: **necessidade publicada**, **valor sugerido** da escada do
  perfil e **valor livre**, cada valor com o equivalente em moedas na mesma tela (`RF-14-02`,
  `RF-14-03`, `RN-14-40`). A quarta forma — **missão aberta** — entra com a fatia 5, quando a
  entidade `MissaoDoApoiador` existir: decisão do fundador de 2026-09-01.
- **Comprovante obrigatório** em PDF, JPG ou PNG, com o núcleo recusando formato fora da lista
  (`RF-14-04`, `RN-14-05`, `RN-14-06`).
- A tela declara, antes do envio, que o pré-cadastro **não cria cadastro nem acesso**, que a
  plataforma não emite recibo e que um Admin vai conferir o comprovante (`RF-14-05`,
  `RN-14-01`).
- Repetição da mesma origem cai no freio que o núcleo já aplica, e a tela mostra o tempo de
  espera em linguagem simples (`RF-14-06`).
- Quem apoia **sem transferir dinheiro** — material, serviço ou divulgação — é encaminhado ao
  formulário da vitrine (`RF-14-07`, `RN-14-05`).
- **Fora desta fatia:** o aviso de coleta que o PRD-14 §11 pede na porta pública é o
  `RF-14-58`, do recorte da fatia 8 — a porta nasce sem ele e o ganha lá.

### O núcleo guarda o perfil declarado e confere o formato do comprovante (PRD-14 §§9, 11)

- `SolicitacaoDeParticipacao` passa a guardar o **perfil** declarado na pretensão de Apoiador,
  dado que o PRD-14 §11 manda reter e a gestão acessa (`RF-14-01`, `RN-14-39`). O atributo
  entra na linha da entidade no PRD-01 §8, que hoje não o lista: decisão do fundador de
  2026-09-01.
- O comprovante enviado em formato fora de PDF, JPG ou PNG é recusado com **422** e a lista dos
  formatos aceitos, como o PRD-14 §9 prevê (`RF-14-04`, `RN-14-06`).

## Capabilities

### New Capabilities

Nenhuma. A porta pública é superfície da App 08 e o pré-cadastro já é capacidade do núcleo.

### Modified Capabilities

- `area-do-apoiador`: a App 08 deixa de ser inteiramente autenticada — ganha a porta pública
  com o pré-cadastro, a escada por perfil, o comprovante obrigatório, a declaração de que nada
  ali cria acesso e o encaminhamento de quem apoia sem dinheiro.
- `fila-de-avaliacao`: a solicitação de participação passa a carregar o **perfil declarado** e
  a recusar comprovante em formato não aceito.

## Impact

- `apps/app-08-apoiador/`: porta pública nova antes da entrada, com o formulário de
  pré-cadastro e o encaminhamento à vitrine; `.env.example` ganha o endereço do formulário da
  vitrine, vazio no Ciclo 01 até a App 06 existir.
- `backend/src/nucleo/fila/`: atributo `perfil` na `SolicitacaoDeParticipacao`, conferência do
  formato do comprovante e o perfil na saída que a gestão lê.
- Nenhuma mudança de rota: `POST /v1/solicitacoes-de-participacao` e
  `GET /v1/vitrine/necessidades` já existem, ambas públicas sob chave de aplicação.
- `docs/prds/prd-01-backend-api.md` §8 e `openspec/cronograma-de-fatias.md`.
