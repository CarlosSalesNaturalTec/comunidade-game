# Desenho

## Context

A fatia é inteira da App 09. O núcleo já entrega tudo o que ela precisa: `GET /trilhas/minhas`
devolve, por trilha, as missões com `etapa_do_ciclo`, `e_sondagem` e os `desafios_de_coleta`
aninhados, e a trilha com a `culminancia` — os três sinais das travas de publicação. As três
travas em si estão em `openspec/specs/trilha-e-missao/spec.md`, no requisito da publicação, e
o bloco recolhível é o padrão consolidado da fatia transversal de 2026-09-07.

Ver `proposal.md` — Why, para a motivação, e o delta de `specs/area-do-mestre/` para os
requisitos.

## Goals / Non-Goals

**Goals:**

- Paginar as missões por etapa do ciclo sem inventar rota, campo ou migração.
- Dar ao Mestre, a qualquer momento, a leitura do que ainda falta para publicar.
- Fixar a ordem dos blocos da missão onde ela não se perca — na spec consolidada.

**Non-Goals:**

- Qualquer escrita ou leitura nova no núcleo.
- A recusa por falta de etiqueta ODS (`RF-09-96`, `RF-09-97`): Ciclo 02.
- Reordenar os blocos da **trilha** (ODS da trilha, cobertura, culminância). A decisão do
  fundador é sobre os blocos da missão.

## Decisions

1. **O painel de pendências deriva no cliente, do payload que a tela já tem.** As três travas
   se leem de `missao.e_sondagem`, dos `desafios_de_coleta` das missões e de `trilha.culminancia`.
   _Alternativa descartada:_ campo `pendencias_de_publicacao` em `TrilhaDoMestreSaida`,
   reaproveitando `_travas_de_publicacao_pendentes` do núcleo — mantém a regra em fonte única,
   mas envelhece no instante seguinte: a tela atualiza a trilha em estado local a cada
   declaração, sem refetch, e o campo do servidor só se renovaria com uma ida à rede por
   declaração. O precedente é da própria tela: `coberturaDaTrilha` já é recalculada no cliente
   "a cada confirmação para a tela acompanhar o que o Mestre acabou de declarar".
2. **O painel é checklist, não porteiro.** Ele não desabilita o botão de publicar. Quem recusa
   segue sendo o núcleo, com a mensagem dele (`RF-09-08`). Assim a regra do cliente pode estar
   errada sem nunca bloquear o Mestre — o pior caso é um painel desatualizado, não uma trilha
   impublicável.
3. **A paginação é de apresentação: as quatro etapas são fixas e todas aparecem.** Agrupa-se
   `trilha.missoes` por `etapa_do_ciclo` na `TelaDaTrilha`, que passa à `ListaDeMissoes` só as
   missões da etapa aberta. _Alternativa descartada:_ a `ListaDeMissoes` paginar sozinha —
   quem escolhe a etapa aberta é a tela, e a lista continua recebendo o que deve desenhar.
   Etapa vazia continua visível para o Mestre ver que ela existe e está por preencher.
4. **A nova missão nasce na etapa aberta.** Sem isso, a missão criada na página de marcos
   desapareceria para abertura, que é o padrão fixo de hoje no formulário. O Mestre continua
   podendo alterar a etapa antes de confirmar.
5. **O painel é da trilha, não da etapa.** A sondagem que falta aparece com qualquer etapa
   aberta — a trava é da trilha inteira, e escondê-la atrás da paginação recriaria, dentro da
   tela, o problema que a fatia veio resolver.
6. **A ordem dos blocos é movimentação de JSX.** Os `useState` de formulário aberto e o
   `gravadoEm` são do componente `ListaDeMissoes`, não dos blocos: mover os blocos não os
   toca, e nenhum bloco muda de props ou de comportamento.

## Risks / Trade-offs

- **A regra das três travas passa a existir em dois lugares — núcleo e tela.** → Mitigação: a
  decisão 2 garante que a cópia do cliente nunca decide nada; a spec de `area-do-mestre` nomeia
  as três travas, de modo que uma quarta trava no núcleo é mudança de spec que atravessa os
  dois lados; e o teste do painel fica ao lado do teste da recusa, no mesmo arquivo.
- **A paginação pode fazer o Mestre perder de vista uma missão.** → Mitigação: as quatro etapas
  aparecem sempre, inclusive as vazias, e a contagem de missões de cada uma fica visível na
  própria navegação entre etapas.
- **Reordenar blocos costuma quebrar teste que depende de índice.** → Mitigação: os testes de
  `trilhas.test.tsx` alcançam cada bloco por nome (`findByText("Conteúdo")`), nunca por posição;
  conferido antes de escrever esta change.
