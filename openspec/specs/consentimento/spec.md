## Purpose

O consentimento é a prova do que foi autorizado, por quem e quando. Esta capacidade cobre o
registro versionado e **somente inserção** que responde "o que valia naquela data": cada decisão
do responsável — conceder ou revogar — entra como registro novo, com a versão do termo, a autoria
e o momento, e nenhuma delas apaga a anterior. É esse registro que, na fatia seguinte, libera o
cadastro biométrico do Guerreiro(a).

## Requirements

### Requirement: O consentimento tem porta HTTP, sob sessão de adulto

O núcleo SHALL expor o registro de consentimento por **`POST /v1/consentimentos`**, restrita a
Admin e Mestre pela matriz. A rota SHALL receber o responsável que decide, o Guerreiro(a) a que
se refere, o tipo, a decisão, a origem do ato e a testemunha quando houver, e SHALL devolver o
identificador e o momento do registro. A rota NEVER SHALL devolver decisão de consentimento de
Guerreiro(a) algum: ela é de escrita. (`RF-01-19`, `RF-04-12`, `RN-01-12`, PRD-04 §9)

#### Scenario: Mestre registra o termo assinado no encontro

- **WHEN** um Mestre em sessão registra o consentimento de biometria de um Guerreiro(a)
  vinculado ao responsável que decidiu
- **THEN** o núcleo grava o registro com a testemunha, a data e a hora com fuso, e responde 201

#### Scenario: Papel sem permissão não registra consentimento

- **WHEN** uma persona que não é Admin nem Mestre chama a rota
- **THEN** o núcleo responde 403 e nenhum consentimento é gravado

#### Scenario: Consentimento sobre Guerreiro(a) sem vínculo é recusado

- **WHEN** a rota recebe um responsável que não tem vínculo vigente com aquele Guerreiro(a)
- **THEN** o núcleo recusa e nenhum consentimento é gravado

### Requirement: O consentimento é versionado, com autoria, data e hora

O núcleo SHALL registrar cada consentimento com o responsável que decidiu, o Guerreiro(a) a que
se refere, o **tipo**, a **versão do termo**, a **decisão**, a data e hora com fuso, a testemunha
quando houver, a origem do ato e quem o operou. A versão do termo SHALL ser obrigatória: sem ela
não há prova do que foi autorizado. O consentimento SHALL alcançar apenas Guerreiro(a) vinculado
ao responsável que decide. (`RF-01-19`, `RN-01-12`, `RF-01-15`, PRD-01 §§8, 11)

A versão do termo SHALL ser **carimbada pelo núcleo**, a partir da versão vigente que ele guarda
em configuração, e a porta HTTP NEVER SHALL recebê-la do cliente: quem consome a API não escolhe
a versão do termo que o registro vai afirmar. Trocar o termo SHALL ser trocar a configuração, e
registro gravado antes da troca SHALL continuar afirmando a versão que valia quando ele foi
feito. O valor inicial é `2026-08`. (`RF-04-12`, `RN-01-12`, documento 09 — decisão do fundador,
2026-08-24)

O **tipo** SHALL ser um valor de conjunto fechado, e não texto livre. São dois, e são os que a
documentação nomeia:

| Tipo                        | O que cobre                                                       |
| ---------------------------- | ----------------------------------------------------------------- |
| `autorizacao_de_divulgacao` | divulgação do perfil, do histórico e das criações, imagem em fotos e vídeos de eventos e captação da produção — uma só autorização (`RN-13-05`) |
| `biometria`                 | captura e tratamento biométrico do onboarding, de finalidade própria e termo impresso, fora da autorização única (`RN-13-06`, `RN-01-17`) |

Consentimento com tipo fora desse conjunto SHALL ser recusado com **422**. (`RN-13-05`,
`RN-13-06`)

#### Scenario: O registro guarda o que valia

- **WHEN** um consentimento é gravado
- **THEN** o registro carrega a versão do termo, a decisão, quem decidiu e a data e hora com fuso

