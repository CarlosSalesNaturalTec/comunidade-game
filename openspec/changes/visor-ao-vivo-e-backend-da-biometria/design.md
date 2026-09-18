## Context

Ver `proposal.md` — Why. O que o desenho precisa saber: `comum/biometria` é o **único** módulo
que importa a Human, carrega modelo e toca `getUserMedia`, e a fronteira que ele estabelece — só
`boolean` e `number[]` saem dele — é o que garante o invariante 12 **por construção**. Quatro
telas de três aplicações o consomem; três delas são do App 01 e estão no recorte desta change.

A câmera já é aberta ali (`abrirCamera`), num elemento de vídeo criado e nunca anexado ao
documento. Pôr o visor na tela é, portanto, decidir **quem anexa esse elemento** — e é isso que
põe a fronteira em jogo.

## Goals / Non-Goals

**Goals:** fazer a captura concluir no aparelho do encontro; deixar visível a quem opera o que a
câmera está vendo; e impedir que uma falha de preparo volte a se disfarçar de ausência de
pessoa.

**Non-Goals:** o espelho na tela do App 05 (recorte do PRD-05, decisão do fundador 2026-09-17);
trocar o secret do limiar, que segue como tarefa em aberto da change da bancada; e qualquer
mudança no núcleo.

## Decisions

**1. O backend da Human passa a ser declarado, e é `webgl`.** Hoje a configuração o omite, e a
biblioteca autosseleciona `webgpu` sempre que `navigator.gpu` existir — o que é verdade em
Chrome mesmo onde `requestAdapter()` devolve `null`. O `webgl` é o denominador comum dos
aparelhos modestos que o documento 03 §3.2 assume, e a escolha deixa de depender do que o
navegador do encontro reporta. _Alternativa descartada:_ manter a autosseleção e tratar a falha
— sobra a mesma negociação frágil no caminho de toda captura, num aparelho compartilhado onde
ninguém vai ler console.

**2. O espelho é acoplado pelo módulo, não entregue à tela.** `comum/biometria` passa a expor
uma função que recebe o **elemento contêiner** que a tela forneceu e anexa ali dentro o próprio
elemento de vídeo. A tela empresta um lugar; nunca recebe `MediaStream`, quadro ou pixel, e
continua sem ter como ler a imagem. A fronteira que garante o invariante 12 permanece de pé por
construção, e não por disciplina de quem escreve tela. _Alternativa descartada:_ devolver o
`MediaStream` para a tela renderizar — quebra a garantia, porque a partir dele qualquer tela
extrai quadro.

**3. A detecção corre em laço, e o acionamento deixa de ser o instante do julgamento.** Hoje um
único `detect()` decide, no quadro que existir no momento do clique — com a câmera recém-aberta
e a exposição ainda se ajustando. Passa a repetir até a vivacidade passar ou o tempo se esgotar,
e o retorno abstrato acompanha o laço. _Alternativa descartada:_ aguardar um tempo fixo antes do
tiro único — escolhe um número arbitrário e continua reprovando quem só precisava de mais um
segundo.

**4. O preparo é um passo com desfecho próprio.** Carregar modelo e abrir câmera deixam de
correr embutidos na prova de vivacidade: falham com frase própria, distinta da reprovação. É a
mesma correção de camada que a change do CORS do bucket e a da dimensão do descritor já fizeram
— e é a terceira ocorrência do mesmo padrão, o que faz dela requisito (`RF-04-65`) e não
cuidado de implementação. _Alternativa descartada:_ registrar a causa só no console — foi
exatamente o que deixou o defeito de pé neste último mês.

**5. O retorno é abstrato porque o quadro é proibido, não porque é mais bonito.** Rosto
enquadrado e vivacidade confirmada são estados, e a tela os mostra como estado. O visor é
permitido por ser visor; a imagem capturada não volta à tela em nenhuma das três (`RN-04-34`,
documento 99 §6 invariante 12).

## Risks / Trade-offs

**`webgl` é mais lento que `webgpu` onde a GPU existe** → o aparelho do encontro é modesto por
premissa, e a captura não é caminho de tempo crítico; concluir sempre vale mais que concluir
rápido às vezes.

**O visor aumenta o tempo com a câmera aberta** → `encerrarCaptura` continua sendo chamada ao
fim de toda tentativa, aprovada ou não, e a desmontagem da tela segue encerrando o fluxo; o que
muda é a pessoa saber por que está esperando.

**O laço pode não terminar** → o tempo máximo é parte do requisito, e esgotá-lo é desfecho
legível na tela, não silêncio.

**Visor e invariante 12** → o risco é de leitura, não de implementação: por isso a distinção
entre visor ao vivo e imagem capturada entra no invariante e no documento 03 §3.3 **nesta mesma
change**, e não fica só na spec.

## Migration Plan

1. Nenhuma migração, nenhuma rota, nenhuma mudança de contrato.
2. _Deploy_ da App 01. O App 05 recebe o conserto do backend no _deploy_ seguinte dele, por
   depender do mesmo módulo — a tela dele não muda nesta change.
3. Conferir no aparelho do encontro, com DevTools: as requisições a `/modelos-de-biometria/`
   passam a existir, e a captura conclui.
4. Feito isso, a medição do limiar pode enfim acontecer — tarefa 4.1 da change
   `2026-09-17-bancada-de-calibracao-do-limiar`.
5. _Rollback_: reverter o _merge_. Nada de estado a desfazer.
