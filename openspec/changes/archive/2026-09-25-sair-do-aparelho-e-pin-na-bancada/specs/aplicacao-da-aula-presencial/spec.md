# Spec Delta

## ADDED Requirements

### Requirement: A tela inicial encerra a sessão de trabalho, com o PIN de quem a abriu

A App 01 SHALL oferecer, **na tela inicial e somente nela**, o encerramento da sessão de trabalho do
aparelho. NEVER SHALL oferecê-lo nas telas de atendimento: a tela inicial é a que aparece entre um
atendimento e o seguinte (`RF-04-28`), e a criança que encerrasse a sessão no meio do atendimento
dela derrubaria a de quem abriu o aparelho — que só volta por login Google, indisponível sem rede.
(`RF-04-71`, `RF-04-05`)

O encerramento SHALL exigir o **PIN de quem abriu o aparelho**, digitado no ato, conferido contra o
verificador que a sessão de trabalho já guarda. O PIN NEVER SHALL ser gravado no aparelho, e a
conferência NEVER SHALL depender de rede: é a mesma conferência que a confirmação de identidade já
faz sem rede. (`RF-04-71`, `RN-04-41`, `RN-04-38`)

O contador de erros seguidos SHALL ser **o mesmo** da confirmação de identidade e da bancada de
medição: errar o PIN em qualquer um dos três SHALL contar para os três, e o bloqueio de cinco erros
SHALL recusar os três. (`RN-04-41`, `RN-04-38`)

Com o PIN **bloqueado**, a aplicação SHALL recusar o encerramento e SHALL dizer como fechar o
aparelho mesmo assim — a sessão de trabalho não sobrevive ao fechamento da aba. NEVER SHALL deixar o
aparelho sem saída alguma: a recusa sem alternativa trancaria o encontro. (`RN-04-41`)

Quem abriu o aparelho **sem PIN cadastrado** SHALL encerrar sem PIN, com o aviso que a aplicação já
apresenta nesse caso. (`RN-04-41`, `RN-04-38`)

Havendo **presença na fila local** ainda não sincronizada, a aplicação SHALL avisar antes de
encerrar, dizendo quantas aguardam e que a sincronização exige o aparelho aberto naquela aula.
NEVER SHALL descartar a fila ao encerrar: ela sobrevive ao encerramento e à recarga da página.
(`RF-04-71`, `RF-04-23`, `RF-04-25`)

Encerrada a sessão de trabalho, a aplicação SHALL descartar o verificador do PIN e SHALL voltar à
tela de abertura do aparelho, sem dado de atendimento algum em tela. (`RF-04-71`, `RF-04-28`,
`RN-04-38`)

#### Scenario: A saída existe na tela inicial e só nela

- **WHEN** a sessão de trabalho está aberta
- **THEN** a tela inicial apresenta o encerramento da sessão de trabalho, e nenhuma tela de
  atendimento o apresenta

#### Scenario: Encerrar pede o PIN de quem abriu

- **WHEN** quem opera aciona o encerramento e digita o PIN correto de quem abriu o aparelho
- **THEN** a sessão de trabalho encerra, o verificador é descartado e a aplicação volta à tela de
  abertura

#### Scenario: PIN errado no encerramento conta no mesmo contador

- **WHEN** o PIN digitado no encerramento está errado
- **THEN** a aplicação recusa o encerramento, o erro conta no mesmo contador da confirmação de
  identidade, e a sessão de trabalho continua aberta

#### Scenario: PIN bloqueado recusa, mas diz como fechar o aparelho

- **WHEN** o PIN está bloqueado por cinco erros seguidos e alguém aciona o encerramento
- **THEN** a aplicação recusa e diz que fechar a aba do navegador encerra a sessão de trabalho

#### Scenario: Sem PIN cadastrado, encerrar passa

- **WHEN** quem abriu o aparelho não tem PIN cadastrado e aciona o encerramento
- **THEN** a sessão de trabalho encerra, com o aviso de PIN não cadastrado que a aplicação já
  apresenta

#### Scenario: A fila local pendente é anunciada antes de encerrar

- **WHEN** há presença na fila local ainda não sincronizada e alguém aciona o encerramento
- **THEN** a aplicação diz quantas aguardam e que a sincronização exige o aparelho aberto naquela
  aula, antes de encerrar

#### Scenario: Encerrar não descarta a fila

- **WHEN** a sessão de trabalho é encerrada com presença na fila local
- **THEN** a fila continua guardada no aparelho, e sincroniza quando o aparelho for reaberto
  naquela aula

## MODIFIED Requirements

### Requirement: O Mestre mede no aparelho a distância entre descritores

A App 01 SHALL oferecer ao **Mestre ou ao Admin em sessão de trabalho** uma tela que captura
descritores no aparelho, compara-os entre si e apresenta a **distância** na mesma unidade que o
núcleo usa para comparar — a medição que calibra o limiar de comparação. **Descritor e imagem**
NEVER SHALL sair do aparelho: a comparação inteira acontece nele, e ao núcleo SHALL ir apenas o
**limiar confirmado e as distâncias medidas**, quando a medição concluir. (`RF-04-63`,
`RF-04-66`, documento 03 §3.3)

Abrir essa tela SHALL exigir o **PIN de quem abriu o aparelho**, digitado no ato, pela mesma
conferência e pelo mesmo contador de erros da confirmação de identidade e do encerramento da sessão
de trabalho: a medição grava o número que decide se o reconhecimento confere naquele ponto de apoio,
e a sessão de trabalho sozinha não prova que o adulto responsável está ali. PIN bloqueado NEVER
SHALL abrir a tela; quem não tem PIN cadastrado SHALL abri-la, com o aviso que a aplicação já
apresenta. A exigência é **da tela**: o núcleo segue guardando a gravação pela permissão de quem
grava, e NEVER SHALL ser lida como conferência do núcleo. (`RN-04-41`, `RN-04-37`, `RN-04-38`,
decisão do fundador de 2026-09-25)

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

#### Scenario: A bancada não abre sem o PIN

- **WHEN** alguém escolhe o caminho da medição na tela inicial
- **THEN** a aplicação pede o PIN de quem abriu o aparelho, e a câmera não é preparada antes de ele
  conferir

#### Scenario: PIN bloqueado não abre a bancada

- **WHEN** o PIN está bloqueado por cinco erros seguidos
- **THEN** a bancada não abre, e a recusa diz o mesmo que a das demais recusas por PIN bloqueado
