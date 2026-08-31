## Context

`openspec/specs/consentimento/spec.md` já consolidou o essencial: `Consentimento` somente
inserção (com _trigger_ e _listeners_), tipo em conjunto fechado, versão do termo carimbada pela
configuração e `condicao_de_autorizacao_vigente` — a expressão SQL da vigência com a recusa
prevalecendo, já usada por `vitrine/`, `criacoes_originais/`, `pontuacao/`, `jogos/` e
`sessoes/`. `openspec/specs/solicitacao-do-responsavel/spec.md` já tem a fila, o prazo de 7 dias
e o desfecho. A fatia não reabre nada disso: acrescenta a **porta do responsável** sobre o que
já existe.

## Goals / Non-Goals

**Goals:**

- As duas rotas `/v1/eu/guerreiros/{id}/autorizacao`, com as guardas de vínculo e os 409 da
  PRD-13 §9.
- O estado em três valores derivado do mesmo histórico, sem coluna de estado.
- A solicitação da divergência aberta pelo núcleo, uma só em aberto por Guerreiro(a).
- As telas da autorização na App 07.

**Non-Goals:**

- Rever a vigência que as superfícies públicas já leem — `RF-13-16` e `RN-13-11` são cobertos
  por cenário, não por código novo.
- `POST /v1/guerreiros/{id}/autorizacao/assistida` e o anexo do termo (`RF-13-35` a `RF-13-38`):
  são da fatia 6.
- Termos, leitura do termo e histórico de acessos (`RF-13-29` a `RF-13-34`): fatia 5.
- O texto do termo quanto à entrega de dados — trava da fatia 5, não desta (PRD-13 §14).

## Decisions

### 1. Os três estados são derivação, não coluna

`vigente` / `suspensa` / `nao_autorizada` saem da mesma subconsulta da decisão mais recente por
responsável que `condicao_de_autorizacao_vigente` já monta. `suspensa` exige **concessão e
recusa convivendo** — é a divergência que `RF-13-19` e a PRD-13 §5.4 nomeiam; recusa sem
concessão alguma é `nao_autorizada`, e não abre solicitação porque não há divergência a tratar.
Para toda superfície pública os dois estados não vigentes são o mesmo, e `RN-13-11` continua
valendo pela expressão que já existe — nenhum chamador dela muda.

Descartado: gravar o estado numa coluna do Guerreiro(a). Contraria `RN-13-10` e criaria duas
verdades sobre o mesmo fato.

### 2. Idempotência por comparação com a decisão mais recente do próprio responsável

A escrita compara a decisão que chega com a mais recente daquele responsável sobre aquele
Guerreiro(a): igual, devolve o registro existente sem gravar; diferente, grava. Atende ao
"reenviar a mesma concessão não gera dois registros" da PRD-13 §10 sem chave de idempotência no
cabeçalho — que nenhum documento decidiu.

Descartado: índice único por (responsável, Guerreiro(a), tipo, decisão). Impediria o legítimo
conceder → revogar → conceder de `RF-13-21`.

### 3. Os dois 409 se decidem pela decisão mais recente de cada um

- Concessão com recusa mais recente de **outro** responsável → 409 com o estado e a orientação
  de procurar a gestão (PRD-13 §9). A recusa prevalece, e não é a concessão de um terceiro que
  a desfaz.
- Revogação quando a decisão mais recente **do próprio** responsável não é concessão → 409: não
  há o que revogar.

O responsável que ele próprio recusou **pode conceder** — é o caminho que o documento 09 nomeia
("o caso volta à pauta se quem recusou mudar de posição"). Sem essa distinção o estado suspenso
seria definitivo, o que contraria a decisão do fundador gravada no documento 05 §4.

### 4. A solicitação da divergência é do tipo `esclarecimento`, com marca de origem no registro

Decisão do fundador, 2026-08-31: a solicitação nasce do tipo `esclarecimento` — sem quinto tipo
—, em nome de quem recusou, e **uma só enquanto estiver em aberto** por Guerreiro(a). Como a
guarda é por Guerreiro(a) e não por responsável, e como ela não pode ser confundida com o
esclarecimento que o próprio responsável escreve, `SolicitacaoDoResponsavel` ganha um campo
booleano de origem — aberta pela suspensão, ou não — com migração e valor padrão falso. Ele é
**mecanismo**, não regra: a fila da App 03 continua vendo um esclarecimento como qualquer outro,
e nenhuma leitura existente muda.

Descartado: reconhecer a solicitação da divergência pelo texto que o núcleo escreve — frágil, e
quebraria à primeira reescrita do texto.

A abertura corre no **mesmo commit** da recusa: a recusa nunca é recusada porque a solicitação
não pôde nascer, e não existe estado suspenso sem caso na fila.

### 5. Quem lê o histórico lê o do Guerreiro(a), não só o próprio

`RF-13-18` já manda mostrar aos **demais** responsáveis quem motivou a suspensão; o histórico de
`RF-13-21` segue a mesma medida e traz as decisões de todos os responsáveis vinculados àquele
Guerreiro(a), cada uma com quem decidiu. `RN-13-04` continua respeitada: o recorte é o
Guerreiro(a) vinculado, e nada de criança de terceiro aparece.

### 6. A tela é uma aba do vinculado escolhido, não uma tela de topo

`TelaDeVinculados` já guarda o vinculado selecionado; a autorização entra como segunda aba ao
lado da evolução, e a alternância entre vinculados continua valendo nas duas (`RF-13-05`). A
decisão exige rede e a tela diz isso em vez de simular sucesso (PRD-13 §10) — nenhum otimismo de
interface sobre um registro versionado.

### 7. Nada nesta fatia entra no livro-razão

Conceder, revogar e abrir a solicitação da divergência não têm custo: nenhum lançamento previsto
(PRD-07). Nenhum dado de território é tocado, e nenhuma série temporal nasce aqui.

## Risks / Trade-offs

- **A guarda da divergência é por Guerreiro(a), não por responsável** — logo, com uma em aberto,
  uma segunda recusa de outro responsável não gera registro na fila. É o que o fundador decidiu:
  a gestão trata o caso, não cada ato. O histórico da autorização continua guardando cada recusa,
  então nada se perde.
- **Nomear quem recusou** é exposição de um responsável a outro. É requisito explícito
  (`RF-13-18`) e o recorte para em nome, data e hora — nunca motivo, que a plataforma não coleta.
- **Campo novo em `SolicitacaoDoResponsavel`** custa uma migração. Alternativa era o quinto tipo,
  que teria custado uma mudança de requisito no PRD-13.
