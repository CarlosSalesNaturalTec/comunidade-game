# Design

## Context

Ver `proposal.md` — Why. O padrão do grupo de quem opera está consolidado em
`openspec/specs/aplicacao-da-aula-presencial/spec.md` (fatias 25, 26 e 31); a captura é a
`TelaDeCaptura` do onboarding, que já recebe `guerreiroId` e o token de trabalho. A fatia só
muda **de onde o recadastro parte** e **como a sessão abre**.

## Decisions

**1. O recadastro é um `CaminhoDaEntrada` novo, que abre na confirmação.**
`TelaDeEntradaDoGuerreiro` ganha `caminho="recadastro"`, cujo estado inicial é `"confirmando"`
em vez de `"entrada"`. Sem tela de reconhecimento, a sessão que chega à captura só pode ter sido
aberta por confirmação presencial, e a garantia que `viaDeEntrada` dava passa a vir da própria
rota de navegação. *Alternativa descartada:* manter `viaDeEntrada` e oferecer também o
reconhecimento, que deixaria um caminho que nunca leva à captura.

**2. Sem guarda de presença.**
`caminho === "recadastro"` não entra no ramo da `GuardaDePresenca`: com a sessão aberta, a
`TelaInicial` monta a `TelaDeCaptura` direto (decisão do fundador de 2026-11-10).

**3. A captura conclui numa tela de desfecho, não volta calada.**
Antes, `aoConcluir` voltava às equipes sem frase. Agora uma tela "Imagem recadastrada" diz que a
nova imagem foi gravada e que a anterior deixou de valer (`template-biometrico`), e a ação do
cabeçalho volta ao início pelo `voltarAoInicio`, que encerra a sessão do Guerreiro(a)
(`RF-04-28`). Nenhum desfecho termina sem frase.

**4. O recadastro entra logo depois da medição.**
Os dois são atos de biometria, raros, e a medição já abre o grupo. A cauda do grupo — chave da
troca, entregas e encerramento — não muda, e os testes que a conferem por índice seguem válidos
sem edição.

**5. Glifo novo em `comum/`.**
`recadastro`: quinas de enquadramento com um rosto dentro, no traço da grade de `24` px. Não
repete `onboarding` (pessoa com sinal de mais), que diria "cadastrar alguém novo".

## Risks / Trade-offs

- Sem a guarda, o Mestre pode recadastrar quem não registrou presença no encontro. É aceito:
  a criança precisa estar diante da câmera, e o PIN de quem abriu o aparelho é exigido no ato.
