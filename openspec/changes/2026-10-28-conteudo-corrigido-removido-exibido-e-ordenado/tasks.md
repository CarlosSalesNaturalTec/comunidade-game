# Tasks

## 1. Ordem verdadeira no banco e na criação

- [ ] 1.1 Em `backend/src/nucleo/conteudos/regra.py`, `criar_conteudo` passa a atribuir a ordem
      como `max(ordem) + 1` dentro da missão, e o parâmetro `ordem` sai da assinatura
      (`RF-09-126`, design — decisão 2). Verificar em `backend/tests/test_conteudo.py` que o
      terceiro conteúdo de uma missão nasce com ordem posterior à dos dois anteriores e que a
      leitura o traz por último — cenário "O conteúdo novo entra por último".
- [ ] 1.2 Em `backend/src/nucleo/conteudos/rotas.py`, `CriarConteudoEntrada` perde o campo
      `ordem`; com `extra="forbid"`, mandá-lo responde **422** (`RF-09-126`, **BREAKING**,
      design — decisão 2). Verificar com uma requisição que manda `ordem` e recebe 422.
- [ ] 1.3 Revisão do Alembic que renumera `conteudo_da_missao.ordem` por missão, por
      `registrado_em` e desempate por `id`, com `downgrade` vazio e o motivo em comentário
      (`RF-09-126`, design — decisões 4 e *Migration Plan*). Verificar, em teste que grava três
      conteúdos com a mesma ordem e aplica a renumeração, que eles saem com ordens distintas na
      sequência de criação — cenário "O conteúdo já gravado é renumerado".

## 2. Correção do conteúdo

- [ ] 2.1 `corrigir_conteudo` em `conteudos/regra.py`: alcança corpo, endereço, autoria e
      fonte; reaproveita `conferir_autoria_estrita_da_trilha` e as recusas de coerência por
      tipo que `criar_conteudo` já aplica; campo omitido conserva o valor (`RF-09-123`,
      design — *Risks*, `PATCH` parcial). Verificar que a correção grava e que o conteúdo
      permanece na mesma missão e na mesma ordem.
- [ ] 2.2 Guarda de `RN-09-45` em `corrigir_conteudo`: tentar trocar o **tipo** responde
      **422** dizendo que o caminho é remover e cadastrar outro (`RN-09-45`).
- [ ] 2.3 `abrir_envio` passa a recusar conteúdo que já tem `referencia` gravada, com o mesmo
      motivo (`RN-09-45`, design — decisão 5). Verificar que a segunda abertura de sessão para
      o mesmo conteúdo é recusada e os bytes gravados permanecem.
- [ ] 2.4 `PATCH /v1/conteudos/{id}` em `conteudos/rotas.py`, devolvendo o conteúdo corrigido
      no mesmo formato de `saida_do_conteudo` (`RF-09-123`, design — decisão 1).
- [ ] 2.5 Testes da correção em `backend/tests/test_conteudo.py`, cobrindo os cenários "O
      Mestre autor corrige o corpo do texto", "A correção alcança a trilha publicada", "Mestre
      que não é o autor é recusado", "Admin não corrige conteúdo", "A correção confere a
      coerência do tipo", "A correção confere a fonte do terceiro", "Trocar o tipo é recusado"
      e "Reabrir envio de conteúdo já confirmado é recusado" (`RF-09-123`, `RN-09-45`).

## 3. Remoção do conteúdo

- [ ] 3.1 `remover_conteudo` em `conteudos/regra.py`: guarda de autoria, `armazenamento.remover`
      antes de apagar a linha, referência ausente no armazenamento contando como removida, e
      falha do armazenamento subindo como erro de camada sem apagar nada (`RF-09-124`,
      `RN-09-07`, design — decisão 6). Nenhum lançamento no livro-razão.
- [ ] 3.2 `DELETE /v1/conteudos/{id}` em `conteudos/rotas.py`, com **204** (`RF-09-124`,
      design — decisão 1).
- [ ] 3.3 Testes da remoção em `backend/tests/test_conteudo.py`, cobrindo "O conteúdo de texto
      é removido", "Remover conteúdo com arquivo apaga os bytes", "Remover conteúdo sem envio
      confirmado não falha", "A remoção alcança a trilha publicada", "Quem não é o autor não
      remove" e "Os restantes não são renumerados" (`RF-09-124`).

## 4. Movimento na ordem

