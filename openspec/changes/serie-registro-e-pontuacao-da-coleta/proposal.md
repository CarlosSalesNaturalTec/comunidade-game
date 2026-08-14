## Why

**PRD de origem:** PRD-08 — Comunidades Virtuais e dados do território. Terceira fatia dele e
décima oitava da esteira, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-08-07` (Guerreiro(a) abre série individual), `RF-08-08` (registra
medição com valor, data e hora da medição e origem), `RF-08-09` (crédito por registro válido ao
Poder do Território), `RF-08-12` (valor fora da faixa entra "a conferir"), `RF-08-15` (a hora da
medição é distinta da hora do envio), `RF-08-21` (foto ou vídeo como o próprio registro),
`RN-08-03`, `RN-08-04`, `RN-08-05`, `RN-08-06`, `RN-08-10`, `RN-08-11`, `RN-08-15`, `RN-08-17` e
`RN-08-25`.

É o verbo pelo qual o PRD-08 existe. As duas fatias anteriores montaram tudo o que a coleta
consome — a comunidade, o local, o catálogo de tipos e o desafio — e pararam antes da medição.
Sem a série não há registro; sem o registro não há dado de território, e os invariantes 6 e 7 do
documento 99 §6 — a coleta obrigatória em toda trilha e a guarda permanente com o coletor
identificado — não têm sobre o que recair.

Ela também abre o caminho da credencial de dispositivo. `RF-01-67` e `RF-01-68` são a última
dívida do PRD-01, e `RN-01-53` os prende ao par de identificador e série: a série que eles
exigem nasce aqui.

## What Changes

- Nasce a **série de coleta**, individual e aberta pelo Guerreiro(a) sobre um desafio e um local
  cadastrado da sua comunidade, com a cadência herdada do desafio (`RF-08-07`, `RN-08-04`).
- A abertura da série **confere o teto de granularidade da comunidade**, que a criação do
  desafio deixou passar de propósito (`RN-08-25`, PRD-08 §5.3).
- Nasce o **registro de coleta**, com valor, unidade, data e hora da medição, data e hora do
  registro e origem. Nasce **válido** (`RF-08-08`, `RN-08-09` na sua metade de abertura).
- O registro aceita **foto ou vídeo como o próprio registro**, sem valor numérico, quando o tipo
  de coleta declara essa forma (`RF-08-21`).
- Valor fora da faixa esperada do tipo é **aceito e gravado**, marcado "a conferir" — venha de
  digitação ou de sensor (`RF-08-12`).
- O registro é **somente inserção**: valor, data da medição e coletor nunca mudam, e o vínculo
  com o coletor é permanente (`RN-08-10`, `RN-08-11`, PRD-08 §8).
- O registro pertence à **comunidade vigente do Guerreiro(a) na data da medição** (`RN-08-03`).
- O registro válido **credita ao Poder do Território** o valor do documento 11 §5, sem teto por
  período, respeitando quantos registros do mesmo período o desafio declara que pontuam
  (`RF-08-09`, `RN-08-05`, `RN-08-06`, `RN-08-15`).
- Nenhum jogo credita ponto de coleta: o crédito nasce do registro (`RN-08-17`, invariante 8).

### A correção do `RF-08-15`

O PRD-08 contradiz a sua própria fonte, e o nível 1 vence. O documento 03 §7 é normativo:

> O registro de coleta exige rede: sem ela, fica bloqueado até reconectar. Não há fila local
> como a da presença do App 01.

O documento 09 registra a mesma decisão em "Já decididos". O PRD-08 guardou de uma redação
anterior a fila local — em `RF-08-15`, na exceção de §5.3, na descrição da rota de §9, no
requisito não funcional de §10 e no cenário de §12. **Não é decisão nova**: nada entra no
documento 09 e nada muda no documento 03. É o PRD que volta à fonte, nesta change, porque é ela
que implementa a rota.

O que sobrevive do `RF-08-15` e continua sendo requisito desta fatia é a **distinção entre a
hora da medição e a hora do envio**, que o modelo de dados de §8 já carrega em dois campos: o
Guerreiro(a) registra agora uma medição que fez antes, e é a hora da medição que vale.

### Por que o ciclo de vida da série não entra aqui

`RF-08-10` e `RF-08-11` — interrompida por dois períodos de cadência, retomada pelo registro
seguinte —, mais o encerramento pelo fim da vigência do desafio, são a fatia seguinte. Ela tem
forma própria e precedente pronto: a change `ciclo-de-vida-da-chave-de-terceiro` decidiu que
transição por decurso de prazo **se decide na leitura e é persistida no mesmo ato**, porque o
Ciclo 01 roda sem agendador. A série abre `ativa` e assim permanece nesta fatia.

### Por que a auditoria não entra aqui

`RF-08-13` e `RN-08-09`, `RN-08-16` e `RN-08-20` — a amostra semanal do Mestre, a invalidação
com motivo e o estorno — são a mesma fatia do ciclo de vida ou a seguinte. O que esta entrega é
o registro que **nasce válido** e a marca "a conferir" que alimenta aquela amostra.

### Fora do escopo

O que o PRD-08 §3.2 já exclui: importação de fontes públicas de dados; georreferenciamento por
coordenada de GPS; interface das telas de coleta; escolha do banco de séries temporais.

O que é do PRD-08 mas de outra fatia:

| Fica para                          | Porque                                                    |
| ---------------------------------- | --------------------------------------------------------- |
| `RF-08-10`, `RF-08-11`             | ciclo de vida da série: interrupção, retomada, encerramento |
| `RF-08-13`                         | invalidação e estorno, com a amostra semanal do Mestre     |
| `RF-08-22` a `RF-08-24`            | solicitação de local: superfície de avaliação própria      |
| `RF-08-16`, `RF-08-19`, `RF-08-20` | painel público e exportação agregada                       |
| `RF-08-17`, `RF-08-18`             | consulta das séries pelo Guerreiro(a) e pelo responsável   |
| `RF-08-26`, `RF-08-27`             | cobertura de ODS e meta 17.18                              |
| `RF-08-28`, `RN-08-24`             | piso de três coletores: vale na saída publicada            |
| `RN-08-12`, `RN-08-13`             | anonimização e corte no bairro: valem na saída             |
| `RN-08-19`                         | despersonalização por revogação do consentimento           |

Do PRD-01, `RF-01-67` e `RF-01-68` — a credencial de dispositivo — ficam para a fatia que vem
depois desta, agora que a série que os define passa a existir. `RF-08-14`, o registro de origem
sensor, os acompanha: esta fatia grava a **origem** do registro, e a origem `sensor` só se torna
alcançável quando houver credencial que a autentique.

## Capabilities

### New Capabilities

- `serie-de-coleta`: a série individual do Guerreiro(a) sobre um desafio e um local da sua
  comunidade — abertura, conferência do teto de granularidade, cadência herdada e o estado
  `ativa` com que nasce. É um coletor por série, e a série é de quem está na sessão, nunca do
  aparelho.
- `registro-de-coleta`: a medição gravada na série — valor e unidade, ou mídia como o próprio
  registro; hora da medição distinta da hora do envio; origem; a marca "a conferir" para o que
  cai fora da faixa esperada do tipo; e a imutabilidade que só deixa a situação evoluir.

### Modified Capabilities

- `pontos-niveis-e-badges`: ganha a fonte de crédito da coleta. O requisito vigente credita
  ponto regular por trilha ou poder e nunca o debita; passa a valer que o registro válido
  credita ao **Poder do Território** o valor do documento 11 §5, recorrente e sem teto por
  período, limitado a quantos registros do mesmo período de cadência o desafio declara que
  pontuam — e nunca ao poder da trilha em que o desafio nasceu (`RF-08-09`, `RN-08-05`,
  `RN-08-06`, `RN-08-15`).

## Impact

- `backend/src/nucleo/coletas/`: a pasta que a fatia anterior deixou pronta recebe a
  `SerieDeColeta`, o `RegistroDeColeta` e as rotas de escrita do Guerreiro(a).
- `backend/src/nucleo/pontuacao/`: a regra de crédito da coleta ao Poder do Território, ao lado
  das que já creditam resultado, quiz e criação original.
- `backend/src/nucleo/locais/`: nada muda no modelo; a série é quem confere o nível do local
  contra o teto da comunidade e a granularidade exigida do desafio.
- `backend/src/nucleo/comunidades/`: leitura do vínculo vigente do Guerreiro(a) na data da
  medição e do teto de granularidade.
- `backend/src/nucleo/armazenamento/`: a mídia do registro por foto ou vídeo.
- `backend/src/nucleo/permissoes.py`: as operações de escrita da série e do registro, escopadas
  ao Guerreiro(a) dono da série.
- `backend/src/nucleo/principal.py`: as rotas novas no roteador de coletas.
- `backend/alembic/`: migração das duas tabelas, com a de registros **particionada por tempo**,
  como manda o documento 03 §1.
- `backend/tests/`: abertura da série, recusa fora da comunidade e acima do teto de
  granularidade, registro com hora de medição anterior ao envio, mídia como registro, valor
  fora da faixa marcado "a conferir", crédito ao Poder do Território, o segundo registro do
  período que não pontua e a recusa de edição e de exclusão do registro.
- `docs/`: a correção do `RF-08-15` no PRD-08 §§6, 5.3, 9, 10, 12 e 15. O PRD-08 segue
  **aprovado** em `docs/prds/index.md` até a sua última fatia, e o documento 99 não muda —
  nenhuma relação entre documentos foi alterada.

## Pergunta ao fundador antes das specs

Uma só, e ela trava `RF-08-09`: **como o núcleo identifica o Poder do Território?**

`RN-08-15` manda creditar a coleta ao Poder do Território e **não** ao poder da trilha em que o
desafio nasceu. Mas o poder é catálogo cadastrado por Admin (`RF-01-62`), com nome livre — o
documento 02 §2 nomeia o Poder do Território entre os demais, e a tabela `poder` de hoje tem
`nome`, `descricao`, `natureza` e `vigencia`, nada que diga "é este".

Isso não se resolve dentro de um artefato do OpenSpec, e não é o mesmo que os parâmetros que a
documentação deixa de propósito para a operação declarar: é um vínculo que a regra de negócio
exige e o modelo ainda não expressa. A resposta muda o desenho — marcar o poder no catálogo,
declarar o identificador na implantação ou semeá-lo — e por isso vem antes das specs.
