# Tasks

## 1. Núcleo — identidade na sessão e ranking pelo vínculo

- [ ] 1.1 `RF-01-76`: `EuSaida` e `GET /v1/eu` em `backend/src/nucleo/sessoes/rotas.py` passam
      a devolver `nick` e `avatar` do Guerreiro(a) em sessão, ausentes para os demais papéis
      no mesmo padrão de `divulgacao_autorizada`. Verificar pela resposta da rota em sessão de
      Guerreiro(a) e em sessão de Mestre.
- [ ] 1.2 `RF-05-52`, `RF-05-53`, `RF-05-84`, `RN-05-16`: `GET /v1/eu/ranking` em
      `backend/src/nucleo/pontuacao/rotas.py`, derivando a comunidade do `VinculoJogador`
      vigente, com os mesmos filtros (trilha **ou** poder) e a mesma paginação; sem vínculo
      vigente, recusa. Verificar pela resposta em Guerreiro(a) com e sem vínculo.
- [ ] 1.3 `RF-05-52`: remover `GET /v1/rankings/{comunidade}` depois que 3.1 e 3.2 passarem à
      rota nova. Verificar que nenhuma chamada a ela resta em `apps/`, `comum/` e `backend/`.

## 2. Testes do núcleo

- [ ] 2.1 `RF-01-76`: testes de `GET /v1/eu` cobrindo os cenários de `persona-e-credencial` —
      Guerreiro(a) recebe nick e avatar, Guerreiro(a) sem avatar composto, adulto não recebe
      os campos, e nada de imagem real, nome civil ou contato na resposta.
- [ ] 2.2 `RF-05-52`, `RF-05-53`, `RF-05-84`, `RN-05-16`, `RN-05-21`: testes de
      `GET /v1/eu/ranking` cobrindo os cenários de `pontos-niveis-e-badges` — comunidade vinda
      do vínculo, ranking de quem nunca abriu série de coleta, própria posição sem ponto
      creditado, recusa sem vínculo vigente, recusa de papel que não é Guerreiro(a), filtros
      por trilha e por poder, e o ranking público inalterado.

## 3. Camada comum e Apps 05 e 01

- [ ] 3.1 `RF-05-50`, `RF-05-51`, `RF-01-76`: `comum/carta/api.ts` e
      `comum/carta/CartaDoGuerreiro.tsx` montam a carta de `GET /v1/eu` e `GET /v1/eu/ranking`
      e deixam de ler `GET /v1/series-de-coleta/minhas`. Verificar que a carta monta para
      Guerreiro(a) sem série de coleta e sem ponto creditado.
- [ ] 3.2 `RF-05-52`, `RF-05-84`: `apps/app-05-guerreiro/src/api/carteira.ts` e
      `carteira/RankingDaTurma.tsx` passam à rota nova, sem descobrir a comunidade antes, e
      sai o texto que manda abrir série de coleta. Verificar pela tela de quem não tem coleta.
- [ ] 3.3 `RF-04-67`: em
      `apps/app-01-aula-presencial/src/entrada/TelaDeEntradaDoGuerreiro.tsx`, a confirmação da
      presença passa a ser dita uma vez só no desfecho, e o aviso de carta incompleta deixa o
      tom de coisa em curso. Verificar pelo texto da tela do desfecho.

## 4. App 03 — nome do responsável

- [ ] 4.1 `RF-02-06`: `apps/app-03-gestao/src/personas/api.ts` envia `{ nome }` em
      `POST /v1/responsaveis`, e `personas/FormularioDeResponsavel.tsx` ganha o campo de nome,
      barrando o envio em branco. Verificar pelo cadastro concluído sem 422.

## 5. Testes das aplicações

- [ ] 5.1 `RF-05-50`, `RF-05-51`, `RF-05-52`, `RF-05-84`: testes de `comum/carta` e da carteira
      da App 05 cobrindo os cenários de `area-do-guerreiro` — carta e ranking com série de
      coleta ausente, carta completa com desempenho zerado, e nenhuma chamada às séries.
- [ ] 5.2 `RF-04-67`: teste do desfecho da presença da App 01 cobrindo os cenários de
      `aplicacao-da-aula-presencial` — carta apresentada a quem não tem coleta, confirmação
      dita uma vez, e o aviso de falta sem anúncio de espera.
- [ ] 5.3 `RF-02-06`: teste do formulário de responsável da App 03 cobrindo os cenários de
      `aplicacao-de-gestao` — cadastro com o nome declarado e envio barrado sem nome —
      **afirmando o corpo enviado ao núcleo**, sem dublar `cadastrarResponsavel`.

## 6. Documentação

- [ ] 6.1 Mover a linha "`GET /v1/eu` não devolve nick nem avatar do Guerreiro(a)" de
      "Decisões pendentes" para "Já decididos" em `docs/09-topicos-em-aberto-e-sugestoes.md`,
      redigida como a decisão do fundador de 2026-09-26.
- [ ] 6.2 PRD-01: `RF-01-76` na tabela de requisitos, a linha de `GET /v1/eu` na §9, a decisão
      na §13 e a rastreabilidade na §15. PRD-05: a §9 troca `GET /v1/rankings/{comunidade}`
      por `GET /v1/eu/ranking`.
- [ ] 6.3 Marcar as duas fatias como `implementado` em `openspec/cronograma-de-fatias.md`, com
      o slug desta change. `docs/prds/index.md`, documento 99 e a `nav` do `mkdocs.yml` não
      mudam: nenhum PRD trocou de situação, nenhuma relação entre documentos mudou e nenhum
      arquivo nasceu em `docs/`.
