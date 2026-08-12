## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Terceira fatia, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-01-13`, `RF-01-14`, `RF-01-15`, `RF-01-19` (a parte que a fatia
anterior deixou), `RN-01-12`, `RN-01-19`, `RN-01-20`, `RN-01-21`.

A fatia anterior entregou a persona e a sessão do adulto, e parou onde a criança começa. O que
falta antes da biometria não é a câmera: é **quem responde pela criança**. `RN-01-17` não deixa
o núcleo gravar o _template_ sem consentimento do responsável registrado, e não há responsável
registrado enquanto não existirem o cadastro dele, o vínculo com o Guerreiro(a) e a entidade que
guarda o que foi autorizado, em que versão do termo e quando.

Esta fatia entrega esses três, e nada além. Ela é pequena de propósito e é a última peça de
identidade antes de `RF-01-04` a `RF-01-08`.

## What Changes

- Admin ou Mestre passa a **cadastrar o responsável** — a única persona que o Mestre cadastra —
  sem que isso crie acesso além do dele (`RF-01-13`).
- Nasce o **vínculo** entre responsável e Guerreiro(a), com o **grau de parentesco em texto
  livre** declarado em cada um (`RF-01-13`, `RN-01-19`).
- O núcleo passa a recusar o vínculo que passaria de **três responsáveis** para o mesmo
  Guerreiro(a); os três existentes seguem válidos (`RF-01-14`, `RN-01-19`).
- O vínculo só alcança Guerreiro(a) **já cadastrado**: não há caminho que crie a criança pelo
  cadastro do responsável (`RN-01-20`).
- O responsável autenticado passa a enxergar **apenas os Guerreiros e Guerreiras vinculados a
  ele** (`RF-01-15`).
- Nasce o `Consentimento` como entidade **versionada e somente inserção**, com autoria, data e
  hora e versão do termo; revogar é registro novo, nunca edição do anterior (`RF-01-19`,
  `RN-01-12`).
- Fica gravado que **recusa de consentimento não exclui o Guerreiro(a) da atividade**
  (`RN-01-21`).

### O que esta fatia não tem, e não é omissão

As rotas que **escrevem** consentimento não são do PRD-01: `POST /v1/consentimentos` está no
PRD-04 (termo assinado no encontro, App 01) e `POST /v1/eu/guerreiros/{id}/autorizacao` está no
PRD-13 (App 07). A listagem `GET /v1/eu/guerreiros`, que mostra ao responsável quem está
vinculado a ele, também é do PRD-13. O PRD-01 §9 não declara nenhuma delas.

O que cabe aqui, portanto, é a **entidade e as invariantes** — versionamento, somente inserção,
autoria — e o **escopo de leitura** do responsável, que valem para qualquer rota que venha a
gravá-los ou lê-los. Nenhuma rota de consentimento é criada nesta change: criá-la seria escrever
requisito que o PRD-01 não tem.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação, cadência
de coleta e valoração de aporte; captura da imagem e geração do descritor no aparelho;
telemetria da Batalha de Laser e personalização por IA.

O que é do PRD-01 mas de outra fatia, por dependência declarada ou por pendência aberta:

| Fica para                           | Porque                                                        |
| ----------------------------------- | ------------------------------------------------------------- |
| `RF-01-04` a `RF-01-08`             | a biometria é a fatia seguinte, destravada por esta           |
| `RF-01-17`                          | o painel do dia só existe quando App 03 e App 09 existirem    |
| `RF-01-29`                          | a trilha de auditoria consultável é rota de Admin, de outra fatia |
| `RF-01-49` a `RF-01-53`, `RF-01-55` | documento 09, "Números da proteção das rotas públicas"        |
| `RF-01-46`, `RF-01-47`              | documento 09, "Entrega do conjunto de dados"                  |
| `RF-01-20` a `RF-01-26`, `RF-01-30` a `RF-01-45`, `RF-01-56` a `RF-01-60` | domínio, ODS, operação e rotas públicas de conteúdo |

O **anexo do termo impresso** e os atributos `origem` e `quem operou` do `Consentimento` são
declarados no PRD-01 §8 e usados pelo PRD-13; a entidade nasce aqui com eles, e a rota que anexa
a digitalização (`POST /v1/consentimentos/{id}/anexo`) é do PRD-13.

Nenhum prazo, número ou provedor é decidido nesta change. O teto de três responsáveis
(`RN-01-19`) já está no PRD; nada mais aqui carrega número.

## Capabilities

### New Capabilities

- `responsavel-e-vinculo`: o cadastro do responsável por Admin ou Mestre, o vínculo com o
  Guerreiro(a) já cadastrado, o grau de parentesco em texto livre, o teto de três responsáveis e
  o escopo de leitura do responsável. Atende `RF-01-13`, `RF-01-14`, `RF-01-15`, `RN-01-19`,
  `RN-01-20`.
- `consentimento`: a entidade versionada e somente inserção, com autoria, data e hora, versão do
  termo e decisão; a revogação como registro novo; e a recusa que não exclui o Guerreiro(a) da
  atividade. Atende `RF-01-19`, `RN-01-12`, `RN-01-21`.

### Modified Capabilities

Nenhuma. `permissoes-e-escopo-de-comunidade` já enuncia que a matriz do PRD-01 §4 é conferida em
toda operação, e a linha do responsável naquela matriz é "os Guerreiros e Guerreiras sob sua
responsabilidade": esta fatia **cumpre** esse requisito ao criar o vínculo a que ele aponta, como
a `ComunidadeVirtual` fez pelo filtro por comunidade, sem alterar o texto daquela capacidade.
`persona-e-credencial` também segue como está — a persona de responsável já existe desde a fatia
anterior; o que nasce aqui é o vínculo dela.

## Impact

- **Banco:** terceira migração, criando `VinculoResponsavel` e `Consentimento` com os atributos
  do PRD-01 §8. `Consentimento` nasce **somente inserção**, sem rota nem caminho de código que o
  edite ou apague.
- **Rotas novas:** `POST /v1/responsaveis` e `POST /v1/responsaveis/{id}/vinculos`, ambas de
  Admin ou Mestre, sob o middleware de chave da fatia 1 e a sessão da fatia 2.
- **Escopo de leitura:** o núcleo passa a ter uma segunda dimensão de recorte além da comunidade
  — o vínculo do responsável —, aplicada onde o papel for responsável.
- **Contrato para as demais changes:** a fatia da biometria depende do `Consentimento` que nasce
  aqui (`RN-01-17`); PRD-04 e PRD-13 dependem dele e do vínculo para as rotas que os escrevem.
- **Documentação:** nenhuma decisão nova é tomada nesta change, então nenhum documento-fonte e o
  documento 09 mudam. `docs/prds/index.md` e o documento 99 seguem como estão — o PRD-01
  continua aprovado e em implementação.
- **Sem implantação:** a change entrega migração e rotas portáteis, não a subida no Cloud Run.
