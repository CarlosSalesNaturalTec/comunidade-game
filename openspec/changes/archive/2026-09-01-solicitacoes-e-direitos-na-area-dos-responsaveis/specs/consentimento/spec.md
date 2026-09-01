## ADDED Requirements

### Requirement: O responsável recusa a biometria pela App 07, e só a recusa

O núcleo SHALL expor ao responsável em sessão a **recusa da biometria** do vinculado por rota
própria, distinta da autorização única, restrita ao papel responsável e ao **vínculo vigente**
com o Guerreiro(a) do caminho: sem vínculo SHALL responder **403** sem revelar dado algum daquela
criança. A rota SHALL gravar um `Consentimento` de tipo **`biometria`** com decisão de **recusa**,
origem **própria**, o responsável em sessão como quem decide e quem opera, e a **versão do termo
carimbada pelo núcleo**. (`RF-13-27`, `RN-13-06`, `RN-13-10`)

A rota NEVER SHALL aceitar **concessão**: a biometria tem **termo impresso próprio**, assinado no
encontro e gravado por Admin ou Mestre, e a App 07 só oferece a recusa — o que o PRD-13 §3.2 já
declara ao deixar o consentimento biométrico fora do escopo da aplicação, salvo o que a
`RF-13-27` lhe dá. Recusar SHALL ser a gravação de um registro novo, nunca a edição do anterior.

#### Scenario: O responsável recusa a imagem do vinculado

- **WHEN** um responsável em sessão recusa a biometria de um Guerreiro(a) a que está vinculado
- **THEN** o núcleo grava um consentimento de `biometria` com decisão de recusa, origem própria,
  a versão vigente do termo e a data e hora com fuso

#### Scenario: A rota não concede

- **WHEN** chega por essa rota um pedido de concessão da biometria
- **THEN** o núcleo o recusa e nada é gravado

#### Scenario: Guerreiro(a) não vinculado é recusado

- **WHEN** um responsável recusa a biometria de um Guerreiro(a) a que não está vinculado
- **THEN** o núcleo responde 403, nada é gravado e a recusa não revela dado daquela criança

#### Scenario: Outro papel não recusa por esta rota

- **WHEN** uma persona que não é responsável chama a rota
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: A recusa da biometria não mexe na autorização única

- **WHEN** um responsável que havia concedido a autorização única recusa a biometria
- **THEN** o estado da autorização única permanece concedido, e as duas decisões seguem
  independentes

#### Scenario: A recusa repetida não gera segundo registro

- **WHEN** o responsável recusa a biometria do mesmo vinculado duas vezes
- **THEN** o histórico guarda um só registro, e a segunda resposta traz o mesmo da primeira

### Requirement: A recusa da biometria marca o apagamento e declara a alternativa

A gravação da recusa da biometria SHALL, no mesmo ato, **marcar o _template_ do Guerreiro(a) para
apagamento em 5 dias**, e a resposta SHALL trazer a **data** desse apagamento — é o que a App 07
mostra ao responsável. A recusa NEVER SHALL, por si, retirar o Guerreiro(a) de atividade alguma:
sem _template_ ele entra por nick e confirmação humana no encontro. (`RF-13-27`, `RF-13-28`,
`RF-13-43`, `RN-13-09`, `RN-13-22`, decisão do fundador, 2026-09-01, documento 09 §1)

#### Scenario: A recusa devolve a data do apagamento

- **WHEN** um responsável recusa a biometria de um vinculado com _template_ gravado
- **THEN** a resposta traz a data do apagamento, cinco dias à frente

#### Scenario: Recusa sobre quem não tem _template_

- **WHEN** um responsável recusa a biometria de um vinculado que nunca teve captura
- **THEN** a recusa é gravada, nenhuma marca é criada e a resposta não traz data de apagamento

#### Scenario: A recusa não exclui de nada

- **WHEN** a recusa da biometria é gravada
- **THEN** nenhuma inscrição, presença, missão ou lançamento do Guerreiro(a) é recusado por
  causa dela

### Requirement: O responsável lê o estado da biometria e a data do apagamento

O núcleo SHALL devolver ao responsável em sessão, para cada vinculado, o **estado da biometria**
— se há captura gravada e qual a decisão mais recente do termo próprio —, e, havendo apagamento
marcado, a **data** dele e o **gatilho** que o originou. Ele NEVER SHALL alcançar o estado da
biometria de Guerreiro(a) a que não esteja vinculado, e a resposta NEVER SHALL conter o
_template_, o descritor nem parte deles. (`RF-13-27`, `RF-13-44`, `RN-13-04`, `RN-13-14`,
documento 03 §9, decisão do fundador, 2026-08-31, documento 09 §1)

#### Scenario: A família vê que o apagamento está marcado, e para quando

- **WHEN** o responsável consulta o estado da biometria de um vinculado com apagamento marcado
- **THEN** recebe a data do apagamento e o gatilho que o originou

#### Scenario: Sem marca, a consulta diz apenas o estado

- **WHEN** o responsável consulta o estado da biometria de um vinculado sem apagamento marcado
- **THEN** recebe o estado da captura e nenhuma data de apagamento

#### Scenario: A consulta não devolve o _template_

- **WHEN** o responsável consulta o estado da biometria
- **THEN** a resposta não contém o descritor nem o _template_, nem inteiros nem em parte

#### Scenario: Criança não vinculada não é alcançada

- **WHEN** o responsável consulta o estado da biometria de um Guerreiro(a) a que não está
  vinculado
- **THEN** o núcleo responde 403 e nada daquela criança é revelado
