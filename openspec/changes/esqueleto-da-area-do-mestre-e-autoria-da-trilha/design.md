# Design — esqueleto da Área do Mestre e autoria da trilha

## Context

Ver `proposal.md` — Why. O que molda o desenho:

- `trilhas/regra.py` já tem `criar_trilha`, `criar_missao`, `criar_atividade`,
  `consultar_trilhas` e `conferir_posse_da_trilha`, com as recusas da spec implementadas e
  cobertas. **31 arquivos de teste** montam os próprios cenários chamando essas funções: mudar
  a assinatura delas é caro, reexpô-las não custa nada.
- O PRD-09 §9 declara as rotas desta fatia. Não declara rota de leitura de missão nem de
  atividade, e não declara rota de edição de nenhuma das três.
- A App 03 tem **61 chamadas** a `chamarNucleo`, espalhadas por 11 arquivos `api.ts`. Qualquer
  mudança de assinatura da camada de acesso atinge as 61.
- `comum/` é _workspace_ consumido como fonte, não como pacote publicado: a App 03 já importa
  `comum/react` direto.

## Goals / Non-Goals

**Goals:**

- Abrir a porta HTTP sem reescrever regra alguma.
- Acrescentar ao modelo só os rótulos que a autoria exige e que o PRD-09 §8 já declara.
- Deixar a camada de acesso ao núcleo pronta para a terceira aplicação, não só para a segunda.

**Non-Goals:**

- Edição de trilha, missão ou atividade já criadas. O PRD-09 §9 não declara rota de edição, e
  o `RF-09-02` fala em ordenar, não em reordenar. Reordenação e edição são fatia própria — a
  unicidade adiável de `uq_missao_trilha_id_posicao` já existe no modelo para quando ela vier.
- Publicar `comum/` como pacote versionado. Segue consumido como fonte.

## Decisions

### 1. A porta reexpõe a regra; não a reescreve

`trilhas/rotas.py` traduz corpo HTTP para os parâmetros das funções de `regra.py` e devolve o
que elas produzem — o mesmo que `poderes/rotas.py` fez na fatia anterior. As recusas continuam
nascendo na regra, e nenhum teste existente muda.

_Alternativa descartada:_ mover a validação para a camada de rota, com Pydantic cobrindo o que
hoje é `ErroDeValidacao`. Duplicaria a recusa em dois lugares e quebraria os testes que chamam
a regra direto.

### 2. Missões e atividades saem aninhadas na leitura da trilha

`GET /v1/trilhas/minhas` devolve cada trilha com as missões dela na ordem da posição, e cada
missão com as atividades dela. Não nascem `GET /trilhas/{id}/missoes` nem
`GET /missoes/{id}/atividades`.

_Por quê:_ o PRD-09 §9 não as declara, e artefato do OpenSpec não cria contrato que o PRD não
tem. A App 09 monta a tela inteira de autoria com uma chamada, que é o que ela precisa.

_Custo aceito:_ a resposta cresce com a trilha. Aceitável no Ciclo 01 — duas trilhas, dezenas
de missões. Quando incomodar, as rotas próprias entram por decisão do fundador.

### 3. `etapa_do_ciclo` é enum fechado; `cadencia_de_retomada` é lista de dias

A etapa tem exatamente quatro valores no documento 11 §2.4 — abertura, desenvolvimento, marcos
e fechamento —, então entra como `Enum(..., native_enum=False)`, o padrão que
`ModalidadeDeAtividade` e `FormatoDeAtividade` já usam na mesma tabela.

A cadência de retomada entra como **lista de dias inteiros contados do desbloqueio**, porque é
essa a forma que o `RF-09-101` descreve ao sugerir "2, 7 e 21 dias".

_Alternativa descartada:_ reaproveitar o enum `Cadencia` de `coletas/modelo.py`. O documento 11
§2.2 diz "o mesmo vocabulário do desafio de coleta", mas aquele enum é `diaria`, `semanal`,
`mensal` — frequência que se repete, e não consegue expressar "2, 7 e 21 dias do desbloqueio".
O vocabulário compartilhado é a palavra "cadência", não o conjunto de valores.

### 4. A cadência entra por rota própria, não pelo cadastro da missão

`POST /v1/missoes/{id}/retomada`, como o PRD-09 §9 declara — e não campo de
`POST /v1/trilhas/{id}/missoes`. A missão nasce sem retomada e a recebe depois, o que também é
o que o `RF-09-83` permite ao deixá-la sem retomada.

### 5. Título obrigatório, descrição opcional

