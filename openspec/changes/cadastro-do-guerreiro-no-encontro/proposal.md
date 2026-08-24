# Cadastro do Guerreiro(a) no encontro

Origem: **PRD-04 — App 01: Aula presencial**, §6.1. Segunda fatia do PRD-04.

Atende `RF-04-07`, `RF-04-08`, `RF-04-09`, `RF-04-10`, `RF-04-15`, `RF-04-17`, `RF-04-28` e
`RF-04-60`; **fecha** o `RF-04-01`, atendido em parte pela fatia anterior.

## Why

A fatia `esqueleto-da-aula-presencial-e-equipe-da-aula` abriu a App 01 com o caminho do
onboarding **desabilitado**, e gravou três decisões do fundador cujo código foi adiado para cá:
o cadastro de Guerreiro(a) pelo Mestre (decisão 2) e a conferência de nick atrás da sessão de
trabalho do aparelho (decisão 3). Decisão gravada sem código é dívida que envelhece: a matriz
do PRD-01 §4 e o PRD-04 §9 já dizem o que a rota faz, e a rota ainda não faz.

O que trava hoje não é uma tela. É que **nenhum Guerreiro(a) entra na plataforma pela porta que
o produto desenhou**. `POST /v1/guerreiros` só existe pelo caminho da gestão, restrito a Admin
em duas camadas — `Operacao.tudo` na rota e uma recusa explícita dentro de
`cadastrar_guerreiro_pela_gestao`. Sem esta fatia, a única forma de existir um Guerreiro(a) é um
Admin cadastrá-lo pela App 03, o que contradiz o invariante 3 do documento 99 §6: só o
Guerreiro(a) tem autocadastro.

Esta fatia entrega a **jornada 5.3** inteira — a criança que chega sem o responsável — porque é
a que não depende de consentimento nem de câmera. É a mesma escolha que a fatia anterior fez ao
entrar sem biometria, e pelo mesmo motivo: `RF-04-15` já prevê o cadastro ativo e sem imagem.

## What Changes

### O autocadastro sob a sessão de trabalho do aparelho

O núcleo passa a ter **dois caminhos distintos** para criar persona de Guerreiro(a), não um com
uma condição a mais:

| Caminho | Quem autentica | Autoria do cadastro | Atende |
| --- | --- | --- | --- |
| Gestão (App 03) | Admin | o Admin que cadastrou | `RF-02-01` |
| Encontro (App 01) | Mestre ou Admin, pela sessão de trabalho | o próprio Guerreiro(a) | `RF-04-07`, `RN-04-04` |

A distinção não é estilo: o invariante 3 diz que **só o Guerreiro(a) tem autocadastro**, e a
sessão de trabalho do aparelho **autentica** a escrita sem se tornar autora dela. Colar os dois
caminhos na mesma função apagaria isso. A matriz ganha a operação que a decisão 2 já gravou.

O cadastro nasce **ativo**, vinculado à comunidade da aula vigente sem que ninguém a informe
(`RF-04-10`, já garantido por `criar_persona`), **sem imagem**, e a **presença do dia é
registrada no mesmo ato** (`RF-04-17`). `registrar_presenca` já é idempotente por par de aula e
Guerreiro(a) e já aceita o momento do fato — não é reescrito.

### A faixa de 6 a 16 anos passa a existir no código

O invariante 1 do documento 99 §6 fixa a faixa etária, e **nenhuma linha do backend a aplica**:
`cadastrar_guerreiro_pela_gestao` confere apenas que a data de nascimento não é nula.

Decisão do fundador, 2026-08-24: a faixa é exigida **na regra**, e vale **retroativamente
também para o caminho da gestão** da App 03 — não só para o App 01. Requisito de tela não
protege invariante; se ficasse só na App 01, a App 03 seguiria cadastrando fora da faixa.

### A recusa de nick, e por que não existe rota de conferência do onboarding

Aqui esta fatia **corrige o PRD-04 §9 e a §13**, e o motivo importa.

