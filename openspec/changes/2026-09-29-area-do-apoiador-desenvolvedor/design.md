# Design

## Context

Ver `proposal.md` — Why. O que já está de pé e condiciona o desenho:

- `backend/src/nucleo/assistente/` traz o padrão do assistente de trilhas — porta abstrata,
  adaptador local fora de produção, adaptador Gemini em produção pela chave única do projeto,
  `None` como indisponibilidade e desfecho classificado pelo próprio modelo.
- O freio por origem já existe, com resumo do IP em memória e contagem separada por superfície
  (`openspec/specs/protecao-das-rotas-publicas/spec.md`).
- `POST /v1/solicitacoes-de-chave` e `POST /v1/chaves/{id}/url` já estão prontos e públicos.
- O corpus decidido tem hoje ~1,8 milhão de caracteres. A imagem do núcleo é construída com
  contexto em `backend/`: `docs/` e o `README.md` da raiz **não** estão lá na hora do `docker
  build`. Importar `nucleo.principal` **não** exige ambiente completo — a conferência mora no
  `lifespan`, por decisão anterior —, então o contrato OpenAPI pode ser gerado pelo próprio
  núcleo fora do serviço.

## Goals / Non-Goals

**Goals:** a rota pública do assistente sobre corpus fechado e recortado; o artefato de corpus
montado pela esteira; a seção da App 06 com as quatro partes, os prazos e a apresentação da URL.

**Non-Goals:** nenhuma entidade nova e nenhuma migração; nenhuma guarda da conversa; nenhum
provedor novo — o Gemini já está decidido no documento 03 §1.12.

## Decisions

### 1. O corpus é um artefato de blocos, montado pela esteira e lido no arranque

Um módulo do núcleo monta o artefato: cada arquivo de `docs/`, o `README.md` da raiz e o
contrato OpenAPI viram **blocos** — um por seção `##` do markdown e um por rota do contrato —,
cada bloco com origem, título e texto, num arquivo JSON. A esteira roda o módulo **antes do
`docker build`**, escrevendo o artefato dentro de `backend/`, e o `Dockerfile` o copia. Em
tempo de resposta o núcleo só **lê** o artefato: nenhuma requisição a terceiro (documento 03
§8).

Alternativas descartadas: gerar o artefato no arranque do contêiner — `docs/` não está na
imagem; copiar `docs/` para o contexto do build — polui o contexto e duplica 1,8 MB por camada.

Sem artefato (desenvolvimento e teste) o corpus é **vazio**, e toda pergunta sai como fora do
corpus — comportamento declarado, nunca exceção silenciosa.

### 2. O recorte por pergunta escolhe blocos por sobreposição de palavras, com teto

Decisão do fundador de 2026-09-29. O núcleo pontua cada bloco pela sobreposição das palavras da
pergunta com título e texto, ordena e acumula blocos até o **teto de 40 000 caracteres** —
dobro do teto do assistente de trilhas, que basta para várias seções de documentação e mantém
previsível o custo por pergunta no _free tier_ que o documento 09 declara.

Alternativas descartadas: corpus inteiro a cada pergunta (~450 mil tokens, recusado pelo
fundador); busca por vetores (exigiria provedor de _embeddings_, que documento nenhum decide).

### 3. Porta própria, e não a do assistente de trilhas

`PortaDoAssistenteDoDesenvolvedor` nova, com `responder(texto, corpus, historico)` devolvendo
desfecho, resposta e **opções do próximo passo**. A porta existente carrega
`transcricao_da_pergunta` — que só faz sentido onde a fala é transcrita no aparelho — e o
desfecho `tarefa_escolar`, que aqui não existe. Mesmo par de adaptadores: local fora de
produção, Gemini em produção, `None` como indisponibilidade.

### 4. A abertura é texto da App 06, não resposta do modelo

Decisão do fundador de 2026-09-29. Nenhuma chamada ao núcleo quando a área abre: a abertura e o
primeiro conjunto de escolhas são texto da aplicação. Assim o `RF-03-68` continua cumprido com
o assistente fora do ar (`RF-03-72`) e a visita não custa nada.

### 5. A conversa viaja com a pergunta e não é guardada em lugar nenhum

Para o assistente "aprofundar o tópico escolhido" (PRD-03 §5.8), a App 06 envia junto da
pergunta as **últimas seis mensagens** da conversa, que vivem só no estado da página. O núcleo
as repassa ao modelo e **não grava nada** — nem pergunta, nem resposta, nem origem. Recarregar
a página perde tudo (PRD-03 §8).

Alternativa descartada: guardar a conversa no núcleo por sessão anônima — contraria o §8 do PRD
e o `RN-03-15`.

### 6. As opções do próximo passo vêm do modelo, com conjunto fixo de reserva

O modelo devolve as opções no mesmo JSON do desfecho e da resposta. Resposta sem opções, ou
fora do corpus, recebe o **conjunto fixo** declarado no núcleo, e nenhuma mensagem sai sem
pergunta (`RF-03-69`). Mesmo precedente da recusa fixa do assistente de trilhas.

### 7. A rota entra como superfície própria do freio por origem

Decisão do fundador de 2026-09-29. Contagem separada das demais, sem dividir janela com a busca
por nick nem com os formulários, e sem alcançar a solicitação de chave (`RN-03-35`).

### 8. Dois endereços na App 06

`/desenvolvedor` para a área e `/apresentar-url` para a apresentação da URL, no mesmo padrão de
endereço próprio de `/participar`, `/solicitar-dados` e `/quero-participar`. A apresentação pede
o **identificador** da chave e a URL, nunca o segredo.

## Risks / Trade-offs

- **Corpus envelhece entre implantações do núcleo** → é o que a decisão do fundador diz
  ("montado pela esteira a cada implantação do núcleo"), e o `backend-deploy.yml` só dispara por
  `backend/**`: mudança só em `docs/` não renova o corpus até a próxima implantação do núcleo.
  Aceito e declarado aqui, não corrigido por conta própria.
- **Sobreposição de palavras erra sinônimo** → a pergunta cai como fora do corpus, que é a saída
  declarada do `RF-03-70`: aponta a documentação em vez de inventar. O teto generoso reduz o
  caso.
- **Rota pública que gasta modelo pago** → freio por origem (decisão 7) e cota da chave da
  aplicação.
- **Vazamento pelo corpus** → o artefato só contém `docs/`, o `README.md` e o contrato OpenAPI,
  todos já públicos; nada de `backend/`, de `openspec/` nem de segredo.
- **Montagem do artefato quebra a implantação** → o passo da esteira falha antes do `docker
  build`, e a revisão anterior segue servindo; o núcleo sem artefato ainda sobe, respondendo
  tudo como fora do corpus.

## Migration Plan

Nenhuma migração: a fatia não cria entidade nem coluna. A ordem de implantação é uma só — o
passo da esteira roda antes do build, e o núcleo novo já sobe com o artefato dentro da imagem.
