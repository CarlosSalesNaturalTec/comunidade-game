## Context

Ver `proposal.md` — Why. Três padrões já consolidados guiam a fatia, e o desenho aplica os
três em vez de inventar:

- **Leitura aninhada em `GET /v1/trilhas/minhas`** — `trilha-e-missao` já a define, e as
  changes `2026-09-12-leitura-do-desafio-de-desbloqueio-pelo-mestre` e
  `2026-09-15-leitura-de-conteudo-e-bibliografia-pelo-mestre` já a estenderam duas vezes, do
  mesmo modo. A culminância é a terceira.
- **Saída de bytes pelo núcleo** — `desbloqueio-da-missao` já a define para a imagem da
  pergunta do quiz, com autorização estrita ao Mestre autor e ao Guerreiro(a) inscrito. O
  arquivo do conteúdo repete o molde.
- **Tipo do arquivo gravado no envio** — a pergunta do quiz já guarda o tipo da imagem; o
  conteúdo da missão o apura e o descarta.

## Goals / Non-Goals

**Goals:**

- Ligar a culminância gravada à leitura que o Mestre autor já faz, sem rota nova.
- Dar ao núcleo a segunda saída de bytes, na mesma forma da primeira.
- Fazer a pré-visualização apresentar o que a tela do Guerreiro(a) apresenta, pela mesma
  ordem e pelos mesmos dados.

**Non-Goals:**

- Unificar a leitura da missão num componente de `comum/` partilhado entre App 05 e App 09.
- Tocar no envio: ele continua direto ao armazenamento, fora do núcleo.
- Mudar a leitura pública `GET /v1/trilhas/{id}`, que já está correta.

## Decisions

### 1. A culminância vai aninhada em `GET /v1/trilhas/minhas`, e não em rota própria

`TrilhaDoMestreSaida` ganha o campo; `listar_minhas_trilhas_rota` o popula com a mesma consulta
que `obter_trilha_publica_rota` já faz. **Nulo** é "esta trilha não tem culminância" — a
ausência é dita, nunca suposta, e o cliente deixa de precisar distinguir `undefined` de `null`.

_Descartado:_ `GET /v1/trilhas/{id}/culminancia` em rota própria — uma chamada por trilha na
tela que já lista todas, e o PRD-09 §9 não a declara.
_Descartado:_ a App 09 chamar `obterTrilhaPublica` — só serve trilha publicada, e a
pré-visualização existe justamente para o rascunho. Essa função está exportada e nunca é
chamada na App 09; sai como limpeza.

### 2. O tipo do arquivo ganha coluna, apurada na confirmação do envio

`PortaDeArmazenamento.ler` devolve `bytes` e nada mais, e mudar a porta obrigaria os dois
adaptadores a carregar metadado que só este caso usa. `confirmar_envio` já consulta o
armazenamento pelo tamanho real: grava o tipo no mesmo ponto, com **revisão Alembic** na mesma
change — a lição de `2026-09-10-migracao-das-tabelas-de-recompensa-de-marco` é que modelo sem
migração volta como conserto.

Linha antiga, gravada antes da coluna, sai como `application/octet-stream`, como a imagem da
pergunta já faz para o mesmo caso. Nenhum retrocarregamento: o tipo é adiante.

_Descartado:_ deduzir o tipo pela extensão da referência — a referência é nossa, não do
arquivo enviado.
_Descartado:_ confiar no tipo declarado na abertura da sessão — o recebido pode desmentir o
declarado, que é a razão de o tamanho já ser reapurado ali.

### 3. `GET /v1/conteudos/{id}/arquivo` copia a autorização da imagem da pergunta

Mestre autor da trilha **ou** Guerreiro(a) inscrito nela; qualquer outra persona recebe 403.
Conteúdo sem envio confirmado responde 404. A regra nova fica em `conteudos/regra.py`, ao lado
de `confirmar_envio`, e a rota apenas a reexpõe — como `ler_imagem_da_pergunta_rota` faz.

