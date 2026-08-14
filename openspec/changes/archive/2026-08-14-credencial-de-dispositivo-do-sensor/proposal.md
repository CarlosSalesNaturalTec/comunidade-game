## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Décima nona fatia da esteira, na ordem do
documento 99 §9.

**Requisitos atendidos:** `RF-01-67` (Admin ou Mestre emite credencial de dispositivo,
vinculada ao Guerreiro(a) e à série, com o segredo devolvido uma única vez), `RF-01-68` na sua
metade de revogação por ato (com motivo e autoria), `RN-01-53` (a credencial é o próprio
registro do aparelho, e entre as ativas há uma por par de identificador e série), e do PRD-08
`RF-08-14` (registro de sensor autenticado por credencial de dispositivo, com a origem gravada)
e `RN-08-23` (a credencial é do aparelho, não abre sessão nem lê dado).

É a **última dívida do PRD-01**. O `docs/prds/index.md` carrega hoje uma exceção declarada por
escrito — o PRD-01 segue "implementado" com `RF-01-67` e `RF-01-68` de fora, porque nasceram
depois da implementação. Fechá-la devolve a entrega nº 1 do documento 99 §9 ao estado inteiro
que a entrega nº 2 pressupõe.

A fatia anterior abriu a porta e disse por onde ela se fecha. `RN-01-53` prende a credencial ao
par de identificador e série, e a série passou a existir naquela entrega; a rota de registro
gravou a **origem** e deixou `sensor` recusada com 422, apontando por identificador para esta
fatia. É o Robô Educa da trilha entrando na série que o Guerreiro(a) construiu para alimentar.

## What Changes

- Nasce a **credencial de dispositivo**, quarto tipo da `Credencial` que o PRD-01 §8 já prevê,
  com **série vinculada** e **trilha em que o aparelho foi construído** (`RF-01-67`).
- A emissão é ato de **Admin ou do Mestre autor do desafio** da série, e devolve o
  **identificador** e o **segredo**, este uma única vez, guardando apenas o resumo
  criptográfico — a mesma forma que a chave de aplicação já exige (`RF-01-67`, `RN-01-35`).
- Entre as credenciais ativas há **uma por par de identificador e série**: o aparelho que
  alimenta mais de uma série tem uma credencial por série, todas com o mesmo identificador, e
  nunca duas vivas para a mesma série (`RN-01-53`).
- A credencial **não amplia direito**: NEVER abre sessão, NEVER lê dado algum e só grava
  registro na série a que está presa (`RN-08-23`, `RN-01-34`).
- Admin ou o Mestre autor do desafio **revoga** a credencial, com **motivo e autoria**; a
  chamada seguinte é recusada (`RF-01-68`).
- A origem **`sensor`** deixa de ser recusada na gravação de registro e passa a exigir a
  credencial. O registro guarda o **dispositivo** que o gravou, atributo que o PRD-08 §8 já
  declara (`RF-08-14`).
- O registro de origem sensor segue todas as regras do registro que a fatia anterior entregou —
  hora da medição distinta da hora do envio, faixa esperada do tipo, imutabilidade, comunidade
  vigente na data e crédito ao Poder do Território. A credencial muda **quem autentica**, nunca
  o que vale para a medição.

### Por que a queda ao fim do vínculo não entra aqui

`RF-01-68` tem duas metades. A primeira — revogação por ato, com motivo e autoria — é desta
fatia. A segunda — a credencial cair ao **fim do vínculo do Guerreiro(a)** — fica para depois,
e a razão é que **o marco não existe no núcleo**.

O documento 03 §12.2 define fim do vínculo como pedido do responsável ou 12 meses sem nenhuma
atividade registrada. Nenhuma das duas vias está implementada: a do pedido do responsável é do
PRD-13, que trata dos pedidos do titular, e a dos 12 meses exigiria declarar o que conta como
"atividade registrada" — critério que nenhum documento define e que um artefato do OpenSpec não
pode inventar. Levado ao fundador, ficou decidido entregar agora só a revogação por ato.

Cuidado que a fatia seguinte herda: `VinculoJogador.data_fim` **não** é esse marco. Ele é o
vínculo com a **Comunidade Virtual**, e usá-lo mataria a credencial numa transferência entre
comunidades — que é outra coisa, e está fora do Ciclo 01 por `RF-08-03`.

### Fora do escopo

O que o PRD-01 §3.2 já exclui. Além disso, do próprio PRD-01 e do PRD-08:

| Fica para                          | Porque                                                       |
| ---------------------------------- | ------------------------------------------------------------ |
| `RF-01-68`, metade do fim do vínculo | o marco não existe no núcleo; ver acima                    |
| `RF-08-10`, `RF-08-11`             | ciclo de vida da série: interrupção, retomada, encerramento  |
| `RF-08-13`                         | invalidação e estorno, com a amostra semanal do Mestre       |
| `RF-08-22` a `RF-08-24`            | solicitação de local: superfície de avaliação própria        |
| `RF-08-16`, `RF-08-19`, `RF-08-20` | painel público e exportação agregada                         |
| `RF-08-17`, `RF-08-18`             | consulta das séries pelo Guerreiro(a) e pelo responsável     |
| `RF-08-26`, `RF-08-27`             | cobertura de ODS e meta 17.18                                |
| `RF-08-28`, `RN-08-24`             | piso de três coletores: vale na saída publicada              |
| `RN-08-19`                         | despersonalização por revogação do consentimento             |