#### Scenario: A versão vem da configuração, não do cliente

- **WHEN** um consentimento é registrado pela porta HTTP
- **THEN** o registro carrega a versão vigente que o núcleo guarda, e nenhum campo do corpo da
  requisição a determina

#### Scenario: Versão trocada não reescreve o passado

- **WHEN** a versão vigente do termo é trocada na configuração
- **THEN** os consentimentos já gravados continuam afirmando a versão que valia quando foram
  feitos

#### Scenario: Consentimento sem versão do termo é recusado

- **WHEN** um consentimento chega sem a versão do termo
- **THEN** o núcleo responde 422 indicando o campo em falta, e nada é gravado

#### Scenario: Responsável não consente por criança que não é sua

- **WHEN** um responsável decide sobre um Guerreiro(a) que não está vinculado a ele
- **THEN** o núcleo recusa e nenhum consentimento é gravado

#### Scenario: Tipo fora do conjunto é recusado

- **WHEN** um consentimento chega com tipo que não é `autorizacao_de_divulgacao` nem `biometria`
- **THEN** o núcleo responde 422 indicando o campo em falta, e nada é gravado

#### Scenario: A biometria não entra na autorização única

- **WHEN** um responsável concede a `autorizacao_de_divulgacao` de um Guerreiro(a)
- **THEN** nenhum consentimento de `biometria` passa a existir por consequência, e o cadastro
  biométrico continua exigindo o consentimento próprio dele

### Requirement: A autorização vigente se resolve pelo histórico, e a recusa prevalece

O núcleo SHALL derivar a **vigência** de um consentimento do histórico somente inserção, sem
guardar estado à parte: para cada par de Guerreiro(a) e tipo, vale a decisão **mais recente** de
cada responsável vinculado. Havendo mais de um responsável, a **recusa prevalece**: basta que um
deles tenha revogado ou negado, na decisão mais recente dele, para que a autorização **não**
esteja vigente. A resolução SHALL responder também **por data**, devolvendo o que valia em
qualquer momento anterior. (`RF-01-19`, `RN-01-12`, `RN-01-10`, `RN-13-07`)

#### Scenario: Concessão única torna a autorização vigente

- **WHEN** o único responsável vinculado concede a autorização de divulgação
- **THEN** a autorização está vigente para aquele Guerreiro(a)

#### Scenario: A decisão mais recente de cada responsável é a que vale

- **WHEN** um responsável concede, revoga e concede de novo, nessa ordem
- **THEN** vale a última concessão, e as duas decisões anteriores continuam consultáveis

#### Scenario: Recusa de um responsável derruba a autorização

- **WHEN** dois responsáveis estão vinculados, um concedeu e o outro revogou
- **THEN** a autorização não está vigente

#### Scenario: Sem decisão nenhuma, não há autorização

- **WHEN** nenhum responsável decidiu sobre a autorização de divulgação de um Guerreiro(a)
- **THEN** a autorização não está vigente

#### Scenario: A vigência responde por data anterior

- **WHEN** se pergunta se a autorização estava vigente numa data anterior a uma revogação
- **THEN** o núcleo responde pela decisão que valia naquela data, e não pela mais recente

### Requirement: O consentimento é somente inserção

O núcleo SHALL tratar o consentimento como registro de **somente inserção**. Revogar SHALL ser a
gravação de um registro novo com a decisão contrária, e o registro anterior SHALL continuar
consultável. Nenhuma rota, comando ou operação do núcleo SHALL editar ou apagar um consentimento
já gravado. (`RF-01-19`, `RN-01-12`, PRD-01 §8)

#### Scenario: Revogar cria registro novo

- **WHEN** um responsável revoga um consentimento que havia concedido
- **THEN** o núcleo grava um registro novo com a decisão de revogação, e o anterior continua
  consultável

#### Scenario: Consentimento gravado não é editado nem apagado

