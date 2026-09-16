## 1. A culminância volta ao Mestre autor (núcleo)

- [x] 1.1 `RF-09-29`, `RF-09-30`, `RF-09-04`: acrescentar `culminancia: CulminanciaSaida | None`
      a `TrilhaDoMestreSaida` e populá-la em `listar_minhas_trilhas_rota`
      (`backend/src/nucleo/trilhas/rotas.py`), com a mesma consulta que
      `obter_trilha_publica_rota` já faz. Verificar pelo teste de rota da tarefa 5.1: trilha com
      culminância volta com os três campos, trilha sem ela volta com o campo nulo, e a trilha em
      rascunho também.

## 2. O arquivo do conteúdo passa a ter tipo e a ser servido (núcleo)

- [x] 2.1 `RF-09-16`, `RF-09-17`, `RF-09-115`: acrescentar a coluna do tipo do arquivo a
      `ConteudoDaMissao` (`backend/src/nucleo/conteudos/modelo.py`) e gravá-la em
      `confirmar_envio` (`conteudos/regra.py`) a partir do que o armazenamento apurou, ao lado
      do tamanho real que já é reapurado ali. Verificar pelo teste da tarefa 5.2.
- [x] 2.2 `RF-09-16`, `RF-09-17`: escrever a revisão Alembic da coluna nova em
      `backend/alembic/versions/`, sem retrocarregar linha existente. Verificar pelo teste de
      paridade entre `alembic upgrade head` e `Base.metadata`, que já existe na suíte.
- [x] 2.3 `RF-05-11`, `RF-09-25`, `RN-01-28`: escrever a regra de leitura dos bytes em
      `conteudos/regra.py`, no molde de `ler_imagem_da_pergunta` — serve ao Mestre autor da
      trilha e ao Guerreiro(a) inscrito nela, 403 para qualquer outra persona, 404 para conteúdo
      sem envio confirmado, e tipo indeterminado para linha gravada antes da coluna. Verificar
      pelo teste da tarefa 5.2.
- [x] 2.4 `RF-05-11`, `RF-09-25`: expor `GET /v1/conteudos/{id}/arquivo` em
      `conteudos/rotas.py`, devolvendo os bytes com o tipo gravado — a rota só reexpõe a regra,
      como `ler_imagem_da_pergunta_rota` faz. Verificar pelo teste de rota da tarefa 5.2.

## 3. A App 09 reabre a culminância e pré-visualiza a missão inteira

- [x] 3.1 `RF-09-29`, `RF-09-30`: em `apps/app-09-mestre/src/trilhas/api.ts`, tipar
      `culminancia` como campo que `GET /v1/trilhas/minhas` traz, remover o comentário que
      descreve a ausência como intencional e remover `obterTrilhaPublica`, exportada e nunca
      chamada. Verificar pelo teste da tarefa 5.3.
- [x] 3.2 `RF-09-29`, `RF-09-30`, `RF-09-06`, `RF-09-07`: em `TelaDaTrilha.tsx`, fazer o resumo,
      o bloco da culminância, o painel de pendências e o rótulo do botão refletirem a culminância
      gravada; o formulário de alteração passa a nascer preenchido com o que veio do núcleo.
      Verificar pelo teste da tarefa 5.3.
- [x] 3.3 `RF-09-14` a `RF-09-17`, `RF-09-25`: acrescentar à camada de acesso da App 09 a
      leitura do arquivo do conteúdo como _blob_, pelo núcleo e com a chave de aplicação, no
      molde de `lerImagemDaPergunta`, liberando a URL de objeto ao desmontar. Verificar pelo
      teste da tarefa 5.3.
- [x] 3.4 `RF-09-25`, `RF-09-14`, `RF-09-15`, `RF-09-21`, `RF-09-26`, `RF-09-81`: reescrever
      `PreVisualizacaoDaMissao.tsx` para apresentar, na ordem da tela do Guerreiro(a), título,
      aviso de missão opcional, conteúdo com imagem e vídeo exibidos, crédito e licença,
      bibliografia, atividades e o desafio de desbloqueio ou a sondagem em leitura; envio não
      concluído é dito pendente. Verificar pelo teste da tarefa 5.3.
