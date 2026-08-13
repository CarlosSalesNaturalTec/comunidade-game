## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Décima terceira fatia, na ordem do
documento 99 §9.

**Requisitos atendidos:** `RF-01-25` (participação, sugestões e propostas em fila única),
`RF-01-46` (solicitação de dados com finalidade declarada e desfecho), `RF-01-47` (conjunto
só liberado após aprovação de Admin), `RF-01-49` (registro da solicitação de chave),
`RN-01-03`, `RN-01-25`, `RN-01-28` e `RN-01-37` (nenhuma solicitação cria cadastro, persona
ou acesso), `RN-01-29` (sem CPF, CNPJ ou documento de quem aporta) e `RN-01-48` (critério
que o Admin aplica ao aprovar ou recusar a entrega de dados).

A fatia anterior entregou o freio por origem **antes** das rotas que ele protege, e o deixou
com três superfícies declaradas e nenhuma existindo: a consulta por nick, o formulário de
participação e o de dados. Esta change constrói **duas das três** — e nasce já freada, sem
emenda depois.

A fila é também a porta de entrada de quatro PRDs que vêm depois: a App 03 a avalia
(`RF-02-25`, `RF-02-26`, `RF-02-77`, `RF-02-78`), a vitrine envia os três formulários
públicos (PRD-03 §6.3), o pré-cadastro do Apoiador chega por ela (PRD-14) e as sugestões
vêm das Apps 05, 07, 08 e 09. Nenhum deles anda antes dela.

`RN-01-48` acabou de ser decidido pelo fundador: a pendência "Entrega do conjunto de dados"
foi gravada no documento-fonte (03 §12.3), movida no documento 09 e aplicada ao PRD-01, ao
PRD-02 e ao PRD-03 no commit que antecede esta change.

## What Changes

- Nasce a **fila única de avaliação**, com uma entidade por natureza de item —
  `SolicitacaoDeParticipacao`, `SolicitacaoDeDados`, `SolicitacaoDeChave` e
  `SugestaoOuProposta`, como o PRD-01 §8 as nomeia — sobre um **ciclo comum**: situação,
  prazo, quem avaliou, parecer, desfecho e data.
- Nascem as **três rotas públicas de envio** do PRD-01 §9: `POST
  /v1/solicitacoes-de-participacao`, `POST /v1/solicitacoes-de-dados` e `POST
  /v1/solicitacoes-de-chave`. As duas primeiras **declaram a superfície do freio** por
  origem entregue na fatia 12; a terceira não a declara, por `RN-01-46`.
- **Nenhuma delas cria cadastro, persona ou acesso**, e nenhuma devolve dado, arquivo ou
  chave no ato do envio (`RN-01-03`, `RN-01-25`, `RN-01-28`, `RN-01-37`). O que a
  solicitação aceita, aprovada, é **abrir o cadastro para o Admin fazer** — o ato é dele.
- O **pré-cadastro do Apoiador** entra pela solicitação de participação, com aporte
  declarado e comprovante anexado. A plataforma **não coleta CPF, CNPJ nem documento de
  identidade** (`RN-01-29`), e creditar moedas pelo aporte homologado é do PRD-07.
- **Sugestões e propostas** entram na mesma fila por rota autenticada, com autor e persona
  identificados, vindas das Apps 05, 07, 08 e 09.
- O **desfecho é ato de Admin**: aprova ou recusa com parecer, autor e data — escrita que a
  trilha de auditoria da fatia 11 já registra sozinha. Na solicitação de dados o critério é
  o de `RN-01-48`: solicitante identificado, finalidade declarada compatível com pesquisa ou
  política pública e compromisso de não tentar reidentificar ninguém.
- `RF-01-47` entra como **guarda**: nenhum conjunto de dados sai sem aprovação registrada.

### A exportação do conjunto não cabe nesta fatia

