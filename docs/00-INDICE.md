# Comunidade Game — Documentação do Projeto

> Documentação de referência do projeto, organizada por temas. Cada documento é
> autocontido e se conecta aos demais por links.

## Estrutura

1. **[01-visao-valores-e-proposito.md](01-visao-valores-e-proposito.md)** — O que é o projeto, por que existe, valores e causas, objetivos, público-alvo e premissas.
2. **[02-conceito-do-jogo-e-gamificacao.md](02-conceito-do-jogo-e-gamificacao.md)** — O "jogo ligado à vida real": personas, poderes, trilhas, batalhas, pontos, níveis, recompensas e o Manual do Jogador.
3. **[03-plataforma-e-arquitetura.md](03-plataforma-e-arquitetura.md)** — Backend API, **as 7 aplicações a serem desenvolvidas** (todas Web Apps responsivos, Mobile First), canais de acesso, princípios técnicos e proteção de dados.
4. **[04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md)** — Economia de recursos ("moeda" da plataforma), pessoa jurídica vinculada, transparência, receitas, desafios extras de Apoiadores e impacto social.
5. **[05-implantacao-e-operacao.md](05-implantacao-e-operacao.md)** — Como implantar em uma comunidade: pontos de apoio, acervo didático, roteiro das aulas, Quiz ao Vivo, formação de mestres, multiplicadores e voluntários, replicabilidade e fases do piloto.
6. **[06-robo-educa.md](06-robo-educa.md)** — **1ª trilha da plataforma**: construir o próprio robô e dar vida a ele com IA por voz.
7. **[07-batalha-de-laser.md](07-batalha-de-laser.md)** — **2ª trilha da plataforma**: enredo, regras e projeto técnico completo da batalha presencial com NodeMCU e MQTT.
8. **[08-base-para-prds.md](08-base-para-prds.md)** — Conteúdo estruturado como insumo para elaboração de PRDs (Product Requirements Documents).
9. **[09-topicos-em-aberto-e-sugestoes.md](09-topicos-em-aberto-e-sugestoes.md)** — Decisões pendentes e propostas em avaliação.
10. **[10-case-01-guerreira-zeferina.md](10-case-01-guerreira-zeferina.md)** — **Case 01**: o piloto real na Comunidade Guerreira Zeferina (Salvador/BA), Ciclo 01 — ago a dez/2026: hipóteses, metas e critérios de avaliação.
11. **[11-modelo-de-gamificacao.md](11-modelo-de-gamificacao.md)** — **Fonte única do motor do jogo**: anatomia da trilha (conteúdo, atividades, desafios, encontros, batalhas, culminâncias), motor de pontuação, níveis, badges, recompensas, distribuição pelas etapas do ciclo e os **reflexos no ecossistema** (vitrine, cards, representação visual da comunidade, jogos sobre o backend), com matriz de rastreabilidade para os PRDs.
12. **[12-guia-do-apoiador.md](12-guia-do-apoiador.md)** — **Guia do Apoiador**: linhas gerais, por que apoiar, estrutura necessária para o Ciclo 01, como apoiar e desafios extras.
13. **[13-codigo-de-conduta-versao-previa.md](13-codigo-de-conduta-versao-previa.md)** — **Código de Conduta (versão prévia)**: modelo básico a ser co-criado com os jogadores na primeira interação presencial.

## As 7 aplicações desta etapa

Definição vigente: **todas as aplicações serão desenvolvidas como Web Apps responsivos,
Mobile First** ([03 §2](03-plataforma-e-arquitetura.md#2-canais--meios-de-acesso)).

| Aplicação | O que faz | PRD |
|---|---|---|
| **App 01 — Onboarding** | Escolha entre áudio ou texto, cadastro de novo jogador (com vínculo à sua Comunidade Virtual) e registro de presença | PRD-04 |
| **App 02 — Assistente por voz** | ChatBot de áudio nos moldes do Robô Educa, com **Modo Ouvinte** na aula | PRD-06 |
| **App 03 — Gestão** | CRUDs, criação das Comunidades Virtuais, entradas manuais e painéis do dia | PRD-02 |
| **App 04 — Jogo** | Jogo em JavaScript sobre a base de personagens da plataforma — **consome pontos, não os gera** (engine sugerida: **Phaser.js**) | PRD-12 |
| **App 05 — Área do Jogador** | Guia e apoio nas trilhas, e acompanhamento das séries de coleta de dados | PRD-05 |
| **App 06 — Vitrine pública** | Apresentação da plataforma, sem login: jogadores, poderes, mestres, batalhas, apoiadores e painéis das comunidades | PRD-03 |
| **App 07 — Pais e responsáveis** | Evolução do jogador, solicitações, direitos de recusa e transparência sobre os dados armazenados | PRD-13 |

## Trilhas

As **duas primeiras trilhas** da plataforma são de autoria do **Mestre fundador**, autor
deste repositório: **[Robô Educa](06-robo-educa.md)** (1ª) e
**[Batalha de Laser](07-batalha-de-laser.md)** (2ª), ambas do Poder da IA e Robótica.

**Toda trilha da plataforma contém desafios de coleta de dados reais** do território do
jogador, e essa coleta **pontua de forma recorrente enquanto a série se mantiver ativa**
([02 §3](02-conceito-do-jogo-e-gamificacao.md#regra-vigente-toda-trilha-coleta-dados-reais)).

O **acervo de 298 livros do projeto Include (Campus Party)** e os **30 kits em MDF**, doados
pelo **Goethe-Institut (Salvador)** — um dos primeiros Apoiadores da plataforma —, são
**material de apoio e insumo dessas duas trilhas** e estão **vinculados ao MVP do
[Case 01](10-case-01-guerreira-zeferina.md#5-o-acervo-include-e-os-kits-mdf-neste-mvp)**.
Inventário em
[02 §3](02-conceito-do-jogo-e-gamificacao.md#acervo-didático-de-apoio--coleção-include-e-kits-mdf-goethe-institut);
posse dos livros em **regime misto** (linha Alpha doada ao jogador na abertura da trilha,
linha Include I como acervo permanente) e estratégia de conservação em
[05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação).

## Como ler

- **[Proposta]** marca ideias ainda **não decididas** pelo fundador — avalie e adote se
  fizer sentido. Todo o resto é definição vigente do projeto.
- Links entre documentos conectam decisões que se sustentam mutuamente.
- O **[doc 11](11-modelo-de-gamificacao.md)** é a fonte normativa de **como os elementos
  do jogo se integram** — trilhas, pontuações, níveis, badges, recompensas e seus reflexos
  na vitrine, nos cards e nos jogos; os PRDs ([doc 08](08-base-para-prds.md)) partem da
  sua [matriz de rastreabilidade](11-modelo-de-gamificacao.md#9-matriz-de-rastreabilidade--prds).
