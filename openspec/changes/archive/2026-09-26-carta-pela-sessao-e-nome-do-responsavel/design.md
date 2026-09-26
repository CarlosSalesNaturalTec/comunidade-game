# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa ter à mão:

- `GET /v1/rankings/{comunidade}` já busca o `VinculoJogador` vigente de quem pergunta e
  recusa com 403 quando a comunidade da URL não bate com ele. A comunidade recebida de fora é
  **conferida contra** a que o núcleo já tem, nunca usada em lugar dela.
- A derivação do ranking (`consulta_de_ranking`) liga os pontos por `outerjoin`: Guerreiro(a)
  sem ponto algum aparece com total zero e posição atribuída. Não há caso de "ainda não está
  no ranking".
- `openspec/specs/responsavel-e-vinculo` já exige o nome no cadastro de responsável desde
  2026-08-24. O recorte (2) não decide nada: alinha a App 03 a uma regra vigente.

## Goals / Non-Goals

**Goals:**

- A carta e o ranking do Guerreiro(a) dependem só do que todo Guerreiro(a) tem: sessão e
  vínculo.
- Um caminho só para "quem sou eu" e um caminho só para "onde estou na turma", consumidos
  igual pelas Apps 01 e 05.

**Non-Goals:**

- Alterar a derivação do ranking, a ordenação, os filtros ou a paginação.
- Alterar o ranking público da vitrine, que deriva de outra regra.
- Entregar a lista de responsáveis cadastrados na App 03.

## Decisions

**1. `GET /v1/eu` ganha nick e avatar, servidos só ao Guerreiro(a).** Os campos saem quando o
papel não é Guerreiro(a), no mesmo padrão que `divulgacao_autorizada` e
`tem_pin_de_confirmacao` já usam nessa resposta — a leitura não muda de forma para ninguém.
_Descartado:_ rota nova só para a identidade, que duplicaria a leitura que toda aplicação já
faz na entrada.

**2. `GET /v1/eu/ranking` substitui `GET /v1/rankings/{comunidade}`.** A comunidade sai da URL
e vem do vínculo vigente — o mesmo que a rota já lê para conferir. O prefixo `/v1/eu/…` é o
que as outras vinte rotas do PRD-05 §9 usam para "o Guerreiro(a) em sessão"; a rota antiga era
a única exceção, e é justamente a que obrigou as telas a descobrir a comunidade antes de
perguntar. Filtros e paginação seguem idênticos.
_Descartado:_ manter a rota antiga e só aceitar `minha` no lugar do identificador — dois
contratos para a mesma leitura, e a adivinhação continuaria possível.

**3. A rota antiga é aposentada, não mantida em paralelo.** Os dois únicos consumidores
(`comum/carta` e a carteira da App 05) passam à rota nova na mesma change, e nada mais a
chama. Mantê-la viva significaria manter viva a conferência redundante que causou o defeito.
_Ponto para o fundador confirmar na revisão:_ a rota é logada e restrita ao Guerreiro(a), fora
do alcance das chaves de terceiro, que leem a vitrine pública — a aposentadoria não quebra
integração externa. Havendo preferência por depreciar em vez de remover, é o único ponto desta
change que muda.

**4. A carta deixa de ler as séries de coleta.** `comum/carta` passa a montar de `GET /v1/eu`
(nick, avatar) e `GET /v1/eu/ranking` (desempenho), mantendo progresso e portfólio como estão.
A regra de carta completa **não** é afrouxada: o documento 11 §8.2 exige o desempenho na
variante, e o que muda é a leitura passar a devolvê-lo sempre, não a exigência cair.
_Descartado:_ dispensar o desempenho de `cartaEstaCompleta` — contraria o §8.2 e foi
descartado pelo fundador.

**5. A App 03 ganha o campo de nome, e o teste deixa de dublar o cadastro.** O teste que cobre
o formulário afirma o **corpo enviado ao núcleo**, em vez de substituir a função que o monta:
foi o `vi.spyOn` sobre `cadastrarResponsavel` que deixou o defeito atravessar o CI por um mês.

## Risks / Trade-offs

- **A aposentadoria da rota antiga é quebra de contrato** → é logada e restrita ao
  Guerreiro(a); os dois consumidores mudam na mesma change, e o PRD-05 §9 registra a troca.
  Submetido ao fundador na decisão 3.
- **`GET /v1/eu` passa a tocar o nick e o avatar em toda chamada** → é a leitura mais chamada
  da plataforma; a busca é por identificador da persona em sessão, sem varredura, e não abre
  consulta nova por requisição além da que já existe.
- **Guerreiro(a) sem vínculo vigente** → a leitura do ranking recusa, e a carta cai no aviso,
  como hoje. Não é regressão: Guerreiro(a) sem vínculo já não tinha ranking, e o vínculo é
  obrigatório por `persona-e-credencial`.
- **A carta passa a aparecer onde antes não aparecia** → é o objetivo, mas amplia a
  superfície visual das Apps 01 e 05 para todo Guerreiro(a) novo; os testes das duas telas
  afirmam a carta montada com desempenho zerado.

## Migration Plan

Sem migração de dados: nenhuma entidade, coluna ou índice muda. A ordem dentro da change é
núcleo primeiro (as duas rotas), depois `comum/carta`, depois as telas das Apps 05, 01 e 03 —
a rota antiga sai só depois que o último consumidor passa à nova, para a suíte nunca ficar
vermelha no meio.
