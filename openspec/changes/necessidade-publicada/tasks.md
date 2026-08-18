## 1. Derivação da necessidade

- [x] 1.1 Criar `backend/src/nucleo/necessidades/` com `__init__.py` e `regra.py` (`RF-07-18`)
- [x] 1.2 Definir a projeção da necessidade — aula, tipo de recurso, quantidade que falta,
      valor em moedas, comunidade, ponto de apoio, data e horário —, sem modelo de banco e sem
      migration (`RF-07-27`, design — Decisions 1)
- [x] 1.3 Implementar a atribuição gulosa por par tipo/ponto de apoio: parte de
      `disponivel_de()`, percorre as aulas pendentes de lastro em `inicio_em asc` e emite a
      falta de cada uma (`RF-07-18`, `RN-07-37`, design — Decisions 2)
- [x] 1.4 Excluir da derivação a aula em qualquer situação que não seja pendente de lastro, e o
      par cuja falta seja zero (`RF-07-18`, `RN-07-01`)
- [x] 1.5 Valorar a falta em moedas por `consultar_valor_de_referencia()` na data corrente, com
      duas casas, omitindo o campo quando não houver vigência válida (`RN-07-04`, `RN-07-05`,
      design — Decisions 4)
- [x] 1.6 Filtrar a derivação pelas comunidades a que uma persona está vinculada, para servir a
      leitura do Mestre (`RF-07-27`, design — Decisions 6)

## 2. Rotas de leitura

- [x] 2.1 Criar `rotas.py` com `GET /vitrine/necessidades`, pública, sem credencial de persona
      e sob chave de aplicação (`RF-07-27`, `RF-03-47`, `RF-01-02`, `RF-01-16`)
- [x] 2.2 Acrescentar `GET /necessidades/minhas`, exigindo sessão de Mestre e filtrando pelo
      vínculo de comunidade, fora do prefixo `/vitrine` (`RF-07-27`, design — Decisions 5)
- [x] 2.3 Garantir que as duas rotas sirvam a mesma projeção e que nenhuma traga valor em reais
      nem dado de pessoa (`RN-07-05`, invariante 16 do documento 99 §6)
- [x] 2.4 Registrar o roteador em `backend/src/nucleo/principal.py` (`RF-07-27`)

## 3. Rastreabilidade do aporte

- [x] 3.1 Acrescentar a citação de `RF-07-29` ao requisito do aporte declarado no pré-cadastro,
      sem alterar comportamento nem teste (`RF-07-29`)

## 4. Testes

- [x] 4.1 Falta de uma aula pendente vira necessidade com a quantidade certa (`RF-07-18`)
- [x] 4.2 Aula pendente por um tipo não gera necessidade do tipo já coberto (`RF-07-18`)
- [x] 4.3 Aula confirmada, realizada, cancelada ou prevista não gera necessidade (`RN-07-01`)
- [x] 4.4 Duas aulas disputando o mesmo saldo: a de horário inicial mais próximo conta primeiro,
      e a soma das faltas é a falta real do conjunto (`RF-07-18`, design — Decisions 2)
- [x] 4.5 A derivação e `confirmar_aulas_pendentes()` percorrem as aulas na mesma ordem, no
      mesmo cenário (`RN-07-37`, design — Decisions 3)
- [x] 4.6 Aula cujo horário já passou continua na lista enquanto pendente de lastro
      (`RF-07-18`)
- [x] 4.7 Aporte parcial abate a falta e a aula segue pendente de lastro (`RF-07-31`)
- [x] 4.8 Aporte que fecha o saldo apaga a necessidade e confirma a aula no mesmo ato
      (`RF-07-31`, `RN-07-37`)
- [x] 4.9 Cada provedor recebe as moedas do que aportou, na cobertura por mais de um (`RN-07-23`)
- [x] 4.10 A falta é valorada pela vigência corrente, e tipo sem vigência sai sem valor em
      moedas (`RN-07-04`, `RF-07-02`)
- [x] 4.11 A rota pública responde sem credencial de persona e recusa sem chave de aplicação
      (`RF-01-02`, `RF-01-16`)
- [x] 4.12 Nenhuma das rotas devolve valor em reais nem identifica pessoa (`RN-07-05`, critério
      de aceite do PRD-07 §12)
- [x] 4.13 A lista do Mestre traz as aulas das comunidades a que ele está vinculado e deixa de
      fora a comunidade alheia (`RF-07-27`)
- [x] 4.14 `ruff format --check .`, `ruff check .` e `pytest` passam em `backend/`

## 5. Documentação

- [x] 5.1 Corrigir o PRD-07 §9: `GET /vitrine/necessidades` no lugar de `GET /necessidades`, e
      `GET /necessidades/minhas` para o Mestre
- [x] 5.2 Atualizar o `RF-03-47` do PRD-03 com os campos que a vitrine passa a publicar
- [x] 5.3 Atualizar `docs/prds/index.md` com a narrativa da fatia entregue e a situação do
      PRD-07
- [x] 5.4 Conferir que os documentos 04 §1 e 09 já refletem as quatro decisões desta change,
      gravadas antes dela
- [x] 5.5 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR
