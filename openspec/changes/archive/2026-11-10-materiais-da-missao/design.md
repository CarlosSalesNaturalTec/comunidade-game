# Design

## Context

Fatia que aplica padrões já consolidados: a correção da missão (`trilha-e-missao`, fatia 28 —
campos opcionais, autoria estrita, `extra="forbid"`), a duplicação da trilha (fatia 13) e a
programação do encontro (`aplicacao-da-aula-presencial`, `RF-04-35`). O desenho cobre só o
campo novo.

## Goals / Non-Goals

**Goals:** o Mestre autor declara e corrige os materiais da missão na App 09; a App 01 os mostra
na programação do encontro.

**Non-Goals:** pré-requisito da trilha (descartado); vínculo com recurso, necessidade ou
patrimônio; exibição na vitrine ou na App 05.

## Decisions

1. **Coluna `missao.materiais`, `ARRAY(Text)`, não nula, com padrão `'{}'`.** As missões já
   gravadas ficam com lista vazia, sem _backfill_. Mesmo tipo da `cadencia_de_retomada`.
   Descartada: tabela própria — item sem atributo nem referência não pede entidade.
2. **O campo entra nas portas que já existem**: `CriarMissaoEntrada` e `CorrigirMissaoEntrada`
   ganham `materiais: list[str] | None`, e `criar_missao`/`corrigir_missao` o conferem por uma
   função única, `_conferir_materiais_da_missao`. Descartada: rota própria
   `PUT /v1/missoes/{id}/materiais` — duplicaria a autoria e a recusa que o `PATCH` já tem.
3. **Conferência mínima**: tira os espaços das pontas e recusa item vazio com 422. Sem teto de
   itens nem de tamanho, nem remoção de repetidos: nenhum número foi decidido.
4. **`materiais` vai em `MissaoSaida`**, com padrão `[]`, porque criação e correção respondem por
   ela e `MissaoDoMestreSaida` a herda. A leitura pública da trilha passa a carregá-lo também,
   sem tela que o mostre. Descartada: tipo de saída paralelo só para a autoria.
5. **Programação do encontro**: o item ganha `missao_materiais: list[str]`, ao lado de
   `missao_titulo`. A App 01 mostra a lista na tela da programação, antes do conteúdo.
6. **App 09**: o `FormularioDeMissao`, que já serve criação e correção, ganha o campo com
   entrada de texto, "Acrescentar" e remover por item. Na correção manda `materiais` só se a
   lista mudou, para não reescrever o que não foi tocado.
7. **Duplicação**: `duplicar_trilha` copia `materiais` junto dos demais campos da missão.

## Risks / Trade-offs

- **A programação da App 01 é a tela da equipe**: as crianças também veem os materiais. O
  fundador escolheu a App 01 sem fixar a tela; se preferir o grupo "Para quem opera o
  aparelho", muda só a tela, não o contrato.
- Lista sem teto: um Mestre pode declarar muitos itens. Aceito enquanto não houver número
  decidido.
