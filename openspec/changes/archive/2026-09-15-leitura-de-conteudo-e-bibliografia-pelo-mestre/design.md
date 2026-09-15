## Context

Ver `proposal.md` — Why. O que o desenho precisa considerar:

- `MissaoSaida.conteudos` e a saída da bibliografia já existem como campo e como tipo; a rota
  pública (`obter_trilha_publica_rota`) já os popula corretamente, no mesmo laço de missões.
  `listar_minhas_trilhas_rota` só não chama as mesmas funções.
- `GET /v1/trilhas/minhas` já devolve `MissaoDoMestreSaida`, subclasse de `MissaoSaida`
  exclusiva do Mestre autor — a mesma que a change `2026-09-12-leitura-do-desafio-de-desbloqueio-pelo-mestre`
  usou para aninhar o desafio de desbloqueio pelo mesmo motivo.
- `saida_da_bibliografia_publica` deriva `disponivel` e `apoiador_nome` a partir de
  `ler_disponibilidade_e_credito(sessao, bibliografia, ponto_de_apoio_id=...)`. Sem
  `ponto_de_apoio_id`, a função já devolve `disponivel=None` (indeterminado) e ainda assim
  resolve `apoiador_nome` quando o exemplar tem aporte de origem — o crédito não depende do
  ponto de apoio, só a disponibilidade depende.
- A tela do Mestre (`Bibliografia.tsx`) hoje lê `entrada.disponivel` como booleano puro:
  `{entrada.disponivel ? "disponível" : "não disponível"}`. Isso nunca foi exercitado com dado
  real, porque a leitura nunca trouxe bibliografia de volta — é código morto que esta change
  ativa.

## Goals / Non-Goals

**Goals:**

- O Mestre autor relê o conteúdo e a bibliografia que já gravou, em qualquer sessão, do mesmo
  jeito que já relê o desafio de desbloqueio.
- A leitura da bibliografia ao Mestre autor nunca afirma disponibilidade que não pode
  determinar, mesmo depois de passar a trazer o campo.

**Non-Goals:**

- Rota nova de leitura. Não se cria porta onde a existente já é do autor.
- Mudar como a disponibilidade e o crédito são derivados (`bibliografia-da-missao` já fixa
  isso) — só estende onde a derivação é chamada.
- Tocar o upload, a trava de fonte do conteúdo de terceiro ou a leitura pública — já corretos.
- Mudar o formato de `ConteudoSaida` ou `BibliografiaPublicaSaida` — reaproveitados como estão.

## Decisions

**1. `listar_minhas_trilhas_rota` passa a chamar as mesmas funções que a rota pública já usa.**
`conteudos=consultar_conteudos_da_missao(sessao_bd, missao.id)` e, para a bibliografia,
`consultar_bibliografia_da_missao` seguido de `saida_da_bibliografia_publica` por entrada —
literalmente o mesmo par de chamadas do laço em `obter_trilha_publica_rota`. _Descartada:_
escrever uma consulta nova só para o Mestre — duplicaria a que já existe e teria de ser
mantida em dobro.

**2. A bibliografia ao Mestre autor reaproveita `BibliografiaPublicaSaida`, com
`ponto_de_apoio_id=None`.** O Mestre não lê como um Guerreiro(a) de um ponto de apoio
específico — não há qual ponto de apoio usar. Passar `None` é o comportamento que
`ler_disponibilidade_e_credito` já trata: disponibilidade fica indeterminada, e o crédito ao
Apoiador continua resolvido quando existe aporte de origem, porque não depende do ponto de
apoio. _Descartada:_ um tipo `BibliografiaDoMestreSaida` sem `disponivel`/`apoiador_nome` — a
`area-do-mestre` spec já promete o crédito ao Mestre ("Havendo vínculo, a aplicação SHALL
apresentar ao Mestre [...] o Apoiador creditado"), e omitir os campos privaria o Mestre do
crédito que a função já sabe calcular.

**3. A tela do Mestre passa a tratar `disponivel` como três estados, não dois.**
`Bibliografia.tsx` (`apps/app-09-mestre/src/trilhas/Bibliografia.tsx`) usa hoje um ternário que
trata `disponivel` ausente como `false` — "não disponível". Depois da decisão 2, toda entrada
vinculada chega com `disponivel: null` (nunca `true` nem `false`, porque não há ponto de apoio
na leitura do autor), e o ternário passaria a **afirmar indisponibilidade que não existe**,
contrariando o que `bibliografia-da-missao` já promete ("a leitura NEVER SHALL afirmar nem
negar disponibilidade" quando o dado não pode ser determinado). A tela passa a distinguir
`disponivel === true`, `disponivel === false` (não se aplica à leitura do Mestre, mas o tipo
permite) e `disponivel == null`, mostrando neste terceiro caso que a disponibilidade depende do
ponto de apoio de cada Guerreiro(a), sem afirmar nem negar. _Descartada:_ deixar o ternário
como está — introduziria uma informação falsa exatamente pelo conserto desta change.

**4. O *merge* local em `onSalvo`/`onSalva` permanece.**
Ele continua a dar feedback imediato de gravação sem esperar um novo carregamento da trilha
inteira — a mesma razão pela qual `DesafioDeDesbloqueio.tsx` manteve o padrão equivalente na
change anterior. O que muda é só a fonte inicial: a lista deixa de nascer vazia e passa a
nascer com o que a leitura trouxe, e o *merge* local segue acrescentando o que é gravado
durante a sessão em curso. _Descartada:_ remover o merge e recarregar a trilha inteira a cada
gravação — troca uma resposta imediata por uma viagem de rede extra a cada conteúdo ou entrada
de bibliografia.

**5. O comentário que documenta a ausência como intencional sai junto do conserto.**
`api.ts` afirma hoje que `conteudos` "nunca vem de `GET /trilhas/minhas` [...] no mesmo padrão
que `culminancia`". Deixá-lo faria o código descrever o defeito como projeto — mesma lição já
registrada na change do desafio de desbloqueio.

## Risks / Trade-offs

- **A resposta de `/trilhas/minhas` cresce com o conteúdo e a bibliografia de todas as missões
  de todas as trilhas do Mestre** → mesmo trade-off já aceito para o desafio de desbloqueio; o
  teto prático do Ciclo 01 é baixo, e o conteúdo com arquivo já trafega só a referência, nunca
  os bytes.
- **Reaproveitar `BibliografiaPublicaSaida` com `ponto_de_apoio_id=None` espalha o conceito de
  "indeterminado" para mais uma tela** → aceito porque é o mesmo dado, com o mesmo significado,
  que a leitura pública já produz sem `ponto_de_apoio_id`; não é comportamento novo, só um
  chamador novo.
- **A tela precisa de um terceiro estado visual para disponibilidade** → o texto exato é
  detalhe de tela, não de contrato; a spec só exige que a tela não afirme nem negue o que não
  sabe.

## Migration Plan

Nenhuma migração de banco — a change só estende o que duas rotas já leem e escrevem. Rollback é
reverter o commit: nenhuma coluna, tabela nem contrato de escrita muda.

## Open Questions

Nenhuma que trave a implementação.
