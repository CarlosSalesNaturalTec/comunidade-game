## Why

Origem: **PRD-04**, linha sem número do bloco do PRD-04 no `openspec/cronograma-de-fatias.md`
— "Entrada por reconhecimento volta a enviar a aula, e o erro de camada aparece como o que é".
Recorte: `RF-04-18`, `RF-04-20`, `RF-01-27`, `RN-04-36`.

A fatia 15 passou a exigir `aula_id` em `POST /v1/sessoes/guerreiro`, e o cliente da App 01
nunca foi atualizado. Desde aquele _merge_, **toda** tentativa de entrada por reconhecimento
responde 422, e a tela a apresenta com a frase da recusa facial — o núcleo nomeia o campo em
falta na resposta, e a aplicação o descarta. Com a primeira medição do limiar já feita em
produção, é este 422 que mantém o reconhecimento quebrado.

É a quinta vez que uma falha de camada se disfarça de rosto que não confere neste mesmo
caminho. A regra que o impede virou princípio 16 do documento 03 e invariante 25, e esta
change é a primeira a aplicá-la.

## What Changes

- A entrada por reconhecimento da App 01 passa a enviar a **aula** ao abrir a sessão, além do
  nick e do descritor — o dado já está na tela, como propriedade dela.
- A tela da entrada passa a **distinguir a recusa declarada pelo núcleo da falha de camada**:
  só a recusa da conferência recebe a frase do domínio; erro de validação, de rede e de chave
  aparecem pelo que o núcleo declarou no corpo único (`RF-01-27`).
- O tratamento de erro da entrada deixa de cobrir o que roda **depois** do reconhecimento —
  `GET /v1/eu`, o registro da presença e a abertura da sessão local. Falha ali não é recusa de
  rosto, e hoje seria apresentada como tal.
- Sem mudança de contrato no núcleo: a rota já exige a aula, e a capacidade
  `sessao-do-guerreiro` já a descreve.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: a entrada por nick e imagem passa a declarar o envio da aula
  ao núcleo, e a recusa deixa de absorver falha de camada.

## Impact

- `apps/app-01-aula-presencial/src/api/sessoesDeGuerreiro.ts` — a entrada da chamada ganha a
  aula.
- `apps/app-01-aula-presencial/src/entrada/TelaDeEntradaDoGuerreiro.tsx` — o recorte do
  tratamento de erro e a escolha da frase.
- `apps/app-01-aula-presencial/src/entrada/entrada.test.tsx` — cenários novos.
- Nada no `backend/`. Nada na App 05, que tem change própria e depende de decisão já tomada
  mas ainda não implementada.
