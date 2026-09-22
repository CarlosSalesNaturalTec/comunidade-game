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

A **dimensão esperada** do descritor é a da biblioteca de reconhecimento facial decidida no
documento 03 §3.3, e SHALL ser fixa no núcleo, com a origem declarada junto dela. Ela NEVER
SHALL ser parâmetro de implantação: não admite calibração — ou casa com o que a aplicação gera,
ou nenhuma captura é aceita. O ambiente NEVER SHALL poder declará-la, e trocá-la é trocar de
biblioteca. (`RF-01-05`, documento 03 §3.3, decisão do fundador, 2026-09-17)

O **limiar de comparação** também NEVER SHALL ser parâmetro de implantação, por motivo oposto:
ele admite calibração, e depende da câmera e da luz de cada espaço. Ele é **medido por ponto de
apoio**, no encontro. (`RF-01-73`, decisão do fundador, 2026-09-18)

#### Scenario: Envio de imagem é recusado

- **WHEN** chega uma requisição com fotografia de Guerreiro(a) em qualquer rota do núcleo
- **THEN** o núcleo a recusa e nada é gravado

#### Scenario: Descritor malformado é recusado

- **WHEN** chega um descritor fora do formato esperado
- **THEN** o núcleo responde 422 indicando o campo em falta e nenhum _template_ é gravado

#### Scenario: O descritor que a aplicação gera é aceito

- **WHEN** chega o descritor gerado pela biblioteca do documento 03 §3.3, na dimensão dela
- **THEN** o núcleo o aceita, e a dimensão conferida é a mesma em todo ambiente

#### Scenario: A dimensão não se declara no ambiente

- **WHEN** se procura uma variável de ambiente que fixe a dimensão do descritor
- **THEN** nenhuma existe, e o valor conferido vem do próprio núcleo

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

### Requirement: O limiar de comparação é medido por ponto de apoio, e sem ele não se reconhece

O **limiar de comparação** SHALL ser dado de cada **ponto de apoio**, nascido de uma medição
feita no aparelho do encontro, e NEVER SHALL ser parâmetro de implantação: nenhuma variável de
ambiente SHALL declará-lo. (`RF-01-73`, documento 03 §3.3, decisão do fundador, 2026-09-18)

O núcleo SHALL gravar cada medição com o **ponto de apoio**, o **limiar**, as **duas séries de
distâncias** que o produziram, **quem mediu** e **quando**. O limiar vigente de um ponto de apoio
SHALL ser o da medição **mais recente** dele. A gravação SHALL exigir Mestre ou Admin pela
matriz de permissões, e o núcleo NEVER SHALL aceitar descritor nesta rota. (`RF-01-73`,
`RF-01-16`, `RN-01-15`)

A comparação de um Guerreiro(a) **no encontro** SHALL usar o limiar vigente do ponto de apoio
**da aula em que a entrada acontece**. Ponto de apoio **sem limiar medido** SHALL fazer a
comparação **recusar**, e essa recusa SHALL ser indistinguível das demais. (`RF-01-73`,
`RN-01-56`, `RN-01-22`)

A comparação **fora do encontro** — o pedido que não traz aula — SHALL usar o **maior** limiar
vigente entre os pontos de apoio **ativos** da comunidade do **vínculo vigente** do
Guerreiro(a). É o mais frouxo deles: o valor é **emprestado**, medido em espaço que não é o
daquela câmera, e a escolha é a que não tranca a criança fora da aplicação, já que o responsável
abre a sessão quando a comparação recusa. Ponto de apoio **inativo** NEVER SHALL entrar na
conta. Guerreiro(a) **sem vínculo vigente**, e comunidade **sem nenhum ponto de apoio com limiar
medido**, SHALL fazer a comparação recusar, de forma indistinguível das demais.
(`RN-01-57`, `RN-01-56`, `RN-01-22`, documento 03 §3.3, decisão do fundador, 2026-09-21)

A **resolução do limiar** fora do encontro SHALL custar o mesmo qualquer que seja o desfecho —
Guerreiro(a) inexistente, vínculo encerrado, comunidade sem medição ou comparação que confere —
e SHALL NOT variar com **quantos** pontos de apoio a comunidade tem. Um custo que crescesse com
a comunidade, ou que caísse quando o nick não existe, deixaria sondar nick pelo relógio.
(`RN-01-22`, `RN-01-57`)

Toda comparação SHALL continuar sendo auditada, inclusive a que recusa por ausência de limiar.
(`RN-01-14`)

#### Scenario: O limiar não se declara no ambiente

- **WHEN** se procura uma variável de ambiente que fixe o limiar de comparação
- **THEN** nenhuma existe, e o valor usado vem da medição do ponto de apoio

#### Scenario: A medição grava o limiar com as séries que o produziram

- **WHEN** Mestre ou Admin confirma o limiar ao fim de uma medição concluída
- **THEN** o núcleo grava o limiar, as duas séries de distâncias, quem mediu e quando, e passa a
  usá-lo como vigente daquele ponto de apoio

#### Scenario: Medição nova substitui a anterior sem apagá-la

- **WHEN** um ponto de apoio já medido recebe uma medição nova
- **THEN** o limiar vigente passa a ser o da medição nova, e a anterior continua consultável

#### Scenario: Ponto de apoio sem limiar não reconhece ninguém

- **WHEN** chega um pedido de sessão por nick e imagem numa aula cujo ponto de apoio não tem
  limiar medido
- **THEN** o núcleo recusa de forma indistinguível das demais recusas, a comparação é auditada e
  a entrada acontece pela confirmação humana

#### Scenario: Fora do encontro vale o mais frouxo da comunidade

- **WHEN** chega um pedido sem aula de um Guerreiro(a) cuja comunidade tem dois pontos de apoio
  ativos com limiares medidos diferentes
- **THEN** a comparação usa o maior dos dois

#### Scenario: Ponto de apoio inativo não empresta limiar

- **WHEN** o maior limiar da comunidade é o de um ponto de apoio desativado
- **THEN** ele fica fora da conta, e vale o maior entre os ativos

#### Scenario: Comunidade sem medição alguma não reconhece fora do encontro

- **WHEN** chega um pedido sem aula de um Guerreiro(a) cuja comunidade não tem ponto de apoio
  algum com limiar medido
- **THEN** o núcleo recusa de forma indistinguível das demais recusas, e a comparação é auditada

#### Scenario: O limiar emprestado não atravessa comunidade

- **WHEN** chega um pedido sem aula e existem limiares medidos em outra comunidade
- **THEN** nenhum deles é considerado: a busca parte do vínculo vigente do próprio Guerreiro(a)

#### Scenario: A rota da medição não aceita descritor

- **WHEN** chega uma gravação de limiar com descritor no corpo
- **THEN** o núcleo a recusa e nada é gravado
