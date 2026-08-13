## Context

Ver `proposal.md` — Why. O que o desenho encontra pronto:

- `chave_de_aplicacao` já tem **todas as colunas do ciclo** — `prazo_de_apresentacao`,
  `url_apresentada`, `situacao`, `revogada_por`, `motivo_da_revogacao`, `revogada_em` — e um
  índice parcial `uq_chave_vigente_por_aplicacao_e_ambiente` sobre `(aplicacao, ambiente)`
  quando a situação é vigente.
- A conferência da chave roda como dependência de todo roteador de dados, antes da cota, e
  responde 401 indistinto para ausente, inválida e revogada.
- `solicitacao_de_chave` existe com o ciclo comum da fila e **sem vínculo com a chave**.
- A trilha de auditoria alcança toda escrita por _middleware_: emissão e revogação entram nela
  sem nada a declarar.

Três restrições moldam o desenho. O Cloud Run do Ciclo 01 roda **sem escala horizontal** e
**sem agendador** — não há tarefa periódica onde pendurar o vencimento. O terceiro **não tem
persona**: a solicitação de chave não cria cadastro, então nenhuma rota dele pode exigir
credencial de pessoa. E o segredo **não trafega de volta**: a entrega ao solicitante é ato do
Admin, fora da plataforma, porque não há e-mail no Ciclo 01.

## Goals / Non-Goals

**Goals:**

- Fechar o ciclo da chave de terceiro sem infraestrutura que o Ciclo 01 não tem.
- Manter literal o contrato do PRD-01 §9 e do PRD-03 §9 — nenhuma rota muda de forma.
- Não enfraquecer a recusa indistinta da fatia 1 ao acrescentar situações novas.

**Non-Goals:**

- Rotacionar ou reemitir o segredo de uma chave existente: nenhum requisito o pede.
- Notificar o solicitante de qualquer transição — não há e-mail no Ciclo 01.
- Prever chave de terceiro em desenvolvimento: `RN-01-51` a fecha em produção.

## Decisions

### O vencimento se decide na leitura, e a situação gravada acompanha

O prazo vencido **não** espera tarefa periódica. Toda leitura que depende da situação da chave
aplica a mesma regra — prazo vencido sem URL implica revogada — e **persiste a transição** no
mesmo ato. São dois os pontos de leitura, e é por isso que a situação nunca fica atrasada:

```text
   conferência da chave          leitura de gestão (GET /v1/chaves)
   (a chave chama o núcleo)      (o Admin abre o painel)
            │                                 │
            └──────────► mesma regra ◄────────┘
                    vencida sem URL → revogada
                    grava motivo, sem autoria de pessoa
```

Se a chave nunca mais chamar, o painel do Admin faz a transição; se o Admin nunca abrir o
painel, a chamada da chave faz. Nenhum dos dois caminhos depende do outro.

_Alternativas descartadas:_ tarefa periódica — o Ciclo 01 não tem agendador, e um contêiner só
não sustenta _cron_ confiável. Vencimento só derivado, sem gravar — deixaria `GET /v1/chaves`
mostrando "vigente" numa chave que já recebe 401, que é exatamente o que a decisão do fundador
recusou.

A revogação por decurso grava `motivo_da_revogacao` e deixa `revogada_por` **nulo**: é o que
distingue, no próprio registro, a revogação automática de `RF-01-52` da revogação de Admin de
`RF-01-53`, que exige autoria.

### O identificador da chave é a credencial de apresentação da URL

Quem chama `POST /v1/chaves/{id}/url` é a **vitrine**, com a chave dela (`RF-03-77`,
`RN-03-33`) — o terceiro pode nem ter aplicação no ar. Logo a chave da chamada não prova nada
sobre a chave alvo, e o terceiro não tem persona para autenticar.

O que o solicitante tem, e mais ninguém, é o que o Admin lhe entregou na emissão
(`RF-02-89`): o segredo e o **identificador** da chave. O identificador é um UUID v4 — 122
bits — e **nenhuma rota pública o devolve**: a leitura das chaves é de Admin. Possuí-lo é
prova de ter passado pela emissão, e é o que a rota exige.

