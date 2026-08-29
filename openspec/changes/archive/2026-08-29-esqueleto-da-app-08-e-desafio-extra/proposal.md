# Esqueleto da App 08 e desafio extra

Origem: **PRD-14 — App 08: Área do Apoiador**, §§4, 6.1, 6.4 e 8. **Fatia 1** do PRD-14 no
`openspec/cronograma-de-fatias.md`.

Atende `RF-14-08` a `RF-14-11`, `RF-14-29` a `RF-14-39`, `RF-14-74` a `RF-14-76`, `RN-14-02`,
`RN-14-04`, `RN-14-13` a `RN-14-20` e `RN-14-41`; do PRD-07, `RF-07-15` e `RF-07-41`.

## Why

A entidade `DesafioExtra` é a única peça que falta a **três fatias já recortadas e paradas**: a
15 do PRD-02 (aprovação do Admin), a 15 do PRD-09 (validação do Mestre) e a 8 do PRD-05 (o
desafio na Área do Guerreiro(a)). Nenhuma delas pode nascer antes dela, e o PRD-14 §8 é quem a
define — por isso o cronograma põe o PRD-14 na frente.

Quem propõe o desafio é o Apoiador, e ele ainda não tem porta: das oito aplicações, a App 08 é
a única sem pasta. O núcleo já a espera — a chave `app-08-apoiador` está semeada, a
`sessao-do-adulto` já abre sessão de Apoiador e trava a senha provisória, e a matriz de
permissões já dá a ele a operação `propostas_de_desafio_extra`. Falta o cliente.

## What Changes

### A App 08 nasce, com a entrada do Apoiador (PRD-14 §§4, 6.1)

`apps/app-08-apoiador/` entra no monorepo com a esteira de CI da pasta, consumindo `comum/`
como as outras quatro aplicações: entrada por login social ou por usuário e senha (`RF-14-08`),
troca obrigatória da senha provisória antes de qualquer outra tela (`RF-14-09`), recusa de
login sem cadastro prévio com a orientação de usar o pré-cadastro (`RF-14-10`, `RN-14-02`) e
nenhuma tela de convite, delegação ou segundo acesso (`RF-14-11`, `RN-14-04`).

Nada disso é regra nova no núcleo: a `sessao-do-adulto` já decide os três casos. A fatia
entrega o cliente deles.

### A entidade `DesafioExtra` e a proposição (PRD-14 §§6.4, 8)

Nasce `backend/src/nucleo/desafios_extras/`, com os atributos que o PRD-14 §8 declara, e as
rotas que o §9 do PRD-14 dá ao Apoiador:

| Rota                        | Persona  | Atende                                        |
| --------------------------- | -------- | --------------------------------------------- |
| `POST /v1/desafios-extras`  | Apoiador | `RF-14-29` a `RF-14-34`, `RF-14-74` a `RF-14-76` |
| `GET /v1/eu/desafios-extras` | Apoiador | `RF-14-35` a `RF-14-38`                       |

O que a entidade decide nesta fatia:

- **Vínculo e conteúdo da proposta**: trilha em andamento, recompensa, quantidade disponível,
  critério de atribuição e vigência (`RF-14-29`, `RF-14-30`); pontos extras com teto de 10
  (`RF-14-74`, `RN-14-41`); formato presencial ou on-line (`RF-14-75`).
- **Modalidade**: aberto ou direcionado (`RF-14-31`); no direcionado, o nick do destinatário
  como o proponente o digitou e a justificativa do vínculo (`RF-14-32`, `RN-14-17`), sem
  confirmar existência e sem exibir dado algum do destinatário, nem na proposta nem na recusa
  (`RF-14-33`, `RN-14-18`).
- **Custeio e lastro**: por aporte do proponente ou por saldo de recurso existente
  (`RF-14-76`, `RF-07-41`); sem lastro provido a publicação é recusada, e a tela mostra o que
  falta (`RF-14-34`, `RF-07-15`, `RN-14-14`).
- **Situação e imutabilidade**: os quatro estados que o Apoiador acompanha — validação do
  Mestre, aprovação do Admin, publicado, recusado com motivo (`RF-14-35`, `RF-14-36`,
  `RN-14-13`); quantidade restante no publicado (`RF-14-37`); publicado não se edita, e a
  correção é proposta nova, com a anterior guardada no desfecho que teve (`RF-14-38`).
- **Salvaguardas**: nenhuma tela de desafio expõe nome real, contato ou dado de identificação
  de Guerreiro(a) (`RF-14-39`, `RN-14-20`), e ninguém é barrado de disputar o aberto — o que é
  limitado é a quantidade de recompensas (`RN-14-16`), sem teto de desafios simultâneos
  (`RN-14-15`). Os pontos extras correm isolados da pontuação regular (`RN-14-19`).

As **transições** de estado não entram aqui: quem valida é o Mestre (fatia 15 do PRD-09) e quem
aprova e publica é o Admin (fatia 15 do PRD-02), que traz também a reserva e a liberação da
recompensa (`RF-07-39`, `RF-07-40`). Esta fatia entrega a entidade, o estado inicial e a
leitura do proponente.

## Capabilities

### New Capabilities

- `desafio-extra`: a entidade que o PRD-14 §8 define — proposição pelo Apoiador, modalidades
  aberto e direcionado, custeio e lastro, teto de pontos, estados do fluxo, imutabilidade do
  publicado e as salvaguardas que impedem a aplicação de confirmar a existência de um nick.
- `area-do-apoiador`: a App 08 — nesta fatia, a entrada e a sessão do Apoiador, a trava da
  senha provisória e as telas da proposição e do acompanhamento do desafio extra.

### Modified Capabilities

Nenhuma. A `sessao-do-adulto` já cobre os três caminhos de entrada do adulto e a trava da senha
provisória, e a `permissoes-e-escopo-de-comunidade` já dá ao Apoiador a operação
`propostas_de_desafio_extra`: esta fatia consome as duas sem mudar requisito.

## Impact

- **Código novo**: `backend/src/nucleo/desafios_extras/` (modelo, regra, rotas) e
  `apps/app-08-apoiador/`, com a esteira de CI da pasta no mesmo PR.
- **Código lido**: `trilhas/` (trilha em andamento), `aportes/` e o saldo de recurso do
  livro-razão (lastro), `personas/` e `autenticacao` (sessão do Apoiador), `comum/` (camadas de
  acesso e visual).
- **Destrava**: a fatia 15 do PRD-02, a 15 do PRD-09 e a 8 do PRD-05.
- **Fora do escopo**, como o PRD-14 §3.2 já exclui: autocadastro do Apoiador, homologação do
  próprio aporte, aporte em material ou serviço pela aplicação, segundo usuário no mesmo
  cadastro, qualquer canal de mensagem com Guerreiro(a), família ou Mestre, e relatório fechado
  de prestação de contas. Fora desta fatia, mas dentro do PRD-14: pré-cadastro, identidade
  pública, aportes, missões do Apoiador, efetividade, favoritos, propostas e catálogo avulso —
  fatias 2 a 9.
