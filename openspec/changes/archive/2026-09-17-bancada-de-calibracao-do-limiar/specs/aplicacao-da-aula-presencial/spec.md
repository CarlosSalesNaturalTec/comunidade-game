## ADDED Requirements

### Requirement: O Mestre mede no aparelho a distância entre descritores

A App 01 SHALL oferecer ao **Mestre ou ao Admin em sessão de trabalho** uma tela que captura
descritores no aparelho, compara-os entre si e apresenta a **distância** na mesma unidade que o
núcleo usa para comparar — a medição que calibra o limiar de comparação. A tela NEVER SHALL
enviar descritor, imagem ou distância ao núcleo: a medição inteira acontece no aparelho, e o
que sai dela é o **número lido na tela** por quem opera. (`RF-04-63`, documento 03 §3.3)

A tela SHALL guardar **um** descritor de referência por vez. Cada captura seguinte SHALL ser
comparada com ele e **descartada no mesmo ato** — os dois coexistem apenas durante o cálculo —,
e a tela NEVER SHALL apresentar nem persistir o descritor, só a distância. (`RN-04-32`,
documento 99 §6 invariante 12)

Sobre **Guerreiro(a)**, a medição SHALL ser oferecida **apenas dentro do onboarding, depois de
o consentimento de biometria ter sido registrado naquela mesma sessão**. Fora do onboarding, a
tela SHALL medir somente quem opera, e NEVER SHALL abrir a câmera sobre um Guerreiro(a).
(`RN-04-33`, `RN-04-07`, documento 99 §6 invariante 11)

A tela SHALL permanecer na aplicação depois da calibração, como ferramenta de diagnóstico de
quem conduz o encontro. (`RF-04-63`, decisão do fundador, 2026-09-17)

#### Scenario: A distância aparece na unidade do núcleo

- **WHEN** o Mestre captura duas vezes e pede a comparação
- **THEN** a tela apresenta a distância entre os dois descritores, no mesmo cálculo que o núcleo
  usa para decidir se confere

#### Scenario: Só um descritor de referência fica guardado

- **WHEN** uma terceira captura é comparada com a referência
- **THEN** a segunda já havia sido descartada, e em nenhum momento houve mais de um descritor
  de referência guardado

#### Scenario: A medição não fala com o núcleo

- **WHEN** a medição inteira é executada
- **THEN** nenhuma requisição sai do aparelho, e nem descritor nem distância chegam ao núcleo

#### Scenario: Fora do onboarding a câmera não se abre sobre criança

- **WHEN** a tela é alcançada fora do onboarding
- **THEN** ela mede apenas quem opera, e não oferece caminho que capture um Guerreiro(a)

#### Scenario: Dentro do onboarding, mede depois do consentimento

- **WHEN** o onboarding chega ao passo da imagem com o consentimento já registrado
- **THEN** a medição é oferecida ali, sobre o Guerreiro(a) daquele cadastro

## MODIFIED Requirements

### Requirement: A área detalhada diz o destino de cada dado e o canal do responsável

A App 01 SHALL apresentar uma **área detalhada de direitos**, alcançável dos avisos, dizendo em
linguagem simples, para **cada dado que a aplicação coleta**: para que serve, por quanto tempo
fica e quem o acessa — como o PRD-04 §11 os declara.

A área SHALL dizer ainda que:

- a **fotografia é apagada** assim que o _template_ é gerado, e nunca sai do aparelho;
- a **imagem nunca é exibida** a ninguém — não vira avatar, não vai para a vitrine, não aparece
  em ranking e não é mostrada a outro Guerreiro(a);
- **recusar a biometria não exclui ninguém**: a confirmação do Mestre no encontro é a
  alternativa equivalente;
- a **medição do limiar** também abre a câmera, compara no aparelho e descarta no ato, sem
  enviar nada — e sobre Guerreiro(a) só acontece sob o termo já assinado;
- **pedido de acesso, correção ou exclusão é do responsável, pela App 07, com resposta em 7
  dias** — a aplicação NEVER SHALL atendê-los nem prometer atendê-los.

(`RF-04-26`, `RF-04-63`, `RN-04-06`, `RN-04-08`, `RN-04-09`, `RN-04-14`, `RN-04-32`, PRD-04 §11)

#### Scenario: A área detalha cada dado coletado

- **WHEN** alguém abre a área detalhada de direitos
- **THEN** ela apresenta, para cada dado coletado, a finalidade, o prazo de guarda e quem acessa

#### Scenario: A área declara a medição do limiar

- **WHEN** a área detalhada é lida
- **THEN** ela diz que a medição do limiar abre a câmera, compara no aparelho, descarta no ato e
  não envia nada

#### Scenario: A área diz o canal e o prazo

- **WHEN** a área detalhada é lida até o fim
- **THEN** ela diz que o pedido de acesso, correção ou exclusão é feito pelo responsável na
  App 07, com resposta em 7 dias

#### Scenario: A aplicação não recebe pedido de direitos

- **WHEN** alguém procura, na área detalhada, um jeito de pedir exclusão ali mesmo
- **THEN** não há nenhum: a aplicação apenas informa o canal
