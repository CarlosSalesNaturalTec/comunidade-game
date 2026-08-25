## 1. Porta de armazenamento — sessão retomável

- [ ] 1.1 Em `backend/src/nucleo/armazenamento/porta.py`, acrescentar `abrir_sessao` e
      `consultar_envio` a `PortaDeArmazenamento`, sem tocar em `gravar`, `ler` e `remover`
      (`RF-09-19`, design — decisão 2). Verificar: a suíte atual do comprovante do aporte, do
      ressarcimento, da fila e da coleta passa sem alteração.
- [ ] 1.2 Em `backend/src/nucleo/armazenamento/nuvem.py`, implementar as duas operações pela
      sessão retomável do Cloud Storage, mantendo o cliente importado só na criação
      (`RF-09-19`, design — decisão 2). Verificar: o módulo importa sem `google-cloud-storage`
      instalado, como hoje.
- [ ] 1.3 Em `backend/src/nucleo/armazenamento/disco.py`, implementar as duas operações pelo
      mesmo protocolo de `Content-Range`, costurando as partes num arquivo temporário
      (`RF-09-19`, design — decisão 2). Verificar: enviar em duas partes, com corte no meio,
      produz arquivo idêntico ao envio inteiro.
- [ ] 1.4 Acrescentar a configuração do diretório das sessões locais em
      `backend/src/nucleo/configuracao.py`, ao lado de `armazenamento_diretorio_local`
      (design — Migration Plan). Verificar: fora de produção a fábrica devolve o adaptador de
      disco já com o diretório de sessões.

## 2. Entidades e migração

- [ ] 2.1 Criar `backend/src/nucleo/conteudos/modelo.py` com `Conteudo` — missão, ordem, tipo,
      corpo, endereço, referência, tamanho, autoria e fonte, com os anuláveis do design
      (`RF-09-14`, `RF-09-15`, `RF-09-24`, PRD-09 §8, design — decisão 4). Verificar: o modelo
      importa e a tabela nasce na migração.
- [ ] 2.2 Criar `backend/src/nucleo/bibliografias/modelo.py` com `BibliografiaDaMissao` —
      missão, título, capítulo e `item_patrimonial_id` **anulável** (`RF-09-21`, decisão do
      fundador 2026-08-25). Verificar: gravar entrada sem exemplar não viola restrição alguma.
- [ ] 2.3 Gerar a migração com as duas tabelas, sem alterar coluna existente
      (design — Migration Plan). Verificar: `alembic upgrade head` e `downgrade` correm limpos
      no banco de teste.

## 3. Regra do conteúdo

- [ ] 3.1 Em `backend/src/nucleo/conteudos/regra.py`, criar `criar_conteudo` conferindo
      **autoria estrita** do Mestre autor da trilha da missão, recusando outro Mestre e o Admin
      (`RF-09-14`, `RF-09-15`, `RN-09-16`). Verificar: outro Mestre e Admin recebem
      `PermissaoNegada`.
- [ ] 3.2 Na mesma função, exigir de cada tipo o que lhe cabe — corpo no texto, endereço no
      link externo, e nenhum byte nos três de arquivo, que nascem sem referência (`RF-09-14`,
      `RF-09-15`, design — decisão 4). Verificar: texto sem corpo e link sem endereço são
      recusados; conteúdo de vídeo nasce sem referência.
- [ ] 3.3 Na mesma função, exigir **fonte** quando a autoria é de terceiro, e nunca exigir
      anexo (`RF-09-24`, documento 03 §11). Verificar: terceiro sem fonte é recusado; terceiro
      com fonte em texto é aceito; conteúdo próprio sem fonte é aceito.
- [ ] 3.4 Criar `abrir_envio` conferindo autoria, **formato** contra a lista fechada e
      **tamanho declarado** contra o teto do tipo, antes de abrir a sessão (`RF-09-16`,
      `RF-09-17`, `RF-09-115`, `RN-09-06`). Verificar: formato fora da lista e tamanho acima do
      teto não abrem sessão.
- [ ] 3.5 Criar `confirmar_envio`, que consulta o armazenamento pelo tamanho e tipo **reais** e
      só então grava a referência no conteúdo (`RF-09-16`, `RF-09-17`, design — decisão 1).
      Verificar: envio que conclui acima do teto é recusado e o conteúdo permanece sem
      referência.
