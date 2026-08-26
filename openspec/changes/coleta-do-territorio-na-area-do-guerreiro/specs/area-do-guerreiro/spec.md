## ADDED Requirements

### Requirement: A App 05 mostra as séries do Guerreiro(a) e a próxima medição de cada uma

A aplicação SHALL listar ao Guerreiro(a) em sessão as **suas** séries de coleta, cada uma com o
que ela mede, o **local**, o **estado**, **quando é a próxima medição** e **quantos pontos ela
está rendendo**. A série **interrompida** SHALL ser sinalizada como tal, com o **histórico
preservado** e o **caminho de retomada** — registrar de novo —, e a tela SHALL dizer que os
pontos já ganhos **permanecem**. (`RF-05-30`, `RF-05-36`, `RN-05-10`, PRD-05 §5.4)

#### Scenario: A lista abre com o que medir e quando

- **WHEN** o Guerreiro(a) em sessão abre a área de coleta
- **THEN** vê as suas séries com o que cada uma mede, o local, o estado, a próxima medição e os
  pontos que está rendendo

#### Scenario: A série interrompida mostra como retomar

- **WHEN** uma das séries está interrompida
- **THEN** a tela a sinaliza, mantém o histórico visível, diz que os pontos ganhos permanecem e
  oferece o caminho de registrar de novo

#### Scenario: Nenhuma série de outra criança aparece

- **WHEN** o Guerreiro(a) abre a área de coleta
- **THEN** nenhuma série, registro ou dado de outro Guerreiro(a) é exibido

### Requirement: O Guerreiro(a) abre a série escolhendo o desafio e o local

A aplicação SHALL permitir ao Guerreiro(a) **abrir uma série** sobre um dos desafios de coleta
que ele pode assumir, escolhendo o **local** entre os **cadastrados pela gestão** — a aplicação
NEVER SHALL cadastrar local. A escolha SHALL oferecer apenas locais do **nível exigido** pelo
desafio, e a tela SHALL explicar em linguagem simples a recusa que o núcleo devolver.
(`RF-05-31`, `RN-05-11`, `RN-05-24`, PRD-05 §§3.2, 5.4)

#### Scenario: Abertura de série sobre desafio elegível

- **WHEN** o Guerreiro(a) escolhe um desafio que pode assumir e um local do nível exigido
- **THEN** a série é aberta e passa a aparecer na lista das suas séries

#### Scenario: A aplicação não oferece desafio que o núcleo recusaria

- **WHEN** um desafio está fora da vigência, exige granularidade acima do teto da comunidade ou
  já tem série do Guerreiro(a) naquele local
- **THEN** ele não é oferecido como abertura disponível

#### Scenario: A recusa da abertura é explicada sem termo técnico

- **WHEN** a abertura da série é recusada pelo núcleo
- **THEN** a tela explica o motivo em linguagem de criança, sem código de erro nem termo
  técnico

### Requirement: O Guerreiro(a) solicita o local que falta e acompanha a resposta

A aplicação SHALL permitir ao Guerreiro(a) **solicitar a inclusão de um local faltante**,
declarando rótulo, nível pretendido e justificativa, e SHALL exibir a **situação** de cada
solicitação sua até o desfecho: recebida, aprovada — com o local que passa a existir — ou
recusada, **com o motivo**. A tela SHALL deixar claro que o pedido **não cria local** e que
quem decide é o Mestre da trilha ou um Admin. (`RF-05-32`, `RN-05-11`, PRD-05 §5.4)

#### Scenario: Solicitação registrada e acompanhada

- **WHEN** o Guerreiro(a) não encontra o local e solicita a inclusão
- **THEN** a solicitação é registrada e passa a aparecer na lista das suas solicitações como
  recebida

#### Scenario: A recusa chega com o motivo

- **WHEN** uma solicitação do Guerreiro(a) é recusada
- **THEN** a tela mostra a situação recusada e o motivo declarado pelo avaliador

#### Scenario: O local aprovado fica disponível para abrir série

- **WHEN** uma solicitação do Guerreiro(a) é aprovada
- **THEN** a tela mostra o local criado, e ele passa a aparecer entre os locais escolhíveis

### Requirement: O Guerreiro(a) registra a medição por digitação, voz ou mídia

A aplicação SHALL registrar a medição na forma que o **tipo de coleta** do desafio exige:
**valor digitado** ou **ditado por voz** quando a forma é número, e **foto ou vídeo** quando a
forma é mídia. A **origem** SHALL ser gravada — `manual` para o valor digitado, `voz` para o
ditado — e a aplicação NEVER SHALL declarar a origem `sensor`, que é do aparelho com credencial
de dispositivo, não da criança. O ditado por voz SHALL ser transcrito **no próprio aparelho**, e
o áudio NEVER SHALL trafegar nem ficar guardado. (`RF-05-33`, `RN-05-32`, PRD-05 §§6.4, 11)

