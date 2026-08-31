## Context

O núcleo já tem tudo o que a entrada do responsável precisa: `sessao-do-adulto` (login social,
usuário e senha, trava da senha provisória, recusa de login sem cadastro), `responsavel-e-vinculo`
(vínculo com grau de parentesco, teto de três, recorte da leitura e
`exigir_vinculo_do_responsavel`), a operação `guerreiros_sob_sua_responsabilidade` na matriz de
permissões e a chave `app-07-responsaveis` semeada. O que falta é o cliente e as três leituras.

Do lado do que a evolução mostra, nada é apurado do zero: `trilhas.regra.consultar_progresso` já
devolve nível, obrigatórias desbloqueadas e totais, pontos regulares e badges por trilha —
exatamente o que `GET /v1/eu/progresso` serve ao próprio Guerreiro(a). Presença, `Resultado`,
`PontoRegular`, `Badge`, `CriacaoOriginal` e `OcorrenciaDeConduta` já existem, com as guardas
que cada capability lhes impõe.

## Goals / Non-Goals

**Goals:**

- A App 07 de pé, consumindo `comum/` como as outras cinco, com a esteira da pasta já existente.
- Três leituras novas no núcleo, todas recortadas pelo vínculo vigente, sem entidade nova.
- A evolução montada por reaproveitamento: nenhuma apuração de nível, ponto ou percurso é
  reescrita.

**Non-Goals:**

- Escrita de qualquer espécie pela App 07 — autorização, solicitação e proposta são das fatias 3
  a 6.
- Registro de leitura do termo na primeira tela (jornada 5.1): é `RF-13-29` a `RF-13-34`, fatia 5.
- Estado da reparação da ocorrência: falta requisito que o registre (proposal).

## Decisions

### 1. A leitura da evolução nasce em `backend/src/nucleo/evolucao/`, sem `modelo.py`

O módulo tem `regra.py` e `rotas.py` e **não cria entidade** — o PRD-13 §8 diz que a aplicação
não cria nenhuma. Fica fora de `responsaveis/`, que trata de cadastro e vínculo, porque a
evolução atravessa sete módulos e engordaria o errado. `GET /v1/eu/guerreiros`, ao contrário,
**fica em `responsaveis/rotas.py`**: é a leitura do vínculo, e o `guerreiros_vinculados` que ela
usa já está lá.

_Descartado:_ tudo em `responsaveis/`, que misturaria o cadastro com a leitura agregada.

### 2. Uma chamada por tela, como o PRD-13 §9 declara

`GET /v1/eu/guerreiros/{id}/evolucao` devolve um payload consolidado, e a ocorrência sai em
`GET /v1/eu/guerreiros/{id}/ocorrencias`. São as rotas que o PRD escreveu; a App 07 não faz sete
chamadas para montar uma tela, o que importa no celular modesto de rede instável (PRD-13 §10).

De onde vem cada peça:

| Peça do payload                          | Origem                                                          |
| ---------------------------------------- | --------------------------------------------------------------- |
| Presença                                 | `Presenca` não anulada, por aula, com o momento do fato          |
| Atividades realizadas                    | `Resultado` do Guerreiro(a), com atividade, desfecho e data      |
| Nível, percurso, pontos e badges da trilha | `trilhas.regra.consultar_progresso`, sem reapuração             |
| Pontos por poder                         | `PontoRegular` com `poder_id`, o mesmo recorte da carteira da App 05 |
| Criações validadas                       | `CriacaoOriginal` em `validada`, com título, trilha e `validado_em` |
| Ocorrências                              | `OcorrenciaDeConduta`, com `motivo` (anulável) e momento do fato  |

### 3. O recorte se faz em duas camadas, e a de fora é o papel

`exigir_vinculo_do_responsavel` é permissiva de propósito: para papel que não é responsável ela
não decide nada. Por isso cada rota nova **recusa antes o papel** — só responsável em sessão —,
no molde de `GET /v1/eu/solicitacoes`, e só então exige o vínculo. Sem a primeira camada, um
Mestre em sessão alcançaria a rota do responsável.

### 4. O que não pode aparecer é conferido pela ausência de fonte, e por teste

Nem `evolucao/regra.py` nem a App 07 chegam perto de `assistente/` e `apoio_escolar/`: a
proibição de `RF-13-11` e `RN-13-20` é estrutural, não filtro. `RF-13-12` é o que exige cuidado —
`Resultado` de atividade em equipe e `CriacaoOriginal` coletiva têm outros integrantes por perto.
A saída traz, de terceiro, no máximo avatar e nick, e o teste confere a resposta inteira.

### 5. A App 07 nasce no molde da App 08

`apps/app-07-responsaveis/` copia a estrutura de `apps/app-08-apoiador/` — Vite, React, TS,
`.env.example` com a chave da aplicação, entrada sobre `comum/autenticacao` e a trava da senha
provisória, que ali já resolvem os mesmos três casos de `RF-13-01` a `RF-13-03`. Nenhum workflow
novo: `frontend-ci.yml` já alcança `apps/**`. Falta só registrar a pasta no _workspace_ da raiz.

A alternância entre vinculados (`RF-13-05`) é **estado da aplicação**, não rota: a lista já veio
inteira de `GET /v1/eu/guerreiros`, e trocar de criança troca o `id` da chamada da evolução.

## Risks / Trade-offs

- **A evolução some quando o vínculo termina.** É o efeito correto de `RN-13-04` — o recorte é o
  vínculo vigente —, mas a tela precisa dizer isso, e não mostrar erro cru.
- **Payload consolidado cresce com o histórico da criança.** No Ciclo 01 o volume é de um ciclo
  de uma turma; se crescer, a paginação entra por dentro do payload, sem mudar a rota.
- **A ocorrência sem motivo é a regra, não a exceção, a partir do segundo ciclo.** A tela mostra
  data sem motivo, e não pode inventar texto no lugar.
- **O estado da reparação faltará na tela.** O responsável verá a ocorrência sem saber se a
  reparação foi cumprida — limitação declarada, registrada na §14 do PRD-13 e no documento 09.
  O campo, quando existir, é acréscimo ao payload, sem quebrar a App 07.
