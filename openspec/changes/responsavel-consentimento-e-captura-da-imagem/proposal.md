# Responsável, consentimento e captura da imagem

Origem: **PRD-04 — App 01: Aula presencial**, §§5.2, 6.1. Terceira fatia do PRD-04.

Atende `RF-04-11`, `RF-04-12`, `RF-04-13`, `RF-04-14`, `RF-04-48` e `RF-04-60`, e a metade
do `RF-04-04` que a câmera resolve, sob `RF-01-13`, `RF-01-15`, `RF-01-19`, `RN-01-12`,
`RN-01-17` e `RN-04-07`.

## Why

A fatia anterior entregou a jornada 5.3 — a criança que chega **sem** o responsável. A
jornada 5.2, que é o caminho normal do produto, nunca rodou: hoje **toda** criança é
cadastrada como se tivesse chegado sozinha, porque a App 01 não tem termo, não tem câmera e
não sabe cadastrar responsável. O `RF-04-15` é a exceção, e o repositório a transformou em
regra.

`consentimentos/` é o terceiro módulo órfão que a App 01 destrava — depois de `equipes` na
primeira fatia e do caminho não-gestão de `personas` na segunda. `registrar_consentimento` e
`consultar_consentimento_vigente_em` estão escritos e testados desde a change
`responsavel-vinculo-e-consentimento`, a capacidade `consentimento` está consolidada em
`openspec/specs/consentimento/spec.md` com quatro requisitos, e **nenhum deles é alcançável
por HTTP**.

O que trava é uma cadeia, não uma tela. Cada elo é recusa do elo seguinte:

| Elo                                  | Situação | Quem o exige                             |
| ------------------------------------ | -------- | ---------------------------------------- |
| `POST /v1/guerreiros`                | existe   | —                                        |
| `POST /v1/responsaveis`              | existe   | o vínculo                                |
| `POST /v1/responsaveis/{id}/vinculos` | existe  | `registrar_consentimento` (`RF-01-15`)   |
| `POST /v1/consentimentos`            | **falta** | `gravar_ou_recadastrar_template` (`RN-01-17`) |
| `POST /v1/guerreiros/{id}/descritor` | existe   | —                                        |

Sem o elo que falta, o `template` biométrico é inalcançável, e sem `template` a fila na porta
do encontro nunca deixa de depender da confirmação humana. É também o que explica a decisão
do fundador de 2026-08-24 sobre o responsável mínimo: sem vínculo gravado no ato, a jornada
5.2 não fica "menos completa" — ela não roda.

## What Changes

### O cadastro do responsável passa a levar o nome (`RF-04-60`)

`POST /v1/responsaveis` hoje aceita **corpo vazio**: a persona nasce sem nome, sem e-mail e
sem credencial. O `Consentimento` gravado sobre ela apontaria para um responsável anônimo, o
que a §11 do PRD-04 não sustenta — a base legal da captura é o consentimento **de alguém**.

A rota passa a aceitar o **nome**; o vínculo continua exigindo o **grau de parentesco**, que
`criar_vinculo` já cobra e que agora tem requisito que o preveja (`RF-04-60`). E-mail,
credencial de acesso à App 07 e a digitalização do termo assinado **continuam sendo da
gestão** (App 03), como o PRD-13 §11 já atribui e o PRD-04 §3.2 já exclui desta aplicação.

### A porta HTTP do consentimento (`RF-04-12`, PRD-04 §9)

`POST /v1/consentimentos` registra o termo assinado, com testemunha, data e hora. Nenhuma
regra nova: o tipo do conjunto fechado, o vínculo vigente exigido e a natureza somente
inserção são os que a capacidade `consentimento` já consolida.

A **versão do termo é carimbada pelo núcleo**, por nova constante de `Configuracao` — a rota
não a recebe do cliente. Decisão do fundador, 2026-08-24: cliente não escolhe a versão do
termo jurídico que a linha de auditoria vai afirmar. Trocar o termo é trocar a configuração.

### A câmera na App 01 (`RF-04-13`, `RF-04-14`, `RF-04-48`)

A aplicação passa a exibir o termo na tela, colher a confirmação da assinatura pelo Mestre ou
Admin — que fica registrado como **testemunha** —, e só então capturar a imagem. No próprio
aparelho, pela biblioteca **Human**, na ordem **prova de vivacidade e depois descritor
facial** (documento 03 §3.3). Ao núcleo vai apenas o descritor; a fotografia é **descartada
sem sair do aparelho** e nunca é exibida.

### Sem câmera, fecha só a captura (`RF-04-04`, `RN-04-03`)

Decisão do fundador, 2026-08-24: aparelho sem câmera **não fecha o onboarding inteiro**. A
jornada 5.3 continua disponível — cadastro ativo, sem imagem, com registro de quem confirmou
— e a tela avisa que a captura exige outro aparelho. É o que o `RN-04-09` exige: não ter
biometria nunca tira ninguém da aula.

## Capabilities

### New Capabilities

Nenhuma. As três capacidades tocadas já existem e são consolidadas.

### Modified Capabilities

- `consentimento`: ganha a porta HTTP que nunca teve, e a versão do termo passa a ser
  carimbada pelo núcleo em vez de declarada pelo cliente.
- `responsavel-e-vinculo`: o cadastro do responsável passa a aceitar o nome, e o grau de
  parentesco do vínculo ganha o requisito de tela que o previa (`RF-04-60`).
- `aplicacao-da-aula-presencial`: o onboarding ganha o cadastro do responsável mínimo, o
  termo na tela, a testemunha e a captura da imagem; a restrição da fatia anterior se reduz à
  entrada por reconhecimento facial.

## Impact

**Núcleo** — `consentimentos/rotas.py` (novo), `responsaveis/rotas.py` e `responsaveis/regra.py`
(nome), `configuracao.py` (constante da versão do termo), `principal.py` (registro do roteador).
`consentimentos/regra.py`, `biometria/` e `personas/` não mudam de regra.

**App 01** — a captura no fluxo do onboarding, o termo, o cadastro do responsável e a primeira
integração de biblioteca de terceiro no navegador do repositório (Human). Vitest com câmera e
modelos falsos: nenhum teste baixa modelo nem abre dispositivo.

**Fora desta fatia** — `RF-04-16` (captura de quem já se cadastrou sem imagem, quando o
responsável comparece depois) fica para a fatia da câmera na entrada: a App 01 só conhece o
**nick**, e resolver nick → id esbarra no `RN-01-22`. `RF-04-11` entrega só a exibição na
tela; a leitura em voz alta depende da modalidade áudio (`RF-04-06`), que ainda não existe.
Continuam fora, porque o PRD-04 §3.2 já os exclui: o anexo da digitalização do termo e o
vínculo com Guerreiro(a) já cadastrado, ambos da App 03.
