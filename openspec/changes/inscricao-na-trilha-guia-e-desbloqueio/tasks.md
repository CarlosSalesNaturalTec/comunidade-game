# Tarefas — inscrição na trilha, guia do percurso e desafio de desbloqueio

## 1. Documentação da decisão nova — antes do código

- [x] 1.1 Gravar no documento 11 §2.2 que o **desbloqueio da missão é fato do Guerreiro(a) na
      trilha** e que o **quiz o núcleo afere, o desafio prático o Mestre autor julga** — uma
      linha na tabela de elementos da missão e uma nas regras que fecham o modelo, sem
      reabrir o que já está lá. Verificar que nenhum outro documento repete a regra.
- [x] 1.2 Mover no documento 09 §1 as duas decisões para "Já decididos", com data e origem
      (change desta fatia), e abrir as duas pendências novas: a **marcação item a item da H5**
      e a **divergência dos níveis 2 e 4** entre "missão desbloqueada" e "missão com Resultado
      lançado". Verificar que a tabela continua fechando e que nada foi duplicado.
- [x] 1.3 Aplicar as decisões no PRD-09 (§§6.4 e 9 — a rota do julgamento do desafio prático,
      que nenhum PRD declarava) e no PRD-05 (§§6.2 e 13), citando o identificador sem repetir
      texto normativo. Verificar `mkdocs build --strict` e `npm run lint`.

## 2. Núcleo — inscrição na trilha (`RF-05-09`, `RN-05-43`, `RN-05-44`)

- [x] 2.1 Criar o modelo `InscricaoNaTrilha` e a migração, com unicidade em
      (`guerreiro_id`, `trilha_id`) — design, decisão 1. Verificar que a migração sobe e
      desce limpa no banco de teste.
- [x] 2.2 Implementar a regra da inscrição em `trilhas/regra.py`: exige trilha publicada
      (422), é ato do próprio Guerreiro(a) (403 para terceiro), a segunda inscrição na mesma
      trilha devolve a existente, e várias trilhas convivem. Verificar por
      `uv run pytest tests/test_inscricao_na_trilha.py -x`.
- [x] 2.3 Expor `POST /v1/eu/trilhas/{id}/inscricao` e `GET /v1/eu/trilhas` — a lista traz as
      trilhas inscritas com a próxima missão de cada uma e nunca inscrição de terceiro
      (`RF-05-08`, `RF-05-17`, `RN-05-21`). Verificar pelos testes de rota do mesmo arquivo.

## 3. Núcleo — desafio de desbloqueio e percurso (`RF-09-26`, `RF-05-13`, `RF-05-14`)

- [x] 3.1 Acrescentar o **desafio de desbloqueio** à `Missao` — coluna anulável, quiz ou
      desafio prático — e a migração; declarar de novo substitui o anterior, como a cadência
      de retomada já faz (design, decisão 4). Verificar que missão sem desafio segue
      publicável.
- [x] 3.2 Expor `POST /v1/missoes/{id}/desbloqueio` para o **Mestre autor** declarar o
      desafio, com 403 para quem não é autor (`RF-09-26`). Verificar por
      `uv run pytest tests/test_desbloqueio_da_missao.py -x`.
- [x] 3.3 Criar o modelo `DesbloqueioDaMissao` e a migração, com unicidade em
      (`guerreiro_id`, `missao_id`) — design, decisão 1.
- [x] 3.4 Implementar a submissão do **quiz** pelo Guerreiro(a) inscrito: o núcleo afere,
      passando grava o desbloqueio na mesma transação, não passando permite repetir sem
      limite e sem punição; sem inscrição recusa com 422; o ato não credita ponto
      (`RF-05-13`, `RF-05-14`, `RN-05-06`, `RN-05-20`). Expor
      `POST /v1/eu/missoes/{id}/desbloqueio`.
- [x] 3.5 Implementar o **desafio prático**: o Guerreiro(a) declara que cumpriu, o Mestre
      autor julga (403 para quem não é autor), o desbloqueio nasce no julgamento e enquanto
      ele não vem a missão fica "aguardando o Mestre", nunca reprovada — design, decisão 5.
      Expor a rota de julgamento e a listagem do que espera julgamento, para a App 09.
- [x] 3.6 Implementar a derivação do percurso em `trilhas/regra.py`: próxima missão pela
      menor `posicao` sem desbloqueio, bloqueadas com o **motivo** nomeando a anterior,
      opcional marcada e fora da conta do nível, sondagem como próxima até ser respondida e
      sem certificar nível (`RF-05-08`, `RF-05-10`, `RF-05-72`, `RF-05-73`, `RF-05-81`,
      `RN-05-33`, `RN-05-34`) — design, decisões 2 e 3. Expor
      `GET /v1/eu/trilhas/{id}/missoes/{ordem}` com o **estado da missão no percurso**, sem
      duplicar o conteúdo que `GET /v1/trilhas/{id}` já serve (design, decisão 6).
- [x] 3.7 Expor `GET /v1/eu/progresso`: nível, obrigatórias desbloqueadas, quantas faltam
      para o próximo e badges e recompensas por trilha ou poder, reaproveitando as consultas
      que já existem (`RF-05-15`, `RF-05-16`, `RN-05-03`, `RN-05-04`) — design, decisão 7.

## 4. Núcleo — a segunda condição do nível 1 (`RF-05-09`, `RN-05-43`)

