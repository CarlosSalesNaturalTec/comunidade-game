## Context

`openspec/specs/identidade-do-adulto/spec.md` já traz a conferência restrita a nicks de adulto,
a unicidade global e a definição do próprio nick pelo adulto autenticado;
`openspec/specs/prova-de-habilidade/spec.md` traz a publicação e a remoção do artefato pelo
Mestre, com o do cadastro irremovível. Esta fatia fecha o que ficou pela metade nas duas: o
avatar, a leitura da própria identidade e a edição do artefato.

A rota do Apoiador — `PUT`/`GET /v1/eu/apoiador/identidade` — é o precedente inteiro: mesma
forma de entrada com os dois campos opcionais, mesma guarda de papel. A diferença é o **piso de
10 moedas** do avatar, que `RN-14-11` prende à marca do Apoiador e não alcança o Mestre.

## Goals / Non-Goals

**Goals:** `RF-09-114` atendido dos dois lados — nick e avatar —, com a leitura que a tela
exige; a edição de artefato do Mestre, com o do cadastro editável, irremovível e rastreável; a
gestão vendo o original.

**Non-Goals:** cadastrar Mestre, editar nome, e-mail ou papel, remover artefato de cadastro,
mexer no caminho do Apoiador, e dar à gestão qualquer edição de cadastro de adulto.

## Decisions

1. **A entrada da identidade do Mestre passa a ser a mesma do Apoiador, menos o piso.**
   `DefinirNickEntrada`, que só tem `nick`, dá lugar a uma entrada com `nick` e `avatar`
   opcionais; `definir_avatar_do_mestre` grava sem consultar moeda alguma. _Descartado:_
   reaproveitar `definir_avatar_do_apoiador` com o piso desligado por parâmetro — esconderia
   dentro de uma função a regra de que o piso é do Apoiador.

2. **`GET /v1/eu/mestre/identidade` devolve só nick e avatar.** A saída do Apoiador carrega
   moedas acumuladas, liberação e o que falta para o avatar próprio — tudo `RN-14-11`, que não
   alcança o Mestre. _Descartado:_ reusar `IdentidadeDoApoiadorSaida` — serviria campo de moeda
   a quem não tem regra de moeda.

3. **O original é coluna do artefato, preenchida uma vez.** `endereco_original` e
   `rotulo_original` nascem nulos e são gravados na **primeira** edição de um artefato de
   cadastro, com `editado_em`; edição seguinte só troca o valor vigente. Assim "permanece"
   passa a ter prova, e a leitura da gestão distingue o que foi mexido. _Descartado:_ histórico
   completo de versões — é auditoria, que o Ciclo 01 adiou (`RF-09-48`, Ciclo 02).

4. **A posse continua na regra, e a distinção do cadastro continua sendo
   `declarado_por_id`.** A edição exige Mestre do próprio perfil, como a publicação e a
   remoção já exigem; o que `declarado_por_id` decide deixa de ser "pode mexer" e passa a ser
   só "pode remover" e "guarda o original". _Descartado:_ operação nova na matriz de permissões
   — ela não distingue perfil próprio de alheio, que é o que importa aqui.

5. **A ficha da gestão marca e mostra, não compara.** Artefato editado aparece com o valor
   vigente e, abaixo, o original, rotulado como declarado no cadastro. _Descartado:_ fila de
   conferência na gestão — cresceria a fatia e o fundador não a pediu.

## Migration Plan

Três colunas nulas em `artefato_comprobatorio`, com revisão do Alembic que cria e derruba.
Nenhum dado existente muda: artefato nunca editado permanece com as três nulas, e é assim que a
leitura o reconhece como não mexido.
