## 1. Núcleo — entidade e matriz da consulta ao assistente

- [ ] 1.1 Criar `backend/src/nucleo/assistente/modelo.py` com `ConsultaAoAssistente` — `equipe_id`
      e `guerreiro_id` anuláveis sob `CheckConstraint` de exatamente um, `assistente`
      (`trilhas` | `apoio_escolar`), `desfecho`, `pergunta`, `resposta` e `ComAutoria` — e a
      migração Alembic da tabela; verificar que `alembic upgrade head` sobe e desce limpo e que
      o `CheckConstraint` recusa os dois vínculos juntos (`RF-04-36`, `RF-04-40`, design —
      decisão 6).
- [ ] 1.2 Acrescentar a operação `consulta_ao_assistente` à matriz de `permissoes.py`, no
      Guerreiro(a) escreve e lê; verificar pelo teste da matriz que Mestre, Admin e responsável
      não a recebem (`RF-04-36`, design — decisão 6).

## 2. Núcleo — corpus, porta e adaptadores

- [ ] 2.1 Criar `porta.py`, `local.py`, `nuvem.py` e `fabrica.py` do assistente no padrão de
      `producoes`: contrato pergunta + corpus → desfecho + resposta, adaptador local fora de
      produção sem credencial, Gemini em produção com a chave e o modelo do `template_de_missao`,
      e `None` como indisponibilidade; verificar em `tests/test_assistente_porta.py` que o local
      responde sem rede, que a nuvem devolve `None` em erro, demora e JSON fora do formato, e
      que o áudio não aparece em log algum (`RF-04-36`, `RF-04-40`, design — decisões 1, 3 e 4).
- [ ] 2.2 Implementar em `regra.py` a montagem do corpus — equipe → atividade corrente → missão →
      trilha, com os conteúdos das missões de posição ≤ à da corrente, na ordem da posição e da
      `ordem`, truncando pela mais recente para trás e mantendo a missão corrente inteira;
      verificar que conteúdo de missão de posição posterior nunca entra e que equipe sem
      atividade corrente é recusada com 422 (`RF-04-36`, `RN-04-19`, design — decisão 2).
- [ ] 2.3 Implementar em `regra.py` a gravação da consulta e os três desfechos — respondida,
      fora do corpus e tarefa escolar, todos gravados e todos em 200, com o texto da recusa e o
      do encaminhamento fixos no núcleo — e `ConsultaAoAssistenteIndisponivel` (503) sem gravar
      nada; verificar que nenhum ponto, badge, desbloqueio ou resultado nasce da consulta
      (`RF-04-37`, `RF-04-38`, design — decisões 3 e 5).

## 3. Núcleo — rota da consulta

- [ ] 3.1 Criar `POST /v1/assistente/trilhas/consultas` em `rotas.py`, em `multipart/form-data`
      com `texto` **ou** `arquivo`, restrita ao Guerreiro(a) integrante da equipe, lendo os bytes
      em memória e deixando-os sair de escopo ao fim da chamada; verificar em
      `tests/test_consulta_ao_assistente_rota.py` o 403 de quem não integra a equipe e do adulto
      em sessão, o 422 das duas formas juntas ou de nenhuma, o 200 dos três desfechos e o 503 da
      indisponibilidade (`RF-04-36` a `RF-04-40`, `RN-04-21`, PRD-04 §9).
- [ ] 3.2 Registrar o roteador em `principal.py` e conferir que a rota aparece no OpenAPI com a
      chave de aplicação exigida, como as demais rotas de dados sob `/v1` (`RF-01-02`).

## 4. App 01 — tela do assistente

- [ ] 4.1 Criar `src/api/assistente.ts` e a tela `src/trilhas/TelaDoAssistente.tsx`, alcançável da
      programação, com pergunta por texto e por fala, microfone aberto só ao toque e fechado ao
      fim da fala, e a conversa vivendo apenas no estado da tela; verificar que nenhuma gravação
      chega ao `localStorage` e que a conversa some ao fim do atendimento (`RF-04-36`, `RF-04-39`,
      `RF-04-28`, `RN-04-20`).
- [ ] 4.2 Apresentar recusa, encaminhamento à App 05 e indisponibilidade como resposta em tela —
      nunca como erro — e bloquear a pergunta sem rede sem enfileirar nada (`RF-04-37`,
      `RF-04-38`, `RF-04-58`).

## 5. App 01 — rede fora e fila local

- [ ] 5.1 Elevar o estado "sem rede" a `sessao-de-trabalho/AparelhoDaAula.tsx`, alimentado pela
      falha de chamada e pelo evento `online` do navegador, e apresentar o aviso de operação sem
      conexão em toda tela, retirando-o quando a rede volta (`RF-04-23`, `RF-04-24`, design —
      decisão 9).
