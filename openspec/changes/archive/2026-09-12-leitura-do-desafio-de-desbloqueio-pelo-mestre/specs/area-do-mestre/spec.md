## MODIFIED Requirements

### Requirement: A App 09 monta o desafio de desbloqueio da missão

A aplicação SHALL permitir ao **Mestre autor** montar o **desafio de desbloqueio** de cada
missão da trilha que ele autora, escolhendo entre **quiz** e **desafio prático**. A tela SHALL
dizer que é esse desafio que **abre a missão seguinte** para o Guerreiro(a). Missão que ainda
**não tem** desafio declarado SHALL ser sinalizada na bancada, sem impedir a publicação da
trilha. Trilha de outro Mestre NEVER SHALL ser oferecida para edição.

No **quiz**, a tela SHALL permitir **acrescentar e remover perguntas**, sem limite de
quantidade, cada uma com o seu enunciado, quatro alternativas e a indicação de qual é a
correta, e SHALL preservar a ordem em que o Mestre as dispôs. A tela SHALL impedir a gravação
de um quiz **sem nenhuma pergunta**, dizendo o que falta. O resumo do bloco recolhível SHALL
dizer **quantas perguntas** o quiz tem. A tela SHALL dizer ao Mestre que **passa quem acerta ao
menos 60%** das perguntas, para que ele saiba o efeito de quantas escreve. (`RF-09-26`,
`RF-09-118`, `RN-09-43`)

A tela SHALL **reabrir o desafio já declarado** toda vez que o Mestre autor volta à missão,
em sessão nova inclusive: o tipo escolhido, o enunciado do prático e, no quiz, cada pergunta
com o seu enunciado, as quatro alternativas, a **alternativa correta marcada** e a imagem que
ela tem. A tela NEVER SHALL apresentar como "sem desafio" missão que tem desafio declarado,
nem no bloco nem no resumo da linha. Gravar de novo para corrigir texto NEVER SHALL, por si,
descartar pergunta ou imagem que o Mestre não removeu. (`RF-09-26`, `RF-09-118`, `RF-09-119`)

Cada pergunta do quiz SHALL oferecer **anexar uma imagem**, sempre opcional, e a tela SHALL
dizer o **teto de 1 MB** e os **formatos aceitos** antes do envio. Durante o envio a tela SHALL
mostrar o **progresso**; recusado o arquivo, SHALL dizer o motivo em linguagem do Mestre — o
formato que chegou e os aceitos, ou o tamanho e o teto —, sem apagar o que ele já escreveu na
pergunta. Pergunta que já tem imagem SHALL permitir **trocá-la** e **removê-la**, e a imagem
anexada SHALL **permanecer** quando o Mestre grava o desafio de novo para corrigir texto. A
tela NEVER SHALL exigir habilidade técnica: nem formato digitado, nem redimensionamento, nem
endereço de arquivo. (`RF-09-119`, decisão do fundador de 2026-09-11)

A imagem anexada SHALL ser **exibida ao Mestre autor** na pergunta a que pertence, e não
apenas anunciada em texto: o Mestre SHALL ver o que o Guerreiro(a) verá. A imagem que não
carregar NEVER SHALL impedir o Mestre de ler, corrigir ou gravar a pergunta — a tela diz que
não abriu e segue utilizável. (`RF-09-119`)

Na missão marcada como **sondagem**, a tela SHALL apresentá-la **como sondagem**, e não como
desbloqueio comum: o bloco SHALL se chamar **Sondagem**, SHALL dizer que ela **abre a trilha**
e mostra ao Mestre de onde a turma parte, e SHALL dizer que **não há passar nem reprovar** —
a trilha abre assim que o Guerreiro(a) responde. A tela NEVER SHALL anunciar o corte de 60%
na sondagem, porque ele não se aplica a ela (`RN-05-46`), e NEVER SHALL oferecer a escolha
entre quiz e desafio prático, porque a sondagem é **na forma de quiz** (`RF-09-81`). O aviso
de sondagem sem perguntas e o resumo da linha SHALL usar o mesmo vocabulário.
(`RF-09-81`, `RN-09-30`)

#### Scenario: O Mestre autor monta o desafio da sua missão

- **WHEN** o Mestre autor abre uma missão da sua trilha e monta o desafio de desbloqueio
- **THEN** a aplicação grava o desafio e a missão passa a exibi-lo

#### Scenario: O Mestre acrescenta e remove perguntas do quiz

- **WHEN** o Mestre autor acrescenta três perguntas ao quiz e remove a segunda
- **THEN** a tela mantém as duas restantes na ordem em que ficaram, e grava só elas

#### Scenario: Quiz sem pergunta não grava