O PRD-04 §9 declara `GET /v1/guerreiros/nick/disponivel`, e a decisão 3 da fatia anterior a pôs
atrás da sessão do aparelho. Mas a spec consolidada `persona-e-credencial` veda o oráculo de
nick de Guerreiro(a) definindo a vedação **pelo que a resposta alcança, não por quem pergunta**,
e declara a conferência restrita a nick de adulto como a **única** exceção. Uma rota de
conferência de alcance total contradiria esse requisito, ainda que exigisse a sessão do
aparelho — e o problema é real, porque `conferir_disponibilidade_de_nick` responde "disponível"
para nick de Guerreiro(a) em uso enquanto `criar_persona` aplica unicidade global: a tela diria
livre e a gravação recusaria.

Decisão do fundador, 2026-08-24: **a recusa vem da gravação**. Nenhuma rota de consulta ganha
alcance total. O cadastro do encontro recusa o nick em uso e devolve, na própria recusa, as
**variações conferidas com alcance total** (`RF-04-08`). A rota pública
`GET /v1/nicks/disponibilidade` segue adulto-only e **intocada**, e
`GET /v1/guerreiros/nick/disponivel` **não passa a existir** — o PRD-04 §9 sai da lista de
rotas desta aplicação.

O que resta de oráculo exige, cumulativamente: a chave da App 01, sessão de trabalho aberta,
aula agendada vigente e Mestre ou Admin autenticado na sala. É a presencialidade pagando o que
a rota pública não pode pagar.

### Decisão do fundador, 2026-08-24 — o responsável no encontro

Gravada aqui; **o código dela é da fatia seguinte**, junto do consentimento e da câmera.

`registrar_consentimento` exige `VinculoResponsavel` vigente, e o PRD-04 §3.2 punha o cadastro
de responsável fora do escopo desta aplicação. Na primeira turma ninguém teria responsável
cadastrado, e **toda criança cairia na jornada 5.3 por acidente de implementação**, não por
escolha da família — a jornada 5.2 nunca rodaria.

A App 01 passa a cadastrar o **responsável mínimo e o vínculo no ato do encontro**. O custo em
código é quase nulo: `POST /v1/responsaveis` e `POST /v1/responsaveis/{id}/vinculos` já existem,
já são de Admin e Mestre pela matriz, e `cadastrar_responsavel` já cria a persona sem dado
algum. O **anexo da digitalização** do termo continua fora: é da gestão, como o PRD-04 §3.2 já
diz.

`criar_vinculo` exige o **grau de parentesco**, dado que nenhum requisito do PRD-04 menciona.
Decisão do fundador: ele ganha requisito próprio, `RF-04-60`, no PRD-04 §6.1.

### A tela do encontro

A tela inicial habilita o caminho do onboarding, fechando o `RF-04-01`. O cadastro é
**formulário guiado, sem IA** — a conversa conduzida por modelo é da fatia seguinte. Coleta nome,
nick, forma de tratamento, data de nascimento e características do avatar (`RF-04-07`); recusa
nick em uso apresentando as variações devolvidas pelo núcleo (`RF-04-08`); interrompe e chama o
Mestre ou o Admin quando a idade cai fora da faixa (`RF-04-09`); e volta à tela inicial ao fim de
cada atendimento, sem deixar dado do anterior (`RF-04-28`).

## Capabilities

### New Capabilities

Nenhuma. O caminho do onboarding é da capacidade que a fatia anterior criou.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: ganha o **caminho do onboarding** — o cadastro do Guerreiro(a)
  no encontro pela jornada 5.3, a recusa de nick com variações em linguagem simples, a
  interrupção por idade fora da faixa e a presença registrada no mesmo ato. O requisito da tela
  inicial deixa de trazer o caminho do onboarding desabilitado.
- `persona-e-credencial`: o autocadastro do Guerreiro(a), hoje afirmado como invariante sem
  caminho que o exerça, ganha a sessão de trabalho do aparelho como **autenticação sem
  autoria**; a persona de Guerreiro(a) passa a exigir **idade entre 6 e 16 anos**; e o requisito
  "O núcleo nunca descobre nem sugere um nick" ganha a **segunda exceção declarada** — a recusa
  de gravação do cadastro do encontro, que sugere variações de alcance total sem que exista rota
  de consulta com esse alcance.
