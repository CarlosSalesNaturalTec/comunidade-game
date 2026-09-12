## Context

Ver `proposal.md` — Why. O que o desenho precisa respeitar já está de pé:

- `PerguntaDoDesbloqueio` é entidade própria desde a fatia 18, com `ordem`, as quatro
  alternativas, a correta e as três colunas da imagem. A unicidade de (missão, ordem) é índice
  **parcial** sobre as vigentes — `substituida_em IS NULL` —, justamente para que uma geração
  substituída conviva com a vigente.
- `RN-05-47`: pergunta que alguma submissão já respondeu nunca é apagada. `RespostaDaSubmissao`
  aponta `pergunta_id`, e é esse apontamento que o carimbo protege.
- A referência da imagem nasce do id da pergunta e **nunca se renomeia**
  (`referencia_da_imagem_da_pergunta`); conservar imagem é copiar a string, não mover arquivo.
- `declarar_desafio_de_desbloqueio` já carimba as vigentes e insere a geração nova, e
  `_conferir_perguntas_do_quiz` já é a conferência de completude do quiz.

## Goals / Non-Goals

**Goals:**

- Escrita por pergunta que não toca nas demais, reaproveitando a conferência e o carimbo que já
  existem em vez de duplicá-los.
- Manter o id da pergunta **estável** no caminho comum da autoria, para que a referência da
  imagem e a tela não precisem se reconciliar a cada correção.

**Non-Goals:**

- Reordenar perguntas por ato próprio — segue pela declaração do desafio inteiro (`specs`).
- Qualquer mudança na submissão, na aferição dos 60% ou na leitura do percurso.
- Renumerar a `ordem` das perguntas restantes depois de uma remoção.

## Decisions

**1. Três rotas por pergunta, ao lado da declaração, no vocabulário que o PRD-09 §9 já usa.**
`POST /v1/missoes/{id}/perguntas-do-desbloqueio` acrescenta,
`PUT /v1/perguntas-do-desbloqueio/{id}` corrige e
`DELETE /v1/perguntas-do-desbloqueio/{id}` remove. O prefixo de coleção e o endereçamento por
id são os mesmos das três rotas de imagem que já existem. `PUT`, não `PATCH`, porque a pergunta
só grava **completa** (`RN-09-44`): o corpo é a pergunta inteira, não um remendo.
_Descartado:_ aninhar tudo sob a missão (`/missoes/{id}/perguntas-do-desbloqueio/{ordem}`) —
endereçar por posição quebra assim que a ordem muda.

**2. Corrigir preserva o id quando ninguém respondeu; carimba quando alguém respondeu.** A
regra consulta `RespostaDaSubmissao` pela `pergunta_id`: sem nenhuma resposta, a linha é
**atualizada no lugar** e o id, a `ordem` e a imagem seguem os mesmos; havendo resposta, a
vigente recebe `substituida_em` e uma linha nova nasce na **mesma `ordem`**, copiando as três
colunas da imagem, como `_ImagemPreservada` já faz na declaração do todo.
_Por quê:_ `RN-05-47` protege a tentativa registrada; onde não há tentativa, não há o que
proteger, e o caminho comum desta fatia — o Mestre montando o quiz antes de a trilha ir ao ar —
fica com id estável, que é o que a tela e a referência da imagem precisam.
_Descartado:_ carimbar sempre — uniforme, mas troca o id a cada correção, obriga a tela a se
reconciliar e faz a tabela crescer por digitação.

**3. Acrescentar entra em `max(ordem) + 1` das vigentes; remover apenas carimba.** Remover não
renumera as restantes: a leitura ordena por `ordem` e conviver com lacuna (1, 2, 4) é mais
barato e mais seguro que reescrever linhas que o ato não mexeu. O índice parcial já garante que
a `ordem` livre de uma geração substituída não colide com a vigente.
_Descartado:_ compactar a `ordem` a cada remoção — escreve em perguntas que o Mestre não pediu
para mudar, contra o próprio requisito da fatia.

**4. A completude por pergunta reaproveita `_conferir_perguntas_do_quiz`.** A conferência
recebe a lista de uma pergunta só e devolve as mesmas recusas 422 por campo. Uma regra, dois
chamadores — a declaração do todo e a escrita isolada —, para que a exigência nunca divirja
entre os dois caminhos.

**5. Remover a última pergunta é recusado com 422.** Um quiz sem nenhuma pergunta é o estado
que `RN-09-43` já recusa na declaração; deixar a remoção por pergunta chegar lá abriria por uma
porta o que a outra fecha. _Ponto a confirmar com o fundador antes do `apply`_ — a alternativa
é permitir e devolver a missão ao estado "sem desafio", que hoje nenhuma rota produz.

**6. A tela guarda a pergunta gravada e a pergunta em edição.** Cada pergunta ganha marca de
gravação, erro e progresso próprios — os dois últimos já são por índice na tela de hoje. Anexar
imagem a pergunta sem id dispara a gravação dela e emenda o envio com o id que voltou; estando
incompleta, a tela mostra a recusa do núcleo naquela pergunta e não abre envio.
_Descartado:_ gravar a pergunta em segundo plano a cada digitação — o Mestre perde o controle
de quando o que escreveu virou definitivo.

## Risks / Trade-offs

- **Duas gerações na mesma `ordem` durante a correção carimbada** → o carimbo precede a
  inserção, com `flush` entre os dois, como a declaração do todo já faz; o índice parcial nunca
  vê duas vigentes.
- **A tela e o núcleo divergirem sobre o id depois de uma correção carimbada** → a resposta do
  `PUT` devolve a pergunta como ficou, id inclusive, e a tela substitui a que tinha. É o mesmo
  contrato da confirmação da imagem.
- **Lacuna na `ordem` confundir quem lê** → a `ordem` é sequência, não índice; a leitura ordena
  por ela e a tela numera as perguntas pela posição na lista, como já faz.
- **Imagem órfã quando a correção carimbada copia a referência** → não há órfã: a referência
  aponta o objeto do envio, que não se renomeia, e as duas gerações a compartilham. Remover a
  imagem segue sendo ato do Mestre, não efeito da correção.

## Migration Plan

Nenhuma migração de schema: as três rotas usam as colunas que a fatia 18 já criou e o índice
parcial que ela já declarou. A declaração do desafio inteiro não muda de contrato, de modo que
a App 05 e o percurso do Guerreiro(a) seguem sem tocar. Rollback é reverter o código.

## Open Questions

Nenhuma que trave o `apply`. A decisão 5 tem alternativa registrada e vai ao fundador junto com
a change; escolhida a outra, muda o cenário da remoção da última pergunta nas `specs` e uma
tarefa, sem alcançar o resto do desenho.
