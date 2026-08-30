## Context

Ver `proposal.md` — Why. O que restringe o desenho e já está resolvido em
`openspec/specs/`:

- A autoria da trilha, a missão, a atividade, a cadência de retomada e a etiqueta ODS já têm
  rota, recusa e tela (`trilha-e-missao`, `atividade-de-trilha`, `etiqueta-ods`,
  `area-do-mestre`). O template **não** ganha caminho de gravação próprio.
- `conteudo-da-missao` já firmou o precedente de recurso de nuvem sem medição por ato, e
  `armazenamento/` já firmou o desenho de porta com adaptador local fora de produção e
  adaptador de nuvem em produção.
- `desbloqueio-da-missao` já grava o fato `DesbloqueioDaMissao(guerreiro, missao, aprovado,
  julgado_por)`, com o prático em aberto até o julgamento do Mestre autor.
- `recompensa-de-marco` já tem declaração, entrega, baixa no livro-razão e as cinco recusas; o
  que muda é **de onde vem o marco alcançado**.
- O `Poder` já traz `natureza`, `vigencia`, `papel` e `ativo`, com o papel declarado por Admin
  e nunca deduzido do nome (`RN-01-54`).

## Goals / Non-Goals

**Goals:**

- O template pede ao modelo só o que é redação livre — a estrutura e o ODS — e confere no
  núcleo tudo o que é fato da missão.
- O núcleo funciona, na esteira e em desenvolvimento, **sem credencial de nuvem**.
- O marco alcançado passa a ser o desbloqueio numa única derivação, usada pela recusa da
  entrega, pela leitura do Guerreiro(a) e pela fila do Mestre.

**Non-Goals:**

- Cache, cota, fila ou repetição automática do pedido ao modelo: sem medição de consumo
  (`RF-09-90`), não há o que orçar; a indisponibilidade avisa e o Mestre segue à mão.
- Versionar ou comparar sugestões: a `SugestaoDeEstrutura` é registro do que foi proposto, não
  estado da missão.
- Migrar entrega já registrada: a mudança do marco alcançado altera quem **pode** receber
  daqui em diante, nunca o que já foi entregue.

## Decisions

**1. O modelo propõe; o núcleo confere.** A estrutura sugerida (`RF-09-85`) e a etiqueta ODS
(`RF-09-95`) saem do modelo; as **lacunas** (`RF-09-86`), a exigência de atividade desplugada
(`RF-09-88`) e a cadência de 2, 7 e 21 dias (`RF-09-116`) são calculadas pelo núcleo sobre o que
está gravado na missão e no poder da trilha. Lacuna é fato, não opinião: um modelo que
alucinasse lacuna inexistente mandaria o Mestre corrigir o que está certo. Descartado deixar
tudo com o modelo, e descartado montar a estrutura sem modelo algum — o documento 03 §11 diz que
a IA da autoria monta a estrutura.

**2. Porta e adaptadores, no padrão de `armazenamento/`.** `template_de_missao/porta.py` define o
contrato; `fabrica.py` escolhe pelo ambiente; o adaptador de produção fala com a API do Gemini
(documento 03 §1.12) e o adaptador local devolve estrutura fixa a partir do tópico, sem rede. A
esteira e o desenvolvimento rodam sem credencial, como o `ArmazenamentoEmDisco` já faz.
Descartado chamar o Gemini direto da regra (testa mal) e descartado chamar do frontend (a chave
do modelo não vai ao navegador).

**3. A indisponibilidade do modelo é resposta 200 com sugestão vazia, nunca 5xx.** As lacunas o
núcleo entrega de qualquer modo, e o template nunca é etapa obrigatória da autoria
(`RF-09-91`). Devolver erro faria a tela parecer quebrada por uma função que é auxílio.
Descartado 503 e descartado repetir o pedido em silêncio.

**4. `SugestaoDeEstrutura` é registro, não estado.** Uma linha por pedido, com missão, tópico,
estrutura proposta (JSON), lacunas apontadas e situação — `proposta`, `aceita`, `recusada`,
`alterada` (PRD-09 §8). Pedir de novo grava linha nova. A situação é escrita pela App 09 quando
o Mestre age; **nada** na missão é alterado por esta entidade. O atributo "custo de _cloud_
lançado" que o PRD-09 §8 lista fica **fora**: o `RF-09-90` — essencial, e repetido pela `RN-09-07`
— proíbe medir, e a coluna só existiria para ficar vazia. A `conteudo-da-missao` já resolveu a
mesma tensão do mesmo modo. A linha do PRD-09 §8 é corrigida nesta change, como **correção de
rastreabilidade** e não decisão nova, no formato que o próprio PRD já usa no fim da §13.

