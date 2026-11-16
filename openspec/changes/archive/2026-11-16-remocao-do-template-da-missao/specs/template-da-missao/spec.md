## REMOVED Requirements

### Requirement: O Mestre autor cadastra o tópico e recebe a estrutura sugerida

**Reason**: Decisão do fundador de 2026-11-16 — o template da missão sai da App 09 para
simplificar a autoria. `RF-09-85` e `RF-09-91` saem do PRD-09.
**Migration**: O Mestre escreve a missão direto pelos blocos de autoria. As rotas
`POST /v1/missoes/{id}/estrutura` e `POST /v1/sugestoes-de-estrutura/{id}/desfecho` deixam de
existir, e a tabela `sugestao_de_estrutura` é apagada com os registros.

### Requirement: O template aponta as lacunas da missão

**Reason**: Mesma decisão; `RF-09-86` e `RN-09-33` saem do PRD-09.
**Migration**: A trava de produção na criação da atividade (`RN-09-31`) e as travas de
publicação da capacidade `trilha-e-missao` seguem como estão; nada as substitui.

### Requirement: Em trilha de poder técnico a estrutura começa por atividade desplugada

**Reason**: Mesma decisão; `RF-09-88` e `RN-09-34` saem do PRD-09, e a marca de técnico sai do
catálogo de poderes.
**Migration**: Nenhuma — a atividade desplugada continua sendo modalidade que o Mestre declara.

### Requirement: A sugestão traz a etiqueta ODS e a cadência de retomada

**Reason**: Mesma decisão; `RF-09-95` sai do PRD-09 e `RF-09-116` é reescrito.
**Migration**: A etiqueta ODS da missão segue declarada pelo Mestre (`etiqueta-ods`). A
cadência de 2, 7 e 21 dias passa a abrir preenchida no bloco de cadência da App 09
(`area-do-mestre`).

### Requirement: O template não escreve o conteúdo da missão

**Reason**: Mesma decisão; `RF-09-87` sai do PRD-09. Sem IA na autoria, não há o que proibir.
**Migration**: Nenhuma — o conteúdo já é escrito só pelo Mestre.

### Requirement: Nada entra na trilha sem o Mestre confirmar

**Reason**: Mesma decisão; `RF-09-89` sai do PRD-09.
**Migration**: Nenhuma — sem sugestão, toda gravação já é ato do Mestre.

### Requirement: Nenhum consumo do modelo é medido nem lançado

**Reason**: Sem a porta do template, não há consumo de modelo nesta capacidade. `RF-09-90`
permanece no PRD-09 e segue aplicado pela `producao-da-missao`.
**Migration**: Nenhuma.

### Requirement: A indisponibilidade do modelo não trava a autoria

**Reason**: Sem a porta do template, não há modelo a ficar indisponível na autoria.
**Migration**: Nenhuma.
