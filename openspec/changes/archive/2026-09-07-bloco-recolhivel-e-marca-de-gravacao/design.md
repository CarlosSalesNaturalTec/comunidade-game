## Context

`openspec/specs/camada-visual-comum/spec.md` já fixa o piso das §§4, 5 e 6 do documento 15 —
alvo de toque, foco visível, nada só por cor, nenhum movimento decorativo — e já resolveu, com
o `Dialogo`, o caso de um comportamento que o navegador entrega de graça. As oito aplicações
consomem `comum/` sem construtor de estilo: CSS puro, propriedades personalizadas, sem
framework (documento 03 §1.2). O desenho abaixo se mantém nisso.

O que a fatia decide é pequeno e cabe em cinco pontos: qual elemento sustenta o recolhimento,
de onde vem o resumo, onde vive o estado aberto/fechado, de onde vem o momento da gravação e
quem o guarda na tela da trilha.

## Goals / Non-Goals

**Goals:** `BlocoRecolhivel` e `MarcaDeGravacao` em `comum/react`, cumprindo o documento 15
§§6.1 e 6.2; a adoção dos dois na tela da trilha da Área do Mestre, que é o caso que os
originou; a nota do tópico descartável no template da missão.

**Non-Goals:** a paginação por etapa do ciclo e o painel de travas, que são a fatia 17 do
PRD-09; as outras sete aplicações; o temperamento Arena; qualquer requisito de produto novo;
qualquer campo novo no núcleo.

## Decisions

1. **`BlocoRecolhivel` é `details`/`summary` nativo, não botão com região controlada.** O
   navegador entrega o estado, o teclado e a semântica de expansível, e `details` fechado não
   renderiza o conteúdo — o que é justamente o ganho numa tela de sessenta blocos. É a mesma
   escolha que o `Dialogo` fez com `dialog`. O componente acrescenta o resumo na linha, o
   rótulo textual e a supressão do marcador nativo, substituído por rótulo que diz o estado.
   _Descartado:_ `button` + `aria-expanded` sobre uma `div` — reimplementaria o que o navegador
   já faz, com mais chance de erro de acessibilidade.

2. **O resumo é dado por quem monta o bloco, e o componente não conhece o domínio.**
   `BlocoRecolhivel` recebe título e resumo; quem sabe dizer "2 entradas" ou "nenhum" é a tela.
   _Descartado:_ o componente contar filhos — acertaria na lista e erraria em todo bloco cujo
   estado não é uma contagem, como a cadência de retomada.

3. **O estado aberto/fechado é interno ao componente, e nasce fechado a cada montagem.**
   Nada na tela precisa saber que bloco está aberto, e a decisão do fundador é que todos nasçam
   fechados. _Descartado:_ estado controlado pelo pai, que espalharia dez `useState` por missão
   sem ninguém para lê-los; _descartado:_ lembrar a escolha entre visitas, que exigiria guardar
   preferência de tela — coisa que não existe em lugar nenhum do projeto.

4. **O momento da marca é o do aparelho, no retorno da escrita, e vale pela sessão.** A marca
   nasce quando a chamada volta sem erro e vive no estado do bloco que gravou; ao recarregar a
   página não há marca, porque nesta sessão nada foi gravado ainda — o que a spec já diz ("bloco
   que ainda não gravou nada não apresenta marca"). _Descartado:_ tirar o momento do servidor —
   as rotas dos onze blocos não devolvem instante de atualização, e criá-lo seria campo novo no
   núcleo, isto é, requisito novo, que não nasce numa change.

5. **Quem guarda o momento é o componente que monta o bloco, não o que faz a escrita.** Seis
   das onze escritas acontecem em formulário que **fecha ao gravar** — atividade, conteúdo,
   bibliografia, desafio de coleta, culminância e missão —, e um componente desmontado não
   sustenta marca nenhuma. O instante sobe pelo mesmo retorno (`onSalvo`) que já leva o dado
   gravado, e o bloco, que permanece, o guarda. Nas cinco escritas que acontecem no próprio
   bloco — cadência, desbloqueio, ODS da trilha, ODS da missão e recompensa —, ele já é o dono.
   `MarcaDeGravacao` é apresentação pura: recebe o instante e o formata. _Descartado:_ guardar
   o instante no formulário — a marca sumiria no mesmo ato que a produziu; _descartado:_ um
   contexto React que registrasse gravações por bloco — indireção para um dado que o bloco já
   tem em mãos.

6. **A adoção recolhe os dez blocos por missão e mantém a linha da missão sempre visível.** A
   linha com posição, título, sondagem, etapa e obrigatoriedade é o que distingue uma missão da
   outra: se ela recolhe, a lista deixa de ser navegável. "Pré-visualizar missão" é ação, não
   bloco de declaração, e continua botão. _Descartado:_ recolher a missão inteira num só bloco —
   esconderia o esqueleto junto com o detalhe.

## Risks / Trade-offs

- **`details` fechado não renderiza o conteúdo, e teste que buscava um campo sem abrir o bloco
  passa a falhar.** É o comportamento desejado, mas alcança `trilhas.test.tsx`, que hoje acha
  tudo de uma vez; os testes da tela passam a abrir o bloco antes de agir, como o usuário faz.
- **Onze blocos ganham um `useState` a mais cada.** É repetição assumida: a alternativa —
  centralizar o registro das gravações — custaria mais do que resolve, e o padrão de cada bloco
  cuidar da própria escrita já é o da tela.
- **A marca some ao recarregar a página.** Consequência da decisão 4, e a única saída seria
  campo novo no núcleo. Quem recarrega e não vê marca vê o dado gravado na tela, que continua
  vindo do servidor.
