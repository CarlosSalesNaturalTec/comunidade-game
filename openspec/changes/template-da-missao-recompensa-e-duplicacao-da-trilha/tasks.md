## 1. Documentação da decisão nova, antes do código

- [ ] 1.1 Gravar a decisão do poder técnico no documento-fonte e na pauta: uma linha nas
      "Regras dos poderes" do documento 02 §2 dizendo que **a marca de técnico é declarada no
      catálogo, nunca deduzida do nome**, e a linha correspondente movida para os já decididos
      do documento 09 §1, com a data de 2026-08-29. Verificar: `npm run lint` e
      `mkdocs build --strict` passam, e o documento 09 não guarda a mesma decisão em aberto.
- [ ] 1.2 Aplicar a decisão no PRD-01: o atributo no `Poder` da §8 e a menção no `RN-01-54` ou
      no `RF-01-62`, sem repetir a regra do documento 02 (`RF-01-62`, `RN-01-54`). Verificar: o
      PRD-01 cita a marca uma vez, e a rastreabilidade da §15 continua fechando.
- [ ] 1.3 Corrigir a linha de `SugestaoDeEstrutura` no PRD-09 §8, retirando o atributo "custo de
      _cloud_ lançado", que o `RF-09-90` proíbe medir, com a nota de correção de rastreabilidade
      no fim da §13, no formato que a seção já usa (`RF-09-90`, `RN-09-07`). Verificar: o PRD-09
      não pede mais medição em lugar algum.

## 2. Catálogo de poderes — a marca de técnico

- [ ] 2.1 Acrescentar a coluna `tecnico` ao `Poder` (padrão falso, não nula), aceitá-la no
      cadastro e na alteração por Admin e devolvê-la na leitura da gestão, sem tocar `natureza`
      nem `papel` (`RF-01-62`, `RN-01-54`, `RF-02-10`, `RN-09-34`). Verificar: os testes do
      catálogo de poderes passam.
- [ ] 2.2 Escrever a migração Alembic desta change — `poder.tecnico` e a tabela
      `sugestao_de_estrutura` da tarefa 3.1 numa revisão só (design — Migration Plan).
      Verificar: `alembic upgrade head` e `downgrade` rodam limpos no banco de teste.
- [ ] 2.3 Apresentar a marca no formulário e na lista de poderes da App 03, em linguagem simples
      dizendo o que ela muda — a sugestão de atividade desplugada (`RF-02-10`, `RN-09-34`).
      Verificar: `poderes.test.tsx` cobre marcar, desmarcar e ler a marca.

## 3. Template da missão — núcleo

- [ ] 3.1 Criar o módulo `template_de_missao` com o modelo `SugestaoDeEstrutura` — missão,
      tópico, estrutura proposta, lacunas e situação (`proposta`, `aceita`, `recusada`,
      `alterada`) —, sem coluna de custo (`RF-09-85`, `RF-09-90`, PRD-09 §8, design — decisão
      4). Verificar: o modelo grava e relê uma sugestão no banco de teste.
- [ ] 3.2 Escrever a porta, a fábrica e os dois adaptadores no padrão de `armazenamento/`: o
      local, sem rede, e o do Gemini para produção, com validação do formato da resposta e
      tratamento de falha como indisponibilidade (`RF-09-85`, `RF-09-95`, `RF-09-91`, documento
      03 §1.12, design — decisões 2, 3). Verificar: a fábrica escolhe o adaptador pelo ambiente
      e o núcleo sobe sem credencial configurada.
- [ ] 3.3 Implementar o cálculo das lacunas no núcleo — missão sem atividade, atividade com
      produção em branco, retomada não declarada e, em trilha de poder técnico, missão sem
      atividade desplugada —, independente do que o modelo respondeu (`RF-09-86`, `RF-09-88`,
      `RN-09-31`, `RN-09-34`, design — decisão 1). Verificar: missão completa devolve lista
      vazia.
- [ ] 3.4 Implementar a regra do pedido de estrutura: só o Mestre autor (403), tópico
      obrigatório (422), sugestão gravada a cada pedido, cadência de 2, 7 e 21 dias e etiqueta
      ODS propostas sem gravar nada na missão, e nenhum lançamento no livro-razão (`RF-09-85`,
      `RF-09-87`, `RF-09-89`, `RF-09-90`, `RF-09-95`, `RF-09-116`, `RN-09-33`). Verificar: o
      teste do módulo passa.
- [ ] 3.5 Publicar `POST /v1/missoes/{id}/estrutura`, devolvendo estrutura e lacunas, e
      respondendo em linguagem simples quando o modelo não vem — 200 com sugestão vazia e as
      lacunas presentes, nunca 5xx e nunca mensagem do provedor (`RF-09-85`, `RF-09-91`, PRD-09
      §9, design — decisão 3). Verificar: o teste de rota cobre autor, não autor, tópico vazio e
      modelo indisponível.
