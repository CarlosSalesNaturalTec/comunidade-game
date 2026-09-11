## MODIFIED Requirements

### Requirement: A App 05 entrega a produção da missão nas três formas, avisando o que descarta

A App 05 SHALL oferecer, na missão desbloqueada, a **entrega da produção** nas três formas —
escrever, falar ou fotografar o que fez à mão (`RF-05-74`) —, com as três apresentadas lado a
lado e nenhuma como padrão obrigatório.

A fala SHALL ser **transcrita no próprio aparelho**, e ao núcleo SHALL seguir **a transcrição**,
nunca o áudio. A transcrição SHALL aparecer no campo da produção **antes do envio** e SHALL ser
editável ali, como qualquer produção digitada. A App 05 NEVER SHALL gravar o áudio em arquivo,
em armazenamento do navegador ou em qualquer lugar do aparelho, e NEVER SHALL guardar a foto no
aparelho depois do envio.

Antes de entregar falando, a tela SHALL dizer, em linguagem da criança, que **a gravação não
sai do aparelho** e que o que segue é só o texto da fala. Antes de enviar a **foto**, a tela
SHALL dizer que ela é **descartada na leitura** e que ficam guardadas apenas a transcrição e a
devolutiva (`RF-05-76`, `RN-05-32`, `RN-05-36`).

Onde o navegador do aparelho não oferecer a transcrição da fala, a tela SHALL **dizê-lo em
linguagem da criança** e SHALL manter as formas que não dependem dela — escrever, fotografar e
entregar ao Mestre no encontro —, e NEVER SHALL cair de volta no envio de áudio ao núcleo. O
mesmo aviso SHALL valer quando a transcrição falhar ou não entender nada da fala, sem perder o
que já estava escrito. (`RF-05-74`, `RF-05-76`, `RN-05-32`, documento 03 §§1.12, 12.2)

#### Scenario: As três formas aparecem na missão

- **WHEN** o Guerreiro(a) abre uma missão que ele desbloqueou
- **THEN** a tela oferece escrever, falar e fotografar o que fez à mão

#### Scenario: A fala vira texto no aparelho

- **WHEN** o Guerreiro(a) escolhe falar e fala a produção
- **THEN** a transcrição aparece no campo da produção, editável, e o que segue ao núcleo é o
  texto transcrito, com a forma "áudio" declarada e nenhum áudio enviado

#### Scenario: A tela avisa o descarte antes de enviar

- **WHEN** ele escolhe fotografar o manuscrito
- **THEN** a tela diz que a foto é descartada na leitura e que ficam só a transcrição e a
  devolutiva

#### Scenario: A tela avisa que a gravação não sai do aparelho

- **WHEN** ele escolhe falar a produção
- **THEN** a tela diz que a gravação não sai do aparelho e que o que segue é só o texto da fala

#### Scenario: O aparelho não fica com a mídia

- **WHEN** o envio termina
- **THEN** nem a foto nem áudio algum permanecem no aparelho

#### Scenario: O navegador não transcreve

- **WHEN** a entrega da produção abre num navegador sem a transcrição de fala
- **THEN** a tela o diz em linguagem da criança e mantém escrever, fotografar e entregar ao
  Mestre no encontro, sem oferecer a fala

#### Scenario: A transcrição não entendeu a fala

- **WHEN** o Guerreiro(a) fala e o aparelho não devolve transcrição alguma
- **THEN** a tela o diz em linguagem da criança, sem perder o que estava escrito, e ele pode
  falar de novo ou digitar
