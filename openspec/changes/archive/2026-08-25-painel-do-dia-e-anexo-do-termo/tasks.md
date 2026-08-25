## 1. Escolha da equipe no núcleo

- [x] 1.1 Acrescentar à equipe da aula a **atividade corrente**, sobrescrita a cada declaração e
      nunca acumulada, com a migração correspondente; verificar que a coluna aceita nulo e que a
      equipe da trilha não a recebe (`RF-02-42`, `RF-04-35`)
- [x] 1.2 Implementar a regra de declaração da escolha: só integrante daquela equipe declara
      (403 para os demais), só atividade da programação daquela aula é aceita (422 fora dela), e
      declarar de novo substitui a corrente (`RF-02-42`, `RF-04-35`)
- [x] 1.3 Dar porta HTTP à declaração, sob a sessão do Guerreiro(a), e servir a escolha corrente
      junto da programação em `GET /v1/equipes/{id}/missao`; verificar pelo OpenAPI que a rota
      nasceu sob `/v1` (`RF-04-35`, `RF-01-16`)

## 2. Anexo da digitalização do termo

- [x] 2.1 Criar o `AnexoDoTermo` como registro próprio que aponta para o consentimento, com quem
      anexou e quando, sem tocar em coluna alguma do consentimento; verificar que o consentimento
      segue de somente inserção (`RF-02-68`, `RN-01-12`)
- [x] 2.2 Implementar a regra do anexo pela `PortaDeArmazenamento`, no caminho simples do
      comprovante de aporte: PDF, JPG ou PNG (422 fora dos três), só tipo `biometria` (422 para
      `autorizacao_de_divulgacao`), segundo anexo recusado com 409 (`RF-02-68`)
- [x] 2.3 Expor `POST /v1/consentimentos/{id}/anexo` restrita a Admin (403 para as demais
      personas), com a digitalização fora de rota pública e a escrita na trilha de auditoria
      (`RF-02-68`, `RN-02-21`)

## 3. Painel do dia no núcleo

- [x] 3.1 Criar `backend/src/nucleo/painel_do_dia/` como módulo só de leitura, sem modelo e sem
      migração, que resolve a aula em andamento pela janela de data e horários e devolve o
      encontro vazio fora de toda janela (`RF-02-41` a `RF-02-47`)
- [x] 3.2 Compor as presenças com o modo de comprovação e quem confirmou, e derivar **quem
      aguarda aparelho** — presente sem equipe naquela aula — em consulta, sem entidade nem fila
      (`RF-02-41`, `RF-02-43`)
- [x] 3.3 Compor as equipes com integrantes e a missão da atividade corrente declarada, deixando
      em branco a equipe que não declarou (`RF-02-42`, `RF-02-08`)
- [x] 3.4 Compor a atividade prevista, as reservas da aula e o saldo dos tipos de recurso do ponto
      de apoio, tomando os tipos do catálogo configurável e sem fixar tipo algum em código
      (`RF-02-44`, `RF-02-45`, `RN-07-36`)
- [x] 3.5 Compor os lançamentos pendentes do encontro — a atividade realizada ainda não lançada e
      os termos de biometria sem digitalização — e verificar que cada um sai da lista quando a
      rota que o atende é executada (`RF-02-46`, `RF-02-47`, `RF-02-69`)
- [x] 3.6 Expor `GET /v1/painel-do-dia` para Admin e Mestre, com o Mestre limitado às comunidades
      dele e 403 para Guerreiro(a), responsável e Apoiador, devolvendo a criança só por nick e
      avatar (`RN-02-20`, `RN-02-22`)

## 4. Testes do núcleo

- [x] 4.1 `tests/test_equipe_escolha.py` — declaração, troca que substitui, atividade fora da
      programação (422), não integrante (403), leitura que não grava escolha e escolha que não
      sobrevive à aula (`RF-02-42`, `RF-04-35`)
