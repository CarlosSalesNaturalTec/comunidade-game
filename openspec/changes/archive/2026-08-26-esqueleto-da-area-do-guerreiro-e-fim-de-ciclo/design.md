## Context

Ver `proposal.md` — Why. O que molda o desenho, e não está lá:

- A capacidade `sessao-do-guerreiro` já resolve a fatia A inteira do lado do núcleo. Nenhuma
  decisão de backend é tomada aqui.
- `apps/app-01-aula-presencial/src/biometria/biometria.ts` é hoje o **único** módulo do
  repositório que importa a Human, carrega modelo e toca `getUserMedia` — a fronteira que
  sustenta o invariante 12 por construção. A App 05 precisa da mesma fronteira.
- `ocorrencia_de_conduta` recusa `UPDATE` e `DELETE` em duas camadas: `event.listen` de mapper
  no ORM e o _trigger_ `trg_ocorrencia_de_conduta_somente_insercao` no Postgres. O expurgo do
  motivo é um `UPDATE`, e colide com as duas.
- `PontoRegular` é **agregado** — uma linha por (Guerreiro(a), trilha ou poder), somada a cada
  crédito, sem detalhe por evento — e o débito é **aparado em zero**
  (`pontuacao/regra.py`, `RN-01-55`). O quanto uma ocorrência custou de fato não está gravado
  em lugar nenhum.
- Não existe entidade `Ciclo` e não deve existir: `configuracao.py` traz `ciclo_rotulo`,
  declarado na implantação.

## Goals / Non-Goals

**Goals:**

- Uma só fronteira de biometria no repositório, consumida pelas duas aplicações.
- Um caminho de expurgo que anule o motivo sem afrouxar a regra de somente inserção para mais
  nada.
- Tirar a ocorrência do ranking devolvendo **exatamente** o que ela tirou.

**Non-Goals:**

- Nenhuma rota nova de núcleo para a fatia A. Se alguma se mostrar necessária, é sinal de que o
  recorte está errado — pare.
- Nenhuma tela da App 05 além da entrada. Trilha, coleta, portfólio e acervo são fatias
  próprias.
- Nenhuma entidade `Ciclo`, nenhum calendário, nenhum congelamento de indicador.

## Decisions

### 1. A biometria sobe para `comum/`, não é duplicada

`biometria.ts` sai de `apps/app-01-aula-presencial/src/biometria/` e passa a
`comum/biometria/`, com o `alias` do `@vladmandic/human` replicado no `vite.config.ts` da
App 05 e no do Vitest. As duas aplicações passam a consumir a mesma fronteira, que continua
expondo só `boolean` e `number[]`.

_Alternativa descartada:_ copiar o módulo para a App 05 — duas cópias da fronteira que sustenta
o invariante 12, cada uma podendo divergir da outra.

### 2. O expurgo é `UPDATE` de Core, e o _trigger_ é estreitado; o ORM segue fechado

Os `event.listen` de mapper **não** são tocados: todo caminho de ORM continua recusando
alteração. O expurgo emite um `UPDATE` de Core, que não dispara evento de mapper, e o _trigger_
do Postgres passa a permitir **exatamente uma** forma de alteração — a que anula `motivo` e
carimba `encerrada_em`, com todas as demais colunas inalteradas. Qualquer outro `UPDATE`, e todo
`DELETE`, continuam recusados dentro e fora do ORM.

O estreitamento é do _trigger_, não da regra: a garantia que a spec exige — "a anulação do
motivo é a única alteração que a regra de somente inserção admite" — passa a ser verificável no
banco, e não só no código.

_Alternativa descartada:_ derrubar o _trigger_ durante o ato e recriá-lo — janela em que a
tabela fica aberta a qualquer escrita, e um erro no meio a deixa aberta.

### 3. A ocorrência passa a gravar o que foi debitado de fato

`ocorrencia_de_conduta` ganha `valor_debitado` (inteiro, gravado na inserção): quanto o débito
efetivamente tirou depois do aparo em zero. `valor` continua sendo o valor nominal do documento
11 §5, e os dois divergem quando o saldo da trilha era menor que 5.

