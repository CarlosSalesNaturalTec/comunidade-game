## Why

Origem: **PRD-04** (App 01 — aula presencial), §6.2, jornada 5.9. Atende `RF-04-41`,
`RF-04-42`, `RF-04-43`, `RF-04-44` e `RF-04-58`.

O Quiz ao Vivo atravessa três aplicações e duas já entraram: a App 09 cadastra o banco
(`banco-do-quiz-ao-vivo`) e a App 03 conduz a partida (`conducao-da-partida-de-quiz`). Falta o
elo em que a criança joga. Sem ele o Quiz existe inteiro no núcleo e na gestão, e ninguém
responde — a fase 3 do piloto (documento 05 §7) pressupõe a partida acontecendo.

As duas rotas do aparelho — `GET /v1/partidas-de-quiz/{id}/pergunta` e
`POST /v1/partidas-de-quiz/{id}/respostas` — saíram testadas por contrato na fatia da condução.
Esta fatia entrega quem as chama, e fecha três lacunas que só apareceram ao olhar do aparelho.

## What Changes

**Núcleo — três lacunas do caminho do aparelho:**

- **A partida não é descoberta.** Nenhuma rota devolve ao Guerreiro(a) a partida da aula em que
  ele está, e sem o identificador as duas rotas do aparelho são inalcançáveis. Nasce
  `GET /v1/aulas/{id}/partidas`, que devolve as partidas da aula e, em cada uma, **a equipe do
  Guerreiro(a) em sessão já derivada** — o núcleo garante na abertura que é uma só, e é essa
  garantia que cumpre `RF-04-42` sem o aparelho escolher nem casar por nick (`RF-04-41`,
  `RF-04-42`).
- **A equipe nunca vê se acertou.** `pergunta_para_equipe` omite liberação e alternativa
  correta, e `estado_da_partida` exige `conducao_do_quiz_ao_vivo_das_suas_aulas` — o
  Guerreiro(a) recebe 403. Liberado o resultado por quem conduz, a leitura do aparelho passa a
  levar a **alternativa correta**, **se a equipe dele acertou** e **qual equipe chegou
  primeiro**. Antes da liberação nada disso sai, como já é hoje (`RF-04-44`).
- **A spec diverge do código.** O cenário "A leitura devolve o estado corrente", da capacidade
  `quiz-ao-vivo`, diz "quem conduz **ou o aparelho de uma equipe disputante** lê a partida", e o
  código recusa o aparelho. A fatia reconcilia os dois: o aparelho lê pela rota que é dele, e o
  cenário deixa de prometer o que `estado_da_partida` não faz.

**App 01 — o aparelho da equipe:**

- Módulo `quiz/` novo, alcançado por um quarto caminho na tela inicial, com a entrada do
  Guerreiro(a) por nick e imagem já entregue na quarta fatia.
- Sondagem periódica da pergunta no ar, sem conexão longa (documento 03 §1).
- Envio de **uma** resposta por equipe e pergunta, com a segunda recusada (`RF-04-43`).
- Exibição do resultado quando quem conduz o libera (`RF-04-44`).
- Sem rede, a resposta de quiz fica indisponível (`RF-04-58`).

**Documentação:** o `RF-04-42` fala em "vinculado o aparelho", a jornada 5.9 item 1 põe o
vínculo aparelho–equipe na App 03 e a §3.2 o exclui do escopo da App 01. Os três contrariam o
documento 05 §5, fonte única do Quiz ao Vivo, que decide que **a plataforma não controla
aparelhos no Ciclo 01** e que a resposta é da equipe, nunca do aparelho de onde veio. Pela
hierarquia de autoridade o documento 05 prevalece e o PRD-04 se corrige: o vínculo é estado do
próprio aparelho, e não entidade do núcleo. Não é decisão nova — é o código e o PRD alcançando
a fonte (fundador, 2026-08-25). Um vínculo persistido também impediria a jornada 5.9 item 6,
"equipe sem aparelho responde pelo aparelho do Mestre".

## Capabilities

### New Capabilities

Nenhuma. As duas capacidades tocadas já existem.

### Modified Capabilities

- `quiz-ao-vivo`: a descoberta da partida pelo Guerreiro(a) em sessão, com a equipe dele
  derivada; o resultado liberado servido ao aparelho da equipe; e o cenário da leitura por
  sondagem reconciliado com o que o núcleo faz.
- `aplicacao-da-aula-presencial`: o quarto caminho da tela inicial e o aparelho da equipe na
  partida — sondagem, resposta única, resultado e comportamento sem rede.

## Impact

- `backend/src/nucleo/quiz/regra.py` e `rotas.py`: rota nova de descoberta e ampliação da saída
  do aparelho. `permissoes.py` **não muda** — o Guerreiro(a) já tem
  `resposta_de_quiz_da_equipe` em leitura e escrita.
- `backend/src/nucleo/quiz/modelo.py` e `alembic/`: **sem migração** — a fatia não cria nem
  altera tabela.
- `apps/app-01-aula-presencial/src/quiz/` (novo), `src/inicio/TelaInicial.tsx` e `src/api/`.
- `docs/prds/prd-04-aula-presencial.md` §3.2, §5.9 e §6.2; `docs/09-topicos-em-aberto-e-sugestoes.md`
  §1; `docs/prds/index.md`. O **documento 05 não muda**.

## Fora do escopo

Reproduz o que o PRD-04 §3.2 já exclui, e o que a fatia deixa para depois:

- **Caminho das trilhas** — a missão da equipe, o conteúdo e a atividade do dia (`RF-04-29`,
  `RF-04-35`).
- **Assistente de trilhas** e entrega da produção da missão (`RF-04-36` a `RF-04-40`,
  `RF-04-45` a `RF-04-47`).
- **Abertura e condução da partida**, que são da App 03 e já entraram.
- **Fila local sem rede** (`RF-04-23` a `RF-04-25`) e captura de quem se cadastrou sem imagem
  (`RF-04-16`).
