## ADDED Requirements

### Requirement: A bancada mede em duas séries e grava o limiar do ponto de apoio

A bancada SHALL medir em **duas séries declaradas**, e quem opera SHALL escolher em qual está
capturando:

- o **piso**, capturas da **mesma pessoa** contra a referência;
- o **teto**, capturas de **pessoas diferentes** da referência.

A tela SHALL apresentar as duas séries **separadas**, com o maior valor do piso e o menor valor
do teto em destaque, e SHALL deixar claro a qual série cada medição pertence. (`RF-04-66`,
decisão do fundador, 2026-09-18)

A medição SHALL ser considerada **concluída** quando reunir, ao mesmo tempo:

- ao menos **8 medições de piso**;
- ao menos **8 medições de teto**, de ao menos **2 pessoas diferentes** da referência;
- **maior piso estritamente menor que menor teto**.

Não havendo folga entre as séries, a bancada NEVER SHALL gravar limiar algum: ela SHALL dizer
que não existe limiar viável com aquelas capturas e SHALL oferecer nova medição. (`RN-04-35`)

Concluída a medição, a bancada SHALL **propor** como limiar o **ponto médio entre o maior piso e
o menor teto**, e SHALL gravá-lo somente depois de **Mestre ou Admin confirmar** o valor
proposto. A gravação SHALL alcançar o **ponto de apoio da aula em curso** e SHALL levar ao núcleo
o número e as **duas séries de distâncias** — e nada mais. (`RF-04-66`, `RN-04-35`)

A tela SHALL dizer, antes da gravação, qual ponto de apoio receberá o limiar, e SHALL apresentar
o desfecho da gravação a quem confirmou. (`RF-04-66`)

#### Scenario: As duas séries aparecem separadas

- **WHEN** quem opera captura medições de piso e, em seguida, medições de teto
- **THEN** a tela apresenta as duas séries separadas, com o maior piso e o menor teto em destaque

#### Scenario: A medição incompleta não grava

- **WHEN** a medição tem menos que o mínimo de uma das séries, ou o teto veio de uma pessoa só
- **THEN** a bancada não oferece a gravação e diz o que ainda falta medir

#### Scenario: Séries que se sobrepõem não geram limiar

- **WHEN** o maior valor do piso alcança ou ultrapassa o menor valor do teto
- **THEN** a bancada diz que não existe limiar viável com aquelas capturas, oferece nova medição
  e nada é gravado

#### Scenario: O valor proposto é o ponto médio, e quem opera confirma

- **WHEN** a medição conclui com folga entre as séries
- **THEN** a bancada propõe o ponto médio entre o maior piso e o menor teto, e só grava depois
  da confirmação de Mestre ou Admin

#### Scenario: A gravação alcança o ponto de apoio da aula em curso

- **WHEN** o limiar é confirmado
- **THEN** ele é gravado no ponto de apoio da aula em que a sessão de trabalho está aberta, com
  as duas séries de distâncias, e a tela apresenta o desfecho

## MODIFIED Requirements

### Requirement: O Mestre mede no aparelho a distância entre descritores

A App 01 SHALL oferecer ao **Mestre ou ao Admin em sessão de trabalho** uma tela que captura
descritores no aparelho, compara-os entre si e apresenta a **distância** na mesma unidade que o
núcleo usa para comparar — a medição que calibra o limiar de comparação. **Descritor e imagem**
NEVER SHALL sair do aparelho: a comparação inteira acontece nele, e ao núcleo SHALL ir apenas o
**limiar confirmado e as distâncias medidas**, quando a medição concluir. (`RF-04-63`,
`RF-04-66`, documento 03 §3.3)

A tela SHALL guardar **um** descritor de referência por vez. Cada captura seguinte SHALL ser
comparada com ele e **descartada no mesmo ato** — os dois coexistem apenas durante o cálculo —,
e a tela NEVER SHALL apresentar nem persistir o descritor, só a distância. (`RN-04-32`,
documento 99 §6 invariante 12)

A tela SHALL apresentar o **visor ao vivo** enquanto captura, com o mesmo retorno abstrato das
demais telas de câmera, e NEVER SHALL devolver o quadro capturado. (`RF-04-64`, `RN-04-34`)

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

- **WHEN** as capturas e as comparações da medição são executadas
- **THEN** nenhuma requisição sai do aparelho: só a gravação do limiar confirmado fala com o
  núcleo, e ela acontece depois de a medição ter concluído

#### Scenario: Nem descritor nem imagem chegam ao núcleo

- **WHEN** a medição inteira é executada, inclusive a gravação do limiar
- **THEN** nenhuma requisição carrega descritor ou imagem, e o que sai do aparelho é o limiar
  confirmado com as distâncias medidas

#### Scenario: A bancada mede com o visor aberto

- **WHEN** a bancada captura a referência ou uma comparação
- **THEN** o visor ao vivo aparece na tela, e o quadro capturado não é devolvido

#### Scenario: Fora do onboarding a câmera não se abre sobre criança

- **WHEN** a tela é alcançada fora do onboarding
- **THEN** ela mede apenas quem opera, e não oferece caminho que capture um Guerreiro(a)

#### Scenario: Dentro do onboarding, mede depois do consentimento

- **WHEN** o onboarding chega ao passo da imagem com o consentimento já registrado
- **THEN** a medição é oferecida ali, sobre o Guerreiro(a) daquele cadastro
