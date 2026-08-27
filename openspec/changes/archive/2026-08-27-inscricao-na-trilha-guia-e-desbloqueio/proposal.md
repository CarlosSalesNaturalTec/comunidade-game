# Inscrição na trilha, guia do percurso e desafio de desbloqueio

Origem: **PRD-05 — App 05: Área do Guerreiro(a)**, §§3.1, 5.2, 5.3, 6.2 e 9, e **PRD-09 —
Área do Mestre**, §§6.4 e 9. **Quarta fatia** do PRD-05 e fatia avulsa do PRD-09. Atende
`RF-05-08` a `RF-05-18`, `RF-05-72`, `RF-05-73` e `RF-05-81`, e `RF-09-26`, sob `RN-05-03`,
`RN-05-04`, `RN-05-06`, `RN-05-20`, `RN-05-21`, `RN-05-33`, `RN-05-34`, `RN-05-43` e
`RN-05-44`.

## Why

A App 05 tem entrada, coleta e carteira. Falta **o motivo de ela existir**: a criança abre a
aplicação e não vê a trilha. Não há como se inscrever, não há próxima missão, não há o que
está bloqueado nem por quê — e a jornada 5.2 do PRD-05 começa exatamente por aí, com a tela
inicial abrindo na próxima missão "sem que a criança precise procurar em menu" (§12).

Duas travas seguravam este recorte, e as duas caíram:

- A **inscrição na trilha** foi decidida em 2026-08-26 e já está gravada no documento 11 §2 e
  no documento 09 §1, mas **nunca nasceu no núcleo**: `RF-05-09` e a rota
  `POST /v1/eu/trilhas/{id}/inscricao` do PRD-05 §9 seguem sem entidade onde gravar, e o
  nível 1 continua derivando "inscrito" de haver `Resultado` na trilha — fazendo depender de
  ato do Mestre o que é ato da criança.
- O **desafio de desbloqueio** (`RF-09-26`) foi adiado duas vezes no PRD-09 por uma pergunta
  em aberto: se o desbloqueio é fato do Guerreiro(a) ou da equipe. O fundador decidiu em
  2026-08-27 que é **fato do Guerreiro(a) na trilha**, e a fatia grava a decisão no documento
  11 §2.2 antes de implementá-la.

Sem as duas, `RF-05-08`, `RF-05-10` e `RF-05-13` não têm o que consultar: o núcleo hoje sabe
quais missões o Guerreiro(a) concluiu, mas ninguém deriva qual é a próxima nem por que a
seguinte está travada.

## What Changes

**Documentação antes do código** — a decisão do desbloqueio é nova e não nasce aqui: o
documento 11 §2.2 passa a dizer de quem é o fato, o documento 09 §1 registra a decisão, e só
então o PRD-09 e o PRD-05 a aplicam.

**Núcleo — o percurso do Guerreiro(a) na trilha**

- Nasce a **`InscricaoNaTrilha`**: Guerreiro(a), trilha e momento. Exige **trilha publicada**,
  é **uma por Guerreiro(a) e trilha**, **não se desfaz** e **não obriga a concluir**
  (`RF-05-09`, `RN-05-43`, `RN-05-44`).
- O **nível 1 passa a exigir as duas condições** do documento 11 §6 — inscrição **e** primeira
  atividade realizada —, no lugar da derivação por `Resultado` que o núcleo usava desde a
  fatia de pontuação do PRD-01. **BREAKING** para a capacidade `pontos-niveis-e-badges`:
  Guerreiro(a) com resultado lançado e sem inscrição deixa de alcançar o nível 1.
- Nasce o **desafio de desbloqueio da missão**, autorado pelo Mestre autor na forma de quiz ou
  de desafio prático (`RF-09-26`).
- Nasce a **submissão do desafio pelo Guerreiro(a)**. No **quiz**, o núcleo afere e a missão
  seguinte abre **na hora**. No **desafio prático**, o Guerreiro(a) declara que cumpriu e o
  **Mestre autor julga** — decisão do fundador em 2026-08-27, porque desafio prático não tem
  critério que o núcleo possa aferir sozinho. Em qualquer das duas formas, não passando ele
  **repete quantas vezes quiser, sem ser eliminado** (`RF-05-13`, `RF-05-14`, `RN-05-20`).
- Nasce a **derivação do percurso**: qual é a próxima missão, quais estão bloqueadas e **o
  motivo de cada bloqueio** — nunca cadeado mudo (`RF-05-08`, `RF-05-10`). Só a missão
  obrigatória entra no denominador do nível; a opcional pontua e fica fora (`RF-05-81`,
  `RN-05-33`).

**App 05 — o bloco "Trilha"**

- **Escolha do poder** entre os do catálogo do ciclo e **inscrição** nas trilhas dele
  (`RF-05-09`).
- **Tela inicial na próxima missão**, com o que fazer e o que ela desbloqueia (`RF-05-08`).
- **Missão bloqueada com o motivo** e o que falta para abri-la (`RF-05-10`).
- **Conteúdo da missão** — texto, imagens, vídeo e arquivos — e **bibliografia** com título,
  capítulo e se há exemplar no ponto de apoio do Guerreiro(a) (`RF-05-11`, `RF-05-12`).
- **Missão de sondagem** respondida antes da primeira missão, com a tela dizendo que ela serve
  para o Mestre ajustar e **não altera nível** (`RF-05-72`, `RF-05-73`, `RN-05-34`).
