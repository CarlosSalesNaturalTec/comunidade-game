## Context

Ver `proposal.md` — Why. Das quatro fatias anteriores já existem: middleware de chave em toda
rota sob `/v1`, corpo único de erro com código, mensagem e campo, `Persona` em tabela única com o
papel como discriminador, `Sessao` opaca conferida no banco, mixin `ComAutoria` e a matriz de
permissões declarativa.

Duas coisas do que já existe moldam esta fatia. A matriz de `permissoes.py` **já traz**
`Operacao.suas_trilhas_e_conteudos` no conjunto de escrita do Mestre: o vocabulário nasceu
completo na fatia 2, e o que falta não é a operação, é o **objeto** dela. E `Consentimento.tipo`
firmou o padrão de campo que os documentos declaram como lista aberta: `String`, com o valor
conferido na regra, sem virar enumeração fechada.

A restrição que domina o desenho é `RN-01-42`: a trilha é bem comum da plataforma. Ela é a
primeira entidade do núcleo que **não** carrega comunidade, contra o hábito das quatro fatias
anteriores, em que quase tudo filtra por ela.

Esta fatia não entrega nenhuma rota — as de autoria são do PRD-09. O módulo nasce com modelo e
regra, como `consentimentos/` nasceu na fatia 3.

## Goals / Non-Goals

**Goals**

- Fazer a ausência de comunidade na trilha ser propriedade do esquema, conferível por teste, e
  não convenção que a próxima fatia esquece.
- Deixar a reordenação das missões possível para o PRD-09 **sem** migração de estrutura depois.
- Separar a conferência de **papel** da conferência de **posse**, sem inchar a matriz.
- Deixar o catálogo de poderes cadastrável em produção, sem _deploy_ para acrescentar poder.

**Non-Goals**

- Rotas de autoria, travas de publicação e despublicação: são do PRD-09 (ver `proposal.md`).
- Pontuação, níveis, badges e resultado: dependem de coleta (PRD-08) e culminância (PRD-09).
- Lastro da atividade (`RN-01-07`): precisa dos recursos do PRD-07.
- **Livro-razão**: esta fatia não tem operação com custo — é cadastro, sem consumo de modelo de
  IA nem de armazenamento. O lançamento de _cloud_ entra com os _uploads_ de `RF-09-20`.
- **Série temporal**: não há dado de território nesta fatia; ela chega com o PRD-08.

## Decisions

### O poder é tabela cadastrada, não enumeração no código

`RF-01-62` põe o catálogo sob cadastro de Admin, e enumeração em código exigiria _deploy_ para
acrescentar poder — o oposto do que o requisito pede. A tabela `poder` guarda nome, descrição, a
**natureza** e a **vigência**.

A natureza é enumeração fechada de dois valores — `de_guerreiro` e `derivado_do_aporte` —, porque
o documento 02 §2 nomeia exatamente esses dois comportamentos e `RN-01-43` transforma a distinção
em recusa. A vigência é enumeração de `vigente` e `ciclo_futuro`, o par que o documento 02 §2
marca; ela é descritiva e não trava vínculo de trilha.

Alternativa descartada: `booleano recebe_trilha` no lugar da natureza — diz o efeito e esconde o
motivo, e o motivo é o invariante 21.

### Os três eixos da atividade: dois fechados, um aberto

Modalidade e formato viram `enum.StrEnum`, porque o documento 11 §4 lista os valores por extenso
e não os declara extensíveis. **Natureza** vira `String`, com o valor conferido na regra e não no
banco: o mesmo documento diz, com todas as letras, que é **lista aberta** — trilhas de outras
áreas acrescentam naturezas —, e é o padrão que `Consentimento.tipo` já firmou.

Alternativa descartada: natureza como enumeração com valor `outra` — obriga migração a cada
trilha de área nova, que é justamente o que a lista aberta evita.

### A posição da missão tem unicidade adiável

`missao` carrega `posicao` inteira, com unicidade em `(trilha_id, posicao)` declarada
**`DEFERRABLE INITIALLY IMMEDIATE`**. Reordenar missões é trocar posições, e qualquer troca passa
por um estado intermediário em que duas missões dividem a mesma posição; com a restrição adiável,
o PRD-09 reordena dentro de uma transação sem que o núcleo precise de migração para acomodá-lo.

Alternativas descartadas: posições espaçadas de 10 em 10 — adia o problema até o rebalanceamento;
sem restrição alguma, com a ordem conferida só na regra — perde a garantia no banco, onde ela é
barata.

### A sondagem é declarada, não deduzida da posição

`missao` carrega `e_sondagem` booleana, com **índice único parcial** por trilha — uma sondagem por
trilha — e a conferência de primeira posição na regra. Deduzir a sondagem da posição 1 faria
qualquer missão que chegasse ao topo virar sondagem sem o Mestre declarar, e o documento 11 §2.2
põe a declaração no Mestre.

A conferência de que a trilha **tem** sondagem não entra: `RF-09-82` a faz na publicação, e a
_spec_ prevê o rascunho existindo sem ela.

### Papel e posse são duas conferências, não uma

`conferir_permissao` continua respondendo "este papel pode esta operação". A posse — "esta trilha
é deste Mestre" — entra como função própria em `trilhas/regra.py`, aplicada depois da matriz.
Somar a posse à matriz obrigaria a matriz a conhecer entidade, e a docstring dela diz o contrário:
a matriz é dado, não decisão espalhada.

Como esta fatia não tem rota, a posse nasce como função de regra, coberta por teste. O PRD-09 a
pendura na dependência da rota que criar, sem reescrever a regra.

Alternativa descartada: uma `Operacao.trilhas_de_outro_mestre` na matriz — inverte a leitura da
tabela do PRD-01 §4, que concede, não proíbe.

### A ausência de comunidade na trilha é testada, não combinada

Um teste afirma que a tabela `trilha` não tem coluna de comunidade, no mesmo formato dos testes de
"nenhum existe" das fatias anteriores. É o que impede a próxima fatia de acrescentar o vínculo por
hábito e passar no _lint_.

## Risks / Trade-offs

- **Natureza aberta acumula variação de digitação** ("construção" e "construcao" como naturezas
  distintas) → a regra normaliza antes de gravar; o catálogo sugerido pelo template de `RF-09-85`
  reduz a digitação livre quando o PRD-09 chegar.
- **A posse fica sem rota que a exercite nesta fatia** → coberta por teste de regra; o risco real
  seria o PRD-09 reimplementar a conferência, e é o que a função nomeada evita.
- **Unicidade adiável é sutil** → quem lê a migração precisa entender por que ela é adiável; o
  comentário da migração aponta a reordenação de `RF-09-02` como motivo.
- **A trilha sem comunidade destoa do resto do núcleo** → é decisão gravada (`RN-01-42`,
  documento 02 §3), e o teste de ausência de coluna a mantém explícita.

## Open Questions

- Se a **natureza** da atividade merecerá catálogo normalizado quando a cobertura de ODS
  (`RF-01-42`) começar a agregar por ela. Nada nesta fatia muda de forma: a coluna continua
  `String`, e a normalização, se vier, é migração de dado.
- Quais índices a consulta pública de trilhas vai exigir. A fatia não expõe rota pública, e o
  desenho de índice se decide com a consulta real do PRD-03.
