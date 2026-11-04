# Tasks

## 1. Modelo e migração da comprovação

- [ ] 1.1 Acrescentar a `DesbloqueioDaMissao` (`backend/src/nucleo/trilhas/modelo.py`) as cinco
      colunas anuláveis da comprovação — `comprovacao`, `comprovacao_referencia`,
      `comprovacao_tamanho`, `comprovacao_tipo_do_arquivo` e `entrega_presencial` —, com a
      _docstring_ dizendo que exatamente um entre comprovação e entrega presencial é preenchido e
      que a linha apagada no julgamento reprovado leva a comprovação junto (`RF-05-91`,
      `RN-05-51`, `RN-05-52`, design — decisões 1 e 3).
- [ ] 1.2 Criar a revisão Alembic das cinco colunas, sem _backfill_, com `downgrade` que as
      derruba; verificar pelo teste de paridade entre `alembic upgrade head` e `Base.metadata`
      que já está na suíte (`RF-05-91`, design — Migration Plan).

## 2. Lista de tipos e tetos de tamanho compartilhados

- [ ] 2.1 Extrair de `backend/src/nucleo/criacoes_originais/regra.py` a lista fechada de MIME e os
      tetos por tipo — 200 MB para vídeo, 20 MB para os demais — para onde a comprovação e a
      criação original os leiam dos mesmos nomes, sem duplicá-los, mantendo o comportamento atual
      da criação (`RF-05-91`, design — decisão 4).
- [ ] 2.2 Afirmar em `backend/tests/test_criacao_original.py` que a recusa por tipo fora da lista e
      por tamanho acima do teto segue idêntica depois da extração — o teto citado na mensagem
      inclusive (`RF-05-91`).

## 3. Regra da entrega e da exigência

- [ ] 3.1 Em `backend/src/nucleo/trilhas/regra.py`, fazer `submeter_desafio_de_desbloqueio`
      receber a comprovação e a escolha de entrega presencial: conferir a forma entregue contra
      `missao.desafio_pratico_forma_de_comprovacao` com 422 na divergência, recusar com 422 os dois
      vazios e os dois cheios nomeando o que falta, gravar texto e link em `comprovacao` e deixar a
      mídia para o envio, e aceitar sem comprovação o prático antigo que não tem forma declarada
      (`RF-05-91`, `RN-05-51`, design — decisões 2, 3 e 7).
- [ ] 3.2 Fazer a entrega nova antes do julgamento **substituir** a anterior na mesma linha, e
      recusar com 422 a entrega em prático já julgado como cumprido; conferir que o julgamento
      reprovado, que já apaga a linha, leva a comprovação com ela sem código de limpeza próprio
      (`RN-05-52`, `RN-05-20`).
- [ ] 3.3 Acrescentar a `regra.py` abrir, confirmar e ler o envio da comprovação, no molde de
      `abrir_envio_da_criacao`, `confirmar_envio_da_criacao` e `ler_arquivo_da_criacao`: a sessão
      retomável recebe a origem de quem envia, a referência só é gravada ao confirmar, a leitura
      autoriza o próprio Guerreiro(a) e o Mestre autor com 403 para o resto, e responde 404 sem
      mídia ou com envio não concluído (`RF-05-91`, `RF-05-93`, design — decisão 4).
- [ ] 3.4 Cobrir em `backend/tests/test_desbloqueio_da_missao.py` os cenários das specs de
      `desbloqueio-da-missao`: a comprovação gravada com a declaração nas formas texto, link e
      mídia; a forma divergente e o quiz com comprovação recusados; a declaração sem comprovação e
      sem alternativa recusada; a entrega presencial gravada sem mídia e não contada como tentativa
      falha; a substituição antes do julgamento e a recusa depois do aprovado; a comprovação que
      vai com a linha apagada; e o prático antigo que segue declarável (`RF-05-91`, `RN-05-51`,
      `RN-05-52`).

## 4. Rotas da submissão e do arquivo

- [ ] 4.1 Em `backend/src/nucleo/trilhas/rotas.py`, acrescentar a comprovação e a entrega
      presencial a `SubmeterDesafioDeDesbloqueioEntrada`, que é `extra="forbid"`, e devolver na
      saída o que ficou gravado, de modo que a tela reencontre a entrega sem segunda chamada
      (`RF-05-91`, `RF-05-93`).
- [ ] 4.2 Criar `POST`, `PATCH` e `GET` de `/v1/eu/missoes/{id}/desbloqueio/comprovacao`,
      espelhando as três rotas de `/v1/criacoes/{id}/arquivo`, com a permissão do Guerreiro(a) em
      sessão na escrita e a autorização de `ler_arquivo_da_comprovacao` na leitura (`RF-05-91`,
      `RF-05-93`, design — decisão 4).
- [ ] 4.3 Fazer as três leituras que já servem o desafio devolverem a comprovação entregue ao
      Mestre autor e ao próprio Guerreiro(a) — a forma, se é entrega presencial e se há mídia —,
      sem servir bytes na listagem, para que a bancada da fatia 27 a encontre pronta (`RF-05-93`).
