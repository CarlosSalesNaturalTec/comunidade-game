## Context

Ver `proposal.md` — Why. O que restringe o desenho é o que a fatia anterior deixou de pé:

- `coletas/regra.py` tem **`_consulta_de_registros_publicaveis`**, que já executa os três passos
  da publicação — rotular cada registro válido com (tipo de coleta, local publicado), subir ao
  nível da comunidade o recorte abaixo do piso e suprimir o que não o alcança no topo. Ela
  devolve uma consulta, não uma lista, e `paginar_serie_publica` a consome como subquery.
- `locais/regra.py` tem **`resolver_locais_publicados`**, a CTE recursiva que mapeia local →
  local publicado, escrita justamente para não nascer duas vezes.
- `configuracao.py` já carrega o piso de coletores e o `ciclo_rotulo`.
- `ods/regra.py` tem `cobertura_por_trilha`, `cobertura_por_comunidade` e
  `comunidades_com_cobertura`; a de comunidade parte de `Resultado` e não conhece a coleta.
- `coletas/regra.py` tem `resolver_etiquetas_do_desafio`, que já resolve a etiqueta herdada da
  missão ou da trilha — a fonte que falta ligar à cobertura.
- `armazenamento/` expõe a `PortaDeArmazenamento`, usada pelo comprovante de aporte e pela
  mídia do registro.

## Goals / Non-Goals

**Goals:**

- A exportação reusar **exatamente** a consulta da série pública, para que guarda afrouxada num
  lado não possa existir sem afrouxar no outro.
- Uma só fonte da cobertura por comunidade, com as duas origens somadas dentro dela, para que a
  rota pública e a declaração da meta 17.18 leiam o mesmo número.

**Non-Goals:**

- A entrega do conjunto abaixo do bairro sob aprovação de Admin: não há `RF` que a declare, e a
  pergunta está no `proposal.md`.
- Auditoria e invalidação: o filtro por situação válida já está escrito e a fatia da auditoria
  passa a preenchê-lo sem tocar nesta.
- Geração assíncrona ou agendada do arquivo: o Ciclo 01 roda sem agendador, e o conjunto de uma
  comunidade cabe na resposta da chamada.

## Decisions

### A exportação chama a mesma consulta da série pública, sem cópia

`_consulta_de_registros_publicaveis` já é o ponto único onde o corte no bairro, a ausência de
coletor, o piso e a supressão acontecem. A exportação a chama com os mesmos argumentos e
serializa o resultado; nenhuma guarda é reimplementada.

É a decisão que sustenta o requisito "herda integralmente as guardas": um conjunto em arquivo é
mais fácil de cruzar que uma tela, e a única forma de garantir que as duas saídas não divirjam
com o tempo é **não haver duas apurações**.

_Alternativa descartada:_ consulta própria da exportação, otimizada para varredura — duplicaria
a regra de privacidade em dois lugares, e o dia em que uma mudasse sem a outra seria um
vazamento silencioso.

### O conjunto sai em uma resposta, com o CSV no corpo e os metadados em cabeçalho

O documento 03 §12.3 pede "uma tabela por arquivo". A série é **uma** tabela, de modo que o
corpo é o CSV dela e nada mais — sem envelope JSON em volta, que quebraria a leitura direta em
planilha.

O que não é linha da tabela — dicionário de dados, licença CC BY-SA, período coberto e
declaração da meta 17.18 — **não entra no CSV**, porque comentário no meio de um CSV o
desalinha em qualquer planilha. Vai em **cabeçalhos de resposta** e numa **rota irmã** que
devolve o dicionário e as declarações em JSON, endereçada no próprio cabeçalho do CSV.

_Alternativas descartadas:_ ZIP com CSV + dicionário — exige descompactar antes de abrir, o que
contraria "legíveis em planilha"; linhas de comentário no topo do CSV — desalinha o cabeçalho
declarado que o mesmo parágrafo do documento 03 exige.

### Não há GeoJSON no Ciclo 01, e isso não é lacuna

