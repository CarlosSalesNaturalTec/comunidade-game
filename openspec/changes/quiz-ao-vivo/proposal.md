## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Décima fatia, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-01-36`, `RF-01-39` (segunda metade — uma equipe só por partida),
`RF-01-17` (parcial — a condução do Quiz ao Vivo das suas aulas), `RF-01-21`, `RF-01-03`,
`RF-01-16`, `RF-01-18`, `RN-01-38`.

O Quiz ao Vivo é o que a nona fatia nomeou ao adiar `RF-01-36` e a segunda metade de
`RF-01-39`: `Equipe` já existe, `Aula` já existe, e falta a partida que corre sobre as duas.
É também **o último recorte do PRD-01 inteiramente destravado** — os requisitos que restam
depois dele esperam os números da proteção das rotas públicas, o livro-razão do PRD-07, o
território do PRD-08 ou a entrega do conjunto de dados, todos pendentes no documento 09 §1.

A matriz de permissões guarda dois assentos vazios desde a segunda fatia —
`resposta_de_quiz_da_equipe` e `conducao_do_quiz_ao_vivo_das_suas_aulas` —, e esta fatia
ocupa os dois. Nenhuma entrada nova na matriz: as duas já estão no PRD-01 §4.

## What Changes

### Decisão nova aplicada antes desta change

**A plataforma não controla aparelhos no Ciclo 01.** A decisão foi tomada pelo fundador
durante a exploração desta fatia e subiu a hierarquia antes de virar plano, na ordem que o
`CLAUDE.md` exige: gravada no documento-fonte das regras da partida (05 §5), refletida na
trava antifraude do documento 11 §5.1, registrada no documento 09 nas duas linhas de "Já
decididos" que afirmavam a vinculação do aparelho, e acompanhada em 03 §4 e no descritor da
fonte única do documento 99 §3.

O PRD-01 **não muda**: `RF-01-36` já fala em resposta por **equipe e pergunta**, e o §8 nunca
teve entidade de aparelho. A trava contra a resposta por outra equipe passa a ser **só** a
equipe única por partida (`RF-01-39`), que o núcleo verifica.

### A partida

- Nasce a **PerguntaDeQuiz**, de autoria do Mestre curador: enunciado, **quatro alternativas**
  e a correta (documento 09, *Formato da pergunta do Quiz ao Vivo*). **Sem tempo por
  pergunta** — o ritmo é de quem conduz, e o núcleo não cronometra.
- Nasce a **PartidaDeQuiz**, vinculada à aula, conduzida pelo **Mestre que ministra a aula ou
  por um Admin** (`RF-01-17`, `RF-01-16`). As equipes disputantes são declaradas na abertura.
- Nasce a **RespostaDeQuiz**, por **equipe e pergunta**, com o **momento de chegada no
  servidor** (`RF-01-36`). O momento é carimbado **na chegada**, nunca declarado pelo cliente
  — é o critério de desempate do documento 05 §5, e cliente não arbitra a própria ordem.
- Uma resposta por equipe e pergunta: o reenvio com a rede instável não duplica nem
  reordena, no mesmo desenho de tolerância que a `Presenca` já usa desde a nona fatia.

### Uma equipe só por partida

- O núcleo **recusa a abertura da partida** em que o mesmo Guerreiro(a) apareça em duas das
  equipes disputantes (`RF-01-39`, segunda metade). É a exceção declarada à regra da nona
  fatia — várias equipes na aula, uma só na partida (documento 03 §4.1).
- As equipes da partida são **equipes da aula** daquela aula, nunca da trilha: a partida corre
  no encontro, e a equipe da trilha tem outro tempo de vida (`RF-01-37`, documento 02 §5).

### O quiz como fonte do motor de pontuação

- A partida passa a ser **fonte automática** de ponto regular (`RF-01-21`, documento 11 §5):
  **1 ponto por acerto da equipe**, **+1 de bônus à primeira a acertar** pela ordem de chegada,
  **teto de 10 pontos por partida**. O ponto vale para **cada integrante** da equipe, no mesmo
  desenho de crédito por integrante que a criação original firmou na nona fatia.
- O **Mestre anula a pergunta** havendo contestação (documento 05 §5). Como **ponto regular
  nunca é debitado** (`RN-01-38`, com gatilho no ORM e no Postgres desde a sexta fatia), a
  anulação **não pode** estornar de `PontoRegular`. O documento 11 §5 lança o quiz como
  automático **da partida**, não da pergunta — o desenho de quando o crédito se consolida é
  questão do `design.md`, não regra nova.

### O que esta fatia não tem, e não é omissão

**As rotas** não são deste PRD, como nas fatias 5 a 9: o banco de perguntas é da App 09
(PRD-09), a condução da partida é da App 03 (PRD-02) e o recebimento da pergunta com o envio
da resposta é do App 01 (PRD-04). O PRD-01 §9 diz expressamente que as rotas de domínio ficam
nos PRDs que as definem. Esta entrega é **entidade e regra**.

