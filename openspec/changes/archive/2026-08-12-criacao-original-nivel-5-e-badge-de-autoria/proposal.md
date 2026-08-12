## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Sétima fatia, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-01-26`, `RN-01-13`, `RF-01-21` (parcial — a parte de nível 5 e
badge de autoria).

A sexta fatia entregou o motor de pontuação, mas adiou o nível 5 e o badge de autoria por
dependerem de "culminância validada" (documento 11 §6), que ela leu como entidade do PRD-09
ainda inexistente. Olhando o próprio modelo de dados que o PRD-09 declara (§8), `Culminancia`
não tem campo de situação — quem carrega "entregue, validada, devolvida" é `CriacaoOriginal`,
entidade do PRD-01 (`RF-01-26`). "Culminância validada" do documento 11 §6 se resolve, então,
com `CriacaoOriginal.situacao == validada`, sem esperar a fatia de PRD-09. Esta fatia entrega a
criação original que faltava desde a quinta fatia — "toda trilha termina em criação original"
— e fecha, de quebra, o nível 5 e o badge de autoria que o documento 11 já descreve.

## What Changes

- Nasce a **Criação Original**: o Guerreiro(a) entrega, contra uma trilha, o que produziu a
  partir do que aprendeu — a mesma permissão que o PRD-01 §4 já lista ("Guerreiro(a) escreve:
  ... suas criações"). Autoria individual nesta fatia (`RF-01-26`).
- O **Mestre autor da trilha** (ou Admin) valida ou devolve a entrega, pela mesma conferência de
  posse já usada em trilha, missão, atividade e resultado (`conferir_posse_da_trilha`).
- **Autoria nunca se perde**: devolver para ajuste muda a situação, não o autor do registro
  (`RN-01-13`).
- Ao **validar**, o núcleo credita, na mesma operação:
  - 50 pontos regulares, integrais, na trilha da criação (documento 11 §5);
  - o badge **de autoria** (documento 11 §7) — novo valor em `TipoDeBadge`;
  - o **nível 5 — Mestre Aprendiz** (documento 11 §6), se ainda não certificado.
- Devolver não credita nada — nem ponto, nem badge, nem nível.

### O que esta fatia não tem, e não é omissão

- **`Culminancia`** — a declaração prévia do que se espera e o critério de validação — tem os
  atributos definidos no PRD-09 (PRD-01 §8, PRD-09 §8). O Mestre valida por julgamento próprio;
  o critério formal pré-declarado chega com o PRD-09.
- **`RecompensaDeMarco`** — mesma razão: atributos do PRD-09.
- **Crédito em equipe.** O documento 11 §5 credita os 50 pontos "integrais a cada integrante" —
  regra que só faz sentido plena com `Equipe`, que ainda não existe no núcleo (`RF-01-37` a
  `RF-01-39`, mesma lacuna que `Resultado` já deixou registrada na sexta fatia). Aqui, o único
  integrante — o próprio Guerreiro(a) — recebe os 50 pontos inteiros.
- **Rota de leitura pública/portfólio.** A vitrine que expõe a criação original publicamente
  fica travada pela pendência "Números da proteção das rotas públicas" do documento 09, como já
  valia para `RF-01-33`/`RF-01-34` desde a quarta fatia.
- **Motivo de devolução como campo estruturado.** `RF-01-26` exige só a persistência com
  autoria; o fluxo de "recusa com motivo, devolvendo para ajuste" (`RF-09-34`) é do PRD-09.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação, cadência de
coleta e valoração de aporte (a régua já é do documento 11, aplicada aqui, não inventada);
captura da imagem, conversa de cadastro e geração do descritor no aparelho; exclusão do
_template_; telemetria da Batalha de Laser e personalização por IA.

## Capabilities

### New Capabilities

- `criacao-original`: o registro de que um Guerreiro(a) entregou uma criação original contra
  uma trilha, com autoria permanente, e o Mestre autor validando ou devolvendo a entrega.

### Modified Capabilities

- `pontos-niveis-e-badges`: acrescenta o crédito de 50 pontos regulares ao validar uma criação
  original, o novo valor de badge **de autoria**, e o critério do nível 5 — Mestre Aprendiz.

## Impact

- `backend/src/nucleo/`: módulo novo `criacoes_originais/` (entidade e regra de entrega e
  validação), lendo `trilha` e `persona` já existentes; `pontuacao/modelo.py` e
  `pontuacao/regra.py` ganham o valor `de_autoria` em `TipoDeBadge` e a certificação do nível 5.
- `backend/alembic/`: migração para `criacao_original` e para o novo valor de `TipoDeBadge`.
- Nenhuma rota nova sob `/v1`: como a quinta e a sexta fatias, esta entrega entidade e regra de
  crédito, não rota de gestão — a rota de entrega e a de validação são das aplicações de gestão
  (PRD-02, PRD-09, PRD-05), que ainda não têm o seu turno na esteira de construção.
- `docs/`: nenhuma decisão nova nesta fatia — a régua de pontos, níveis e badges já está no
  documento 11 §§5–7. `docs/prds/index.md` recebe a situação atualizada se ela mudar ao fim da
  implementação.
