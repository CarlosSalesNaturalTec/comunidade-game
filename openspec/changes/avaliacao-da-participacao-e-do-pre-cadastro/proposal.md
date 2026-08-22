## Why

**Origem: PRD-02**, com `RF-02-18`, `RF-02-19`, `RF-02-20`, `RF-02-65`, `RF-02-83`, `RF-02-84`
e `RF-02-85`, e `RF-02-86` em parte. Do núcleo, atende `RF-01-25`, `RN-01-49`, `RN-01-03` e
`RN-01-28`; do PRD-07, consome `RF-07-30` e `RN-07-21`, já implementados.

O PRD-02 §6.2 é o maior bloco intocado do PRD em curso, e a fila de participação é a porta por
onde entra gente na plataforma: candidato a Mestre, candidato a Apoiador com pré-cadastro e
aporte declarado. Sem ela, quem chega pela vitrine fica onde caiu.

O que falta não é regra — é superfície, a mesma forma da fatia
`agenda-da-aula-e-ponto-de-apoio`. A capacidade `fila-de-avaliacao` já define o ciclo comum
das quatro naturezas — situação, prazo de 7 dias, quem avaliou, parecer e data do desfecho — e
`backend/src/nucleo/fila/regra.py` já implementa `avaliar_solicitacao_de_participacao` e
`esta_em_atraso`. **Nenhuma rota as alcança:** os únicos chamadores em toda a árvore são
`tests/test_fila.py` e `tests/conftest.py`. As quatro rotas de entrada existem; nenhuma de
leitura, nenhuma de desfecho.

O mesmo vale para a homologação do pré-cadastro: `POST /aportes` já aceita
`solicitacao_de_participacao_id`, já recusa homologar a mesma declaração duas vezes e já credita
pela vigência da data do aporte. O Admin não tem de onde ver a solicitação que homologaria.

## What Changes

- **`GET /solicitacoes-de-participacao`**: fila paginada, restrita a Admin, com nome, e-mail,
  WhatsApp, pretensão, apresentação, instituição e links, o **atraso derivado** de
  `esta_em_atraso` — nunca gravado — e o **pré-cadastro do Apoiador** com o aporte declarado
  (`RF-02-18`, `RF-02-65`, `RF-02-83`, `RF-01-28`).
- **`POST /solicitacoes-de-participacao/{id}/avaliacao`**: desfecho de Admin — aceita ou
  recusada, com parecer, autor e data. **Nenhum cadastro, persona ou acesso nasce daqui**
  (`RF-02-19`, `RF-02-86`, `RN-01-03`, `RN-01-28`).
- **Área "Filas" na App 03**: lista unificada com **filtro por natureza**, decidida pelo
  fundador em 2026-08-22. O esqueleto do filtro nasce nesta fatia com uma natureza só —
  participação; as outras três entram na fatia seguinte. As quatro rotas do PRD-02 §9 seguem
  separadas: a unificação é composição da tela, não rota nova.
- **Desfecho na tela**: aceitar abre o cadastro de Mestre ou Apoiador **pré-preenchido**, sem
  criar acesso, reaproveitando os formulários que a change `cadastro-de-personas` entregou
  (`RF-02-20`).
- **Homologação do pré-cadastro na tela**: o Admin registra o aporte declarado apontando a
  solicitação. Nenhuma rota nova — `POST /aportes` já faz (`RF-02-84`, `RF-07-30`, `RN-07-21`).

Nenhuma rota de escrita existente muda. `POST /solicitacoes-de-participacao` e `POST /aportes`
ficam como estão.

### O que fica para depois — e por quê

Nada disto é exclusão nova: o PRD-02 §3.1 mantém tudo em escopo, e a fatia apenas não alcança.

| Adiado                                        | Trava                                                          |
| --------------------------------------------- | -------------------------------------------------------------- |
| Exibir e julgar o comprovante (`RF-02-83`)    | nenhuma rota devolve arquivo guardado — change própria         |
| Recusa por comprovante ilegível (`RF-02-86`)  | mesma trava: o desfecho existe, o julgamento visual não        |
| Card do Apoiador na vitrine (`RF-02-85`)      | a vitrine não tem rota de Apoiador — é PRD-03                  |
| As outras três naturezas da fila              | fatia seguinte, `avaliacao-de-dados-de-chave-e-de-sugestao`    |

O comprovante é **fatia própria** por decisão do fundador em 2026-08-22: a porta de
armazenamento tem `ler()` sem nenhum chamador HTTP, e a escolha entre servir o arquivo pelo
núcleo autenticado ou por URL assinada do bucket é do documento 03, não deste PRD. Enquanto ela
não vier, `RF-02-83` fecha na identificação e no aporte declarado, e `RF-02-86` fecha no
desfecho com motivo — não na legibilidade.

### Decidido pelo fundador em 2026-08-22

**`RF-02-93` está duplicado no PRD-02** — §6.2 linha 222 (*critério de aprovação da solicitação
de dados*) e §6.5 linha 304 (*amostra semanal de coleta*), com enunciados diferentes; a §15
rastreia só o primeiro. O de **§6.5 recebe identificador novo**, e o de §6.2 mantém `RF-02-93`.
Não alcança esta fatia — a correção do PRD entra com a fatia seguinte, que implementa o
requisito de §6.2.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `fila-de-avaliacao`: a natureza **participação** ganha **superfície de leitura e de
  desfecho**. A capacidade hoje define o ciclo comum, o prazo e a garantia de que nada cria
  cadastro — e silencia sobre quem lê a fila e sob que credencial o desfecho se registra.
- `aplicacao-de-gestao`: a App 03 ganha a **área Filas**, a quinta área da aplicação, com o
  filtro por natureza e o encaminhamento da solicitação aceita ao cadastro pré-preenchido.

## Impact

**Backend** — só adição, nenhuma migração:

- `backend/src/nucleo/fila/rotas.py` — `GET /solicitacoes-de-participacao` e
  `POST /solicitacoes-de-participacao/{id}/avaliacao`
- `backend/src/nucleo/fila/regra.py` — `avaliar_solicitacao_de_participacao` e
  `esta_em_atraso` passam a ser consumidas, não alteradas

**App 03** — `apps/app-03-gestao/`: área nova, consumindo a camada de `comum/react/`. Os
formulários de Mestre e Apoiador de `src/personas/` passam a aceitar valores iniciais vindos da
solicitação; nenhum deles muda de contrato.

**Documentação** — `docs/09-topicos-em-aberto-e-sugestoes.md` §1 recebe a duplicidade de
`RF-02-93` como pendência de correção do PRD. Nenhuma decisão nova de produto é tomada por esta
change.
