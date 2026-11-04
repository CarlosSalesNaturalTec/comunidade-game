# Tasks

## 1. PRDs: os identificadores antes do código

- [ ] 1.1 Revisar o PRD-09 criando `RF-09-132` (a bancada exibe a produção entregue e o
      critério de aceite), `RF-09-133` (o julgamento tem dois vereditos — cumpriu e
      publicável), `RF-09-134` (o julgamento registra o motivo em linguagem simples),
      `RF-09-135` (julgar que cumpriu credita 5 pontos regulares na trilha da missão),
      `RN-09-52` (publicável só sobre entrega cumprida e com comprovação gravada), `RN-09-53`
      (motivo exigido em todo veredito negativo), `RN-09-54` (a reprovação não apaga a
      declaração; entregar de novo reabre a mesma linha) e `RN-09-55` (os 5 pontos creditam uma
      vez por par Guerreiro(a)–missão, sem retroatividade) — na §6.4, na §7, na linha de
      `DesbloqueioDaMissao` da §8, na §9 e na §15 de rastreabilidade (origem 02 §4 e 11 §§2.2 e
      5); verificar que nenhum dos oito já existia com
      `grep -o "R[FN]-09-[0-9]*" docs/prds/prd-09-area-do-mestre.md | sort -u`
- [ ] 1.2 Revisar o PRD-05 criando `RF-05-94` (a tela do prático apresenta o veredito do Mestre
      e o motivo, e reabre a entrega quando não cumpriu) e **corrigindo o enunciado do
      `RN-05-52`**, que hoje manda apagar a comprovação com a declaração reprovada e a decisão
      do fundador de 2026-11-04 reverte; atualizar a §15 de rastreabilidade do PRD-05 nas duas
      linhas
- [ ] 1.3 Conferir se a §11 (LGPD) dos dois PRDs precisa de linha nova: o motivo é texto do
      Mestre dirigido à criança, e a comprovação reprovada passa a **ficar guardada** em vez de
      ser apagada no julgamento — registrar a conclusão no PR, ainda que seja "não precisa"

## 2. Núcleo: os dois vereditos, o motivo e o que para de apagar (`RF-09-133`, `RF-09-134`, `RN-09-52` a `RN-09-54`)

- [ ] 2.1 Migração Alembic em `desbloqueio_da_missao`: renomear `aprovado` para `cumpriu`,
      acrescentar `publicavel` (`Boolean`, anulável), `motivo_do_julgamento` (`Text`, anulável)
      e `julgado_em` (`DateTime(timezone=True)`, anulável), com `downgrade` que desfaz os
      quatro. Sem *backfill*: nenhum saldo muda e nenhuma linha é apagada (design — decisão 3).
      Verificar com `alembic upgrade head`, `alembic downgrade -1` e o teste de paridade entre
      `head` e `Base.metadata` que já existe
- [ ] 2.2 Atualizar `DesbloqueioDaMissao` em `backend/src/nucleo/trilhas/modelo.py` com as
      quatro colunas e reescrever a *docstring*, que hoje descreve o apagamento da linha
      reprovada; citar `RF-09-133`, `RF-09-134`, `RN-09-54` e as decisões 1 a 3 do design
- [ ] 2.3 Reescrever `julgar_desafio_pratico` em `trilhas/regra.py` para receber os dois
      vereditos e o motivo: exigir o motivo quando `cumpriu` é falso ou quando `publicavel` é
      falso com `cumpriu` verdadeiro (`RN-09-53`); recusar `publicavel` sem `cumpriu` e sobre
      entrega presencial ou sem comprovação gravada (`RN-09-52`); **parar de apagar** a linha
      reprovada, gravando veredito, motivo e `julgado_em` (`RN-09-54`); manter o 403 de quem
      não é autor e o 422 de julgar o já julgado, inclusive da linha legada (`julgado_em` nulo
      com `cumpriu` verdadeiro)
- [ ] 2.4 Fazer a entrega reabrir a declaração recusada em `submeter_desafio_de_desbloqueio`,
      no caminho do prático:
      `cumpriu`, `publicavel`, `motivo_do_julgamento` e `julgado_em` voltam a nulo e a
      comprovação é substituída, sem segundo registro; manter o 422 de entregar sobre o que já
      foi julgado como cumprido (`RN-09-54`, `RN-05-52`)