- [ ] 4.1 `mover_conteudo` em `conteudos/regra.py`: troca a ordem com o vizinho no sentido
      pedido, recusa mover o primeiro para cima e o último para baixo sem alterar nada, e
      mantém a unicidade da ordem na regra, sem restrição no banco (`RF-09-126`, design —
      decisão 3).
- [ ] 4.2 `POST /v1/conteudos/{id}/ordem` em `conteudos/rotas.py`, com `direcao` em `cima` ou
      `baixo` (`RF-09-126`, design — decisão 1).
- [ ] 4.3 Testes do movimento em `backend/tests/test_conteudo.py`, cobrindo "O conteúdo sobe
      uma posição", "Mover o primeiro para cima é recusado" e "Quem não é o autor não move"
      (`RF-09-126`).

## 5. O bloco Conteúdo na App 09

- [ ] 5.1 Em `apps/app-09-mestre/src/trilhas/api.ts`, as chamadas `corrigirConteudo`,
      `removerConteudo` e `moverConteudo`, e `criarConteudo` deixa de mandar `ordem`
      (`RF-09-123`, `RF-09-124`, `RF-09-126`).
- [ ] 5.2 `ConteudoPreVisualizado` sai de `PreVisualizacaoDaMissao.tsx` para módulo próprio e
      a pré-visualização passa a importá-lo, sem mudança no que ela exibe (`RF-09-125`,
      design — decisão 7). Verificar que os testes atuais da pré-visualização seguem passando.
- [ ] 5.3 Rótulo derivado por conteúdo em `ListaDeMissoes.tsx` — primeiras palavras do corpo,
      domínio do endereço, nome do arquivo —, com a autoria sempre visível e a fonte no
      conteúdo de terceiro (`RF-09-125`, `RF-09-24`).
- [ ] 5.4 Exibição no bloco: texto e link embutidos, e imagem, vídeo e arquivo de apoio
      envoltos em estado por item, de modo que nenhum `MidiaDoNucleo` monte antes do comando do
      Mestre; conteúdo sem envio confirmado dito pendente (`RF-09-125`, `RN-09-46`, design —
      decisão 7).
- [ ] 5.5 Controles de corrigir, remover, subir e descer em cada conteúdo listado, com a recusa
      do núcleo apresentada com o motivo declarado (`RF-09-123`, `RF-09-124`, `RF-09-126`,
      `RN-09-16`).
- [ ] 5.6 `FormularioDeConteudo.tsx` passa a servir correção além de criação, sem oferecer
      troca de tipo nem de arquivo, dizendo que para isso o caminho é remover e cadastrar
      outro; `chaveDoRascunho` desce ao id do conteúdo em correção (`RF-09-123`, `RN-09-45`,
      design — decisão 8).
- [ ] 5.7 Testes da tela em `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`, cobrindo "Três
      conteúdos de texto se distinguem na lista", "O link é identificado pelo domínio", "A
      fonte do terceiro aparece na linha", "O texto aparece sem pedir nada", "Abrir a tela não
      busca arquivo algum", "A imagem é exibida quando o Mestre pede", "Conteúdo sem envio
      confirmado é dito pendente", "O Mestre corrige o texto já gravado", "O rascunho de uma
      edição não invade outra", "O Mestre remove um conteúdo", "O Mestre move um conteúdo na
      lista", "Trocar o tipo é dito, não oferecido", "A recusa do núcleo chega com o motivo" e
      "Corrigir e remover alcançam a trilha publicada" (`RF-09-123` a `RF-09-126`, `RN-09-45`,
      `RN-09-46`).

## 6. Documentação

- [ ] 6.1 Documento 03 §11 ganha o marcador da correção, remoção, exibição e ordem do conteúdo,
      e o documento 09 §1 ganha a linha da decisão do fundador de 2026-10-27, como o pacote
      aprovado os redigiu (`RF-09-123` a `RF-09-126`, `RN-09-45`, `RN-09-46`).
- [ ] 6.2 PRD-09 §8 recebe `RF-09-123` a `RF-09-126`, `RN-09-45` e `RN-09-46` nas tabelas de
      requisitos e de regras, e a fatia 24 fica **implementada** no
      `openspec/cronograma-de-fatias.md`, com o slug desta change. `docs/prds/index.md` não
      muda — a situação do PRD-09 continua a mesma —, nem o documento 99, nem a `nav` do
      `mkdocs.yml`, porque nenhum arquivo nasceu nem foi renomeado.
