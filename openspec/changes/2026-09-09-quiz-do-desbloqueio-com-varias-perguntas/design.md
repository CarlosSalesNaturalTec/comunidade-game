## Context

Ver `proposal.md` — Why. O que restringe o desenho é o estado de hoje: o desafio de
desbloqueio não é entidade, são seis colunas na `Missao`
(`tipo_do_desafio_de_desbloqueio`, `desafio_de_desbloqueio_enunciado`,
`desafio_de_desbloqueio_alternativa_1..4` e `desafio_de_desbloqueio_alternativa_correta`), e o
percurso do Guerreiro(a) é **derivado na leitura**, sem tabela de estado por missão: quem o
sustenta é `DesbloqueioDaMissao`, único por (`guerreiro_id`, `missao_id`). Há trilhas com
desafio já declarado e Guerreiros com missão já desbloqueada — a migração não pode perder
nenhum dos dois.

## Goals / Non-Goals

**Goals:**

- Tirar o desafio das colunas da `Missao` sem tocar em como o percurso é derivado.
- Guardar o histórico das tentativas sem transformar `DesbloqueioDaMissao` em série.
- Migrar os desafios de pergunta única existentes sem perda e sem intervenção manual.

**Non-Goals:**

- A imagem por pergunta (fatia 19) — o modelo desta fatia não a antecipa em coluna alguma.
- Qualquer leitura agregada das submissões para medir a H5: esta fatia grava o dado, não o lê.
- Mexer no desafio **prático**, no julgamento do Mestre autor ou na cadência de retomada.

## Decisions

### 1. Três tabelas novas, e `DesbloqueioDaMissao` intocada

`PerguntaDoDesbloqueio` (missão, ordem, enunciado, quatro alternativas, correta) substitui as
seis colunas. `SubmissaoDoDesbloqueio` (guerreiro, missão, instante, acertos, total) guarda
cada tentativa, com `RespostaDaSubmissao` (submissão, pergunta, alternativa escolhida, se
acertou) por pergunta.

`DesbloqueioDaMissao` continua sendo o **fato** — único por par, com `aprovado` em
`True`/`None` —, e `derivar_percurso` não muda uma linha. A submissão é histórico ao lado do
fato, não no lugar dele.

- Descartado gravar as respostas na própria `DesbloqueioDaMissao`: o par é único e o histórico
  pede N linhas.
- Descartado reaproveitar `quiz.modelo.PerguntaDeQuiz`, do Banco do Quiz ao Vivo: aquela é
  pergunta do banco do Mestre, serve a partidas diferentes e tem ciclo de vida próprio.
- Descartado guardar as perguntas como JSON numa coluna da `Missao`: perde a integridade da
  alternativa correta e a referência da resposta à pergunta que ela responde.

### 2. O enunciado do quiz desce para a pergunta; o do prático fica onde está

No **quiz**, cada pergunta tem o seu enunciado e o desafio não tem um. No **prático**, o
`enunciado` segue no desafio, como hoje — é ele que descreve o que o Guerreiro(a) precisa
cumprir. O `tipo_do_desafio_de_desbloqueio` continua na `Missao`, porque é ele que diz se a
missão tem desafio e de que natureza.

### 3. O corte de 60% em inteiro

`acertos * 10 >= total * 6`, sem ponto flutuante: 3 de 5 passa, 2 de 3 passa, 1 de 2 não passa.
Um único caminho de aferição para todo quiz — a regra do documento 11 §2.2 não abre exceção por
quantidade de perguntas.

### 4. A sondagem não é aferida

Missão com `e_sondagem` verdadeiro desbloqueia **ao submeter**, qualquer que seja o número de
acertos (`RN-05-46`). A submissão é gravada igual, com acertos e total, para que o registro
sirva à medida do ciclo. A ramificação é uma só, na aferição, e não um segundo caminho de
submissão.

### 5. A retentativa reenvia o quiz inteiro

Cada submissão traz a resposta de todas as perguntas e é aferida sozinha; pergunta acertada
numa tentativa anterior não é aproveitada na seguinte. Descartado o acerto acumulado entre
tentativas: torna "quantas você acertou" ambíguo para a criança e o histórico, ilegível.

### 6. Contrato das duas rotas

`POST /v1/missoes/{id}/desbloqueio` passa a receber `perguntas`, lista de
`{enunciado, alternativas, alternativa_correta}`, no lugar de `enunciado`, `alternativas` e
`alternativa_correta` no topo — que permanecem no prático. Lista vazia com `tipo=quiz` é 422.

`POST /v1/eu/missoes/{id}/desbloqueio` passa a receber `respostas`, lista de
`{pergunta_id, alternativa_escolhida}`, no lugar de `alternativa_escolhida`. A saída ganha
`acertos` e `total`, ao lado de `aprovado` e `aguardando_mestre`. Resposta faltando, repetida
ou apontando pergunta de outra missão é 422.

A leitura da missão no percurso passa a servir `perguntas` — **sem** a alternativa correta, que
nunca sai do núcleo para o Guerreiro(a).

## Risks / Trade-offs

- **A migração é o ponto de risco: derruba seis colunas com dado vivo.** → Uma migração em três
  passos na mesma revisão: cria as tabelas, copia cada desafio de quiz existente como a
  primeira e única pergunta da sua missão, depois derruba as colunas. O `downgrade` refaz o
  caminho inverso trazendo de volta a pergunta de menor ordem — perde as demais, o que é
  inerente a voltar para um modelo de pergunta única.
- **Cliente antigo quebra ao submeter.** → É a quebra declarada na proposta; as duas telas são
  entregues na mesma fatia e não há consumidor externo dessas rotas.
- **Quiz com muitas perguntas pesa numa tela só, em rede fraca.** → Nesta fatia o texto é o
  único conteúdo, e o volume é escolha do Mestre autor, que a App 09 informa. A imagem, que é o
  que realmente pesa, entra na fatia 19 com teto de 1 MB por pergunta.
- **Guardar toda tentativa faz a tabela crescer com o ciclo.** → Foi decisão do fundador
  (documento 09 §1); o volume do Ciclo 01 é de uma comunidade, e não há consulta agregada nesta
  fatia que precise de índice além do par (guerreiro, missão).
