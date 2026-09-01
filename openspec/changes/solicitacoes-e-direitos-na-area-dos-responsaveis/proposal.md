## Why

**PRD-13 — Área dos pais e responsáveis (App 07), fatia 4 do
`openspec/cronograma-de-fatias.md`: Solicitações e direitos.**

Atende `RF-13-23`, `RF-13-27`, `RF-13-28`, `RF-13-43`, `RF-13-44`, `RN-13-12` e `RN-13-22`, e
entrega na App 07 as telas sobre o núcleo que a fatia 14 do PRD-02 já implementou (`RF-13-22`,
`RF-13-24` a `RF-13-26`, `RN-13-13`, `RN-13-14`).

O responsável exerce os direitos do titular pela App 07, mas hoje a aplicação não tem por onde:
a `SolicitacaoDoResponsavel` existe no núcleo sem tela, o limite da exclusão não é declarado
antes do aceite, e o _template_ biométrico — o dado mais sensível que a plataforma guarda —
não é apagado nem a pedido nem ao fim do vínculo, apesar de o documento 03 §§3.3 e 12.2 exigirem
os dois.

## What Changes

**Telas da App 07 sobre o núcleo já existente**

- Abertura de solicitação nos quatro tipos — acesso, correção, exclusão e esclarecimento —
  sobre um vinculado (`RF-13-22`, `RF-13-24`).
- **Aviso do limite antes do aceite da exclusão**: a tela declara que o registro de dado do
  território é despersonalizado, não apagado, e que o _template_ biométrico é a exceção —
  apagado (`RF-13-23`, `RN-13-12`, `RN-13-22`).
- Acompanhamento das próprias solicitações, com protocolo, situação, prazo de 7 dias e a marca
  de em atraso (`RF-13-25`, `RF-13-26`).
- Recusa da imagem captada no onboarding, com o termo próprio dela, a alternativa equivalente
  declarada no mesmo ato e o aviso do apagamento com a data (`RF-13-27`, `RF-13-28`).

**Apagamento do _template_ biométrico no núcleo**

- Três gatilhos marcam a data do apagamento: **desfecho aceito** de solicitação de exclusão e
  **recusa da biometria pelo responsável**, em **5 dias**; **fim do vínculo**, em **30 dias**
  com o aviso prévio na App 07 (`RF-13-43`, `RF-13-44`, `RN-13-22`, documento 03 §12.2).
- **Fim do vínculo do Guerreiro(a)** passa a existir no núcleo: ato de Admin, e varredura
  automática dos **12 meses sem atividade registrada** (decisão do fundador, 2026-09-01).
- **Comando de manutenção do núcleo** cumpre os prazos: apaga o que venceu e encerra o vínculo
  de quem completou 12 meses sem atividade (decisão do fundador, 2026-09-01).
- Apagado o _template_, o Guerreiro(a) **continua participando de tudo**, entrando por nick e
  confirmação do Mestre ou de um Admin no encontro (`RF-13-28`, `RN-13-09`).

**Fora desta fatia, por decisão do fundador (2026-09-01)**

- A **execução** da despersonalização do registro de território — romper o vínculo de autoria e
  destruir o mapeamento — vai para o **Ciclo 02**, com os requisitos diretamente relacionados a
  ela. Nesta fatia a `RN-13-12` entra apenas como o **limite declarado** na tela, que é o que
  `RF-13-23` exige.
- A **tela da App 03** que encerra o vínculo é do PRD-02: aqui nasce a rota do núcleo, e a
  fatia da gestão entra no cronograma do PRD-02.

## Capabilities

### New Capabilities

- `fim-do-vinculo-do-guerreiro`: o marco que inicia os prazos de guarda — ato de Admin,
  varredura dos 12 meses sem atividade e o que o fim do vínculo dispara.

### Modified Capabilities

- `area-dos-responsaveis`: telas de solicitação, o aviso do limite antes do aceite da exclusão,
  o acompanhamento das próprias e a recusa da imagem do onboarding com o aviso do apagamento.
- `template-biometrico`: o apagamento — hoje a capacidade cobre guarda, conferência, gravação e
  recadastro, e nenhum requisito apaga o _template_.
- `consentimento`: o responsável recusa a biometria pela App 07; a concessão continua sendo do
  termo impresso, gravada por Admin ou Mestre.
- `solicitacao-do-responsavel`: o desfecho aceito de uma solicitação de exclusão marca o
  apagamento do _template_ — a única execução que o desfecho passa a disparar.

## Impact

- **Backend** (`backend/src/nucleo/`): `biometria` (apagamento e prazos), `consentimentos`
  (recusa pelo responsável), `solicitacoes_do_responsavel` (gatilho do desfecho), `personas` ou
  módulo próprio do fim do vínculo, `cli` (comando de manutenção) e uma migração Alembic.
- **App 07** (`apps/app-07-responsaveis/`): telas novas de solicitações e da recusa da imagem;
  a tela de autorização passa a exibir o aviso do apagamento com a data.
- **Rotas** (PRD-13 §9): `POST /v1/solicitacoes` e `GET /v1/eu/solicitacoes` passam a ter
  consumidor; `POST /v1/eu/guerreiros/{id}/autorizacao` recebe a recusa da biometria e
  `GET /v1/eu/guerreiros/{id}/autorizacao` passa a devolver a data do apagamento.
- **Documentação**: documento 09 §1 (quatro decisões novas), documento 03 §§3.3 e 12.2,
  PRD-13 §§3.2, 9, 13 e 14, e a linha da fatia no cronograma.
