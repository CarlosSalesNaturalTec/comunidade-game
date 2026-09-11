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

Cada pergunta do quiz SHALL oferecer **anexar uma imagem**, sempre opcional, e a tela SHALL
dizer o **teto de 1 MB** e os **formatos aceitos** antes do envio. Durante o envio a tela SHALL
mostrar o **progresso**; recusado o arquivo, SHALL dizer o motivo em linguagem do Mestre — o
formato que chegou e os aceitos, ou o tamanho e o teto —, sem apagar o que ele já escreveu na
pergunta. Pergunta que já tem imagem SHALL permitir **trocá-la** e **removê-la**, e a imagem
anexada SHALL **permanecer** quando o Mestre grava o desafio de novo para corrigir texto. A
tela NEVER SHALL exigir habilidade técnica: nem formato digitado, nem redimensionamento, nem
endereço de arquivo. (`RF-09-119`, decisão do fundador de 2026-09-11)

#### Scenario: O Mestre autor monta o desafio da sua missão

- **WHEN** o Mestre autor abre uma missão da sua trilha e monta o desafio de desbloqueio
- **THEN** a aplicação grava o desafio e a missão passa a exibi-lo

#### Scenario: O Mestre acrescenta e remove perguntas do quiz

- **WHEN** o Mestre autor acrescenta três perguntas ao quiz e remove a segunda
- **THEN** a tela mantém as duas restantes na ordem em que ficaram, e grava só elas

#### Scenario: Quiz sem pergunta não grava

- **WHEN** o Mestre autor escolhe quiz e tenta gravar sem nenhuma pergunta
- **THEN** a tela recusa a gravação e diz que o quiz precisa de ao menos uma pergunta

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

#### Scenario: O resumo diz quantas perguntas o quiz tem

- **WHEN** o Mestre autor recolhe o bloco do desafio de desbloqueio de uma missão com quiz de
  oito perguntas
- **THEN** o resumo do bloco diz que o quiz tem oito perguntas

#### Scenario: A bancada sinaliza a missão sem desafio

- **WHEN** o Mestre autor abre uma trilha com missão que ainda não declarou desafio
- **THEN** a missão vem sinalizada como sem desafio, e a trilha segue publicável

#### Scenario: Trilha de outro Mestre não é editável

- **WHEN** o Mestre abre uma trilha de que não é autor
- **THEN** nenhuma ação de montar ou alterar o desafio de desbloqueio é oferecida
