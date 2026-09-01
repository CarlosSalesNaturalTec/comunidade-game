## Why

**PRD-13 — Área dos pais e responsáveis (App 07), fatias 5 e 6 do
`openspec/cronograma-de-fatias.md`: Transparência, termos e histórico de acessos; Atendimento
assistido, propostas e avisos.**

Atende `RF-13-29` a `RF-13-42`, `RN-13-15` a `RN-13-19`. São as duas últimas fatias do PRD-13.

A App 07 já mostra a evolução, a autorização e as solicitações, mas o responsável ainda não tem
como saber **o que a plataforma guarda da criança, por quanto tempo e quem acessou** — a
transparência que o documento 03 §12 exige e que sustenta a confiança da família no canal
oficial. Não há tela de termo: o núcleo carimba a versão vigente em cada consentimento sem que o
responsável possa ler o que aquela versão diz, nem consultar a que valia numa data passada. E o
responsável sem smartphone continua dependendo de um ato que a plataforma não sabe registrar em
nome dele.

## What Changes

**Transparência e termos (fatia 5)**

- **O que o núcleo guarda daquele Guerreiro(a)**, com a finalidade e o prazo de guarda de cada
  dado, na tabela do PRD-01 §11 e nos prazos do documento 03 §12.2 (`RF-13-29`).
- **Histórico de acessos** recortado ao vinculado — data, hora, quem acessou, em que papel e
  qual dado —, que é a trilha de auditoria do PRD-01 exposta a quem responde pela criança
  (`RF-13-30`). O trabalho de rotina do Mestre aparece como rotina.
- **Solicitação de esclarecimento aberta a partir de um acesso listado**, sem sair da tela
  (`RF-13-31`).
- **Catálogo versionado de termos**: o texto de cada versão, em linguagem simples, a versão
  vigente, o histórico que responde "o que valia naquela data" e o **registro da leitura**
  (`RF-13-32`, `RF-13-33`).
- **Cláusula de entrega de dados** no termo: gratuita, anonimizada, aprovada caso a caso pelo
  Admin e licenciada em CC BY-SA (`RF-13-34`, `RN-13-19`, documento 03 §12.3).

**Atendimento assistido, propostas e avisos (fatia 6)**

- **Ato assistido da autorização única**, no **modo assistido da própria App 07**: um Admin ou
  Mestre entra com a própria credencial, escolhe o Guerreiro(a) e o responsável presente, e o
  registro entra **em nome do responsável**, com quem operou e quem testemunhou, e a mesma
  força do ato feito pelo próprio (`RF-13-35`, `RF-13-36`, `RF-13-38`, `RN-13-16`).
- **Proposta de evolução** registrada na fila única da gestão e acompanhada até o retorno, com
  o motivo em linguagem simples quando não adotada, sempre dentro da plataforma (`RF-13-39`,
  `RF-13-40`, `RN-13-15`).
- **Proposta de responsável não pontua** (`RN-13-18`): hoje o desfecho *adotada* credita 20
  pontos extras e o badge de protagonismo ao autor sem conferir se ele é Guerreiro(a) — o
  crédito passa a alcançar apenas quem tem pontuação.
- **Aviso discreto de coleta** em toda tela da App 07 que grava dado, com acesso à área
  detalhada, que é a própria tela de transparência (`RF-13-41`), no mesmo padrão das Apps 01,
  03, 05 e 09.
- **Nenhum canal com Apoiadores ou terceiros** na aplicação (`RF-13-42`, `RN-13-17`).

**Decisões novas do fundador (2026-09-01), a gravar nos documentos-fonte**

- **Redação da cláusula de entrega de dados** aprovada, o que destrava o `RF-13-34`. A linha
  "Redação dos termos" do documento 09 **continua aberta** pelos outros dois textos — o termo
  biométrico e o da autorização única — e pela revisão jurídica dos três.