- **Desafio de desbloqueio**, com repetição sem punição (`RF-05-13`, `RF-05-14`).
- **Progresso**: o nível na trilha e quantas missões faltam para o próximo, em missões
  desbloqueadas — nível é percurso, não saldo (`RF-05-15`, `RF-05-16`, `RN-05-03`,
  `RN-05-04`).
- **Alternância entre trilhas** preservando o contexto de cada uma (`RF-05-17`).
- Resultado ainda não lançado pelo Mestre aparece como **"aguardando lançamento"**
  (`RF-05-18`, `RN-05-06`).

**App 09 — a bancada do desafio**

- O Mestre autor **cria o desafio de desbloqueio** da missão que autora (`RF-09-26`).
- O Mestre autor **julga os desafios práticos** declarados como cumpridos nas suas trilhas,
  por Guerreiro(a) (`RF-09-26`, `RF-05-13`).

## Capabilities

### New Capabilities

- `inscricao-na-trilha`: o vínculo entre Guerreiro(a) e trilha — ato da criança, exige trilha
  publicada, um por par, não se desfaz.
- `desbloqueio-da-missao`: o desafio autorado pelo Mestre, a submissão pelo Guerreiro(a) e a
  derivação do percurso — próxima missão, missão bloqueada e o motivo do bloqueio.

### Modified Capabilities

- `pontos-niveis-e-badges`: o nível 1 passa a exigir inscrição **e** primeira atividade
  realizada, fechando a condição que a capacidade já enuncia e não verificava.
- `area-do-guerreiro`: a App 05 ganha o bloco da trilha — inscrição, guia, conteúdo,
  sondagem, desbloqueio e progresso.
- `area-do-mestre`: a App 09 ganha a autoria do desafio de desbloqueio.

## Impact

**Código**

- `backend/src/nucleo/trilhas/` — a inscrição, o desafio de desbloqueio e a derivação do
  percurso.
- `backend/src/nucleo/pontuacao/` — a segunda condição do nível 1.
- `apps/app-05-guerreiro/` — o bloco `trilha/`, terceiro item do nav de `AreaDoGuerreiro`.
- `apps/app-09-mestre/` — a bancada do desafio de desbloqueio.

**API** — as rotas do PRD-05 §9 que o recorte cobre (`GET /v1/eu/trilhas`,
`POST /v1/eu/trilhas/{id}/inscricao`, `GET /v1/eu/trilhas/{id}/missoes/{ordem}`,
`POST /v1/eu/missoes/{id}/desbloqueio` e `GET /v1/eu/progresso`) e a do PRD-09 §9
(`POST /v1/missoes/{id}/desbloqueio`). O julgamento do desafio prático **não tem rota
declarada em nenhum PRD** — nasce da decisão de 2026-08-27 e é declarada no PRD-09 §9 na
tarefa de documentação. **Nenhuma rota existente muda de contrato.**

O **conteúdo e a bibliografia não precisam de rota nova**: `GET /v1/trilhas/{id}` já os serve
na trilha publicada, com a licença, o crédito ao autor e a disponibilidade do exemplar por
`ponto_de_apoio_id` — a capacidade `conteudo-da-missao` já o declara. As rotas `/v1/eu/*`
carregam apenas o que é **do Guerreiro(a)**: o estado de cada missão no percurso dele.

**Infraestrutura** — uma tabela nova (`inscricao_na_trilha`) e o desafio de desbloqueio na
missão: **duas migrações**, nenhuma outra mudança.

**Documentação** — três alterações, na ordem da hierarquia de autoridade:

1. Documento 11 §2.2 — o desbloqueio da missão é **fato do Guerreiro(a) na trilha**, e o
   **desafio prático é julgado pelo Mestre autor**, enquanto o quiz o núcleo afere.
2. Documento 09 §1 — as duas decisões acima entram em "Já decididos"; entram também, como
   **pendências novas**, (a) a marcação item a item que o critério da hipótese **H5** exige —
   o Mestre declarar qual item do poder cada pergunta cobre —, sem `RF` que a operacionalize
   em nenhum PRD, e (b) a divergência entre "missão desbloqueada" e "missão com Resultado
   lançado" nos **níveis 2 e 4**, que esta fatia deixa como está por decisão do fundador em
   2026-08-27.
3. PRD-09 e PRD-05 — aplicam as decisões, sem repetir o texto normativo; o PRD-09 §9 ganha a
   rota do julgamento do desafio prático.

**Fora do escopo**, reproduzindo o que o PRD-05 §3.2 já exclui: **autoria de trilha e de
conteúdo** é da App 09; **lançamento de resultado, presença e mérito** é do Mestre ou do
Admin, e aqui só se consulta; **formação de equipe** é do App 01. Da §6.2, ficam para a fatia
seguinte a **entrega da produção da missão** com devolutiva (`RF-05-74` a `RF-05-78`) e a
**retomada por revisão espaçada** (`RF-05-79`, `RF-05-80`) — decisão do fundador de
2026-08-27, para que a leitura por IA e o descarte de foto e áudio sejam tratados por inteiro
numa fatia própria. Desafios e equipes (§6.3), criação original e portfólio (§6.5) e o avatar
(`RF-05-51`) são fatias próprias.

**Pendências** — nenhuma da §14 do PRD-05 toca este recorte, e nenhuma das duas que a fatia
**abre** a trava. A marcação item a item da H5 é medição de hipótese do documento 10, e o
percurso do Ciclo 01 funciona sem ela. A divergência dos níveis 2 e 4 é anterior a esta fatia:
o núcleo os deriva de `Resultado` desde a fatia de pontuação do PRD-01, nenhum `RF` do recorte
pede outra coisa, e mexer nisso mudaria a certificação de quem já a tem.
