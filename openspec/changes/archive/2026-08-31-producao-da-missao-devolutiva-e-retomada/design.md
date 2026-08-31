## Context

Fatia sobre entidades já de pé. `ProducaoDaMissao` nasceu inteira na fatia 9 do PRD-04, com
`guerreiro_id` anulável reservado a esta fatia e o `CHECK` de "equipe **ou** Guerreiro(a),
exatamente um" já na tabela; `Missao.cadencia_de_retomada` e `DesbloqueioDaMissao` vieram das
fatias do PRD-09; `derivar_percurso` e o padrão "o percurso nasce na leitura, sem tabela de
estado por missão" estão firmados em `openspec/specs/area-do-guerreiro`. O contrato de leitura
e devolutiva — descarte de mídia, devolutiva sem crédito, 503 na leitura indisponível — está
firmado em `openspec/specs/producao-da-missao`. **Nada de esquema muda.**

Motivação e recorte: ver `proposal.md`. As duas decisões de produto desta fatia — onde vive o
"uma vez por agendamento" e quem é "quem recusa foto ou áudio" — foram do fundador e estão
registradas lá.

## Goals / Non-Goals

**Goals:**

- Abrir a porta individual **sobre** o contrato da porta de equipe, sem contrato paralelo.
- Derivar a retomada na leitura, sem coluna, tabela nem migração nova.

**Non-Goals:**

- Qualquer trava nova no `Resultado` ou no lançamento do Mestre.
- Medir, contar ou lançar no livro-razão o consumo do modelo: aqui o custo é recurso de nuvem,
  na régua que `RF-09-90` já fixou e a spec da capacidade já grava.

## Decisions

**1. Duas funções de entrada em `producoes/regra.py`, uma leitura só.**
`registrar_producao` (equipe) fica como está; nasce `registrar_producao_individual`. O que as
duas compartilham — conferência da forma única, chamada ao adaptador, desfecho da leitura
indisponível e montagem do registro — é extraído para um trecho comum; o que difere são as
recusas, que não têm interseção: integrância e aula encerrada de um lado, inscrição e
desbloqueio do outro.
_Alternativa descartada:_ uma função só com `equipe` e `guerreiro` opcionais — o corpo viraria
dois caminhos costurados por `if`, e a recusa de cada porta ficaria ilegível.

**2. A atividade vem declarada no corpo da entrega.**
`atividade_id` é obrigatório na tabela, e a missão pode ter várias atividades. A equipe resolve
isso pela `atividade_corrente_id` que ela declarou na programação do encontro; o Guerreiro(a)
sozinho não tem esse ponteiro. Então o corpo declara a atividade, e o núcleo confere que ela
pertence à missão da rota — 422 se não pertencer.
_Alternativas descartadas:_ tomar a primeira atividade da missão (esconderia da criança o que
ela está entregando); derivar da lista de atividades em aberto da fatia 6 (nem sempre há
exatamente uma).

**3. A trava do percurso reaproveita `derivar_percurso`.**
Inscrição e desbloqueio não são reconferidos por consulta própria a `InscricaoNaTrilha` e
`DesbloqueioDaMissao`: a entrega pergunta ao mesmo `derivar_percurso` que
`GET /v1/eu/trilhas/{id}/missoes/{ordem}` já usa. Uma regra de percurso, um lugar.
_Alternativa descartada:_ consulta direta às duas tabelas — duplicaria a regra e sairia do ar
assim que o percurso mudasse.

**4. O agendamento da retomada se resolve por tempo, sem coluna.**
Cada dia da `cadencia_de_retomada` é um agendamento, com `prazo = momento do desbloqueio + d
dias`. Um agendamento está em aberto quando `agora() >= prazo` e **não existe** produção
individual daquele Guerreiro(a) naquela missão com `registrado_em >= prazo`. Como os prazos
crescem, uma produção posterior a `prazo_i` fecha o agendamento `i` e os anteriores, e uma
produção anterior a todos não fecha nenhum — que é, literalmente, "refazer por conta própria
não rende ponto novo" (`RN-05-38`). Nenhum estado persistido, nada a dessincronizar.
_Alternativas descartadas:_ coluna de agendamento na `ProducaoDaMissao` (levada ao fundador e
recusada — ver `proposal.md`); tabela de agendamentos materializada (estado paralelo ao
percurso, contra o padrão já firmado na capacidade).

**5. Cada rota nasce no módulo dono do que ela lê ou escreve.**
`POST /v1/eu/missoes/{id}/producao` em `producoes/`, onde a entidade mora;
`GET /v1/eu/retomadas` em `trilhas/`, onde vivem percurso, missão e cadência — o mesmo critério
da fatia 6.
_Alternativa descartada:_ módulo `retomadas/` novo — a fatia não tem entidade própria.

**6. A porta individual tem a mesma superfície da porta de equipe.**
`multipart/form-data`, `forma` mais `texto` **ou** `arquivo`, o mesmo
`PortaDaProducaoDaMissao` injetado, os mesmos códigos de erro. O byte do arquivo é lido em
memória e sai de escopo ao fim da chamada, sem tocar `armazenamento`, disco ou log — a garantia
de `RF-05-76` é a mesma de `RF-04-46`, e não se reimplementa.
_Alternativa descartada:_ JSON com a mídia em base64 — inflaria o corpo em 33% no celular
modesto do ponto de apoio (PRD-05 §10).

**7. Na App 05, a entrega entra na tela da missão; a retomada, no bloco da trilha.**
A entrega da produção é passo da missão (PRD-05 §5.3) e fica dentro de `Missao`, depois do
conteúdo e do desafio de desbloqueio. As retomadas viram uma tela do bloco **Trilha** já
existente. A navegação de topo **não cresce**: quatro botões cabem no celular modesto, seis
não — o mesmo argumento da fatia 6.
_Alternativa descartada:_ bloco novo "Retomadas" na navegação de topo.

## Risks / Trade-offs

- **A leitura das retomadas percorre inscrições, desbloqueios e produções de um Guerreiro(a)**
  → o volume do Ciclo 01 é de uma turma por comunidade e a consulta parte sempre de uma só
  criança; nenhuma pré-agregação se justifica agora.
- **O agendamento resolvido por tempo não distingue "entreguei a retomada" de "entreguei a
  missão pela primeira vez, tarde"** → é o comportamento que o fundador escolheu ao manter a
  regra só na App 05: nos dois casos a criança reviu a missão depois do prazo, que é o que a
  retomada quer. Distinguir exigiria a coluna recusada.
- **Retomada de missão cuja trilha foi despublicada continuaria aparecendo** → a derivação
  parte das inscrições em trilha publicada, como `derivar_percurso` já faz; nada de novo.
- **A devolutiva depende de serviço externo e pode não vir** → o desfecho já está fixado na
  capacidade (201 com devolutiva em branco no texto, 503 sem gravar em áudio e foto) e a tela
  passa a dizer isso à criança.

## Migration Plan

Nenhuma migração de esquema: `guerreiro_id` já existe e é anulável, o `CHECK` de exclusividade
já está na tabela, e `cadencia_de_retomada` já está na `Missao`. As duas rotas são novas e não
alteram contrato existente — a porta de equipe segue idêntica. Rollback é reverter o deploy.