- **O termo impresso da autorização única não é digitalizado nem anexado**: o papel assinado
  fica **somente no arquivo físico** da gestão, e o ato entra na plataforma como **atendimento
  assistido**. O anexo de digitalização continua exclusivo do consentimento de `biometria`, ato
  de Admin, como o `RF-02-68` já definiu — o `RF-13-37` se cumpre por ele, sem rota nova, e a
  jornada 5.8.3, o critério de aceite do PRD-13 §12 e a linha do anexo no §9 são corrigidos.
- **O atendimento assistido acontece na própria App 07**, em modo assistido: a aplicação passa
  a admitir sessão de Admin ou de Mestre **apenas** para isso. Como nenhuma rota diz quem
  responde por um Guerreiro(a), nasce `GET /v1/guerreiros/{id}/responsaveis`, restrita a Admin
  e Mestre pela operação de vínculo que a matriz já concede — nenhuma `Operacao` nova.

**Fora desta fatia**

- O que o PRD-13 §3.2 já exclui, sem exclusão nova. O **estado da reparação da ocorrência de
  conduta** e as **metas numéricas de H2** seguem pendentes (PRD-13 §14) e não são requisito de
  nenhuma tela daqui.
- **Publicar ou editar termo pela App 03**: nenhum requisito o prevê. O texto do termo é
  conteúdo semeado na implantação, e trocar o termo vigente é trocar a configuração — como já
  está decidido na capability `consentimento`.

## Capabilities

### New Capabilities

- `catalogo-de-termos`: o texto versionado de cada termo, em linguagem simples, a versão
  vigente, o histórico que responde pela versão de uma data e o registro de leitura do
  responsável.
- `transparencia-de-dados`: o que o núcleo guarda de um Guerreiro(a), com a finalidade e o
  prazo de guarda de cada dado, respondido ao responsável vinculado.

### Modified Capabilities

- `auditoria`: a trilha deixa de ser lida só pelo Admin — o responsável a lê **recortada ao
  Guerreiro(a) vinculado**, sem alcançar escrita de outra criança (`RF-13-30`).
- `consentimento`: o ato assistido da autorização única ganha rota própria, com o responsável
  presente identificado, testemunha obrigatória e registro em nome dele (`RF-13-35`,
  `RF-13-36`, `RF-13-38`, `RN-13-16`).
- `responsavel-e-vinculo`: quem responde por um Guerreiro(a) passa a ser legível por Admin e
  Mestre, para que o modo assistido escolha o responsável presente (`RF-13-35`).
- `fila-de-avaliacao`: o crédito da proposta adotada alcança apenas autor Guerreiro(a); as
  demais personas recebem o desfecho sem ponto e sem badge (`RN-13-18`).
- `area-dos-responsaveis`: as telas de transparência, acessos, termos e propostas, o aviso
  discreto de coleta em toda tela que grava dado, a ausência de canal com terceiros e o **modo
  assistido**, única sessão de Admin ou de Mestre que a aplicação admite (`RF-13-29` a
  `RF-13-36`, `RF-13-38` a `RF-13-42`, `RN-13-15` a `RN-13-18`).

## Impact

**Backend** — módulo novo `termos/` (modelo, regra e rotas de `GET /v1/termos` e
`POST /v1/termos/{versao}/leitura`, com a semente do texto vigente); `GET
/v1/eu/guerreiros/{id}/dados` e `GET /v1/eu/guerreiros/{id}/acessos`; `POST
/v1/guerreiros/{id}/autorizacao/assistida` e `GET /v1/guerreiros/{id}/responsaveis`; o
Guerreiro(a) alcançado por cada escrita, gravado junto da trilha de auditoria; conferência do
papel do autor em `fila/regra.py`; migração Alembic para o termo, o registro de leitura e o
recorte da trilha.

**App 07** — telas de transparência (dados, acessos e esclarecimento), de termos (vigente,
leitura e histórico) e de propostas; o modo assistido para sessão de Admin ou de Mestre;
`AvisoDeColeta` e o caminho para a área detalhada, no padrão já vendorizado nas outras
aplicações.

**Documentação** — documento 03 §§9 e 12.3, documento 09 §1, PRD-13 §§5.8, 6.6, 9 e 14,
`docs/prds/index.md` e `openspec/cronograma-de-fatias.md`.
