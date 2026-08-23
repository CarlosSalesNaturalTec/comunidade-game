## 1. Ocorrência de conduta — núcleo

- [x] 1.1 Criar `nucleo/ocorrencias_de_conduta/modelo.py` com `OcorrenciaDeConduta` —
      `guerreiro_id`, `aula_id`, `atividade_id`, `valor`, `motivo` anulável,
      `momento_do_fato` e `ComAutoria` — mais a migração da tabela; verificar que a migração
      sobe e desce limpa (`RF-09-46`, `RN-01-52`).
- [x] 1.2 Criar `nucleo/ocorrencias_de_conduta/regra.py` com `lancar_ocorrencia_de_conduta`:
      valor fixo de 5 gravado na coluna, recusa de requisição que traga valor, teto de 10 por
      Guerreiro(a) e por aula presencial conferido na mesma transação, motivo exigido, trilha
      derivada de atividade → missão → trilha, `conferir_posse_da_trilha` para a recusa de
      atividade alheia e recusa de atividade que não é da aula (`RF-09-46`, `RF-01-57`,
      `RN-09-08`, `RN-09-09`, doc 11 §5).
- [x] 1.3 Ligar o débito: a regra chama `debitar_ponto_regular` com a trilha derivada, na mesma
      operação da inserção, e a spec de `pontos-niveis-e-badges` deixa de tratar a conduta como
      entrega posterior; verificar saldo parando em zero, nível e badge intactos e ponto extra
      inalterado (`RF-01-57`, `RF-01-69`, `RN-01-55`).
- [x] 1.4 Fechar a imutabilidade fora do ORM, no padrão de `Lancamento`: alterar ou remover
      ocorrência gravada é recusado (`RF-09-46`, `RN-01-52`).

## 2. As três portas HTTP

- [x] 2.1 Extrair de `aulas/rotas.py` para `resultados/regra.py` a montagem comum de
      `ResultadoDeclarado`, sem alterar o comportamento da rota do Admin; verificar que a suíte
      de `resultado-de-atividade` segue verde (design — Decisão 1, risco 1).
- [x] 2.2 Criar `nucleo/resultados/rotas.py` com `POST /atividades/{id}/lancamentos` — Mestre
      autor, lista de participantes numa transação, sem consumir reserva nem mudar a situação
      da aula, 403 para atividade alheia e recusa inteira quando um participante é inválido
      (`RF-09-43`, `RF-09-44`, `RF-09-49`, `RF-09-74`).
- [x] 2.3 Acrescentar a `aulas/rotas.py` o `POST /aulas/{id}/presencas`, exigindo
      `Operacao.confirmacao_de_identidade_do_guerreiro` e recusando com 403 o modo
      reconhecimento vindo do Mestre, sem alterar `registrar_presenca` (`RF-09-45`,
      `RF-01-20`, `RF-01-17`).
- [x] 2.4 Acrescentar a `aulas/rotas.py` o `GET /minhas-turmas`, exigindo `Operacao.suas_turmas`,
      filtrado pelo escopo de comunidade do Mestre e pelas atividades de que ele é autor,
      agrupado por `FormatoDeAtividade` e paginado em `PaginaDeResultado` (`RF-09-42`,
      `RF-09-73`, `RN-09-08`).
- [x] 2.5 Criar `nucleo/ocorrencias_de_conduta/rotas.py` com a rota de lançamento e registrar os
      roteadores novos em `principal.py`; verificar que as rotas aparecem no OpenAPI sob `/v1`
      (`RF-09-46`).

## 3. Testes do núcleo

- [x] 3.1 `tests/test_ocorrencia_de_conduta.py` — cenários da spec `ocorrencia-de-conduta`:
      débito de 5 sem valor informado, 422 quando o valor vem na requisição, teto alcançado na
      terceira ocorrência, teto de um não consome o de outro, débito na trilha da atividade,
      403 para Mestre não autor, 422 sem motivo, 422 para atividade fora da aula, saldo parando
      em zero, nível e badge preservados, ponto extra intacto, recusa de alteração e omissão do
      motivo apagado.
- [x] 3.2 `tests/test_lancamento_por_atividade.py` — cenários da spec `resultado-de-atividade`:
      lançamento de vários participantes num ato, reservas e situação da aula intocadas, 403
      para Mestre não autor, recusa inteira por participante inválido e 405 na tentativa de
      editar lançamento.
- [x] 3.3 `tests/test_presenca_do_mestre.py` e cobertura de `GET /minhas-turmas` — cenários das
      specs `aula-e-presenca`: confirmação gravando o Mestre como confirmador, 403 no modo
      reconhecimento, reenvio idempotente, turmas só do Mestre em sessão, atividade de outro
      Mestre ausente, separação por formato e 403 para papel sem a operação.

## 4. App 09 — área Minhas turmas

- [x] 4.1 Criar a área Minhas turmas com a lista de aulas e atividades separadas por formato,
      exibindo Guerreiros e Guerreiras por nick e avatar (`RF-09-42`, `RF-09-73`, `RN-09-18`).
- [x] 4.2 Criar a tela de lançamento com seleção de participantes e desfecho de cada um, envio
      num ato só e recusa apresentada em linguagem simples (`RF-09-43`, `RF-09-44`, `RF-09-74`,
      `RN-09-16`).
- [x] 4.3 Criar a confirmação de presença e a tela da ocorrência de conduta — escolha da
      atividade e motivo, sem pedir valor nem item do Código de Conduta, com a recusa por teto
      explicada em linguagem simples (`RF-09-45`, `RF-09-46`, `RN-09-09`).
- [x] 4.4 Cobrir as três telas em Vitest, nos cenários da spec `area-do-mestre`.

## 5. Documentação

- [x] 5.1 Atualizar `docs/09-topicos-em-aberto-e-sugestoes.md` §1 com a pendência do fim de
      ciclo — quem apaga o motivo da ocorrência (`RN-01-52`) e quem a tira do ranking (doc 11
      §5), duas consequências do mesmo gatilho ausente — e `docs/prds/index.md` com a situação
      do PRD-09 e a correção do `RF-01-57`, hoje dado por inteiro à change
      `auditoria-e-estorno-da-coleta` quando só o estorno foi entregue. Nenhum arquivo novo em
      `docs/`, logo sem alteração na `nav` do `mkdocs.yml`; nenhuma relação entre documentos
      mudou, logo sem alteração no documento 99.