A calibração do sensor não é requisito desta fatia nem de outra: o PRD-08 §14 já registra que o
sensor descalibrado não era pendência própria — o valor fora da faixa entra "a conferir", venha
de digitação ou de sensor, e cai na auditoria por amostragem do Mestre.

## Capabilities

### New Capabilities

- `credencial-de-dispositivo`: a credencial do sensor construído pelo Guerreiro(a) — emissão
  por Admin ou pelo Mestre autor do desafio, com identificador, segredo devolvido uma única vez
  e a trilha em que o aparelho foi construído; a unicidade por par de identificador e série
  entre as ativas; a conferência a cada chamada, sem sessão; o que ela NEVER faz — abrir
  sessão, ler dado, escrever fora da série a que está presa; e a revogação com motivo e
  autoria.

### Modified Capabilities

- `registro-de-coleta`: a origem `sensor` deixa de ser recusada. O requisito vigente aceita
  apenas `manual` e `voz` e recusa `sensor` com 422 "enquanto essa credencial não existir";
  passa a valer que a origem `sensor` é gravada quando a chamada se autentica por credencial de
  dispositivo, que o registro guarda o **dispositivo** que o gravou, e que a autoria continua
  sendo a do **coletor da série** a que a credencial está presa — nunca do aparelho
  (`RF-08-14`, `RN-08-23`, `RN-08-11`).
- `permissoes-e-escopo-de-comunidade`: a exigência de persona na escrita ganha a sua única
  exceção declarada. O requisito vigente recusa toda escrita sem credencial de persona, ainda
  que a chamada traga chave de aplicação vigente; passa a valer que a **credencial de
  dispositivo** grava registro na série a que está presa sem sessão de persona, e que a escrita
  por ela **continua gravando autoria** — a do Guerreiro(a) coletor a que a credencial está
  vinculada, com o papel dele. A exceção alcança **essa única operação** e nenhuma outra
  (`RF-08-14`, `RN-08-23`, `RF-01-03`, `RN-01-34`).

## Impact

- `backend/src/nucleo/personas/`: a `Credencial` ganha o tipo `dispositivo`, a série vinculada,
  a trilha do aparelho e os campos de revogação — revogada por, motivo e data — que o PRD-01 §8
  já declara para toda credencial.
- `backend/src/nucleo/autenticacao.py`: a conferência da credencial de dispositivo, por chamada
  e sem sessão, ao lado da conferência de persona.
- `backend/src/nucleo/coletas/`: a rota de registro passa a aceitar a autenticação por
  dispositivo, e o `RegistroDeColeta` aponta para a credencial que o gravou.
- `backend/src/nucleo/permissoes.py`: as operações de emissão e revogação, escopadas a Admin e
  ao Mestre autor do desafio, e a exceção de escrita por dispositivo.
- `backend/src/nucleo/principal.py`: as rotas de emissão e revogação.
- `backend/alembic/`: migração das colunas novas da `Credencial` e do `RegistroDeColeta`, e a
  troca do índice único de credencial descrita no `design.md`.
- `backend/tests/`: emissão por Admin e pelo Mestre autor, recusa do Mestre que não é autor,
  segredo devolvido uma vez e nunca recuperável, duas credenciais vivas para a mesma série
  recusadas, mesmo identificador em séries distintas aceito, registro de origem sensor com
  autoria do coletor, credencial de outra série recusada, credencial revogada recusada na
  chamada seguinte, e a credencial que não abre sessão nem lê dado.
- `docs/`: a decisão do Mestre autor do desafio, gravada no documento 03 §1.1, registrada no
  documento 09 e aplicada ao PRD-01 §§6 e 13; e `docs/prds/index.md`, de onde sai a exceção
  declarada do `RF-01-67`/`RF-01-68`, substituída pela nota da metade de `RF-01-68` que fica.
  O documento 99 não muda — nenhuma relação entre documentos foi alterada.

## Decisão que esta fatia recebeu

Uma ambiguidade apareceu ao recortar a fatia e foi levada ao fundador, porque não se resolve
dentro de um artefato do OpenSpec. Ela percorre o fluxo — documento 03 §1.1, documento 09 e
PRD-01 — antes de a change virar código.

**Qual Mestre emite a credencial.** O documento 03 §1.1 e o documento 09 dizem "emitidos por
**Admin ou Mestre**", sem qualificar qual Mestre. Mas a série pertence a um desafio de uma
trilha que tem Mestre autor, e o PRD-08 §9 já recusa com 403 a invalidação de registro por
Mestre que não é o autor do desafio. Aplicar a letra deixaria um Mestre emitir credencial de
sensor numa série de trilha alheia — mais largo que o padrão vigente do domínio.

**Decisão: emite e revoga o Admin ou o Mestre autor do desafio** da série a que a credencial se
vincula. Alinha a credencial ao escopo que o Mestre já tem sobre a própria trilha, e é
restrição, não ampliação: nada que o documento 03 §1.1 permitia a um Admin muda.