- **WHEN** qualquer caminho do núcleo tenta alterar ou remover um consentimento já gravado
- **THEN** a operação é recusada e o registro permanece como foi gravado

#### Scenario: O histórico responde por data

- **WHEN** se pergunta o que valia para um Guerreiro(a) em uma data anterior
- **THEN** o núcleo responde pelo registro vigente naquela data, e não pela decisão mais recente

### Requirement: Recusa de consentimento não exclui o Guerreiro(a) da atividade

O núcleo NEVER SHALL usar a recusa ou a revogação de um consentimento para impedir a
participação do Guerreiro(a) na atividade. A decisão do responsável SHALL restringir apenas o que
aquele termo cobre, e o Guerreiro(a) SHALL continuar participando como qualquer outro.
(`RN-01-21`, PRD-01 §11)

#### Scenario: Criança sem consentimento participa igual

- **WHEN** o responsável de um Guerreiro(a) recusa um consentimento
- **THEN** o Guerreiro(a) continua podendo participar da atividade, e nenhuma operação de
  participação é recusada por causa disso

#### Scenario: A revogação não desfaz a participação

- **WHEN** um responsável revoga um consentimento que havia concedido
- **THEN** o que o Guerreiro(a) já realizou permanece registrado, e ele segue participando

### Requirement: O termo impresso assinado no encontro recebe a digitalização anexada

O consentimento de tipo `biometria` é o único firmado em **termo impresso**, assinado no
encontro e confirmado na App 01 pelo Mestre ou pelo Admin que testemunhou (`RF-04-12`). O núcleo
SHALL aceitar, depois do ato, a **digitalização** desse termo, anexada pela gestão.

O anexo SHALL ser gravado como **registro próprio**, que aponta para o consentimento e guarda
quem anexou e quando; ele NEVER SHALL alterar campo algum do consentimento, que permanece de
somente inserção. Anexo de consentimento que já tem digitalização SHALL ser recusado com **409**:
substituir digitalização não é operação do Ciclo 01.

O núcleo SHALL aceitar a digitalização em **PDF, JPG ou PNG** e SHALL recusar com **422**
qualquer outro formato, guardando-a pela porta de armazenamento. A digitalização NEVER SHALL ser
servida em rota pública, e alcançá-la SHALL exigir credencial de gestão.

Anexar SHALL ser ato de **Admin**; qualquer outra persona SHALL receber **403**. Anexo sobre
consentimento de tipo `autorizacao_de_divulgacao` SHALL ser recusado com **422**: esse tipo é
decidido na aplicação, sem termo impresso a digitalizar. (`RF-02-68`, `RN-02-21`, `RN-01-12`,
PRD-02 §§6.3, 9)

#### Scenario: Admin anexa a digitalização do termo de biometria

- **WHEN** um Admin anexa um PDF ao consentimento de biometria de um Guerreiro(a)
- **THEN** o núcleo guarda a digitalização pela porta de armazenamento e grava quem anexou e
  quando, sem alterar o consentimento

#### Scenario: Formato fora dos três é recusado

- **WHEN** chega uma digitalização que não é PDF, JPG nem PNG
- **THEN** o núcleo responde 422 e nada é guardado

#### Scenario: Segunda digitalização no mesmo consentimento é recusada

- **WHEN** um Admin anexa digitalização a um consentimento que já tem uma
- **THEN** o núcleo responde 409 e a digitalização anterior permanece

#### Scenario: Consentimento de divulgação não recebe anexo

- **WHEN** um Admin tenta anexar digitalização a um consentimento de tipo
  `autorizacao_de_divulgacao`
- **THEN** o núcleo responde 422 e nada é guardado

#### Scenario: Quem não é Admin não anexa

- **WHEN** um Mestre tenta anexar a digitalização de um termo de biometria
- **THEN** o núcleo responde 403 e nada é guardado

#### Scenario: A digitalização não é servida sem credencial de gestão

