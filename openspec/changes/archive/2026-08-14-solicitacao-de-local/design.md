## Context

A pasta `backend/src/nucleo/locais/` já entrega a hierarquia de seis níveis e o cadastro direto
por Admin. Toda a validação de hierarquia que a aprovação precisa reusar — pai do nível
imediatamente acima, mesma comunidade, `comunidade` sem pai — vive **dentro** de
`cadastrar_local`, e a primeira linha dessa função recusa quem não é Admin. O Mestre que aprova
bate nesse portão antes de alcançar a validação.

A cadeia que define o avaliador já está montada e testada: `DesafioDeColeta.missao_id` →
`Missao.trilha_id` → `Trilha.autor_id`, conferida por `conferir_posse_da_trilha`, que aceita o
Admin e o Mestre autor e recusa qualquer outro com 403. É o mesmo caminho que a emissão da
credencial de dispositivo percorre, e `criar_desafio_de_coleta` já o exige na criação — de modo
que **autor do desafio e autor da trilha são a mesma persona por construção**, e a diferença de
redação entre o PRD-08 §9 ("Mestre que não é autor do desafio") e a jornada §5.3 ("Mestre da
trilha") não descreve duas pessoas.

## Goals / Non-Goals

**Goals:**

- Dar ao local uma segunda origem — a aprovação — sem duplicar a validação de hierarquia.
- Prender a solicitação à trilha pelo desafio de origem, para que o escopo do Mestre saia da
  cadeia que já existe, e não de uma regra transitória.
- Manter a `SolicitacaoDeLocal` com exatamente os atributos do PRD-08 §8.
- Preservar o filtro obrigatório por comunidade na lista de abertas, como na rota irmã
  `GET /locais`.

**Non-Goals:**

- Reusar a `fila-de-avaliacao`: a aprovação cria cadastro, o que aquela capacidade proíbe em
  toda situação, e o avaliador pode ser o Mestre — ver a proposal.
- Prazo de resposta, contagem de atraso ou qualquer ciclo herdado daquela fila.
- Consulta do Guerreiro(a) ao status da própria solicitação — ver Open Questions.
- Transferência de comunidade e qualquer efeito sobre `VinculoJogador`.

## Decisions

### Separar o portão de autorização do núcleo de validação da hierarquia

`cadastrar_local` passa a ser a casca que confere o papel Admin e delega; a validação de
comunidade, nível, rótulo e pai desce para uma função interna sem opinião sobre quem chama. A
aprovação entra por essa função interna, depois de passar pelo **seu** portão
(`conferir_posse_da_trilha`).

Assim as duas origens do local compartilham a mesma validação e a regra de hierarquia continua
escrita **uma vez** — o requisito modificado de `local-do-territorio` exige que as duas gravem
sob as mesmas regras, e duplicar o código seria o caminho mais curto para elas divergirem.

- _Alternativa descartada:_ dar ao Mestre o papel Admin na chamada interna — mentira de
  autorização que envenena a autoria e a trilha de auditoria.
- _Alternativa descartada:_ duplicar a validação na regra de avaliação — divergência garantida
  na primeira mudança de hierarquia.

### O local pai vem no corpo da avaliação

Decisão do fundador registrada na proposal. No desenho ela significa: o corpo de
`POST /solicitacoes-de-local/{id}/avaliacao` carrega `local_pai_id` quando o desfecho é
aprovação, e `motivo` quando é recusa. A `SolicitacaoDeLocal` **não ganha coluna de local pai** —
o pai é dado do ato de avaliar, não do pedido, e guardá-lo na solicitação criaria atributo que o
PRD-08 §8 não declara.

### A validação da hierarquia acontece antes de qualquer escrita do desfecho

Aprovação com pai inválido recusa com 422 e deixa a solicitação **em aberto**, sem avaliador nem
data gravados. O desfecho é um ato só: ou o local nasce e a solicitação fecha, ou nada acontece.
Evita o estado morto de uma solicitação marcada aprovada sem local correspondente.

### A solicitação guarda o local criado

O PRD-08 §8 desenha "vira Local se aprovada" e não nomeia atributo que ligue os dois. A
`SolicitacaoDeLocal` guarda o **local criado** na aprovação — escrituração de desenho, não regra
nova: é o que permite conferir, na auditoria e no teste, que a aprovação criou um local e um só,
e é o que sustenta o cenário "aprovação não cria um segundo local".

- _Alternativa descartada:_ deduzir o local por comunidade, nível e rótulo — quebra assim que
  dois locais irmãos tiverem o mesmo rótulo, que nada proíbe.

### A situação é um enum de três valores, e o desfecho é irreversível

`recebida`, `aprovada`, `recusada`. Só `recebida` admite transição, e apenas para as outras
duas. Não há reabertura, edição de motivo nem troca de avaliador — o PRD não os prevê, e a
irreversibilidade do desfecho é a mesma escolha que a invalidação de registro já segue no
domínio.

### O recorte por papel da lista sai da mesma cadeia do avaliador

A lista de abertas filtra por comunidade — obrigatório, via
`contrato_de_listagem(filtro_comunidade_obrigatorio=True)`, igual à rota irmã `GET /locais`. Em
cima disso, o Mestre recebe o recorte pelas trilhas de que é autor, pela junção
solicitação → desafio → missão → trilha; o Admin não recebe recorte adicional. Um caminho só,
com um predicado a mais para o Mestre — não duas consultas.

### A pasta é `locais/`

A solicitação é sobre o local, cria local e reusa a validação dele. `locais/regra.py` passa a
importar `coletas.modelo` e `trilhas` — não há ciclo, porque `coletas.modelo` importa apenas
`locais.modelo`, que é folha, e `trilhas` não importa `locais`.

- _Alternativa descartada:_ pasta própria `solicitacoes_de_local/` — dependência num sentido só,
  ao custo de separar a validação de hierarquia de quem a usa.

## Risks / Trade-offs

- **A refatoração de `cadastrar_local` toca código já entregue e testado** → a casca preserva a
  assinatura pública e o 403 para quem não é Admin; os testes vigentes de `local-do-territorio`
  passam sem alteração, e é isso que prova a refatoração.
- **`locais/regra.py` passa a alcançar `coletas` e `trilhas`, e os dois pacotes se tocam** →
  legal e sem ciclo hoje, mas é a primeira vez que `locais` deixa de ser folha. A dependência
  fica confinada à regra de solicitação e avaliação; `cadastrar_local` e `paginar_locais`
  seguem sem conhecer coleta.
- **Solicitação presa a um desafio cujo desafio some ou cuja trilha muda de autor** → o PRD não
  prevê exclusão de desafio nem troca de autoria de trilha, e nada no núcleo as implementa; a
  solicitação em aberto continua alcançável pelo Admin em qualquer caso.
- **Duas solicitações iguais em aberto na mesma comunidade** → o PRD não as proíbe e esta fatia
  não inventa a proibição; a aprovação da segunda cria um segundo local irmão, e cabe ao
  avaliador recusá-la com motivo.

## Migration Plan

Migração do Alembic criando `solicitacao_de_local`, com as chaves estrangeiras para persona,
comunidade, desafio de coleta e local criado. Tabela nova, sem dado preexistente e sem alteração
de tabela em uso — a refatoração de `cadastrar_local` não muda esquema. Rollback é o `downgrade`
que remove a tabela; as três rotas somem com ele e nenhuma outra depende delas.

## Open Questions

Nenhuma trava esta fatia. Uma fica anotada para a entrega da App 05:

**Por qual rota o Guerreiro(a) acompanha o status da própria solicitação?** `RF-05-32` diz que
ele "solicita a inclusão de local faltante **e acompanha o status da solicitação**", e o critério
de aceite do PRD-08 §12 diz que a recusa "devolve o motivo ao Guerreiro(a)". Mas a §9 do PRD-05
lista apenas `POST /v1/solicitacoes-de-local`, sem rota de leitura — enquanto lista
`GET /v1/eu/sugestoes` para o caso equivalente das sugestões. A lacuna é do PRD-05, não deste
recorte, e não se preenche dentro de um artefato do OpenSpec: é pergunta ao fundador quando a
App 05 entrar na esteira.