- `cadastro-de-persona`: o cadastro do Guerreiro(a) pela gestão passa a recusar idade fora da
  faixa de 6 a 16 anos, pela decisão retroativa. O papel que a rota aceita **não muda** — a
  gestão continua sendo caminho de Admin.

## Impact

| Onde | O quê |
| --- | --- |
| `backend/src/nucleo/personas/regra.py` | caminho do autocadastro, faixa etária, conferência interna de alcance total |
| `backend/src/nucleo/personas/rotas.py` | `POST /v1/guerreiros` pelos dois caminhos; variações na recusa |
| `backend/src/nucleo/permissoes.py` | operação de cadastro de Guerreiro(a) no encontro, para Mestre e Admin |
| `apps/app-01-aula-presencial/src/onboarding/` | pasta nova |
| `apps/app-01-aula-presencial/src/inicio/TelaInicial.tsx` | habilita o caminho do onboarding |

Sem migração Alembic: nenhuma coluna nova. `registrar_presenca`, `criar_persona` e
`conferir_disponibilidade_de_nick` não são reescritos — o alcance total é função nova, ao lado
da que existe, e a rota pública não a alcança.

Documentação no mesmo PR: PRD-04 §3.2 (sai o cadastro de responsável, fica o anexo do termo),
§4 (a coluna do que Mestre e Admin não podem fazer perde "cadastrar responsável por aqui"), §6.1
(`RF-04-60`), §9 (sai `GET /v1/guerreiros/nick/disponivel`) e §13 (a linha da conferência de
nick alcança a fonte); documento 03 §3.3 e documento 09 (as duas decisões novas em "Já
decididos"); `docs/prds/index.md` (situação do PRD-04 e narrativa da fatia). A matriz do PRD-01
§4 e o documento 02 §1 **já foram atualizados** pela fatia anterior — conferir, não duplicar.

## Fora do escopo

Reproduz o que o PRD-04 §3.2 já exclui, mais o limite desta fatia:

| O quê | Por quê |
| --- | --- |
| Consentimento e a porta HTTP de `consentimentos` | `RF-04-11`, `-12`; fatia seguinte |
| Cadastro do responsável mínimo e do vínculo | decisão gravada aqui, código na fatia seguinte |
| Câmera, vivacidade, descritor e _template_ | `RF-04-04`, `-13`, `-14`, `-48`; fatia seguinte |
| Presença por reconhecimento e recadastro da imagem | `RF-04-16`, `-18`, `-22`; dependem da câmera |
| Conversa conduzida por IA, áudio e chat | `RF-04-06`, `-27`; terceira fatia do onboarding |
| Fila local e sincronização sem rede | `RF-04-23` a `-25`; terceira fatia |
| Anexo da digitalização do termo assinado | PRD-04 §3.2 — é da App 03 |
| Agenda das aulas e ajuste de presenças | PRD-04 §3.2 — é da App 03 |
| Missão, conteúdo, entrega da produção, assistente | `RF-04-35` a `-40`; dependem do PRD-09 §6.3 |

## Pendências levantadas — decisão do fundador

Nenhuma trava esta fatia.

1. **`RF-02-71` continua sem rota**, quarta change seguida. Já registrado nas §14 do PRD-02 e do
   PRD-09; não alcança esta fatia.
2. **O registro de "quem confirmou" do `RF-04-15`** é hoje o `MiddlewareDeAuditoria`, que grava
   a persona da sessão em toda escrita sob `/v1` — mas em modo _best-effort_: falha dele vai só
   para o log, sem desfazer a resposta. A `Presenca` gravada no mesmo ato carrega o confirmador
   sem essa fragilidade. O design resolve por qual dos dois o requisito se cumpre, sem coluna
   nova; se nenhum dos dois bastar, vira pergunta ao fundador antes das tarefas.