- **WHEN** a digitalização é pedida sem credencial de gestão
- **THEN** o núcleo recusa e o arquivo não é servido

### Requirement: O Guerreiro(a) lê o estado da própria autorização de divulgação

O núcleo SHALL declarar, na leitura da persona em sessão, se a **autorização de divulgação** do
Guerreiro(a) está **vigente**, derivada pela mesma resolução do histórico que já vale para toda
a plataforma — sem estado à parte e sem consulta nova. É o que permite à App 05 dizer à criança
qual é o estado do perfil público dela. (`RF-05-50`, `RN-05-14`, `RN-05-21`)

A leitura SHALL devolver **apenas se está ou não vigente**. NEVER SHALL dizer **qual**
responsável decidiu, **quando** decidiu ou **por quê**: a criança lê o estado do próprio perfil,
nunca o ato do adulto sobre ela. Autorizar continua sendo ato do responsável, na App 07, e esta
leitura NEVER SHALL oferecer caminho de conceder, recusar ou revogar. (`RN-05-21`, documento 03
§12)

#### Scenario: Autorização vigente aparece como vigente

- **WHEN** o responsável concedeu a autorização de divulgação e um Guerreiro(a) lê a própria
  persona em sessão
- **THEN** a resposta diz que a autorização está vigente

#### Scenario: Sem decisão nenhuma, o estado é não autorizado

- **WHEN** nenhum responsável decidiu sobre a divulgação daquele Guerreiro(a)
- **THEN** a resposta diz que a autorização não está vigente

#### Scenario: A revogação de um responsável aparece à criança

- **WHEN** um dos responsáveis vinculados revogou a autorização
- **THEN** a resposta diz que a autorização não está vigente

#### Scenario: O estado não revela quem decidiu

- **WHEN** o Guerreiro(a) lê o estado da própria divulgação
- **THEN** a resposta não traz responsável, data nem motivo da decisão

#### Scenario: A leitura não abre caminho de decidir

- **WHEN** o Guerreiro(a) lê o estado da própria divulgação
- **THEN** nenhuma operação de conceder, recusar ou revogar lhe é oferecida

### Requirement: O responsável concede e revoga a própria autorização única

O núcleo SHALL expor ao responsável em sessão a escrita da autorização única por **`POST
/v1/eu/guerreiros/{id}/autorizacao`**, restrita ao papel responsável pela matriz e ao **vínculo
vigente** com o Guerreiro(a) do caminho: sem vínculo SHALL responder **403** sem revelar dado
algum daquela criança. A rota SHALL receber apenas a **decisão** — conceder ou revogar — e SHALL
gravar um `Consentimento` novo de tipo `autorizacao_de_divulgacao`, com origem **própria**, o
responsável em sessão como quem decide e quem opera, e a **versão do termo carimbada pelo
núcleo**. Revogar SHALL ser a gravação de um registro de recusa, nunca a edição do anterior.
(`RF-13-14`, `RF-13-15`, `RN-13-05`, `RN-13-10`)

A autorização é **uma só**: a mesma decisão cobre divulgação do perfil e das criações, imagem em
fotos e vídeos de eventos e captação da produção. O núcleo NEVER SHALL oferecer ao responsável
decisão separada por finalidade, e NEVER SHALL fazer a `biometria` seguir esta decisão: ela tem
termo impresso próprio e permanece fora dela. (`RN-13-05`, `RN-13-06`)

#### Scenario: Responsável concede a autorização do vinculado

- **WHEN** um responsável em sessão concede a autorização de um Guerreiro(a) a que está vinculado
- **THEN** o núcleo grava um consentimento de `autorizacao_de_divulgacao` com decisão de
  concessão, origem própria, a versão vigente do termo e a data e hora com fuso

#### Scenario: Responsável revoga a que havia concedido

- **WHEN** um responsável que havia concedido revoga a autorização
- **THEN** o núcleo grava um registro novo de recusa, o registro da concessão continua
  consultável e nada é editado nem apagado

