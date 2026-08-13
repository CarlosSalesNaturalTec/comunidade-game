## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Décima quarta fatia, na ordem do
documento 99 §9.

**Requisitos atendidos:** `RF-01-50` (emissão após aprovação de Admin, com o segredo
devolvido uma única vez), `RF-01-51` (os 30 dias contados da emissão e a URL apresentada),
`RF-01-52` (revogação automática de quem não apresenta), `RF-01-53` (revogação por Admin, com
motivo e autoria), `RN-01-35` (o segredo não é recuperável), `RN-01-36` (revogada por prazo,
nova solicitação é sempre possível) e `RN-01-51` (chave de terceiro sempre de produção, uma
por solicitação aprovada).

As duas pontas da jornada §5.5 do PRD-01 já existem e não se tocam. A fatia 1 entregou a
**conferência** da chave em toda chamada e as dezesseis chaves do projeto, e deixou na
entidade as colunas do ciclo inteiro — prazo, URL, revogação — sem nenhuma rota que as
escreva. A fatia 13 entregou a **solicitação de chave** na fila de avaliação, e o seu próprio
cenário diz que o envio "devolve o protocolo e o prazo, sem emitir chave nenhuma". Entre uma
e outra não há nada: hoje um Admin aprova a solicitação e não existe ato que produza a chave.
Esta change constrói esse meio.

Fechá-la encerra a capacidade `chave-de-aplicacao` e destrava a Área do Apoiador
Desenvolvedor da vitrine (PRD-03 §6.3) e a avaliação de chaves da App 03 (PRD-02) — nenhuma
das duas anda sem a emissão.

`RN-01-51` acaba de ser decidido pelo fundador, junto com a separação entre busca por nick e
exibição pública. As duas decisões foram gravadas no documento-fonte (03 §8 e 02 §1),
registradas no documento 09 e aplicadas ao PRD-01 e ao PRD-03 no commit que antecede esta
change.

## What Changes

- Nasce a **emissão da chave de terceiro**, `POST /v1/chaves`, ato de Admin sobre uma
  solicitação **aprovada** na fila. A resposta devolve o segredo **uma única vez**; a base
  guarda só o resumo criptográfico, regra que a capacidade já tem e que aqui ganha a sua
  primeira rota que a exerce (`RF-01-50`, `RN-01-35`).
- A chave de terceiro nasce **de produção** e **presa à solicitação que a originou** — uma
  solicitação aprovada, uma chave. É a solicitação que a identifica, e não o nome da
  aplicação, que dois terceiros podem repetir (`RN-01-51`).
- A **unicidade por aplicação e ambiente** passa a valer **só para as chaves do projeto**.
  Ela existe para garantir as dezesseis de `RF-01-54`; aplicada a terceiro, criaria uma
  colisão de nomes que nenhum requisito pede.
- Nasce o **prazo de apresentação**: 30 dias contados da emissão, gravados na chave
  (`RF-01-51`).
- Nasce `POST /v1/chaves/{id}/url`, pela qual o solicitante **apresenta a URL** do que
  construiu, dentro do prazo. Apresentada, a chave passa a vigente por prazo indeterminado;
  fora do prazo, 422 com a orientação de solicitar nova chave (`RF-01-51`, PRD-01 §9).
- Nasce a **revogação por decurso de prazo**, sem intervenção humana: vencido o prazo sem
  URL, a chamada seguinte recebe 401 (`RF-01-52`).
- Nasce a **revogação por Admin**, `DELETE /v1/chaves/{id}`, com motivo e autoria registrados;
  a aplicação perde o acesso na chamada seguinte (`RF-01-53`).
- Nasce `GET /v1/chaves`, leitura de Admin com prazo, URL apresentada e situação — a lista
  que a App 03 consome. Ela **nunca devolve o segredo**, nem para Admin (`RN-01-35`).
- Revogar **não desfaz nada**: o terceiro só lê, e não há escrita a reverter. Nova solicitação
  é sempre possível, e cada uma rende a sua chave, com o histórico das duas preservado
  (`RN-01-36`).

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação, cadência
de coleta e valoração de aporte; captura da imagem, conversa de cadastro e geração do
descritor no aparelho; exclusão do _template_; telemetria da Batalha de Laser e personalização
por IA.

