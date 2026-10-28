# Proposal

## Why

Fatia **24 do PRD-09** (`openspec/cronograma-de-fatias.md`). Atende `RF-09-123` a
`RF-09-126`, `RN-09-45` e `RN-09-46`, as seis entradas que as decisões do fundador de
2026-10-27 criam no PRD-09 §8.

O conteúdo da missão é rua de mão única. O núcleo só sabe criar (`POST
/v1/missoes/{id}/conteudos`), abrir e confirmar envio, e servir bytes; não há `PATCH` nem
`DELETE` do conteúdo. A App 09 acompanha: `FormularioDeConteudo` só cria, e a lista imprime
o valor cru do tipo — três conteúdos de texto na mesma missão aparecem como três linhas
iguais dizendo "texto", sem nada que os distinga. Um erro de digitação no corpo, um endereço
de vídeo errado ou uma fonte de terceiro mal escrita são permanentes, e o único caminho de
correção é criar outro conteúdo ao lado do errado.

A falta tem **duas** consequências que vão além do incômodo.

**A spec afirma o que nunca foi construído.** `openspec/specs/area-do-mestre/spec.md` já diz,
no requisito "O Mestre escreve o conteúdo da missão", que a aplicação "SHALL apresentar o
conteúdo já escrito na ordem declarada e permitir **reordená-lo, alterá-lo e removê-lo** antes
de publicar" — comportamento que nenhuma rota e nenhuma tela sustentam. É a mesma classe de
defeito das linhas "Leitura de conteúdo e bibliografia pelo Mestre" e "Leitura do desafio de
desbloqueio pelo Mestre" do cronograma. Pior: a frase não tinha âncora no PRD, porque
`RF-09-14` e `RF-09-15` tratam de **escrever**, não de corrigir — é regra que nasceu num
artefato do OpenSpec, o que `openspec/config.yaml` veda. Os `RF` novos lhe dão a âncora que
faltava.

**A ordem não existe na prática.** `FormularioDeConteudo.tsx` manda `ordem: 1` em todo
conteúdo. O núcleo lê com `order_by(ConteudoDaMissao.ordem)`, então todos empatam e a sequência
que o Guerreiro(a) lê fica indefinida — justamente depois de duas fatias terem feito dessa
sequência algo que importa (`2026-09-27-um-conteudo-por-vez-e-o-secundario-recolhido` e
`2026-10-15-ordem-da-tela-da-missao-em-quatro-grupos`). O Mestre nunca teve como declarar a
ordem que a spec diz que ele declara.

## What Changes

As quatro decisões do fundador de 2026-10-27 entram no documento 03 §11, no documento 09 §1 e
no PRD-09 §8 antes de virar código (§ *Impact*).

- **Nasce `PATCH /v1/conteudos/{id}`** (`RF-09-123`), privativo do Mestre autor da trilha,
  alcançando **corpo**, **endereço**, **autoria** e **fonte**. As mesmas recusas da criação
  valem na correção: texto sem corpo e link externo sem endereço respondem **422**, e autoria
  de terceiro sem fonte também. **Tipo e arquivo ficam fora** (`RN-09-45`): trocar um deles é
  remover o conteúdo e cadastrar outro.
- **Nasce `DELETE /v1/conteudos/{id}`** (`RF-09-124`), privativo do Mestre autor, que apaga a
  linha **de verdade** — nada aponta para `conteudo_da_missao` — e chama
  `armazenamento.remover` quando há arquivo confirmado, para não deixar bytes órfãos num
  armazenamento que o projeto deliberadamente não mede (`RF-09-20`).
- **Correção e remoção valem em qualquer situação da trilha**, publicada inclusive. Isso
  **altera** a spec da `area-do-mestre`, que hoje restringe as três operações a "antes de
  publicar": a decisão do fundador de 2026-10-27 segue a mesma gramática que
  `desbloqueio-da-missao` já fixou para a redeclaração do desafio — o que já foi gravado por
  Guerreiros e Guerreiras não é apagado nem alterado.
