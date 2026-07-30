# 10 — Case 01: Comunidade Guerreira Zeferina

> **Primeiro case real da plataforma.** Este documento é a fonte única do piloto: contexto,
> ciclo, hipóteses, metas e critérios de avaliação.

## 1. Estado do projeto e do case

O **Comunidade Game** está, em Julho de 2026, em **formato de ideação**: a documentação deste
repositório compila ideias, materiais e experiências acumulados em datas anteriores e os
organiza como projeto. Nada do que está aqui foi ainda validado em operação da plataforma —
o que já foi validado é a **prática presencial** (oficinas do [Robô Educa](06-robo-educa.md)
desde 2018).

O **Case 01 — Comunidade Guerreira Zeferina** é o ponto em que a ideação encontra a
realidade: a primeira comunidade em que a plataforma será implantada e medida.

| | |
|---|---|
| **Comunidade** | Guerreira Zeferina |
| **Localização** | Salvador — Bahia — Brasil |
| **Ciclo 01** | **Agosto a dezembro de 2026** |
| **Escopo do ciclo** | Implantação do **MVP** da plataforma + trilhas 1 e 2 |
| **Situação em jul/2026** | Ideação concluída; hipóteses formuladas; ciclo por iniciar |

## 2. Por que Guerreira Zeferina