- [ ] 3.6 Registrar o desfecho da sugestão — aceita, recusada ou alterada — sem que ele altere a
      missão (`RF-09-89`, `RN-09-33`). Verificar: recusar uma sugestão deixa a missão intacta.

## 4. Recompensa por desbloqueio e fila do Mestre — núcleo

- [ ] 4.1 Escrever `missoes_desbloqueadas_pelo_guerreiro` em `trilhas/regra.py`, contando só o
      desbloqueio aprovado, e trocá-la por `missoes_concluidas_pelo_guerreiro` nos três pontos de
      `recompensas_de_marco/regra.py` — a quinta recusa da entrega e a leitura do Guerreiro(a) —,
      deixando a função antiga onde nasceu, a serviço dos níveis (`RF-09-84`, `RF-09-75`, design
      — decisão 6). Verificar: os testes de `recompensa-de-marco` passam com a nova derivação.
- [ ] 4.2 Implementar a fila de entregas pendentes do Mestre, filtrada pelo vínculo vigente com
      a comunidade do Guerreiro(a) e não pela autoria da trilha, com nick e avatar, trilha,
      marco, tipo e quantidade, sem moedas nem reais, e publicá-la em
      `GET /v1/recompensas-de-marco/pendentes` (`RF-09-75`, `RN-09-18`, design — decisão 7).
      Verificar: Mestre sem vínculo recebe fila vazia e persona que não é Mestre recebe 403.

## 5. Duplicação da trilha — núcleo

- [ ] 5.1 Implementar a duplicação numa transação — trilha nova em rascunho sob a autoria de quem
      duplicou, com missões e atividades da origem e sem nada que seja fato de pessoa ou lastro —,
      recusando com 403 a duplicação de rascunho alheio e a persona que não é Mestre, e publicá-la
      em `POST /v1/trilhas/{id}/duplicacao` (`RF-09-13`, `RF-09-04`, `RN-09-05`, design — decisão
      8). Verificar: a origem permanece inalterada e a cópia nasce sem inscrição, desbloqueio,
      resultado nem recompensa.

## 6. App 09 — telas

- [ ] 6.1 Criar a tela do template na missão: campo de texto corrente para o tópico, estrutura
      sugerida apresentada como **proposta** e distinta do gravado, lacunas em linguagem simples e
      aviso sem jargão quando a sugestão não vem (`RF-09-85`, `RF-09-86`, `RF-09-91`, `RN-09-16`).
      Verificar: o teste da tela cobre tópico enviado, lacunas apresentadas e sugestão ausente.
- [ ] 6.2 Ligar aceitar, recusar e alterar cada sugestão às rotas de autoria que já existem —
      atividade, cadência e etiqueta ODS —, com a cadência de 2, 7 e 21 dias vindo preenchida e
      alterável, sem gravar conteúdo algum da missão (`RF-09-87`, `RF-09-89`, `RF-09-95`,
      `RF-09-116`, `RN-09-33`). Verificar: aceitar uma atividade grava só ela; recusar não grava
      nada; o conteúdo da missão segue vazio.
- [ ] 6.3 Criar a declaração da recompensa junto da missão — tipo e quantidade, sem preço, sem
      pontos e sem aviso de lastro — e apresentá-la na trilha (`RF-09-84`, `RF-09-71`, `RF-09-72`,
      `RN-09-26`, `RN-09-39`). Verificar: o teste cobre a declaração e a ausência de campo de
      preço.
- [ ] 6.4 Apresentar a fila de entregas pendentes em Minhas turmas, com confirmação da entrega
      pela rota que a fatia 10 do PRD-07 já entregou, recusa traduzida em linguagem simples,
      Guerreiro(a) por nick e avatar e nada em moedas ou reais (`RF-09-75`, `RF-09-76`,
      `RN-09-18`). Verificar: a pendência some da fila depois da entrega confirmada.
- [ ] 6.5 Acrescentar a duplicação na lista de trilhas, com o aviso do que a cópia traz e do que
      não traz, levando o Mestre à trilha nova (`RF-09-13`). Verificar: o teste cobre o aviso,
      a criação em rascunho e a origem inalterada.

## 7. Documentação da entrega

- [ ] 7.1 Marcar as fatias **12** e **13** do PRD-09 como implementadas em
      `openspec/cronograma-de-fatias.md`, com o slug desta change, e corrigir o recorte da fatia
      12 para incluir o `RF-09-116`; atualizar a situação do PRD-09 em `docs/prds/index.md`
      apenas na coluna da tabela. Verificar: as duas linhas trazem o slug e nenhum parágrafo novo
      foi acrescentado ao `index.md`. Nenhum arquivo novo entra em `docs/`, e o `mkdocs.yml` não
      muda.
