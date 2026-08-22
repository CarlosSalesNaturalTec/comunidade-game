## 1. Solicitação de dados no núcleo

- [ ] 1.1 `GET /solicitacoes-de-dados` em `fila/rotas.py`, no molde da rota de participação da
      fatia anterior: paginada, restrita a Admin, com solicitante, instituição, finalidade
      declarada, recorte pedido, situação, prazo, atraso derivado e o desfecho quando houver
      (`RF-02-77`, `RF-01-46`, `RF-01-16`, `RN-01-49`).
- [ ] 1.2 `POST /solicitacoes-de-dados/{id}/avaliacao`, consumindo `avaliar_solicitacao_de_dados`
      **sem alterá-la**: parecer obrigatório nos dois desfechos e **compromisso de não
      reidentificação** transportado como campo do desfecho, não conferido só na tela
      (design — decisão 2). Aprovação sem o compromisso e parecer vazio recebem 422; guarda de
      reavaliação com 409; quem não é Admin recebe 403 (`RF-02-78`, `RF-02-93`, `RN-01-48`,
      `RN-02-26`).

## 2. Solicitação de chave no núcleo

- [ ] 2.1 `GET /solicitacoes-de-chave` em `fila/rotas.py`: paginada, restrita a Admin, com quem
      pediu, o que pretende construir, situação, prazo, atraso derivado, desfecho quando houver
      e a indicação de que a solicitação **já rendeu chave**. O segredo não sai em campo algum
      (`RF-02-87`, `RF-01-49`, `RN-01-51`, `RN-02-28`).
- [ ] 2.2 `POST /solicitacoes-de-chave/{id}/avaliacao`, consumindo `avaliar_solicitacao_de_chave`
      **sem alterá-la**: aceita ou recusada com parecer, 422 fora do vocabulário, 409 na
      reavaliação, 403 para quem não é Admin. O desfecho **não emite chave**;
      `emitir_chave_de_terceiro` e `POST /chaves` ficam como estão (`RF-02-88`, `RF-01-49`,
      design — decisão 1).

## 3. Sugestões e propostas no núcleo

- [ ] 3.1 `GET /sugestoes` em `fila/rotas.py`: paginada, restrita a Admin, reunindo numa fila só
      o que vem das Apps 05, 07, 08 e 09, com autor, persona dele, teor, situação, prazo,
      atraso derivado e, no desfecho, parecer e motivo do retorno (`RF-02-25`, `RF-01-25`,
      `RN-01-49`).
- [ ] 3.2 `POST /sugestoes/{id}/avaliacao`, consumindo `avaliar_sugestao` **sem alterá-la**:
      adotada ou não adotada, motivo do retorno exigido na não adotada com 422 sem ele, 409 na
      reavaliação, 403 para quem não é Admin. O crédito dos 20 extras, o badge de protagonismo
      e a data de descarte da transcrição vêm da regra, não da rota (`RF-02-26`, `RF-01-56`,
      `RN-01-50`).

## 4. Testes do núcleo

- [ ] 4.1 Em `backend/tests/test_fila_rota.py`, os cenários da solicitação de dados: Admin lê a
      fila com finalidade e recorte; prazo vencido vem em atraso; Mestre recebe 403; aprovação
      com compromisso grava o desfecho; aprovação sem compromisso recebe 422; parecer vazio
      recebe 422; reavaliação recebe 409 (`RF-02-77`, `RF-02-78`, `RF-02-93`, `RN-01-48`).
- [ ] 4.2 Ainda em `test_fila_rota.py`, os cenários da guarda de entrega: nenhum conjunto sai de
      solicitação sem desfecho ou recusada, e a entrega sobre solicitação aprovada fica
      registrada com o que foi entregue e a quem (`RF-02-79`, `RF-01-47`, `RN-02-26`).
- [ ] 4.3 Em `backend/tests/test_chave_de_terceiro_rota.py`, o caminho de ponta a ponta que
      ninguém percorreu junto (design — riscos): solicitação → aprovação pela rota nova →
      emissão devolvendo o segredo uma vez → apresentação da URL. Mais: aprovar **não** emite;
      emissão sobre solicitação recusada ou sem desfecho é recusada; a mesma solicitação não
      rende duas chaves (`RF-02-88`, `RF-02-89`, `RF-01-50`, `RN-01-51`).
- [ ] 4.4 Ainda em `test_fila_rota.py`, os cenários da sugestão: adotada credita 20 extras e o
      badge na mesma operação; regravar adotada **não** credita de novo; não adotada sem motivo
      recebe 422; não adotada com motivo grava a data de descarte 90 dias à frente; reavaliação
      recebe 409 (`RF-02-26`, `RF-01-56`, `RN-01-50`).

