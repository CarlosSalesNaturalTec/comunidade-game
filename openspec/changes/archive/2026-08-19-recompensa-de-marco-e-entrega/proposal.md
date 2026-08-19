## Why

Décima fatia do **PRD-07**. O livro-razão já tem duas saídas de recurso construídas — a baixa
da reserva na aula realizada e a troca por recompensa avulsa. Falta a terceira, e é a única
que a criança conquista sem pagar nada: a **recompensa de marco** — o livro da linha Alpha, a
camisa e o kit em MDF —, entregue quando o Guerreiro(a) alcança um marco da trilha, com
**baixa definitiva** no livro-razão (`RF-07-13`, `RN-07-08`, `RN-07-14`).

Fechá-la esgota o que resta de essencial e desimpedido no PRD-07: sobram apenas a conferência
de inventário (`RF-07-20`, desejável) e o bloco do desafio extra, travado pela entidade
`DesafioExtra`, cujo ciclo de vida é do PRD-09 e do PRD-14.

A fatia também quita, de passagem, o núcleo de autoria de recompensa do PRD-09 (`RF-09-71`,
`RF-09-76`) e a escrita que o PRD-02 atribuía ao Admin (`RF-02-50`, `RF-02-51`).

## What Changes

### Entidades novas

- **`RecompensaDeMarco`** — declarada pelo Mestre autor na sua trilha: marco, tipo de recurso,
  quantidade (`RF-09-71`). Entidade do modelo do PRD-01 §8, com atributos detalhados no
  PRD-09 §8.
- **`EntregaDeRecompensa`** — uma por Guerreiro(a) que recebe: ponto de apoio, Mestre que
  entregou, data, e o lançamento de débito que emitiu (`RF-07-13`, `RF-09-76`).

### Rotas

| Método | Rota                                     | Persona              |
| ------ | ---------------------------------------- | -------------------- |
| POST   | `/v1/trilhas/{id}/recompensas-de-marco`  | Mestre autor         |
| GET    | `/v1/trilhas/{id}/recompensas-de-marco`  | gestão               |
| POST   | `/v1/recompensas-de-marco/{id}/entregas` | Mestre da comunidade |
| GET    | `/v1/entregas`                           | filtrada por persona |

### Cinco recusas, todas antes de qualquer escrita

1. tipo de recurso de natureza **durável** — terceira guarda da inércia do saldo durável;
2. **lastro** reverificado no ato: saldo disponível do tipo no ponto de apoio menor que a
   quantidade;
3. **quantidade** da `RecompensaDeMarco` esgotada;
4. Mestre **não vinculado à comunidade** do Guerreiro(a);
5. Guerreiro(a) que **não alcançou o marco** declarado.

### Decisões novas desta fatia

Levadas ao fundador e por ele decididas antes desta proposta. Cada uma é gravada no
documento-fonte e movida no documento 09 §1 no mesmo PR.

| Decisão                                                                                                                                 | Documento-fonte |
| --------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| **Quem confirma a entrega é o Mestre vinculado à comunidade** do Guerreiro(a), e a baixa sai nesse ato                                   | 02 §8.1         |
| **O lastro é reverificado no ato da entrega**, contra o ponto de apoio dela                                                             | 02 §8.1         |
| **A garantia de lastro migra da publicação da trilha para a entrega**: a trilha é bem comum e não tem ponto de apoio contra o qual conferir | 02 §8.1         |
| **A entrega verifica o marco** contra o percurso já derivado pela capacidade `pontos-niveis-e-badges`                                   | 02 §8.1         |

### Correções que a fatia grava nos PRDs

- **PRD-02**: `RF-02-50` e `RF-02-51` passam a **mostrar** a entrega, não a escrevê-la — mesmo
  precedente do `RF-02-67`, que deixou de atribuir a um frontend um ato do núcleo.
- **PRD-09 §8**: a `RecompensaDeMarco` **não** guarda situação de entrega (a quantidade é N e
  cada Guerreiro(a) recebe uma: a entrega é entidade própria) e **não** declara ponto de apoio
  (a trilha é bem comum — quem o declara é a entrega).
- **PRD-09**: `RF-09-72` e `RN-09-27` deixam de exigir o lastro na publicação da trilha.
- **PRD-07 §8**: a frase que hoje nomeia só a troca passa a nomear também a entrega entre os
  débitos que não declaram aula; `RF-07-13` ganha o ator.

## Capabilities

### New Capabilities

- `recompensa-de-marco`: a declaração do marco que concede recompensa, a entrega ao
  Guerreiro(a) que o alcançou e a baixa definitiva que ela emite — `RF-07-13`, `RN-07-08`,
  `RN-07-14`, `RF-09-71`, `RF-09-76`, `RN-09-26`, `RN-09-39`, `RF-02-50`, `RF-02-51`,
  `RN-02-15`, `RN-02-16`, `RN-02-17`.

### Modified Capabilities

- `livro-razao`: o débito passa a ter **três** origens, e a da entrega não declara aula —
  `Lancamento.aula` segue significando "a reserva daquela aula foi baixada" (`RN-07-15`,
  `RF-07-16`).
- `patrimonio`: a inércia do saldo durável ganha a **terceira** guarda — o durável não é
  reservável por aula, não lastreia item do catálogo avulso e não é entregue como recompensa
  de marco (`RN-07-07`, invariante 9).

## Impact

- **Código**: `backend/src/nucleo/` — módulo novo da recompensa de marco; leitura do percurso
  em `pontos-niveis-e-badges` e do saldo em `livro-razao`; emissão de débito no livro-razão.
- **API**: quatro rotas novas sob `/v1`, na convenção já vigente.
- **Documentação, no mesmo PR**: documento 02 §8.1 (quatro decisões novas), documento 09 §1
  "Já decididos", PRD-02, PRD-07 §§6 e 8, PRD-09 §§6, 7 e 8, `docs/prds/index.md` e o
  documento 99 §8, porque a relação PRD-07 × PRD-09 muda.
- **Fora do escopo**, como o PRD-07 §3.2 já exclui: empréstimo de bancada, reposição
  solidária e a interface de gestão, que é do PRD-02.