- [ ] 3.6 Travar que **nada** de consumo de nuvem é medido: nenhuma coluna de bytes acumulados,
      nenhum lançamento gerado (`RF-09-20`, `RN-09-07`, documento 04). Verificar: enviar e
      confirmar um arquivo não cria lançamento no livro-razão nem altera saldo.

## 4. Regra da bibliografia

- [ ] 4.1 Em `backend/src/nucleo/bibliografias/regra.py`, criar `criar_bibliografia` com
      autoria estrita, exigindo título e capítulo e aceitando o exemplar como **opcional**
      (`RF-09-21`). Verificar: entrada sem exemplar é aceita; sem capítulo é recusada; de outro
      Mestre recebe `PermissaoNegada`.
- [ ] 4.2 Na mesma função, recusar exemplar inexistente e **ignorar** Apoiador enviado pelo
      cliente (`RF-09-21`, `RF-09-23`). Verificar: exemplar inexistente é recusado; Apoiador
      declarado no corpo não é gravado.
- [ ] 4.3 Criar a leitura que **deriva** disponibilidade e crédito — do ponto de apoio do
      exemplar e do aporte de origem dele —, cobrindo as três saídas do crédito (`RF-09-22`,
      `RF-09-23`, design — decisão 3). Verificar: sem vínculo nada é afirmado; com vínculo e sem
      aporte de origem não há crédito; com vínculo e aporte de Apoiador há crédito.

## 5. Porta HTTP

- [ ] 5.1 Criar `backend/src/nucleo/conteudos/rotas.py` com
      `POST /v1/missoes/{id}/conteudos`, `POST /v1/conteudos/{id}/arquivo` — que abre a sessão e
      devolve o endereço — e a confirmação do envio (`RF-09-14` a `RF-09-19`, PRD-09 §9).
      Verificar: as rotas aparecem em `/openapi.json` sob `/v1` e exigem chave de aplicação.
- [ ] 5.2 Criar `backend/src/nucleo/bibliografias/rotas.py` com
      `POST /v1/missoes/{id}/bibliografia` (`RF-09-21`, PRD-09 §9). Verificar: a rota responde
      201 e o corpo traz a entrada gravada.
- [ ] 5.3 Criar, no adaptador de disco, a rota local que recebe as partes por `Content-Range`,
      registrada **somente fora de produção** (`RF-09-19`, design — decisão 2). Verificar: em
      produção a rota não é registrada.
- [ ] 5.4 Registrar os roteadores em `backend/src/nucleo/principal.py` e mapear as recusas para
      os códigos do PRD-09 §9 — 403 para quem não é o Mestre autor, 422 para formato fora da
      lista e para conteúdo de terceiro sem fonte, 413 para tamanho acima do teto. Verificar: os
      três códigos saem no formato de erro único do PRD-01.
- [ ] 5.5 Estender `GET /v1/trilhas/{id}` para servir conteúdo e bibliografia por missão, na
      ordem declarada, só em trilha publicada (`RF-09-09`, `RF-09-10`, `RN-09-05`). Verificar:
      trilha em rascunho segue sem sair, e a publicada traz conteúdo, fonte do terceiro e
      bibliografia.

## 6. Testes do núcleo

- [ ] 6.1 Criar `backend/tests/test_conteudo.py` cobrindo os cenários da spec
      `conteudo-da-missao` — autoria estrita, os cinco tipos, fonte do terceiro, e a recusa de
      texto sem corpo e de link sem endereço (`RF-09-14`, `RF-09-15`, `RF-09-24`).
- [ ] 6.2 No mesmo arquivo, cobrir o envio — sessão aberta, retomada depois de corte no meio,
      bytes que nunca entram em tabela, conteúdo sem confirmação que não serve arquivo, e sessão
      pedida por quem não é o autor (`RF-09-16`, `RF-09-17`, `RF-09-19`, `RN-01-28`).
- [ ] 6.3 No mesmo arquivo, cobrir formatos e tetos — lista fechada, 413 do vídeo acima de
      200 MB e do arquivo acima de 20 MB, **dois vídeos na mesma missão aceitos**, e o envio que
      diverge do tamanho declarado (`RF-09-115`, `RF-09-16`, `RF-09-17`, `RF-09-18`,
      `RN-09-06`).
