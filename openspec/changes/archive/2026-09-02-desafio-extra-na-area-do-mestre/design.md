## Context

A entidade `DesafioExtra` e o seu ciclo já existem: `openspec/specs/desafio-extra/spec.md`
traz a proposta do Apoiador (fatia 1 do PRD-14) e a fila, a aprovação, a publicação que reserva
a recompensa e o encerramento (fatia 15 do PRD-02). Esta fatia acrescenta a única transição que
faltava — a do Mestre — e o segundo proponente. Nenhum ato novo tem custo: a reserva e a baixa
continuam sendo da publicação, já entregue.

Duas guardas do núcleo já servem sem mudança: `lastro_provido` lê o aporte homologado **do
proponente**, sem supor papel, e `Aporte.provedor_id` é uma persona qualquer — o aporte por
absorção do Mestre (fatia 9 do PRD-09) entra como custeio sem código novo.

## Goals / Non-Goals

**Goals:** a validação e a recusa do Mestre autor; a fila do que ele tem a validar; o Mestre
como proponente, com a situação de nascimento decidida pelo proponente; a área da App 09.

**Non-Goals:** mexer no caminho do Apoiador, que fica igual; tocar a aprovação, a publicação, a
reserva ou o encerramento, que são do Admin e já existem; registrar a conclusão do desafio, que
é fatia à parte.

## Decisions

1. **A recusa do Mestre reaproveita `motivo_da_recusa`; só o parecer é coluna nova.** Um desafio
   é recusado uma vez, por Mestre ou por Admin, e `mestre_validador_id`/`admin_aprovador_id` já
   dizem por quem. A validação, porém, guarda texto que a recusa não guarda: entra
   `parecer_do_mestre` (texto, nulo), com uma revisão do Alembic. _Descartado:_ colunas
   separadas de motivo por papel — duplicariam a leitura sem distinguir nada.

2. **Um só ato de validação, com o desfecho no corpo:** `POST /v1/desafios-extras/{id}/validacao`
   recebe `situacao` — `em_aprovacao_do_admin` ou `recusado` — com `parecer` ou `motivo`, no
   mesmo molde da rota de aprovação do Admin que já existe. _Descartado:_ duas rotas
   (`/validacao` e `/recusa`) — a §9 do PRD-09 declara uma só.

3. **A posse fica na regra, não na matriz de permissões:** a rota exige apenas persona em
   sessão, e a regra confere `trilha.autor_id == operador.id`, respondendo **403** a qualquer
   outra — o mesmo desenho de `validar_criacao_original`. A matriz ganha uma única entrada, a
   da escrita: `propostas_de_desafio_extra` no papel Mestre. _Descartado:_ operação nova de
   validação na matriz — ela não distingue trilha própria de alheia, que é o que importa aqui.

4. **A dispensa é lida, não gravada.** `propor_desafio_extra` decide a situação de nascimento a
   partir do proponente: Mestre autor da trilha nasce em `em_aprovacao_do_admin`, qualquer outro
   em `em_validacao_do_mestre`. Quem quiser saber que houve dispensa lê a situação com
   `mestre_validador_id` nulo — no mesmo padrão de `lastro_provido`, derivado e nunca espelhado.
   _Descartado:_ coluna `validacao_dispensada` — espelho de dois campos que já dizem tudo.

5. **A justificativa pedagógica ocupa o campo `justificativa_do_vinculo`.** É o mesmo slot do
   direcionado, com o sentido dado pelo papel do proponente (documento 04 §3); a App 09 rotula
   "justificativa pedagógica" e a App 08 segue rotulando "justificativa do vínculo". _Descartado:_
   coluna própria — sempre nula para um dos dois proponentes, e a restrição
   `ck_desafio_extra_direcionado_exige_nick_e_justificativa` teria de ramificar por papel.

6. **`GET /v1/eu/desafios-extras` passa a filtrar por proponente, não por papel.** A consulta já
   é por `proponente_id`; cai só a recusa de quem não é Apoiador, que passa a alcançar Mestre.

7. **A App 09 ganha uma área, não duas.** `desafiosExtras/` reúne a fila do que validar e o que
   o Mestre propôs, no molde de `criacoesOriginais/` e `territorio/`; o `App.tsx` ganha a área
   na lista existente.

## Risks / Trade-offs

- **Ampliar uma rota que o Apoiador já usa em produção** → o caminho dele não muda em nenhum
  campo; a única bifurcação é a situação de nascimento, e os testes atuais da proposta do
  Apoiador ficam como regressão.
- **O Mestre autor propõe à própria trilha sem curadoria de terceiro** → é a `RN-09-41`, não um
  atalho: a aprovação do Admin continua exigida e o teto de 10 pontos vale para qualquer
  proponente (`RN-09-40`).
- **Um Mestre pode propor à trilha de outro** → cai na fila do Mestre autor como qualquer
  proposta (`RF-09-109`), e a fila nunca traz trilha alheia.

## Migration Plan

Uma revisão do Alembic acrescenta `desafio_extra.parecer_do_mestre` (texto, nulo). Sem
retrocarga: os desafios existentes estão todos em `em_validacao_do_mestre`, sem parecer a
gravar. A volta atrás derruba a coluna.
