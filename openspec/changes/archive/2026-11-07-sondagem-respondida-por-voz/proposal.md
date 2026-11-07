# Sondagem respondida por voz

Origem: **PRD-05**, fatia **15** do `openspec/cronograma-de-fatias.md` (aberta nesta change), com
alcance no **PRD-04** pela mesma tela no aparelho do encontro. Identificadores **novos**, criados
na revisão dos dois PRDs nesta change: `RF-05-97`, `RF-05-98`, `RN-05-54`, `RN-05-55` e
`RF-04-77`; alcança `RF-05-72`, `RF-05-73`, `RN-05-34`, `RN-05-46`, `RN-05-47` e `RF-04-73`.
Aplica a decisão do fundador de 2026-11-07, elicitada em `/opsx:propose` e registrada nesta change
no documento 03 §§1.12 e 4, no documento 09 §1 e nos PRDs 04 e 05.

## Why

A narração já fala o enunciado e as alternativas da sondagem, mas quem ainda não lê precisa
voltar a ler para tocar a alternativa: ouvir sem poder responder falando deixa a camada pela
metade justamente na primeira missão de toda trilha. A sondagem é o lugar certo para começar —
não define nível (`RN-05-34`) e abre a trilha ao ser respondida, nunca ao ser acertada
(`RN-05-46`) —, então errar a ligação da fala com a alternativa não custa nada à criança.

## What Changes

- **Só na sondagem**, com o **áudio ligado**: terminada a fala da pergunta e das alternativas, o
  microfone abre por **5 segundos**, com uma barra de progresso visível e a transcrição aparecendo
  na tela enquanto dura. Ao fim, a resposta é marcada e a sondagem avança; na última pergunta, a
  sondagem é submetida sozinha (`RF-05-97`, `RF-04-77`).
- A frase falada é ligada à **alternativa aproximada**. Silêncio ou fala que não bate com nenhuma
  alternativa segue como **transcrição literal**, resposta sem alternativa (`RF-05-98`).
- Desligado o áudio, a sondagem fica **exatamente como está**, por toque. O desafio de desbloqueio
  e o Quiz ao Vivo não mudam (`RN-05-54`).
- **Ligar o áudio pede a permissão do microfone**, nesse toque; o microfone só capta na janela de
  5 segundos e fecha em seguida — a aplicação continua sem escutar a aula (`RN-05-54`).
- A transcrição usa a **Web Speech API** (`SpeechRecognition`, já em `comum/fala/`); no Chrome ela
  é feita nos serviços do Google, o que o fundador aceitou. `SpeechSynthesisUtterance` segue
  sendo só a voz que fala.
- **BREAKING** no corpo de `POST` da submissão do desafio de desbloqueio: cada resposta passa a
  aceitar `alternativa_escolhida` **nula** com `resposta_falada` (texto), **só em missão de
  sondagem**; conta como não acertada e é gravada no histórico (`RF-05-98`, `RN-05-55`,
  `RN-05-47`). A única chamadora é `comum/trilha`, que muda no mesmo PR.

## Capabilities

### New Capabilities

- `sondagem-por-voz`: a janela de escuta após a narração da pergunta da sondagem — abertura do
  microfone, barra de 5 s, transcrição à vista, ligação à alternativa aproximada e envio
  automático, nas Apps 01 e 05.

### Modified Capabilities

- `desbloqueio-da-missao`: a resposta da sondagem aceita transcrição sem alternativa, gravada como
  não acertada (`RF-05-98`, `RN-05-55`).
- `narracao-por-sintese-de-fala`: a camada avisa quando a fala termina, e ligar o áudio passa a
  pedir a permissão do microfone (`RF-05-97`, `RN-05-54`).
- `area-do-guerreiro`: a sondagem da App 05 é respondida por voz com o áudio ligado (`RF-05-97`).
- `aplicacao-da-aula-presencial`: idem no aparelho do encontro, e o microfone passa a abrir também
  na janela da sondagem, além do assistente (`RF-04-77`).

## Fora do escopo

- Responder por voz o desafio de desbloqueio, o Quiz ao Vivo ou qualquer outro quiz.
- Leitura das respostas da sondagem pelo Mestre: o histórico é gravado, não lido (`RN-05-47`).
- O prazo de guarda da transcrição da sondagem: fica como pendência no documento 09 §1.

## Impact

| Área                                               | O que muda                                                  |
| -------------------------------------------------- | ----------------------------------------------------------- |
| `comum/fala/`                                      | janela de escuta com prazo, resultado parcial e permissão   |
| `comum/narracao/`                                  | `narrar` avisa o fim da fala; ligar o áudio pede o microfone |
| `comum/trilha/`                                    | `Sondagem`, `DesafioDeDesbloqueio`, `api.ts` e ligação      |
| `backend/src/nucleo/trilhas/{rotas,regra,modelo}.py` | resposta falada na sondagem                                |
| `backend/alembic/versions/`                        | `alternativa_escolhida` nulável e `resposta_falada`         |
| `docs/03-*`, `docs/09-*`, PRD-04, PRD-05, doc 99 §8 | registro da decisão e dos identificadores novos           |
| `openspec/cronograma-de-fatias.md`                 | linha da fatia 15 do PRD-05                                 |