#### Scenario: Guerreiro(a) não vinculado é recusado

- **WHEN** um responsável decide sobre um Guerreiro(a) a que não está vinculado
- **THEN** o núcleo responde 403, nada é gravado e a recusa não revela dado daquela criança

#### Scenario: Outro papel não decide por esta rota

- **WHEN** uma persona que não é responsável chama a rota
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: A versão do termo não vem do cliente

- **WHEN** o responsável decide pela rota
- **THEN** o registro carrega a versão vigente que o núcleo guarda, e nenhum campo do corpo da
  requisição a determina

#### Scenario: Conceder a divulgação não concede a biometria

- **WHEN** o responsável concede a autorização única de um Guerreiro(a)
- **THEN** nenhum consentimento de `biometria` passa a existir, e o cadastro biométrico continua
  exigindo o termo impresso próprio

### Requirement: A decisão repetida do mesmo responsável não gera segundo registro

O núcleo SHALL tratar a escrita da autorização como **idempotente** quanto à decisão: recebendo
do mesmo responsável, sobre o mesmo Guerreiro(a), a **mesma decisão que já é a mais recente dele**,
o núcleo NEVER SHALL gravar um segundo registro e SHALL responder com o registro que já existe.
É o que impede que o reenvio por falha de rede vire duas linhas no histórico. (PRD-13 §10)

#### Scenario: Reenvio da mesma concessão por falha de rede

- **WHEN** o responsável envia duas vezes a mesma concessão sobre o mesmo Guerreiro(a)
- **THEN** o histórico guarda um só registro, e a segunda resposta traz o mesmo registro da
  primeira

#### Scenario: Decisão contrária sempre grava

- **WHEN** o responsável que havia concedido envia uma revogação
- **THEN** o núcleo grava o registro novo, porque a decisão mudou

### Requirement: A recusa de um responsável suspende a autorização e prevalece sobre a concessão

O núcleo SHALL derivar, do histórico somente inserção e sem estado à parte, **três estados** da
autorização única de um Guerreiro(a), tomando a decisão mais recente de **cada** responsável
vinculado:

| Estado           | Quando                                                                    |
| ---------------- | ------------------------------------------------------------------------- |
| `vigente`        | há ao menos uma decisão e **nenhuma** delas é recusa                      |
| `suspensa`       | há ao menos uma concessão **e** ao menos uma recusa — a divergência       |
| `nao_autorizada` | não há decisão alguma, ou há recusa sem concessão de nenhum responsável   |

A **recusa prevalece**: nos estados `suspensa` e `nao_autorizada` a autorização **não** está
vigente, e o Guerreiro(a) NEVER SHALL aparecer em vitrine, ranking público, portfólio público ou
elenco do jogo. O estado suspenso SHALL equivaler, para toda superfície pública, à ausência de
autorização. (`RF-13-17`, `RN-13-07`, `RN-13-11`)

O núcleo NEVER SHALL usar a recusa, a revogação ou o estado suspenso para impedir a participação
do Guerreiro(a) na atividade. (`RN-13-09`)

#### Scenario: Concessão de um e recusa de outro dá suspensa

- **WHEN** um responsável concedeu e outro responsável vinculado ao mesmo Guerreiro(a) revogou
- **THEN** o estado é `suspensa` e a autorização não está vigente

#### Scenario: Recusa isolada não é divergência

- **WHEN** o único responsável que decidiu recusou, e nenhum outro concedeu
- **THEN** o estado é `nao_autorizada`, e não `suspensa`

#### Scenario: Sem decisão nenhuma

- **WHEN** nenhum responsável decidiu sobre aquele Guerreiro(a)
- **THEN** o estado é `nao_autorizada`

#### Scenario: Todos concederam

- **WHEN** todos os responsáveis vinculados que decidiram concederam
- **THEN** o estado é `vigente`

