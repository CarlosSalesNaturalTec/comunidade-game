# Design

## Context

Ver `proposal.md` — Why. A spec alterada é a do requisito "O Guerreiro(a) entra por nick e
imagem, e só o caminho Presença registra a presença", em
`openspec/specs/aplicacao-da-aula-presencial/spec.md`.

`TelaDeEntradaDoGuerreiro` já recebe `caminho: CaminhoDaEntrada` e já o usa para decidir
comportamento. O que falta é levá-lo ao texto: os dois `Cabecalho` da tela trazem título fixo.
A correção é local ao componente — nenhuma outra tela, rota ou API é tocada.

## Goals / Non-Goals

**Goals:**

- O título da entrada sai do `caminho`, nas duas telas do componente.
- O teste passa a distinguir os quatro caminhos, em vez de casar com todos.

**Non-Goals:**

- Mudar subtítulo, corpo, botões ou qualquer comportamento da entrada.
- Mexer na `TelaInicial`, na `GuardaDePresenca` ou nas telas de desfecho da presença.

## Decisions

1. **Um mapa `Record<CaminhoDaEntrada, string>` no módulo, ao lado das demais constantes de
   mensagem, em vez de ternário em cada `Cabecalho`.** O componente já concentra as frases em
   constantes nomeadas no topo (`MENSAGEM_DE_RECUSA`, `MENSAGEM_DE_PIN_ERRADO` e as outras);
   o mapa segue essa convenção e mantém as quatro redações juntas e conferíveis contra a tabela
   da `proposal`. _Descartado:_ ternário em cada título — duplicaria a redação nas duas telas e
   deixaria as duas livres para divergir.

2. **As duas telas usam o mesmo mapa.** O caminho é o mesmo; a forma da entrada — reconhecimento
   ou confirmação — já se distingue pelo subtítulo e pelos campos. _Descartado:_ um título por
   par (caminho × forma) — oito redações para uma distinção que o subtítulo já faz.

3. **O subtítulo fica como está nas duas telas.** Ele descreve o ato, que não muda com o
   caminho. A spec exige que a tela anuncie o caminho, não que reescreva o ato.

4. **O marcador de tela nos testes passa a ser o título do caminho.** Hoje
   `inicio.test.tsx` usa `/quem está chegando/i` para afirmar "chegou à presença", expressão que
   casa com os quatro caminhos — é o que deixou o defeito passar pela fatia 18. Com o título por
   caminho, o mesmo marcador volta a ser específico, e ganha cobertura a entrada pelos caminhos
   das equipes, do quiz e da troca.

## Risks / Trade-offs

- **Teste que hoje passa pelo motivo errado pode continuar passando pelo motivo errado** →
  antes de alterar o componente, rodar o teste do recorte e confirmar que o marcador novo falha
  no código atual; só então corrigir.
- **Redação divergindo da aprovada pelo fundador** → a tabela da `proposal` é a referência, e o
  mapa único a mantém num lugar só.