A comunidade **já foi palco do projeto em 2024**, quando a iniciativa se chamava
**Inova Comunidade** ([01 §1](01-visao-valores-e-proposito.md#nomes-do-projeto)). Aquela
edição reuniu o **Robô Educa**, o **Poder da Rima** e o **Poder da Capoeira** — os três
realizados e validados na própria comunidade; Rima e Capoeira serão retomados em ciclo
futuro ([02 §3](02-conceito-do-jogo-e-gamificacao.md#demais-trilhas-previstas)). Isso
significa que o piloto **não começa do zero**:

- Existe **relação prévia** com moradores, lideranças e famílias.
- Existe **memória concreta** do que funcionou e do que não funcionou na edição de 2024.
- O público-alvo local **já viu uma oficina acontecer** — a proposta não é abstrata para ele.

Em um projeto cujo maior risco é a adesão, começar por um território onde já houve entrega é
a decisão de menor risco possível.

> A comunidade escolhida também atende ao critério de
> [05 §1](05-implantacao-e-operacao.md#1-estratégia-de-implantação): implantação inicial em
> comunidade **próxima à residência do fundador**, para viabilizar a presença frequente que o
> primeiro ciclo exige.

## 3. Hipóteses do Ciclo 01 (formuladas em jul/2026)

O ciclo é, antes de tudo, um **teste de hipóteses**. Elas estão escritas aqui na forma em que
foram formuladas, para que ao fim do ciclo seja possível dizer, sem reescrever a história, se
cada uma se confirmou.

| # | Hipótese | Como se verifica |
|---|---|---|
| **H1** | O público-alvo inicial — **crianças e jovens de 6 a 16 anos** — vai se interessar pelo tema e **se inscrever** na plataforma e nas trilhas | Nº de cadastros efetivados no onboarding (App 01) e nº de jogadores que iniciam uma trilha |
| **H2** | Os **pais ou responsáveis** vão permitir a participação, tomar conhecimento do tratamento de dados (LGPD) e **aceitar os termos** relativos à criança sob sua responsabilidade | Nº de autorizações de responsável concedidas / nº de jogadores ativos, medido na **App 07** ([03 §9](03-plataforma-e-arquitetura.md#9-app-07--área-dos-pais-e-responsáveis)) |
| **H3** | Os **recursos de implantação do MVP** serão supridos pela equipe de **mestres e apoiadores** | Lastro registrado no livro-razão x recursos necessários às atividades previstas ([04](04-modelo-economico-e-sustentabilidade.md)) |

Observações sobre as hipóteses:

- **H1 e H2 são independentes.** A [adesão em duas etapas](02-conceito-do-jogo-e-gamificacao.md#9-manual-do-jogador-fluxo-de-entrada)
  foi desenhada exatamente para isso: o jogador participa com cadastro livre (H1), e a
  autorização do responsável (H2) libera apenas a **divulgação pública** do perfil. Se H1 se
  confirmar e H2 não, o ciclo ainda acontece — o que não acontece é a vitrine.
- **H3 é condição de existência.** Pela regra de lastro, **atividade sem recurso provido não
  ocorre** ([04 §1](04-modelo-economico-e-sustentabilidade.md#1-a-economia-de-recursos-da-plataforma)).
  H3 falhar não degrada o ciclo: interrompe-o. É a hipótese a monitorar mais de perto.

## 4. Desafio / Meta do Ciclo 01

**Implantar o MVP na Comunidade Guerreira Zeferina**, com três frentes simultâneas:

### 4.1 Operação na comunidade — agosto a novembro de 2026

- **Credenciamento de jogadores** — cadastro pelo App 01 (áudio ou texto) e registro de
  presença ([03 §3](03-plataforma-e-arquitetura.md#3-app-01--onboarding-cadastro-e-registro-de-presença)).
- **Cadastro da comunidade digital** — a Comunidade Virtual "Guerreira Zeferina" é **criada
  vazia por um Admin antes do primeiro onboarding** (sem ela não há como vincular jogador) e
  passa a existir de fato na medida em que os jogadores registram dados reais do território
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)). **Toda trilha do
  ciclo precisa ter ao menos um desafio de coleta**, com cadência definida — é o que faz a
  comunidade digital ganhar corpo dentro do Ciclo 01
  ([02 §3](02-conceito-do-jogo-e-gamificacao.md#regra-vigente-toda-trilha-coleta-dados-reais)).
- **Implementação das trilhas 1 e 2** — [Robô Educa](06-robo-educa.md) e
  [Batalha de Laser](07-batalha-de-laser.md), com os encontros presenciais em **dinâmica
  assíncrona** ([05 §3](05-implantacao-e-operacao.md#3-roteiro-da-aula-presencial)).

### 4.2 Construção dos artefatos digitais

Construir o que os **PRDs deste projeto** especificam
([08-base-para-prds.md](08-base-para-prds.md)):

- **Backend API** (PRD-01) — núcleo do qual tudo depende.
- **Aplicações desta etapa** — as cinco apps definidas em
  [03 §2.1](03-plataforma-e-arquitetura.md#21-aplicações-a-serem-desenvolvidas), priorizadas
  conforme as fases de [05 §11](05-implantacao-e-operacao.md#11-fases-sugeridas-de-implantação-do-piloto-proposta).
- **Ecossistema digital** — o universo em que as Comunidades Virtuais existem
  ([01 §7](01-visao-valores-e-proposito.md#7-o-fundador-primeiro-admin-e-primeiro-mestre)).

> **Transparência de método:** os artefatos digitais do Ciclo 01 são construídos com o
> **auxílio e a potencialização de ferramentas de IA**, sob idealização e direção humanas —
> a IA é a alavanca que permite ao fundador entregar o escopo acima dentro do prazo do
> ciclo ([01 §7](01-visao-valores-e-proposito.md#como-os-artefatos-são-construídos--ia-como-alavanca)).

### 4.3 Captação de recursos de infraestrutura

Conseguir os **recursos básicos dos recursos digitais da plataforma**: servidores,
armazenamento e execução das aplicações. Como qualquer outro recurso, entram no livro-razão
e compõem o **Poder Econômico** de quem os aportar
([04 §1](04-modelo-economico-e-sustentabilidade.md#1-a-economia-de-recursos-da-plataforma)).

> **Nota de escopo:** a meta de operação vai de **agosto a novembro**; o ciclo se estende a
> **dezembro**, reservado à culminância, à conferência de inventário e à avaliação das
> hipóteses.

## 5. O acervo Include e os kits MDF neste MVP

A coleção de **298 livros** e os **30 kits em MDF** doados pelo **Goethe-Institut
(Salvador)** estão **vinculados ao MVP do Case 01**: é neste ciclo, e nesta comunidade, que
entram em uso pela primeira vez como material de apoio e insumo das trilhas 1 e 2
([02 §3](02-conceito-do-jogo-e-gamificacao.md#acervo-didático-de-apoio--coleção-include-e-kits-mdf-goethe-institut)).

Consequências práticas para o ciclo:

- **Regime misto já decidido:** os 252 exemplares da **linha Alpha são entregues ao jogador
  na abertura da trilha** — providenciar a logística da entrega e o kit de encapar antes da
  primeira aula. Os 46 da **linha Include I** ficam como acervo permanente do ponto de apoio
  ([05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação)).
- O **tombamento dos 46 exemplares permanentes** e a estratégia de conservação são atividade
  do próprio ciclo.
- Os **30 kits MDF** dimensionam a primeira turma que monta o robô em MDF; o saldo precisa
  estar visível no painel do dia.
- O **mapeamento capítulo → ponto de trilha** deve cobrir, no mínimo, os pontos das trilhas
  1 e 2 efetivamente aplicados aqui — não o acervo inteiro.
- A prestação de contas do acervo ao fim do ciclo é o primeiro relatório real de
  transparência da plataforma, devido ao Apoiador que doou — que assinou **Termo de Doação**
  com a **Robô Educa — Kits Robóticos Educacionais**
  ([04 §1](04-modelo-economico-e-sustentabilidade.md#pessoa-jurídica-vinculada-ao-projeto)).

### 5.1 [Proposta] Distribuição das trilhas e do acervo no Ciclo 01

Aplicação do modelo de distribuição de trilha por etapas do ciclo
([11 §2.3](11-modelo-de-gamificacao.md#23-distribuição-da-trilha-pelas-etapas-do-ciclo))
ao calendário ago–dez/2026. Marcada como proposta porque o calendário dos encontros ainda
é pendência do case ([§7](#7-pontos-a-definir-do-case)).

| Período | Etapa | Trilha em foco | Conteúdo e acervo |
|---|---|---|---|
| **Agosto** | Abertura | **Trilha 1 — Robô Educa** (início) | Onboarding e credenciamento; Comunidade Virtual criada antes do 1º encontro; ritual de entrada — entrega dos livros **Alpha Mecânica** (montagem do corpo) e do **kit MDF ou PET**; abertura das **séries de coleta** com cadência definida |
| **Setembro** | Desenvolvimento | Trilha 1 — pontos intermediários | Voz, prompts, limites da IA; **Include Programação I** e **Include Mecânica I** em bancada; séries de coleta rendendo pontos; desafios extras de Apoiadores |
| **Outubro** | Desenvolvimento / transição | Conclusão da trilha 1 → **Trilha 2 — Batalha de Laser** (início) | Publicação da versão do robô (fecho da trilha 1); entrega dos livros **Alpha Eletrônica** e **Alpha Sensores** na abertura da trilha 2; construção dos artefatos; **Include Eletrônica I** e **Include Sensores I** em bancada |
| **Novembro** | Desenvolvimento + marco | Trilha 2 completa | Wi-Fi/MQTT, lógica do jogo, sensor de território instalado; **Batalha de Laser** presencial como marco do ciclo, com telemetria alimentando ranking e portfólio |
| **Dezembro** | Fechamento | — | **Culminância** (apresentação pública, com consentimentos), conferência de inventário do acervo, prestação de contas ao Apoiador e avaliação das hipóteses H1–H3 |

Notas de paginação:

- A dinâmica é **assíncrona**: os meses indicam onde o **planejamento de recursos e de
  bancada** se concentra, não uma exigência de que todos os jogadores estejam no mesmo
  ponto — quem entra em outubro começa pela abertura da trilha 1 normalmente.
- A transição trilha 1 → trilha 2 é **por jogador/equipe**, ao concluir a trilha 1; o mês
  de outubro é apenas o centro de gravidade esperado.
- Os **30 kits MDF** limitam as montagens em MDF da trilha 1; o saldo no painel do dia
  define quando a oficina passa ao material reciclado
  ([05 §2](05-implantacao-e-operacao.md#c-kits-em-mdf-30-unidades)).
- O **mapeamento capítulo → ponto de trilha** precisa estar pronto para os pontos de cada
  mês antes de o mês começar — cobre só o que o ciclo usa, não o acervo inteiro
  ([09 §1](09-topicos-em-aberto-e-sugestoes.md#1-decisões-pendentes)).

## 6. Como o ciclo é avaliado

Ao fim de dezembro de 2026, o ciclo responde:

1. **Adesão (H1)** — quantos jogadores se cadastraram, quantos iniciaram trilha, quantos
   permaneceram até a culminância.
2. **Consentimento (H2)** — quantos responsáveis autorizaram a divulgação do perfil; quais
   foram as dúvidas e objeções recorrentes sobre dados da criança.
3. **Lastro (H3)** — quais atividades aconteceram, quais não aconteceram por falta de
   recurso, e quem proveu o quê.
4. **Entrega técnica** — quais aplicações chegaram a rodar em condição real de aula, com
   rede instável e aparelhos modestos.
5. **Território** — quantos registros de dados alimentaram a Comunidade Virtual e o que eles
   já permitem dizer sobre o lugar.
6. **Protagonismo** — quantas criações originais os jogadores apresentaram na culminância e
   quantas sugestões de melhoria registraram para as atividades e para a plataforma
   ([02 §4](02-conceito-do-jogo-e-gamificacao.md#criações-originais-dos-jogadores)).

Esses seis pontos são a base dos **indicadores de impacto** que o projeto ainda precisa
formalizar ([09 §2](09-topicos-em-aberto-e-sugestoes.md#indicadores-de-impacto)) — e o
*baseline* contra o qual a segunda comunidade será comparada.

## 7. Pontos a definir do case

- **Ponto de apoio físico** na comunidade: qual espaço, com que disponibilidade e quem
  responde pela guarda do acervo ([05 §2](05-implantacao-e-operacao.md#2-estrutura-física--pontos-de-apoio)).
- **Calendário do ciclo**: datas dos encontros presenciais entre agosto e novembro e data da
  culminância.
- **Tamanho da turma** e número de mestres/voluntários necessários por encontro.
- **Metas numéricas** de H1 e H2 — quantos cadastros e quantas autorizações caracterizam
  hipótese confirmada.
- **Registro da edição de 2024** (Inova Comunidade): reunir o que existe de memória, fotos e
  contatos daquela edição como linha de base do relacionamento com a comunidade.
