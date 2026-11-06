# Proposal

## Why

Correção da **fatia 13 do PRD-05** (`2026-11-04-entrega-da-comprovacao-do-pratico`), sem
requisito novo: atende de novo `RF-05-91`, `RF-05-92`, `RF-05-93`, `RN-05-51` e `RF-04-76`, que
a fatia declarou implementados e que **não chegam à tela**. Relatado pelo fundador em
2026-11-06, com a missão "Montador Iniciante" (Robô Educa) já redeclarada com forma **imagem** e
critério de aceite.

`GET /v1/eu/trilhas/{id}/missoes/{ordem}` serve o desafio com `forma_de_comprovacao`,
`criterio_de_aceite` e `titulo_curto` (`DesafioDeDesbloqueioSaida`), mas
`comum/trilha/api.ts` e `comum/trilha/DesafioDeDesbloqueio.tsx` leem
`desafio_pratico_forma_de_comprovacao` e `desafio_pratico_criterio_de_aceite` — os nomes da
leitura do **Mestre** (`MissaoSaida`). A forma chega sempre ausente, o `?? null` a trata como
prático antigo e a tela, nas **Apps 01 e 05**, oferece só "Já cumpri!": sem critério, sem aviso,
sem campo de arquivo e sem a alternativa de entregar no encontro. A suíte ficou verde porque o
teste do núcleo afirma os nomes curtos e os testes das telas simulam a resposta com os longos.

Consequência no dado: toda declaração de prático em mídia feita desde 2026-11-04 nasceu **sem
arquivo** e aguarda o Mestre sem nada a julgar; a bancada da App 09 diz "O envio do arquivo
ainda não concluiu." e a tela da criança mostra "O que você entregou" vazio, sem caminho para
enviar.

## What Changes

- **A tela do Guerreiro(a) lê os nomes que o núcleo serve**: a interface `DesafioDeDesbloqueio`
  de `comum/trilha/api.ts` e o componente passam a `forma_de_comprovacao`,
  `criterio_de_aceite` e `titulo_curto`. O núcleo não muda. (`RF-05-91`, `RF-05-92`,
  `RF-04-76`)
- **Contrato fixado dos dois lados**: um exemplo da resposta do percurso, gravado uma vez em
  `comum/`, é conferido pelo teste do núcleo contra a resposta real e usado pelos testes das
  telas — diferença de nome passa a quebrar teste. (`RF-05-91`)
- **Declaração em mídia que ficou sem arquivo recebe o arquivo**: enquanto o Mestre não julga,
  a tela da criança oferece enviar o arquivo que não chegou, pela sessão de envio que o núcleo
  já aceita nesse estado — é a "retomada sem perder a declaração" do `RF-05-91`, e recupera as
  declarações do período do defeito sem o Mestre recusar ninguém. (`RF-05-91`, `RF-05-93`)
- **A bancada da App 09 diz a verdade sobre a declaração sem comprovação**: distingue o prático
  sem forma declarada (nada foi pedido) da mídia cujo arquivo não chegou, e nunca afirma envio
  em andamento que não existe. (`RF-09-132`, `RF-05-93`)
- **Tela da criança sem título vazio**: "O que você entregou" só aparece quando há o que
  apresentar. (`RF-05-93`)

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `desbloqueio-da-missao`: a leitura do percurso fixa os nomes dos três campos do prático.
- `area-do-guerreiro`: a declaração em mídia sem arquivo, ainda não julgada, oferece o envio.
- `area-do-mestre`: a bancada diz o que falta na declaração sem texto nem arquivo.

`aplicacao-da-aula-presencial` não muda: a App 01 consome o mesmo componente e a spec dela já
exige o comportamento da App 05.

## Impact

- `comum/trilha/api.ts`, `comum/trilha/DesafioDeDesbloqueio.tsx` e um exemplo de contrato em
  `comum/contratos/`.
- Testes: `comum/trilha/trilha.test.tsx`, `apps/app-01-aula-presencial/src/trilhas/trilhas.test.tsx`,
  `apps/app-05-guerreiro/src/trilha/{DesafioDeDesbloqueio,Missao,Sondagem}.test.tsx`,
  `backend/tests/test_desbloqueio_da_missao.py`.
- `apps/app-09-mestre/src/turmas/TelaDeDesbloqueiosPendentes.tsx`.
- `.github/workflows/backend-ci.yml`: passa a disparar também por `comum/contratos/**`.
- Núcleo, rotas e migração: nada.

## Fora do escopo

- Renomear os campos na leitura do Mestre (`MissaoSaida`) ou no núcleo.
- Tornar obrigatória a forma no prático antigo (`RN-09-50` segue valendo).
- Tudo o que o PRD-05 §3.2 já exclui.