O que é do PRD-01 mas de outra fatia:

| Fica para                          | Porque                                              |
| ---------------------------------- | --------------------------------------------------- |
| `RF-01-33`, `RF-01-34`, `RF-01-43` | rotas de vitrine pública, o terceiro gancho do freio |
| `RF-01-22`, `RF-01-59`             | contrato de leitura dos jogos                       |
| `RF-01-66`, `RN-01-47`             | as séries do território são do PRD-08               |
| `RF-01-31`                         | o prazo da versão anterior segue pendente (§14)     |

A **tela** de avaliação e emissão é da App 03 (PRD-02) e o **formulário** é da vitrine
(PRD-03); aqui ficam só as rotas que as duas consomem.

## Capabilities

### Modified Capabilities

- `chave-de-aplicacao`: a capacidade hoje cobre a conferência, a recusa que não informa e as
  chaves do projeto. Passa a cobrir o **ciclo de vida da chave de terceiro** — emissão sobre
  solicitação aprovada, ambiente e identidade, prazo, URL, revogação por decurso e revogação
  por Admin. O requisito da semeadura muda num ponto: a **unicidade por aplicação e ambiente
  se declara como regra das chaves do projeto**, não de toda chave (`RF-01-50` a `RF-01-53`,
  `RN-01-51`, `RN-01-36`).
- `fila-de-avaliacao`: a solicitação de chave hoje termina no desfecho. Passa a **guardar a
  chave emitida**, como o PRD-01 §8 a descreve, e a aprovação passa a ser a condição da
  emissão — nenhuma chave nasce sem solicitação aprovada (`RF-01-49`, `RF-01-50`).

Não muda: a exigência de chave em toda rota, a recusa indistinta entre ausente, inválida e
revogada, e a cota por faixa já valem para a chave de terceiro desde a fatia 1 — a emissão só
passa a produzir chaves que aquelas regras já sabem tratar. A trilha de auditoria alcança a
emissão e a revogação por _middleware_, sem nada a declarar.

## Impact

- `backend/src/nucleo/chaves/`: nasce a regra do ciclo de vida e o roteador; `modelo.py` ganha
  o vínculo com a solicitação e a natureza passa a decidir a unicidade.
- Migração do Alembic: o vínculo com `solicitacao_de_chave` e a troca do índice parcial
  `uq_chave_vigente_por_aplicacao_e_ambiente`, que passa a alcançar só a natureza "do
  projeto".
- `backend/src/nucleo/chaves/conferencia.py`: a conferência passa a observar o prazo vencido.
- `backend/src/nucleo/fila/`: a solicitação de chave guarda a chave emitida.
- `backend/src/nucleo/principal.py`: registra o roteador de chaves.
- `docs/`: o documento 03 §8 e o documento 09 passam a dizer que a emissão entrega ao
  solicitante **o identificador e o segredo**, e que o prazo é parâmetro da implantação;
  `RF-02-89` acompanha, porque é a App 03 que exibe e entrega. As demais decisões entraram nos
  documentos 02, 03 e 09 e nos PRD-01 e PRD-03 no commit que antecede esta change.
  `docs/prds/index.md` não muda de situação: o PRD-01 segue "aprovado", fatiado em changes.

## Questões levadas ao fundador antes do desenho

As três foram respondidas e estão fechadas no `design.md` — Decisions:

1. **Como a revogação por decurso acontece.** Decidido: o vencimento se aplica na leitura, e a
   **situação gravada acompanha**, para que a leitura de gestão não mostre "vigente" numa
   chave que já recebe 401. Sem agendador, que o Ciclo 01 não tem.
2. **O que protege `POST /v1/chaves/{id}/url`.** Resolvido no desenho, sem criar regra: quem
   faz a chamada é a **vitrine**, com a chave dela, e o que prova a titularidade é o
   **identificador da chave**, entregue ao solicitante na emissão e nunca devolvido por rota
   pública.
3. **Onde o prazo vira número.** Decidido: **configuração**, com 30 como valor padrão, ao lado
   das cotas e dos limites do freio.

O desenho registra ainda uma escolha conservadora que o fundador pode derrubar: apresentada a
URL uma vez, a segunda apresentação é recusada, porque substituir URL não está em requisito
nenhum.