- [ ] 2.5 Trocar `JulgarDesafioPraticoEntrada` em `trilhas/rotas.py` por `cumpriu: bool`,
      `publicavel: bool` e `motivo: str | None`, mantendo `extra="forbid"`, e devolver os três
      vereditos gravados na resposta; ajustar as leituras que citam `aprovado` —
      `listar_desbloqueios_praticos_pendentes` e `derivar_percurso` — ao nome novo, sem mudar o
      predicado de três estados (design — decisão 1)

## 3. Núcleo: os 5 pontos (`RF-09-135`, `RN-09-55`)

- [ ] 3.1 Criar `VALOR_DO_DESBLOQUEIO_PRATICO = 5` e
      `creditar_pontuacao_do_desbloqueio_pratico` em `backend/src/nucleo/pontuacao/regra.py`,
      no molde de `creditar_pontuacao_da_criacao_original` — credita ponto regular ao
      Guerreiro(a) que entregou, na trilha da missão, e **não** certifica nível nem concede
      badge (design — decisão 4), com o comentário citando o documento 11 §5
- [ ] 3.2 Chamá-la de `julgar_desafio_pratico` na mesma transação, só quando `cumpriu` é
      verdadeiro, e nunca na linha legada nem no rejulgamento recusado (`RN-09-55`)

## 4. Núcleo: o veredito servido ao Guerreiro(a) e a bancada (`RF-09-132`, `RF-05-94`)

- [ ] 4.1 Acrescentar a `MissaoNoPercursoSaida` e ao percurso o veredito, o motivo e o momento
      do julgamento, ao lado de `comprovacao_entregue`, servidos só ao próprio Guerreiro(a)
      (`RF-05-94`, design — decisão 5)
- [ ] 4.2 Acrescentar a `DesbloqueioPendenteSaida` o **tipo do arquivo** da comprovação, para
      a tela saber como apresentá-la, conferindo antes o que a fatia 13 já pôs lá — critério de
      aceite e comprovação entregue já estão (`RF-09-132`). A saída devolve hoje
      `guerreiro_nome`, e a linha 27 do cronograma descreve a bancada como mostrando o **nick**:
      a divergência é anterior a esta fatia e não entra no recorte — levá-la ao fundador no PR,
      não corrigi-la aqui
- [ ] 4.3 Testes de núcleo em `backend/tests/test_desbloqueio_da_missao.py` e
      `test_percurso_da_trilha.py`, cobrindo os cenários dos deltas de `desbloqueio-da-missao`:
      os dois vereditos num ato só; cumpriu sem publicável; publicável recusado sobre o não
      cumprido e sobre a entrega presencial; motivo exigido nos dois vereditos negativos e
      dispensado em cumpriu-e-publicável; a declaração recusada que **permanece** com o motivo;
      entregar de novo reabrindo a mesma linha, sem segundo registro; o 422 de julgar o já
      julgado e de entregar sobre o cumprido; o percurso trazendo veredito e motivo ao próprio
      Guerreiro(a) e 403 a terceiro; e a linha legada, que não se rejulga e não credita.
      Verificar com
      `uv run pytest tests/test_desbloqueio_da_missao.py tests/test_percurso_da_trilha.py -x`
- [ ] 4.4 Testes do crédito em `backend/tests/test_pontuacao.py`, cobrindo os cenários do delta
      de `pontos-niveis-e-badges`: os 5 pontos na trilha da missão e só a quem entregou; o
      crédito sem Resultado algum na missão; recusado-reaberto-cumprido creditando uma vez; o
      não cumprido que não credita nem debita; nenhum nível certificado e nenhum badge
      concedido; e o julgado antes da regra, sem crédito retroativo. Verificar com
      `uv run pytest tests/test_pontuacao.py -x`

## 5. App 09: a bancada com a produção à vista (`RF-09-132`, `RF-09-133`, `RF-09-134`)

- [ ] 5.1 Estender `apps/app-09-mestre/src/trilhas/api.ts`: os três campos do julgamento em
      `julgarDesafioPratico`, e em `DesbloqueioPendente` a comprovação, o critério de aceite e o
      tipo do arquivo
- [ ] 5.2 Reescrever `TelaDeDesbloqueiosPendentes.tsx` para apresentar, em cada pendência, a
      comprovação entregue — texto e endereço como texto, imagem, áudio e vídeo pelo
      `MidiaDoNucleo` de `comum/react`, arquivo pelo controle de abrir — e o critério de aceite
      ao lado; dizer a entrega no encontro como presencial, nunca como entrega faltando, e
      seguir permitindo julgar quando a mídia não carrega (`RF-09-132`)
