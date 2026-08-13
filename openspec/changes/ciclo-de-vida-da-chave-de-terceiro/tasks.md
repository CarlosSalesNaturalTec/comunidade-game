## 1. Modelo e migração

- [ ] 1.1 Acrescentar a `ChaveDeAplicacao` (`backend/src/nucleo/chaves/modelo.py`) o vínculo
      **único** com `solicitacao_de_chave`, nulo para a chave do projeto (`RN-01-51`,
      `design.md` — índice parcial). Verificável: duas chaves não conseguem apontar a mesma
      solicitação
- [ ] 1.2 Trocar o predicado de `uq_chave_vigente_por_aplicacao_e_ambiente` para alcançar só
      `natureza = 'do_projeto'` (`RF-01-54`, `RN-01-51`). Verificável: duas chaves de terceiro
      vigentes com o mesmo par aplicação e ambiente coexistem, e duas do projeto não
- [ ] 1.3 Escrever a migração Alembic do vínculo e do índice recriado (`design.md` — Migration
      Plan). Verificável: a migração sobe e desce, e as dezesseis chaves semeadas continuam
      vigentes depois de subir
- [ ] 1.4 Acrescentar `prazo_de_apresentacao_dias: int = 30` a `Configuracao`
      (`backend/src/nucleo/configuracao.py`), junto das cotas e do freio (`RN-01-36`,
      `design.md` — o prazo é configuração). Verificável: o ambiente que não declara sobe com
      30

## 2. Emissão

- [ ] 2.1 Implementar a emissão em `backend/src/nucleo/chaves/regra.py`: exige solicitação
      **aprovada**, cria a chave de natureza de terceiro presa a ela e devolve o segredo uma
      única vez (`RF-01-50`, `RN-01-35`). Verificável: teste de que a segunda leitura da mesma
      chave não recupera o segredo
- [ ] 2.2 Recusar a emissão sobre solicitação recebida, em avaliação ou recusada, e sobre
      solicitação que já rendeu chave (`RF-01-50`, `RN-01-51`). Verificável: os quatro casos
      recusam e nenhuma chave é criada
- [ ] 2.3 Emitir sempre no ambiente de **produção**, qualquer que seja o ambiente em que o
      Admin opera (`RN-01-51`). Verificável: emissão feita num núcleo de desenvolvimento
      produz chave de produção
- [ ] 2.4 Gravar o prazo de apresentação na emissão, contado da data de emissão pela
      configuração, e não recalculá-lo depois (`RF-01-51`, `design.md`). Verificável: mudar a
      configuração não altera o prazo de uma chave já emitida
- [ ] 2.5 Expor `POST /v1/chaves`, restrita a Admin (`RF-01-50`, PRD-01 §9). Verificável:
      Mestre, Apoiador e responsável recebem 403

## 3. Apresentação da URL

- [ ] 3.1 Implementar a apresentação: identifica a chave pelo `{id}`, registra a URL com data e
      hora e mantém a chave vigente sem novo prazo (`RF-01-51`). Verificável: chave com URL
      apresentada segue vigente depois de passada a data do prazo original
- [ ] 3.2 Recusar apresentação fora do prazo com 422 e a orientação de solicitar nova chave
      (`RF-01-51`, PRD-01 §12). Verificável: o corpo do erro traz a orientação em linguagem
      simples
- [ ] 3.3 Recusar a segunda apresentação para a mesma chave, mantendo a primeira URL
      (`RF-01-51`, `design.md` — escolha conservadora). Verificável: a URL registrada não muda
- [ ] 3.4 Recusar `{id}` desconhecido sem revelar se a chave existe, e recusar `{id}` de chave
      do projeto, que não tem prazo a cumprir (`RF-01-51`, `RN-01-33`). Verificável: as duas
      recusas não confirmam existência
- [ ] 3.5 Expor `POST /v1/chaves/{id}/url` como rota **pública** — sem credencial de persona,
      com a chave da aplicação que chama —, sem confundir a chave da chamada com a chave alvo
      (`RF-01-51`, `RN-01-33`, PRD-01 §9). Verificável: chamada com a chave da vitrine registra
      a URL na chave de terceiro indicada e nada na chave da chamada

## 4. Revogação