- [x] 3.5 `RF-09-25`, `RF-09-114`: passar a `PreVisualizacaoDaMissao`, a partir de
      `ListaDeMissoes.tsx`, o crédito pelo **nick** do Mestre em sessão, lido por
      `GET /v1/eu/mestre/identidade`, com queda para "Mestre autor" quando o nick for nulo —
      hoje `autorNome` chega sempre nulo. Verificar pelo teste da tarefa 5.3.

## 4. A App 05 exibe o arquivo do conteúdo

- [x] 4.1 `RF-05-11`: em `apps/app-05-guerreiro/src/api/trilha.ts`, acrescentar a leitura do
      arquivo do conteúdo como _blob_, pela rota nova e com a chave de aplicação. Verificar pelo
      teste da tarefa 5.4.
- [x] 4.2 `RF-05-11`, `RF-05-12`: em `trilha/Missao.tsx`, substituir `conteudoLegivel`, que hoje
      imprime a referência do armazenamento como texto, pela exibição da imagem e do vídeo;
      conteúdo sem envio confirmado é omitido ou dito pendente, e nenhuma referência chega à
      tela. Verificar pelo teste da tarefa 5.4.

## 5. Testes

- [x] 5.1 `backend/tests/test_trilha_rota.py` e `test_culminancia.py`: a leitura das trilhas
      próprias traz a culminância declarada, traz nula quando não há, alcança trilha em rascunho
      e não traz a culminância de trilha de outro Mestre — os quatro cenários de `culminancia` e
      os três de `trilha-e-missao` (`RF-09-29`, `RF-09-30`, `RF-09-04`).
- [x] 5.2 `backend/tests/` do conteúdo: a confirmação grava o tipo apurado; os bytes são
      servidos ao Mestre autor e ao Guerreiro(a) inscrito; 403 a persona alheia; 404 a conteúdo
      de texto e a envio não confirmado; trilha em rascunho é alcançada pelo autor; e linha
      gravada antes da coluna sai com tipo indeterminado — os cenários de `conteudo-da-missao`
      (`RF-05-11`, `RF-09-16`, `RF-09-17`, `RF-09-115`).
- [x] 5.3 `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`: a culminância gravada reabre em
      sessão nova e o formulário nasce preenchido; o painel de pendências não a acusa quando ela
      existe; e a pré-visualização apresenta cada item que a tela do Guerreiro(a) apresenta —
      atividades, obrigatoriedade, desbloqueio, crédito pelo nick e imagem exibida —, de modo que
      tirar um deles quebre a suíte (design — decisão 4). Cobre os cenários de `area-do-mestre`
      (`RF-09-29`, `RF-09-30`, `RF-09-25`).
- [x] 5.4 `apps/app-05-guerreiro/src/trilha/Missao.test.tsx`: a imagem do conteúdo aparece como
      imagem, nenhuma referência de armazenamento chega à tela e envio não concluído não aparece
      quebrado — os cenários novos de `area-do-guerreiro` (`RF-05-11`, `RF-05-12`).

## 6. Documentação

- [x] 6.1 Acrescentar `GET /v1/conteudos/{id}/arquivo` à tabela de contrato de API do PRD-09 §9,
      na linha seguinte às do envio, no molde da linha que a imagem da pergunta já tem
      (`RF-05-11`, `RF-09-25`); registrar em `docs/09-topicos-em-aberto-e-sugestoes.md` §1, como
      já decidido, a decisão do fundador de 2026-09-16 sobre o crédito da pré-visualização pelo
      nick e sobre o recorte do que ela apresenta; acrescentar ao bloco do PRD-09 de
      `openspec/cronograma-de-fatias.md` a linha sem número desta change, com a situação
      "implementado"; e conferir se alguma relação entre documentos mudou, atualizando o
      documento 99 só nesse caso. Nenhum arquivo novo entra em `docs/`, portanto a `nav` do
      `mkdocs.yml` não muda; a situação do PRD-09 em `docs/prds/index.md` não muda, porque a
      change é conserto e não fatia nova.
