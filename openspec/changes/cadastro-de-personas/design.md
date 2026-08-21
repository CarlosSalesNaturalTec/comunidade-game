## Context

Ver `proposal.md` — Why. O núcleo já tem `personas.regra.criar_persona`, com nick, avatar e
papel governados, e já tem as rotas de responsável, vínculo e credencial provisória — falta
apenas expor a criação de persona. A App 03 já tem `comunidades`, `agenda` e `pontos-de-apoio`
como precedente de módulo de tela. Depende de `nick-de-adulto`, que entrega nick opcional em
adulto e unicidade alcançando o Mestre.

## Goals / Non-Goals

**Goals:**

- Expor `criar_persona` sem duplicar a regra que já existe.
- Fechar o caminho da colisão de nick de ponta a ponta, do 422 do núcleo à tela do Admin.

**Non-Goals:**

- Onboarding da criança no App 01 (PRD-04) — esta fatia é o caminho da gestão.
- Fila do pré-cadastro e publicação do card do Apoiador: fatia própria.

## Decisions

**Uma rota por papel, não uma rota com `papel` no corpo.** `POST /v1/guerreiros`,
`POST /v1/mestres`, `POST /v1/apoiadores` e `POST /v1/admins`. Cada papel exige campos
diferentes — nascimento e nick só do Guerreiro(a), artefato comprobatório só do adulto —, e uma
rota única obrigaria validação condicional por papel no corpo, que é onde erro de permissão se
esconde. Alternativa descartada: `POST /v1/personas` com `papel`, mais enxuta e menos legível
no OpenAPI.

**Os artefatos comprobatórios entram em tabela satélite**, seguindo o que
`personas/modelo.py` já declara como padrão — atributo próprio de papel vira satélite quando a
fatia que o traz chega. Cada artefato guarda endereço e rótulo, e a persona pode ter vários.
Alternativa descartada: coluna de texto com os links concatenados, que impediria contar
"ao menos um" sem parsing.

**A gravação do nick pelo Admin é rota separada da edição da persona.** `PUT
/v1/personas/{id}/nick`, de Admin, alcançando só adulto. Manter fora do corpo de edição evita
que uma correção de e-mail carregue nick junto e dispare a colisão sem que o Admin tenha
pedido. Alternativa descartada: nick como campo opcional do `PUT` da persona.

**A App 03 nunca sugere nick ao Admin.** A conferência de disponibilidade da change
`nick-de-adulto` existe para quem escolhe o próprio nick; o Admin está gravando um nick que a
pessoa já lhe passou por fora. Oferecer sugestão ali seria pôr o Admin a inventar identidade
alheia, contra a decisão de que o nick é de quem o usa.

## Risks / Trade-offs

**A tela de cadastro de Guerreiro(a) é a que mais chega perto de dado de criança** — nome,
nascimento e nick numa só tela. Mitigação: `RN-02-22` já veda a imagem, e a tela traz o aviso
de coleta que PRD-02 §11 exige de toda tela que coleta dado; nenhuma delas exibe imagem nem
_template_.

**Adulto sem nick passa a ser estado visível na gestão** — e um Admin pode deixá-lo assim
indefinidamente. Mitigação: a lista sinaliza quem está sem nick e explica a consequência, mas
a fatia não cria prazo nem trava: prazo seria regra nova, e regra nova não nasce em change.

## Migration Plan

Aditiva: nasce a tabela satélite de artefato comprobatório, e os dados próprios de papel que
ainda não tenham satélite ganham o seu. Nenhuma persona existente muda de estado — as semeadas
seguem válidas, sem artefato, porque a exigência vale na criação pela rota nova. Rollback é a
migração inversa.
