# Design

## Context

Ver `proposal.md` — Why. O que já existe e condiciona o desenho:

- `_paginar_personas(sessao, papel=…, parametros=…)` já serve `/v1/mestres` e
  `/v1/apoiadores`: o molde da listagem paginada por papel está pronto.
- `guerreiros_vinculaveis` já recorta uma leitura de Mestre pela comunidade do vínculo
  vigente (`VinculoJogador`) — é o precedente do recorte por papel.
- `listar_responsaveis_do_guerreiro_rota` já resolve nomes em lote com `Persona.id.in_(…)`
  e já lê sob `Operacao.vinculo_com_guerreiros_e_guerreiras`, que Admin e Mestre têm.
- `Persona.criada_por` é persistido por `criar_persona`; nenhum campo novo é preciso para
  achar o que o Mestre cadastrou.
- `POST /v1/responsaveis/{id}/vinculos` já aceita qualquer responsável por identificador: a
  retomada do vínculo não precisa de rota nova.

## Goals / Non-Goals

**Goals:** uma rota de leitura com dois recortes por papel; a tela que a consome e retoma o
vínculo.

**Non-Goals:** `Operacao` nova; migração; tela na App 09 (fatia 22 do PRD-09); qualquer
escrita além do vínculo que já existe.

## Decisions

1. **`GET /v1/responsaveis`, paginada em `PaginaDeResultado` com cursor**, no molde de
   `/v1/mestres`. _Alternativa descartada:_ devolver tudo sem paginação — quebraria a
   convenção de listagem do PRD-01 já aplicada em toda a gestão.

2. **Sem `Operacao` nova: `exigir_permissao(Operacao.vinculo_com_guerreiros_e_guerreiras, "le")`.**
   Admin a tem por `Operacao.tudo`; o Mestre já a tem em leitura. É exatamente o precedente
   que `RF-13-35` registrou para `GET /v1/guerreiros/{id}/responsaveis`. _Alternativa
   descartada:_ `leitura_de_responsaveis` própria, que multiplicaria a matriz sem recortar
   nada que a regra não recorte melhor.

3. **O recorte por papel mora na regra, não na rota** — `responsaveis_visiveis(sessao, *,
   operador, parametros)`, no molde de `guerreiros_vinculaveis`. Admin: todos. Mestre:
   `vínculo vigente com Guerreiro(a) da comunidade do seu vínculo` **OU**
   `Persona.criada_por == mestre.id`. _Alternativa descartada:_ dois endpoints, um por
   papel — duplicaria contrato para uma diferença de cláusula.

4. **O ramo `criada_por` é parte do recorte, não conveniência.** Sem ele, o Mestre que
   cadastra e sai antes de vincular perde o responsável para sempre — o próprio defeito que
   a fatia corrige, reintroduzido no papel que mais cadastra em campo. Decisão do fundador,
   2026-09-26.

5. **Duas consultas em lote para os vinculados, nunca uma por responsável.** Depois de
   paginar os responsáveis: um `select` de `VinculoResponsavel` com `responsavel_id.in_(…)`
   e `fim IS NULL`, e um de `Nick` com `persona_id.in_(…)`. _Alternativa descartada:_
   chamar `guerreiros_vinculados` por responsável, que é N+1 na página inteira.

6. **A tela reaproveita o padrão de `ListaDeAdultos`** — `Tabela` de `comum/react`, colunas
   com `recolhida` para o que não cabe no celular. _Alternativa descartada:_ layout próprio,
   que destoaria das sub-áreas vizinhas.

7. **A retomada do vínculo reusa o passo de vínculo do `FormularioDeResponsavel`**, que
   passa a aceitar um responsável já existente em vez de sempre nascer do cadastro. A tela
   já trata a recusa do teto de três; esse tratamento segue valendo na retomada. _Alternativa
   descartada:_ formulário separado, que duplicaria a mensagem do teto e o seletor.

8. **Guerreiro(a) sem nick gravado** aparece com a ausência sinalizada, como a coluna Nick
   de `ListaDeAdultos` já faz — a linha nunca some.

## Risks / Trade-offs

- [O Mestre passa a ler nome de responsável que antes não alcançava em lista] → o recorte da
  decisão 3 o limita às comunidades em que atua mais o que ele mesmo cadastrou; a resposta
  não traz credencial nem contato, e o cenário de 403 para os demais papéis é coberto por
  teste.
- [A rota nasce autorizada ao Mestre sem tela que a consuma] → é o preço da opção A escolhida
  pelo fundador: a regra fica decidida de uma vez e a fatia 22 do PRD-09 fica visível no
  cronograma em vez de virar dívida. A cobertura de teste do recorte do Mestre entra agora.
- [`VinculoJogador` do Mestre pode estar ausente] → Mestre sem vínculo vigente recai no ramo
  `criada_por` apenas, como `guerreiros_vinculaveis` já trata a ausência devolvendo vazio.
