# Proposal

**Origem:** PRD-04 — Aula presencial (App 01), **fatia 34** do `openspec/cronograma-de-fatias.md`
("Conservação e customizações a julgar, no encontro"). Atende `RF-04-81`, `RF-04-82`,
`RF-04-83`, `RF-04-84` (servindo o `RF-09-113`) e a jornada §5.13 do PRD-04, sob a `RN-01-66`
já vigente no núcleo. Decisão do fundador de 2026-11-12 (documento 09 §1, "Customização do kit
recebido") e decisão de 2026-11-13 sobre a mídia do último aprovado, abaixo. Depende da fatia
"Customização do kit recebido no núcleo" do PRD-01 e da fatia 31 do PRD-09, ambas implementadas.

## Why

O núcleo já julga a customização e valida a conservação do bem recebido, mas nenhuma tela faz
isso: o julgamento compara o kit real com o registro e por isso é sempre presencial, e a App 09
não tem essa fila (PRD-04 §13, decisões de 2026-11-12). Sem esta fatia, o registro da criança
nunca é julgado e a conservação (`RF-09-113`) não tem onde ser validada.

## What Changes

- **App 01 — caminho "customizações a julgar"** no grupo de quem opera, só com a sessão de
  trabalho aberta por Mestre, no molde das entregas pendentes do encontro (`RF-04-81`, §5.13.2).
- **Fila do encontro**: cada Guerreiro(a) com presença registrada na aula, por nick e avatar,
  com os bens recebidos; em cada kit aberto, o registro pendente — mídia e descrição — ao lado do
  último aprovado do kit (`RF-04-81`).
- **Julgamento**: aprovar, ou reprovar com motivo em linguagem simples (`RF-04-82`); aprovado, a
  tela confirma o ponto extra e a entrada no acervo, e a recusa do núcleo aparece como vem
  (`RF-04-83`).
- **Captura na hora**: kit aberto sem registro pendente recebe ali a foto ou o vídeo e a
  descrição da criança, por voz ou texto, em nome dela (`RF-04-82`, §5.13.3).
- **Conservação na mesma fila**: por bem recebido, o Mestre valida a conservação; no kit, a tela
  oferece conservação **ou** customização, e o bem que já pontuou no encontro não oferece nenhuma
  das duas (`RF-04-84`, `RN-01-66`, §5.13.5).
- **Núcleo — rota nova** que serve os bytes do **último aprovado** de um bem — a customização
  aprovada mais recente ou, sem ela, a comprovação do prático — ao Guerreiro(a) dono e a Mestre
  vinculado à comunidade dele. Decisão do fundador de 2026-11-13: hoje a comprovação só é servida
  ao Mestre **autor** da trilha, e quem julga no encontro é o Mestre da aula, o que deixaria o
  lado a lado do `RF-04-81` sem imagem até a segunda customização. A rota da comprovação do
  prático não muda.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `customizacao-do-kit`: o último aprovado de um bem passa a ter os bytes servidos ao
  Guerreiro(a) dono e ao Mestre vinculado à comunidade dele, pela rota do bem.
- `aplicacao-da-aula-presencial`: a App 01 apresenta a fila do cuidado do encontro, julga a
  customização, captura na hora e valida a conservação.

## Fora do escopo

- O registro e o cancelamento pela própria criança no aparelho do encontro (`RF-04-80`): fatia
  35 do PRD-04.
- O registro em casa (`RF-05-102`, `RF-05-103`): fatia 18 do PRD-05. A customização no
  portfólio (`RF-03-88`): fatia 14 do PRD-03.
- Agrupar entregas como "robô": escolha do Mestre da aula, sem suporte do núcleo (documento 09
  §1, "Customização do kit recebido").
- Conferência automática de "só o kit, sem rosto": é o Mestre quem confere ao julgar.

## Impact

- **Backend:** `backend/src/nucleo/cuidado_do_bem/` (regra e rota do arquivo do último aprovado)
  e o teste do módulo. Sem migração.
- **App 01:** `apps/app-01-aula-presencial/src/` — cliente novo em `api/`, tela nova numa pasta
  `cuidado/`, item novo no grupo de quem opera em `inicio/TelaInicial.tsx`; reúso de
  `MidiaDoNucleo`, da transcrição de fala e do envio retomável de `comum/`. Glifo novo em
  `comum/react/Icone.tsx`, se nenhum existente servir.
- **Documentação:** a linha "Customização do kit recebido" do documento 09 §1 ganha a decisão
  de 2026-11-13; a linha da fatia 34 no cronograma.