**Decisão do fundador, 2026-08-25**, tomada na exploração desta fatia: ao fim do ciclo o ranking
devolve **o que foi tirado**, não o nominal — a ocorrência sai do ranking como se não tivesse
acontecido, e nunca vira crédito líquido. Como é decisão nova, entra no documento-fonte (11 §5),
na tabela do documento 09 e no PRD-02 antes de virar código.

_Alternativas descartadas:_ devolver sempre os 5 nominais — no caso aparado a criança termina com
mais pontos no ranking do que chegou a ter; não devolver nada — o débito pesaria na posição para
sempre, contra o documento 11 §5.

### 4. `encerrada_em` marca a saída do ranking; `motivo IS NULL` não é o sinal

A ocorrência ganha `encerrada_em` (momento, anulável), carimbado pelo mesmo `UPDATE` do expurgo.
O ranking soma de volta o `valor_debitado` das ocorrências com `encerrada_em` preenchido.

Os dois efeitos do ato coincidem sempre, mas são coisas diferentes: apagar o motivo é guarda de
dado sensível, sair do ranking é regra de jogo. Ler `motivo IS NULL` como sinal de ranking
amarraria uma à outra para sempre.

_Alternativa descartada:_ derivar do `motivo IS NULL` — funciona hoje e conflate LGPD com
gamificação.

### 5. O fim de ciclo não tem entidade e herda a auditoria da escrita

O ato é uma operação, não um registro: nada é criado, e o rótulo do ciclo segue o declarado na
implantação. A capacidade `auditoria` já exige registro para **toda escrita bem-sucedida** — o
ato entra por ele, sem requisito novo, e é por esse registro que se sabe quando um ciclo foi
encerrado.

### 6. A App 05 não reimplementa camada nenhuma

Tokens, fontes, cliente de API com os dois cabeçalhos, componentes acessíveis e guarda de sessão
vêm de `comum/`, como nas outras três aplicações. A App 05 declara apenas a própria chave de
aplicação e o endereço do núcleo, por variável de ambiente do Vite, uma por ambiente.

## Risks / Trade-offs

- **Os modelos da Human não estão provisionados no repositório.** `modelBasePath` aponta para
  `/modelos-de-biometria/`, e nada — nem `public/`, nem passo de build — põe os arquivos lá. É
  lacuna preexistente da App 01, que a App 05 herda ao subir o módulo para `comum/`. → Fora do
  recorte desta fatia; **levar ao fundador** como defeito da App 01, porque hoje a entrada por
  reconhecimento não opera em produção em nenhuma das duas.
- **`valor_debitado` não é recuperável no passado.** Ocorrências já gravadas não sabem quanto
  tiraram. → A migração preenche com o valor nominal e a decisão fica registrada ali; alcança só
  o que existir antes dela.
- **Um _trigger_ estreitado mal escrito abre a tabela.** → O teste da regra cobre as duas pontas:
  o expurgo passa, e `UPDATE` de qualquer outra coluna — inclusive um que anule o motivo mas
  mude `valor` junto — é recusado pelo banco.
- **Duas fatias num PR só.** Não compartilham código, e o `verify` confere dois recortes
  independentes. → As tarefas ficam em blocos separados, e a suíte de cada esteira roda no seu
  bloco.
- **A App 05 nasce com uma tela só.** Um endereço no ar que só sabe abrir e fechar sessão. → É o
  mesmo desenho das três aplicações anteriores, e o custo de não ter a pasta é maior.

## Migration Plan

1. Migração Alembic: `valor_debitado` (não anulável, com preenchimento das linhas existentes
   pelo valor nominal) e `encerrada_em` (anulável) em `ocorrencia_de_conduta`; substituição da
   função do _trigger_ pela versão estreitada. A cópia do _trigger_ presa ao `after_create` do
   modelo acompanha, porque é o caminho que os testes usam.
2. Sem passo de dados: nenhum ciclo foi encerrado ainda, e `encerrada_em` nasce vazio em tudo.
3. _Rollback_: a migração reversa devolve a função original do _trigger_ e derruba as duas
   colunas. Só é segura enquanto nenhum ciclo tiver sido encerrado — depois dela, o motivo
   expurgado não volta, por desenho.
4. A App 05 sobe com o alvo de _hosting_ e o workflow próprios; até as duas chaves de aplicação
   serem semeadas, o núcleo não responde a ela — comportamento esperado, igual ao das outras.
