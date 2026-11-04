# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta, e já está de pé:

- `GET /v1/vitrine/criacoes` pagina por **keyset** `(validado_em, id)` descendente, com cursor
  opaco (`codificar_cursor`/`decodificar_cursor`), e `CriacaoPublicaSaida` leva `trilha_id`,
  `trilha`, `validada_em`, `producao` e `autores` — **sem** `id`, que a abertura exige.
- O portão da criação é `condicoes_de_criacao_publica`, **uma** função usada pela listagem e
  pela rota de bytes `GET /vitrine/criacoes/{id}/arquivo` (`RN-01-63`).
- A comprovação do prático mora em `DesbloqueioDaMissao`, gravada pelas changes de 2026-11-04:
  `cumpriu`, `publicavel`, `julgado_em`, `comprovacao`, `comprovacao_referencia`,
  `comprovacao_tamanho`, `comprovacao_tipo_do_arquivo` e `entrega_presencial`. O título curto e
  a forma aceita são da missão (`Missao.desafio_pratico_titulo_curto`).
- As duas fontes compartilham o **mesmo** conjunto de seis tipos
  (`TipoDeProducaoDaCriacaoOriginal`): texto, imagem, áudio, link externo, vídeo e arquivo.
- Nenhuma rota sob `/v1` aceita `<img src>` direto: a chave da aplicação vai em cabeçalho, e
  `comum/react/MidiaDoNucleo` já resolve isso para imagem, áudio e vídeo.
- `ListaDeRegistros` é compartilhada por quatro seções da App 06 e não tem estado por linha.

## Goals / Non-Goals

**Goals:**

- Uma leitura por página da seção, uma ordem e uma paginação, com as duas fontes dentro.
- Portão único por fonte, usado pela listagem **e** pela rota de bytes dela.
- Abertura da produção sem endereço novo e sem nada gravado no aparelho (`RN-03-22`).

**Non-Goals:**

- Campo novo no modelo e migração: a fatia só lê.
- Rota de listagem nova: o endereço da seção segue o do PRD-03 §9.
- Mexer em `ListaDeRegistros`, que outras três seções usam.

## Decisions

1. **Uma rota, duas consultas, junção em memória.** Cada fonte roda a sua consulta com o mesmo
   recorte de cursor e `tamanho + 1` itens; o resultado é ordenado por `(data, id)`
   decrescente e truncado em `tamanho`. É correto porque item além do `tamanho + 1`-ésimo de
   uma fonte nunca cabe entre os `tamanho` primeiros da união. O cursor **não** ganha marca de
   fonte: o `id` é UUID, único entre as tabelas, e a tupla já ordena.
   _Descartado:_ `UNION ALL` com o keyset numa só consulta — a hidratação de cada fonte exige
   segunda passada de todo modo, e o mapeamento no ORM fica opaco. _Descartado:_ visão ou
   tabela de acervo — objeto de dado novo para o que duas consultas respondem.
2. **A chave do cursor passa a `aprovado_em`, e a antiga `validado_em` continua aceita.** O
   cursor é opaco, mas quem estiver no meio da paginação no momento da implantação receberia
   422 numa seção pública. Ler as duas chaves custa duas linhas.
3. **O título é derivado, não gravado.** Na comprovação é `desafio_pratico_titulo_curto` da
   missão; na criação é o nome da trilha, que a rota já busca em `nomes_de_trilha`. Decisão do
   fundador de 2026-11-04. _Descartado:_ coluna `titulo` em `CriacaoOriginal` com migração —
   nasceria sem nada para preencher, e o fundador decidiu que o nome da trilha é o título.
4. **Quem não repete a trilha é a App 06, pela `fonte`, não o núcleo.** O payload leva sempre
   `titulo` e `trilha`; a linha omite a trilha quando a `fonte` é a criação da culminância, em
   que o título já é ela. A regularidade do contrato importa porque a rota pública é o que
   terceiros constroem por cima (PRD-03 §8). _Descartado:_ o núcleo manda `trilha` nula nessa
   fonte — esconde dado de terceiro para resolver questão de tela.
5. **Rota de bytes por fonte, e portão irmão.** Nasce
   `GET /v1/vitrine/comprovacoes/{id}/arquivo`, e `condicoes_de_comprovacao_publica` fica ao
   lado de `condicoes_de_criacao_publica`, servindo à listagem e a ela — uma regra, nunca duas
   cópias que possam divergir (`RN-01-63`). A recusa é **404 em todos os casos**, como na rota
   irmã. _Descartado:_ rota única `/vitrine/acervo/{fonte}/{id}/arquivo` — mudaria de lugar uma
   rota pública já publicada, e cada fonte tem portão próprio de todo jeito.
6. **A abertura é estado de um componente dentro da linha, não da lista.** `ProducaoDoAcervo`
   entra em `dados` da `LinhaDeRegistro` e guarda o aberto/fechado em `useState` próprio.
   `ListaDeRegistros` fica intacta, e o estado morre ao recarregar e ao trocar de página, que é
   o que o `RN-03-22` exige. _Descartado:_ `LinhaDeRegistro` ganhar um nó de detalhe e a lista
   dona do estado — acrescenta a quatro seções o que uma precisa.
7. **Imagem, áudio e vídeo reusam `comum/react/MidiaDoNucleo`**, com `token` nulo: ele já busca
   os bytes com a chave em cabeçalho, monta a URL de objeto, a revoga e trata a falha em
   moldura de tamanho fixo. Texto sai do próprio item, link externo vira link de saída, e
   arquivo vira transferência pela mesma busca em bytes, nomeada pelo título.
   _Descartado:_ uma quarta implementação de busca de mídia na App 06 — é o desvio que a
   moldura comum veio corrigir.

## Risks / Trade-offs

- **A paginação busca `2 × (tamanho + 1)` linhas para servir `tamanho`** → com dez por página
  são 22 linhas por leitura, em duas consultas indexadas; o custo é desprezível diante de uma
  terceira estrutura de dados a manter em sincronia.
- **Uma fonte vazia não quebra a ordem, mas esconde o defeito se o portão errar** → os cenários
  do delta exigem as duas fontes intercaladas no tempo na mesma travessia por cursor, não só
  uma de cada.
- **A seção passa a fazer uma busca de bytes por produção aberta, sem freio** → só ao
  acionar, e nunca ao abrir a seção; o freio por origem do PRD-03 §8 segue valendo para a rota.
- **Mídia que não abre deixaria a linha quebrada** → a linha diz em linguagem simples que a
  produção não está disponível, sem revelar o motivo da recusa, e segue exibindo título, data,
  trilha e autoria.

## Migration Plan

Nenhuma migração de dados: a fatia só lê o que já está gravado. Os quatro campos novos do
payload são aditivos, e a rota de bytes nasce sem cliente anterior. Reverter é remover a
segunda fonte da listagem e a rota nova — nenhum dado fica órfão.
