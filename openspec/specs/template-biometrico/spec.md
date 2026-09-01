## Purpose

O _template_ biométrico é o dado mais sensível que a plataforma guarda: representação matemática
do rosto de uma criança. Esta capacidade cobre a guarda cifrada, a conferência no login, a
gravação condicionada ao consentimento do responsável, o recadastro pela gestão e a auditoria de
todo acesso — e a garantia de que nem o _template_ nem a imagem saem do núcleo por rota alguma.

## Requirements

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

### Requirement: Três gatilhos marcam a data do apagamento do _template_

O núcleo SHALL marcar o _template_ biométrico de um Guerreiro(a) para apagamento, com **data**
gravada, em três situações e nos prazos do documento 03 §12.2:

| Gatilho                                                          | Prazo                |
| ---------------------------------------------------------------- | --------------------- |
| Desfecho **aceito** de solicitação do responsável do tipo exclusão | **5 dias**           |
| **Recusa da biometria** registrada pelo responsável              | **5 dias**           |
| **Fim do vínculo** do Guerreiro(a) com o projeto                 | **30 dias**          |

A marca SHALL guardar o **gatilho** que a originou e a **data do apagamento**, contada do
instante do gatilho. Gatilho que alcança Guerreiro(a) **sem _template_ gravado** NEVER SHALL
falhar: não há o que marcar, e o ato que o disparou SHALL ser gravado do mesmo jeito.
(`RF-13-43`, `RF-13-44`, `RN-13-22`, documento 03 §§3.3, 12.2)

O _template_ é a **exceção ao limite da exclusão**: ele é **apagado**, não despersonalizado.
(`RN-13-22`, invariante 12 do documento 99 §6)

#### Scenario: O desfecho aceito da exclusão marca 5 dias

- **WHEN** o Admin registra o desfecho aceito de uma solicitação do tipo exclusão de um
  Guerreiro(a) com _template_ gravado
- **THEN** o _template_ fica marcado para apagamento em 5 dias, com o gatilho registrado

#### Scenario: A recusa da biometria marca 5 dias

- **WHEN** o responsável recusa a biometria de um vinculado com _template_ gravado
- **THEN** o _template_ fica marcado para apagamento em 5 dias

#### Scenario: O fim do vínculo marca 30 dias

- **WHEN** o vínculo de um Guerreiro(a) com _template_ gravado é encerrado
- **THEN** o _template_ fica marcado para apagamento em 30 dias

#### Scenario: Gatilho sobre quem não tem _template_ não falha

- **WHEN** um dos três gatilhos alcança um Guerreiro(a) que nunca teve _template_ gravado
- **THEN** o ato do gatilho é gravado normalmente e nenhuma marca de apagamento é criada

#### Scenario: Desfecho recusado não marca nada

- **WHEN** o Admin registra o desfecho **recusado** de uma solicitação do tipo exclusão
- **THEN** nenhum _template_ é marcado para apagamento

#### Scenario: Desfecho aceito de outro tipo não marca nada

- **WHEN** o Admin aceita uma solicitação de acesso, correção ou esclarecimento
- **THEN** nenhum _template_ é marcado para apagamento

### Requirement: A marca não se cancela e a data não se adia

O _template_ marcado SHALL ser apagado na data marcada, **sem exceção**: NEVER SHALL existir
rota, ato ou consentimento novo que cancele a marca ou adie a data, e a marca já existente NEVER
SHALL ser substituída por outra de gatilho posterior. Quem voltar ao projeto faz **nova captura,
com novo termo** — o que o documento 03 §9 já diz ao responsável no aviso. (decisão do fundador,
2026-09-01, documento 09 §1)

#### Scenario: Não existe rota que desfaça a marca

- **WHEN** se procura no núcleo uma operação que cancele o apagamento marcado
- **THEN** nenhuma existe, e a tentativa de alcançá-la responde 404

#### Scenario: Concessão nova não salva o _template_ marcado

- **WHEN** um consentimento de biometria de concessão é gravado depois de o _template_ ter sido
  marcado e antes da data
- **THEN** a marca permanece com a mesma data, e o _template_ será apagado

#### Scenario: Gatilho novo não empurra a data

- **WHEN** um _template_ marcado para 5 dias recebe também o gatilho do fim do vínculo
- **THEN** a data marcada continua sendo a primeira, e não é adiada para 30 dias

### Requirement: Apagado, o _template_ não se recompõe nem deixa rastro do descritor

O comando de manutenção SHALL apagar o _template_ cuja data já passou, e o apagamento SHALL
**destruir o dado cifrado**, não apenas ocultá-lo: NEVER SHALL restar coluna, cópia ou registro
de auditoria de onde o descritor possa ser recomposto. O apagamento SHALL entrar na auditoria do
_template_ como qualquer outro acesso, guardando **o quê apagou**, o Guerreiro(a), o gatilho e o
momento — e esse registro NEVER SHALL conter o descritor. (`RF-13-43`, `RF-13-44`, `RN-01-14`,
documento 03 §3.3)

Depois do apagamento, a comparação de login por imagem daquele Guerreiro(a) SHALL deixar de
conferir, e a auditoria já gravada dos acessos anteriores SHALL permanecer — ela é de guarda
permanente e somente inserção.

#### Scenario: Vencida a data, o comando apaga

- **WHEN** o comando de manutenção roda depois da data marcada
- **THEN** o _template_ daquele Guerreiro(a) deixa de existir no núcleo

#### Scenario: O apagamento entra na auditoria sem o descritor

- **WHEN** um _template_ é apagado
- **THEN** a auditoria guarda o Guerreiro(a), o gatilho e o momento, e o registro não contém o
  descritor nem parte dele

#### Scenario: A auditoria anterior permanece

- **WHEN** um _template_ é apagado
- **THEN** os registros de acesso gravados antes dele continuam consultáveis e inalterados

#### Scenario: A entrada por imagem deixa de conferir

- **WHEN** um pedido de sessão por nick e imagem chega depois do apagamento
- **THEN** a comparação não confere, e a tentativa é auditada como qualquer outra

### Requirement: Sem _template_, o Guerreiro(a) continua participando de tudo

O núcleo NEVER SHALL usar a marca de apagamento, nem o apagamento consumado, para impedir a
participação do Guerreiro(a) em qualquer atividade. Sem _template_, ele SHALL entrar por **nick e
confirmação do Mestre ou de um Admin no encontro** — a alternativa equivalente que já vale para
quem nunca teve captura — e a presença dele SHALL ser registrada do mesmo jeito. (`RF-13-28`,
`RN-13-09`, `RN-01-21`, invariante 11 do documento 99 §6)

#### Scenario: Apagado o _template_, a criança entra por confirmação humana

- **WHEN** um Guerreiro(a) cujo _template_ foi apagado chega ao encontro
- **THEN** o Mestre abre a sessão dele pelo nick, com confirmação humana, e a participação segue
  igual

#### Scenario: A marca não bloqueia nada enquanto não vence

- **WHEN** um Guerreiro(a) tem _template_ marcado para apagamento e a data ainda não chegou
- **THEN** ele entra, participa e é avaliado como qualquer outro, e nenhuma operação é recusada
  por causa da marca
