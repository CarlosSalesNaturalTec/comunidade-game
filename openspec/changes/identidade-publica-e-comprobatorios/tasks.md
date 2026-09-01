## 1. Núcleo — o piso de moedas e o avatar

- [ ] 1.1 Em `backend/src/nucleo/poder_sustentador/regra.py`, escrever `moedas_acumuladas_de` —
      a soma de `Aporte.valor_em_moedas` do provedor, sem lançamento de ajuste, para o direito
      que não regride —, com docstring dizendo por que ela não é `poder_sustentador_de`
      (`RF-14-14`, `RN-14-11`)
- [ ] 1.2 Em `backend/src/nucleo/erros.py`, declarar `PisoDeMoedasNaoAlcancado` (409) levando
      quantas moedas faltam, no molde dos demais 409 (`RF-14-14`, `RF-14-16`, PRD-14 §9)
- [ ] 1.3 Em `backend/src/nucleo/personas/rotas.py`, aceitar `avatar` opcional no
      `PUT /v1/eu/apoiador/identidade` ao lado do nick, recusando com `PisoDeMoedasNaoAlcancado`
      quem estiver abaixo das 10 moedas acumuladas e gravando sem validar a forma do valor; o
      nick continua sob a regra que já existe (`RF-14-12`, `RF-14-14`, `RF-14-17`, `RN-14-10`,
      `RN-14-11`)
- [ ] 1.4 No mesmo arquivo, criar `GET /v1/eu/apoiador/identidade` com nick, avatar, moedas
      acumuladas, se o avatar próprio está liberado e quantas moedas faltam; restrita ao
      Apoiador em sessão, 403 para outro papel, e nada em reais (`RF-14-15`, `RF-14-16`,
      `RN-14-09`)

## 2. Núcleo — o documento comprobatório do Apoiador

- [ ] 2.1 Em `backend/src/nucleo/personas/modelo.py`, acrescentar `anexado_por_id` e `anexado_em`
      a `ArtefatoComprobatorio`, nulos, com o comentário do que é pendente pela decisão 5 do
      design (`RF-14-19`, `RN-14-12`)
- [ ] 2.2 Escrever a migração Alembic que acrescenta as duas colunas sem reescrever linha alguma,
      com `downgrade` que as remove; verificar com `alembic upgrade head` seguido de
      `alembic downgrade -1` (`RF-14-19`)
- [ ] 2.3 Em `backend/src/nucleo/personas/regra.py`, escrever a declaração do documento pelo
      Apoiador — endereço e rótulo obrigatórios, 422 sem eles —, o predicado de publicação
      (pendente só o que o próprio Apoiador declarou e ninguém anexou) e a anexação por Admin,
      que grava quem anexou e quando e é idempotente sobre documento já anexado (`RF-14-18`,
      `RF-14-19`, `RF-14-20`, `RN-14-12`, `RF-02-101`)
- [ ] 2.4 Em `backend/src/nucleo/personas/rotas.py`, expor `POST /v1/eu/apoiador/documentos` e
      `GET /v1/eu/apoiador/documentos` — restritas ao Apoiador em sessão, cada documento com a
      marca de publicado ou pendente — e
      `POST /v1/apoiadores/{id}/artefatos/{artefato_id}/anexacao`, restrita a Admin, com 404 para
      documento que não seja daquele Apoiador (`RF-14-18` a `RF-14-20`, `RN-14-12`, `RF-02-101`)

## 3. Testes do núcleo

- [ ] 3.1 Em `backend/tests/test_poder_sustentador.py`, cobrir `moedas_acumuladas_de`: soma dos
      aportes homologados, aporte pendente fora da conta e ressarcimento pago que derruba o Poder
      Sustentador **sem** mexer no acumulado (`RF-14-14`, `RN-14-11`)
- [ ] 3.2 Em `backend/tests/test_persona_rota.py`, cobrir a identidade do Apoiador: avatar
      gravado com 10 moedas, recusado com 409 e quanto falta com 5 moedas — critério de aceite do
      PRD-14 §12 —, envio aberto sem ato da gestão ao cruzar o piso, avatar mantido depois do
      ressarcimento, troca de avatar e nick a qualquer tempo, 403 para outro papel e a leitura
      com o que falta, sem reais (`RF-14-12` a `RF-14-17`, `RN-14-09` a `RN-14-11`)
- [ ] 3.3 Criar `backend/tests/test_documentos_do_apoiador_rota.py`: documento declarado nasce
      pendente, sem endereço ou rótulo volta 422, outro papel volta 403, a anexação por Admin o
      publica com autoria e data, quem não é Admin volta 403 e o documento segue pendente,
      documento de outro Apoiador volta 404, anexação repetida não troca a autoria, e a leitura
      separa publicado de pendente sem alcançar documento alheio (`RF-14-18` a `RF-14-20`,
      `RN-14-12`, `RF-02-101`)
