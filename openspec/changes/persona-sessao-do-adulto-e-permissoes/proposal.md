## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Segunda fatia, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-01-03`, `RF-01-09`, `RF-01-10`, `RF-01-11`, `RF-01-12`,
`RF-01-16`, `RF-01-18`, `RF-01-19`, `RF-01-61`, `RN-01-01`, `RN-01-02`, `RN-01-04`,
`RN-01-05`, `RN-01-18`.

A fatia anterior entregou o porteiro da **aplicação**. Falta o da **pessoa**: quase tudo o que
resta do PRD-01 espera por persona autenticada — sem ela não há autoria para gravar na escrita,
não há papel para conferir e não há comunidade por onde filtrar. Esta fatia entrega esse portão
e para exatamente onde a biometria da criança começa.

## What Changes

- Nasce a **persona** nos cinco papéis do PRD-01 §4 — Admin, Mestre, Guerreiro(a), Responsável
  e Apoiador —, com o vínculo de comunidade que `RN-01-05` exige do Guerreiro(a) (`RF-01-19`).
- A implantação passa a semear a **persona Admin do fundador**, único cadastro que não passa
  por outro Admin, com a identidade social declarada na implantação (`RF-01-61`).
- O adulto passa a autenticar por **login social** vinculado a cadastro existente; conta sem
  cadastro correspondente é recusada **sem criar persona** (`RF-01-09`, `RF-01-10`,
  `RN-01-04`).
- Admin ou Mestre passa a criar **credencial de usuário e senha provisória** para o adulto sem
  conta social, com o mesmo vínculo e as mesmas permissões (`RF-01-11`, `RN-01-18`).
- Enquanto a senha provisória não é trocada, a sessão **só serve para trocá-la**: qualquer
  outra rota responde 403 (`RF-01-12`).
- Toda rota de escrita passa a exigir persona autenticada e a gravar **autoria, data e hora**
  (`RF-01-03`). A trilha de auditoria consultável é outra fatia.
- A **matriz de permissões por papel** do PRD-01 §4 passa a ser conferida em toda operação
  (`RF-01-16`).
- Toda consulta de dado de comunidade passa a aceitar e aplicar o **filtro por comunidade**
  (`RF-01-18`).
- Nasce a `ComunidadeVirtual` como entidade, porque `RN-01-05` e `RF-01-18` precisam apontar
  para algo. `RF-01-23` põe as entidades do território sob a guarda do núcleo; o comportamento
  delas é do PRD-08.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação, cadência
de coleta e valoração de aporte; captura da imagem e geração do descritor no aparelho;
telemetria da Batalha de Laser e personalização por IA.

O que é do PRD-01 mas de outra fatia, por dependência declarada ou por decisão do fundador:

| Fica para                        | Porque                                                          |
| -------------------------------- | --------------------------------------------------------------- |
| `RF-02-01` a `RF-02-05`          | as rotas de cadastro de persona são do PRD-02, não desta fatia  |
| `RF-01-13` a `RF-01-15`          | responsável, vínculo e consentimento entram na fatia seguinte   |
| `RF-01-04` a `RF-01-08`          | nick, imagem e _template_ exigem o consentimento da fatia acima |
| `RF-01-17`                       | o painel do dia só existe quando App 03 e App 09 existirem      |
| `RF-01-49` a `RF-01-53`, `RF-01-55` | os números da cota seguem pendentes no documento 09          |
| `RF-01-29`                       | a trilha de auditoria consultável é rota de Admin, de outra fatia |
| `RF-01-20` a `RF-01-26`, `RF-01-30` a `RF-01-47`, `RF-01-56` a `RF-01-60` | domínio, ODS, operação e rotas públicas de conteúdo |

A **duração da sessão** — do adulto e do Guerreiro(a) — não é decidida aqui: é parâmetro de
configuração declarado na implantação, a calibrar no primeiro encontro real, como o PRD-01 §14
prevê. Nenhum artefato desta change grava um número.

## Capabilities

### New Capabilities

- `persona-e-credencial`: a persona nos cinco papéis, o vínculo obrigatório de comunidade do
  Guerreiro(a), quem cadastra quem, a credencial de usuário e senha provisória e a semeadura da
  persona Admin do fundador. Atende `RF-01-11`, `RF-01-19`, `RF-01-61`, `RN-01-01`, `RN-01-02`,
  `RN-01-05`, `RN-01-18`.
- `sessao-do-adulto`: abertura de sessão por login social e por usuário e senha, a recusa que
  não cria persona, o encerramento e a trava da senha provisória. Atende `RF-01-09`,
  `RF-01-10`, `RF-01-12`, `RN-01-04`.
- `permissoes-e-escopo-de-comunidade`: a matriz de permissões por papel, a escrita autenticada
  com autoria registrada e o filtro por comunidade em toda consulta. Atende `RF-01-03`,
  `RF-01-16`, `RF-01-18`.

### Modified Capabilities

Nenhuma. `chave-de-aplicacao` já enuncia, no requisito "Rota pública dispensa credencial de
persona, nunca a chave", que rota autenticada exige as duas coisas; esta fatia **cumpre** esse
requisito sem alterar o seu texto. `convencoes-da-api` é reusada como está — o corpo de erro e o
contrato de paginação valem para as rotas que nascem aqui.

## Impact

- **Banco:** segunda migração, criando `Persona` nos cinco papéis, `Credencial`, `Sessao` e
  `ComunidadeVirtual`, com os atributos do PRD-01 §8.
- **Semeadura:** o comando de implantação que hoje cria as chaves passa a criar também a persona
  Admin do fundador, lendo a identidade social declarada no ambiente.
- **Rotas novas:** `POST /v1/sessoes/social`, `POST /v1/sessoes/credencial`,
  `DELETE /v1/sessoes/atual`, `POST /v1/credenciais`, `POST /v1/credenciais/senha` e
  `GET /v1/eu`, todas sob o middleware de chave que a fatia anterior instalou.
- **Contrato para as demais changes:** toda fatia seguinte do PRD-01 — e as changes de PRD-08 e
  PRD-07 — depende da sessão, da matriz de permissões e do filtro por comunidade que nascem
  aqui.
- **Documentação:** o documento 02 §1, o documento 09 e o PRD-01 já foram atualizados pela
  decisão da semeadura do primeiro Admin, que destravou esta fatia.
- **Sem implantação:** a change entrega migração e comando portáteis, não a subida no Cloud Run.