- [ ] 5.2 Criar `src/fila/filaDePresenca.ts` — `{ aula_id, nick, momento_do_fato }` em
      `localStorage`, chaveado pela aula —, enfileirando a confirmação do Mestre com a rede fora
      e descartando o item ao sincronizar; verificar que nada além desses três campos é gravado
      (`RF-04-23`, `RN-04-12`, `RN-04-13`, design — decisão 8).
- [ ] 5.3 Implementar a sincronização automática na volta da rede, refazendo por item a sequência
      `POST /v1/sessoes/guerreiro/confirmacao` → `GET /v1/eu` → `POST /v1/aulas/{id}/presencas`
      com o `momento_do_fato` da fila, tratando o registro já existente devolvido pelo núcleo
      como sucesso e descartando o token da sessão aberta no ato (`RF-04-25`, `RN-04-13`, design
      — decisão 7).
- [ ] 5.4 Bloquear, sem rede, o caminho do onboarding e a entrada por reconhecimento, com aviso
      na tela dizendo por quê, e encaminhar à confirmação pelo Mestre ou Admin (`RF-04-24`,
      `RN-04-09`, `RN-04-12`).
- [ ] 5.5 Apresentar ao Mestre ou Admin da sessão de trabalho a lista do que está na fila e do
      que falhou, com nick, hora do fato e nova tentativa, fora de qualquer tela de atendimento
      do Guerreiro(a) (`RF-04-23`, `RF-04-25`, `RN-04-14`).

## 6. App 01 — aviso de coleta e encerramento

- [ ] 6.1 Criar `src/direitos/AreaDetalhadaDeDireitos.tsx` com o conteúdo do PRD-04 §11 em
      linguagem de criança — finalidade, prazo e quem acessa de cada dado, o descarte da
      fotografia, a imagem nunca exibida, a alternativa a quem recusa a biometria e o canal do
      responsável pela App 07 com resposta em 7 dias —, sem chamada ao núcleo, de modo a abrir
      com a rede fora (`RF-04-26`, `RN-04-06`, `RN-04-08`, `RN-04-09`, `RN-04-14`).
- [ ] 6.2 Acrescentar o aviso discreto de coleta à `inicio/TelaInicial.tsx` e à
      `onboarding/TelaDeCaptura.tsx`, com o caminho para a área detalhada (`RF-04-26`).
- [ ] 6.3 Encerrar o `onboarding/FluxoDeOnboarding.tsx` com a despedida que diz como entrar da
      próxima vez — nick e câmera para quem capturou a imagem, nick e confirmação do Mestre para
      quem ficou sem ela, dita como caminho normal — e voltar à tela inicial sem resíduo
      (`RF-04-27`, `RF-04-28`, `RN-04-09`).

## 7. Testes das telas

- [ ] 7.1 `src/trilhas/assistente.test.tsx` — os cenários do assistente: as duas formas de
      perguntar, o microfone que só abre ao toque e fecha ao fim da fala, recusa e encaminhamento
      como resposta, o assistente indisponível sem rede sem enfileirar, e a conversa que não
      sobrevive ao atendimento.
- [ ] 7.2 `src/fila/fila.test.tsx` — os cenários da fila: presença enfileirada com a rede fora,
      nada além de presença na fila, sincronização automática com a hora do fato preservada,
      reenvio que não duplica nem alarma, item descartado ao sincronizar, e a lista de pendências
      visível ao Mestre e invisível ao Guerreiro(a).
- [ ] 7.3 `src/direitos/direitos.test.tsx` e complemento de `src/onboarding/fluxo.test.tsx` — os
      cenários do aviso nas duas telas, da área detalhada (cada dado, canal e prazo, e a ausência
      de pedido atendido ali) e das duas despedidas do onboarding, com a volta à tela inicial.
- [ ] 7.4 Complemento de `src/inicio/inicio.test.tsx` e `src/onboarding/onboarding.test.tsx` — o
      aviso de operação sem conexão em tela e o bloqueio do onboarding e do reconhecimento sem
      rede, com o encaminhamento à confirmação humana.

## 8. Documentação

- [ ] 8.1 Marcar as fatias 10, 11 e 12 do PRD-04 como implementadas em
      `openspec/cronograma-de-fatias.md`, com o slug desta change; registrar no documento 03
      §4.2 o recorte do corpus do assistente e, no documento 09 §1, a decisão do corpus
      (2026-08-30) e as duas pendências novas — a falha de sincronização no painel do dia
      (PRD-04 §5.6.5) e a etiqueta de IA que aguarda a nota de transparência da vitrine; refletir
      no PRD-04 §§8, 9, 13 e 14 a entidade, a rota e as decisões. O documento 99,
      `docs/prds/index.md` e a `nav` do `mkdocs.yml` **não mudam** — nenhuma relação entre
      documentos se altera, o PRD-04 segue "aprovado" e nenhum arquivo nasce em `docs/`.
