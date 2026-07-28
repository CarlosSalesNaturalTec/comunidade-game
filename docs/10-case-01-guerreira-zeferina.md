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

A comunidade **já foi palco do projeto Robô Educa em 2024**, quando a iniciativa se chamava
**Inova Comunidade** ([01 §1](01-visao-valores-e-proposito.md#nomes-do-projeto)). Isso
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
| **H2** | Os **pais ou responsáveis** vão permitir a participação, tomar conhecimento do tratamento de dados (LGPD) e **aceitar os termos** relativos à criança sob sua responsabilidade | Nº de autorizações de responsável concedidas / nº de jogadores ativos |
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
  presença ([03 §5](03-plataforma-e-arquitetura.md#5-frontend-03--onboarding-cadastro-e-registro-de-presença)).
- **Cadastro da comunidade digital** — a Comunidade Virtual "Guerreira Zeferina" passa a
  existir na medida em que os jogadores registram dados reais do território
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)).
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

### 4.3 Captação de recursos de infraestrutura

Conseguir os **recursos básicos dos recursos digitais da plataforma**: servidores,
armazenamento e execução das aplicações. Como qualquer outro recurso, entram no livro-razão
e compõem o **Poder Econômico** de quem os aportar
([04 §1](04-modelo-economico-e-sustentabilidade.md#1-a-economia-de-recursos-da-plataforma)).

> **Nota de escopo:** a meta de operação vai de **agosto a novembro**; o ciclo se estende a
> **dezembro**, reservado à culminância, à conferência de inventário e à avaliação das
> hipóteses.

## 5. O acervo Include neste MVP

A coleção de **298 livros doada pelo Goethe-Institut** está **vinculada ao MVP do Case 01**:
é neste ciclo, e nesta comunidade, que o acervo entra em uso pela primeira vez como material
de apoio das trilhas 1 e 2
([02 §3](02-conceito-do-jogo-e-gamificacao.md#acervo-didático-de-apoio--coleção-include-goethe-institut)).

Consequências práticas para o ciclo:

- A decisão **doar x reaproveitar** precisa estar tomada **antes da primeira turma**
  ([09 §1](09-topicos-em-aberto-e-sugestoes.md#1-decisões-pendentes)).
- O **tombamento** e a estratégia de conservação são atividade do próprio ciclo
  ([05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação)).
- O **mapeamento capítulo → ponto de trilha** deve cobrir, no mínimo, os pontos das trilhas
  1 e 2 efetivamente aplicados aqui — não o acervo inteiro.
- A prestação de contas do acervo ao fim do ciclo é o primeiro relatório real de
  transparência da plataforma, devido ao Apoiador que doou.

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

Esses cinco pontos são a base dos **indicadores de impacto** que o projeto ainda precisa
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
