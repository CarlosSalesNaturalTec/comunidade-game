# Proposal

Origem: **PRD-04**, fatia **29** do `openspec/cronograma-de-fatias.md` — _O ato da missão só
depois de todos os conteúdos_. Alcança `RF-04-73`, `RF-05-11`, `RF-05-13`, `RF-05-14` e
`RF-05-89`, **sem identificador novo**: visibilidade e ordem de ato na tela é apresentação, que
nenhum enunciado fixa — mesmo precedente das fatias 25, 26, 27 e 28.

A fatia **não estava** no cronograma, cujo bloco do PRD-04 parava na 28. O recorte é decisão do
fundador de **2026-10-16**, e a linha da fatia 29 entra no cronograma nesta mesma change.

## Why

O ato da missão — a sondagem ou o desafio de desbloqueio — é apresentado **sem gate nenhum**,
abaixo da sequência dos conteúdos. A criança vê o quiz desde o primeiro conteúdo, antes de ler
o que a missão tem a ensinar, e a Arena de "uma decisão por tela" (documento 15 §6) passa a
oferecer duas: continuar lendo ou responder já.

Contraria o propósito do desbloqueio, que é aferir o que a missão ensinou: responder antes de
percorrer o conteúdo transforma o corte de 60% (`RN-05-45`) em sorteio, e o `RF-04-73` pede o
ato no aparelho do encontro, não o ato antes da leitura.

## What Changes

- O **desafio de desbloqueio** e a **sondagem** passam a aparecer **somente depois** que o
  Guerreiro(a) alcança o **último conteúdo** da missão. Antes disso ficam ocultos.
- Missão **sem conteúdo algum** apresenta o ato **direto** — sem essa borda a missão travaria,
  e ela alcança em cheio a sondagem, que costuma não ter conteúdo e é justamente a que abre a
  trilha (`RF-05-72`).
- Missão com **um único** conteúdo já entra no último: o ato aparece junto dele, como hoje.
- O índice do conteúdo da vez **sobe** do `SequenciaPaginada` para quem decide renderizar o
  ato, pelas propriedades `indice`/`aoIrPara` que o paginador **já** oferece e que o
  `DesafioDeDesbloqueio` já usa nas perguntas. `comum/react` **não é tocado**.

Fora do escopo, por decisão do fundador de 2026-10-16:

- A **navegação dos conteúdos não muda**: nada de estado "concluído" ao fim da sequência, de
  botão "Rever conteúdo" nem de ocultar os conteúdos já vistos.
- O **aviso da recompensa de marco** ao desbloquear (`RF-05-45`) fica fora, e não vira fatia.
- A **entrega da produção** da App 05 **não** entra no gate: ela aparece em missão já
  `desbloqueada`, estado distinto daquele em que o ato existe. Gatilhá-la seria decisão nova.

Nada em `docs/` muda. O documento 15 §6.4 e o `NEVER SHALL` das duas specs — "no último
conteúdo NEVER SHALL oferecer avançar para lugar nenhum" — seguem **intactos**: o último
conteúdo continua sendo o fim da linha; o que muda é que é nele que o ato aparece.

## Capabilities

### New Capabilities

Nenhuma. A fatia condiciona comportamento que as duas capacidades já descrevem.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: o requisito _A tela da missão apresenta quatro grupos
  separados por linha muda_ fixa **onde** o ato aparece ("no mesmo grupo do conteúdo, acima da
  primeira linha") e nada diz sobre **quando**. Passa a declarar o gate e as duas bordas.
- `area-do-guerreiro`: o requisito _A tela da missão agrupa o conteúdo, o que se lê depois e o
  rodapé_ tem a mesma lacuna, e recebe o mesmo gate — com a ressalva explícita de que a
  **entrega da produção**, que aquele enunciado também lista como ato, **permanece sem gate**.

## Impact

- `comum/trilha/Missao.tsx` — o único arquivo de produção alterado.
- `comum/trilha/trilha.test.tsx` — cenários do gate e das duas bordas.
- `comum/react/SequenciaPaginada.tsx` — **não é tocado**, e com ele o quiz do desbloqueio e o
  conteúdo do dia da programação (`TelaDaProgramacao.tsx`) seguem como estão.
- Alcança as **Apps 01 e 05 juntas**, porque `comum/trilha` é compartilhada desde a fatia 21 —
  precedente das fatias 22, 27 e 28: a mesma criança não vê telas diferentes na aula e em casa.
- Nada no backend, nenhuma rota nova, nenhum glifo novo, nada em `docs/` nem no `mkdocs.yml`.
- `openspec/cronograma-de-fatias.md` — a linha da fatia 29 nasce aqui.
