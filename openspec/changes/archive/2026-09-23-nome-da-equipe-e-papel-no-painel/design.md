# Design

## Context

A equipe já existe em `openspec/specs/equipe/` e o painel em `openspec/specs/painel-do-dia/`;
esta fatia acrescenta um campo e uma rota, sem padrão novo. O que muda por quê está na proposta;
o comportamento, nos deltas. Três pontos vieram do fundador na elicitação (proposta, "What
Changes"): comparação sem caixa e sem espaços, troca travada com a composição e "Equipe N" nas
equipes existentes.

## Goals / Non-Goals

**Goals:** nome gravado, validado e único no núcleo; uma rota de troca; o nome nas leituras
que o App 01 e o painel já fazem; o papel de cada integrante na saída do painel.

**Non-Goals:** tela inicial, exigência de presença para formar equipe (fatia 18); nome na
condução do quiz e na App 05.

## Decisions

1. **Coluna `equipe.nome`, `String(20)`, `NOT NULL`, gravada aparada.** A regra de tamanho
   (1 a 20 depois de aparar) mora numa função só de `equipes/regra.py`, chamada na criação e na
   troca, e recusa com `ErroDeValidacao(campo="nome")` — o 422 do corpo único do PRD-01. A
   entrada Pydantic declara `nome: str` sem `max_length`, para que a mensagem venha da regra, em
   português, e não do validador genérico.
   - Descartado: `CHECK` de tamanho no banco — o `String(20)` já barra o excesso, e o vazio
     aparado é regra de negócio.
2. **Unicidade conferida na regra e garantida por dois índices únicos parciais sobre
   `lower(nome)`:** `(aula_id, lower(nome)) WHERE aula_id IS NOT NULL` e
   `(trilha_id, lower(nome)) WHERE trilha_id IS NOT NULL`, declarados no modelo com `Index` e
   `func.lower`, no padrão de `uq_nick_valor`. A regra consulta antes de gravar, para responder
   422 com a frase do domínio; o índice é a trava contra dois aparelhos criando o mesmo nome no
   mesmo instante. Como o nome é gravado aparado, `lower` basta para "sem caixa e sem espaços".
   - Descartado: só a consulta na regra — deixa a corrida aberta; só o índice — a colisão viraria
     erro de banco, sem a frase do domínio.
3. **Troca por `PATCH /v1/equipes/{id}` com corpo `{"nome": ...}`**, sob a operação
   `equipe_que_forma_na_aula`/`escreve`, a mesma das demais escritas de composição. A regra
   `renomear_equipe` confere, nesta ordem: Admin ou Mestre → 403; não integrante → 403; trava
   da composição → reaproveita `_confirmar_equipe_aberta` (aula encerrada, trilha homologada) →
   422; tamanho e unicidade, excluindo a própria equipe da consulta → 422. Devolve `EquipeSaida`.
4. **`nome` entra em `EquipeSaida`**, e com isso chega a todas as leituras que já a usam
   (`GET /v1/aulas/{id}/equipes`, `/v1/eu/equipes`, `/v1/eu/trilhas/{id}/equipe`). Não é dado
   pessoal: é texto que a própria equipe escolheu.
5. **Painel:** `EquipeDoPainelSaida` ganha `nome`, e os integrantes passam de
   `AvatarENickSaida` a `IntegranteDoPainelSaida(AvatarENickSaida)` com `papel: str | None`,
   lido de `IntegranteDaEquipe.papel` — o mesmo desenho de `IntegranteSaida` em
   `equipes/rotas.py`.
6. **Migração:** adiciona a coluna anulável, preenche `"Equipe " || row_number()` particionado
   por `coalesce(aula_id, trilha_id)` e ordenado por `registrado_em, id`, passa a `NOT NULL` e
   cria os dois índices. Nomes gerados assim não colidem dentro da mesma aula ou trilha. O
   `downgrade` apaga índices e coluna.
7. **App 01:** `criarEquipe` e `criarEquipeDaTrilha` recebem `nome`; nova `renomearEquipe`.
   `TelaDeEquipes` ganha o campo "Nome da equipe" acima de "Criar equipe", com o botão
   desabilitado enquanto o nome aparado estiver vazio, e o `<input>` limitado a 20 caracteres;
   cada equipe mostra o nome como título do item, e as que o Guerreiro(a) integra ganham
   "Trocar o nome", que abre o campo no próprio item. `EquipeDaTrilha` faz o mesmo, sem a troca
   depois da homologação. O limite de 20 no campo pede `maxLength` opcional em
   `comum/react/Campo` — acréscimo retrocompatível.
8. **App 03:** o item da equipe no painel troca `nomeDaEquipe` (nicks juntados) pelo
   `equipe.nome`, seguido da lista de integrantes em "nick — papel", só "nick" quando não há
   papel.

## Risks / Trade-offs

- [O App 01 em cache chama a criação sem `nome` depois do deploy do núcleo] → recebe 422 com a
  frase "a equipe precisa de nome"; o PWA atualiza no recarregamento. Núcleo e App 01 saem no
  mesmo PR e no mesmo deploy.
- [Corrida entre dois aparelhos com o mesmo nome] → o índice recusa o segundo; a resposta é o
  erro de integridade do banco, e não a frase do domínio. Aceito: exige o mesmo nome na mesma
  aula no mesmo instante.

## Migration Plan

`alembic upgrade head` no deploy, antes do tráfego novo. Rollback: `alembic downgrade -1`
remove a coluna; o App 01 anterior volta a funcionar, porque não envia nem lê o nome.
