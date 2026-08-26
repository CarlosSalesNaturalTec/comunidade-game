## 1. Núcleo — leituras do território

- [ ] 1.1 Derivar a **próxima medição** da série em `coletas/regra.py`, a partir de
      `periodo_de_cadencia`, e acrescentá-la — com o tipo de coleta (nome, forma de registro e
      unidade) — à saída de `consultar_series_do_guerreiro`; série interrompida ou encerrada
      sai sem próxima medição (`RF-05-30`, `RN-05-10`). Verificação: os cenários novos de
      `tests/test_serie_de_coleta.py` (tarefa 4.1) passam.
- [ ] 1.2 Escrever a consulta do **histórico da própria série** em `coletas/regra.py` —
      paginada por cursor, do mais recente ao mais antigo, com valor, unidade, mídia, origem,
      situação, marca "a conferir", pontos creditados e o **motivo** do registro invalidado;
      403 para série de outro coletor e para outro papel (`RF-05-37`, `RF-05-38`, `RN-05-09`,
      `RN-05-21`).
- [ ] 1.3 Escrever a consulta dos **desafios que o Guerreiro(a) pode assumir** em
      `coletas/regra.py`, extraindo de `abrir_serie_de_coleta` o predicado de vigência e de
      teto de granularidade para que as duas partam do mesmo lugar (design — decisão 4); cada
      desafio sai com tipo, cadência, vigência, granularidade, missão, trilha e a marca de já
      assumido naquele local (`RF-05-30`, `RN-05-24`).
- [ ] 1.4 Escrever a consulta das **próprias solicitações de local** em `locais/regra.py`,
      paginada e sem filtro de comunidade obrigatório, com situação, motivo da recusa e local
      criado pela aprovação; 403 para outro solicitante e para outro papel (`RF-05-32`,
      `RN-05-11`, `RN-05-21`).
- [ ] 1.5 Publicar as três rotas de coleta em `coletas/rotas.py` e a de solicitações em
      `locais/rotas.py`, nos nomes da tabela do design — decisão 5, com o contrato de listagem
      já usado por `series-de-coleta/minhas`. Verificação: `tests/test_coletas_rota.py` e
      `tests/test_solicitacao_de_local_rota.py` (tarefa 4.2) passam.

## 2. App 05 — o bloco da coleta

- [ ] 2.1 Criar o cliente das rotas de coleta em `apps/app-05-guerreiro/src/api/`, no molde de
      `sessoesDeGuerreiro.ts`: séries, histórico, desafios disponíveis, locais, abertura de
      série, registro por _multipart_ e solicitações de local.
- [ ] 2.2 Tela das **minhas séries**: o que cada uma mede, local, estado, próxima medição e
      pontos rendidos; a série interrompida sinalizada, com histórico preservado, a frase de
      que os pontos permanecem e o caminho de retomada (`RF-05-30`, `RF-05-36`).
- [ ] 2.3 Fluxo de **abrir série**: escolha do desafio entre os disponíveis e do local entre os
      cadastrados do nível exigido, sem oferecer o que o núcleo recusaria, com a recusa
      explicada sem termo técnico (`RF-05-31`, `RN-05-11`, `RN-05-24`).
- [ ] 2.4 Fluxo de **solicitar local que falta** e a lista das próprias solicitações, com
      situação, motivo da recusa e o local criado pela aprovação, deixando claro que o pedido
      não cria local (`RF-05-32`).
- [ ] 2.5 Tela de **registrar medição**: valor digitado (origem `manual`), ditado por voz
      transcrito no aparelho (origem `voz`, áudio nunca enviado nem guardado — design —
      decisão 1) e foto ou vídeo quando a forma do tipo assim exige (design — decisão 2);
      origem `sensor` nunca é oferecida (`RF-05-33`, `RN-05-32`).
- [ ] 2.6 Devolutiva da gravação: pontuou na hora, ou entrou **a conferir** com a explicação
      acolhedora de que o Mestre vai olhar, sem acusação e sem código técnico (`RF-05-34`,
      `RF-05-35`, `RN-05-08`).