O PRD-09 §8 lista `titulo` e `descricao` na `Atividade` sem dizer qual é exigido. O título é
exigido porque sem ele nenhuma tela lista a atividade; a descrição é opcional porque o título e
a `producao_esperada` — que já é obrigatória na regra — dizem o que a atividade é. A `Missao`
exige título pelo mesmo motivo.

### 6. A camada de acesso sobe para `comum/` com a assinatura intacta

`comum/api/` recebe `cliente.ts` e `tipos.ts`; `comum/autenticacao/` recebe `ContextoDeSessao`,
`armazenamentoDeSessao` e `BotaoDeEntradaGoogle`. **`chamarNucleo(caminho, opcoes)` mantém a
assinatura exata**, e cada uma das 61 chamadas da App 03 muda só o caminho do `import`.

A configuração — chave de aplicação, URL do núcleo e client ID do Google — **não** sobe: fica
em cada aplicação, que chama `configurarAcessoAoNucleo({ chaveDeAplicacao, urlDoNucleo })` uma
vez, no `main.tsx`, antes de renderizar. Chamada ao núcleo antes da configuração SHALL falhar
com erro explícito, nunca partir com chave vazia.

_Alternativa descartada:_ trocar `chamarNucleo` por uma fábrica `criarCliente({...})` devolvendo
o cliente configurado. É mais explícito, mas reescreveria as 61 chamadas numa fatia cujo assunto
é outro — refatoração grande em app verde é onde defeito entra sem ser visto.

_Alternativa descartada:_ deixar `import.meta.env.VITE_*` dentro de `comum/`. Funcionaria, porque
o Vite substitui a variável no build de cada aplicação. Mas esconderia o acoplamento: a camada
comum passaria a exigir que toda aplicação futura nomeie as variáveis do mesmo jeito.

### 7. A App 09 espelha a App 03

Mesma pilha — Vite, React 19, TypeScript, Vitest, Biome —, mesma forma de pastas por assunto,
mesmo `package.json` com `comum: "*"`. O `frontend-ci.yml` já filtra `apps/**` e cobre a pasta
nova sem alteração; entram só o alvo em `.firebaserc` e o `app-09-deploy.yml`, espelho do
`app-03-deploy.yml`. O `firebase.json` já declara o alvo `mestre`.

### 8. A migração acrescenta título em duas etapas

`Missao.titulo` e `Atividade.titulo` são `NOT NULL` em tabelas que já existem. A migração
acrescenta a coluna anulável, preenche o que houver com o identificador da linha e só então
aplica o `NOT NULL` — assim ela roda igual em base vazia e em base com dado de
desenvolvimento. `etapa_do_ciclo` entra pelo mesmo caminho; `descricao` e
`cadencia_de_retomada` entram anuláveis e ficam assim.

## Risks / Trade-offs

| Risco | Mitigação |
| --- | --- |
| Mover a camada de acesso quebra a App 03, que está verde | A assinatura de `chamarNucleo` não muda; só o `import`. Os testes de `cliente.test.ts` sobem junto e rodam antes de a App 09 começar |
| `configurarAcessoAoNucleo` esquecido no boot manda chave vazia ao núcleo | A camada falha com erro explícito na primeira chamada não configurada, em vez de enviar cabeçalho vazio |
| A leitura aninhada cresce sem paginação | Aceito no Ciclo 01 (decisão 2). A rota é do Mestre e traz só as trilhas dele |
| Backfill de `titulo` deixa texto sem sentido em base de desenvolvimento | É base de desenvolvimento; produção ainda não tem trilha. O valor de preenchimento é o identificador, legível e único |
| Segunda aplicação sem endereço configurado no Firebase | O alvo `mestre` já está no `firebase.json`; falta só `.firebaserc` e a esteira, ambos na fatia |

## Migration Plan

1. Migração Alembic com as cinco colunas, na ordem da decisão 8.
2. `comum/` recebe a camada; a App 03 passa a importar de lá e a suíte dela roda.
3. `trilhas/rotas.py` e o registro em `principal.py`.
4. `apps/app-09-mestre/` e a esteira de publicação.

Reversão: a migração desfaz as cinco colunas; a camada em `comum/` volta a
`apps/app-03-gestao/src/` pelo caminho inverso. Nada nesta fatia apaga dado.

## Open Questions

Nenhuma. A única que havia — o formato da cadência de retomada — foi decidida pelo fundador em
2026-08-22, confirmando a decisão 3: **lista de dias contados do desbloqueio**. O enum
`Cadencia` do desafio de coleta não é reaproveitado, porque `diaria`, `semanal` e `mensal` não
expressam a sugestão de 2, 7 e 21 dias do `RF-09-101`.