`RF-01-66` — exportar em CSV, GeoJSON e dicionário de dados — e `RN-01-47` — a licença
CC BY-SA do conjunto entregue — **não entram**, e não por recorte de conveniência: o que se
exportaria são as **séries do território**, entidades do PRD-08, que é a entrega nº 2 do
documento 99 §9 e ainda não existe. Não há conjunto a gerar. O que esta fatia entrega da
entrega de dados é o **registro do pedido, o critério e a guarda** — `RF-01-46` e
`RF-01-47`. A geração do arquivo nasce junto com as séries que ela lê.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação,
cadência de coleta e valoração de aporte; captura da imagem, conversa de cadastro e geração
do descritor no aparelho; exclusão do _template_; telemetria da Batalha de Laser e
personalização por IA.

O que é do PRD-01 mas de outra fatia:

| Fica para                           | Porque                                          |
| ----------------------------------- | ----------------------------------------------- |
| `RF-01-66`, `RN-01-47`              | as séries do território são do PRD-08           |
| `RF-01-50` a `RF-01-53`             | ciclo de vida da chave: emissão, prazo, URL e revogação |
| `RF-01-33`, `RF-01-34`, `RF-01-43`  | rotas de vitrine pública, o terceiro gancho do freio |
| `RF-01-22`, `RF-01-59`              | contrato de leitura dos jogos                   |
| `SolicitacaoDoResponsavel`          | nenhum RF do PRD-01 a nomeia; entra com o PRD-13 |

## Capabilities

### New Capabilities

- `fila-de-avaliacao`: a fila única de avaliação da gestão — as quatro naturezas de item
  sobre um ciclo comum de situação, prazo, parecer e desfecho; as três rotas públicas de
  envio que não criam cadastro nem acesso; a rota autenticada de sugestão e proposta; e o
  critério que o Admin aplica ao aprovar ou recusar a solicitação de dados.

### Modified Capabilities

Nenhuma. O freio por origem já declara em `protecao-das-rotas-publicas` que vale para os
formulários de participação e de dados — as rotas novas se prendem ao mecanismo existente,
sem mudar requisito dele. A trilha de auditoria já alcança toda escrita por middleware, e
`chave-de-aplicacao` só muda quando a **emissão** entrar, na fatia seguinte.

## Impact

- `backend/src/nucleo/fila/`: módulo novo — as quatro entidades, o ciclo comum de situação
  e desfecho, as rotas de envio e as de avaliação.
- Migração do Alembic para as quatro tabelas.
- `backend/src/nucleo/principal.py`: registra o roteador da fila.
- `backend/src/nucleo/protecao/`: as duas rotas de formulário declaram a superfície do
  freio; **nenhuma mudança no mecanismo**.
- `docs/`: nada a atualizar. A decisão da entrega de dados já entrou nos documentos 03 e 09
  e nos PRD-01, PRD-02 e PRD-03 no commit que antecede esta change. `docs/prds/index.md`
  não muda de situação: o PRD-01 segue "aprovado", fatiado em changes.

## Questões que precisam do fundador antes das `specs`

1. **Atributos de `SugestaoOuProposta`.** O PRD-01 §8 nomeia a entidade no diagrama mas é a
   única da fila **sem linha de atributos** na tabela. O PRD-05 diz que a sugestão do
   Guerreiro(a) é texto **ou áudio de até 60 segundos, transcrito** (`RF-05-54`), e o
   PRD-02 pede autor e persona identificados (`RF-02-25`). Faltam os campos e, sobretudo,
   **de quem é a transcrição do áudio** — do núcleo, da App 05 ou do PRD-11. Nenhum artefato
   do OpenSpec resolve isso.
2. **O prazo de 7 dias vale para quais naturezas?** PRD-02 §5.2 e PRD-03 `RF-03-30` fixam
   7 dias para a **solicitação de participação**. A solicitação de dados, a de chave e a
   sugestão têm prazo declarado? Se sim, qual?

## Questões que ficam para o `design.md`

1. **Uma tabela ou quatro.** O PRD-01 §8 nomeia quatro entidades com atributos próprios, mas
   o ciclo de avaliação é o mesmo nas quatro. Se o ciclo comum vira tabela-base com
   especialização, ou se cada entidade repete as colunas de situação e desfecho, é desenho
   de execução.
2. **Onde fica o comprovante anexado** do pré-cadastro do Apoiador — o Cloud Storage já está
   decidido no documento 03 §1 — e o que o núcleo guarda dele no registro.
