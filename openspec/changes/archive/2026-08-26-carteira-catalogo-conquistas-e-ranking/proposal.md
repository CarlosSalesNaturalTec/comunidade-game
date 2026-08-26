# Carteira, catálogo, conquistas e ranking na Área do Guerreiro(a)

Origem: **PRD-05 — App 05: Área do Guerreiro(a)**, §§3.1, 5.6, 6.6, 6.7 e 9. **Terceira fatia**
do PRD-05. Atende `RF-05-45`, `RF-05-46`, `RF-05-50`, `RF-05-52`, `RF-05-53`, `RF-05-82`,
`RF-05-83`, `RF-05-84`, `RF-05-86`, `RF-05-87` e `RF-05-88`, sob `RN-05-07`, `RN-05-16`,
`RN-05-18`, `RN-05-21`, `RN-05-39`, `RN-05-40`, `RN-05-41` e `RN-05-42`.

## Why

A App 05 tem entrada e coleta. O que a criança conquista — pontos extras, recompensa de marco,
posição na turma — ela ainda não vê em lugar nenhum: o Ciclo 01 inteiro do PRD-07 corre no
núcleo sem que o dono dos pontos os alcance.

É também o recorte que o núcleo já sustenta quase por inteiro. `GET /v1/eu/pontos-extras`,
`GET /v1/catalogo-avulso`, `GET /v1/trocas` e `GET /v1/entregas` já filtram por persona e já
respondem ao Guerreiro(a) em sessão — o `RF-05-83` está citado no código do catálogo desde a
fatia do catálogo avulso. Duas leituras faltam, e nenhuma cria regra: a **recompensa
conquistada e ainda não entregue**, que hoje só existe depois que o Mestre a entrega, e o
**ranking da turma**, que hoje só existe na versão pública, filtrada pela autorização de
divulgação.

Vem antes do guia da trilha (§6.2) porque não depende de decisão nem de outra aplicação: o
desafio de desbloqueio espera a autoria da App 09, e a inscrição na trilha, decidida em
2026-08-26, ainda precisa nascer no núcleo.

## What Changes

**Núcleo — duas leituras, nenhuma escrita**

- Nasce a leitura das **recompensas de marco conquistadas** pelo Guerreiro(a) em sessão: as
  que o percurso dele já alcançou, cada uma dizendo se a entrega foi confirmada pelo Mestre ou
  se ainda a aguarda. O marco alcançado é conferido contra o mesmo percurso que a capacidade
  `recompensa-de-marco` já deriva na recusa de entrega, sem duplicar a consulta (`RF-05-45`).
- Nasce o **ranking da turma**, logado: ordena por ponto regular, por trilha ou poder, e
  alcança **a turma inteira** — exceção declarada à regra da divulgação, porque a tela é
  logada e restrita à Comunidade Virtual de quem pergunta (`RF-05-52`, `RF-05-53`, `RF-05-84`,
  `RN-05-16`). O ranking público de `leitura-publica-da-vitrine` não muda.
- `GET /v1/eu` passa a declarar, para o Guerreiro(a), se a **autorização de divulgação** dele
  está vigente — derivada do histórico de consentimento, nunca gravada de novo (`RF-05-50`).

**App 05 — carteira, catálogo, conquistas, perfil e ranking**

- **Carteira de pontos extras**: o acumulado e o saldo disponível **separados**, nunca somados
  nem confundidos com ponto regular (`RF-05-82`, `RN-05-39`, `RN-05-40`, `RN-05-42`).
- **Catálogo avulso da comunidade**, com preço em pontos extras e estoque (`RF-05-83`); a tela
  informa que a **troca é presencial, com o Mestre, ao fim do encontro** e **não oferece troca
  nem reserva** (`RF-05-86`, `RF-05-87`).
