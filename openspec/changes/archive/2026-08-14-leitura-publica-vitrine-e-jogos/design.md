## Context

Ver `proposal.md` — Why. O que o núcleo já oferece e condiciona o desenho:

- `incluir_roteador_de_dados` (`principal.py`) prende a **chave de aplicação** e a **cota de
  leitura** a todo roteador sob `/v1`. Um roteador novo entra por ela e nasce protegido, sem
  declarar nada.
- `exigir_freio_por_origem(superficie)` (`protecao/freio.py`) é fábrica de _dependency_. A
  superfície **`consulta_por_nick`** já existe, com limite e janela em `Configuracao`, e hoje
  só é exercitada por rota de teste em `tests/conftest.py` — nasceu esperando esta fatia.
- O corpo único de erro (`CorpoDeErro`: código, mensagem, campo) vem de `RF-01-27`, e o
  manipulador de `404` já devolve o código `nao_encontrado`.
- `Consentimento` é **somente inserção**, com `tipo` hoje em texto livre. Não há estado de
  vigência guardado em lugar nenhum.
- `Persona` é deliberadamente magra: `id`, `papel`, `comunidade_virtual_id`, `criada_por`,
  `criada_em`. O nick vive em tabela própria. **Não há nome civil no núcleo** — o que reduz
  bastante o que a fronteira pública precisa impedir de vazar.
- `Configuracao` (pydantic-settings, prefixo `CG_`) é onde vivem os parâmetros de implantação.

## Goals / Non-Goals

**Goals:**

- Uma só definição da projeção pública, por onde toda saída desta change passa.
- Um só predicado de autorização vigente, usado pela vitrine e pelos jogos.
- Paginação e posição de ranking corretas **depois** do portão, não antes.
- A ausência de rota de escrita para jogos verificável por teste, não por disciplina.

**Non-Goals:**

- Cache das respostas públicas. `RF-01-10` do PRD-01 §10 pede consulta cacheável, e a cota
  por chave já protege o pico; caching é fatia de operação, não desta.
- Interpretar as características do avatar. O núcleo as carrega; quem as define e as desenha
  é o PRD-04 e o PRD-05.
- Qualquer rota de escrita. Toda esta change é leitura.

## Decisions

### A projeção pública é um tipo, não uma seleção de campos por rota

O risco desta change é um campo pessoal atravessar a fronteira porque uma rota entre seis
montou a resposta à mão. A projeção nasce como **um módulo só** — `vitrine/publico.py` —, com
os tipos de saída pública e a função que converte domínio em saída. Nenhuma rota monta
resposta a partir de entidade do domínio; todas passam por ali, e o `response_model` do
FastAPI faz a segunda rede na serialização.

O módulo dos jogos importa **a mesma** projeção. É o que dá sentido literal ao invariante 8
("como na vitrine"): não é uma regra repetida em dois lugares, é o mesmo código.

- _Alternativa descartada:_ `response_model` por rota, montado caso a caso — seis chances de
  esquecer, e o contrato dos jogos seria uma sétima.
- _Alternativa descartada:_ filtro de serialização global por lista de campos proibidos —
  protege contra o que se lembrou de proibir, não contra o campo novo de uma fatia futura.

### O portão da divulgação entra na consulta, não depois dela

A spec exige que a exclusão de quem não autorizou **não deixe rastro**: sem posição vazia no
ranking e sem contagem que denuncie. Um pós-filtro sobre a página já lida entrega página curta
e posição furada — a segunda colocação sumiria em vez de ser ocupada por quem vem depois.

O predicado de vigência entra como **condição da consulta**, resolvido em SQL junto do
`LIMIT`/`OFFSET` e da numeração. Paginar e ranquear passam a operar sobre o conjunto já
visível.

- _Alternativa descartada:_ pós-filtro na aplicação — quebra os dois cenários de "não deixa
  rastro" e ainda faz N+1.

### A vigência é consulta derivada do histórico, sem coluna de estado

Guardar "está autorizado" em coluna duplicaria a verdade e brigaria com o somente inserção
que a capacidade já tem. A vigência se resolve assim: para o par Guerreiro(a) e tipo, toma-se
a **decisão mais recente de cada responsável vinculado**; a autorização está vigente quando
existe ao menos uma decisão e **nenhuma** delas é recusa (`RN-13-07` — a recusa prevalece).

Expressa como expressão SQL reutilizável, ela serve tanto ao `WHERE` das listagens quanto à
pergunta pontual do perfil por nick, sem dois caminhos que possam divergir.

