## Why

Origem: **PRD-05**, linha sem número do bloco do PRD-05 no `openspec/cronograma-de-fatias.md`
— "Entrada da Área do Guerreiro(a) fora do encontro". Recorte: `RF-05-01` a `RF-05-04`,
`RN-05-01`, `RN-05-02`, `RN-05-48`, `RF-01-12`.

A App 05 é usada em casa, entre as aulas. Hoje **não há entrada alguma ali**: o reconhecimento
responde 422 pelo mesmo defeito que quebrou a App 01, e a sessão assistida exige um Mestre ou
Admin se autenticando com Google no aparelho da criança — o que em casa não existe. Não é
degradação de experiência, é porta trancada.

O núcleo passa a reconhecer fora do encontro e a aceitar o responsável como confirmador na
fatia anterior. Esta leva isso à tela.

## What Changes

- A entrada por reconhecimento da App 05 abre a sessão **sem aula** — ali não há encontro, e o
  limiar vem da comunidade do Guerreiro(a).
- A sessão assistida passa a ser do **responsável**, que entra por **login social ou usuário e
  senha**. Oferecer apenas um dos dois trancaria fora quem tem o outro.
- A **troca de senha provisória** é resolvida no mesmo fluxo: o primeiro uso da credencial do
  responsável costuma ser justamente o resgate do filho, e hoje terminaria em beco sem saída.
- Mestre e Admin continuam abrindo a sessão quando estão presentes; o caminho não se estreita,
  se alarga.
- O tratamento largo de erro da entrada recebe a mesma correção feita na App 01: falha de camada
  deixa de ser apresentada como rosto que não confere.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `area-do-guerreiro`: a entrada passa a valer fora do encontro, a sessão assistida admite o
  responsável com os dois caminhos de login e a senha provisória, e a recusa deixa de absorver
  falha de camada.

## Impact

- `apps/app-05-guerreiro/src/api/sessoesDeGuerreiro.ts` — a chamada da conferência.
- `apps/app-05-guerreiro/src/entrada/TelaDeEntradaDoGuerreiro.tsx` — o recorte do tratamento de
  erro e a escolha da frase.
- `apps/app-05-guerreiro/src/entrada/ConfirmacaoAssistida.tsx` — os dois caminhos de login do
  responsável, a troca de senha provisória e o texto da tela.
- `apps/app-05-guerreiro/src/entrada/entrada.test.tsx` — cenários novos.
- Nada no `backend/`: a fatia anterior entrega tudo o que esta consome, e precisa entrar antes.