- [ ] 2.7 Tela do **histórico da série**: data, valor, situação e pontos de cada registro, e o
      motivo do registro invalidado, com a frase de que só ele perdeu os pontos (`RF-05-37`,
      `RF-05-38`, `RN-05-09`).
- [ ] 2.8 **Recusa sem rede** no registro, com o motivo em linguagem simples e nenhuma fila,
      medição ou mídia guardada no aparelho (`RF-05-85`).
- [ ] 2.9 **Aviso discreto de coleta de dados** nas telas que coletam, com acesso à área
      detalhada, sem bloquear a tela (`RF-05-57`).
- [ ] 2.10 Ligar o bloco da coleta à área do Guerreiro(a) em sessão, sem exibir nenhum dado de
      outra criança em nenhuma das telas novas (`RN-05-21`).

## 3. Testes do núcleo

- [ ] 3.1 `tests/test_serie_de_coleta.py`: os cenários novos da capacidade `serie-de-coleta` —
      próxima medição do período seguinte, período corrente sem medição válida, série
      interrompida e encerrada sem próxima medição, tipo de coleta na saída — e a paginação
      existente intacta (`RF-05-30`).
- [ ] 3.2 `tests/test_registro_de_coleta.py`: os cenários do histórico da própria série —
      ordem, registro a conferir sem pontos, invalidado com motivo, demais registros
      preservados, série interrompida com histórico completo, 403 de série alheia e de outro
      papel (`RF-05-37`, `RF-05-38`).
- [ ] 3.3 `tests/test_desafio_de_coleta.py` e `tests/test_solicitacao_de_local.py`: os cenários
      dos desafios disponíveis — vigência vencida fora, granularidade acima do teto fora,
      concordância com a abertura da série, já assumido assinalado, 403 de outro papel — e os
      das próprias solicitações — as três situações, motivo da recusa, local criado, nenhuma de
      outro solicitante, 403 de outro papel (`RF-05-30`, `RF-05-32`).
- [ ] 3.4 `tests/test_coletas_rota.py` e `tests/test_solicitacao_de_local_rota.py`: as quatro
      rotas no ar, com o contrato de listagem — cursor, tamanho, 422 do parâmetro não
      declarado — e o recorte por papel.

## 4. Testes da App 05

- [ ] 4.1 Testes das telas de série e abertura: lista com próxima medição e pontos, série
      interrompida com o caminho de retomada, desafio inelegível não oferecido, recusa da
      abertura explicada sem termo técnico (`RF-05-30`, `RF-05-31`, `RF-05-36`).
- [ ] 4.2 Testes do registro: origem `manual` na digitação, origem `voz` no ditado com o áudio
      nunca enviado, mídia pedida quando a forma do tipo assim exige, devolutiva do "a
      conferir" sem acusação, recusa sem rede sem nada guardado no aparelho (`RF-05-33`,
      `RF-05-34`, `RF-05-35`, `RF-05-85`).
- [ ] 4.3 Testes do histórico, das solicitações de local e do aviso de coleta: motivo do
      registro invalidado visível, situação e motivo da solicitação, aviso presente sem
      bloquear a tela, nenhum dado de outra criança em nenhuma tela (`RF-05-32`, `RF-05-37`,
      `RF-05-38`, `RF-05-57`, `RN-05-21`).

## 5. Documentação

- [ ] 5.1 Gravar a decisão do fundador de 2026-08-26 — **o ditado por voz do registro de coleta
      é transcrito no aparelho, sem áudio ao núcleo e sem custo de nuvem** — no documento 03
      (§§7 e 12.2, onde o descarte do áudio já está) e como linha nova em "Já decididos" do
      documento 09; aplicar ao PRD-05 §§6.4 e 11 sem repetir o texto normativo.
- [ ] 5.2 Corrigir a redação da tabela de rotas do PRD-05 §9 para as rotas que existem —
      `series-de-coleta/minhas` e `registros-de-coleta` no lugar de `eu/series` e
      `series/{id}/registros` — e acrescentar as três rotas novas (design — decisão 5);
      atualizar `docs/prds/index.md` com a segunda fatia do PRD-05. O documento 99 não muda:
      nenhuma relação entre documentos foi alterada, e nenhum arquivo novo entra em `docs/`.