O documento 03 §12.3 prevê "GeoJSON para a geometria", mas o PRD-08 §3.2 exclui o
georreferenciamento por coordenada do Ciclo 01: a granularidade é a **hierarquia de locais
declarada**, não o ponto no mapa. Não existe geometria a exportar, e inventar uma — centroide de
bairro, polígono aproximado — seria criar dado que a plataforma não coletou e pôr no arquivo uma
precisão que ela não tem.

O local sai no CSV como **rótulo e nível**, que é a granularidade real do dado. Quando o ciclo
que trouxer coordenada chegar, o GeoJSON acompanha sem mudar o CSV.

### O período coberto é apurado do conjunto, não repetido do pedido

`RF-08-27` pede o período **coberto**, que não é o período **pedido**: pedir o ano inteiro e ter
medição só em dois meses cobre dois meses. A declaração sai da primeira e da última medição
efetivamente contidas no conjunto — depois do piso, porque recorte suprimido não cobriu nada.

Conjunto vazio declara período vazio, e não o intervalo pedido.

### A cobertura por comunidade ganha a segunda fonte dentro de `cobertura_por_comunidade`

A união acontece **dentro** da função que já existe, não numa função paralela. Assim a rota
pública, a declaração da meta 17.18 e qualquer leitor futuro herdam a fonte nova sem mudança de
chamada — e não há como um deles ficar para trás.

`comunidades_com_cobertura` acompanha: hoje ela lista as comunidades com ao menos um `Resultado`,
e passa a listar também as que têm série aberta sobre desafio etiquetado. Sem isso a comunidade
que só coletou seria calculada corretamente e **nunca perguntada**.

_Alternativa descartada:_ `cobertura_de_coleta_por_comunidade` à parte, somada nos chamadores —
cada chamador novo teria de lembrar de somar, e o primeiro que esquecesse publicaria cobertura
menor que a real.

### O estado da série não filtra a cobertura

A cobertura mede **alcance declarado**, como o documento 04 §4 diz ao apresentar os indicadores
de cobertura — não continuidade nem mérito. Uma série interrompida cobriu o objetivo enquanto
existiu, e retirá-la faria a cobertura de uma comunidade **encolher** com o tempo, o que
nenhuma leitura de `RF-08-26` sustenta.

O indicador que o documento 04 §4 chama de "séries de coleta ativas por ODS, com o tempo em que
se mantiveram" é outro, e mais fino: não é `RF-08-26` e não entra aqui.

## Risks / Trade-offs

- **A exportação sem período varre a comunidade inteira e serializa tudo na resposta** → mesmo
  risco da consulta, agora sem paginação para amortecê-lo. Aceito no Ciclo 01 pela ordem de
  grandeza de uma comunidade; a saída, se pesar, é a geração para a `PortaDeArmazenamento` com
  a resposta devolvendo a referência — troca de transporte, não de regra.
- **Metadados fora do CSV podem se perder no caminho** → quem baixar só o corpo fica sem a
  licença e sem a declaração da meta. Mitigado pelo cabeçalho que endereça a rota irmã, e é o
  preço de manter o CSV abrível em planilha; a alternativa quebrava o requisito mais duro dos
  dois.
- **A cobertura pode crescer para quem já lia a rota** → é o defeito sendo corrigido, não
  regressão: a etiqueta do desafio existia sem leitor desde a fatia do desafio de coleta. No
  Ciclo 01 nenhuma aplicação consome a rota.
- **Duas fontes de cobertura podem contar o mesmo objetivo duas vezes** → a agregação é de
  **conjunto**, união de distintos; o teste cobre trilha e desafio etiquetados com o mesmo
  objetivo devolvendo-o uma só vez.
- **O piso apurado sobre o período muda o conjunto conforme o recorte pedido** → é o desenho, e
  é o que impede reconstruir por diferença um recorte suprimido pedindo dois períodos que se
  encaixam. Fica anotado: quem cruzar exportações de períodos vizinhos vê agregados que não
  somam, e isso é proteção, não defeito.
