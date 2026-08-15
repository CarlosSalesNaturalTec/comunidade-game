## Context

Ver `proposal.md` — Why. O que restringe o desenho é o que já está de pé:

- `locais/modelo.py` guarda a hierarquia de seis níveis com `local_pai_id` e `ORDEM_DOS_NIVEIS`
  declarada; a chave estrangeira composta já garante que pai e filho são da mesma comunidade.
- `coletas/modelo.py` tem `RegistroDeColeta` **particionado por RANGE em `momento_do_fato`**,
  com chave primária composta `(id, momento_do_fato)`, e `situacao` com o único valor `valida`
  por enquanto. `comunidade_virtual_id` está **gravado no próprio registro**, resolvido pelo
  vínculo vigente na data da medição — não se deriva na leitura.
- O local **não** está no registro: ele é da `SerieDeColeta`, um por série. A série é
  individual, de modo que o par (série → local, série → coletor) é estável.
- `paginacao.py` tem `contrato_de_listagem`, `PaginaDeResultado`, `codificar_cursor` e
  `decodificar_cursor`, com os filtros universais `comunidade`, `periodo_inicio`, `periodo_fim`
  e `persona` já declarados, e o teto de tamanho na `Configuracao`.
- `vitrine/rotas.py` é o precedente de rota pública: sem `Depends(exigir_persona)`, com a chave
  de aplicação conferida transversalmente, e nunca escrevendo.
- Os testes rodam contra **PostgreSQL de verdade** (`conftest.py`), de modo que CTE recursiva e
  função de janela são testáveis e não precisam de caminho de compatibilidade.

## Goals / Non-Goals

**Goals:**

- Um só ponto no núcleo que resolva o **local publicado** de um registro, para que a exportação
  da fatia seguinte não reimplemente a subida da hierarquia.
- O piso de coletores decidido **antes** de qualquer corte de página, para que a supressão de um
  recorte não dependa de onde a página começa.
- Nenhum caminho pelo qual um coletor alcance a resposta — nem por campo, nem por filtro, nem
  por contagem.

**Non-Goals:**

- Exportação agregada a instituições e cobertura de ODS das séries: fatias seguintes, e o
  desenho só precisa deixar a resolução do local publicado reaproveitável.
- Cache de resposta: o PRD-08 §10 pede a consulta cacheável, e o cabeçalho de cache não muda o
  contrato — entra quando houver medida de carga, não por antecipação.
- Auditoria e invalidação: o filtro por `situacao == valida` já nasce escrito, e a fatia da
  auditoria passa a preenchê-lo sem tocar nesta.

## Decisions

### O recorte publicado é o par tipo de coleta × local, e o local é resolvido subindo a hierarquia

O PRD-08 §5.6 publica "as séries históricas **por tipo de coleta**, agregadas até o bairro": o
recorte é o par, não o local sozinho. É também o recorte sobre o qual `RN-08-24` faz sentido —
o piso protege quem coleta *aquilo* *ali*, e contar coletores de um bairro somando tipos
diferentes deixaria passar o tipo de coletor único.

O local publicado é o ancestral de nível **bairro** do local da série, ou a **comunidade**
quando a série está direto nela. Resolve-se na leitura, por **CTE recursiva** sobre
`local_pai_id` — a hierarquia tem no máximo seis níveis e o banco é PostgreSQL por decisão do
documento 03 §1.

_Alternativas descartadas:_ gravar o bairro no registro — o registro é somente inserção
(`RN-08-10`) e uma correção de hierarquia deixaria a série publicada mentindo; recorte só por
local — deixa passar o tipo de coletor único dentro de um bairro movimentado.

### O piso é apurado sobre o resultado inteiro, e só depois a página é cortada

A supressão de um recorte não pode depender do tamanho nem do início da página: um bairro que
sobe para a comunidade tem de subir em todas as páginas, sempre. A apuração acontece, então, em
**três passos na mesma consulta**, antes de qualquer `LIMIT`:

```text
1. rotular   cada registro válido da comunidade e do período com
             (tipo_de_coleta, local_publicado)                     ← CTE recursiva

2. apurar    COUNT(DISTINCT coletor) por (tipo, local_publicado)   ← função de janela
             recorte < piso  →  local_publicado := comunidade

3. reapurar  COUNT(DISTINCT coletor) por (tipo, comunidade)        ← já com os que subiram
             ainda < piso    →  o recorte inteiro não sai
```