- [x] 4.1 Em `pontuacao/regra.py`, fazer `avaliar_niveis` exigir **inscrição e** primeira
      atividade realizada para certificar o `NIVEL_1`, sem tocar nos níveis 2, 4 e 5 (design,
      decisão 8; proposal — pendência (b)). Verificar por
      `uv run pytest tests/test_pontuacao.py -x`, incluindo que resultado sem inscrição não
      certifica e que a certificação vem assim que a inscrição existe.

## 5. Testes do núcleo

- [x] 5.1 `tests/test_inscricao_na_trilha.py` — os cenários da capacidade
      `inscricao-na-trilha`: trilha publicada exigida, ato do próprio Guerreiro(a), segunda
      inscrição sem vínculo novo, várias trilhas, ausência de desinscrição, leitura só das
      próprias e lista vazia sem erro.
- [x] 5.2 `tests/test_desbloqueio_da_missao.py` — os cenários da capacidade
      `desbloqueio-da-missao`: autoria do desafio e substituição, missão sem desafio
      publicável, quiz aferido pelo núcleo, desbloqueio de um não alcança o colega, repetição
      sem punição, 422 sem inscrição, desbloqueio sem crédito de ponto, julgamento do prático
      pelo Mestre autor com 403 para terceiro e "aguardando o Mestre" enquanto não julga.
- [x] 5.3 `tests/test_percurso_da_trilha.py` — a derivação: próxima missão, bloqueio com
      motivo, missão desbloqueada permanece aberta, 403 no percurso alheio, sondagem como
      próxima e depois a primeira comum, sondagem sem nível nem ponto, opcional marcada e
      fora do denominador.
- [x] 5.4 Estender `tests/test_pontuacao.py` com os três cenários do nível 1 modificados —
      inscrição com atividade certifica, resultado sem inscrição não certifica, inscrição sem
      atividade não certifica — e confirmar que os cenários de níveis 2, 4 e 5 seguem verdes.

## 6. App 05 — o bloco da trilha

- [x] 6.1 Criar `apps/app-05-guerreiro/src/api/trilha.ts` com as chamadas do bloco, e
      acrescentar "Trilha" como terceiro item do nav de `AreaDoGuerreiro.tsx`, atualizando o
      comentário que hoje a declara fatia futura. Verificar por `vitest run` no app.
- [x] 6.2 `EscolhaDoPoder.tsx` — catálogo de poderes do ciclo, trilhas publicadas do poder
      escolhido e inscrição; nenhuma ação de desinscrever (`RF-05-09`).
- [x] 6.3 `GuiaDaTrilha.tsx` — abre na próxima missão com o que fazer e o que ela desbloqueia,
      alterna entre trilhas preservando o contexto, e sem inscrição leva à escolha do poder
      (`RF-05-08`, `RF-05-17`).
- [x] 6.4 `Missao.tsx` — conteúdo na ordem do autor com crédito e licença, bibliografia com
      título, capítulo e disponibilidade no ponto de apoio (indeterminada sem vínculo), e
      missão bloqueada com o motivo e a opcional marcada (`RF-05-10`, `RF-05-11`, `RF-05-12`,
      `RF-05-81`).
- [x] 6.5 `Sondagem.tsx` — primeiro passo da trilha recém inscrita, dizendo que serve para o
      Mestre ajustar e que não muda o nível, sem apresentar acerto e erro como nota
      (`RF-05-72`, `RF-05-73`).
- [x] 6.6 `DesafioDeDesbloqueio.tsx` — realiza o desafio; passando no quiz a seguinte abre na
      hora, no prático a tela informa que aguarda o Mestre, e não passando convida a tentar
      de novo sem contagem de fracassos (`RF-05-13`, `RF-05-14`).
- [x] 6.7 `Progresso.tsx` — nível e quantas obrigatórias faltam, pontos, badges e recompensas
      por trilha ou poder, "aguardando lançamento" para o que o Mestre não lançou, e nenhuma
      ação de lançar resultado, presença ou mérito (`RF-05-15`, `RF-05-16`, `RF-05-18`,
      `RN-05-06`).
- [x] 6.8 Testes do bloco — um arquivo por tela, cobrindo os cenários da capacidade
      `area-do-guerreiro` desta fatia, no padrão dos testes de `coleta/` e `carteira/`.

## 7. App 09 — a bancada do desafio

- [x] 7.1 Tela de autoria do desafio de desbloqueio na missão, com quiz ou desafio prático,
      sinalizando a missão que ainda não o tem e sem oferecer edição em trilha alheia
      (`RF-09-26`).
- [x] 7.2 Bancada dos **desafios práticos a julgar**: declarações não julgadas das próprias
      trilhas, com Guerreiro(a), missão e data; julgar abre a missão seguinte para aquele
      Guerreiro(a), e a tela diz que não passar não elimina ninguém (`RF-09-26`, `RF-05-13`,
      `RF-05-14`).
- [x] 7.3 Testes das duas telas, cobrindo os cenários da capacidade `area-do-mestre` desta
      fatia.

## 8. Fechamento da documentação

- [x] 8.1 Acrescentar a linha desta fatia à seção do PRD-05 em `docs/prds/index.md` — uma
      linha na tabela de fatias, e a nota de que ela também atende `RF-09-26` do PRD-09.
      Nenhum arquivo novo nasce em `docs/`, então a `nav` do `mkdocs.yml` não muda; o
      documento 99 só muda se a relação entre documentos tiver mudado, o que esta fatia não
      faz.
