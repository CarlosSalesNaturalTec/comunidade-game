## 1. Núcleo — catálogo de termos e registro de leitura

- [x] 1.1 `RF-13-32`, `RF-13-33`: criar `src/nucleo/termos/` com `Termo(tipo, versao, texto,
      vigente_desde)` e `LeituraDeTermo(responsavel, versao, lida_em)`, esta única por
      responsável e versão (design — decisões 2 e 3); verificar que o modelo importa e que a
      restrição de unicidade está declarada.
- [x] 1.2 `RF-13-32`, `RF-13-33`, `RF-13-34`: escrever a regra de consulta — vigente por tipo e
      versões anteriores com o período em que valeram — e a de registro de leitura, que devolve
      o registro existente em vez de criar o segundo; verificar pelos testes da tarefa 5.1.
- [x] 1.3 `RF-13-32`, `RN-13-19`: expor `GET /v1/termos` sob `exigir_persona`, de qualquer
      papel, e `POST /v1/termos/{versao}/leitura` sob `Operacao.consentimentos` do responsável,
      recusando 403 outro papel e 404 versão fora do catálogo (design — decisão 6).
- [x] 1.4 `RF-13-34`, `RN-13-19`: semear o texto do termo aprovado pelo fundador na versão que a
      `Configuracao` já carimba, com a cláusula de entrega gratuita, anonimizada, aprovada caso
      a caso pelo Admin e sob CC BY-SA (design — Migration Plan); verificar que `GET /v1/termos`
      devolve o texto semeado.

## 2. Núcleo — transparência e histórico de acessos

- [x] 2.1 `RF-13-30`: acrescentar `acesso_ao_dado_do_guerreiro` (auditoria, Guerreiro(a)), com
      índice por Guerreiro(a) e por momento, mantendo a trilha somente inserção (design —
      decisão 1).
- [x] 2.2 `RF-13-30`: fazer o `MiddlewareDeAuditoria` colher todo `guerreiro_id` dos
      `path_params` e do corpo JSON em cache, inclusive dentro de listas, e gravar uma linha por
      criança alcançada, sem que rota alguma declare nada; verificar pelos testes da tarefa 5.2.
- [x] 2.3 `RF-13-30`, `RN-13-04`: expor `GET /v1/eu/guerreiros/{id}/acessos`, paginada no
      contrato único de listagem, da mais recente para a mais antiga, restrita ao responsável
      vinculado, sem conteúdo do dado e sem linha de outra criança.
- [x] 2.4 `RF-13-29`, `RN-13-20`: criar `src/nucleo/transparencia/` com o catálogo declarado das
      tabelas do PRD-01 §11 e do documento 03 §12.2, cada linha com finalidade, prazo, se está
      guardada daquele Guerreiro(a) e a marca de restrita à gestão para consulta ao assistente e
      transcrição de apoio escolar (design — decisão 4).
- [x] 2.5 `RF-13-29`, `RN-13-04`: expor `GET /v1/eu/guerreiros/{id}/dados`, restrita ao
      responsável vinculado, sem devolver conteúdo de dado algum.

## 3. Núcleo — ato assistido, responsáveis e crédito da proposta

- [x] 3.1 `RF-13-35`, `RN-13-03`: expor `GET /v1/guerreiros/{id}/responsaveis` sob
      `Operacao.vinculo_com_guerreiros_e_guerreiras`, devolvendo só os vínculos vigentes, com
      nome e grau de parentesco, sem credencial nem contato.
- [x] 3.2 `RF-13-35`, `RF-13-36`, `RF-13-38`, `RN-13-16`: expor `POST
      /v1/guerreiros/{id}/autorizacao/assistida` sobre `registrar_consentimento`, com origem
      assistida, responsável presente vinculado (422 sem ele, 403 sem vínculo), testemunha
      obrigatória (422 sem ela), quem operou e a versão carimbada pela configuração (design —
      decisão 5).
- [x] 3.3 `RN-13-18`: em `avaliar_sugestao`, creditar os 20 pontos extras e o badge de
      protagonismo **apenas** quando o autor tem papel de Guerreiro(a), gravando o desfecho das
      demais personas sem crédito (design — decisão 8).
- [x] 3.4 Gerar a migração Alembic das três tabelas novas e da semente do termo, e verificar que
      `alembic upgrade head` e `downgrade` correm limpos.

## 4. App 07 — telas

- [x] 4.1 `RF-13-29`, `RN-13-20`: tela de transparência do vinculado — dado, finalidade, prazo,
      a marca do que não está guardado e a declaração do que é restrito à gestão —, só de
      leitura, com o pedido apontado para a solicitação.
- [x] 4.2 `RF-13-30`, `RF-13-31`: histórico de acessos com data, hora, quem acessou, papel e
      dado, o acesso de rotina apresentado como rotina, e o esclarecimento aberto da própria
      linha, com a referência do acesso.
- [x] 4.3 `RF-13-32`, `RF-13-33`, `RF-13-34`: tela do termo — texto vigente em linguagem
      simples, registro da leitura com data e hora, histórico das versões anteriores e o
      caminho, a partir de cada decisão da autorização, para o texto que valia naquela data.