- [ ] 3.4 Em `backend/tests/test_artefatos_do_mestre_rota.py`, confirmar que o artefato do Mestre
      e o declarado por Admin no cadastro seguem públicos com as colunas novas vazias
      (`RF-09-66`, `RN-14-12`)

## 4. App 08 — identidade pública e comprobatórios

- [ ] 4.1 Criar `apps/app-08-apoiador/src/identidade/api.ts` com a leitura e a gravação de
      `/v1/eu/apoiador/identidade` e a conferência de nick por `/v1/nicks/disponibilidade`, por
      `chamarNucleo` (`RF-14-12`, `RF-14-13`, `RF-14-16`)
- [ ] 4.2 Implementar `src/identidade/TelaDeIdentidadePublica.tsx`: define ou troca nick e avatar
      a qualquer tempo, não pede de novo o nick que veio do pré-cadastro, apresenta as sugestões
      na recusa de nick sem dizer de quem ele é, e mostra a prévia do card na moldura comum com
      nick e total em moedas (`RF-14-12`, `RF-14-13`, `RF-14-17`, `RN-14-09`, `RN-14-10`)
- [ ] 4.3 Na mesma tela, apresentar abaixo do piso o **avatar padrão do projeto** — marca neutra
      enquanto a marca gráfica for pendência do documento 09 — com quantas moedas faltam, sem
      cobrar nem insistir, e abrir o envio do avatar próprio ao cruzar as 10 moedas; a recusa 409
      do núcleo aparece com quanto falta (`RF-14-14`, `RF-14-15`, `RF-14-16`, `RN-14-11`)
- [ ] 4.4 Criar `src/documentos/api.ts` e `src/documentos/TelaDeComprobatorios.tsx`: envio por
      endereço e rótulo, sem campo de anexo de arquivo, com a declaração — antes do envio — de
      que o documento só vai à página pública quando um Admin o anexar, e a lista separando o
      publicado do pendente (`RF-14-18`, `RF-14-19`, `RF-14-20`, `RN-14-12`)
- [ ] 4.5 Em `src/App.tsx`, acrescentar as duas áreas à navegação que já existe, sem roteador
      (`RF-14-12`, `RF-14-18`)

## 5. Testes da App 08

- [ ] 5.1 Criar `apps/app-08-apoiador/src/identidade/identidade.test.tsx`: nick do pré-cadastro
      já preenchido, nick em uso recusado com sugestões e sem revelar de quem é, card com avatar
      padrão e as moedas que faltam para quem tem 5, envio aberto para quem tem 10, recusa 409
      apresentada com quanto falta, troca de avatar e nick, e nenhuma saída em reais — critérios
      de aceite do PRD-14 §12 (`RF-14-12` a `RF-14-17`, `RN-14-09`, `RN-14-11`)
- [ ] 5.2 Criar `src/documentos/comprobatorios.test.tsx`: a tela pede endereço e rótulo e não
      oferece anexo de arquivo, a declaração de que só o Admin publica aparece antes do envio, o
      enviado aparece como pendente e a lista separa o que já está publicado (`RF-14-18` a
      `RF-14-20`, `RN-14-12`)

## 6. Documentação

- [ ] 6.1 Gravar a decisão nova nos documentos-fonte: o **ato do Admin que anexa ao cadastro o
      documento enviado pelo Apoiador** em `docs/02-conceito-do-jogo-e-gamificacao.md` §1, junto
      da regra do artefato comprobatório, e a linha correspondente em "Já decididos" de
      `docs/09-topicos-em-aberto-e-sugestoes.md` §1 — decisão do fundador de 2026-09-01
      (`RF-14-19`, `RN-14-12`)
- [ ] 6.2 Acrescentar o `RF-02-101` a `docs/prds/prd-02-frontend-de-gestao.md` §6.2, a rota de
      anexação à tabela da §9 e a linha de rastreabilidade na §15 (`RF-02-101`)
- [ ] 6.3 Acrescentar à tabela de rotas de `docs/prds/prd-14-area-do-apoiador.md` §9 e de
      `docs/prds/prd-01-backend-api.md` §9 o `GET /v1/eu/apoiador/identidade`, o
      `GET /v1/eu/apoiador/documentos` e a rota de anexação (`RF-14-16`, `RF-14-19`, `RF-14-20`)
- [ ] 6.4 Marcar a fatia 3 do PRD-14 como `implementado` em
      `openspec/cronograma-de-fatias.md`, trocando o recorte previsto pelo slug da change e
      anotando na fatia 16 do PRD-02 que a fila e a tela da anexação são dela. Nada mais muda em
      `docs/`: o documento 99 §8 já registra a dependência do PRD-14 com o PRD-02,
      `docs/prds/index.md` só muda quando o PRD inteiro estiver implementado e nenhum arquivo
      novo entra em `docs/` nem na `nav`
