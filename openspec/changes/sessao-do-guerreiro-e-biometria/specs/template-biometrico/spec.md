## Purpose

O _template_ biométrico é o dado mais sensível que a plataforma guarda: representação matemática
do rosto de uma criança. Esta capacidade cobre a guarda cifrada, a conferência no login, a
gravação condicionada ao consentimento do responsável, o recadastro pela gestão e a auditoria de
todo acesso — e a garantia de que nem o _template_ nem a imagem saem do núcleo por rota alguma.

## ADDED Requirements

### Requirement: Ao núcleo chega descritor, nunca imagem

O núcleo SHALL aceitar apenas o **descritor** gerado no aparelho e SHALL NOT aceitar fotografia
em nenhuma rota. O descritor SHALL ser recusado com 422 quando não tiver o formato esperado. O
_template_ SHALL servir exclusivamente para identificar o Guerreiro(a) — presença e autenticação
—, e nenhuma rota SHALL usá-lo para outra finalidade. (`RF-01-05`, `RN-01-15`, PRD-01 §§3.2, 11)

#### Scenario: Envio de imagem é recusado

- **WHEN** chega uma requisição com fotografia de Guerreiro(a) em qualquer rota do núcleo
- **THEN** o núcleo a recusa e nada é gravado

#### Scenario: Descritor malformado é recusado

- **WHEN** chega um descritor fora do formato esperado
- **THEN** o núcleo responde 422 indicando o campo em falta e nenhum _template_ é gravado

### Requirement: O _template_ é guardado cifrado e nenhuma rota o devolve

O núcleo SHALL guardar o _template_ **cifrado**, com a chave de cifragem lida na subida do
serviço e nunca gravada junto ao dado. A comparação SHALL acontecer no núcleo. **Nenhuma rota do
núcleo SHALL devolver o _template_**, nem inteiro, nem em parte, nem em resposta de erro. A
resposta da gravação SHALL confirmar o registro sem devolver o que foi gravado. (`RF-01-05`,
`RN-01-14`, PRD-01 §11, documento 03 §3.3)

#### Scenario: A gravação não devolve o que gravou

- **WHEN** um _template_ é gravado com sucesso
- **THEN** a resposta confirma a gravação e não contém o descritor nem o _template_

#### Scenario: Não existe rota de leitura do _template_

- **WHEN** se procura no núcleo uma rota que devolva o _template_ de um Guerreiro(a)
- **THEN** nenhuma existe, e a tentativa de alcançá-la responde 404

#### Scenario: O ambiente que não declara a chave de cifragem não sobe

- **WHEN** o núcleo é iniciado sem a chave de cifragem declarada
- **THEN** o serviço falha na subida, sem assumir valor padrão e sem gravar _template_ em claro

### Requirement: A gravação do _template_ exige consentimento do responsável

O núcleo SHALL recusar com **422** a gravação do _template_ de um Guerreiro(a) que não tenha
consentimento do responsável registrado e vigente para a captura biométrica. Vigente SHALL
significar que o registro mais recente daquele tipo é de concessão, não de revogação. O
Guerreiro(a) sem _template_ SHALL continuar participando de tudo, entrando por confirmação
humana. (`RF-01-07`, `RN-01-17`, `RN-01-21`, PRD-01 §§9, 11)

#### Scenario: Sem consentimento não há gravação

- **WHEN** chega um descritor de Guerreiro(a) sem consentimento registrado para a biometria
- **THEN** o núcleo responde 422 e nenhum _template_ é gravado

#### Scenario: Com consentimento registrado, grava

- **WHEN** chega um descritor de Guerreiro(a) cujo responsável registrou o consentimento
- **THEN** o núcleo grava o _template_ cifrado, e o Guerreiro(a) passa a entrar por nick e imagem

#### Scenario: Consentimento revogado bloqueia gravação nova

- **WHEN** chega um descritor de Guerreiro(a) cujo registro mais recente é de revogação
- **THEN** o núcleo responde 422 e nenhum _template_ é gravado

### Requirement: Mestre ou Admin grava e recadastra o _template_

O núcleo SHALL aceitar a gravação e o recadastro do _template_ apenas de Mestre ou Admin em
sessão, e SHALL registrar **quem gravou ou recadastrou**, com data e hora. O recadastro SHALL
substituir o _template_ anterior, que SHALL deixar de conferir a partir daquele momento. Persona
de qualquer outro papel SHALL receber 403, inclusive o próprio Guerreiro(a). (`RF-01-07`,
`RF-01-08`, `RF-01-03`, PRD-01 §§4, 9)

#### Scenario: Recadastro substitui e fica registrado

- **WHEN** um Mestre recadastra a imagem de referência de um Guerreiro(a)
- **THEN** o _template_ anterior deixa de conferir, o novo passa a conferir, e o registro guarda
  quem recadastrou, com data e hora

#### Scenario: O Guerreiro(a) não recadastra a si mesmo

- **WHEN** um Guerreiro(a) em sessão tenta gravar ou recadastrar o próprio _template_
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: Todo acesso ao _template_ é auditado

O núcleo SHALL registrar **todo acesso** ao _template_ — a gravação, o recadastro e **cada
comparação de login** —, guardando quem ou o quê acessou, o Guerreiro(a) alcançado, a data e hora
com fuso e o desfecho. O registro SHALL ter guarda **permanente** e SHALL ser somente inserção.
(`RN-01-14`, PRD-01 §11, documento 03 §3.3)

#### Scenario: A comparação de login gera registro

- **WHEN** um pedido de sessão por nick e imagem compara o descritor com o _template_
- **THEN** o núcleo grava um registro de acesso com o Guerreiro(a), o momento e o desfecho da
  comparação, tenha ela conferido ou não

#### Scenario: A gravação gera registro

- **WHEN** um Mestre grava ou recadastra um _template_
- **THEN** o núcleo grava um registro de acesso com quem operou, o Guerreiro(a) e o momento

#### Scenario: O registro de acesso não se edita

- **WHEN** se procura no núcleo uma operação que altere ou apague um registro de acesso
- **THEN** nenhuma existe: o registro é somente inserção
