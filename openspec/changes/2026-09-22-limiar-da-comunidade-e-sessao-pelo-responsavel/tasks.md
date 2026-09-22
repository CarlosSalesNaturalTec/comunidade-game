## 1. O limiar fora do encontro

- [ ] 1.1 `RN-01-57` — em `backend/src/nucleo/biometria/regra.py`, acrescentar a resolução do
      limiar pela comunidade: o **maior** limiar vigente entre os pontos de apoio **ativos** da
      comunidade do vínculo vigente do Guerreiro(a). Verificar por teste que dois pontos de apoio
      ativos com limiares diferentes fazem valer o maior, e que o inativo fica de fora.
- [ ] 1.2 `RN-01-57`, `RN-01-56` — fazer `autenticar_por_nick_e_descritor` aceitar a aula como
      opcional e escolher entre os dois caminhos pela presença dela (design — decisão 1).
      Verificar que sem vínculo vigente, e sem nenhuma medição na comunidade, a comparação
      recusa.
- [ ] 1.3 `RN-01-22`, `RN-01-57` — igualar o trabalho dos dois caminhos, para que o tempo da
      resposta não revele por qual deles o pedido passou (design — decisão 3). Verificar que a
      recusa do caminho sem aula percorre trabalho equivalente ao da recusa do caminho com aula.
- [ ] 1.4 `RN-01-14` — conferir que a auditoria da comparação continua acontecendo no caminho
      novo, inclusive nas recusas por falta de vínculo e por falta de medição.

## 2. A rota da sessão aceita pedido sem aula

- [ ] 2.1 `RF-01-04`, `RN-01-57` — em `backend/src/nucleo/sessoes/rotas.py`, tornar `aula_id`
      opcional em `AbrirSessaoDeGuerreiroEntrada`, mantendo `extra="forbid"`. Verificar que o
      pedido sem aula abre a sessão pelo limiar da comunidade e que o pedido com aula segue
      idêntico ao de hoje.

## 3. O responsável confirma, com escopo

- [ ] 3.1 `RF-01-74`, `RF-01-16` — em `backend/src/nucleo/permissoes.py`, criar a operação com
      escopo do responsável e acrescentá-la ao papel `responsavel` na matriz, sem tocar na
      operação do Mestre e do Admin (design — decisão 5). Verificar que o teste que percorre a
      tabela do PRD-01 §4 passa a exigi-la.
- [ ] 3.2 `RF-01-74`, `RN-01-58` — fazer a resolução do nick da confirmação receber quem
      confirma e conferir o vínculo de responsável vigente quando o papel for `responsavel`
      (design — decisão 4). Mestre e Admin seguem confirmando qualquer Guerreiro(a). Verificar
      que o responsável abre a sessão de quem é dele e não abre a de mais ninguém.
- [ ] 3.3 `RN-01-58`, `RN-01-22` — fazer a recusa por falta de escopo sair idêntica à recusa por
      nick inexistente, no código, na mensagem e no trabalho feito. Verificar que vínculo
      encerrado recusa como nick inexistente.

## 4. Testes

- [ ] 4.1 `RF-01-04`, `RN-01-57`, `RN-01-56` — em `backend/tests/test_sessao_de_guerreiro.py`,
      cobrir "Pedido sem a aula segue pelo limiar da comunidade", "Sem vínculo vigente, o pedido
      sem aula recusa" e "Comunidade sem nenhum limiar medido", além de conferir que os cenários
      do caminho com aula seguem verdes.
- [ ] 4.2 `RN-01-57` — em `backend/tests/test_biometria.py`, cobrir "Fora do encontro vale o mais
      frouxo da comunidade", "Ponto de apoio inativo não empresta limiar" e "O limiar emprestado
      não atravessa comunidade".
- [ ] 4.3 `RF-01-74`, `RN-01-58` — cobrir "O responsável confirma quem está sob a
      responsabilidade dele", "O responsável não confirma criança alheia", "Vínculo de
      responsável encerrado não confirma mais" e "Apoiador não confirma criança".
- [ ] 4.4 `RN-01-22`, `RN-01-57`, `RN-01-58` — cobrir a indistinguibilidade pelo tempo: entre os
      dois caminhos da comparação e entre a recusa por escopo e a por nick inexistente.
- [ ] 4.5 `RF-01-16` — em `backend/tests/test_permissoes.py`, cobrir "Papel certo, vínculo
      ausente" e "O escopo não depende da aplicação que chamou".

## 5. Documentação

- [ ] 5.1 Marcar a linha desta fatia como implementada em `openspec/cronograma-de-fatias.md`.
      Nada muda em `docs/`: o documento 03, o documento 09, o documento 99 e os PRDs 01 e 05 já
      receberam, no PR de documentação que criou `RF-01-74`, `RN-01-57` e `RN-01-58`, tudo o que
      estas decisões mudaram; nenhum arquivo nasce em `docs/` e a situação do PRD-01 não muda.
