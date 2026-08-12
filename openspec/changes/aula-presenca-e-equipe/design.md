## Context

Ver `proposal.md` — Why. Do que já existe e vale reaproveitar: `ComAutoria` (autor, papel e
momento do registro), `ComMomentoDoFato` (data do fato separada da do registro), o par
`validado_por_id`/`validado_em` de `CriacaoOriginal` — o padrão de "ato que muda o estado, com
quem e quando" —, as duas colunas anuláveis com `CheckConstraint` de `EtiquetaODS` — o padrão de
"referencia A ou B, nunca as duas" — e `TETO_DE_RESPONSAVEIS = 3` em `responsaveis/regra.py`, o
padrão de limite por contagem conferido na regra.

Duas frentes com uma dependência entre si: `aulas/` não depende de ninguém, e `equipes/` depende
de `aulas/` (a equipe da aula) e de `trilhas/` (a equipe da trilha). A terceira frente é a
migração de `criacao_original`, que só existe porque a equipe da trilha nasceu.

## Goals / Non-Goals

**Goals**

- Modelar os dois tempos de vida da equipe numa entidade só, sem duplicar as regras de
  composição que valem para os dois.
- Tornar a fixidez da equipe da trilha uma propriedade conferível do registro, não um combinado
  de operação.
- Migrar `criacao_original` de autoria individual para autoria de equipe sem perder nenhuma
  autoria já gravada.
- Deixar a presença idempotente, porque o App 01 opera com a rede fora e sincroniza depois.

**Non-Goals**

- Quiz ao Vivo: `PerguntaDeQuiz`, `PartidaDeQuiz` e `RespostaDeQuiz` são da décima fatia.
- Lastro e reserva de recursos no agendamento (`RN-01-07`): dependem do PRD-07.
- Qualquer rota sob `/v1`: as de aula, presença e equipe são do PRD-02 e do PRD-04, e a da
  homologação nasce no PRD da aplicação que o documento 09 ainda vai definir.
- Badge Guardião do Acervo: `Aula/Agenda` era a dependência que faltava, mas ele é lançamento do
  Mestre e está fora do escopo declarado na proposta.

## Decisions

### `Aula` guarda dois instantes com fuso, não data mais dois horários

`inicio_em` e `fim_em` como `DateTime(timezone=True)`, com a data derivada de `inicio_em`. O
PRD-01 §9 exige data e hora sempre com fuso, e a derivação de aulas vigentes (`RF-01-32`) vira
uma comparação só — `inicio_em <= agora <= fim_em` — contra o `tempo.agora()` que o núcleo já
usa. `CheckConstraint` exige `fim_em > inicio_em`.

Alternativa descartada: três colunas (`data`, `horario_inicial`, `horario_final`), literais ao
texto do PRD-01 §8 — deixariam ambíguo o fuso de cada horário e obrigariam a recompor o instante
a cada consulta.

### `Equipe` é uma entidade só, com `aula_id` e `trilha_id` anuláveis e `CheckConstraint`

O mesmo padrão de `EtiquetaODS`: as duas colunas anuláveis e uma restrição de banco exigindo
exatamente uma preenchida. É o que a decisão do fundador pediu — dois tempos de vida na mesma
entidade — e o que mantém composição, teto e limite de familiar escritos uma vez só.

Alternativa descartada: duas tabelas (`EquipeDaAula` e `EquipeDaTrilha`) — duplicaria as regras
de composição e a tabela de integrantes, e `RF-01-38` passaria a existir em dois lugares.

### A fixidez é derivada de `homologado_em`, não de uma enumeração de situação

`Equipe` carrega `homologado_por_id` e `homologado_em`, anuláveis, no padrão de
`CriacaoOriginal.validado_por_id`/`validado_em`. Equipe fixa é aquela cujo `homologado_em` não é
nulo; toda entrada e saída de integrante confere isso antes de gravar (`RN-01-44`). A equipe da
aula nunca é homologada — a fixidez dela vem do fim da aula, não de um ato.

Alternativa descartada: coluna `situacao` com "aberta" e "homologada" — guardaria em dois lugares
o mesmo fato que `homologado_em` já responde, e abriria caminho para os dois divergirem.

### O integrante de 17 anos ou mais é o que não tem papel de Guerreiro(a)