- **WHEN** o Mestre autor escolhe quiz e tenta gravar sem nenhuma pergunta
- **THEN** a tela recusa a gravação e diz que o quiz precisa de ao menos uma pergunta

#### Scenario: O quiz declarado reabre preenchido em sessão nova

- **WHEN** o Mestre autor declarou um quiz, saiu da aplicação e volta à mesma missão
- **THEN** a tela apresenta as perguntas declaradas, com as alternativas e a correta marcada,
  e não um formulário vazio

#### Scenario: O resumo da linha reflete o desafio declarado em sessão nova

- **WHEN** o Mestre autor volta à trilha cuja missão tem quiz de três perguntas declarado
- **THEN** o resumo da linha diz que o quiz tem três perguntas, e não que a missão está sem
  desafio

#### Scenario: O desafio prático reabre com o enunciado declarado

- **WHEN** o Mestre autor declarou um desafio prático, saiu da aplicação e volta à missão
- **THEN** a tela apresenta o tipo prático escolhido e o enunciado declarado

#### Scenario: O Mestre anexa a imagem de uma pergunta

- **WHEN** o Mestre autor escolhe uma imagem para a terceira pergunta do quiz
- **THEN** a tela mostra o progresso do envio e, ao fim, a pergunta passa a exibir a imagem
  anexada

#### Scenario: Imagem recusada explica o motivo sem perder o que foi escrito

- **WHEN** o Mestre autor escolhe uma imagem de 4 MB para uma pergunta
- **THEN** a tela diz o tamanho do arquivo e o teto de 1 MB, e o enunciado e as alternativas já
  escritos permanecem na tela

#### Scenario: Corrigir o texto não apaga a imagem

- **WHEN** o Mestre autor corrige o enunciado de uma pergunta com imagem e grava o desafio de
  novo
- **THEN** a pergunta continua com a mesma imagem, sem novo envio

#### Scenario: O Mestre remove a imagem de uma pergunta

- **WHEN** o Mestre autor remove a imagem de uma pergunta e grava o desafio
- **THEN** a pergunta passa a constar sem imagem

#### Scenario: O Mestre autor vê a imagem que anexou

- **WHEN** o Mestre autor abre uma missão cujo quiz tem pergunta com imagem
- **THEN** a tela exibe a imagem naquela pergunta, e não apenas a informação de que ela existe

#### Scenario: Imagem que não abre não trava a edição

- **WHEN** o Mestre autor abre o quiz e a imagem de uma pergunta não carrega
- **THEN** a tela avisa que aquela imagem não abriu e o Mestre segue podendo corrigir e gravar
  a pergunta

#### Scenario: O Mestre anexa imagem a pergunta declarada em sessão anterior

- **WHEN** o Mestre autor volta à missão em sessão nova e escolhe uma imagem para uma pergunta
  já declarada
- **THEN** a tela envia a imagem daquela pergunta, sem exigir que ele grave o desafio de novo
  antes

#### Scenario: O resumo diz quantas perguntas o quiz tem

- **WHEN** o Mestre autor recolhe o bloco do desafio de desbloqueio de uma missão com quiz de
  oito perguntas
- **THEN** o resumo do bloco diz que o quiz tem oito perguntas

#### Scenario: A bancada sinaliza a missão sem desafio

- **WHEN** o Mestre autor abre uma trilha com missão que ainda não declarou desafio
- **THEN** a missão vem sinalizada como sem desafio, e a trilha segue publicável

#### Scenario: A sondagem é apresentada como sondagem

- **WHEN** o Mestre autor abre o bloco do desafio na missão marcada como sondagem
- **THEN** o bloco se chama Sondagem e diz que ela abre a trilha e mostra de onde a turma parte

#### Scenario: A sondagem não anuncia o corte de 60%

- **WHEN** o Mestre autor monta as perguntas da sondagem
- **THEN** a tela diz que não há passar nem reprovar e que a trilha abre quando o Guerreiro(a)
  responde, e em nenhum lugar anuncia o corte de 60%

#### Scenario: A sondagem não oferece desafio prático

- **WHEN** o Mestre autor abre o bloco da sondagem
- **THEN** a escolha entre quiz e desafio prático não é oferecida, e as perguntas são montadas
  direto

#### Scenario: A sondagem sem perguntas é dita como sondagem

- **WHEN** o Mestre autor abre a missão de sondagem que ainda não tem pergunta declarada
- **THEN** o aviso e o resumo da linha dizem que a sondagem ainda não tem perguntas

#### Scenario: Trilha de outro Mestre não é editável

- **WHEN** o Mestre abre uma trilha de que não é autor
- **THEN** nenhuma ação de montar ou alterar o desafio de desbloqueio é oferecida