**5. Marca de técnico é coluna própria do `Poder`, não valor de `papel`.** `papel` admite um
único valor por poder e no máximo um poder com o papel do Território; ser técnico é outro eixo,
alcança vários poderes e convive com o papel. Boolean `tecnico`, padrão falso, declarado e
alterável por Admin — alterável porque dela não deriva vínculo nem crédito, só a próxima
sugestão (ao contrário de `natureza` e `papel`). Descartado deduzir do nome (proibido pela
`RN-01-54`) e descartado perguntar ao Mestre no pedido (nenhum documento lhe atribui isso).

**6. Marco alcançado = desbloqueio aprovado.** Uma função em
`trilhas/regra.py` — `missoes_desbloqueadas_pelo_guerreiro(guerreiro_id, trilha_id)`, que devolve
as missões com `DesbloqueioDaMissao.aprovado is True` — substitui
`missoes_concluidas_pelo_guerreiro` nos três pontos de `recompensas_de_marco/regra.py`. A função
antiga **permanece** onde nasceu: ela é do motor de níveis (`pontos-niveis-e-badges`), que conta
percurso por `Resultado`, e continua correta lá. Prático não julgado (`aprovado is None`) não
alcança o marco, coerente com "aguardando o Mestre, nunca reprovada".

**7. A fila de pendências é da comunidade, não da autoria.** Quem entrega é o Mestre vinculado à
Comunidade Virtual do Guerreiro(a) — é a condição que a entrega já exige. Filtrar pela autoria da
trilha deixaria recompensa conquistada sem ninguém para entregá-la no encontro. A fila reusa o
mesmo `VinculoJogador` vigente que `_validar_entrega` já consulta.

**8. Duplicação copia a árvore de autoria e nada de pessoa.** Uma transação: `Trilha` nova em
rascunho com autor de quem duplicou e nome marcado como cópia, as `Missao` com posição, título,
dificuldade, obrigatoriedade, sondagem, etapa, cadência e as colunas do desafio de desbloqueio, e
as `Atividade` de cada missão. Ficam de fora inscrição, desbloqueio, resultado, criação original,
recompensa de marco, entrega, desafio de coleta, conteúdo, bibliografia, culminância, etiqueta e
auditoria — o que é fato de pessoa ou lastro da origem. Conteúdo e culminância ficam de fora
porque a cópia não publica: a trava de publicação da `trilha-e-missao` cobra os dois de quem
duplicou, que é o autor da trilha nova. Descartado copiar tudo e apagar depois; descartado copiar
só a casca sem missões, que não seria ponto de partida.

**9. Rotas.** `POST /v1/missoes/{id}/estrutura` (PRD-09 §9), `GET /v1/recompensas-de-marco/
pendentes` e `POST /v1/trilhas/{id}/duplicacao`. A declaração da recompensa e a confirmação da
entrega usam as rotas que a fatia 10 do PRD-07 já entregou; a fatia 13 lhes dá tela.

## Risks / Trade-offs

- **A troca do marco alcançado muda quem pode receber.** → Guerreiro(a) com `Resultado` na missão
  mas sem desbloqueio deixa de constar como conquistador. É o que os documentos 03 §11 e 11 §2.2
  determinam, e nenhuma entrega já registrada é tocada. A troca entra na mesma change que dá tela
  à recompensa, para que a mudança apareça ao Mestre de uma vez.
- **O adaptador local devolve estrutura pobre.** → Ele existe para a esteira e para o
  desenvolvimento, não para a comunidade; a tela é a mesma nos dois, e o teste cobre o contrato,
  não a redação do modelo.
- **A resposta do modelo pode vir fora do formato.** → O adaptador valida o formato antes de
  devolver e, não validando, trata como indisponibilidade — a mesma resposta em linguagem simples
  da decisão 3, sem expor nada do provedor.
- **A duplicação de trilha grande é uma transação longa.** → Trilha do Ciclo 01 tem dezenas de
  missões e atividades, não milhares; se um dia crescer, a operação vira assíncrona sem mudar o
  contrato.

## Migration Plan

1. Migração Alembic única: tabela `sugestao_de_estrutura`, coluna `poder.tecnico` (padrão falso,
   não nula) e nada em `recompensa_de_marco` — a troca do marco alcançado é de regra, não de
   esquema.
2. O Admin marca o Poder da IA e Robótica como técnico pela App 03 depois da implantação; até
   lá, nenhuma trilha recebe sugestão de atividade desplugada, e nada mais muda.
3. Sem credencial do Gemini configurada, o núcleo sobe e opera: o template responde como
   indisponível e o restante da autoria segue inteiro.
4. Rollback: a migração desce sem perda — a `SugestaoDeEstrutura` é registro auxiliar e a marca
   do poder só alimenta sugestão.
