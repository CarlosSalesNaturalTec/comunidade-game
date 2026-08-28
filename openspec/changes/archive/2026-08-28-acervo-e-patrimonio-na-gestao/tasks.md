## 1. App 03 — a porta do acervo

- [x] 1.1 Criar `apps/app-03-gestao/src/acervo/api.ts` com o tombamento
      (`POST /v1/itens-patrimoniais`), a leitura do acervo por comunidade
      (`GET /v1/itens-patrimoniais?comunidade_virtual_id=`) e a anotação na ficha de vida
      (`POST /v1/itens-patrimoniais/{id}/ficha-de-vida`), tipando o item com a ficha de vida que
      o núcleo já devolve inteira (`RF-02-52`, `RF-02-53`, `RF-02-55`; design — Context).
      Verificação: cenários das tarefas 4.1 e 4.2.
- [x] 1.2 Criar `apps/app-03-gestao/src/acervo/TelaDoAcervo.tsx`: seletor de comunidade no padrão
      de `TelaDeTerritorio`, carga do acervo, dos pontos de apoio e dos adultos para resolver
      nomes, releitura depois de cada escrita e recusa de sessão tratada como nas demais áreas
      (`RF-02-52`, `RF-02-53`; design — decisões 3 e 6).
- [x] 1.3 Ligar a área **Acervo** à navegação do `App.tsx`, entre Pontos de Apoio e Agenda
      (`RF-02-52`).

## 2. App 03 — exemplar, ficha de vida e anotação

- [x] 2.1 Criar `ListaDoAcervo.tsx` e `Acervo.css`: lista densa com título, número de tombo,
      ponto de apoio e estado de conservação por nome, o responsável designado resolvido, a
      ausência de responsável como informação, texto próprio para a comunidade sem acervo e
      nenhuma ação de retirada, empréstimo, devolução ou transferência (`RF-02-52`, `RN-02-18`;
      design — decisões 3 e 7).
- [x] 2.2 Criar `FormularioDeTombamento.tsx`, oferecido só ao Admin: título, número de tombo,
      ponto de apoio da comunidade escolhida e estado de conservação em texto, apontando o campo
      em falta no próprio campo e traduzindo a recusa de tombo repetido em linguagem simples, sem
      perder o que foi digitado (`RF-02-52`; design — decisão 5).
- [x] 2.3 Criar `FichaDeVida.tsx`: seção do exemplar, aberta e fechada por item, com as anotações
      da mais antiga à mais recente — teor, estado de conservação, autor e data e hora —, texto
      próprio quando não há anotação e nenhum caminho de editar ou remover (`RF-02-53`; design —
      decisão 2).
- [x] 2.4 Criar `AnotacaoNaFichaDeVida.tsx`, oferecida ao Admin e ao Mestre: teor em escolha
      fechada — cuidado, perda ou dano — e estado de conservação apurado; escolhido perda ou
      dano, a tela diz que nada é debitado ao Guerreiro(a) nem à família e não oferece campo
      algum para identificar culpado (`RF-02-55`, `RN-02-16`).

## 3. App 03 — responsável pelo acervo do ponto de apoio

- [x] 3.1 Em `apps/app-03-gestao/src/pontos-de-apoio/api.ts`, acrescentar a designação
      (`PUT /v1/pontos-de-apoio/{id}/responsavel`) (`RF-02-52`, `RF-07-49`).
- [x] 3.2 Criar `pontos-de-apoio/DesignarResponsavel.tsx`, oferecido só ao Admin, com os Mestres
      e Apoiadores cadastrados no seletor, a troca substituindo o designado anterior e a recusa
      do núcleo em linguagem simples (`RF-02-52`, `RF-07-49`; design — decisão 4).
- [x] 3.3 Em `ListaDePontosDeApoio.tsx`, trocar o rótulo "Responsável designado" pelo **nome** do
      designado, mantendo a ausência como informação, e ligar o caminho da designação
      (`RF-02-52`, `RN-07-34`; design — decisão 3).

## 4. Testes

- [x] 4.1 `apps/app-03-gestao/src/acervo/acervo.test.tsx` — acervo: a lista com os quatro campos e
      o nome do responsável, o exemplar de ponto de apoio sem responsável apresentado assim
      mesmo, a comunidade sem acervo com texto próprio, o tombamento pelo Admin, o campo em falta
      barrado antes do envio, o tombo repetido explicado sem apagar o digitado, o caminho do
      tombamento ausente para o Mestre, a ausência de qualquer ação de retirada, empréstimo,
      devolução ou transferência e a ausência de valor em reais (`RF-02-52`, `RN-02-18`,
      `RN-02-19`).
- [x] 4.2 No mesmo arquivo — ficha de vida: as anotações em ordem do tempo com teor, estado,
      autor e data e hora, o exemplar sem anotação com texto próprio, a ausência de caminho de
      edição e de remoção, a anotação de cuidado pelo Mestre, o aviso de que perda e dano não
      geram débito, a ausência de campo para identificar culpado e o estado de conservação em
      falta barrado antes do envio (`RF-02-53`, `RF-02-55`, `RN-02-16`).
- [x] 4.3 Em `apps/app-03-gestao/src/pontos-de-apoio/pontos-de-apoio.test.tsx` — a designação de
      um Mestre, a troca substituindo o anterior, o nome do designado na lista, a ausência sem
      aviso de erro e o caminho não oferecido a quem não é Admin (`RF-02-52`, `RF-07-49`,
      `RN-07-34`).

## 5. Documentação

- [x] 5.1 Em `openspec/cronograma-de-fatias.md`, marcar a fatia 12 como implementada com o slug
      da change, retirando `RF-02-96` do recorte — já entregue por
      `2026-08-21-desativacao-do-ponto-de-apoio` — e acrescentando `RF-07-49`; abrir linha nova,
      em aberto, para `RF-02-50` e `RF-02-51` (entregas confirmadas), que não estavam em fatia
      alguma. Não há decisão nova: nada muda nos documentos-fonte, no documento 09, no documento
      99 nem no PRD-02, nenhum arquivo nasce em `docs/` e a `nav` do `mkdocs.yml` fica como está;
      `docs/prds/index.md` só muda se a situação do PRD-02 mudar.