- **Histórico das trocas** do Guerreiro(a), com item, preço cobrado e data (`RF-05-88`).
- **Conquistas**: a recompensa de marco alcançada, dizendo que quem confirma a entrega é o
  Mestre; nenhuma tela oferece comprar recompensa com pontos de natureza alguma (`RF-05-45`,
  `RF-05-46`, `RN-05-07`, `RN-05-41`).
- **Perfil**: o estado do perfil público e se a divulgação foi autorizada — leitura apenas, já
  que autorizar é ato do responsável na App 07 (`RF-05-50`).
- **Ranking da comunidade** por trilha ou poder, só com pontos regulares, com a turma inteira e
  a própria posição sempre visível; de terceiros, só avatar e nick (`RF-05-52`, `RF-05-53`,
  `RF-05-84`, `RN-05-18`, `RN-05-21`).

## Capabilities

### New Capabilities

Nenhuma. A fatia estende capacidades existentes: a App 05 vive em `area-do-guerreiro` desde a
primeira fatia, e a economia de pontos já está descrita pelas capacidades do PRD-07 e do
PRD-01.

### Modified Capabilities

- `area-do-guerreiro`: a App 05 ganha carteira, catálogo, histórico de trocas, conquistas,
  perfil e ranking.
- `recompensa-de-marco`: nasce a leitura das recompensas conquistadas pelo Guerreiro(a), com a
  situação da entrega.
- `pontos-niveis-e-badges`: nasce o ranking logado da turma, que alcança quem não autorizou
  divulgação.
- `consentimento`: o Guerreiro(a) passa a ler o estado da própria autorização de divulgação.

## Impact

**Código**

- `backend/src/nucleo/recompensas_de_marco/` — a leitura das conquistadas.
- `backend/src/nucleo/pontuacao/` — o ranking da turma.
- `backend/src/nucleo/sessoes/` — o estado da divulgação na saída de `GET /v1/eu`.
- `apps/app-05-guerreiro/` — as telas do bloco, consumindo `comum/`.

**API** — duas rotas novas sob `/v1`, ambas de leitura e restritas ao Guerreiro(a) em sessão, e
um campo novo em `GET /v1/eu`. Nenhuma rota existente muda de contrato: `GET /v1/eu/pontos-extras`,
`GET /v1/catalogo-avulso`, `GET /v1/trocas` e `GET /v1/entregas` são consumidas como estão.

**Infraestrutura** — nenhuma. Nenhuma tabela nova, nenhuma migração.

**Documentação** — o PRD-05 §9 declara `GET /v1/rankings/{comunidade}` como **pública**, o que
contraria o `RF-05-84`, o `RN-05-16` e a decisão do ranking interno já gravada no documento 09:
a tela é logada, e é isso que sustenta a exceção à divulgação. A rota nasce **autenticada**, e a
§9 é corrigida na tarefa de documentação. Não é decisão nova — é o PRD alcançando a fonte.

**Fora do escopo**, reproduzindo o que o PRD-05 §3.2 já exclui: a **execução da troca** é
presencial, no App 01; a **compra de recompensa de marco** não existe em nenhuma natureza de
ponto; a **autorização de divulgação** é ato do responsável, na App 07 — aqui só se lê o
estado; o **acervo do Guerreiro(a)** (`RF-05-47` a `RF-05-49`) entra a partir do Ciclo 02. O
`RF-05-51`, do avatar, fica fora por decisão do fundador de 2026-08-26: é **desejável**, é a
única escrita do bloco e puxa a edição de `Persona`. Guia da trilha, desafios e equipes,
criação original e portfólio são fatias próprias.

**Pendências** — as duas da §14 do PRD-05 tocam este recorte e **não o travam**: o catálogo de
qual marco entrega qual recompensa (`RF-05-45`) e os preços do catálogo avulso (`RF-05-83`) são
cadastro da gestão, não desenho. As telas nascem sobre o que a gestão cadastrar, e sem cadastro
mostram lista vazia.
