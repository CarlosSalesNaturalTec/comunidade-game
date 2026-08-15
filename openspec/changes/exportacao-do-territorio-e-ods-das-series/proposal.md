## Why

**PRD de origem:** PRD-08 — Comunidades Virtuais e dados do território. Oitava fatia dele e
vigésima quarta da esteira, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-08-19` (exportação de dados agregados e anonimizados por
comunidade e período), `RF-08-27` (a exportação a instituições declara a contribuição à meta
17.18 e o período coberto), `RF-08-26` (o painel público da comunidade exibe a cobertura de ODS
das **suas séries**, agregada por ciclo), com `RN-08-12`, `RN-08-13`, `RN-08-22`, `RN-08-24` e
`RF-08-28` recaindo sobre as duas saídas novas.

A fatia anterior abriu a série pública e **parou na leitura**. O que ela entregou responde a
quem navega; não responde a quem precisa **levar o dado embora** — o pesquisador, o gestor
público, a instituição que vai usar a série num estudo. O documento 04 §4 diz o que a
plataforma de fato entrega à Agenda 2030: "dado local, desagregado, datado e de guarda
permanente sobre um território periférico". Enquanto o dado só se lê na tela, essa afirmação
não tem arquivo que a sustente.

`RF-08-26` entra junto porque **é a mesma conta**. A cobertura de ODS existe hoje no núcleo,
mas apurada apenas pelas trilhas em que há Resultado registrado — a coleta não a alimenta. O
desafio de coleta já herda a etiqueta ODS desde a fatia do tipo e do desafio (`RF-08-25`), e
essa etiqueta **não tem nenhum leitor**: a cobertura da comunidade ignora as séries que a
própria comunidade produziu. `RF-08-27` precisa exatamente dessa conta para declarar a que
objetivo o conjunto exportado serve, de modo que separá-las faria a mesma agregação nascer
duas vezes.

O documento 04 §4 já nomeia o indicador de cobertura que falta: "séries de coleta ativas por
ODS, com o tempo em que se mantiveram".

## What Changes

- Nasce a **exportação pública do território**: rota que devolve, em **CSV**, a série agregada
  de uma comunidade num período, com **uma tabela por arquivo e cabeçalho declarado**, na forma
  que o documento 03 §12.3 fixa (`RF-08-19`).
- A exportação sai acompanhada de um **dicionário de dados**, que descreve cada campo, a
  unidade, a cadência e a origem (`RF-08-19`, documento 03 §12.3).
- O conjunto declara a licença **CC BY-SA** e a **contribuição à meta 17.18**, com o **período
  coberto** explícito (`RF-08-27`, documento 03 §12.3, documento 04 §4).
- A exportação herda **integralmente** as guardas da leitura pública: agrega até o **bairro**,
  não leva coletor, aplica o **piso de três coletores distintos** com subida ao nível acima e
  suprime o recorte que não o alcança nem no topo (`RN-08-12`, `RN-08-13`, `RF-08-28`,
  `RN-08-24`).
- A **cobertura de ODS da comunidade passa a somar as séries de coleta**: aos objetivos vindos
  das trilhas com Resultado juntam-se os dos **desafios de coleta com série aberta** na
  comunidade (**BREAKING** para quem já lesse a rota de cobertura — a resposta pode crescer;
  no Ciclo 01 nenhuma aplicação a consome ainda) (`RF-08-26`).
- A cobertura continua **agregada por comunidade e ciclo, nunca por Guerreiro(a)**, e a
  etiqueta continua **descritiva** — não pontua, não é poder (`RN-08-21`, `RN-08-22`).

### Fora do escopo

O que o PRD-08 §3.2 já exclui segue excluído — importação de fontes públicas, GPS por
coordenada, interface das telas e escolha do banco de séries. Além disso, e por recorte desta
fatia:

| Fica para                          | Porque                                                        |
| ---------------------------------- | ------------------------------------------------------------- |
| `RF-08-13`, `RN-08-09`, `RN-08-20` | auditoria e invalidação: travadas pela contradição do estorno |
| `RF-08-18`                         | consulta do responsável pela App 07: é PRD-13                 |
| `RF-08-20`                         | crescimento visual do painel: é frontend, documento 11 §8.3   |
| `RN-08-19`                         | despersonalização por revogação do consentimento              |
| mídia do registro em público       | o PRD-08 §11 a condiciona à auditoria, que ainda não existe   |

A **entrega do conjunto abaixo do bairro**, mediante solicitação aprovada por Admin (documento
03 §12.3, `RN-08-13`), **não entra**. Nenhum `RF` do PRD-08 declara essa rota — `RF-08-19` é a
exportação **agregada**, que o PRD-08 §9 marca como **pública** —, e a capacidade
`fila-de-avaliacao` já grava que "conjunto não sai sem aprovação registrada" sem que exista a
superfície que o libera. Construí-la exigiria decidir o que o Admin aprova exatamente e como o
conjunto chega ao solicitante: vira pergunta ao fundador, não suposição.

O **GeoJSON** que o documento 03 §12.3 prevê também fica de fora, e por impossibilidade, não por
recorte: o PRD-08 §3.2 exclui o georreferenciamento por coordenada do Ciclo 01, de modo que
**não há geometria** a exportar. O tratamento está no `design.md`.

## Capabilities

### New Capabilities

- `exportacao-do-territorio`: a saída do dado do território em arquivo — a exportação pública em
  CSV da série agregada de uma comunidade por período, com uma tabela por arquivo e cabeçalho
  declarado; o dicionário de dados que descreve campo, unidade, cadência e origem; a licença
  CC BY-SA, a declaração da contribuição à meta 17.18 e o período coberto; e a herança
  integral das guardas da leitura pública — corte no bairro, ausência de coletor e piso de
  três coletores distintos.

### Modified Capabilities

- `etiqueta-ods`: a cobertura por comunidade passa a ter **duas fontes**. O requisito vigente a
  define como a união das etiquetas das trilhas em que há Guerreiro(a) daquela comunidade com
  Resultado registrado; passa a valer que a ela se soma a união das etiquetas dos **desafios de
  coleta com série aberta** por Guerreiro(a) daquela comunidade. Os demais eixos — trilha, poder
  e ciclo — não mudam, e a proibição de agregar por Guerreiro(a) continua inteira (`RF-08-26`,
  `RF-08-25`, `RN-08-22`).
- `leitura-publica-da-vitrine`: a rota pública de cobertura de ODS passa a refletir a fonte
  nova, sem mudar o contrato — segue agregada por comunidade e ciclo, e segue sem qualquer
  recorte por Guerreiro(a) (`RF-08-26`, `RF-01-43`).

## Impact

- `backend/src/nucleo/coletas/`: a serialização em CSV da agregação que a fatia anterior já
  produz, reusando a resolução do local publicado e a apuração do piso sem reescrevê-las.
- `backend/src/nucleo/ods/regra.py`: a cobertura por comunidade ganha a segunda fonte, vinda do
  desafio de coleta com série aberta.
- `backend/src/nucleo/comunidades/rotas.py`: a rota de exportação da comunidade.
- `backend/src/nucleo/configuracao.py`: o rótulo da licença e o texto da declaração da meta
  17.18, se a implantação precisar declará-los — nunca embutidos no código.
- `backend/tests/`: CSV com cabeçalho declarado e uma tabela por arquivo; dicionário de dados
  cobrindo todo campo exportado; período coberto e meta 17.18 na saída; piso de três coletores
  valendo igual na exportação; nenhum coletor no arquivo; cobertura de comunidade somando
  trilha e coleta; comunidade só com coleta cobrindo o objetivo do desafio; cobertura sem
  recorte por Guerreiro(a).
- `docs/`: nenhuma decisão de produto nova — o formato, a licença, a aprovação e a meta 17.18
  já estão nos documentos 03 §12.3 e 04 §4. Muda apenas `docs/prds/index.md`, na nota de
  situação do PRD-08. O documento 99 não muda.

## Perguntas que seguem com o fundador

As três da fatia anterior continuam abertas — o estorno versus `RF-01-57`, o "a conferir" e os
indicadores do `GET /comunidades`. Esta fatia acrescenta uma:

4. **Como o conjunto abaixo do bairro chega a quem teve a solicitação aprovada.** O documento 03
   §12.3 e `RN-08-13` garantem que ele existe e que só sai com aprovação de Admin, mas nenhum
   `RF` declara a rota, o formato da entrega nem o que exatamente o Admin aprova como recorte.