- **O bloco Conteúdo passa a identificar e a exibir** (`RF-09-125`). Cada conteúdo ganha
  **rótulo derivado** — primeiras palavras do corpo, domínio do link, nome do arquivo — e a
  exibição do próprio conteúdo. Texto e link saem embutidos, que não custam requisição;
  imagem, vídeo e arquivo de apoio só buscam os bytes **quando o Mestre pede** (`RN-09-46`),
  porque `BlocoRecolhivel` monta os filhos mesmo fechado e exibir tudo de saída faria a
  abertura da tela da trilha puxar os arquivos de todas as missões da etapa pelo núcleo.
- **O Mestre declara a ordem movendo o conteúdo na lista** (`RF-09-126`), para cima ou para
  baixo, por `POST /v1/conteudos/{id}/ordem`. O `ordem: 1` pregado é corrigido, e o que já está
  gravado é renumerado por migração.
- **BREAKING**: `ordem` deixa de ser campo do corpo de `POST /v1/missoes/{id}/conteudos` — o
  núcleo passa a atribuí-la, posterior à dos conteúdos que a missão já tem. Com
  `extra="forbid"`, mandar o campo responde **422**. Declarar a ordem passa a ser **mover**, não
  digitar um número; enquanto o cliente declarasse o número, ele declararia 1. O único cliente
  que o manda é a App 09, que vem no mesmo PR.

**Fora do escopo.** A **atividade** da missão é a fatia 25 do cronograma, com change e PR
próprios: ela não se apaga, e o recorte dela arrasta quatro capacidades em leitura. Seguem
igualmente fora, como o PRD-09 §3.2 já exclui, a conferência prévia do que é enviado — que é
auditoria por amostragem do Admin — e qualquer medição de armazenamento consumido
(`RF-09-20`, `RN-09-07`).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `conteudo-da-missao`: o conteúdo passa a se corrigir em corpo, endereço, autoria e fonte, e
  a se remover com o arquivo que tiver; tipo e arquivo não se alteram; a ordem é declarada
  pelo Mestre e deixa de nascer igual para todos.
- `area-do-mestre`: o bloco Conteúdo identifica cada item por rótulo derivado, exibe-o — sob
  demanda no que tem arquivo —, corrige, remove e reordena, e as três operações deixam de
  estar restritas a "antes de publicar".

## Impact

- `backend/src/nucleo/conteudos/regra.py` — `corrigir_conteudo`, `remover_conteudo` e
  `mover_conteudo`, com a guarda de autoria que `criar_conteudo` já aplica e as mesmas
  recusas de coerência por tipo.
- `backend/src/nucleo/conteudos/rotas.py` — `PATCH` e `DELETE` de `/conteudos/{id}`, e a rota
  que move o conteúdo na ordem.
- `backend/alembic/versions/` — revisão que renumera o conteúdo já gravado, hoje todo em
  `ordem = 1`, pela sequência de criação dentro de cada missão.
- `apps/app-09-mestre/src/trilhas/api.ts` — as chamadas novas.
- `apps/app-09-mestre/src/trilhas/FormularioDeConteudo.tsx` — passa a servir criação **e**
  correção; a chave do rascunho em `localStorage`, hoje indexada só pela missão, desce ao
  conteúdo para que edição e criação não se sobrescrevam.
- `apps/app-09-mestre/src/trilhas/ListaDeMissoes.tsx` — o bloco Conteúdo com rótulo, exibição
  sob demanda, editar, remover, subir e descer.
- `apps/app-09-mestre/src/trilhas/PreVisualizacaoDaMissao.tsx` — `ConteudoPreVisualizado` sai
  para módulo próprio e é reusado pelo bloco de cadastro, que precisa concordar com ele.
- Documentação, no mesmo PR: documento 03 §11 (marcador novo), documento 09 §1 (a linha da
  decisão), PRD-09 §8 (os quatro `RF` e as duas `RN`) e a situação da fatia 24 no
  `openspec/cronograma-de-fatias.md`.
