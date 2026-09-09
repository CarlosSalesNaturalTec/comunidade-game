## 1. Camada de API da App 03

- [ ] 1.1 Em `src/recursos/api.ts`, acrescentar `cadastrarTipoDeRecurso` ao lado da
      `listarTiposDeRecurso` que já existe — `POST /v1/tipos-de-recurso` com nome, natureza,
      unidade, exige comprovante, valor em moedas e início de vigência, devolvendo o tipo criado
      com o valor vigente. Verificar pelo teste de que a chamada monta o corpo esperado e
      propaga a recusa 422 com o campo (`RF-02-107`, design — decisão 2).
- [ ] 1.2 Criar `src/catalogos/api.ts` com `listarTiposDeColeta` e `cadastrarTipoDeColeta`. A
      listagem segue `proximo_cursor` até o fim, como `src/territorio/api.ts` faz com os locais.
      Verificar pelo teste de que duas páginas do núcleo viram uma lista só (`RF-02-108`,
      design — decisões 2 e 3).

## 2. Área Catálogos

- [ ] 2.1 Criar `src/catalogos/TelaDeCatalogos.tsx` reunindo os dois catálogos, no molde de
      `TelaDePoderes` — sem seletor de comunidade, com `Moldura`, `Cabecalho` e `Aviso` da camada
      comum, e recusa de sessão tratada por `ehRecusaDeSessao`. Verificar pelos cenários "A área
      reúne os dois catálogos" e "A área não pede comunidade" (`RF-02-107`, `RF-02-108`,
      design — decisão 1).
- [ ] 2.2 Registrar a área em `src/App.tsx`, ao lado de `Poderes`, com chave `catalogos` e rótulo
      `Catálogos`. Verificar pelo teste de navegação de `App.test.tsx`, que já confere os rótulos
      das áreas (`RF-02-107`, `RF-02-108`).

## 3. Catálogo de tipos de recurso

- [ ] 3.1 Criar `src/catalogos/ListaDeTiposDeRecurso.tsx` — lista densa com nome, natureza,
      unidade, marca de exige comprovante e valor em moedas vigente, mais a linha fixa que diz
      que a lista traz os tipos com valor vigente na data, e o estado de catálogo vazio como
      informação. Verificar pelos cenários "A lista traz o valor da vigência corrente", "A lista
      diz que mostra apenas o que tem valor vigente" e "Catálogo vazio não é apresentada como
      falha" (`RF-02-107`, design — decisão 4).
- [ ] 3.2 Criar `src/catalogos/FormularioDeTipoDeRecurso.tsx` — nome, natureza em escolha entre
      as quatro, unidade, exige comprovante opcional, valor em moedas e início de vigência com a
      data de hoje por padrão, num ato único, oferecido só ao Admin. Verificar pelos cenários
      "Admin cadastra o tipo com a primeira vigência no mesmo ato", "A natureza é escolhida,
      nunca digitada", "O tipo nasce sem exigir comprovante" e "Quem não é Admin não alcança o
      cadastro" (`RF-02-107`, `RN-02-20`, `RN-07-22`).
- [ ] 3.3 Apresentar a recusa do núcleo em linguagem simples, no campo que a originou — campo em
      falta, natureza fora das quatro, valor negativo ou com mais de duas casas. Verificar pelo
      cenário "A recusa do núcleo é apresentada no campo" (`RF-02-107`, `RN-07-04`).

## 4. Catálogo de tipos de coleta

- [ ] 4.1 Criar `src/catalogos/ListaDeTiposDeColeta.tsx` — lista densa com nome, forma de
      registro, unidade e faixa quando houver, e o tipo desativado assinalado. Verificar pelos
      cenários "A lista traz os tipos cadastrados", "O tipo por evidência aparece sem unidade e
      sem faixa", "O tipo desativado aparece assinalado" e "A lista segue a paginação até o fim"
      (`RF-02-108`, `RF-08-06`).
- [ ] 4.2 Criar `src/catalogos/FormularioDeTipoDeColeta.tsx` — nome e forma de registro em
      escolha entre as três; unidade e faixa aparecem e passam a ser exigidas apenas na forma
      `número`, e somem nas formas `foto` e `vídeo`. Oferecido só ao Admin. Verificar pelos
      cenários "Admin cadastra o tipo que se mede por número", "A forma número exige unidade e
      faixa antes de confirmar", "A forma por evidência dispensa unidade e faixa", "A forma de
      registro é escolhida, nunca digitada" e "Quem não é Admin não alcança o cadastro"
      (`RF-02-108`, `RF-08-12`, `RF-08-21`, `RN-02-20`, design — decisão 5).
- [ ] 4.3 Apresentar a recusa do núcleo em linguagem simples, no campo que a originou — campo em
      falta, forma fora das três, faixa invertida. Verificar pelo cenário "A recusa da faixa é
      apresentada no campo" (`RF-02-108`).

## 5. Testes

- [ ] 5.1 Criar `src/catalogos/catalogos.test.tsx` cobrindo os vinte cenários da spec do delta,
      agrupados pelos cinco requisitos, com o núcleo dublado por `vi.spyOn` sobre os módulos de
      API, no padrão de `poderes.test.tsx` e `territorio.test.tsx` (`RF-02-107`, `RF-02-108`).
- [ ] 5.2 Estender `src/recursos/recursos.test.tsx` com o `cadastrarTipoDeRecurso` da tarefa 1.1,
      sem tocar nos casos que já passam (`RF-02-107`).

## 6. Documentação

- [ ] 6.1 No PRD-02: acrescentar `RF-02-107` e `RF-02-108` à tabela da §6.1, as quatro rotas
      consumidas à tabela da §9 e a pendência da edição, desativação e vigência nova à §14; a
      mesma pendência entra na tabela do documento 09 §1. Nenhum documento-fonte muda e nada se
      move de "pendente" para "decidido": o cadastro dos dois catálogos por Admin já estava
      decidido (`proposal.md` — Decisão de planejamento).
- [ ] 6.2 Marcar a fatia 19 como implementada em `openspec/cronograma-de-fatias.md`, com o slug
      da change. `docs/prds/index.md` não muda — a situação do PRD-02 segue a mesma —, o
      documento 99 não muda — nenhuma relação entre documentos mudou — e o `mkdocs.yml` não muda,
      porque nenhum arquivo nasceu em `docs/`.
