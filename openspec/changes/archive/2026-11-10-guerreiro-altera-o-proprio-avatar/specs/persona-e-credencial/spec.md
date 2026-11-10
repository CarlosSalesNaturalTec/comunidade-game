## ADDED Requirements

### Requirement: O Guerreiro(a) em sessão altera o próprio avatar

O núcleo SHALL aceitar, por `PATCH /v1/eu/avatar`, que o **Guerreiro(a) em sessão** troque as
características do **próprio** avatar, a qualquer tempo e quantas vezes quiser. A rota NEVER
SHALL receber identificador de persona: ela alcança só a persona da sessão, e por isso NEVER
SHALL alterar o avatar de outro Guerreiro(a). (`RF-05-51`, `RN-05-21`, PRD-05 §9)

Persona de **qualquer outro papel** SHALL receber 403 e nada SHALL ser gravado: o avatar de
Mestre e de Apoiador tem rota própria, e a edição de Guerreiro(a) pela gestão segue sendo a do
Admin (`RF-02-01`). (`RF-05-51`, PRD-05 §9)

O avatar SHALL seguir **opaco ao núcleo**, como nas rotas do Apoiador e do Mestre: o núcleo
grava o texto recebido sem validar forma, e quem compõe e lê o objeto do documento 15 §7.2 é a
camada comum. Texto **vazio** SHALL ser recusado com 422, porque o avatar do Guerreiro(a) é
obrigatório desde o cadastro. A resposta SHALL devolver o avatar gravado, e a leitura da
sessão (`GET /v1/eu`) SHALL passar a devolvê-lo dali em diante. (`RF-05-51`, `RF-01-76`,
documento 15 §7.2)

#### Scenario: O Guerreiro(a) troca o próprio avatar

- **WHEN** o Guerreiro(a) em sessão envia um avatar novo para `PATCH /v1/eu/avatar`
- **THEN** o núcleo grava o avatar na persona dele, devolve o avatar gravado, e `GET /v1/eu`
  passa a devolver o avatar novo

#### Scenario: Trocar de novo não tem limite

- **WHEN** o Guerreiro(a) em sessão troca o próprio avatar uma segunda vez no mesmo dia
- **THEN** o núcleo grava a segunda troca como gravou a primeira

#### Scenario: Outro papel não usa a rota do Guerreiro(a)

- **WHEN** um Mestre, um Apoiador, um Admin ou um responsável em sessão chama
  `PATCH /v1/eu/avatar`
- **THEN** o núcleo responde 403 e o avatar de ninguém muda

#### Scenario: A rota alcança só a persona da sessão

- **WHEN** dois Guerreiros(as) existem e um deles troca o próprio avatar
- **THEN** o avatar do outro permanece o que era

#### Scenario: Avatar vazio é recusado

- **WHEN** o Guerreiro(a) em sessão envia avatar vazio
- **THEN** o núcleo responde 422 e o avatar vigente permanece

#### Scenario: Sem sessão não há troca

- **WHEN** a rota é chamada sem credencial de persona
- **THEN** o núcleo recusa como recusa toda rota de escrita sem sessão, e nada é gravado
