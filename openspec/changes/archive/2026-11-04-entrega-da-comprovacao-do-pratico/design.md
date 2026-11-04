# Design

## Context

Ver `proposal.md` — Why. O que molda o desenho:

- **A declaração já existe e é uma linha única por par.** `DesbloqueioDaMissao` tem
  `(guerreiro_id, missao_id)` único, `aprovado` anulável e `julgado_por_id`; no prático ela nasce
  com `aprovado` em aberto e é **apagada** quando o julgamento não passa. A comprovação é dado
  **dessa** linha, não de uma entidade nova.
- **O padrão de mídia do aluno está consolidado.** `CriacaoOriginal` guarda `producao` (corpo do
  texto ou endereço do link), `referencia`, `tamanho` e `tipo_do_arquivo`, com `POST`/`PATCH`/
  `GET` de `/criacoes/{id}/arquivo` e os tetos de `criacoes_originais/regra.py` — 200 MB para
  vídeo, 20 MB para os demais, sobre lista fechada de MIME. A fatia do núcleo de 2026-11-04
  acabou de fechar o `GET` que faltava ali.
- **A tela do desbloqueio é uma só para as duas aplicações.**
  `comum/trilha/DesafioDeDesbloqueio.tsx` é consumida pela App 05 (`trilha/Trilha.tsx`) e pela
  App 01 (`trilhas/TelaDeTrilhasDoGuerreiro.tsx`), ambas com `submissaoDoDesbloqueioLigada`.
  O prático hoje é um botão "Já cumpri!" sem campo algum.
- **A forma aceita é `TipoDeProducaoDaCriacaoOriginal`.** A fatia 26 gravou
  `desafio_pratico_forma_de_comprovacao` com esse mesmo enum de seis valores, e as três leituras
  do desafio já o devolvem. `comum/trilha/api.ts` ainda **não** tem os três campos no tipo
  `DesafioDeDesbloqueio` — é desta change trazê-los.

## Goals / Non-Goals

**Goals:**

- A comprovação é dado da declaração, gravada no mesmo ato, e legível por quem a entregou e por
  quem a julga.
- A tela é **uma**, e as duas aplicações herdam o mesmo comportamento sem reimplementá-lo.
- O caminho da criança que não entrega pelo aparelho fica explícito no modelo, não implícito na
  ausência de dado.

**Non-Goals:**

- Nenhum veredito novo, nenhum ponto, nenhum motivo de recusa — `aprovado: bool` e o
  `JulgarDesafioPraticoEntrada` ficam como estão; é a fatia 27.
- Nenhuma leitura pública da comprovação: o portão da vitrine é a fatia 12 do PRD-03.
- Nenhuma mudança no quiz, na sondagem nem nas rotas de pergunta.

## Decisions

1. **A comprovação são colunas na `DesbloqueioDaMissao`, não entidade nova.** A linha já é uma
   por par, já nasce e morre com a declaração, e o apagamento no julgamento reprovado leva a
   comprovação junto sem código de limpeza. Entram `comprovacao` (texto ou endereço),
   `comprovacao_referencia`, `comprovacao_tamanho`, `comprovacao_tipo_do_arquivo` e
   `entrega_presencial`, todas anuláveis, espelhando os nomes de `CriacaoOriginal`.
   _Descartado:_ tabela `ComprovacaoDoPratico` própria — não há cardinalidade que a justifique, e
   obrigaria a replicar o apagamento. _Descartado:_ reusar `ProducaoDaMissao` — é produção de
   **atividade**, sem ato de aprovação, e o documento 09 §1 a exclui do acervo de propósito.

2. **A `forma de comprovação` não vem na submissão: é lida da missão.** O núcleo confere o que o
   Guerreiro(a) entregou contra `missao.desafio_pratico_forma_de_comprovacao` e recusa a
   divergência com 422. Mandar a forma no corpo deixaria o cliente escolhê-la.
   _Descartado:_ aceitar a forma do cliente e só avisar — o `RN-09-50` fez a forma ser **uma**
   justamente para não haver escolha na ponta.

3. **A entrega presencial é coluna booleana, não ausência de comprovação.** Sem ela, "não
   entregou" e "vai entregar no encontro" ficariam indistinguíveis, e a bancada da fatia 27 não
   teria como dizer ao Mestre o que esperar. Exatamente um entre comprovação e
   `entrega_presencial` é preenchido, e a regra recusa os dois vazios e os dois cheios.
   _Descartado:_ um valor sentinela em `comprovacao` — dado de controle escondido em campo de
   texto livre.

