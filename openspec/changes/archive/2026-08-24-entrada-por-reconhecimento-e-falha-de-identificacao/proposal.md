# Entrada por reconhecimento e falha de identificação

Origem: **PRD-04 — App 01: Aula presencial**, §§5.4, 5.5 e 6.1. Quarta fatia do PRD-04.

Atende `RF-04-18`, `RF-04-19`, `RF-04-20`, `RF-04-21` e `RF-04-22`, e **fecha** o `RF-04-29`,
atendido em parte pela primeira fatia. Sob `RF-01-04`, `RF-01-06`, `RF-01-20`, `RN-01-16`,
`RN-01-22`, `RN-04-06`, `RN-04-09`, `RN-04-12` e `RN-04-14`.

## Why

A terceira fatia ensinou o aparelho a **gerar** o descritor facial e o núcleo a guardá-lo. Não
há, hoje, um único caminho que o **leia**: o _template_ é gravado no onboarding e nunca mais
consultado. Quem já é cadastrado volta ao encontro seguinte e entra do mesmo jeito de quem não
tem biometria — pelo nick e pela confirmação de um adulto.

O órfão desta vez está no `enum`, e o próprio núcleo o anuncia:

```text
aulas/modelo.py    ModoDeComprovacao.reconhecimento   nenhuma rota o produz
                   ModoDeComprovacao.confirmacao      duas rotas o produzem

aulas/rotas.py     "o modo reconhecimento continua exclusivo do App 01"
                   …e a App 01 não o tem.
```

São **duas** portas órfãs no mesmo nó. A outra é `POST /v1/sessoes/guerreiro` — nick e
descritor, escrita e testada desde a change `sessao-do-guerreiro-e-biometria`, com a recusa
indistinguível do `RN-01-22` já no lugar — que **nenhum cliente chama**.

A consequência é maior que uma tela. A presença por reconhecimento é o que o produto promete à
criança ao fim do cadastro (`RF-04-27`), é o que dispensa um adulto na porta a cada chegada, e
é o dado que o painel do dia da App 03 e a App 07 leem como participação. Enquanto ela não
existe, o `ModoDeComprovacao` tem um valor que nenhuma linha da plataforma pode produzir, e a
biometria da fatia anterior é escrita sem leitura.

Esta fatia também é o **piso da fila local** (`RF-04-23` a `RF-04-25`, jornada 5.6): a fila
guarda apenas presença, e hoje não há presença a enfileirar fora do ato do cadastro.

## What Changes

### A presença por reconhecimento ganha quem a escreva (`RF-04-18`, PRD-04 §9)

`POST /v1/aulas/{id}/presencas` hoje recusa o modo `reconhecimento` antes de chamar a regra. A
rota passa a aceitá-lo **quando a chave declara a App 01**, pelo mesmo desenho de dois caminhos
que a segunda fatia deu ao `POST /v1/guerreiros`:

| Caminho          | Quem autentica                      | Modo aceito     | Confirmador       |
| ---------------- | ----------------------------------- | --------------- | ----------------- |
| Gestão (App 09)  | Mestre ou Admin                     | confirmação     | quem confirmou    |
| Encontro (App 01) | sessão de trabalho do aparelho      | os dois         | só na confirmação |

Decisão do fundador, 2026-08-24: **quem escreve a presença por reconhecimento é a sessão de
trabalho do aparelho**. Ela autentica sem se tornar autora — a mesma distinção que o invariante
3 exigiu no autocadastro da segunda fatia. O Guerreiro(a) **não** ganha operação de escrita na
matriz: a presença não é ato dele, é fato do encontro. `registrar_presenca` já dispensa
confirmador no modo reconhecimento e não é reescrita.

### A entrada por nick e imagem (`RF-04-29`, `RF-04-18`)

A App 01 passa a tentar primeiro `POST /v1/sessoes/guerreiro` — nick digitado, descritor gerado
no aparelho pelo módulo de biometria da fatia anterior, na mesma ordem de vivacidade e depois
descritor. Reconhecida, a sessão abre **e a presença do dia é registrada no mesmo ato**. A
fotografia continua sem sair do aparelho (`RN-04-12`).