O passo 3 é o que a leitura ingênua erra: um bairro de dois coletores que sobe **acrescenta**
os coletores dele ao recorte da comunidade, e a contagem do topo tem de ser a **união dos
distintos que ali chegaram**, nunca a soma das contagens — dois bairros com o mesmo par de
coletores continuam somando dois, não quatro.

_Alternativa descartada:_ apurar o piso por página — o mesmo bairro apareceria numa página e
sumiria noutra, conforme o corte.

### O item paginado é o ponto da série, não o recorte

"Série histórica agregada até o bairro" agrega no **espaço**, não no tempo: nenhum documento
declara janela de agregação temporal, e inventar uma — diária, semanal, mensal — seria criar
regra num artefato do OpenSpec. O ponto sai como foi medido, com a data e hora da medição, e
carrega o recorte a que pertence.

Isso também resolve a paginação: o recorte é conjunto de tamanho imprevisível, e devolver
recortes inteiros faria uma página variar de dez linhas a dez mil. A ordenação estável é
**(tipo, local publicado, momento da medição, id do registro)** e o cursor opaco carrega essa
quádrupla, no mesmo `codificar_cursor` das demais listagens. O `id` desempata medições
simultâneas do mesmo recorte, que sem ele repetiriam ou sumiriam na virada de página.

_Alternativas descartadas:_ paginar por recorte com os pontos embutidos — página de tamanho
imprevisível; agregar por janela temporal — regra que nenhum documento declara.

### A contagem de coletores fica na guarda, não na resposta

O piso precisa da contagem; a resposta, não. Devolvê-la publicaria a espessura da base de
coletores de cada bairro — informação que nenhum requisito pede e que, num bairro de exatamente
três, diz mais do que o piso quis esconder. Fica interna.

### O período recorta pela data da medição, e a partição colabora

`RF-08-15` já manda toda regra dependente de tempo usar a data da medição, e `momento_do_fato`
é justamente a chave de particionamento da tabela: o filtro por período **poda partições**, em
vez de varrer a série inteira. É o retorno do desenho que a fatia do registro escolheu.

Sem período informado, a consulta alcança toda a série da comunidade — comportamento correto
para "série histórica", e o custo fica registrado em Riscos.

### O corte no bairro é mais estrito que o critério de aceite, de propósito

O critério do PRD-08 §12 diz "não devolve ... local abaixo de **rua**"; `RN-08-13` e o documento
02 §1 dizem que a saída pública **para no bairro**. Vale o mais estrito: a regra é de nível 1 e
o critério de aceite é satisfeito por consequência — quem não devolve abaixo do bairro também
não devolve abaixo da rua. Registrado aqui para não parecer engano de leitura na revisão.

### A mídia não sai, e o ponto sai mesmo assim

O PRD-08 §11 põe a foto e o vídeo do território como "público, **após auditoria**", e a
auditoria não existe no núcleo. Publicar agora exporia justamente a mídia que `RN-08-16` manda
invalidar quando contiver pessoa identificável — a proteção da criança dependeria de uma fatia
que ainda não foi escrita. O ponto de um tipo por evidência sai com a data da medição e o
recorte, sem valor e sem arquivo; quando a auditoria entrar, a mídia auditada passa a poder
acompanhar sem mudar o contrato.

## Risks / Trade-offs

- **A consulta sem período varre a comunidade inteira** → a poda de partição não ajuda quando
  não há período, e a apuração do piso é sobre o resultado inteiro por desenho. Aceito no Ciclo
  01: uma comunidade tem uma ordem de grandeza de séries que cabe na consulta, e o PRD-08 §10
  prevê a rota cacheável quando houver carga que justifique.
- **A CTE recursiva roda por consulta** → a hierarquia tem seis níveis e a poda por comunidade
  a mantém pequena; se pesar, o caminho é materializar o ancestral de bairro, não trocar o
  desenho.
- **O piso protege o recorte, não a coincidência entre recortes** → três bairros, cada um com
  os mesmos três coletores, publicam três recortes que juntos ainda são três pessoas. É o que a
  regra do documento 02 §1 declara, e ampliá-la seria criar regra; fica anotado para quando a
  entrega abaixo do bairro (documento 03 §12.3) for desenhada.
- **`situacao` tem hoje um único valor** → o filtro por `valida` não é observável em teste até a
  fatia da auditoria existir. O teste que o cobre grava a situação diretamente, para que o
  filtro não nasça sem prova.
- **Duas rotas públicas a mais aumentam a superfície sem sessão** → nenhuma delas escreve, a
  chave de aplicação continua exigida e a cota por chave já é transversal; o freio por origem
  não se aplica, porque protege consulta por nick e formulário, não leitura agregada.
