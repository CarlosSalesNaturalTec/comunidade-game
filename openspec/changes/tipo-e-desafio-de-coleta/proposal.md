## Why

**PRD de origem:** PRD-08 — Comunidades Virtuais e dados do território. Segunda fatia dele e
décima sétima da esteira, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-08-05` (Admin mantém o catálogo de tipos de coleta), `RF-08-06`
(Mestre cria o desafio de coleta), `RF-08-25` (desafio herda a etiqueta ODS da missão ou da
trilha), `RN-08-21` (a etiqueta da série é descritiva), `RN-08-25` (granularidade exigida livre
no desafio) e a metade do `RF-01-41` que se prende ao desafio de coleta.

A fatia anterior parou de propósito antes da medição, e nomeou esta: sem `DesafioDeColeta` não
há série, porque `RF-08-07` manda o Guerreiro(a) abrir a série **selecionando um desafio**. É o
elo que falta entre a trilha, que já existe, e tudo o que o PRD-08 ainda deve.

Ela também paga uma dívida do PRD-01. O `RF-01-41` esperava justamente esta entidade: a fatia
`etiqueta-ods` gravou a etiqueta na trilha e na missão, mas não teve para onde propagá-la. O
destino nasce aqui.

## What Changes

- Nasce o **catálogo de tipos de coleta**, cadastrado por Admin, com nome, forma de registro,
  unidade de medida e faixa esperada — mínimo e máximo (`RF-08-05`, PRD-08 §8).
- Nasce o **desafio de coleta**, criado pelo Mestre e vinculado a uma missão da sua trilha, com
  tipo escolhido no catálogo, cadência, vigência, granularidade exigida e quantos registros do
  mesmo período pontuam (`RF-08-06`, PRD-08 §§5.2, 8).
- A **granularidade exigida é livre na criação** do desafio. O teto da comunidade é conferido
  na abertura da série, que é da fatia seguinte (`RN-08-25`).
- A **etiqueta ODS passa a se propagar**: o desafio herda a da missão que o criou ou, na falta
  dela, a da trilha, como rótulo descritivo que não altera pontuação, cadência nem validade
  (`RF-08-25`, `RN-08-21`, `RF-01-41`).

### Por que a solicitação de local não entra aqui

`RF-08-22` a `RF-08-24` estavam bloqueados apenas pelo desafio de origem, que nasce nesta
fatia, e a fatia anterior os encaminhou para cá. **Decisão do fundador: viram fatia própria.**

O motivo é o achado que a fatia anterior registrou. A `fila-de-avaliacao` não os comporta — ela
exige que nenhuma solicitação crie cadastro, persona ou acesso, e `RN-08-18` manda o oposto, a
aprovação **cria** o local —, e o avaliador pode ser o Mestre da trilha, não só um Admin. É uma
superfície de avaliação nova, de tamanho próprio, e não o apêndice de uma fatia de catálogo.

### Por que a série e o registro não entram aqui

`RF-08-07` em diante são a fatia seguinte, e é lá que entram também `RF-01-67`, `RF-01-68` e
`RF-08-14` — a credencial de dispositivo do sensor. Ela se prende à série (`RN-01-53` a torna
única pelo par de identificador e série), de modo que nascer antes dela seria nascer sem o que
a define.

### Por que `RN-08-14` é declarada e não é conferida aqui

`RN-08-14` exige ao menos um desafio de coleta por trilha, e o PRD-08 §5.2 diz onde a trava
mora: a trilha só pode ser **publicada** com um. A publicação é do PRD-09, como a spec
`trilha-e-missao` já registra ao deixar lá a transição de rascunho para publicada. Mesmo
precedente da sondagem, cuja recusa é `RF-09-82`. O desafio nasce aqui; a trava que o exige é
de quem publica.

### Fora do escopo

O que o PRD-08 §3.2 já exclui: importação de fontes públicas de dados; georreferenciamento por
coordenada de GPS; interface das telas de coleta; escolha do banco de séries temporais.

O que é do PRD-08 mas de outra fatia:

| Fica para                             | Porque                                                  |
| ------------------------------------- | ------------------------------------------------------- |
| `RF-08-22` a `RF-08-24`               | solicitação de local: superfície de avaliação própria    |
| `RF-08-07` a `RF-08-13`, `RF-08-21`   | série, registro, invalidação e auditoria                 |
| `RF-08-16`, `RF-08-19`, `RF-08-20`    | painel e exportação: exigem série                        |
| `RF-08-17`, `RF-08-18`                | consulta das séries pelo Guerreiro(a) e pelo responsável |
| `RF-08-26`, `RF-08-27`                | cobertura de ODS e meta 17.18: agregam sobre séries      |
| `RF-08-28`, `RN-08-24`                | piso de três coletores: vale na saída publicada          |

`RF-08-21` merece nota: a **forma de registro** — número, foto ou vídeo — é atributo do tipo de
coleta e entra aqui, porque `RF-08-05` a exige no catálogo. Aceitar a mídia como o próprio
registro é da fatia do registro.

A metade do `RF-01-41` que propaga a etiqueta para o **desafio extra** também não entra: o
desafio extra é do PRD-14 e hoje existe só como operação em `permissoes.py`. Fecha-se aqui a
metade cujo destino existe.

## Capabilities

### New Capabilities

- `catalogo-de-tipos-de-coleta`: o catálogo do que se mede — nome, forma de registro, unidade
  de medida e faixa esperada com mínimo e máximo. É o vocabulário que o desafio consome e a
  origem da faixa que, na fatia do registro, marcará a medição estranha para auditoria.
- `desafio-de-coleta`: o desafio criado pelo Mestre dentro da sua trilha, preso a uma missão,
  com tipo, cadência, vigência, granularidade exigida e quantidade de registros que pontuam por
  período.

### Modified Capabilities

- `etiqueta-ods`: a etiqueta ganha propagação. O requisito vigente a grava na trilha e na
  missão, com a da missão prevalecendo; passa a valer que o desafio de coleta **herda** a da
  missão que o criou ou, na falta dela, a da trilha, e que essa herança é descritiva — não toca
  pontuação, cadência nem validade (`RF-01-41`, `RF-08-25`, `RN-08-21`).

## Impact

- `backend/src/nucleo/`: módulo novo `coletas/` — o `TipoDeColeta`, o `DesafioDeColeta` e as
  rotas de escrita do Mestre. É a pasta que a fatia seguinte encontra pronta para a série e o
  registro.
- `backend/src/nucleo/ods/`: a regra de herança da etiqueta pelo desafio.
- `backend/src/nucleo/trilhas/`: nada muda no modelo; o desafio é quem aponta para a missão.
- `backend/src/nucleo/permissoes.py`: a operação de escrita do desafio, escopada ao Mestre
  autor da trilha.
- `backend/src/nucleo/principal.py`: registra o roteador novo.
- `backend/alembic/`: migração das duas tabelas.
- `backend/tests/`: o catálogo, a criação do desafio pelo Mestre da trilha, a recusa do Mestre
  que não é autor dela, a herança da etiqueta pela missão e o recuo para a da trilha.
- `docs/`: as duas decisões abaixo, já gravadas antes desta change virar código — documento 02
  §1 (fonte única), documento 09 ("Já decididos") e PRD-08 §§4, 6, 7, 9, 13 e 15. O PRD-08
  segue **aprovado** em `docs/prds/index.md` até a sua última fatia.

## Decisões que esta fatia recebeu

Duas lacunas do PRD-08 apareceram ao recortar a fatia e foram levadas ao fundador, porque
nenhuma se resolve dentro de um artefato do OpenSpec. Ambas já percorreram o fluxo — documento
02 §1, documento 09 e PRD-08 — antes de a change virar código.

### 1. O catálogo de tipos de coleta é cadastrado por Admin

`RF-08-05` dizia que o **sistema mantém** o catálogo, sem atribuir persona: a tabela de §4 dava
ao Admin a comunidade e os locais e ao Mestre o desafio, sem citar o catálogo, e o §9 não tinha
rota que o criasse. **Decisão do fundador: Admin**, como os locais do território. O Mestre
escolhe um tipo do catálogo ao criar o desafio e não cria tipo novo — a mesma separação que já
vale entre quem cadastra o local e quem o seleciona.

`RF-08-05` passou a nomear o Admin, o §4 ganhou o cadastro no que o Admin faz e a criação de
tipo no que o Mestre não pode, e o §9 ganhou a rota `POST /tipos-de-coleta`.

### 2. A granularidade exigida é livre no desafio

O PRD-08 §5.1 chama o atributo da comunidade de **granularidade máxima permitida**, o que soava
como teto, mas nenhuma regra mandava recusar o desafio que o excedesse. Por baixo da dúvida
havia uma tensão de alcance: a spec `trilha-e-missao` estabelece que a **trilha publicada
alcança todas as comunidades**, de modo que não existe uma comunidade única contra a qual
conferir o teto quando o Mestre cria o desafio.

**Decisão do fundador: livre na criação.** O teto vale na **abertura da série** — o Guerreiro(a)
só abre a sua se a comunidade dele alcançar o nível exigido. Nasceu o `RN-08-25`, e a conferência
é da fatia da série, não desta.