O núcleo não guarda data de nascimento, e a faixa do Guerreiro(a) é 6 a 16 (invariante 2): quem
está numa equipe e não é Guerreiro(a) é o familiar de que trata `RF-01-38`. O limite é conferido
por contagem na regra, como `TETO_DE_RESPONSAVEIS`, com `TETO_DE_INTEGRANTES = 5` e
`TETO_DE_INTEGRANTES_NAO_GUERREIROS = 1`.

Alternativa descartada: coluna de idade ou data de nascimento na persona — dado pessoal novo de
criança sem requisito que o peça, contra a §11 do PRD-01.

### Teto e limites ficam na regra; unicidade fica no banco

Contagem não cabe em `CheckConstraint`. Ficam no banco as unicidades que protegem contra corrida:
`(equipe_id, persona_id)` no integrante, `(aula_id, guerreiro_id)` na presença e `(equipe_id)` na
criação original. Ficam na regra o teto de cinco, o limite de um não-Guerreiro(a), a fixidez pós
homologação e a trava de uma equipe da trilha por trilha.

### O núcleo não confere inscrição na trilha, porque ela não existe

Não há entidade de inscrição: o nível 1 é derivado do primeiro `Resultado` (11 §6). Criar equipe
da trilha exige apenas que a trilha exista. Inventar uma trava de matrícula aqui seria regra nova
sem PRD que a sustente.

### A presença idempotente devolve o registro existente, sem erro

`RF-01-20` e o PRD-01 §10 pedem reenvio sem duplicar. A regra procura a presença de
`(aula, guerreiro)` antes de gravar e, achando, devolve a existente com o confirmador e o momento
originais. Não é 409 nem 422: para o App 01 que sincroniza a fila local, o reenvio é sucesso.

Alternativa descartada: `ON CONFLICT DO NOTHING` puro — grava certo, mas não devolve ao chamador
qual registro venceu.

## Migration Plan

A única migração com dado em risco é a de `criacao_original`, hoje única por
`(autor_id, trilha_id)` e sem vínculo com equipe.

1. Criar `aula`, `presenca`, `equipe` e `integrante_da_equipe`.
2. Acrescentar `equipe_id` a `criacao_original`, **anulável**.
3. **Backfill**: para cada criação original existente, criar uma equipe da trilha daquela trilha,
   já homologada, com o `autor_id` como único integrante, e apontar `equipe_id` para ela. Nenhuma
   autoria se perde, e o registro migrado continua respondendo "quem criou isto" com a mesma
   pessoa (`RN-01-13`).
4. Tornar `equipe_id` obrigatória e trocar a unicidade de `(autor_id, trilha_id)` por
   `(equipe_id)`.

`autor_id` **permanece** em `criacao_original`: `ComAutoria` passa a significar "quem entregou
pela equipe", e a autoria coletiva é a equipe. São informações diferentes, e o PRD-01 §4 concede
a entrega ao Guerreiro(a), não à equipe como sujeito de escrita.

Reversão: a ordem inversa devolve a unicidade antiga sem perda, porque o `autor_id` de cada
criação original nunca deixou de existir. As equipes criadas no backfill ficam órfãs de uso e
podem ser removidas junto com a coluna.

## Risks / Trade-offs

- **Backfill que agrupa mal** → cada criação original vira uma equipe de um integrante, nunca uma
  equipe reconstruída por adivinhação. Se duas criações da mesma trilha eram da mesma equipe na
  vida real, o núcleo não tem como saber, e inventar o agrupamento inventaria autoria.
- **`ComAutoria` com dois sentidos em `criacao_original`** → documentado no modelo e no spec: o
  autor é quem entregou, a equipe é quem assina. O risco é de leitura, não de dado.
- **Equipe da trilha nunca homologada** → a criação original entregue por equipe aberta é aceita
  pelos specs, e a composição no momento da validação é a que credita. A trava de "só equipe
  homologada entrega" não está em nenhum requisito; propô-la aqui seria criar regra.
- **Contagem sob concorrência** → dois integrantes entrando ao mesmo tempo numa equipe de quatro
  podem passar dos cinco. A unicidade `(equipe_id, persona_id)` não cobre isso; a conferência
  acontece na mesma transação da inserção, que é o que o núcleo já faz no teto de responsáveis.

## Open Questions

- Qual aplicação carrega a homologação do Mestre — App 03 ou App 09. Já registrada como pendência
  no documento 09; não muda spec, modelo nem tarefa desta fatia, porque a rota nasce no PRD
  daquela aplicação.