- [ ] 5.3 Acrescentar à mesma tela os dois vereditos em controles distintos, o campo do motivo
      e o envio num ato só; manter `publicavel` indisponível quando o Mestre marca que não
      cumpriu e na entrega presencial, e o controle de julgar indisponível enquanto falta motivo
      num veredito negativo; dizer o que cada veredito faz, que o motivo é lido pelo
      Guerreiro(a) e que não passar não o elimina (`RF-09-133`, `RF-09-134`, `RN-09-52`,
      `RN-09-53`)
- [ ] 5.4 Mostrar a recusa do núcleo com o motivo, sem apagar o veredito marcado nem o texto
      escrito
- [ ] 5.5 Testes em `apps/app-09-mestre/src/turmas/TelaDeDesbloqueiosPendentes.test.tsx` dos
      cenários do delta de `area-do-mestre`: a produção aparece na bancada; a comprovação
      escrita aparece como texto; a entrega no encontro é dita como tal; a mídia que não carrega
      não impede julgar; os dois vereditos e o motivo vão num ato só; publicável indisponível
      nos dois casos; o motivo exigido antes do toque e dispensado em cumpriu-e-publicável; e a
      recusa que chega sem limpar a tela. Verificar com
      `npm run test --workspace apps/app-09-mestre`

## 6. App 05: o veredito e o motivo na tela do prático (`RF-05-94`)

- [ ] 6.1 Estender `comum/trilha/api.ts` com o veredito, o motivo e o momento do julgamento em
      `MissaoNoPercurso`, o tipo que a tela do prático já consome
- [ ] 6.2 Apresentar em `comum/trilha/DesafioDeDesbloqueio.tsx` o que o Mestre decidiu: se
      cumpriu, se vai à vitrine e o motivo **na íntegra**, sem resumir nem esconder; não tendo
      cumprido, oferecer entregar de novo em linguagem acolhedora, com a comprovação anterior à
      vista e sem contagem de tentativas; tendo cumprido, apresentar o que foi entregue e
      nenhum controle de entrega; antes do julgamento, seguir dizendo que a missão aguarda o
      Mestre (`RF-05-94`, `RN-05-20`, `RN-09-54`)
- [ ] 6.3 Testes em `apps/app-05-guerreiro/src/trilha/DesafioDeDesbloqueio.test.tsx` dos
      cenários dos deltas de `area-do-guerreiro`: cumprido e publicável dizendo as duas coisas;
      cumprido e não publicável com o motivo; não cumprido com o motivo e o convite a entregar
      de novo; nenhuma nota nem comparação; a espera antes do julgamento; a entrega reaberta com
      a comprovação anterior à vista; e a entrega encerrada depois de cumprido. Verificar com
      `npm run test --workspace apps/app-05-guerreiro`

## 7. Fechamento

- [ ] 7.1 Marcar a fatia 27 do bloco PRD-09 como `implementado` no
      `openspec/cronograma-de-fatias.md`, com o slug desta change na coluna Recorte, e
      **retirar `livro-razao`** da lista de deltas previstos naquela linha, registrando que era
      estimativa de planejamento (decisão do fundador de 2026-11-04, design — decisão 6)
- [ ] 7.2 Acrescentar à linha do documento 09 §1 "O portfólio é o acervo: comprovação no
      prático e os dois vereditos do Mestre" a **quarta reversão** — a reprovação do prático
      deixa de apagar a declaração, que passa a guardar o veredito e o motivo —, corrigindo o
      "Três reversões declaradas", que esta fatia torna quatro; e conferir que nada mais em
      `docs/` mudou por esta change: a decisão já está nos documentos 02 §4, 11 §§2.2 e 5 e
      99 §6, a situação do PRD-09 em `docs/prds/index.md` não muda e nenhum arquivo novo entra
      na `nav` do `mkdocs.yml` — as únicas revisões em `docs/` são as dos PRDs, das tarefas 1.1
      e 1.2

## Workflow follow-up

- Abrir o PR com os artefatos, o código, os testes e a revisão dos dois PRDs, e aguardar a
  aprovação do fundador. O merge usa merge commit, nunca squash.
- Arquivar a change depois do merge, com `/opsx:archive`, consolidando os deltas em
  `openspec/specs/`.
