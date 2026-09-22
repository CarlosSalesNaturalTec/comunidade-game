## 1. O limiar fora do encontro

- [x] 1.1 `RN-01-57` — em `backend/src/nucleo/biometria/regra.py`, acrescentar a resolução do
      limiar pela comunidade: o **maior** limiar vigente entre os pontos de apoio **ativos** da
      comunidade do vínculo vigente do Guerreiro(a). Verificar por teste que dois pontos de apoio
      ativos com limiares diferentes fazem valer o maior, e que o inativo fica de fora.
- [x] 1.2 `RN-01-57`, `RN-01-56` — fazer `autenticar_por_nick_e_descritor` aceitar a aula como
      opcional e escolher entre os dois caminhos pela presença dela (design — decisão 1).
      Verificar que sem vínculo vigente, e sem nenhuma medição na comunidade, a comparação
      recusa.
- [x] 1.3 `RN-01-22`, `RN-01-57` — fazer a **resolução do limiar** fora do encontro custar o
      mesmo em todo desfecho e não variar com o tamanho da comunidade (design — decisão 3, revista
      na implementação). O plano original dizia igualar os **dois caminhos** entre si; medindo,
      isso não é alcançável nem protege nada — quem chama já sabe se mandou aula, e o que pode
      vazar é a causa **dentro** de um caminho. Verificado por contagem de consultas: `[2, 2, 2, 2]`.
- [x] 1.4 `RN-01-14` — conferir que a auditoria da comparação continua acontecendo no caminho
      novo, inclusive nas recusas por falta de vínculo e por falta de medição.

## 2. A rota da sessão aceita pedido sem aula

- [x] 2.1 `RF-01-04`, `RN-01-57` — em `backend/src/nucleo/sessoes/rotas.py`, tornar `aula_id`
      opcional em `AbrirSessaoDeGuerreiroEntrada`, mantendo `extra="forbid"`. Verificar que o
      pedido sem aula abre a sessão pelo limiar da comunidade e que o pedido com aula segue
      idêntico ao de hoje.

## 3. O responsável confirma, com escopo

- [x] 3.1 `RF-01-74`, `RF-01-16` — em `backend/src/nucleo/permissoes.py`, criar a operação com
      escopo do responsável e acrescentá-la ao papel `responsavel` na matriz, sem tocar na
      operação do Mestre e do Admin (design — decisão 5). Verificar que o teste que percorre a
      tabela do PRD-01 §4 passa a exigi-la.
- [x] 3.2 `RF-01-74`, `RN-01-58` — fazer a resolução do nick da confirmação receber quem
      confirma e conferir o vínculo de responsável vigente quando o papel for `responsavel`
      (design — decisão 4). Mestre e Admin seguem confirmando qualquer Guerreiro(a). Verificar
      que o responsável abre a sessão de quem é dele e não abre a de mais ninguém.
- [x] 3.3 `RN-01-58`, `RN-01-22` — fazer a recusa por falta de escopo sair idêntica à recusa por
      nick inexistente, no código, na mensagem e no trabalho feito. Verificar que vínculo
      encerrado recusa como nick inexistente.

## 4. Testes

- [x] 4.1 `RF-01-04`, `RN-01-57`, `RN-01-56` — em `backend/tests/test_sessao_de_guerreiro.py`,
      cobrir "Pedido sem a aula segue pelo limiar da comunidade", "Sem vínculo vigente, o pedido
      sem aula recusa" e "Comunidade sem nenhum limiar medido", além de conferir que os cenários
      do caminho com aula seguem verdes.
- [x] 4.2 `RN-01-57` — em `backend/tests/test_biometria.py`, cobrir "Fora do encontro vale o mais
      frouxo da comunidade", "Ponto de apoio inativo não empresta limiar" e "O limiar emprestado
      não atravessa comunidade".
- [x] 4.3 `RF-01-74`, `RN-01-58` — cobrir "O responsável confirma quem está sob a
      responsabilidade dele", "O responsável não confirma criança alheia", "Vínculo de
      responsável encerrado não confirma mais" e "Apoiador não confirma criança".
- [x] 4.4 `RN-01-22`, `RN-01-57`, `RN-01-58` — cobrir a indistinguibilidade pelo custo, por
      contagem de consultas: a resolução do limiar em todo desfecho, o caminho sem aula entre
      nicks que existem, e a recusa por escopo contra a por nick inexistente. A comparação
      **entre** os dois caminhos saiu do recorte, pelo motivo da tarefa 1.3.
- [x] 4.5 `RF-01-16` — cobrir "Papel certo, vínculo ausente" e "O escopo não depende da
      aplicação que chamou". Os dois ficaram em `test_sessao_de_guerreiro.py`, e não em
      `test_permissoes.py`: exercitam a rota com escopo, e não a tabela da matriz —
      `test_permissoes.py` recebeu só a linha nova da tabela do PRD-01 §4.

## 5. Documentação

- [x] 5.1 Marcar a linha desta fatia como implementada em `openspec/cronograma-de-fatias.md`.
      Nada muda em `docs/`: o documento 03, o documento 09, o documento 99 e os PRDs 01 e 05 já
      receberam, no PR de documentação que criou `RF-01-74`, `RN-01-57` e `RN-01-58`, tudo o que
      estas decisões mudaram; nenhum arquivo nasce em `docs/` e a situação do PRD-01 não muda.