- [x] 4.4 `RF-13-39`, `RF-13-40`, `RN-13-15`, `RN-13-18`: tela de propostas — registro em texto
      na fila única e acompanhamento com o motivo em linguagem simples, sem prometer e-mail nem
      ponto.
- [x] 4.5 `RF-13-41`: `AvisoDeColeta` e `ContextoDeDireitos` da App 07, no padrão das Apps 03,
      05 e 09, com a área detalhada apontando para a tela de transparência, aplicados às telas
      de troca de senha, autorização, recusa da imagem, solicitação, proposta e ato assistido.
- [x] 4.6 `RF-13-35`, `RF-13-36`, `RF-13-38`: modo assistido — `App.tsx` passa a admitir sessão
      de Admin e de Mestre só nele; a tela escolhe o Guerreiro(a) e o responsável presente,
      percorre o termo, exige a testemunha e declara que o ato é gravado em nome do responsável
      (design — decisão 7).
- [x] 4.7 `RF-13-42`, `RN-13-17`: conferir, tela a tela, que nada na App 07 abre canal, campo de
      mensagem ou dado de contato de Apoiador, de terceiro ou de outro parente.

## 5. Testes

- [x] 5.1 `tests/test_termos_rota.py` — os cenários de `catalogo-de-termos`: vigente com texto,
      401 sem persona, histórico com o período de cada versão, leitura registrada, releitura sem
      segundo registro, leitura que não concede autorização, 403 de outro papel e 404 de versão
      inexistente.
- [x] 5.2 `tests/test_auditoria_recorte.py` — os cenários de `auditoria`: escrita sobre uma
      criança e sobre várias ligadas a todas, escrita sem criança fora de todo histórico, o
      acesso de rotina do Mestre com data, hora e dado, nenhuma linha de outra criança, ausência
      de conteúdo, 403 sem vínculo e 403 do responsável na trilha inteira.
- [x] 5.3 `tests/test_transparencia_rota.py` — os cenários de `transparencia-de-dados`: catálogo
      com finalidade e prazo, linha não guardada que permanece na lista, ausência de conteúdo,
      consulta ao assistente marcada como restrita à gestão e 403 de não vinculado e de outro
      papel.
- [x] 5.4 `tests/test_autorizacao_assistida.py` — os cenários de `consentimento` e de
      `responsavel-e-vinculo`: ato assistido do Mestre com testemunha, mesmo estado que o ato do
      próprio, 422 sem responsável presente, 422 sem testemunha, 403 sem vínculo, recusa
      assistida que suspende, 403 de outro papel, e a lista de responsáveis sem vínculo
      encerrado, sem credencial e sem contato.
- [x] 5.5 `tests/test_fila_rota.py` — acrescentar os cenários do crédito: proposta de
      responsável adotada não pontua, proposta de Mestre ou de Apoiador adotada não pontua, e a
      sugestão de Guerreiro(a) continua creditando 20 extras e o badge uma vez só.
- [x] 5.6 `apps/app-07-responsaveis/src/transparencia/transparencia.test.tsx` — os cenários de
      tela da transparência, do histórico de acessos e do esclarecimento aberto da linha.
- [x] 5.7 `apps/app-07-responsaveis/src/termos/termos.test.tsx` — texto vigente, leitura
      registrada, histórico das versões, a declaração da entrega de dados e a ausência de
      decisão separada sobre ela.
- [x] 5.8 `apps/app-07-responsaveis/src/propostas/propostas.test.tsx` e
      `src/direitos/direitos.test.tsx` — proposta registrada e acompanhada sem promessa de
      e-mail nem de ponto; aviso em cada tela que grava dado, nomeando o dado daquela tela,
      levando à transparência e sem bloquear o envio.
- [x] 5.9 `apps/app-07-responsaveis/src/assistido/assistido.test.tsx` — sessão de Mestre que só
      alcança o modo assistido, ato gravado em nome do responsável presente com testemunha,
      Guerreiro(a) e Apoiador ainda recusados, e a ausência de qualquer canal com terceiros.

## 6. Documentação

- [x] 6.1 Registrar as decisões do fundador de 2026-09-01 e fechar a fatia: no **documento 03**,
      §12.3 ganha a frase de que o termo declara a entrega ao responsável e §9 passa a dizer que
      o papel do termo impresso da autorização única fica no arquivo físico, com o ato entrando
      como atendimento assistido; no **documento 09** §1, as três linhas novas — redação da
      cláusula de entrega, o papel no arquivo físico e o modo assistido na App 07 com a leitura
      dos responsáveis — e a linha "Redação dos termos" reduzida aos dois textos que faltam; no
      **PRD-13**, a jornada 5.8, o `RF-13-37`, a linha do anexo e a nova rota na §9, o critério
      de aceite do termo digitalizado na §12, a §13 e a §14 sem a trava do `RF-13-34`; em
      **`docs/prds/index.md`**, a situação do PRD-13; e no
      **`openspec/cronograma-de-fatias.md`**, as fatias 5 e 6 como `implementado`, com o slug
      desta change. Nenhum arquivo novo em `docs/`, logo nada muda na `nav` do `mkdocs.yml`.