**A sincronização em tempo real** entre os dispositivos (documento 05 §5) é da aplicação que
conduz, não do núcleo: o núcleo guarda a pergunta corrente da partida e a ordem de chegada, e
quem transmite é a App 03 com o App 01.

**O painel do dia** (`RF-01-17`, a outra metade) é leitura da App 03, requisito do PRD-02.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação, cadência
de coleta e valoração de aporte; captura da imagem, conversa de cadastro e geração do
descritor no aparelho; exclusão do _template_; telemetria da Batalha de Laser e personalização
por IA.

O que é do PRD-01 mas de outra fatia:

| Fica para                                    | Porque                                             |
| -------------------------------------------- | -------------------------------------------------- |
| `RN-01-07` na aula                           | reserva de recursos depende do PRD-07              |
| `RF-01-23`, `RF-01-24`, `RF-01-41`           | território (PRD-08) e livro-razão (PRD-07)         |
| `RF-01-58` a `RF-01-60`                      | `Troca` e catálogo avulso, do PRD-07               |
| `RF-01-25`, `RF-01-46`, `RF-01-47`           | fila de avaliação e entrega do conjunto de dados   |
| `RF-01-29`                                   | entidade `Auditoria` e a consulta de Admin         |
| `RF-01-22`, `RF-01-43`                       | documento 09, "Números da proteção das rotas públicas" |
| `RF-01-49` a `RF-01-53`, `RF-01-55`          | documento 09, "Números da proteção das rotas públicas" |
| `RF-01-31`                                   | PRD-01 §14, pendência declarada                    |
| `RF-01-44`                                   | trava do Ciclo 02, por definição                   |

## Capabilities

### New Capabilities

- `quiz-ao-vivo`: a pergunta de múltipla escolha do Mestre curador, a partida conduzida na
  aula pelo Mestre que a ministra ou por um Admin, a resposta por equipe e pergunta com o
  momento de chegada carimbado no servidor, a recusa da partida em que um Guerreiro(a) apareça
  em duas equipes, e a anulação de pergunta pelo Mestre.

### Modified Capabilities

- `pontos-niveis-e-badges`: o ponto regular ganha a fonte automática da partida de quiz — 1
  por acerto da equipe, +1 à primeira, teto de 10 por partida —, creditada a cada integrante
  (`RF-01-21`, `RN-01-38` preservado: nada é debitado).
- `equipe`: a regra "o Guerreiro(a) integra mais de uma equipe da mesma aula" recebe a exceção
  da partida de quiz, em que ele joga por uma só (`RF-01-39`).

`permissoes-e-escopo-de-comunidade` **não** entra: as duas operações do quiz já estão no enum
da matriz desde a segunda fatia e no PRD-01 §4, e o requisito da capability é genérico —
conferir a matriz em toda operação.

## Impact

- `backend/src/nucleo/`: módulo novo `quiz/` (`PerguntaDeQuiz`, `PartidaDeQuiz`,
  `RespostaDeQuiz`, a ordem de chegada, a recusa da equipe repetida e a anulação), lendo
  `aulas`, `equipes`, `persona` e a matriz de permissões já existentes.
- `backend/src/nucleo/pontuacao/`: a partida entra como fonte de `PontoRegular`, com a régua
  própria do documento 11 §5 — não passa pelo `creditar_ponto_regular` do resultado, que tem
  outra régua.
- `backend/alembic/`: migração para `pergunta_de_quiz`, `partida_de_quiz` e `resposta_de_quiz`.
- `backend/src/nucleo/permissoes.py`: **sem alteração** — as duas operações já existem.
- Nenhuma rota nova sob `/v1`: entidade e regra, como nas fatias 5 a 9.
- `docs/`: a decisão dos aparelhos **já foi gravada** nos documentos 03, 05, 09, 11 e 99 antes
  desta proposta. `docs/prds/index.md` recebe a situação atualizada se ela mudar ao fim da
  implementação.

## Pergunta ao fundador antes das specs

Uma ambiguidade real, que o `design.md` não pode resolver sozinho porque muda o modelo:

**A que trilha o ponto do quiz se prende?** `PontoRegular` é por **(Guerreiro(a), trilha)** —
nunca global (`RF-01-21`, `RN-01-42`). Mas a partida corre numa **aula**, e a aula tem
comunidade, data e horário; não tem trilha.

Há apoio documental para pendurar a partida numa **atividade**: o documento 05 §5 chama o Quiz
de "atividade-modelo, encaixável no Desafio do dia", o documento 11 §4 lista "Competição ao
vivo (Quiz)" como **natureza de atividade**, e `Atividade.natureza` já é campo aberto no
núcleo. A partida herdaria missão → trilha, e o ponto teria onde cair.

A alternativa é a partida solta na aula — e aí o ponto do quiz não tem trilha a que se
vincular, o que contraria `RF-01-21`.

A leitura da atividade parece a correta, mas ela decide se **toda partida exige uma atividade
declarada**, e isso é escopo, não desenho. Confirme antes de escrever as specs.
