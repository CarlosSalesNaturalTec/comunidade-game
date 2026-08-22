## Context

Ver `proposal.md` — Why. A fatia é **exposição**: o ciclo de avaliação está em
`openspec/specs/fila-de-avaliacao/spec.md` e implementado em `backend/src/nucleo/fila/regra.py`.
Nenhuma regra muda.

O que já está consolidado e esta fatia apenas aplica:

| Padrão                                        | Onde                                                      |
| --------------------------------------------- | --------------------------------------------------------- |
| Envelope de página, cursor e filtros de rota  | `backend/src/nucleo/paginacao.py`, `convencoes-da-api`    |
| Rota restrita a Admin                         | `exigir_permissao(Operacao.tudo, "escreve")`, em `chaves/` |
| Trilha de auditoria de toda escrita           | `MiddlewareDeAuditoria` — automática, sem código na rota  |
| Camada visual e associação do erro ao campo   | `comum/react/`, `camada-visual-comum`                     |
| Formulários de Mestre e Apoiador              | `apps/app-03-gestao/src/personas/`                        |

## Goals / Non-Goals

**Goals:**

- Expor a leitura e o desfecho da participação sem tocar em `avaliar_solicitacao_de_participacao`
  nem em `esta_em_atraso`.
- Deixar a área Filas com a forma que as outras três naturezas vão ocupar sem redesenho.

**Non-Goals:**

- Refatorar a regra da fila. Se a fatia precisar mudá-la, o recorte está errado.
- Servir o comprovante — é change própria, por decisão do fundador.

## Decisions

**1. A fila não usa filtro por comunidade, e por isso não declara
`filtro_comunidade_obrigatorio`.** A solicitação chega pela vitrine pública, antes de existir
qualquer vínculo: não há comunidade a filtrar. `RF-01-18` alcança dado de comunidade, e este
não é.
_Descartado:_ filtro opcional de comunidade, que sugeriria um vínculo que a entidade não tem.

**2. O atraso sai calculado na resposta, como campo derivado.** `esta_em_atraso` compara
`prazo` com o instante da consulta; gravá-lo exigiria varredura periódica e criaria um estado
que a spec proíbe. A ordenação da fila põe o mais antigo primeiro, para que o atraso apareça no
topo sem depender de o Admin ordenar.
_Descartado:_ campo `em_atraso` persistido, contra `RN-01-49`.

**3. A reavaliação é recusada na rota, com 409, e não na regra.** `avaliar_solicitacao_de_
participacao` hoje sobrescreve o desfecho sem reclamar — comportamento aceitável enquanto só o
teste a chamava. A guarda entra na rota para não alterar a assinatura da regra nem os testes que
já a exercitam; a spec a fixa como comportamento observável.
_Descartado:_ mudar a regra, que arrastaria as outras três naturezas para dentro desta fatia.

**4. O pré-preenchimento do cadastro passa por estado da aplicação, não por rota nova.** A App 03
leva os campos da solicitação aos formulários de `src/personas/` como valores iniciais. Nenhum
formulário muda de contrato, e o núcleo não ganha rota de "cadastrar a partir de solicitação" —
que embutiria no núcleo a promessa de que aceitar cadastra, exatamente o que `RN-02-03` proíbe.
_Descartado:_ rota de cadastro derivado da solicitação.

**5. A área Filas nasce com o filtro por natureza já montado, servindo uma natureza só.** A
alternativa — tela só de participação, generalizada depois — custaria reescrever a lista quando
a fatia 2 chegar, uma semana depois. O filtro com uma opção é honesto: mostra o que existe.

**6. `GET /tipos-de-recurso` entrou durante o `/opsx:apply`, restrita a Admin como o cadastro.**
A proposal previa "nenhuma rota nova" para a homologação do aporte, mas `POST /aportes` exige
`tipo_de_recurso_id` e nenhuma rota listava o catálogo. Decidido pelo fundador em 2026-08-22.
_Descartado:_ seletor por UUID digitado, que não é interface funcional para o Admin.

## Risks / Trade-offs

- **A guarda de reavaliação fica na rota e a regra segue permissiva** → um segundo chamador da
  regra poderia sobrescrever um desfecho. Hoje não há outro; a fatia 2 traz as três naturezas
  restantes pelo mesmo caminho, e a consolidação da guarda na regra é candidata a fatia de
  limpeza depois que as quatro existirem.
- **O Admin decide sem ver o comprovante** → é a consequência aceita de separar a leitura de
  arquivo. A tela diz que há comprovante e que ele ainda não é exibível, em vez de silenciar.
- **A fila cresce e a lista fica densa** → o cursor limita a página desde a primeira versão, e a
  ordenação por antiguidade põe o que interessa no topo.
- **`solicitacao_de_participacao` não tem índice por situação** → no Ciclo 01, com uma
  comunidade, o volume não justifica migração; o cursor já limita a varredura.

## Open Questions

- **`RF-02-93` duplicado** no PRD-02 (§6.2 e §6.5). Decidido pelo fundador em 2026-08-22 — o de
  §6.5 recebe identificador novo. Não alcança esta fatia; a correção do PRD entra com a fatia 2.