- [ ] 6.4 Travar a ausência de medição: envio confirmado não gera lançamento, não altera saldo e
      nenhuma rota expõe total de bytes (`RF-09-20`, `RN-09-07`).
- [ ] 6.5 Criar `backend/tests/test_bibliografia.py` cobrindo os cenários da spec
      `bibliografia-da-missao` — entrada com e sem vínculo, exemplar inexistente, mais de uma
      entrada por missão, e as três saídas do crédito ao Apoiador (`RF-09-21` a `RF-09-23`).
- [ ] 6.6 Travar a regressão das travas de publicação: a trilha continua publicando por **três
      travas e nenhuma outra**, e conteúdo de terceiro sem fonte NEVER entra na publicação
      porque nem chega a ser gravado (`RN-09-01` a `RN-09-03`, PRD-09 §9). Verificar: trilha com
      as três travas atendidas e sem conteúdo algum publica.
- [ ] 6.7 Cobrir a leitura pública — conteúdo e bibliografia na trilha publicada, com licença e
      crédito ao autor; nada na trilha em rascunho (`RF-09-09`, `RF-09-10`, `RN-09-05`).

## 7. App 09 — telas

- [ ] 7.1 Criar `apps/app-09-mestre/src/trilhas/FormularioDeConteudo.tsx` com a escrita de
      texto, a imagem, o link externo e a marcação de terceiro que pede a fonte, sem nenhum
      campo técnico (`RF-09-14`, `RF-09-15`, `RF-09-24`, `RN-09-16`). Verificar: a tela não
      confirma conteúdo de terceiro sem fonte.
- [ ] 7.2 Criar o envio de arquivo com **progresso visível** e retomada pela sessão do núcleo,
      com as recusas em linguagem simples dizendo tamanho e limite (`RF-09-16` a `RF-09-19`,
      `RF-09-115`, PRD-09 §10). Verificar: queda simulada no meio retoma do ponto enviado.
- [ ] 7.3 Criar o **salvamento automático do rascunho** do texto (PRD-09 §10). Verificar: o
      texto sobrevive a recarregar a página no meio da escrita.
- [ ] 7.4 Criar `apps/app-09-mestre/src/trilhas/Bibliografia.tsx` com título, capítulo e a
      escolha **opcional** do exemplar numa lista, apresentando disponibilidade e Apoiador só
      quando há vínculo, sem campo para digitar o crédito (`RF-09-21` a `RF-09-23`).
- [ ] 7.5 Criar a **pré-visualização** da missão sobre a leitura pública da trilha, que não
      grava nada nem muda a situação (`RF-09-25`, design — Risks).
- [ ] 7.6 Ligar as telas novas a `TelaDaTrilha.tsx` e ao cliente do núcleo em
      `src/trilhas/api.ts`. Verificar: a missão abre conteúdo, bibliografia e pré-visualização.

## 8. Testes da App 09

- [ ] 8.1 Em `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`, cobrir a escrita de conteúdo, a
      exigência da fonte do terceiro e a ausência de campo técnico (`RF-09-14`, `RF-09-15`,
      `RF-09-24`).
- [ ] 8.2 Cobrir o envio — progresso, retomada depois de queda, recusa por formato e recusa por
      tamanho em linguagem simples, sem código de erro (`RF-09-16` a `RF-09-19`, `RF-09-115`,
      `RF-09-18`).
- [ ] 8.3 Cobrir a bibliografia — entrada sem exemplar sem disponibilidade nem crédito, entrada
      com exemplar apresentando os dois, e ausência de campo para digitar o Apoiador
      (`RF-09-21` a `RF-09-23`).
- [ ] 8.4 Cobrir a pré-visualização, que apresenta conteúdo e bibliografia e não grava nada
      (`RF-09-25`).

## 9. Documentação e fecho

- [ ] 9.1 Atualizar `docs/prds/index.md` com o que esta fatia entregou e o que do PRD-09 segue
      pendente (CLAUDE.md — documentação a cada change). Verificar: `npm run lint` e
      `mkdocs build --strict` passam.
- [ ] 9.2 Rodar uma vez, ao fechar as tarefas, `ruff format .`, `ruff check --fix .` e `pytest`
      no backend, e `biome check .` e `vitest run` na App 09 (CLAUDE.md — ritmo de verificação).