- [ ] 4.4 Cobrir em `backend/tests/test_desbloqueio_da_missao.py` as rotas pelo cliente HTTP: o
      corpo novo da submissão, o campo fora do contrato recusado pelo `extra="forbid"`, o ciclo
      abrir–confirmar–ler, o 403 de quem não é o autor nem quem entregou, e o 404 da comprovação
      sem mídia (`RF-05-91`, `RF-05-93`).

## 5. Camada comum da tela do prático

- [ ] 5.1 Em `comum/trilha/api.ts`, acrescentar ao tipo `DesafioDeDesbloqueio` os três campos que
      a fatia 26 já serve — forma de comprovação, critério de aceite e título curto —, levar a
      comprovação e a entrega presencial ao corpo de `submeterDesafioDeDesbloqueio`, e criar as
      funções de abrir, enviar com progresso, confirmar e ler a comprovação sobre
      `enviarParteComProgresso` e `lerArquivoDoNucleo` de `comum/api/cliente.ts` (`RF-05-91`,
      `RF-05-93`, design — decisão 5).
- [ ] 5.2 Em `comum/trilha/DesafioDeDesbloqueio.tsx`, substituir o botão nu "Já cumpri!" pelo ramo
      do prático: critério de aceite e forma aceita antes de qualquer controle, o aviso da mídia
      guardada e do destino possível à vitrine com acesso à área detalhada, o campo da forma aceita
      — corpo escrito, endereço ou arquivo —, o controle indisponível enquanto a comprovação não
      estiver preenchida, o progresso do envio com retomada na queda de rede, e a comprovação já
      entregue reapresentada em lugar de formulário vazio; o prático antigo sem os três campos
      segue realizável (`RF-05-91`, `RF-05-92`, `RF-05-93`).
- [ ] 5.3 No mesmo componente, oferecer **entregar ao Mestre no encontro** ao lado da entrega,
      enviando a declaração sem mídia e dizendo que o Mestre vai conferir no encontro, sem nenhuma
      mensagem que trate a escolha como falha, desistência ou perda da missão (`RN-05-51`).
- [ ] 5.4 Dar ao ramo do prático os estilos de `comum/trilha/estilos.css` que ele pede, reusando a
      moldura de mídia e os _tokens_ existentes, sem cor literal fora de `comum/tokens.css`
      (`RF-05-92`).
- [ ] 5.5 Cobrir em `comum/trilha/trilha.test.tsx` os cenários das specs de `area-do-guerreiro`: o
      critério e a forma antes do controle; a ausência de seletor de forma; o aviso antes da
      entrega e não depois; o controle indisponível sem comprovação; o progresso e a retomada; a
      comprovação reapresentada; a alternativa presencial à vista, enviando sem mídia e sem ser
      tratada como falha; e o prático antigo sem os três campos (`RF-05-91`, `RF-05-92`,
      `RF-05-93`, `RN-05-51`).

## 6. As duas aplicações

- [ ] 6.1 Afirmar em `apps/app-05-guerreiro/src/trilha/DesafioDeDesbloqueio.test.tsx` que a App 05
      entrega a comprovação pela tela da trilha, com o critério, o aviso e a alternativa
      presencial, pelo componente comum e sem reimplementação própria (`RF-05-91`, `RF-05-92`,
      `RN-05-51`).
- [ ] 6.2 Afirmar em `apps/app-01-aula-presencial/src/trilhas/trilhas.test.tsx` que a App 01 faz o
      mesmo pelo aparelho da aula, e que a exigência, o aviso e a alternativa não divergem da
      App 05 (`RF-04-76`).

## 7. Documentação da fatia

- [ ] 7.1 Revisar o **PRD-05** (`docs/prds/prd-05-area-do-guerreiro.md`) com `RF-05-91` a
      `RF-05-93`, `RN-05-51` e `RN-05-52` nas §§6.2, 7, 8, 9 e 15, e acrescentar à tabela da §11 a
      linha da comprovação do prático, com finalidade, base legal, retenção e quem acessa; revisar
      o **PRD-04** (`docs/prds/prd-04-aula-presencial.md`) com `RF-04-76` nas §§6 e 15. Os
      documentos-fonte já carregam a decisão de 2026-11-03 (02 §4, 11 §§2.2, 5 e 8.2, 99 §6 e
      09 §1) e **não** são reescritos.
- [ ] 7.2 Marcar a fatia 13 do bloco do PRD-05 em `openspec/cronograma-de-fatias.md` como
      implementada, trocando o recorte previsto pelo slug desta change e registrando as duas
      decisões do fundador de 2026-11-04 que a recortaram — a comprovação exigida com a
      alternativa de entrega no encontro, e a rota de leitura entrando nesta fatia. `docs/prds/`
      não muda de situação: o PRD-05 segue em implementação, e o doc 99 §8 não muda, porque o
      PRD-05 já depende do PRD-01 e do PRD-09.
