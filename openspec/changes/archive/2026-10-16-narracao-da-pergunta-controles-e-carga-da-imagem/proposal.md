# Proposal

**Origem:** PRD-04 (Aula presencial, App 01), fatia **28** do
`openspec/cronograma-de-fatias.md`. Alcança `RF-05-11`, `RF-05-13`, `RF-05-89`, `RF-09-119`,
`RF-04-35` e `RN-05-45`. **Nenhum identificador novo nasce aqui:** pelo precedente das fatias
23 e 25, narração entra direto do documento 15 §5.1 e não tem `RF`/`RN` no PRD-04, posição de
botão é apresentação que nenhum enunciado fixa, e o item da imagem é correção de defeito. A
§14 do PRD-04 e o documento 09 §1 não têm pendência que trave este recorte.

**Decisão do fundador de 2026-10-16**, em quatro partes, elicitada em exploração.

## Why

A tela "Trilhas e missões" da App 01 tem três defeitos que atingem justamente quem a
plataforma mais quer alcançar — a criança que ainda não lê com fluência.

1. **A pergunta do quiz não fala.** O documento 15 §5.1 já lista "enunciado de pergunta" entre
   o texto curto que fala sozinho, e a spec `narracao-por-sintese-de-fala` repete o enunciado
   literalmente. Mas a fatia 23 deu roteiro só ao alternador, ao Quiz ao Vivo e ao "Ouvir este
   texto": `comum/trilha` ficou **sem roteiro algum**. Na sondagem a narração fala o título da
   tela e o aviso de enquadramento — que vêm de graça do `Cabecalho` e do `Aviso` — e cala a
   pergunta. É **requisito vigente não implementado**, não decisão nova.
2. **Os controles do desafio contam o que não precisa e permitem o que não deveria.** A tela
   anuncia "Pergunta x de y", que é ruído numa Arena de uma decisão por tela, e oferece o envio
   com perguntas em branco, resolvendo o inválido depois do toque em vez de antes.
3. **A imagem da pergunta anterior fica na tela sob o enunciado novo.** Defeito de estado em
   `MidiaDoNucleo`, não lentidão de rede: informação errada apresentada como se fosse a
   correta, com o indicador de carga já escrito e inalcançável. O mesmo defeito está no
   conteúdo da missão.

## What Changes

### 1. A pergunta do quiz passa a ser narrada

- Cada pergunta é falada **individualmente**, ao **avançar e ao retornar**, com **enunciado +
  alternativas**. Só o enunciado — o recorte do Quiz ao Vivo, onde o tempo de resposta é curto
  — deixaria quem ainda não lê com a pergunta ouvida e as respostas inalcançáveis; a sondagem
  não tem cronômetro.
- A fala é montada a partir do **array de alternativas da pergunta**, nunca do documento
  apresentado, e disparada na **mudança de `pergunta.id`**.
- **BREAKING (contrato da camada):** é o primeiro texto **montado para a voz** da plataforma.
  Até aqui o `aria-hidden` que a spec da narração exige nunca escondeu nada, porque tudo o que
  se falava já era texto visível declarado pela tela. O requisito precisa reconciliar os dois
  casos.
- A App 05 **não** recebe a voz: segue sem montar `ProvedorDeNarracao`, e o roteiro nasce
  inerte nela — mesmo arranjo da fatia 23.

### 2. Os controles do desafio

- **BREAKING:** "Pergunta x de y" **sai de vez**, do paginador comum **inteiro** — quiz,
  conteúdo da missão e tela da programação — e **também** de quem usa leitor de tela. Nada
  migra para o `<legend>` nem para rótulo de região. Reverte o `SHALL` de "a tela diz onde está
  na sequência" nas duas specs que o carregam; o fundador escolheu o alcance largo sabendo que
  nos conteúdos da missão nada mais numera o item.
- Morre com a frase a propriedade `nome` do paginador, que só existia para montá-la.
- "Enviar respostas" desce para a **mesma linha** de "Próxima pergunta" e "Pergunta anterior",
  o que pede encaixe de ações no paginador, com guarda para o quiz de **uma** pergunta — onde a
  linha de controles não renderiza e o botão desapareceria.
