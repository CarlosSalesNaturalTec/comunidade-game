## Context

Ver `proposal.md` — Why. O padrão de envio já está consolidado em
`openspec/specs/conteudo-da-missao/spec.md` e implementado em `nucleo/conteudos`: sessão
retomável aberta pelo núcleo, bytes direto ao armazenamento, referência gravada e conferida na
confirmação. Esta fatia o aplica à `PerguntaDoDesbloqueio` (fatia 18) e decide só o que aquele
padrão não cobre: a imagem que sobrevive à substituição das perguntas, e a leitura dos bytes,
que **nenhuma** rota do núcleo faz hoje.

## Goals / Non-Goals

**Goals:**

- Anexar, trocar e remover a imagem de cada pergunta do quiz, dentro de 1 MB e dos formatos de
  imagem da lista fechada.
- Corrigir texto do quiz sem reenviar arquivo algum.
- Exibir a imagem a quem já pode ver a pergunta, e a mais ninguém.
- Devolver a redeclaração do desafio ao estado em que ela nunca falha.

**Non-Goals:**

- Leitura de bytes dos demais arquivos enviados — vídeo, áudio, PDF e imagem do conteúdo da
  missão: mesma lacuna, alcance maior que esta fatia.
- Remoção de arquivo do armazenamento; nada aqui apaga bytes.
- Redimensionar, converter ou comprimir a imagem no núcleo ou no navegador.

## Decisions

**1. A imagem é coluna da pergunta, não entidade própria.** `imagem_referencia`,
`imagem_tipo` e `imagem_tamanho` em `PerguntaDoDesbloqueio`, como `ConteudoDaMissao` já faz.
Uma por pergunta é cardinalidade 1:1, e a spec já a fixa. _Descartada:_ tabela
`imagem_da_pergunta`, que só acrescentaria junção.

**2. A referência é `perguntas-do-desbloqueio/{id}/imagem`, e não se renomeia.** A referência
nasce do id da pergunta que existia no momento do envio; quando a pergunta é substituída, a
nova linha recebe a **mesma string**, e o objeto continua onde está. _Descartada:_ copiar ou
renomear o objeto para o id novo — custo de bytes a cada correção de vírgula, que é
exatamente o que a decisão do fundador quis evitar.

**3. A referência que volta é conferida contra as perguntas vigentes daquela missão.** O
cliente devolve a referência; o núcleo só a aceita se ela estiver entre as das perguntas que a
missão tinha antes da substituição. Sem isso, o campo seria um endereço de armazenamento
escolhido pelo cliente — porta aberta para apontar arquivo de outra trilha. _Descartada:_
aceitar qualquer string, e conferir só o prefixo.

**4. Substituir a pergunta deixa de apagá-la: ela é marcada.** `substituida_em` nasce nulo e
é carimbado na redeclaração; `perguntas_do_desbloqueio` — o único acessor — passa a filtrar as
vigentes. A unicidade de (missão, ordem) vira **índice parcial** `WHERE substituida_em IS
NULL`, como a unicidade da sondagem por trilha já é feita em `Missao`. Isso conserta o 500 da
fatia 18 e cumpre o `RN-05-47`: a resposta gravada continua apontando a pergunta que foi
respondida, com o enunciado e as alternativas que ela tinha. _Descartadas:_ apagar as
respostas junto (o `RN-05-47` proíbe); copiar enunciado e alternativa para dentro da resposta
(duplicação de dado que a pergunta guardada já tem).

**5. A leitura dos bytes é rota própria da imagem, não rota genérica de referência.**
`GET /v1/perguntas-do-desbloqueio/{id}/imagem` devolve os bytes com o tipo do envio, pela
`PortaDeArmazenamento.ler`, que os dois adaptadores já implementam. A autorização é a mesma
que já decide quem lê a pergunta: o Mestre autor da trilha, ou o Guerreiro(a) inscrito nela.
_Descartadas:_ rota que sirva qualquer referência (o cliente escolheria o arquivo, e a
autorização não teria como decidir); URL assinada do Cloud Storage (o `PortaDeArmazenamento`
não a tem, o adaptador de disco não a faria, e a inscrição — que é quem autoriza — só o núcleo
sabe). Servir 1 MB pelo núcleo é aceitável: o que a arquitetura mantém fora dele é o **envio**,
de até 200 MB.

**6. A tela busca os bytes e cria a URL local.** Toda rota sob `/v1` exige a chave da aplicação
em cabeçalho, e `<img src>` não manda cabeçalho. O `comum/api` ganha uma leitura que devolve
`Blob`; a tela a transforma em `URL.createObjectURL` e a revoga ao desmontar. _Descartada:_
abrir a rota da imagem sem chave, que contraria o documento 03 §1.

**7. O envio reaproveita o que a App 09 já tem.** `enviarArquivo` e
`consultarProgressoDaSessao` não conhecem conteúdo: recebem o endereço da sessão. Só a abertura
é nova, porque o caminho é outro.

## Risks / Trade-offs

- **Imagem órfã no armazenamento** — a referência que não volta deixa de ser apontada e os
  bytes ficam. → É escolha, não descuido: a trilha duplicada aponta a **mesma** referência, e
  apagar bytes quebraria a cópia de outro Mestre. A plataforma não mede armazenamento
  (`RN-09-07`), e 1 MB por pergunta não sustenta rotina de limpeza.
- **Pergunta substituída acumula linha** — redeclarar muitas vezes deixa várias gerações na
  tabela. → São o registro que o `RN-05-47` exige; saem de toda leitura pelo filtro do acessor
  único, e o índice parcial impede colisão de ordem.
- **A imagem pesa no aparelho do Guerreiro(a), em rede fraca** — é o motivo do teto de 1 MB
  (documento 03 §11). → A tela carrega a imagem **por pergunta**, e a falha em carregar nunca
  impede responder.
- **A rota nova é o primeiro caminho de saída de bytes do núcleo** — errar a autorização
  vazaria arquivo. → A autorização é a mesma função que já decide a leitura da pergunta, e os
  testes cobrem os três recusados: Mestre que não é autor, Guerreiro(a) não inscrito e persona
  de outro papel.

## Migration Plan

Revisão única do Alembic: acrescenta as quatro colunas, todas nulas, e troca a
`UniqueConstraint` de (missao_id, ordem) pelo índice parcial. Nada a transportar — as
perguntas existentes nascem sem imagem e vigentes. A paridade entre `alembic upgrade head` e
`Base.metadata`, que `test_migracoes.py` já confere, cobre a revisão.
