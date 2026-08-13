## Context

Ver `proposal.md` — Why. O que o núcleo já oferece e condiciona o desenho:

- `exigir_chave_de_aplicacao` (`backend/src/nucleo/chaves/conferencia.py`) é uma
  **dependency do FastAPI**, aplicada por roteador em `incluir_roteador_de_dados`
  (`principal.py`). Toda rota sob `/v1` já a recebe sem declarar nada.
- Ela grava `ContextoDaChave` em `request.state`, com `natureza` — a faixa da cota — já
  resolvida. Nenhuma coluna nova é necessária.
- `MiddlewareDeAuditoria` é **middleware** e roda **fora** da resolução das dependencies:
  quando ele age, a chave ainda não foi conferida na entrada e já foi conferida na saída.
- O corpo único de erro (`CorpoDeErro`: código, mensagem, campo) vem de `RF-01-27` e não
  tem campo numérico.
- `Configuracao` (pydantic-settings, prefixo `CG_`) é onde vivem os parâmetros; alguns têm
  padrão no código, outros deliberadamente não têm.

## Goals / Non-Goals

**Goals:**

- Cota de leitura por faixa da chave, cobrindo toda rota sob `/v1` sem declaração por rota.
- Freio por origem reutilizável, pronto para as três superfícies quando elas nascerem.
- Precedência **401 antes de 429** preservada, como a spec de `chave-de-aplicacao` exige.
- Nenhuma escrita em banco e nenhuma dependência externa nova.

**Non-Goals:**

- Contagem compartilhada entre processos. O documento 03 §1, princípio 13, fixa o Cloud Run
  sem escala horizontal no Ciclo 01 justamente para que a contagem em memória baste.
- Prender o freio às rotas que ele protege: elas são de fatias seguintes.
- Qualquer forma de CAPTCHA, cadastro ou identificador persistente do visitante.

## Decisions

### A cota é dependency de roteador, não middleware

Middleware roda antes de as dependencies resolverem, então uma cota em middleware não teria
`ContextoDaChave` e teria de reconferir a chave por conta própria — o que duplicaria a busca
no banco e reabriria o caminho de tempo constante que `conferencia.py` construiu de
propósito. Pior: recusaria com 429 antes de saber se a chave é válida, contrariando o delta
de `chave-de-aplicacao`.

A cota entra como **segunda dependency** em `incluir_roteador_de_dados`, declarada **depois**
de `exigir_chave_de_aplicacao`. O FastAPI resolve na ordem declarada, então a chave inválida
levanta `ChaveInvalida` (401) antes de a cota contar qualquer coisa. Cobertura universal pelo
mesmo mecanismo que já entrega a chave — nenhuma rota futura precisa lembrar de nada.

- _Alternativa descartada:_ middleware que reconfere a chave — duplica a busca e desfaz o
  tempo constante da recusa.
- _Alternativa descartada:_ declaração rota a rota — esquecível, e o precedente da auditoria
  já rejeitou essa via.

### "Leitura" é o método HTTP seguro

A cota conta `GET` e `HEAD`. É o critério que não envelhece: qualquer rota de leitura futura
entra sozinha, e nenhuma lista precisa ser mantida.

- _Alternativa descartada:_ lista explícita de rotas de leitura — envelhece a cada fatia.

### O freio por origem é dependency declarada pela rota

Ao contrário da cota, o freio vale só em três superfícies nomeadas, com limites diferentes
entre elas. Ele nasce como **fábrica de dependency** — recebe a superfície e devolve a
dependency —, e cada rota o declara quando for criada. Universalizá-lo seria errado: frearia
rotas que o documento 03 §8 não manda frear, inclusive a solicitação de chave, que a spec
exige deixar livre.

### A janela deslizante é uma fila de instantes por chave de contagem

Estrutura em memória: mapa de `chave de contagem → fila de instantes`, com os instantes fora
da janela descartados na leitura. Expressa "N por janela" diretamente, que é como o documento
03 §8 declara os limites, e serve à cota e ao freio sem duas implementações.

- _Alternativa descartada:_ _token bucket_ — expressa vazão, não "N por janela", e exigiria
  traduzir os números do documento 03.
- _Alternativa descartada:_ contador compartilhado em Redis ou Memorystore — provedor novo,
  que nenhum documento decidiu. Fora de cogitação sem decisão do fundador.

### O tempo de espera vai no `Retry-After` e na mensagem

`RF-01-27` fixa o corpo único e não tem campo numérico; mudá-lo afetaria toda rota já
entregue. O tempo de espera vai no cabeçalho **`Retry-After`**, que é o meio padrão do HTTP e
o que uma aplicação de terceiro sabe ler, e **também** em linguagem simples dentro da
mensagem do corpo, que é o que o PRD-03 pede para a tela do visitante. O formato do corpo não
muda.

### O sal da origem roda por período, com o sal anterior retido por uma janela

O sal nasce no processo e roda por período maior que a maior janela de origem. Na virada, o
sal anterior fica retido pelo tempo de uma janela: os baldes já contados seguem válidos até
expirarem naturalmente, e as chamadas novas já usam o sal novo. Sem isso, cada rotação zeraria
o freio de quem estivesse sendo freado.

### Os números vêm da configuração, com padrão igual ao documento 03 §8

Diferente da duração da sessão e do limiar da biometria — que não têm padrão no código
porque a operação é que os declara —, estes números **estão decididos** no documento 03 §8.
Eles entram em `Configuracao` com esses valores como padrão, ajustáveis por ambiente sem
alterar código.

## Risks / Trade-offs

- **Mais de um contêiner multiplica o limite** → o documento 03 §1, princípio 13, fixa o
  Cloud Run sem escala horizontal no Ciclo 01. O repositório ainda não tem configuração de
  implantação onde escrever `--max-instances=1`; até ela existir, a garantia é documental. O
  núcleo registra a premissa numa linha de log na subida, para que a violação apareça em
  produção em vez de passar despercebida.
- **Reinício zera a contagem** → aceito. É consequência direta de não gravar nada, que é o
  que `RN-01-45` exige. Uma reinicialização dá a quem estava freado uma janela extra.
- **Origem atrás de NAT divide o freio** → uma escola ou lan house inteira conta como uma
  origem. O limite de 30 consultas por 10 minutos foi calibrado sobre uso legítimo (quem
  recebeu o nick busca uma ou duas vezes), o que dá folga para dezenas de pessoas na mesma
  saída. Se aparecer atrito real na operação, é ajuste de configuração, não de código.
- **A rotação do sal dá uma janela extra na virada** → o sal anterior retido por uma janela
  reduz a brecha ao mínimo; zerá-la exigiria guardar estado, que `RN-01-45` proíbe.
- **O freio nasce sem superfície** → a cota, que é a metade que já tem onde agir, cobre toda
  rota no ar desde esta fatia. O freio ganha teste próprio contra rota de teste; as três
  superfícies o declaram quando forem criadas, e as specs delas já apontam para cá.

## Migration Plan

Sem migração de banco: nada do que esta change introduz vai a disco. A implantação precisa
subir com `--max-instances=1` no Cloud Run e pode declarar os números por variável de
ambiente `CG_*` se quiser divergir do padrão do documento 03 §8. Reversão é remover as duas
dependencies de `incluir_roteador_de_dados` e da rota — nenhum dado fica para trás.