- **BREAKING:** o envio só habilita quando **todas** as perguntas estiverem respondidas, sem
  linha explicativa. Isso **aposenta** o mecanismo de hoje — o estado `faltando`, o aviso
  "Falta responder N pergunta(s)" e o salto até a primeira pendente — e, com ele, o único
  retorno **falado** do que falta, porque aquele aviso é narrado de graça. O fundador aceitou o
  preço conhecendo-o.
- A regra vale **só** para `tipo == "quiz"`: o desafio de declaração não tem pergunta e segue
  habilitado.

### 3. A carga da imagem

- `MidiaDoNucleo` passa a **reiniciar o estado** na troca de item, o que faz aparecer o
  indicador de carga que já existe e elimina a mídia obsoleta, a URL revogada em uso e o erro
  que gruda de um item no seguinte.
- A correção é **dentro** do componente, não por `key` no quiz: assim alcança também o
  conteúdo da missão, que tem o defeito idêntico.
- Avançar e voltar ficam **desabilitados** enquanto a mídia carrega, com **válvula de escape**
  na falha — sem ela, rede ruim vira beco sem saída.

## Capabilities

### New Capabilities

Nenhuma. Os três itens alteram comportamento já especificado.

### Modified Capabilities

- `narracao-por-sintese-de-fala`: o que a camada fala numa sequência paginada — enunciado **e**
  alternativas da pergunta, uma por vez, ao avançar e ao retornar — e a reconciliação do
  `aria-hidden` para o texto montado a partir de dado da tela.
- `area-do-guerreiro`: três enunciados. O do desafio de desbloqueio perde o "leva o
  Guerreiro(a) até a pergunta que falta" e ganha o envio condicionado e o roteiro de narração;
  o do conteúdo da missão perde o "diz onde o Guerreiro(a) está na sequência"; o da moldura de
  tamanho fixo ganha o sinal de carga e a trava de navegação.
- `aplicacao-da-aula-presencial`: o enunciado do conteúdo um por vez perde o "diz onde a equipe
  está na sequência".

`camada-visual-comum` **não** entra: o paginador e a moldura de mídia não são especificados
ali. `area-do-mestre` **não** entra: as mídias da App 09 não são paginadas, e o defeito de
estado não se manifesta nela.

## Impact

**Camada comum**

- `comum/react/SequenciaPaginada.tsx` — sai a posição em texto e a propriedade `nome`; entra o
  encaixe de ações e a trava dos controles.
- `comum/react/MidiaDoNucleo.tsx` — reinício de estado na troca de item e o estado de carga
  informado para fora.
- `comum/react/estilos.css` — sai a regra `.cg-sequencia__posicao`.
- `comum/trilha/DesafioDeDesbloqueio.tsx` — roteiro de narração; envio condicionado; botão na
  linha de controles; remoção de `faltando`, do aviso de falta e do salto até a pendente.
- `comum/trilha/Missao.tsx` e `comum/trilha/estilos.css` — ajuste ao paginador sem `nome`; a
  classe `cg-trilha__pergunta--falta` deixa de ter uso.

**Aplicações**

- `apps/app-01-aula-presencial/src/trilhas/TelaDaProgramacao.tsx` — deixa de passar `nome`.
- App 05 recebe o comportamento pelos componentes comuns, **sem** a voz.

**Testes a corrigir** (asserem a frase que sai): `comum/react/SequenciaPaginada.test.tsx` e
`comum/trilha/trilha.test.tsx`.

**Documentação** (regra §3 de `CLAUDE.md`): documento 15 §6.4 é a fonte única de "um conteúdo
por vez" e hoje **não** manda declarar a posição — recebe a decisão de 2026-10-16 para que a
frase não volte por leitura futura; o documento 09 §1 recebe a linha da decisão; o
`openspec/cronograma-de-fatias.md` tem a linha da fatia 28, cuja situação fecha nesta change.
Nenhum PRD muda: os enunciados alcançados são curtos e não fixam a posição em texto nem o
salto até a pergunta pendente.

**Esteiras:** Biome e Vitest em `comum/` e `apps/*`; o lint de documentação e `mkdocs build
--strict` por causa dos documentos 15 e 09.
