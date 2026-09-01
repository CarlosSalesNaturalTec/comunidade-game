## ADDED Requirements

### Requirement: Três gatilhos marcam a data do apagamento do _template_

O núcleo SHALL marcar o _template_ biométrico de um Guerreiro(a) para apagamento, com **data**
gravada, em três situações e nos prazos do documento 03 §12.2:

| Gatilho                                                          | Prazo                |
| ---------------------------------------------------------------- | -------------------- |
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