4. **As três rotas do arquivo espelham `/criacoes/{id}/arquivo`**, mas **não** no mesmo
   caminho. A escrita é do Guerreiro(a) e fica sob `/v1/eu/missoes/{id}/desbloqueio/comprovacao`
   — `POST` abre a sessão de envio retomável com a origem de quem vai enviar, `PATCH` confirma.
   A **leitura** é também do Mestre autor, que não cabe em `/eu/`, e por isso toma a forma da
   rota do julgamento, por missão e Guerreiro(a):
   `GET /v1/missoes/{id}/desbloqueios/{id_do_guerreiro}/comprovacao` — é por ela que a bancada
   da fatia 27 alcança a entrega. Os tetos e a lista de MIME são os de
   `criacoes_originais/regra.py`, extraídos para `armazenamento/limites.py`, onde as duas os
   leem em vez de duplicados. _Descartado:_ bytes inline na submissão, que o núcleo fatia escolheu para a
   produção da missão — ali a foto é pequena e vai ao OCR na hora; aqui a forma aceita pode ser
   vídeo, e 200 MB não passam em corpo de requisição.

5. **A tela é o componente comum, com o formulário dentro dele.** `DesafioDeDesbloqueio.tsx`
   ganha o ramo do prático — critério, aviso, campo da forma aceita, progresso e a alternativa
   presencial —, e `comum/trilha/api.ts` ganha os três campos no tipo e as funções de envio sobre
   `enviarParteComProgresso`, que `comum/api/cliente.ts` já expõe. _Descartado:_ copiar
   `EntregaDeCriacao.tsx` da App 05 — é da culminância, tem seletor de tipo e modalidade de
   equipe, e vive onde a App 01 não alcança; duplicá-lo criaria a quinta reimplementação do mesmo
   padrão, que a fatia da moldura de mídia já pagou para desfazer.

6. **O aviso da mídia guardada é nó próprio da tela, antes do controle de entrega.** O PRD-05
   §11 já exige o aviso visível com acesso à área detalhada em toda tela que coleta dado; aqui ele
   é o que dá sentido ao critério de aceite, e por isso não pode ser rodapé nem confirmação
   posterior.

7. **Sem _backfill_.** Declaração prática gravada antes desta change segue valendo com as colunas
   nulas, como a fatia 26 fixou para os três campos do Mestre, e a leitura dos bytes dela responde
   404. Prático antigo sem forma declarada aceita a declaração sem comprovação, porque não há
   forma contra a qual exigir.

## Risks / Trade-offs

- **A submissão do prático fica BREAKING** → os dois clientes são as Apps 01 e 05 e entram nesta
  change; o teste de cada uma afirma o corpo novo.
- **Vídeo de 200 MB no aparelho da criança, em rede ruim** → é o teto que a criação original já
  pratica, e o envio é retomável com progresso; a alternativa presencial do `RN-05-51` é a saída
  de quem não consegue enviar, e por isso ela não é cortesia, é parte do desenho.
- **A comprovação é mídia de criança que pode ir a público** → nesta change ela é servida só a
  quem entregou e ao Mestre autor, com 403 para o resto; o portão público é da fatia 12 do PRD-03,
  e o aviso do `RF-05-92` é o que torna a guarda informada.
- **A tela do prático cresce dentro de um componente que já pagina o quiz** → o ramo é apartado
  por `ehQuiz`, que já existe, e o formulário do prático nasce em função própria no mesmo arquivo,
  sem tocar a paginação.
- **`EntregaDeCriacao.tsx` da App 05 não lista `audio` em `TIPOS_COM_ENVIO`**, embora o áudio já
  seja o sexto tipo desde a fatia do núcleo → lacuna **preexistente** da criação original,
  registrada aqui e **não consertada** nesta change, que não toca a culminância.

## Migration Plan

Uma revisão Alembic acrescenta as cinco colunas anuláveis a `desbloqueio_da_missao`. Não há
_backfill_ e não há dado a reescrever, de modo que a reversão é o `downgrade` que as derruba. O
teste de paridade entre `alembic upgrade head` e `Base.metadata`, que a migração das tabelas de
recompensa de marco deixou na suíte, cobre a revisão nova.