A confirmação humana deixa de ser o único caminho e passa a ser o que o `RN-04-09` sempre disse
que ela era: a **alternativa equivalente**, para quem não tem _template_, para quem recusou a
biometria e para a falha de reconhecimento.

### Presença já registrada não duplica, e a tela avisa (`RF-04-19`)

Decisão do fundador, 2026-08-24: o núcleo **segue idempotente** — devolve o registro já gravado,
sem erro —, e é a **App 01** que percebe a presença anterior e mostra o aviso da jornada 5.4,
voltando à tela inicial. O PRD-04 §9 previa 409 para a duplicata e 200 para o reenvio da fila,
dois códigos que a mesma rota não distingue; a §9 é corrigida ao `RF-01-20` e ao PRD-01 §10, que
garantem o reenvio sem duplicar e sem erro. Não é decisão nova: é o PRD alcançando a fonte.

### A falha não revela nada, e não deixa ninguém de fora (`RF-04-20`, `RF-04-21`)

A recusa do núcleo já é indistinguível entre nick inexistente, Guerreiro(a) sem _template_ e
descritor que não confere. A tela oferece **nova tentativa** com a mesma frase em todos os
casos, e depois dela o caminho da confirmação humana — que agora **também registra a presença**,
com quem confirmou, e não apenas abre a sessão.

### O recadastro da imagem de referência (`RF-04-22`, jornada 5.5 item 3)

Captura ruim ou imagem que envelheceu: o Mestre ou o Admin recadastra a imagem a partir da
própria aplicação. `POST /v1/guerreiros/{id}/descritor` já grava e recadastra pela mesma rota, e
já audita a substituição — nada muda no núcleo.

O identificador chega **sem oráculo de nick**: a sessão aberta por confirmação presencial é quem
o revela, pelo `GET /v1/quem-sou` daquela sessão. Ninguém pergunta um nick; um adulto confirma
uma criança que está na frente dele, e a sessão diz quem ela é. É isto que dissolve o bloqueio
que a terceira fatia registrou para o `RF-04-22` e o `RF-04-16`.

## Capabilities

### New Capabilities

Nenhuma. As duas capacidades tocadas já existem e são consolidadas.

### Modified Capabilities

- `aula-e-presenca`: a presença no modo reconhecimento ganha a rota que nunca teve, escrita sob
  a sessão de trabalho da App 01 e sem confirmador; a recusa do modo passa a ser de quem
  registra, não da rota inteira.
- `aplicacao-da-aula-presencial`: a entrada do Guerreiro(a) passa a ser por nick e imagem, com a
  confirmação humana como alternativa; a presença é registrada nos dois caminhos; entra o
  recadastro da imagem de referência. Cai a restrição da primeira fatia, que vedava a entrada
  por imagem.

## Impact

**Núcleo** — `aulas/rotas.py` (o modo reconhecimento sob a chave da App 01). `aulas/regra.py`,
`biometria/` e `sessoes/` não mudam: as três regras de que esta fatia depende já estão escritas,
testadas e consolidadas.

**App 01** — a tela de entrada passa a abrir a câmera, a tratar a falha com nova tentativa e a
encaminhar à confirmação humana; a presença passa a ser registrada nos dois caminhos; nasce a
tela de recadastro da imagem. O módulo de biometria da fatia anterior é reusado sem alteração —
nenhum teste baixa modelo nem abre dispositivo.

**Documentação** — PRD-04 §9 corrige o 409 da presença duplicada; §13 recebe as duas decisões de
2026-08-24; documento 09 recebe as linhas correspondentes; `docs/prds/index.md` registra a
fatia.

**Fora desta fatia** — `RF-04-16` (captura de quem se cadastrou sem imagem, quando o responsável
comparece num encontro posterior) fica fora por **recorte**, não mais por bloqueio: o caminho do
identificador que esta fatia abre serve a ele, e o que falta é rodar a jornada 5.2 sobre um
cadastro que já existe. A **fila local sem rede** (`RF-04-23` a `RF-04-25`) é a jornada 5.6, e
esta fatia é o piso dela. Continuam fora, porque o PRD-04 §3.2 já os exclui: o anexo da
digitalização do termo e o vínculo com Guerreiro(a) já cadastrado, ambos da App 03.