Servir arquivo de até 200 MB pelo núcleo é mais pesado que servir 1 MB de imagem. O que a
arquitetura mantém fora do núcleo é o **envio** (`RN-01-28`), e a saída pelo núcleo é o que
preserva a exigência de chave de aplicação em toda rota sob `/v1` (documento 03). Fica como
risco anotado abaixo, não como decisão reaberta.

_Descartado:_ URL assinada do armazenamento direto ao navegador — contornaria a chave de
aplicação e exporia o bucket; nenhum documento a decide.

### 4. A pré-visualização espelha a tela do Guerreiro(a), sem componente comum

Decisão do fundador, 2026-09-16: espelhar agora, deixar o componente único de `comum/` para
fatia própria. `PreVisualizacaoDaMissao` passa a receber a missão inteira e a desenhar, na
ordem de `Missao.tsx` da App 05: título, aviso de opcional, conteúdo, crédito e licença,
bibliografia, atividades e desafio de desbloqueio (ou sondagem) em leitura.

_Descartado:_ o componente comum (caminho C da exploração) — mata a divergência na raiz, mas
custa mais do que a fatia comporta.

**Risco aceito:** as duas telas voltam a poder divergir. Mitigação dentro da fatia: os testes
da pré-visualização cobrem cada item que a tela do Guerreiro(a) apresenta, de modo que tirar um
deles quebre a suíte.

### 5. O crédito da pré-visualização usa o nick do Mestre em sessão

Decisão do fundador, 2026-09-16. A App 09 lê `GET /v1/eu/mestre/identidade`, que já existe, e
usa o **nick**, com queda para "Mestre autor" quando for nulo — o mesmo texto de reserva da App
05. Nenhum campo novo entra em `IdentidadeDoMestreSaida` e nenhuma rota nasce para isso.

**Divergência consciente:** o Guerreiro(a) lê `autor_nome`, que é o **nome** da persona, não o
nick. O crédito da pré-visualização diferirá em texto do que ele verá. O fundador foi
informado e decidiu pelo nick; unificar os dois é decisão dele em fatia futura, não suposição
desta.

_Descartado:_ acrescentar `nome` a `IdentidadeDoMestreSaida` — o crédito ficaria idêntico ao do
Guerreiro(a) por uma linha de backend, mas o fundador decidiu pelo nick.

### 6. As imagens são buscadas pelo núcleo, não por `<img src>`

Toda rota sob `/v1` exige a chave da aplicação em cabeçalho, e `<img src>` não a manda. As duas
aplicações leem o arquivo como _blob_ pela camada de acesso comum e o exibem por URL de objeto,
como `lerImagemDaPergunta` já faz na App 09. A URL de objeto é liberada ao desmontar, para não
vazar memória em missão com muitas imagens.

## Risks / Trade-offs

- **Vídeo de até 200 MB servido pelo núcleo** → O Ciclo 01 serve o arquivo inteiro, como a
  imagem da pergunta já é servida. Se a latência incomodar em rede fraca, a saída por faixas
  de bytes é fatia própria, e o contrato da rota não muda por causa dela.
- **Memória do processo ao servir arquivo grande** → A regra lê do armazenamento e devolve;
  medir e paginar só se o uso real exigir. Anotado, não resolvido aqui.
- **Coluna nova sem retrocarregamento** → Conteúdo antigo sai como tipo indeterminado. O
  navegador pode não exibir alguns desses; o Mestre reenvia se quiser, e nada quebra.
- **A pré-visualização e a tela do Guerreiro(a) podem divergir de novo** → Mitigado pelos
  testes da decisão 4, não pela estrutura. É o preço de adiar o componente comum.
- **A migração precisa subir com o código** → Se a revisão Alembic ficar para depois, a coluna
  existe no modelo e não no banco, e a confirmação de envio responde 500. O teste de paridade
  entre `alembic upgrade head` e `Base.metadata`, que já existe, pega isso.
