## Context

Ver `proposal.md` — Why. O módulo `quiz` já está consolidado em
`openspec/specs/quiz-ao-vivo/spec.md`: cadastro, partida, resposta, anulação e encerramento com
crédito, tudo escrito e testado, sem nenhuma rota. Esta fatia abre a porta do **banco de
perguntas** e acerta duas lacunas do modelo. O padrão de abrir porta HTTP sobre regra pronta é o
da change `etiqueta-ods-da-trilha-e-da-missao`; o que segue são só as escolhas novas.

## Goals / Non-Goals

**Goals:**

- Expor `cadastrar_pergunta` e a leitura do banco sem reescrever recusa alguma da regra.
- Gravar o vínculo com missão e trilha que o `RF-09-39` exige e o `RF-09-40` consulta.

**Non-Goals:**

- Rota para a partida — `abrir_partida`, `registrar_resposta`, `anular_pergunta` e
  `encerrar_partida` ficam intocadas.
- Editar ou apagar pergunta: nenhum `RF` do PRD-09 §6.5 os prevê.

## Decisions

**1. O cliente declara só a missão; a trilha é derivada e persistida.** O PRD-09 §8 lista
`trilha` **e** `missão` entre os atributos, e as duas colunas entram. Mas o corpo da requisição
aceita apenas `missao_id`: `Missao` já pertence a uma `Trilha`, e pedir as duas ao cliente abre
a porta para a contradição de uma missão declarada sob a trilha errada. `trilha_id` é preenchida
por derivação no ato do cadastro, nunca pelo cliente.

_Alternativa descartada:_ derivar a trilha a cada leitura, como `PartidaDeQuiz` faz a partir da
atividade — o filtro por trilha do `RF-09-40` viraria _join_ a cada consulta, e aqui a coluna
não custa nada porque a missão nunca troca de trilha.

**2. As duas colunas nascem `NOT NULL`, sem _backfill_.** A tabela `pergunta_de_quiz` nunca teve
rota: nada além de teste jamais escreveu nela, e não há linha em nenhum ambiente. A migração
Alembic acrescenta as duas colunas obrigatórias direto, sem passo intermediário anulável.

**3. A `PerguntaDeQuiz` não tem situação** — decisão do fundador, 2026-08-23, registrada na
`proposal`. Não entra coluna, não entra rota de desativação, e o `GET` não tem filtro padrão a
aplicar: o banco devolve tudo o que o Mestre cadastrou.

**4. A leitura é uma função nova na regra, não uma consulta na rota.** `perguntas_do_mestre`
recebe os filtros opcionais e o Mestre em sessão, e a rota só a chama — o mesmo desenho de
`GET /trilhas/minhas` e `GET /minhas-turmas`. O recorte por autoria vive na regra, onde é
testável sem HTTP.

**5. O cadastro segue a permissão que a regra já aplica.** `cadastrar_pergunta` exige
`Operacao.suas_trilhas_e_conteudos`, que a matriz do PRD-01 §4 concede a Mestre e Admin. A rota
não acrescenta conferência própria. A leitura é do **Mestre em sessão**, por autoria.

## Risks / Trade-offs

- **A pergunta fica sem porta de saída** → sem editar, sem apagar e sem aposentar, o banco do
  Mestre só cresce. É consequência aceita da decisão 3 e do silêncio do PRD-09 §6.5; se a
  operação da primeira turma mostrar que incomoda, volta como pendência ao documento 09, não
  como suposição aqui.
- **O `RF-09-41` não fecha** → a disponibilidade do banco para a partida depende da condução, que
  espera a App 01 pela formação de equipe. Fica nomeado como pendente na `proposal` e em
  `docs/prds/index.md`, sem entrega fingida.
- **Cadastro por Admin** → a matriz concede a operação a Admin, e a regra já a aceita. O
  `GET /v1/perguntas/minhas` é por autoria, então uma pergunta cadastrada por Admin não aparece
  no banco de Mestre nenhum. Não é defeito desta fatia: é o alcance da matriz do PRD-01, e a
  fatia não o estreita nem o alarga.

## Migration Plan

Uma revisão Alembic acrescenta `missao_id` e `trilha_id` a `pergunta_de_quiz`, ambas `NOT NULL`
com chave estrangeira para `missao` e `trilha`, mais índice em `missao_id` e em `trilha_id` para
os filtros do `RF-09-40`. Sem _backfill_ (decisão 2). O `downgrade` remove as duas colunas.