#### Scenario: Suspensa retira do que é público

- **WHEN** o estado de um Guerreiro(a) passa a `suspensa`
- **THEN** ele deixa de aparecer na vitrine, no ranking público, no portfólio público e no
  elenco do jogo, e nenhum registro dele é apagado

#### Scenario: Estado suspenso não tira ninguém da atividade

- **WHEN** a autorização de um Guerreiro(a) está suspensa
- **THEN** ele continua participando das atividades e nenhuma operação de participação é
  recusada por causa disso

### Requirement: A concessão sobre recusa alheia e a revogação sem nenhuma concessão são recusadas

O núcleo SHALL recusar com **409** a concessão de um responsável quando **outro** responsável
vinculado tiver recusa como decisão mais recente, e a resposta SHALL trazer o estado da
autorização e a orientação de **procurar a gestão** — a recusa prevalece, e não é a concessão de
um terceiro que a desfaz. O responsável que ele próprio recusou SHALL poder conceder a qualquer
tempo: quem recusou mudar de posição é o caminho que reabre o caso. (`RF-13-17`, `RN-13-07`,
PRD-13 §9)

O núcleo SHALL recusar com **409** a revogação quando **nenhum** responsável vinculado tiver
concessão vigente — não há autorização alguma para revogar. Havendo concessão de **qualquer**
responsável, a revogação SHALL ser aceita de **qualquer outro** responsável, ainda que ele
próprio nunca tenha decidido antes: é assim que a divergência nasce — o segundo responsável não
precisa ter concedido primeiro para poder recusar. (`RF-13-15`, `RF-13-17`, `RN-13-07`, PRD-13
§9)

#### Scenario: Concessão sobre recusa de outro responsável

- **WHEN** um responsável concede e outro responsável vinculado tem recusa como decisão mais
  recente
- **THEN** o núcleo responde 409 com o estado da autorização e a orientação de procurar a
  gestão, e nada é gravado

#### Scenario: Quem recusou pode voltar atrás

- **WHEN** o responsável cuja decisão mais recente é a própria recusa concede
- **THEN** o núcleo grava a concessão, porque a recusa que ele desfaz é a dele

#### Scenario: Revogar sem que ninguém tenha concedido

- **WHEN** um responsável revoga e nenhum responsável vinculado tem concessão como decisão
  mais recente
- **THEN** o núcleo responde 409 e nada é gravado

#### Scenario: Quem nunca decidiu revoga sobre a concessão de outro

- **WHEN** um responsável concedeu e um segundo responsável, que nunca havia decidido antes,
  revoga
- **THEN** o núcleo grava a recusa do segundo responsável, porque havia concessão vigente de
  outro para revogar

### Requirement: O responsável lê o estado, quem motivou a suspensão e o histórico

O núcleo SHALL expor ao responsável em sessão a leitura da autorização por **`GET
/v1/eu/guerreiros/{id}/autorizacao`**, restrita ao papel responsável e ao **vínculo vigente**
(403 sem vínculo). A resposta SHALL trazer:

- o **estado** derivado — `vigente`, `suspensa` ou `nao_autorizada`;
- estando `suspensa`, **quem a motivou** — o responsável cuja recusa prevalece — com a **data e
  hora** daquela recusa, para que os demais responsáveis saibam de quem partiu (`RF-13-18`);
- o **histórico** de cada concessão e revogação daquele Guerreiro(a), do mais recente ao mais
  antigo, cada uma com quem decidiu, a **versão do termo**, a origem do ato e a data e hora com
  fuso (`RF-13-21`).

A leitura NEVER SHALL trazer consentimento de `biometria` nem decisão sobre outro Guerreiro(a).
(`RF-13-18`, `RF-13-21`, `RN-13-04`, `RN-13-06`)

#### Scenario: Estado vigente com histórico

- **WHEN** o responsável lê a autorização de um vinculado que ele concedeu, revogou e concedeu
  de novo
