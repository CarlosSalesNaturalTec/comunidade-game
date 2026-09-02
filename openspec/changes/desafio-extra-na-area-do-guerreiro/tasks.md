## 1. A elegibilidade no núcleo

- [ ] 1.1 Em `backend/src/nucleo/desafios_extras/regra.py`, criar
      `desafios_extras_elegiveis_do_guerreiro(sessao, *, guerreiro_id, hoje)`: publicados, com
      `encerrado_em` nulo, vigência correndo em `hoje`, trilha entre as inscrições do
      Guerreiro(a) (`trilhas.regra.consultar_inscricoes_do_guerreiro`) e modalidade aberta ou
      nick do destinatário casando por `lower()` com o `Nick` dele. Sem inscrição, ou sem nada
      elegível, lista vazia (`RF-05-20`, design — decisões 2 e 3).
- [ ] 1.2 Ordenar o retorno pelo fim da vigência mais próximo e, no empate, pelo registro mais
      recente — o que está para acabar aparece primeiro (`RF-05-21`).

## 2. A rota do Guerreiro(a)

- [ ] 2.1 Em `backend/src/nucleo/trilhas/rotas.py`, criar `DesafioExtraDoGuerreiroSaida` com
      recompensa (nome do tipo de recurso e nome do ponto de apoio), quantidade disponível,
      quantidade restante, vigência, critério de atribuição, pontos extras, formato,
      modalidade, e trilha e missão pelo nome. NÃO expor nick do destinatário, justificativa,
      parecer, motivo de recusa, custeio, aporte nem lastro (`RF-05-21`, `RN-05-21`,
      `RN-14-20`, design — decisão 5).
- [ ] 2.2 Trocar o retorno de `GET /v1/eu/desafios` por um objeto `MeusDesafiosSaida` com
      `semanais` (o que a rota já devolvia) e `extras` (o da tarefa 1.1, para a data de hoje).
      Guerreiro(a) sem nada em aberto recebe 200 com os dois conjuntos vazios; persona de outro
      papel segue recebendo 403 (`RF-05-19`, `RF-05-20`, `RN-05-21`). **BREAKING**.

## 3. A tela da App 05

- [ ] 3.1 Em `apps/app-05-guerreiro/src/api/desafiosEEquipes.ts`, tipar
      `DesafioExtraDoGuerreiro` e `MeusDesafios` (os dois conjuntos), e ajustar
      `listarMeusDesafios` ao formato novo da resposta (`RF-05-20`, `RF-05-21`).
- [ ] 3.2 Criar `apps/app-05-guerreiro/src/desafios/MeusDesafiosExtras.tsx`: cada desafio com a
      recompensa, a quantidade disponível, a vigência, o critério, o formato e a trilha/missão,
      em linguagem da criança; o direcionado apresentado como dirigido a ela, sem nomear
      terceiro; o de quantidade restante zero marcado como esgotado, sem sumir; a frase de que
      o ponto extra não conta para o nível; e a mensagem própria quando não há nenhum
      (`RF-05-20`, `RF-05-21`, `RN-05-18`, design — decisão 4).
- [ ] 3.3 Em `MeusDesafios.tsx`, montar os dois blocos apartados a partir da mesma chamada —
      semanais no de cima, extras no de baixo, cada um com o seu rótulo. Nenhuma ação de
      concluir, disputar, comprar ou trocar (`RF-05-19`, `RF-05-20`, `RN-05-06`, design —
      decisão 6).
- [ ] 3.4 Acrescentar ao `index.css` da App 05 o que o bloco novo precisa, no padrão das
      classes `cg-` já usadas em `cg-lista-de-desafios` e `cg-cartao-de-desafio`.

## 4. Testes

- [ ] 4.1 Em `backend/tests/test_desafio_extra_regra.py`, cobrir a elegibilidade: o aberto
      alcança todos os inscritos; o direcionado alcança só o dono do nick; o nick casa com
      grafia de maiúsculas diferente; o direcionado a quem não está na trilha não aparece; não
      aparecem o não publicado, o recusado, o encerrado nem o fora da vigência; o esgotado
      continua aparecendo com restante zero; sem inscrição, lista vazia (`RF-05-20`,
      `RF-05-21`).
- [ ] 4.2 Em `backend/tests/test_meus_desafios.py`, cobrir a rota no formato novo: os dois
      conjuntos vêm apartados; sem nada em aberto, 200 com os dois vazios; persona de outro
      papel, 403; e a saída do extra não traz nick do destinatário, justificativa, parecer,
      motivo de recusa, custeio nem lastro (`RF-05-19`, `RF-05-20`, `RF-05-21`, `RN-05-21`,
      `RN-14-20`).
- [ ] 4.3 Criar `apps/app-05-guerreiro/src/desafios/MeusDesafiosExtras.test.tsx`: o cartão
      mostra recompensa, quantidade, vigência e critério; o esgotado aparece marcado; a tela
      diz que o ponto extra não sobe nível; sem extras, a mensagem explica; e nenhuma ação de
      concluir ou trocar é oferecida (`RF-05-20`, `RF-05-21`, `RN-05-18`).
- [ ] 4.4 Ajustar `apps/app-05-guerreiro/src/desafios/MeusDesafios.test.tsx` ao formato novo da
      resposta e cobrir que semanais e extras aparecem em blocos distintos (`RF-05-19`,
      `RF-05-20`).

## 5. Documentação

- [ ] 5.1 Marcar a fatia 8 do PRD-05 como `implementado` em
      `openspec/cronograma-de-fatias.md`, trocando o recorte previsto pelo slug da change e
      retirando a trava, que caiu. Registrar em `docs/09-topicos-em-aberto-e-sugestoes.md` §1
      as duas decisões do fundador de 2026-09-02 — a inscrição exigida também no direcionado e
      o esgotado que permanece visível — e atualizar a situação do PRD-05 na tabela de
      `docs/prds/index.md`. Nenhum arquivo novo em `docs/`, logo nada muda na `nav` do
      `mkdocs.yml`; o documento 99 não muda, porque nenhuma relação entre documentos mudou.