#### Scenario: Valor digitado grava origem manual

- **WHEN** o Guerreiro(a) digita a medição numa série cujo tipo pede número
- **THEN** o registro é enviado com o valor, a unidade do tipo e a origem `manual`

#### Scenario: Valor ditado grava origem voz e descarta o áudio

- **WHEN** o Guerreiro(a) dita a medição por voz
- **THEN** o valor transcrito no aparelho é enviado com a origem `voz`, e o áudio não trafega
  nem é guardado

#### Scenario: Tipo de mídia pede a foto ou o vídeo

- **WHEN** a série é de um tipo cuja forma de registro é foto ou vídeo
- **THEN** a tela pede a mídia como o próprio registro, e não pede valor numérico

### Requirement: A tela explica o registro a conferir sem acusar a criança

A aplicação SHALL exibir, ao gravar, se o registro **pontuou na hora** ou entrou como **"a
conferir"**. O registro a conferir SHALL ser explicado como **medição que o Mestre vai olhar**,
em linguagem acolhedora, sem acusação, sem sugerir erro e sem termo técnico; a tela SHALL dizer
que os pontos entram se o Mestre confirmar. (`RF-05-34`, `RF-05-35`, `RN-05-08`, PRD-05 §5.4)

#### Scenario: Registro dentro da faixa pontua na hora

- **WHEN** o Guerreiro(a) grava uma medição dentro da faixa esperada do tipo
- **THEN** a tela confirma que a medição valeu e mostra os pontos creditados

#### Scenario: Registro fora da faixa é explicado sem acusação

- **WHEN** o núcleo devolve o registro marcado "a conferir"
- **THEN** a tela diz que a medição foi guardada e que o Mestre vai olhá-la, sem afirmar que
  houve erro e sem código técnico

### Requirement: O Guerreiro(a) lê o histórico da própria série, com o que foi invalidado

A aplicação SHALL exibir o **histórico** da série do Guerreiro(a), com a **data** e o **valor**
de cada registro, quais pontuaram e quais estão a conferir. O registro **invalidado** pelo
Mestre SHALL aparecer com o **motivo**, e a tela SHALL deixar claro que **só ele** perdeu os
pontos e que a série continua. (`RF-05-37`, `RF-05-38`, `RN-05-09`, PRD-05 §12)

#### Scenario: O histórico mostra data e valor de cada registro

- **WHEN** o Guerreiro(a) abre o histórico de uma série sua
- **THEN** vê cada registro com data, valor, situação e pontos

#### Scenario: O registro invalidado aparece com o motivo

- **WHEN** o histórico inclui um registro invalidado pelo Mestre
- **THEN** ele aparece com o motivo, e a tela diz que apenas aquele registro perdeu os pontos

### Requirement: Sem rede, o registro é recusado e nada fica enfileirado no aparelho

A aplicação SHALL **recusar** o registro de coleta quando não houver rede, explicando o motivo
em linguagem simples e orientando a tentar de novo ao reconectar. A aplicação NEVER SHALL
manter fila local de registros pendentes, NEVER SHALL guardar a medição no aparelho e NEVER
SHALL reenviá-la sozinha depois. (`RF-05-85`, PRD-05 §§10, 13)

#### Scenario: A gravação sem rede é recusada na hora

- **WHEN** o Guerreiro(a) tenta gravar uma medição com o aparelho sem rede
- **THEN** a aplicação recusa, explica que é preciso rede e orienta tentar de novo ao
  reconectar

#### Scenario: Nada da medição recusada fica no aparelho

- **WHEN** um registro é recusado por falta de rede
- **THEN** nenhuma medição, mídia ou fila permanece guardada no aparelho compartilhado

### Requirement: Toda tela que coleta dado avisa o que coleta

A aplicação SHALL exibir, em **toda tela que coleta dado**, um **aviso discreto** do que está
sendo coletado, com **acesso à área detalhada** de privacidade. O aviso SHALL estar em
linguagem de criança e NEVER SHALL bloquear a tela. (`RF-05-57`, PRD-05 §11, documento 03 §12)

#### Scenario: A tela de registro traz o aviso

- **WHEN** o Guerreiro(a) abre a tela de registrar medição
- **THEN** um aviso discreto informa o que é coletado e dá acesso à área detalhada

#### Scenario: O aviso não atrapalha o uso

- **WHEN** o aviso é exibido
- **THEN** ele não bloqueia a tela nem exige confirmação para continuar