- [ ] 4.1 Implementar a regra do decurso — prazo vencido sem URL implica revogada — num único
      ponto reaproveitado pelos dois caminhos de leitura (`RF-01-52`, `design.md`).
      Verificável: os dois caminhos produzem o mesmo estado final
- [ ] 4.2 Aplicar e **persistir** a transição na conferência da chave
      (`backend/src/nucleo/chaves/conferencia.py`), mantendo a recusa indistinta de ausente,
      inválida e revogada (`RF-01-52`, `RF-01-48`). Verificável: a chamada seguinte ao
      vencimento recebe 401 idêntico ao de chave inexistente
- [ ] 4.3 Aplicar e persistir a mesma transição na leitura de gestão, para que a chave vencida
      apareça revogada mesmo sem nunca ter voltado a chamar (`RF-01-52`, `design.md` — a
      situação acompanha). Verificável: chave vencida que nunca mais chamou aparece revogada no
      painel
- [ ] 4.4 Gravar, na revogação por decurso, o motivo e **nenhuma autoria de pessoa**, para
      distingui-la da revogação de Admin (`RF-01-52`, `RF-01-53`). Verificável: o registro tem
      motivo e autoria vazia
- [ ] 4.5 Implementar `DELETE /v1/chaves/{id}`, de Admin, exigindo motivo e gravando autoria e
      data e hora (`RF-01-53`). Verificável: revogação sem motivo é recusada e a chave
      permanece vigente
- [ ] 4.6 Confirmar que a revogação não altera nem remove registro algum (`RF-01-53`).
      Verificável: teste que compara o estado do banco antes e depois, fora a própria chave

## 5. Leitura de gestão

- [ ] 5.1 Implementar `GET /v1/chaves`, de Admin, com aplicação, natureza, ambiente, prazo, URL
      apresentada e situação, paginada pelo contrato único (`RF-01-53`, `RF-01-28`, PRD-01 §9).
      Verificável: a listagem responde no formato de paginação já usado pelas demais
- [ ] 5.2 Garantir que a resposta nunca traga o segredo nem o seu resumo criptográfico
      (`RN-01-35`). Verificável: teste que inspeciona o corpo da resposta de uma chave
      recém-emitida
- [ ] 5.3 Recusar a leitura a quem não é Admin (`RF-01-16`). Verificável: as demais personas
      recebem 403

## 6. Fila de avaliação

- [ ] 6.1 Acrescentar a `SolicitacaoDeChave` (`backend/src/nucleo/fila/modelo.py`) o vínculo
      com a chave emitida, como o PRD-01 §8 a descreve (`RF-01-49`, `RF-01-50`). Verificável: a
      solicitação e a chave ficam consultáveis juntas
- [ ] 6.2 Manter a aprovação como ato que **não emite**: o desfecho grava e a emissão segue
      sendo ato seguinte do Admin (`RF-01-49`, `RF-01-50`). Verificável: aprovar não cria chave
      alguma

## 7. Registro e verificação

- [ ] 7.1 Registrar o roteador de chaves em `principal.py` pelo `incluir_roteador_de_dados`
      (`RF-01-01`, `RN-01-32`). Verificável: as rotas novas exigem chave como todas as demais
- [ ] 7.2 Confirmar que emissão, apresentação de URL e revogação entram na trilha de auditoria
      pelo _middleware_, sem nada declarado na rota (`RF-01-29`). Verificável: as três escritas
      produzem registro com autor, papel e momento
- [ ] 7.3 Rodar `ruff format --check .`, `ruff check .` e `pytest` em `backend/`, as três
      verificações que bloqueiam o merge. Verificável: as três passam

## 8. Documentação

- [ ] 8.1 Conferir que `docs/` já reflete o que esta change implementa: documento 03 §8 e
      documento 09 com a entrega do identificador e o prazo como parâmetro da implantação,
      `RF-02-89` com o identificador, e as demais decisões nos documentos 02, 03 e 09 e nos
      PRD-01 e PRD-03. `docs/prds/index.md` não muda de situação — o PRD-01 segue "aprovado",
      fatiado em changes. Verificável: nenhuma regra implementada fica sem origem em `docs/`
- [ ] 8.2 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR,
      ainda que `docs/` não mude nesta change. Verificável: os três passam
