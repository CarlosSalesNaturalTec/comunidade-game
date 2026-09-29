# Tasks

## 1. Corpus montado pela esteira

- [x] 1.1 Criar `backend/src/nucleo/corpus_do_desenvolvedor/montagem.py` com a montagem dos
      blocos — uma seção `##` de cada arquivo de `docs/`, o `README.md` da raiz e uma rota de
      cada do contrato OpenAPI que `nucleo.principal` gera — e a interface de linha de comando
      que escreve o artefato JSON (design — decisão 1, `RN-03-30`). Verificar rodando o comando
      sobre a árvore e conferindo que o artefato sai com blocos das três origens.
- [x] 1.2 Criar `backend/src/nucleo/corpus_do_desenvolvedor/leitura.py` com a leitura do
      artefato no arranque e o **recorte por pergunta** — sobreposição de palavras, ordenação e
      acúmulo até o teto de 40 000 caracteres —, devolvendo corpus vazio quando não há artefato
      (design — decisões 1 e 2, `RF-03-70`).
- [x] 1.3 Acrescentar o passo de montagem ao `.github/workflows/backend-deploy.yml`, antes do
      `docker build`, e o `COPY` do artefato ao `backend/Dockerfile`; ignorar o artefato gerado
      no controle de versão (design — decisão 1). Verificar que o `docker build` local com o
      artefato presente produz imagem que o traz.

## 2. Assistente do Desenvolvedor no núcleo

- [x] 2.1 Criar a porta `PortaDoAssistenteDoDesenvolvedor` e o adaptador local, sem rede, com o
      desfecho e as opções do próximo passo (design — decisão 3, `RF-03-69`, `RF-03-70`).
- [x] 2.2 Criar o adaptador Gemini, na chave e no modelo já configurados, com instrução de
      corpus fechado e validação do JSON de desfecho, resposta e opções; qualquer falha, demora
      ou formato inesperado devolve `None` (design — decisão 3, `RN-03-31`).
- [x] 2.3 Escrever a regra da consulta: recorte do corpus, chamada da porta, recusa fixa fora do
      corpus com o caminho da documentação, conjunto fixo de opções quando o modelo não as
      manda, indisponibilidade declarada e **nada gravado** (`RF-03-70`, `RF-03-72`, `RN-03-30`,
      design — decisão 6).
- [x] 2.4 Expor `POST /v1/assistente-do-desenvolvedor`, pública e sem credencial de persona,
      recebendo a pergunta e as últimas seis mensagens da conversa e recusando campo que
      descreva o visitante (`RF-03-71`, `RN-03-29`, design — decisão 5).
- [x] 2.5 Registrar a rota como superfície própria do freio por origem, contada em separado
      (`RN-03-08`, design — decisão 7).

## 3. Testes do núcleo

- [x] 3.1 `backend/tests/test_corpus_do_desenvolvedor.py`: a montagem cobre as três origens; o
      recorte para no teto; o recorte não inventa texto fora do artefato; sem artefato o corpus
      é vazio (cenários "O recorte não passa do teto" e "Nenhuma requisição a terceiro monta o
      corpus na hora da resposta").
- [x] 3.2 `backend/tests/test_assistente_do_desenvolvedor.py`: pergunta respondida pelo corpus;
      pergunta fora do corpus recebe "não sei" com o caminho da documentação; toda resposta sai
      com a pergunta de múltipla escolha, inclusive a recusa e a resposta do modelo sem opções;
      indisponibilidade declarada; envio com dado do visitante recusado; nenhuma linha gravada
      em nenhum dos casos (`RF-03-69` a `RF-03-72`).
- [x] 3.3 `backend/tests/test_freio_do_assistente_do_desenvolvedor.py`: a repetição encontra 429
      com o tempo de espera e nenhuma pergunta vai ao modelo; a solicitação de chave segue sem
      freio depois de a origem ser freada no assistente (`RN-03-08`, `RN-03-35`).

## 4. Área do Apoiador Desenvolvedor na App 06

- [x] 4.1 Criar `apps/app-06-vitrine/src/desenvolvedor/` com a tela da área reunindo as quatro
      partes — chat, link da documentação MkDocs, link do repositório e formulário de chave —,
      os dois prazos e a declaração sobre a chave (`RF-03-67`, `RF-03-75`, `RF-03-76`,
      `RN-03-29`).
- [x] 4.2 Implementar o chat: abertura em texto fixo da aplicação com as primeiras escolhas, sem
      chamada ao abrir; escolha vale como próxima pergunta; pergunta livre também aceita; as
      últimas seis mensagens viajam com o envio e nada vai a armazenamento local (`RF-03-68`,
      `RF-03-69`, `RN-03-15`, design — decisões 4 e 5).
- [x] 4.3 Tratar a indisponibilidade do assistente como falha do assistente, com o aviso de que
      ele voltará, mantendo documentação, repositório e formulário acessíveis (`RF-03-72`,
      documento 99 §6 invariante 25).
- [x] 4.4 Implementar o formulário de solicitação de chave sobre `POST /v1/solicitacoes-de-chave`
      — solicitante, contato, o que pretende construir e instituição opcional —, declarando que
      nada ali emite chave nem cria cadastro e confirmando com protocolo e prazo, **sem** espera
      crescente (`RF-03-73`, `RF-03-74`, `RN-03-32`, `RN-03-35`).
- [x] 4.5 Implementar a tela de apresentação da URL em `/apresentar-url`, sobre
      `POST /v1/chaves/{id}/url`, pedindo o identificador da chave e a URL — nunca o segredo — e
      mostrando a recusa que o núcleo declarar (`RF-03-77`, design — decisão 8).
- [x] 4.6 Acrescentar os dois endereços a `navegacao/caminhos.ts`, as chamadas a
      `api/solicitacoes.ts` e a entrada da área na navegação da vitrine (`RF-03-67`).

## 5. Testes da App 06

- [x] 5.1 `apps/app-06-vitrine/src/testes/areaDoDesenvolvedor.test.tsx`: a área abre com as
      quatro partes; a abertura chega sem pergunta e sem chamada ao núcleo; toda mensagem
      termina com a escolha; escolher conduz a conversa; recarregar perde a conversa e o
      armazenamento local segue vazio (`RF-03-67` a `RF-03-69`, `RN-03-15`).
- [x] 5.2 `apps/app-06-vitrine/src/testes/chaveDoDesenvolvedor.test.tsx`: o envio devolve
      protocolo e prazo e nunca chave; a tela declara o que a solicitação não faz; envios
      repetidos não anunciam espera; a apresentação da URL aceita identificador e URL, nunca
      pede o segredo, e mostra a recusa do núcleo como o que é; com o assistente fora do ar a
      área segue utilizável (`RF-03-72` a `RF-03-77`, `RN-03-32`, `RN-03-35`).

## 6. Documentação

- [x] 6.1 Gravar as **três decisões novas** de 2026-09-29 no documento-fonte (documento 03 §8) e
      no documento 09 §1 — recorte do corpus por pergunta com teto, freio por origem na rota do
      assistente e abertura como texto fixo da aplicação —, e aplicá-las no PRD-03 (§§6.6, 7 e
      9), sem repetir tabela nem número normativo.
- [x] 6.2 Marcar a fatia 8 do PRD-03 como implementada no `openspec/cronograma-de-fatias.md`,
      com o slug da change e o que ela decidiu, atualizar a situação do PRD-03 em
      `docs/prds/index.md` e conferir o documento 99 — nenhum arquivo novo em `docs/`, logo a
      `nav` do `mkdocs.yml` não muda.
