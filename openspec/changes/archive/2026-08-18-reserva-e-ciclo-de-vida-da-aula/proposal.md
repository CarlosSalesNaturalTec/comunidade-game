## Why

**PRD de origem:** PRD-07 — Economia de recursos e livro-razão. Terceira fatia dele e vigésima
nona da esteira, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-07-08` e `RN-07-01` (o agendamento reserva os recursos declarados
no ponto de apoio da aula; sem saldo ela fica **pendente de lastro**), `RF-07-09` (o lançamento
da atividade realizada converte a reserva em **baixa**; o cancelamento **libera**, e a reserva
nunca expira sozinha), `RN-07-37` (a aula pendente de lastro é confirmada pelo próprio aporte
que fecha a diferença, sem ato humano), `RN-07-36` (o débito herda o ponto de apoio da aula que
o consumiu) e `RN-07-04` (duas casas exatas). Do PRD-01 valem `RF-01-72` (cancelamento por
Admin ou por Mestre da comunidade da aula, com motivo) e `RF-01-17` (a exceção que dá ao Mestre
essa única escrita em gestão). Do PRD-02, servidos por esta fatia, `RF-02-31`, `RF-02-35` e
`RF-02-95`. `RF-01-02`, `RF-01-03`, `RF-01-16` e `RF-01-27` valem por herança do roteador e já
têm capacidade própria — esta change não os redeclara.

Esta é a fatia do **invariante 9** — nenhuma atividade acontece sem lastro. As duas anteriores
entregaram o vocabulário e o movimento de entrada: onde o recurso fica, quanto vale e como
entra. Nenhuma delas gasta coisa alguma. Aqui nasce o **consumo**, e com ele o único uso do
saldo que as duas primeiras construíram.

### O que foi decidido antes desta change

Uma lacuna foi ao fundador e voltou decidida, pelo fluxo de sempre — documento-fonte, documento
09, PRD:

**Quem confirma a aula pendente de lastro é o próprio aporte homologado que fecha a
diferença**, sem ato humano de confirmação. O documento 04 §1 e o PRD-07 §5.3 diziam apenas que
a atividade é confirmada "quando a necessidade é suprida", em voz passiva, e o `RF-02-67`
atribuía o ato à **aplicação** App 03 — o que poria a regra de lastro num frontend, contra a
ordem de autoridade. Nasce a `RN-07-37`, presa ao invariante 9, e o `RF-02-67` passa a mostrar
a confirmação em vez de executá-la.

Duas lacunas do plano de execução foram ao fundador junto com o desenho, e ficam registradas
aqui porque são coerência derivada do modelo, não regra de produto nova — o mesmo tratamento
que a fatia 1 deu à exigência de aula e ponto de apoio serem da mesma comunidade:

1. **A reserva é tudo-ou-nada.** Faltando disponível para qualquer parcela, nada é reservado —
   nem a dos tipos que tinham saldo. O `RF-07-08` não diz o que fazer com a parcela coberta, e
   o documento 04 §1 trata o lastro como bloco: a necessidade "só sai da lista quando o saldo
   fecha". Reservar em parte imobilizaria recurso numa aula que ainda não pode acontecer.
2. **O desempate entre aulas pendentes é pelo horário inicial da aula**, da mais próxima para a
   mais distante, quando um aporte fecha a falta de mais de uma e não alcança todas. Nenhum
   documento declarava a ordem, e alguma precisa existir para a confirmação automática da
   `RN-07-37` ser determinística.

Uma dúvida **não** virou decisão, porque a fonte já a respondia: de onde sai a lista de
recursos a reservar. O documento 04 §1 diz que a aula "declara o que consome e em que ponto de
apoio acontece" — é lista declarada no agendamento, não derivação da atividade prevista. A
redação do PRD-02 §5.4 é narrativa de tela, e a fonte normativa prevalece.

### O recorte, decidido com o fundador

**A fatia entrega a baixa.** `RF-07-09` é requisito do PRD-07, o PRD em curso, e sem ele a
reserva nunca vira débito e o saldo nunca desce. A baixa é o **lançamento da atividade
realizada** — o mesmo ato que registra o resultado de cada participante (documento 04 §1) —,
cuja rota `POST /aulas/{id}/lancamentos` é declarada no PRD-02 (`RF-02-35`). O backend servir
rota declarada num PRD de frontend é o normal: a ordem do documento 99 §9 governa quando a
**App 03** entra, não quem serve o contrato dela.

**A necessidade publicada fica para a fatia seguinte.** A aula que cai em pendente de lastro
não tem, nesta fatia, caminho de saída por aporte — o mesmo padrão explícito com que o `ativo`
do ponto de apoio nasceu sem operação que o mudasse, na fatia 1. `RN-07-37` entra aqui como
comportamento do aporte porque é ele que muda; a **publicação** da falta é que fica.

**Consequência do recorte: a aula ganha superfície HTTP.** `RF-07-08` diz que é o *agendamento*
que reserva, e hoje `agendar_aula()` é regra sem rota, alcançável só por teste. Sem
`POST /v1/aulas` não há por onde disparar a reserva. As quatro rotas do ciclo do lastro entram
juntas — três delas declaradas no PRD-02 §9, pela mesma razão do parágrafo acima.

## What Changes

- Nasce a **reserva**: vínculo entre a aula e uma quantidade de um tipo de recurso num ponto de
  apoio, com estado **reservada**, **consumida** ou **liberada** (PRD-07 §8). Ela não é
  lançamento — compromete saldo sem movimentá-lo.
- O **saldo disponível** passa a ser o saldo derivado dos lançamentos **menos o reservado**. O
  total derivado não muda; o que nasce é a distinção que o PRD-07 §8 já previa em
  `SaldoDeRecurso` — quantidade disponível e quantidade reservada (`RF-07-07`).
- **BREAKING** — a **aula passa a declarar os recursos que consome** e a carregar **situação**:
  prevista, pendente de lastro, confirmada, realizada ou cancelada (PRD-01 §8).
- **Agendar a aula reserva** o que ela consome, no ponto de apoio dela. Havendo saldo
  disponível para tudo, a aula nasce **confirmada**; faltando qualquer parcela, nasce
  **pendente de lastro** e nada é reservado (`RF-07-08`, `RN-07-01`).
- O **aporte homologado que fecha a diferença** de uma aula pendente de lastro **confirma a
  aula e efetiva a reserva no mesmo ato**, sem ato humano (`RN-07-37`).
- O **lançamento da atividade realizada** é ato por aula: registra o resultado de cada
  participante, converte cada reserva em **baixa** — um lançamento de débito por reserva, no
  ponto de apoio da aula — e leva a aula a **realizada** (`RF-07-09`, `RF-02-35`, `RN-07-36`).
- O **`Resultado` passa a declarar a aula** em que foi lançado. É coerência derivada do
  documento 04 §1, que já define a baixa como "o mesmo ato que registra o resultado de cada
  participante": sem a aula no resultado, o ato não tem como achar as reservas.
- **Cancelar a aula libera** as reservas, devolvendo o saldo. Cancela **Admin ou Mestre
  vinculado à comunidade da aula**, com motivo; é a primeira escrita de Mestre em gestão, pela
  exceção do `RF-01-17` (`RF-01-72`, `RF-02-95`).
- A reserva **não expira sozinha**: sai por lançamento ou por cancelamento, sempre com autor e
  momento. Aula que passa da data sem desfecho **mantém** o recurso preso (`RF-07-09`).
- Aula **realizada** ou **cancelada** não volta atrás: lançar ou cancelar duas vezes é recusado.
- Rotas: `POST /v1/aulas` (Admin, agenda e dispara a reserva), `POST /aulas/{id}/reservas`
  (gestão, caminho explícito e idempotente para retentativa ou recursos declarados depois),
  `POST /aulas/{id}/lancamentos` (Admin) e `POST /aulas/{id}/cancelamento` (Admin ou Mestre da
  comunidade) — todas sob chave de aplicação.

### Fora do escopo

O PRD-07 §3.2 já exclui empréstimo de bancada, reposição solidária, entrega de dados a
pesquisadores, o painel de efetividade do Apoiador, a interface de gestão e a contabilidade
fiscal. Nada disso volta aqui.

O que é **adiado por recorte**, não excluído:

| Fica para                                | Porque                                                             |
| ---------------------------------------- | ------------------------------------------------------------------ |
| `RF-07-27`, `RF-07-28`, `RF-07-31`       | necessidade publicada e cobertura parcial, na fatia seguinte       |
| `RF-07-18`                               | o que falta às aulas agendadas — é leitura da necessidade          |
| `RF-07-15`, `RF-07-39` a `RF-07-41`      | a reserva do **desafio extra**, que depende do PRD-14              |
| `RF-07-10`, `RF-07-16`, `RF-07-17`       | Poder Sustentador e prestação de contas, leitura derivada          |
| `RF-02-30` (atividade prevista na aula)  | campo do PRD-02 §8; o PRD-01 §8 não o dá à `Aula` do núcleo        |
| `RF-02-67`                               | é tela da App 03, não rota do núcleo                               |
| desativação de ponto de apoio            | pendência aberta no documento 09                                   |

A `Reserva` do PRD-07 §8 vincula "aula **ou** desafio extra". Só o braço da **aula** entra: o
`DesafioExtra` é entidade do PRD-14 e não existe no núcleo.

## Capabilities

### New Capabilities

- `reserva-de-recurso`: a reserva da aula sobre o saldo — os três estados, o saldo disponível
  como derivado menos reservado, e as duas únicas saídas, baixa e liberação, sem expiração.

### Modified Capabilities

- `aula-e-presenca`: a aula passa a declarar os recursos que consome e a carregar situação; o
  agendamento reserva; o cancelamento por Admin ou Mestre da comunidade libera a reserva; e o
  agendamento ganha rota.
- `resultado-de-atividade`: o `Resultado` passa a declarar a aula, e o lançamento da atividade
  realizada passa a ser ato **por aula** que converte as reservas em baixa.
- `aporte`: o aporte homologado que fecha a diferença de uma aula pendente de lastro confirma a
  aula e efetiva a reserva no mesmo ato.
- `livro-razao`: o saldo derivado passa a distinguir **disponível** de **reservado**; o total
  derivado dos lançamentos não muda.

## Impact

- `backend/src/nucleo/reservas/`: pasta nova — `modelo.py` da `Reserva`, `regra.py` da reserva,
  da baixa e da liberação.
- `backend/src/nucleo/aulas/`: `modelo.py` ganha situação e os recursos declarados; `regra.py`
  ganha o cancelamento e a reserva no agendamento; `rotas.py` nasce com as quatro rotas.
- `backend/src/nucleo/resultados/`: `modelo.py` ganha `aula_id`; `regra.py` ganha o lançamento
  por aula, que converte as reservas.
- `backend/src/nucleo/aportes/regra.py`: ao creditar, tenta fechar as aulas pendentes de lastro
  daquele tipo e ponto de apoio.
- `backend/src/nucleo/livro_razao/regra.py`: o débito da baixa e o saldo disponível.
- `backend/src/nucleo/principal.py`: registro do roteador de aulas.
- `backend/alembic/versions/`: migration com `reserva`, a situação e os recursos da `aula`, e
  `aula_id` em `resultado`.
- `backend/tests/`: reserva no agendamento, pendente de lastro sem reservar nada, confirmação
  pelo aporte que fecha a diferença, baixa que derruba o saldo, liberação por cancelamento,
  ausência de expiração e recusa de desfecho repetido.
- `docs/prds/index.md`: a narrativa da fatia entregue, na entrega.