- [x] 4.2 `tests/test_consentimento_anexo.py` — anexo aceito nos três formatos, formato recusado
      (422), tipo `autorizacao_de_divulgacao` recusado (422), segundo anexo (409), Mestre
      recusado (403) e consentimento inalterado depois do anexo (`RF-02-68`)
- [x] 4.3 `tests/test_painel_do_dia.py` — encontro em andamento numa leitura, encontro vazio fora
      da janela, presença do reconhecimento sem lançamento manual, presente sem equipe na espera
      e saída dela ao entrar numa equipe, equipe com e sem missão, saldo pelo ponto de apoio da
      aula, tipo novo do catálogo aparecendo, pendências entrando e saindo, e as recusas por
      persona (`RF-02-41` a `RF-02-47`, `RF-02-69`, `RN-02-20`)
- [x] 4.4 Cobrir no mesmo arquivo os critérios de aceite do PRD-02 §12 que esta fatia atende:
      presença do App 01 aparece no painel sem lançamento manual, e o painel mostra saldo e
      lançamentos pendentes do encontro em andamento (`RF-02-41`, `RF-02-45`, `RF-02-46`)

## 5. App 01 — declarar a escolha

- [x] 5.1 Na tela da programação, oferecer a escolha da atividade, mostrar qual está corrente e
      declará-la ao núcleo, sem eleger nenhuma por conta própria quando há mais de uma
      (`RF-04-35`, `RF-02-42`)
- [x] 5.2 Sem rede, manter legível o conteúdo já carregado, dizer que a escolha está indisponível
      e não enfileirar a declaração, como já vale para a resposta de quiz (`RF-04-58`)
- [x] 5.3 Testes da tela da programação cobrindo escolha, troca, programação com duas atividades
      sem corrente e o comportamento sem rede (`RF-04-35`, `RF-04-58`)

## 6. App 03 — área Painel do dia

- [x] 6.1 Criar `apps/app-03-gestao/src/painel-do-dia/` com a tela de leitura do encontro:
      presenças, espera, equipes com missão, previsto e provido, saldo e lançamentos pendentes,
      cada pendência levando à tela que a resolve (`RF-02-41` a `RF-02-47`, `RF-02-69`)
- [x] 6.2 Manter a tela atualizada por sondagem, no padrão da condução da partida, avisando a
      queda de rede sem apagar o que carregou e retomando sozinha (`RF-02-48`)
- [x] 6.3 Oferecer ao Admin, a partir da pendência, o envio da digitalização em PDF, JPG ou PNG,
      com a recusa explicada em linguagem simples e sem oferecer o caminho ao Mestre
      (`RF-02-68`, `RN-02-20`)
- [x] 6.4 Garantir que a tela apresenta a criança só por nick e avatar, sem imagem real
      (`RN-02-22`)
- [x] 6.5 Testes da área cobrindo a tela com encontro, a frase de "não há encontro em andamento",
      a ausência de caminho de escrita, a atualização por sondagem, o envio da digitalização e a
      recusa de formato (`RF-02-41` a `RF-02-48`, `RF-02-68`, `RF-02-69`)

## 7. App 09 — caminho para o painel

- [x] 7.1 Em Minhas turmas, oferecer o caminho para o painel do dia da App 03 apenas na aula em
      andamento, sem reconstruir o painel; testes cobrindo a aula na janela, a aula fora dela e a
      ausência de cópia própria (`RF-09-50`, `RN-02-20`)

## 8. Documentação

- [x] 8.1 Corrigir no PRD-02 as três respostas do fundador de 2026-08-25: o `RF-02-43` como
      derivado de presença sem equipe, o `RF-02-45` sem fixar tipos de recurso — no requisito e no
      critério de aceite da §12 —, e o `RF-02-46`/`RF-02-47` consolidados num enunciado só; gravar
      na §13 a decisão de passar a gravar a escolha da equipe, e alinhar o PRD-04 §6.2 no
      `RF-04-35`. Narrar a fatia em `docs/prds/index.md`. Nenhuma linha nova no documento 09,
      nenhum arquivo novo em `docs/` e nenhuma alteração na `nav` do `mkdocs.yml`