- **THEN** a resposta traz o estado `vigente` e as três decisões, da mais recente à mais antiga,
  cada uma com a versão do termo e a data e hora

#### Scenario: Estado suspenso nomeia quem recusou

- **WHEN** um responsável lê a autorização de um vinculado cuja autorização está suspensa pela
  recusa de outro responsável
- **THEN** a resposta traz o estado `suspensa`, quem a motivou e a data e hora daquela recusa

#### Scenario: Sem decisão alguma

- **WHEN** o responsável lê a autorização de um vinculado sobre quem ninguém decidiu
- **THEN** a resposta traz o estado `nao_autorizada` e o histórico vazio

#### Scenario: A leitura não alcança a biometria

- **WHEN** o vinculado tem consentimento de biometria registrado no encontro
- **THEN** ele não aparece nesta leitura, que é só da autorização única

#### Scenario: Guerreiro(a) não vinculado é recusado na leitura

- **WHEN** o responsável lê a autorização de um Guerreiro(a) a que não está vinculado
- **THEN** o núcleo responde 403 e nenhum dado daquela criança é revelado

### Requirement: O ato assistido registra a autorização em nome do responsável presente

O núcleo SHALL aceitar de um **Admin** ou de um **Mestre** em sessão a decisão da autorização
única de um Guerreiro(a) **em nome do responsável presente**, para o caso de quem não tem
smartphone. O registro SHALL gravar o **responsável como quem decide**, **quem operou** o ato, a
**testemunha**, a origem **assistida** e a **versão do termo carimbada pela configuração** — a
rota NEVER SHALL receber a versão do cliente.

O **responsável presente** SHALL ser identificado e SHALL ter **vínculo vigente** com aquele
Guerreiro(a): ato sem responsável identificado SHALL ser recusado com **422**, e responsável sem
vínculo vigente SHALL ser recusado com **403**. A **testemunha** SHALL ser obrigatória: ato sem
ela SHALL ser recusado com **422**.

O ato assistido SHALL ter a **mesma força** do registrado pelo próprio responsável: entra na
mesma derivação do estado vigente, conta na mesma regra de que a recusa prevalece e aparece no
mesmo histórico. Persona de qualquer outro papel SHALL receber **403**. (`RF-13-35`,
`RF-13-36`, `RF-13-38`, `RN-13-16`, `RN-13-07`, PRD-13 §§5.8, 6.6, 9)

#### Scenario: Mestre registra a concessão em nome do responsável presente

- **WHEN** um Mestre registra a concessão da autorização única com o responsável presente e uma
  testemunha
- **THEN** o núcleo grava a decisão em nome do responsável, com origem assistida, quem operou,
  a testemunha e a versão vigente do termo

#### Scenario: O ato assistido produz o mesmo estado que o ato do próprio

- **WHEN** a concessão é registrada pelo modo assistido e o vinculado não tem recusa de outro
  responsável
- **THEN** o estado da autorização passa a concedido, igual ao que o próprio responsável
  produziria no aparelho

#### Scenario: Ato assistido sem responsável presente identificado é recusado

- **WHEN** o ato assistido chega sem identificar o responsável presente
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Ato assistido sem testemunha é recusado

- **WHEN** o ato assistido chega sem a testemunha
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Responsável sem vínculo vigente é recusado

- **WHEN** o ato assistido nomeia um responsável que não tem vínculo vigente com aquele
  Guerreiro(a)
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: A recusa assistida prevalece como qualquer outra

- **WHEN** o modo assistido registra a recusa de um responsável sobre vinculado que outro já
  havia concedido
- **THEN** o estado passa a suspenso, com quem o motivou, data e hora

#### Scenario: Quem não é Admin nem Mestre não opera o ato assistido

- **WHEN** um responsável, um Apoiador ou um Guerreiro(a) chama a rota do ato assistido
- **THEN** o núcleo responde 403 e nada é gravado

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
