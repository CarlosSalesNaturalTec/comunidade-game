# Design

## Context

Ver `proposal.md` — Why. O padrão já está consolidado nos sete workflows de publicação das
Apps: `firebase-tools` em versão exata, comentário de justificativa acima da chamada e o
próprio caminho do workflow nos `paths` do gatilho. Esta change aplica esse padrão ao oitavo,
sem desenhar nada novo. Não há capability de implantação em `openspec/specs/`, e nenhum
comportamento do produto muda.

## Goals / Non-Goals

**Goals:** o deploy do núcleo deixa de mudar de comportamento entre duas execuções sem
revisão; a regra que o garante passa a existir onde um agente a lê antes de escrever o
próximo workflow.

**Non-Goals:** não se corrige o `403` da Service Usage, que é ato de console; não se altera o
que o workflow faz, apenas com que versão de CLI e por qual gatilho.

## Decisions

**A versão é `15.28.1`, a dos outros sete, não a mais recente que funcione.** Alinhar as oito
esteiras na mesma versão é o que torna o comportamento comparável entre elas, e é a versão que
publicou com sucesso no mesmo commit em que `@latest` falhou. Alternativa descartada: apurar e
fixar a versão mais nova que tolere o `403` — subir a versão é ato revisado à parte, e o alvo
aqui é tirar a surpresa, não trocá-la de lugar.

**A regra vai ao `CLAUDE.md`, não a uma spec nem a um teste.** Spec descreve comportamento do
produto, e a versão de uma CLI de implantação não é comportamento — foi por isso que a change
de 21/08 também não criou requisito para ela. Alternativa descartada: guarda automática que
varra os workflows; é o remédio mais forte, mas nenhuma esteira cobre `.github/` hoje e ela
exigiria passo ou workflow novo, então fica registrada como fora do escopo e não como dívida
silenciosa.

**Os `paths` recebem só o próprio caminho do workflow, não o `firebase.json`.** Nos sete, o
`firebase.json` no gatilho custa um build de frontend; aqui custaria build de imagem, migração
e deploy do núcleo a cada mudança em alvo alheio — dez alvos compartilham o arquivo. A
consequência disso, o rewrite do `hosting:api` que não se republica sozinho, vai ao documento
09: a saída limpa é separar aquela publicação do deploy do núcleo, desenho maior que esta
change não cabe.

## Risks / Trade-offs

**A versão fixa envelhece** → é a dívida que a decisão de 21/08 já assumiu, agora em oito
workflows em vez de sete, e visível no arquivo.

**Uma linha no `CLAUDE.md` depende de quem escreve o próximo workflow lê-la** → é o artefato
que entra no contexto de todo agente que trabalha no repositório, o que a põe antes da escrita;
a guarda automática que a tornaria dispensável está registrada como fora do escopo.

**O merge redeploya o núcleo sobre código idêntico ao que já está no ar** → `alembic upgrade
head` não reaplica a `c4e81b2a9d60`, e o serviço sobe revisão nova com a mesma imagem; é o
preço de provar a correção no próprio merge, em vez de por ato manual.
