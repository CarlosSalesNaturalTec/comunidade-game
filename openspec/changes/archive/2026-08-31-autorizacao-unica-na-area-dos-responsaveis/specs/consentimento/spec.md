## ADDED Requirements

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
