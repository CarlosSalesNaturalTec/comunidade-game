## 1. Leitura do catálogo de tipos de recurso no núcleo

- [ ] 1.1 `recursos/regra.py::listar_tipos_de_recurso` e o docstring de
      `GET /v1/tipos-de-recurso`: aceitar persona **Mestre** além de Admin, mantendo a escrita
      privativa do Admin e o descarte do tipo sem valor de referência vigente. Verificar por
      `tests/test_tipo_de_recurso.py` — Mestre lê os mesmos campos que o Admin, com natureza e
      exige comprovante; Apoiador recebe 403; Mestre que tenta cadastrar recebe 403 (`RF-09-56`,
      `RF-09-57`, `RF-07-01`).

## 2. Área de recursos na App 09

- [ ] 2.1 `apps/app-09-mestre/src/recursos/api.ts`: tipos e chamadas de
      `GET /v1/necessidades/minhas`, `POST /v1/aportes/absorcao` (multipart, com `aula_id`,
      `valor_de_origem` e comprovante opcionais) e `GET /v1/meus-aportes/ressarciveis`, mais as
      leituras de apoio de `GET /v1/tipos-de-recurso`, `GET /v1/pontos-de-apoio` e
      `GET /v1/comunidades` para resolver nomes. Verificar pela compilação e pelo uso nas telas
      de 2.2 a 2.4 (`RF-09-56`, `RF-09-57`, `RF-09-59`).
- [ ] 2.2 `recursos/ListaDeNecessidades.tsx`: a falta de cada aula com tipo, quantidade, valor em
      moedas, ponto de apoio e data e horário, na ordem que o núcleo devolveu — sem soma, sem
      reordenação e sem reais. Necessidade de tipo sem valor de referência vigente aparece
      declarando isso, sem valor nem nome arbitrado; lista vazia diz que não há necessidade em
      aberto (`RF-09-56`, `RN-09-12`).
- [ ] 2.3 `recursos/AbsorcaoDaNecessidade.tsx`: o ato de confirmação a partir da linha escolhida
      — tipo, ponto de apoio e aula herdados, quantidade sugerida na falta e editável, valor de
      origem em reais exigido nas naturezas consumível, durável e financeira e ausente em
      serviço, sempre ao lado do equivalente em moedas, e comprovante quando o tipo o exigir,
      restrito a PDF, JPG e PNG. Nenhum campo de provedor, homologação ou destinação; a tela
      declara que o aporte nasce em nome do Mestre e ressarcível, e a recusa do núcleo vira
      mensagem em linguagem simples com a necessidade mantida na lista (`RF-09-57`, `RF-09-58`,
      `RN-09-13`, `RN-09-16`).
- [ ] 2.4 `recursos/MinhasAbsorcoes.tsx`: as absorções do próprio Mestre com tipo, quantidade,
      ponto de apoio, moedas, data e situação — em aberto, ressarcido ou não se aplica, esta
      última apresentada como absorção de serviço e não como pendência. Somente leitura: nenhuma
      ação de exigir, apressar, reordenar ou cancelar. O aviso de que a plataforma não guarda
      dado bancário e de que a chave PIX vai por e-mail ao Admin fica nesta tela, em texto, sem
      endereço e sem `mailto:` (`RF-09-59`, `RF-09-60`, `RN-09-23`).
- [ ] 2.5 `recursos/TelaDeRecursos.tsx` e `App.tsx`: a área "Recursos" na navegação, reunindo as
      necessidades e o acompanhamento das absorções, com a releitura das duas listas depois de
      cada absorção confirmada (design — decisão 8) (`RF-09-56`, `RF-09-57`, `RF-09-59`).

## 3. Testes das telas

- [ ] 3.1 `apps/app-09-mestre/src/recursos/recursos.test.tsx`: os cenários de "A App 09 apresenta
      ao Mestre as necessidades de recurso das aulas dele" e de "O Mestre assume a necessidade
      como absorção em um ato de confirmação" — falta apresentada com os seis campos, ausência de
      reais, tipo sem valor de referência vigente, lista vazia, absorção completa, absorção
      parcial que mantém a necessidade abatida, absorção que fecha o saldo e some da lista,
      valor de origem exigido em consumível e ausente em serviço, ausência de provedor,
      homologação e destinação, e a recusa por tipo sem vigência em linguagem simples.
- [ ] 3.2 `apps/app-09-mestre/src/recursos/ressarcimento.test.tsx`: os cenários de "O Mestre
      acompanha a situação do ressarcimento do que absorveu" e de "A App 09 não coleta nem exibe
      dado bancário" — aportes do próprio Mestre com os seis campos e a situação, ausência de
      ação de apressar, ausência de absorção de outra persona, serviço apresentado como não se
      aplica, ausência de qualquer campo de chave PIX, banco ou conta em toda a área, e o aviso
      do envio da chave por e-mail ao Admin sem que a aplicação envie e-mail.

## 4. Documentação

- [ ] 4.1 `openspec/cronograma-de-fatias.md`: marcar a fatia **9** do PRD-09 como implementada,
      com o slug desta change na linha. Nada muda em `docs/`: a change não tomou decisão nova,
      não alterou requisito de PRD, não mudou a situação do PRD-09 nem a relação entre
      documentos, e não criou arquivo novo em `docs/`.
