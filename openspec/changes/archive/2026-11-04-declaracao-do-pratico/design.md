# Design

## Context

Ver `proposal.md` — Why. O que molda a abordagem é o que já existe:

| Peça | Estado hoje |
| --- | --- |
| Desafio de desbloqueio | `Missao.tipo_do_desafio_de_desbloqueio` e `Missao.desafio_de_desbloqueio_enunciado` — colunas da própria missão, não tabela |
| `declarar_desafio_de_desbloqueio` | recusa quiz sem pergunta e prático sem enunciado; redeclarar substitui |
| `DeclararDesafioDeDesbloqueioEntrada` | `extra="forbid"`, com `tipo`, `enunciado` e `perguntas` |
| Leituras que servem o desafio | `GET /v1/trilhas/minhas` (ao autor), a resposta da própria declaração e o percurso do Guerreiro(a) — `MissaoSaida`, que é a leitura pública, **não** carrega o desafio |
| As seis formas de entrega do aluno | `TipoDeProducaoDaCriacaoOriginal`, `Enum(native_enum=False, length=16)` — seis valores desde a fatia do núcleo |
| Bloco do desafio na App 09 | `DesafioDeDesbloqueio.tsx`, com rádio de tipo e campo de enunciado só no prático |

Nada disso precisa ser inventado — precisa ser estendido. As três decisões do fundador de
2026-11-04 que recortam a fatia estão nas decisões 1, 3 e 4.

## Goals / Non-Goals

**Goals:**

- Os três campos do prático declarados, recusados e lidos pelo núcleo.
- A App 09 pedindo, apresentando e reabrindo os três.

**Non-Goals:**

- A entrega da comprovação e o aviso da mídia guardada (fatia 13 do PRD-05).
- Os dois vereditos, o motivo e os 5 pontos (fatia 27) — `JulgarDesafioPraticoEntrada` não é
  tocado aqui.
- A linha do portfólio com nick e título (fatia 12 do PRD-03).
- Validar a comprovação **contra** a forma declarada: quem valida é a entrega, na fatia 13.

## Decisions

### 1. Uma forma aceita, não um conjunto

Decisão do fundador, 2026-11-04: o prático aceita **uma** das seis formas. É a leitura literal
do documento 11 §2.2 ("que forma de comprovação aceita"), e dá coluna única.

_Alternativa descartada:_ conjunto de formas, com o Guerreiro(a) escolhendo entre as aceitas —
pediria tabela ou coluna de lista e seletor de múltipla escolha, sem requisito que o peça.

### 2. Três colunas em `Missao`, ao lado do enunciado

Os três campos pertencem ao desafio, e o desafio **é** coluna da missão desde a fatia 18: o
`tipo` e o `enunciado` moram lá, e só as perguntas do quiz viraram tabela, porque são muitas.
Os três são um por missão.

_Alternativa descartada:_ tabela `desafio_de_desbloqueio` própria — migração de dado vivo e
duas gerações de leitura, sem ganho algum nesta fatia.

### 3. A forma reusa `TipoDeProducaoDaCriacaoOriginal`

As "seis formas" do documento 02 §4 são as da entrega do Guerreiro(a), e esse conjunto já tem
um enum no núcleo, com os seis valores exatos. `trilhas/modelo.py` passa a importá-lo de
`criacoes_originais/modelo.py`, que não importa `trilhas` — não há ciclo. Um vocabulário de
entrega no núcleo, não dois.

_Alternativa descartada:_ enum novo com os mesmos seis valores — duas listas para o mesmo
conjunto fechado, livres para divergir na sétima forma. Se uma fatia futura quiser um nome
neutro, renomear é barato: a coluna é VARCHAR e não há DDL a refazer.

### 4. Colunas anuláveis, exigência no contrato

Decisão do fundador, 2026-11-04: os três são obrigatórios no que for declarado de agora em
diante, e o prático antigo segue valendo até o Mestre redeclará-lo. Logo: colunas
**anuláveis**, sem _backfill_ — não há valor a inventar para prático já gravado —, e a recusa
por campo fica na **regra**, não no schema, como já acontece com `enunciado`.

_Alternativa descartada:_ colunas não-anuláveis com valor de preenchimento na migração —
inventaria critério e título em nome do Mestre, e a vitrine exibiria esse texto.

### 5. O quiz que manda os três campos é recusado, não ignorado

Os três entram em `DeclararDesafioDeDesbloqueioEntrada`, então `extra="forbid"` deixa de
alcançá-los: é a regra que recusa com 422 dizendo que não se aplicam ao quiz. Ignorar em
silêncio deixaria o Mestre achar que declarou o que não declarou.

### 6. Os três campos viajam onde o enunciado já viaja

Nenhuma rota nova: entram em `MissaoAoAutorSaida`, em `DesafioDeDesbloqueioSaida` (percurso) e
em `MissaoComDesafioDeDesbloqueioSaida`. É a lição das quatro linhas de conserto do bloco
PRD-09 do cronograma — campo gravado e não devolvido é formulário que renasce vazio.

### 7. O teto de 60 é coluna e é regra

`String(60)` na coluna e recusa com 422 na regra, dizendo o teto. Só a coluna daria erro de
banco; só a regra deixaria o banco admitir o que a regra proíbe.

## Risks / Trade-offs

- **O contrato do prático quebra para quem declara com o corpo de hoje.** → O único cliente é
  a App 09, que entra na mesma change; nenhuma outra aplicação declara desafio.
- **Práticos antigos ficam incompletos e invisíveis a quem não abre a missão.** → A tela os
  abre com os campos vazios, e a redeclaração exige os três. Varredura ou aviso em lista é
  decisão do fundador, não suposição desta fatia.
- **A forma declarada não restringe nada ainda.** → Ela só passa a valer na entrega (fatia 13);
  até lá é dado declarado e lido, e a spec não promete recusa de comprovação.
