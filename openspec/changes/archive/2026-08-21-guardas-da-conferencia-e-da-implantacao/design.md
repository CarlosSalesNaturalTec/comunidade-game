## Context

Ver `proposal.md` — Why. O requisito está em `specs/aplicacao-de-gestao/spec.md`.

O curto-circuito `if (!GOOGLE_CLIENT_ID) return;` já existe em
`apps/app-03-gestao/src/autenticacao/BotaoDeEntradaGoogle.tsx` desde a fatia do esqueleto, que
o registrou como "a única dependência externa em tempo de execução da aplicação". Nada o
sustenta: `entrada.test.tsx` substitui o componente inteiro por um duplo, de modo que nenhum
teste do repositório monta o componente de verdade.

## Goals / Non-Goals

**Goals:**

- Travar o comportamento que já existe, para que remover o curto-circuito quebre a suíte.
- Tirar do caminho de implantação o que muda sozinho entre duas publicações.

**Non-Goals:**

- Concluir a causa do bloqueio na GCP, que não está estabelecida.
- Mexer no fluxo de autenticação, no client ID, nas origens autorizadas ou no `firebase.json`.
- Trocar o provedor de identidade ou a forma de carregá-lo.

## Decisions

**O teste monta `BotaoDeEntradaGoogle` de verdade, e não o duplo.** Um arquivo de teste próprio
para o componente, com o client ID controlado por ambiente, conferindo que nenhum `<script>`
apontando para o provedor é acrescentado ao documento. Alternativa descartada: afrouxar o duplo
de `entrada.test.tsx` — aquele arquivo testa sessão, e o duplo ali é acertado.

**A regra da conferência à mão fica no `README.md` da App 03**, junto da seção de conferência
que a fatia anterior criou. Alternativa descartada: documento novo em `docs/` — a pasta é a
documentação do produto, e runbook não entra nela.

**A `firebase-tools` é fixada em versão exata, não em faixa.** `@latest` baixa a CLI a cada
publicação; uma faixa `^` ainda deixaria a minor mudar sem revisão. Alternativa descartada:
adicionar a CLI como dependência de desenvolvimento da raiz — engorda o `npm ci` de toda
esteira para servir só a de implantação.

**A dívida do endereço do núcleo é registrada como pendência, não corrigida aqui.** A volta
para `api.comunidadegame.org` depende do TI liberar o domínio no filtro, que é ato de terceiro.
Registrar sem prazo é o que o documento 09 existe para fazer.

## Risks / Trade-offs

**A regra da conferência sem client ID depende de quem conferir a seguir lembrar dela** → por
isso ela fica no runbook e o requisito fica na spec; o teste garante que o curto-circuito
continue existindo, ainda que a regra seja esquecida.

**Versão fixa de `firebase-tools` envelhece** → é dívida deliberada e visível no workflow, e
subir a versão passa a ser um ato revisado em vez de uma surpresa.

**Esta change não prova que evita novo bloqueio** → ela não é apresentada como correção de
causa; fecha um caminho conhecido de acesso automatizado e deixa o restante sob observação.