- _Alternativa descartada:_ coluna `divulgacao_autorizada` mantida por gatilho — segunda
  fonte da verdade, e a pergunta "o que valia naquela data" deixaria de ter resposta.
- _Alternativa descartada:_ resolver em Python por Guerreiro(a) — N+1 em toda listagem.

### O 404 indistinto vem de não haver desvio para distinguir

A consulta do perfil por nick resolve **nick e vigência na mesma consulta**. Não existe um
ponto no código em que se saiba que o nick existe mas não está autorizado: as duas ausências
são o mesmo `None`, e o mesmo erro sobe. Não é uma decisão de mensagem — é a ausência do
desvio que poderia vazar a diferença por tempo de resposta ou por log.

Essa rota declara `exigir_freio_por_origem("consulta_por_nick")`, a superfície que
`RF-01-65` nomeia e que já está construída.

### Jogos em módulo próprio, com o prefixo que o teste de ausência vigia

`jogos/` é módulo separado de `vitrine/`, com prefixo de rota próprio. Não é organização por
gosto: é o que torna o requisito "não existe rota de escrita para jogos" **verificável**. O
teste percorre `app.routes`, filtra pelo prefixo e afirma que todo método é `GET` ou `HEAD`.
Fundidos num módulo só, a asserção não teria como se dirigir ao subconjunto certo, e a
proteção viraria revisão de código.

O mesmo teste vale como rede para as fatias futuras: quem acrescentar um `POST` ali quebra a
esteira, sem depender de alguém lembrar do invariante 8.

### O saldo disponível não é omitido — ele não entra

A projeção do progresso lê o **acumulado** direto da origem e não recebe o saldo em momento
algum. Omitir na saída um campo que o objeto carrega deixa o vazamento a uma linha de
distância; não carregá-lo torna `RN-01-41` uma propriedade da estrutura.

### O rótulo de ciclo é parâmetro, com valor inicial declarado

Entra em `Configuracao` como `CG_CICLO_ROTULO`, com `Ciclo 01` (invariante 13) como valor
inicial — mesmo tratamento da duração da sessão e do prazo de apresentação da chave. Nenhuma
entidade `Ciclo`, nenhuma dependência do calendário pendente no documento 09 §1.

### As características do avatar são opacas para o núcleo

O núcleo guarda as características e não as interpreta: nenhuma validação de forma, nenhum
conjunto de valores, nenhuma regra de composição. Quem define o que elas são é o PRD-04
(`RF-04-07`), e o núcleo não tem requisito que autorize inventar esse formato. Coluna de
texto estruturado, gravada e devolvida como veio.

- _Alternativa descartada:_ modelar traços do avatar em colunas — seria regra de produto
  criada dentro de um artefato do OpenSpec, o que a hierarquia proíbe.

## Risks / Trade-offs

- **A vigência em SQL fica sutil e é o portão de tudo.** → Ela vira uma expressão nomeada,
  testada isoladamente contra os cinco cenários da spec de `consentimento`, antes de qualquer
  rota usá-la.
- **A migração do `tipo` encontra valores livres já gravados.** → Não há implantação em
  produção, mas há base de desenvolvimento. A migração **falha alto** diante de valor fora do
  conjunto, em vez de mapear para um padrão — converter em silêncio um consentimento é
  exatamente o que o registro somente inserção existe para impedir.
- **Ranking sobre o conjunto filtrado muda de tamanho a cada revogação.** → É o comportamento
  correto pela spec, e a revogação tem efeito imediato por definição. A posição é sempre
  relativa ao que está visível, nunca ao total real.
- **Seis rotas novas ampliam a superfície de leitura de uma vez.** → Todas herdam chave, cota
  e corpo de erro sem declarar nada, e nenhuma escreve. O acréscimo de risco está na
  projeção, e é lá que a decisão a concentrou.

## Migration Plan

Duas migrações do Alembic, ambas aditivas:

1. `persona.avatar` — coluna nova, aceita nulo enquanto as personas existentes não o têm; a
   rota que o grava é do PRD-04, e quem não tem avatar simplesmente não aparece em público,
   por já não ter autorização de divulgação.
2. `consentimento.tipo` — restrição de conjunto fechado, com a verificação de valores
   existentes antes de aplicá-la.

Reversão: as duas migrações têm `downgrade`. Nenhum dado é destruído em nenhuma direção.

## Open Questions

1. **Se o rótulo de ciclo recebe linha no PRD-01 §13 e no documento 09.** Está em
   `proposal.md` — Questão aberta para o fundador. Não muda spec, desenho nem tarefa: muda
   uma linha de `docs/`, e a tarefa de documentação já a prevê como condicional.
