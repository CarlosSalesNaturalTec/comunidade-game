PRD-04 (App 01 — Aula presencial), **sem número de fatia**: correção de defeito preexistente,
não requisito novo — no molde de `2026-09-17-correcao-de-aulas-canceladas-e-modelos-de-biometria`.
Alcança `RF-04-64`, `RN-04-34`, `RF-04-18` e `RF-04-20`, todos já vigentes.

## Why

Na entrada por nick e imagem, quem opera lê, ao mesmo tempo e na mesma tela, duas frases que
parecem se contradizer: **"Pessoa confirmada."**, do visor, e **"Erro: Não foi possível
reconhecer…"**, da recusa do núcleo. Observado em produção em 2026-09-18.

As duas afirmações são verdadeiras e falam de coisas diferentes — a primeira é o laço de
detecção dizendo que há uma pessoa viva diante da câmera; a segunda é o núcleo dizendo que
aquele rosto não confere com o _template_ do nick. Mas a tela as apresenta como se fossem o
mesmo julgamento, e quem conduz o encontro conclui que a aplicação se contradisse.

O defeito é de estado: `TelaDeEntradaDoGuerreiro` entrega ao visor o estado do laço **cru**, e
nada o limpa quando a tentativa termina. O visor congela na última frase e sobrevive ao
desfecho. A `TelaDeCaptura` e a `TelaDeMedicaoDoLimiar`, que nasceram com máquina de estado,
já condicionam o visor ao momento da captura e não têm o defeito — só a tela de entrada, que
controla o andamento por um booleano, ficou de fora.

O custo é de confiança, e é alto agora: enquanto o limiar de comparação não for medido, **toda**
tentativa de reconhecimento recusa, e essa contradição aparece em todas elas.

## What Changes

- Na `TelaDeEntradaDoGuerreiro`, o **retorno do laço deixa de sobreviver ao desfecho** da
  tentativa: o visor só fala enquanto a captura acontece, como o `RF-04-64` já exige e como as
  outras duas telas de câmera já fazem.
- A frase da recusa do núcleo **não muda** — ela segue única e indistinguível entre as três
  causas do `RN-01-22`, e segue distinta da falha de preparo do `RF-04-65`.

Fica **fora**: o valor do limiar de comparação e onde ele mora, que são da change
`2026-09-18-limiar-medido-por-ponto-de-apoio`; e a ordem das mensagens na tela de confirmação
humana, que não tem visor.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: o Requirement "O Guerreiro(a) entra por nick e imagem, e a
  presença é registrada na entrada" ganha o cenário que prende a correção — o retorno do laço
  não sobrevive ao desfecho da tentativa. A regra já está escrita ("enquanto a captura
  acontece"); o que falta é o cenário que impede a regressão.

## Impact

- `apps/app-01-aula-presencial/src/entrada/TelaDeEntradaDoGuerreiro.tsx` — uma condição.
- `apps/app-01-aula-presencial/src/entrada/entrada.test.tsx` — o cenário novo.

Nenhuma mudança no núcleo, em `comum/` ou em `docs/`.