## 5. As três naturezas na área Filas

- [ ] 5.1 `apps/app-03-gestao/src/filas/`: as três naturezas entram no filtro e na lista já
      existentes, cada uma com os campos que lhe são próprios, **sem** mudar a forma da lista,
      do filtro ou da apresentação do atraso (`RF-02-25`, `RF-02-77`, `RF-02-87`).
- [ ] 5.2 Avaliação da solicitação de dados: os **três critérios** apresentados antes da
      decisão, o compromisso de não reidentificação exigido no próprio campo antes de aprovar,
      parecer obrigatório nos dois desfechos, e a entrega registrada apresentada como gratuita
      e anonimizada (`RF-02-93`, `RF-02-78`, `RF-02-79`, `RN-02-26`).
- [ ] 5.3 Avaliação da solicitação de chave em **dois atos**: primeiro o desfecho com parecer,
      depois a emissão sobre a solicitação aprovada. A emissão apresenta identificador e
      segredo com o aviso de que o segredo aparece uma única vez; o segredo vive só na memória
      da tela, nunca em `sessionStorage` (design — decisão 5). Solicitação que já rendeu chave
      não oferece emitir de novo (`RF-02-88`, `RF-02-89`, `RN-02-28`).
- [ ] 5.4 Avaliação da sugestão: motivo do retorno exigido na não adotada, apontado no campo
      antes de chamar o núcleo; a adotada mostra que 20 extras e o badge foram creditados; sem
      caminho de envio por e-mail em lugar nenhum (`RF-02-26`, `RN-02-25`).

## 6. Painel das chaves emitidas

- [ ] 6.1 `apps/app-03-gestao/src/chaves/`: área ao lado das Filas (design — decisão 4), sobre
      o `GET /chaves` que já existe, com prazo, URL apresentada, situação e **rótulo textual**
      nas que estão a vencer e nas revogadas por decurso — legível sem distinguir cores. A
      revogação exige motivo antes de chamar o núcleo, e o segredo não aparece em campo algum
      (`RF-02-90`, `RF-02-91`, `RF-02-92`, `RN-02-28`, `RN-02-29`, documento 15 §5).

## 7. Testes da App 03

- [ ] 7.1 Em `apps/app-03-gestao/src/filas/filas.test.tsx`, os cenários das três naturezas: o
      filtro alcança as quatro; cada natureza mostra os seus campos; os três critérios aparecem
      antes da decisão de dados; aprovar dados sem o compromisso é apontado no campo sem chamar
      o núcleo; a não adotada sem motivo é apontada; a adotada mostra o que foi creditado; não
      há caminho de e-mail (`RF-02-25`, `RF-02-77`, `RF-02-93`, `RF-02-26`, `RN-02-25`).
- [ ] 7.2 Ainda em `filas.test.tsx`, os cenários da chave: aprovar não emite e passa a oferecer
      a emissão; o segredo aparece uma vez com o aviso; ao voltar à mesma solicitação o segredo
      não reaparece; solicitação que já rendeu chave não oferece emitir (`RF-02-88`,
      `RF-02-89`, `RN-02-28`).
- [ ] 7.3 `apps/app-03-gestao/src/chaves/chaves.test.tsx`: o painel mostra prazo, URL e
      situação; prazo a vencer e revogação por decurso vêm por rótulo legível sem cor; revogar
      sem motivo é apontado no campo; o segredo não aparece (`RF-02-90`, `RF-02-91`,
      `RF-02-92`, `RN-02-28`).

## 8. Documentação

- [ ] 8.1 `docs/prds/prd-02-frontend-de-gestao.md`, as duas correções decididas em 2026-08-22:
      acrescentar `POST /v1/solicitacoes-de-chave/{id}/avaliacao` à tabela da §9, entre a
      leitura da fila de chave e `POST /v1/chaves`; e renumerar para **`RF-02-98`** a linha da
      §6.5 sobre a amostra semanal de coleta, deixando `RF-02-93` com o critério de aprovação
      da §6.2, que é o que a §15 já rastreia. Conferir que `RF-02-98` não colide — o maior
      identificador em uso é `RF-02-97`.
- [ ] 8.2 Nenhum outro documento muda: as duas correções não criam regra de produto, e por isso
      nenhum documento-fonte e nenhuma linha do documento 09 são tocados. A situação do PRD-02
      em `docs/prds/index.md` recebe o parágrafo desta fatia e da anterior, sem mudar de
      **aprovado** — as filas fecham a §6.2, mas o painel do dia, o Quiz ao Vivo e os
      lançamentos seguem pendentes.
