## 1. Regra do núcleo

- [x] 1.1 Extrair de `cadastrar_guerreiro_pela_gestao` a validação comum dos dados do
      Guerreiro(a) — nome, nascimento e avatar — e acrescentar a ela a **faixa de 6 a 16 anos**,
      apurada na data da criação e com os extremos aceitos, recusando com 422 no campo
      `nascimento` (`RN-04-11`, `RF-04-09`, design — decisão 3). Verificar que
      `cadastrar_guerreiro_pela_gestao` passa a recusar idade fora da faixa sem que a rota da
      gestão mude.
- [x] 1.2 Criar em `personas/regra.py` a função do **caminho do encontro**, que cria a persona de
      Guerreiro(a) **sem criador** a partir da aula vigente, aplicando a validação comum de 1.1
      (`RF-04-07`, `RF-04-10`, `RN-04-04`, invariante 3, design — decisão 2). Verificar que a
      persona nasce com `criada_por` nulo e vinculada à comunidade da aula.
- [x] 1.3 Criar a conferência de nick de **alcance total** e a geração de variações sobre ela, ao
      lado de `conferir_disponibilidade_de_nick`, que fica intocada (`RF-04-08`, `RN-04-05`,
      design — decisão 4). Verificar que ela enxerga nick de Guerreiro(a), que a adulto-only
      continua não o enxergando, e que nenhuma rota a expõe.

## 2. Permissões e porta HTTP

- [x] 2.1 Acrescentar à matriz a operação de **cadastro de Guerreiro(a) no encontro**, concedida a
      Mestre e Admin (`RF-04-05`, `RF-04-07`; decisão do fundador de 2026-08-24 gravada na fatia
      anterior). Verificar que Guerreiro(a) e Apoiador seguem sem ela.
- [x] 2.2 Fazer `POST /v1/guerreiros` escolher o caminho pela **aplicação declarada na chave** —
      App 01 leva ao caminho do encontro, qualquer outra ao da gestão, que segue exigindo
      `Operacao.tudo` (design — decisão 1). Verificar que a chave da App 03 com sessão de Mestre
      recebe 403 e que a chave da App 01 com a mesma sessão é aceita.
- [x] 2.3 Gravar persona, vínculo de comunidade e **presença** numa transação só no caminho do
      encontro, no modo confirmação e tendo como confirmador a persona da sessão de trabalho
      (`RF-04-15`, `RF-04-17`, design — decisão 5). Verificar que a recusa do cadastro não deixa
      presença órfã e que o confirmador gravado é o adulto da sessão.
- [x] 2.4 Devolver as variações de alcance total no corpo da recusa 422 por nick em uso **apenas**
      no caminho do encontro, sem identificar a persona que tem o nick (`RF-04-08`, `RN-01-30`,
      design — decisão 4). Verificar que o caminho da gestão recusa sem variações.

## 3. App 01 — o caminho do onboarding

- [x] 3.1 Criar `apps/app-01-aula-presencial/src/api/guerreiros.ts` com a chamada do cadastro do
      encontro, tipando a recusa por nick com as variações e a recusa por idade (`RF-04-08`,
      `RF-04-09`).
- [x] 3.2 Criar `apps/app-01-aula-presencial/src/onboarding/TelaDeCadastro.tsx` — coleta de nome,
      nick, forma de tratamento, data de nascimento e características do avatar, recusa de nick em
      linguagem simples com as variações em um toque, e interrupção por idade fora da faixa
      orientando a chamar o Mestre ou o Admin (`RF-04-07`, `RF-04-08`, `RF-04-09`, `RF-04-10`).
      Verificar que a tela nunca consulta disponibilidade de nick antes de enviar (design —
      decisão 6).
- [x] 3.3 Habilitar o caminho do onboarding em `TelaInicial.tsx`, retirando o `disabled` e o
      aviso "em breve", e encaminhar o fim do atendimento pela volta ao início já existente
      (`RF-04-01`, `RF-04-28`). Verificar que nenhum dado da criança recém-cadastrada permanece
      após a volta.

## 4. Testes

- [x] 4.1 Em `backend/tests/`, cobrir a **faixa etária** nos dois caminhos: idade abaixo, acima e
      nos dois extremos, pelo caminho do encontro e pelo da gestão (`RN-04-11`, cenários "Idade
      abaixo da faixa é recusada", "Idade acima da faixa é recusada", "Os extremos da faixa são
      aceitos" e "A faixa alcança o caminho da gestão").
- [x] 4.2 Cobrir a **separação dos dois caminhos**: persona do encontro sem criador, persona da
      gestão com o Admin como criador, Mestre aceito pela chave da App 01 e recusado pela da
      gestão, e ausência de sessão recusada (cenários de "Só o Guerreiro(a) tem autocadastro").
- [x] 4.3 Cobrir a **recusa de nick**: variações de alcance total no caminho do encontro, ausência
      delas no da gestão, recusa que não revela o dono, e a conferência pública seguindo
      adulto-only para nick de Guerreiro(a) (cenários de "O núcleo nunca descobre nem sugere um
      nick").
- [x] 4.4 Cobrir **cadastro e presença no mesmo ato**: presença gravada com o cadastro, cadastro
      recusado sem deixar presença órfã, confirmador igual ao adulto da sessão, e segunda passagem
      do mesmo Guerreiro(a) sem segunda presença (`RF-04-15`, `RF-04-17`, PRD-04 §12).
- [x] 4.5 Em `apps/app-01-aula-presencial/src/onboarding/onboarding.test.tsx`, cobrir a tela:
      coleta dos cinco dados, recusa de nick com variação aceita em um toque, interrupção por
      idade fora da faixa, ausência de qualquer tela de consentimento ou captura, e volta ao
      início sem dado do atendimento anterior (cenários da capacidade
      `aplicacao-da-aula-presencial`).

## 5. Documentação

- [x] 5.1 Atualizar `docs/` com o que esta change decidiu e mudou: documento 03 §3.3 e documento
      09 (as duas decisões novas do fundador de 2026-08-24 — o responsável mínimo cadastrado no
      encontro e a faixa de 6 a 16 retroativa ao caminho da gestão — em "Já decididos"); PRD-04
      §3.2 (sai o cadastro de responsável, permanece o anexo do termo), §4 (Mestre e Admin deixam
      de ter "cadastrar responsável por aqui" entre o que não podem fazer), §6.1 (`RF-04-60`, o
      grau de parentesco do vínculo), §9 (sai `GET /v1/guerreiros/nick/disponivel`, e a recusa de
      gravação passa a ser onde o nick é conferido) e §13 (a linha da conferência de nick alcança
      a fonte); `docs/prds/index.md` (situação do PRD-04 e narrativa desta fatia). Conferir, sem
      duplicar, que a matriz do PRD-01 §4 e o documento 02 §1 já trazem a operação de cadastro de
      Guerreiro(a) pelo Mestre, gravada na fatia anterior. Nenhum arquivo novo em `docs/`, logo
      nada muda na `nav` do `mkdocs.yml`.
