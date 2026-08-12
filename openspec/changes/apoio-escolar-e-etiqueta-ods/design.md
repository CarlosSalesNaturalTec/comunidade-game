## Context

Ver `proposal.md` — Why. Do que já existe: `trilhas.regra.conferir_posse_da_trilha` (Mestre autor
ou Admin), o padrão de posse por autoria (`ComAutoria`), a normalização de campo aberto
(`trilhas.regra._normalizar_natureza`) e a operação `suas_trilhas_e_conteudos`, já concedida ao
Mestre na matriz desde a fundação — nenhuma das duas capacidades desta fatia precisa de operação
nova.

Duas frentes sem relação de dependência entre si: apoio escolar (corpus) e etiqueta ODS. Cada
uma vira um módulo próprio, sem tocar `trilhas/` além de referenciá-lo por chave estrangeira.

## Goals / Non-Goals

**Goals**

- Deixar o corpus cadastrável em produção, com o mesmo rigor de posse que trilha, missão e
  atividade já têm — sem inventar uma segunda forma de conferir autoria.
- Modelar a etiqueta como rótulo puro: presente no esquema, ausente de qualquer cálculo de
  pontuação, nível ou badge.
- Deixar a agregação de cobertura correta hoje (Ciclo 01, um ciclo só) sem fechar a porta para a
  dimensão de ciclo, quando ela existir.

**Non-Goals**

- `Consulta` (a terceira entidade de `RF-01-35`) e qualquer chamada ao Gemini: sem produtor nem
  mecanismo de expurgo por prazo no núcleo (ver `proposal.md`).
- Rota de cadastro, de despublicação ou de consulta pública: nenhuma nasce nesta fatia.
- Propagação da etiqueta para desafio de coleta ou desafio extra (`RF-01-41`): os alvos não
  existem.
- Trava de publicação sem etiqueta a partir do Ciclo 02 (`RF-01-44`): é rota do PRD-09.

## Decisions

### Disciplina não tem posse; Conteúdo tem

A matriz do PRD-01 §4 concede "suas trilhas **e conteúdos**" ao Mestre — o possessivo mira o
conteúdo, não a disciplina. Disciplina é taxonomia (como "natureza" da atividade já é lista
aberta): qualquer Mestre a usa e a estende, e um catálogo fragmentado por autor duplicaria
"Matemática" a cada Mestre novo. Conteúdo é texto de ensino, autoral como trilha e missão: a
posse impede um Mestre reescrever o material de outro sem passar pelo Admin.

Alternativa descartada: disciplina com posse, no padrão do conteúdo — obrigaria cada Mestre a
recriar as mesmas disciplinas, e o documento 03 §7 não distingue entre os dois ao dizer "os
Mestres" cadastram o corpus.

### Despublicação é campo no Conteúdo, não situação de fluxo

`Conteudo` carrega `despublicado_em`, `despublicado_por_id` e `motivo_da_despublicacao`,
opcionais — presentes só quando o Admin age. Não há campo `situacao` com rascunho/publicado: o
conteúdo nasce **publicado** (o Mestre não passa por aprovação prévia, ao contrário da trilha,
que nasce em rascunho) e só o Admin o tira de circulação, sempre com motivo. Content
"publicado" é só a ausência de `despublicado_em`.

Alternativa descartada: enumeração de situação com três valores (publicado, despublicado,
rascunho) — a trilha tem rascunho porque o Mestre a constrói aos poucos antes de abrir para a
turma; o corpus, pelo documento 03 §7, já nasce disponível ao assistente.

### Etiqueta ODS referencia trilha ou missão por duas colunas opcionais, com `CheckConstraint`

`trilha_id` e `missao_id`, ambas anuláveis, com restrição de banco que exige exatamente uma
preenchida — o mesmo padrão de "exatamente um dos dois" que `PontoExtra` já não precisou (é
sempre por Guerreiro(a)), mas que aqui é real: a etiqueta é ou de trilha ou de missão, nunca as
duas, e a restrição no banco torna a regra impossível de violar por qualquer caminho de escrita,
não só pelo que a regra de aplicação cobre.

Alternativa descartada: tabela única de "etiquetável" com tipo e id genérico — ganha
flexibilidade que ninguém pediu e perde a chave estrangeira de verdade, que o banco confere
sozinho.

### A meta é `String` opcional, não estruturada

O documento 11 §2.1 dá exemplos de meta como texto livre (`4.7`, `13.3`, `17.18`) "quando o
Mestre souber" — não é número nem enumeração fechada, e nem toda etiqueta tem uma. `String`
opcional, sem normalização: ao contrário da natureza da atividade e do nome da disciplina, a meta
não é chave de agrupamento, só anotação.

### Cobertura é função de consulta, sem tabela de agregado

`cobertura_por_trilha`, `cobertura_por_poder` e `cobertura_por_comunidade` leem `EtiquetaOds`,
`Trilha`, `Missao` e — para a de comunidade — `Resultado` e `Persona`, e devolvem o conjunto de
objetivos na hora. `RN-01-24` já declara "sobe por agregação... sem lançamento manual": nenhuma
tabela de cobertura precisa existir separada da fonte, e persistir um agregado hoje só criaria
mais uma coisa para desatualizar quando uma etiqueta nova entrar.

A dimensão de **ciclo** não entra como parâmetro: o núcleo não modela mais de um ciclo, e a
assinatura das três funções fica pronta para recebê-lo como filtro quando o Ciclo 02 chegar, sem
mudar o que já existe.

Alternativa descartada: view materializada ou tabela de cache — otimização para uma consulta que
ainda não tem rota nem volume que a justifique.

## Risks / Trade-offs

- **Disciplina sem posse pode ser editada por qualquer Mestre depois de criada** → aceitável: é
  taxonomia compartilhada, e o Admin audita por amostragem como já faz com o corpus.
- **Cobertura por comunidade percorre `Resultado` a cada chamada** → sem rota ainda, sem
  volume real para medir; índice fica para quando a consulta pública (fatia da vitrine) existir.
- **`CheckConstraint` de "exatamente um dos dois" é menos comum que um FK simples** → o comentário
  do modelo aponta a razão, e o padrão já existe em `Missao.e_sondagem` (índice único parcial),
  então não é o primeiro caso de restrição de banco carregando uma regra de negócio no núcleo.

## Open Questions

Nenhuma. As duas lacunas encontradas ao desenhar esta fatia — se a disciplina teria posse e como
representar "trilha ou missão, nunca as duas" — já estão resolvidas acima.
