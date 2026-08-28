## Why

A App 03 agenda a aula, reserva os recursos e mostra o encontro em andamento — mas **não lança
nada**. O painel do dia lista a pendência `lancamento_da_atividade_realizada` desde a fatia 7 e
a spec `aplicacao-de-gestao` manda que "cada pendência leve o operador à tela que já a
resolve": essa tela nunca existiu. Enquanto ela não existe, a aula não passa a **realizada**,
a reserva não vira baixa, o Guerreiro(a) não recebe ponto pela atividade do dia e a infração
ocorrida no encontro não tem onde ser registrada.

O núcleo já entregou tudo o que sustenta a fatia: o lançamento por aula que converte reserva em
baixa (`resultado-de-atividade`), o desfecho em três valores fechados, a ocorrência de conduta
de 5 pontos com teto por aula (`ocorrencia-de-conduta`), o ponto extra do mérito por auxílio
(`ponto-extra`) e o lançamento de ajuste do livro-razão (`livro-razao`). O que falta é a ponta
de gestão.

Origem: **PRD-02**, fatia **10** do `openspec/cronograma-de-fatias.md`, §§5.6, 6.3, 7 e 9.

Requisitos atendidos: `RF-02-34`, `RF-02-36`, `RF-02-37`, `RF-02-39` e `RF-02-40`, sob
`RN-02-12`, `RN-02-13`, `RN-02-14` e `RN-02-21`. Do lado do núcleo, alcança `RF-01-20` (a
presença) e `RF-07-19` (o ajuste), pelas rotas que já existem e pelas duas que nascem aqui.

## What Changes

- A **App 03** ganha a área **Lançamentos**, sobre a **aula vigente** servida por
  `GET /v1/painel-do-dia`: é onde o encontro se fecha antes de acabar (`RF-02-46`,
  `RF-02-47`, jornada §5.6). Três atos:
  - **Lançar a atividade realizada** — a lista de participantes com o **desfecho de cada um**
    entre os três valores fechados, incluindo **mérito extra por auxílio aos colegas**, que é
    como o `RF-02-39` credita ponto extra a quem ajudou o colega (documento 11 §5). Um ato só,
    que converte as reservas em baixa (`RF-02-34`, `RF-02-39`).
  - **Conferir as presenças** vindas do App 01 e **ajustar** — registrar por confirmação a que
    faltou, e **anular** a registrada por engano, com motivo e autor (`RF-02-36`).
  - **Registrar a infração** ocorrida na aula, vinculada ao encontro, à atividade e ao
    Guerreiro(a), com motivo em texto livre e sem revisão de terceiro (`RF-02-37`,
    `RN-02-13`). A tela declara, ao lado do campo, que **descuido acidental com material
    comum não é infração** (`RN-02-14`).
- A área **Pontos de Apoio** ganha o **extrato do livro-razão** do ponto de apoio e, sobre cada
  lançamento, o **ajuste** com quantidade, moedas e motivo — o original permanece intacto, e
  não há caminho de edição nem de remoção (`RF-02-40`, `RN-02-12`).
- Nasce **`GET /v1/lancamentos`**, de Admin, com filtro obrigatório de ponto de apoio, mais
  período e tipo de recurso. Sem ela o Admin não tem por onde achar o lançamento a corrigir:
  o `POST /lancamentos/{id}/ajuste` existe desde o PRD-07 e nenhuma rota lista o que ajustar.
  Decisão do fundador, 2026-08-27, pelo precedente da fatia 9: **leitura que serve RF já
  escrito não é regra nova**. As duas §9 — PRD-07 e PRD-02 — ganham a linha.
- Nasce **`POST /v1/aulas/{id}/presencas/{id}/anulacao`**, de Admin, que **anula** a presença
  registrada por engano — o reconhecimento que apontou a pessoa errada — guardando **motivo,
  autor e momento**, sem apagar o registro. A presença anulada sai do painel do dia e do
  lançamento, e libera o par aula e Guerreiro(a) para o registro correto. Decisão do fundador,
  2026-08-27: é o que faltava para o "ajustável manualmente" do documento 03 §5 existir nos
  dois sentidos. **BREAKING** no esquema: a unicidade de `Presenca` passa a valer **entre as
  não anuladas**, o que exige migração.
