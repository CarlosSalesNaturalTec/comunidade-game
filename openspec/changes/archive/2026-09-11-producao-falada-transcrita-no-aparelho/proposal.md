# Produção falada transcrita no aparelho

Origem: **PRD-05** (fatia sem número, `Produção falada transcrita no aparelho` — `RF-05-74`,
`RF-05-76`, `RN-05-32`). É a fatia irmã de `2026-09-11-pergunta-falada-transcrita-no-aparelho`
(fatia 13 do PRD-04, implementada), e aplica à **entrega da produção** a mesma decisão do
fundador de 2026-09-10, já gravada no documento 03 §§1.12, 7, no documento 09 §1 e nos
enunciados de `RF-05-76` e `RN-05-32`: a fala vira texto no próprio aparelho, e ao núcleo chega
texto.

## Why

As fatias 9 do PRD-04 e 7 do PRD-05 entregaram as duas portas da produção — a da equipe e a
individual — com a fala indo ao núcleo como áudio, transcrita lá pelo Gemini. O `RF-05-76` e a
`RN-05-32` já não dizem isso: dizem que o áudio **não trafega**.

1. **A proteção da criança fica mais forte.** O áudio deixa de ser recebido: não passa por
   memória de servidor, não entra em log, não existe do lado do núcleo. A promessa de
   descartá-lo depois de transcrever vira a promessa de que ele não chega.
2. **A entrega falada volta a funcionar.** As portas de IA respondem indisponibilidade por
   falta de crédito no Gemini (change `2026-09-10-chave-do-gemini-em-producao`), e sem leitura
   a entrega por áudio é recusada com 503. Transcrever no navegador destrava a fala sem
   depender de crédito de provedor.
3. **A entrega falada deixa de se perder.** Transcrita no aparelho, ela passa a valer o que a
   entrega por texto já vale: devolutiva que não vem não derruba o que a criança produziu.
4. **O custo cai.** Áudio é a entrada mais cara das três formas, e a passada multimodal que
   transcrevia e comentava junto vira uma passada de texto.

## What Changes

- **BREAKING** nas duas rotas da produção — `POST /v1/equipes/{id}/producao` e
  `POST /v1/eu/missoes/{id}/producao`: com `forma=audio`, `texto` passa a ser **obrigatório** e
  `arquivo` **recusado**. `arquivo` segue existindo, só para `forma=foto`. Não há consumidor
  externo: as duas chamadoras são as Apps 01 e 05, que mudam no mesmo PR.
- A `forma` (`texto`/`áudio`/`foto`) **já chega explícita** nas duas rotas e segue gravada como
  está — é o que mantém `áudio` distinguível de `texto` agora que as duas carregam texto. A
  linha da fatia no cronograma diz que hoje o núcleo a deduz do campo preenchido; não deduz
  desde a fatia 9 do PRD-04, e a linha é corrigida nesta change.
- A **indisponibilidade da leitura** deixa de alcançar o áudio: sem leitura a entrega falada
  grava normalmente, com a **devolutiva em branco** e **201**, como a entrega por texto. O
  **503** fica só para a foto, a única forma cuja transcrição ainda depende do modelo.
- `PortaDaProducaoDaMissao.ler` passa a tratar `áudio` como texto: o adaptador de nuvem monta
  uma passada só de texto, e o local para de simular transcrição de áudio.
- As Apps **01** e **05** transcrevem a fala pela **Web Speech API**, por `comum/fala` — o
  módulo que a fatia irmã do PRD-04 deixou em `comum/` exatamente para isto. O microfone segue
  abrindo por ação da criança e fechando ao fim da fala; nenhum áudio é gravado no aparelho.
- A transcrição aparece **no campo da produção antes do envio**, editável, e é ela que segue ao
  núcleo com `forma=audio` — o documento 09 §1 registra que o fundador aceitou isso, e que por
  causa disso a forma "áudio" passa a valer o mesmo que a forma "texto".
- Onde o navegador não oferece a API (Firefox, desligada por padrão), as duas telas **avisam** e
  mantêm as formas que não dependem dela — escrever e fotografar —, sem cair de volta no envio
  de áudio.
- O **aviso do descarte** muda nas duas telas: para o áudio, deixa de prometer descarte depois
  da leitura e passa a dizer que a gravação **não sai do aparelho**. Para a foto, segue como
  está.
- `RegistrarMedicao.tsx` da App 05, que tem a própria cópia da Web Speech API desde a fatia 2,
  passa a consumir `comum/fala`. Mesma `RN-05-32` do recorte, nenhum requisito novo: é a
  duplicação que a fatia irmã do PRD-04 já previa consolidar.

## Capabilities

### New Capabilities

Nenhuma. Nem a produção nem as telas são novas: a fatia troca **como** a produção falada chega.

### Modified Capabilities

- `producao-da-missao`: a entrega por áudio chega **em texto** nas duas portas, e `arquivo`
  passa a ser só da foto. A indisponibilidade da leitura deixa de recusar o áudio com 503 e
  passa a tratá-lo como a entrega por texto. O descarte do áudio vira garantia mais forte: ele
  não é recebido (`RF-05-74`, `RF-05-76`, `RN-05-32`, `RN-05-36`).
- `aplicacao-da-aula-presencial`: a equipe entrega a fala **transcrita no aparelho**, e a tela
  declara o que faz onde o navegador não transcreve (`RF-04-45`, `RF-04-46`, `RN-04-20`).
- `area-do-guerreiro`: a App 05 entrega a fala transcrita no aparelho, com o aviso do áudio
  mudado e o mesmo caminho onde o navegador não transcreve (`RF-05-74`, `RF-05-76`,
  `RN-05-32`).

## Fora do escopo

O que o PRD-05 §3.2 já exclui do Ciclo 01 e toca esta fatia: o **apoio escolar por assistente
de voz** (`RF-05-58` a `RF-05-70`) e o **canal de sugestões** com áudio de até 60 segundos
(`RF-05-54` a `RF-05-56`). A **leitura da foto do manuscrito** segue no Gemini, como está.

## Impact

| Área                                                             | O que muda                                       |
| ---------------------------------------------------------------- | ------------------------------------------------ |
| `backend/src/nucleo/producoes/rotas.py`                          | `arquivo` só com `forma=foto`                    |
| `backend/src/nucleo/producoes/regra.py`                           | forma única e desfecho da indisponibilidade      |
| `backend/src/nucleo/producoes/{local,nuvem}.py`                  | áudio tratado como texto; sem `inlineData` de som |
| `apps/app-01-aula-presencial/src/trilhas/EntregaDaProducao.tsx`  | fala transcrita no aparelho, transcrição editável |
| `apps/app-05-guerreiro/src/trilha/EntregaDaProducao.tsx`         | idem, com o aviso do áudio mudado                |
| `apps/app-05-guerreiro/src/coleta/RegistrarMedicao.tsx`          | passa a usar `comum/fala`                        |
| `docs/03-plataforma-e-arquitetura.md` §12.2                      | a linha da retenção do áudio da produção         |
| `openspec/cronograma-de-fatias.md`                               | a situação da fatia e a correção da linha         |

Sem migração de banco: `ProducaoDaMissao` nunca guardou foto nem áudio, e a coluna `forma`
não muda de domínio — as produções já gravadas com `forma=audio` seguem válidas.
