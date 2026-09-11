## MODIFIED Requirements

### Requirement: A equipe entrega a produção da missão pelo aparelho e lê a devolutiva

A App 01 SHALL oferecer à equipe, na atividade que ela declarou estar trabalhando, a **entrega
da produção** em **uma** de três formas: **texto** digitado, **fala** transcrita no aparelho ou
**foto** do que a equipe fez à mão. A tela SHALL apresentar a **produção esperada** declarada na
atividade, para a equipe saber o que entregar.

Entregue, a aplicação SHALL apresentar a **devolutiva** que o núcleo devolveu, e SHALL dizer,
na própria tela, que ela **não vale ponto** e que o resultado é lançado pelo Mestre. Devolutiva
que não veio numa entrega por texto ou por fala SHALL ser apresentada como tal, com a entrega
registrada — nunca como perda do que a equipe produziu; entrega por foto que o núcleo recusou
por leitura indisponível SHALL ser apresentada como pedido de reenvio, em linguagem simples.

O microfone SHALL abrir por **ação do Guerreiro(a)** e fechar ao fim da fala; a aplicação NEVER
SHALL captar o áudio ambiente da aula. A fala SHALL ser **transcrita no próprio aparelho**, e
ao núcleo SHALL seguir **a transcrição**, nunca o áudio: a aplicação NEVER SHALL gravar o áudio
em arquivo, em armazenamento do navegador ou em qualquer lugar do aparelho compartilhado. A
transcrição SHALL aparecer no campo da produção **antes do envio** e SHALL ser editável ali,
como qualquer produção digitada. A aplicação NEVER SHALL guardar no aparelho a foto da produção
depois de enviá-la.

Onde o navegador do aparelho não oferecer a transcrição da fala, a tela SHALL **dizê-lo em
linguagem simples** e SHALL manter as formas que não dependem dela — escrever e fotografar —, e
NEVER SHALL cair de volta no envio de áudio ao núcleo. O mesmo aviso SHALL valer quando a
transcrição falhar ou não entender nada da fala, sem perder o que já estava escrito.
(`RF-04-45`, `RF-04-46`, `RF-04-47`, `RN-04-20`, `RN-04-12`, `RF-05-76`, `RN-05-32`,
documento 03 §§1.12, 12.2)

#### Scenario: A equipe entrega por texto

- **WHEN** a equipe escreve a produção e envia
- **THEN** a aplicação registra a entrega e apresenta a devolutiva devolvida pelo núcleo

#### Scenario: A equipe entrega por fala

- **WHEN** um integrante toca o botão de falar e fala a produção
- **THEN** o microfone fecha ao fim da fala, a transcrição aparece no campo da produção e o que
  segue ao núcleo é o texto transcrito, sem áudio algum

#### Scenario: A equipe corrige a transcrição antes de enviar

- **WHEN** a transcrição da fala aparece no campo da produção e a equipe a edita
- **THEN** o que segue ao núcleo é o texto corrigido, com a forma "áudio" declarada

#### Scenario: O áudio não fica no aparelho

- **WHEN** a produção falada é enviada
- **THEN** nenhum áudio permanece no aparelho — nem em arquivo, nem em armazenamento do
  navegador

#### Scenario: A equipe entrega a foto do manuscrito

- **WHEN** a equipe fotografa o que fez à mão e envia
- **THEN** a aplicação envia a foto e não a mantém no aparelho depois do envio

#### Scenario: A tela diz que a devolutiva não vale ponto

- **WHEN** a devolutiva é apresentada
- **THEN** a tela diz, em linguagem simples, que ela não credita ponto e que quem lança o
  resultado é o Mestre

#### Scenario: A produção esperada aparece antes da entrega

- **WHEN** a tela da entrega é apresentada
- **THEN** ela mostra a produção esperada declarada na atividade

#### Scenario: Devolutiva que não veio não perde a entrega por texto

- **WHEN** o núcleo registra a produção em texto sem devolutiva
- **THEN** a aplicação confirma a entrega e avisa que o retorno não veio desta vez

#### Scenario: Devolutiva que não veio não perde a entrega falada

- **WHEN** o núcleo registra a produção falada sem devolutiva
- **THEN** a aplicação confirma a entrega e avisa que o retorno não veio desta vez

#### Scenario: Leitura indisponível pede reenvio

- **WHEN** o núcleo recusa a entrega por foto porque a leitura não veio
- **THEN** a aplicação pede o reenvio em linguagem simples, sem dizer que a produção se perdeu

#### Scenario: O navegador não transcreve

- **WHEN** a tela da entrega abre num navegador sem a transcrição de fala
- **THEN** a tela avisa que ali a entrega é por texto ou por foto, e não oferece a fala

#### Scenario: A transcrição não entendeu a fala

- **WHEN** um integrante fala e o aparelho não devolve transcrição alguma
- **THEN** a tela o diz em linguagem simples, sem perder o que estava escrito, e a equipe pode
  falar de novo ou digitar