- **O Mestre passa a registrar a infração pela App 03**, e não só pela App 09. Decisão do
  fundador, 2026-08-27, resolvendo a contradição interna do PRD-02: a §9 sempre listou a
  ocorrência como "Mestre ou Admin", enquanto a §4, o `RF-02-49` e a `RN-02-20` diziam que o
  Mestre só lê o painel e conduz o quiz. Vale a §9 — quem está na frente da turma é quem vê o
  fato. O núcleo já aceita o Mestre autor da trilha da atividade
  (`lancamentos_e_pontuacao_negativa_das_suas_atividades`): **nenhuma permissão nova**. Muda o
  texto do PRD-02 (§4, `RF-02-49`, `RN-02-20`), o documento 03 §5 e a spec.
- **Correções de redação do PRD-02**, sem decisão nova: a §8 diz que a infração "não cria
  entidade: é `Resultado` de valor negativo", e o núcleo a gravou como `OcorrenciaDeConduta`
  desde o PRD-01; e a §9 nomeia `POST /aulas/{id}/ocorrencias`, quando a rota entregue é
  `POST /v1/ocorrencias-de-conduta`. Mesmo caminho das correções das fatias 7 e 9.
- **Nenhuma entidade nova.** As colunas novas são três, todas em `Presenca`.

## Capabilities

### New Capabilities

Nenhuma. A fatia é a ponta de gestão de capacidades que já existem, mais duas rotas de apoio.

### Modified Capabilities

- `aplicacao-de-gestao`: nasce a área Lançamentos — desfecho por participante, conferência e
  ajuste das presenças e registro da infração —, o extrato e o ajuste entram na área Pontos de
  Apoio, e o Mestre passa a alcançar a infração além do painel e do quiz (`RF-02-34`,
  `RF-02-36`, `RF-02-37`, `RF-02-39`, `RF-02-40`, `RN-02-12`, `RN-02-13`, `RN-02-14`,
  `RF-02-49`, `RN-02-20`).
- `aula-e-presenca`: a presença registrada por engano passa a ser anulável com motivo e autor,
  sem apagar o registro, e a unicidade por aula e Guerreiro(a) passa a valer entre as não
  anuladas (`RF-02-36`, `RF-01-20`).
- `livro-razao`: nasce a leitura de Admin dos lançamentos de um ponto de apoio, que é por onde
  o ajuste alcança o lançamento a corrigir (`RF-02-40`, `RF-07-19`).

## Impact

- **Backend** — `backend/src/nucleo/aulas/` (a anulação da presença e a unicidade entre as não
  anuladas) e `backend/src/nucleo/livro_razao/` (a listagem). Uma migração Alembic: três
  colunas em `presenca` e a troca da `UniqueConstraint` por índice único parcial.
- **Apps** — `apps/app-03-gestao/src/lancamentos/` (novo) e o extrato em
  `apps/app-03-gestao/src/pontos-de-apoio/`.
- **Reuso, sem recriar** — `GET /v1/painel-do-dia` (aula vigente, presenças, equipes,
  atividades previstas), `POST /v1/aulas/{id}/lancamentos`, `POST /v1/aulas/{id}/presencas`,
  `POST /v1/ocorrencias-de-conduta`, `POST /v1/lancamentos/{id}/ajuste`,
  `GET /v1/pontos-de-apoio/{id}/saldos` e o padrão de tela das áreas Painel do dia e Pontos de
  Apoio.
- **Documentação no mesmo PR** — `docs/03-arquitetura-e-tecnologia.md` §5 (a infração pela App
  03 e a anulação da presença), `docs/09-topicos-em-aberto-e-sugestoes.md` (as três decisões,
  em "Já decididos"), `docs/prds/prd-02-frontend-de-gestao.md` (§4, §6.3, §7, §8, §9 e o
  `RF-02-49`/`RN-02-20`), `docs/prds/prd-07-economia-e-ledger.md` §9 (a linha da listagem) e a
  linha da fatia 10 em `openspec/cronograma-de-fatias.md`. Sem arquivo novo em `docs/` e sem
  alteração na `nav` do `mkdocs.yml`. A situação do PRD-02 em `docs/prds/index.md` não muda:
  seguem sete fatias em aberto depois desta.
- **Fora do escopo**, pelo PRD-02 §3.2 — o **lançamento das atividades do próprio Mestre**, que
  é da App 09 e já foi entregue; a **autoria** de trilha, missão e atividade; e as **regras de
  pontuação**, normatizadas no documento 11. Também fora, por não estarem no recorte da fatia:
  o **item do Código de Conduta** na pontuação negativa (`RF-02-38`), que espera a tipificação
  das infrações no documento 09; o **cadastro de atividade avulsa** (`RF-02-29`), travado pela
  pendência de `Atividade.missao_id`; e o **lançamento de aula já encerrada** — o painel do dia
  serve a aula vigente, e é antes de a aula acabar que o `RF-02-47` manda fechar o encontro.