```text
Admin emite ──▶ entrega fora da plataforma ──▶ solicitante guarda { id, segredo }
                (RF-02-89, sem e-mail no Ciclo 01)          │
                                                            ▼
                          formulário da Área do Apoiador Desenvolvedor
                          POST /v1/chaves/{id}/url  ◄── chave DA VITRINE
```

_Alternativas descartadas:_ autenticar pela chave do próprio terceiro — quem faz a chamada é a
vitrine. Pedir o segredo no formulário — põe credencial viva num campo público e contraria a
regra de que o segredo nunca volta. Token dedicado de apresentação — inventa artefato que
nenhum PRD nomeia.

### O prazo de 30 dias é configuração

`prazo_de_apresentacao_dias` entra em `Configuracao`, com **30** como valor padrão, ao lado
das cotas e dos limites do freio. O número está decidido em `RN-01-36`; o que a configuração
dá é a mesma liberdade de operação que a duração da sessão e os tetos do freio já têm. O prazo
é **gravado na chave** no ato da emissão, e não recalculado a cada leitura: mudar a
configuração depois NEVER altera o prazo de uma chave já emitida.

### O índice parcial passa a valer só para a chave do projeto

`uq_chave_vigente_por_aplicacao_e_ambiente` ganha `AND natureza = 'do_projeto'` no seu
predicado. A unicidade da chave de terceiro passa a ser garantida do outro lado: um vínculo
**único** de `chave_de_aplicacao` para `solicitacao_de_chave`, que é o que faz "uma
solicitação aprovada, uma chave" ser regra do banco e não só do código.

_Alternativa descartada:_ manter o índice global e exigir nome único por terceiro — cria
colisão que nenhum requisito pede e torna frágil o "nova solicitação é sempre possível".

### A segunda apresentação de URL é recusada

Cumprido o prazo, a chave é vigente por prazo indeterminado e não há mais o que apresentar.
Recusar é a leitura conservadora: não cria capacidade de substituição que nenhum PRD descreve.
Registrado aqui porque é escolha, não consequência — se a operação precisar trocar a URL, é
decisão do fundador, não ajuste de implementação.

## Risks / Trade-offs

- **O `{id}` anda no caminho da URL** e entra em log e histórico do navegador → quem o obtiver
  consegue apenas registrar uma URL alheia e manter viva uma chave que morreria. O Admin vê a
  URL no painel (`RF-02-90`) e revoga (`RF-02-92`). Aceito: o dano é contido e reversível, e
  as alternativas custam mais do que protegem.
- **A recusa de identificador desconhecido distingue-se da recusa por prazo vencido**, o que
  em tese informa que um identificador existe → o identificador é um UUID v4 e não se
  adivinha, de modo que a distinção não entrega nada a quem não o tem. Manter a distinção é o
  que permite orientar quem perdeu o prazo, como o PRD-01 §12 pede.
- **A transição por decurso acontece dentro de uma leitura**, o que torna uma leitura
  escritora → a transição é idempotente e converge para o mesmo estado por qualquer caminho;
  duas leituras concorrentes produzem a mesma revogação. Sem escala horizontal no Ciclo 01, a
  concorrência real é a de requisições no mesmo contêiner.
- **Chave emitida sem entrega bem-sucedida ao solicitante** — o Admin fecha a tela e perde o
  segredo → a chave é revogável e nova solicitação é sempre possível. Nenhum requisito prevê
  reemissão, e criá-la seria regra nova.

## Migration Plan

1. Migração do Alembic: acrescenta a `chave_de_aplicacao` o vínculo único com
   `solicitacao_de_chave`, nulo para as chaves do projeto; recria o índice parcial com o
   predicado da natureza.
2. As dezesseis chaves semeadas seguem válidas sem tocar em nada: elas têm natureza do
   projeto, vínculo nulo e continuam sob a mesma unicidade.
3. Não há chave de terceiro na base — a emissão nasce nesta change —, logo não há dado a
   converter e a migração é reversível pela reversão do índice e da coluna.
