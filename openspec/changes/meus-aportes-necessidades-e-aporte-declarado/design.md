## Context

O núcleo já registra aporte (`openspec/specs/aporte/spec.md`), deriva Poder Sustentador e
necessidade de recurso, e a App 08 já tem sessão, porta pública e identidade. O que falta é o
elo entre os dois: um ato de escrita do **Apoiador** que declara dinheiro transferido e espera
homologação. Motivação e recorte: `proposal.md`.

Duas restrições do que já existe moldam o desenho. `Aporte` grava **lançamento, tipo de recurso
e ponto de apoio** obrigatórios — dados que quem transfere não fornece e que só o Admin arbitra
—, e `moedas_acumuladas_de` soma a tabela `aporte` direto, sem olhar lançamento, porque é o
piso do avatar próprio (`RN-14-11`).

## Goals / Non-Goals

**Goals:**

- A declaração pendente não toca derivação alguma que já existe: saldo, Poder Sustentador,
  moedas acumuladas, necessidade em aberto.
- A homologação continua sendo **um** ato: o registro do aporte pelo Admin, como no
  pré-cadastro.
- A App 08 lê necessidade e aporte sem nenhuma rota de cadastro da gestão.

**Non-Goals:**

- Missão do Apoiador, selo e nível de sustento (fatia 5), inclusive a origem "missão" do
  `RF-14-25`.
- Tela da gestão para a fila das declarações: é fatia 16 do PRD-02. Aqui nascem só as rotas.
- Confirmação automática de PIX: `RN-14-06` exige comprovante no Ciclo 01.

## Decisions

1. **A declaração é entidade própria (`AporteDeclarado`), não um `Aporte` que nasce pendente.**
   O `Aporte` só existe homologado, com lançamento, tipo e ponto de apoio preenchidos, e
   `origem_do_registro = app_08` — a terceira origem que o PRD-07 §8 já previa. É o mesmo
   desenho do pré-cadastro, cuja declaração vive em `SolicitacaoDeParticipacao` e só vira
   aporte no registro do Admin. _Alternativa descartada:_ `Aporte` pendente com
   `lancamento_id`, `tipo_de_recurso_id` e `ponto_de_apoio_id` anuláveis mais um campo de
   situação — obrigaria a filtrar "homologado" em toda leitura que hoje soma `Aporte` direto, e
   um esquecimento viraria moeda de graça.

2. **A unicidade impede o crédito em dobro.** `Aporte.aporte_declarado_id` é único e anulável,
   espelhando `solicitacao_de_participacao_id`; o segundo registro apontando a mesma declaração
   é 422, pela mesma regra já escrita para o pré-cadastro.

3. **A origem da escolha é declarativa, não vínculo.** A necessidade de recurso é derivada e
   não tem identificador próprio: a declaração guarda o par **aula + tipo de recurso** que a
   identifica, mais a modalidade (`necessidade`, `valor_sugerido`, `valor_livre`). A
   necessidade pode ter deixado de existir quando o Admin homologar — isso não invalida a
   declaração; quem arbitra o tipo, o ponto de apoio e a data do aporte no registro é o Admin.

4. **O perfil da escada é da tela, não do núcleo.** `Persona` não guarda perfil de pessoa
   física ou jurídica — só a solicitação de pré-cadastro guarda, e ela não sobrevive ao
   cadastro. A tela pergunta o perfil e reusa a escada já escrita em
   `apps/app-08-apoiador/src/preCadastro/ escada.ts`, movida para um módulo compartilhado da
   aplicação. _Alternativa descartada:_ gravar o perfil na `Persona` — dado novo que nenhum
   `RF` do PRD-14 pede.

5. **A recusa é rota nova do núcleo, restrita a Admin, com motivo obrigatório** (`POST
   /v1/aportes/declarados/{id}/recusa`), decidida pelo fundador em 2026-09-01: sem ela o estado
   "recusado" do `RF-14-27` não seria alcançável. A homologação **não** ganha rota: é o `POST
   /v1/aportes` que já existe, agora aceitando `aporte_declarado_id`, e o `RN-14-08` já é o
   `RN-07-16` que aquela rota aplica.

6. **Nome ao lado do identificador nas duas leituras.** `GET /v1/vitrine/necessidades`, `GET
   /v1/necessidades/minhas` e `GET /v1/meus-aportes` passam a trazer o nome do tipo de recurso,
   da comunidade e do ponto de apoio. Sem isso a App 08 precisaria de `/v1/tipos-de-recurso` e
   `/v1/pontos-de-apoio`, que são de Admin e Mestre. Campos novos ao lado dos antigos: a App
   09, que já lê a rota do Mestre, não muda.

7. **Comprovante pela mesma porta de armazenamento** do pré-cadastro e do aporte, com os mesmos
   formatos e o mesmo 422; nunca servido em rota pública, como a capacidade `aporte` já exige.

8. **A conversão para moedas na tela usa a escala do documento 04 §2**, já implementada em
   `escada.ts`. O núcleo devolve o valor declarado da transferência como o Apoiador o informou
   — a valoração em moedas do núcleo só nasce na homologação, pela vigência da data do aporte
   (`RF-07-05`) —, e a aplicação apresenta em moedas fora da tela de declaração (`RF-14-23`).

9. **Sem custo novo no livro-razão.** A declaração não gera lançamento; o único lançamento é o
   crédito da homologação, que a capacidade `aporte` já produz.

## Risks / Trade-offs

- **A declaração pendente vira dado órfão se ninguém homologar nem recusar** → a fila é da
  fatia 16 do PRD-02; até lá as rotas existem e a situação do Apoiador mostra "pendente", sem
  prazo prometido em tela.
- **O par aula + tipo pode não existir mais na homologação** → é declarativo por decisão 3; o
  Admin registra o aporte com o tipo e o ponto que valem no dia, e a declaração só aponta o que
  motivou a transferência.
- **Campos novos nas rotas de necessidade** → aditivos, sem remover nem renomear; o teste da
  App 09 e os testes de rota existentes continuam válidos.
- **A escala reais → moedas vive no frontend** → é onde já estava desde a fatia 2; duplicá-la
  no núcleo criaria segunda fonte para o mesmo número do documento 04 §2.

## Migration Plan

Uma migração Alembic: cria a tabela `aporte_declarado`, acrescenta `aporte_declarado_id` a
`aporte` (anulável, único) e o valor `app_08` ao enum de origem do registro. Todas as adições
são compatíveis com o que está gravado — nenhum aporte existente muda de origem nem perde
campo. A reversão derruba a tabela e a coluna.
