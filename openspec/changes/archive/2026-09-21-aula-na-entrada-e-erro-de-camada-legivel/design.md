## Context

Ver `proposal.md` — Why. O contrato do núcleo já está consolidado em
`openspec/specs/sessao-do-guerreiro/spec.md`: a rota exige nick, descritor **e a aula**. Nada
muda no `backend/`. O desenho aqui decide apenas como a tela da App 01 volta a cumprir esse
contrato e como ela separa recusa de falha.

## Goals / Non-Goals

- **Goal**: a entrada por reconhecimento envia a aula, e a tela distingue a recusa declarada
  pelo núcleo de qualquer outra falha.
- **Non-Goal**: a App 05, que tem a mesma regressão e o mesmo `catch` largo. Sai em change
  própria, porque depende de decisão de produto já tomada (limiar da comunidade, responsável
  que abre a sessão) e ainda não implementada.
- **Non-Goal**: rever a duração da sessão, a medição do limiar ou a fila de presença.

## Decisions

**1. A aula vem da tela, não de uma consulta nova.** `TelaDeEntradaDoGuerreiro` já recebe
`aulaId` como propriedade — é a aula da sessão de trabalho do aparelho, a mesma que o registro
de presença usa. Basta repassá-la.
_Alternativa descartada_: o núcleo resolver a aula vigente sozinho — tiraria da tela a única
informação que a torna verificável e mudaria contrato já consolidado.

**2. A recusa se reconhece pelo código, não pelo status.** O núcleo declara
`autenticacao_biometrica_invalida` no corpo único (`RF-01-27`); é esse código, e só ele, que
recebe a frase do domínio. Qualquer outro código, e qualquer falha que não chegue a produzir
corpo, é falha de camada.
_Alternativa descartada_: discriminar por `status === 401` — juntaria a recusa da conferência
com sessão expirada e chave recusada, que são outra coisa.

**3. Falha de camada mostra o que o núcleo declarou.** Havendo corpo único, a tela apresenta a
`mensagem` dele — é ela que nomeia o campo em falta. Não havendo corpo (rede fora, resposta
ilegível), a tela apresenta a sua própria frase de falha de comunicação. A frase de falha de
preparo da câmera, que o `RF-04-65` já exige, permanece como está.

**4. O tratamento da conferência termina na abertura da sessão.** O que roda depois —
`GET /v1/eu`, o registro da presença, a entrada na sessão local — recebe tratamento próprio,
com frase própria. É a decisão que impede a armadilha inversa: hoje, presença já gravada no
núcleo somada a uma falha na sequência apareceria como rosto que não confere.

## Risks / Trade-offs

- **A tela passa a exibir mensagem vinda do núcleo, escrita para quem opera** → o corpo único
  do `RF-01-27` já exige mensagem em linguagem simples; e a alternativa em vigor — esconder a
  causa atrás da frase do rosto — é o defeito que esta change corrige.
- **Distinguir por código cria acoplamento a uma constante do núcleo** → é o acoplamento que o
  `RF-01-27` existe para oferecer; a `comum/api` já o faz para chave e sessão.
- **O desfecho entre reconhecimento e sessão aberta ganha um estado a mais na tela** → os
  cenários do delta cobrem os dois lados, e a suíte da entrada já exercita o caminho feliz.

## Migration Plan

Não há migração: a mudança é de cliente, sem dado gravado e sem contrato novo. O reconhecimento
volta a funcionar no _deploy_ da App 01, contra o núcleo que já está em produção — a primeira
medição do limiar já foi feita. Rollback é reverter o _commit_.
