# Comunidade Game — Documentação do Projeto

> Documentação de referência do projeto, organizada por temas. Cada documento é
> autocontido e se conecta aos demais por links.

## Situação do projeto

Em **2026** o projeto está em **formato de ideação**: esta documentação compila ideias e
materiais produzidos em datas anteriores e os organiza como projeto. O primeiro case real
previsto é a **[Comunidade Guerreira Zeferina](10-case-01-guerreira-zeferina.md)**, em
Salvador (BA), com o **Ciclo 01 de agosto a dezembro de 2026**.

## Estrutura

1. **[01-visao-valores-e-proposito.md](01-visao-valores-e-proposito.md)** — O que é o projeto, por que existe, valores e causas, objetivos, público-alvo e premissas.
2. **[02-conceito-do-jogo-e-gamificacao.md](02-conceito-do-jogo-e-gamificacao.md)** — O "jogo ligado à vida real": personas, poderes, trilhas, batalhas, pontos, níveis, recompensas e o Manual do Jogador.
3. **[03-plataforma-e-arquitetura.md](03-plataforma-e-arquitetura.md)** — Backend API, **as 5 aplicações a serem desenvolvidas** (todas Web Apps responsivos, Mobile First), frontends (gestão, vitrine, onboarding), canais, personalização por IA, dispositivos embarcados, princípios técnicos.
4. **[04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md)** — Economia de recursos ("moeda" da plataforma), transparência, receitas, despesas, parcerias e impacto social.
5. **[05-implantacao-e-operacao.md](05-implantacao-e-operacao.md)** — Como implantar em uma comunidade: roteiro das aulas, Quiz ao Vivo, cursos, pontos de apoio, formação de mestres, multiplicadores e voluntários, divulgação, replicabilidade.
6. **[06-robo-educa.md](06-robo-educa.md)** — **1ª trilha da plataforma**: construir o próprio robô e dar vida a ele com IA por voz.
7. **[07-batalha-de-laser.md](07-batalha-de-laser.md)** — **2ª trilha da plataforma**: enredo, regras e projeto técnico completo da batalha presencial com NodeMCU e MQTT.
8. **[08-base-para-prds.md](08-base-para-prds.md)** — Conteúdo estruturado como insumo para elaboração de PRDs (Product Requirements Documents).
9. **[09-topicos-em-aberto-e-sugestoes.md](09-topicos-em-aberto-e-sugestoes.md)** — Decisões pendentes e propostas em avaliação.
10. **[10-case-01-guerreira-zeferina.md](10-case-01-guerreira-zeferina.md)** — **Case 01**: o piloto real na Comunidade Guerreira Zeferina (Salvador/BA), Ciclo 01 — ago a dez/2026: hipóteses, metas e critérios de avaliação.

## As 5 aplicações desta etapa

Definição vigente: **todas as aplicações serão desenvolvidas como Web Apps responsivos,
Mobile First** ([03 §2](03-plataforma-e-arquitetura.md#2-canais--meios-de-acesso)).

| Aplicação | O que faz | PRD |
|---|---|---|
| **App 01 — Onboarding** | Escolha entre áudio ou texto, cadastro de novo aluno e registro de presença | PRD-04 |
| **App 02 — Assistente por voz** | ChatBot de áudio nos moldes do Robô Educa, com **Modo Ouvinte** na aula | PRD-06 |
| **App 03 — Gestão** | CRUDs, entradas manuais e painéis do dia | PRD-02 |
| **App 04 — Jogo** | Jogo em JavaScript sobre a base de personagens da plataforma (engine sugerida: **Phaser.js**) | PRD-12 |
| **App 05 — Área do Jogador** | Guia e apoio nas trilhas | PRD-05 |

A **vitrine pública** (PRD-03) permanece no escopo do produto e já está especificada em
[03 §4](03-plataforma-e-arquitetura.md#4-frontend-02--apresentação-da-plataforma-vitrine-pública).

## Trilhas

As **duas primeiras trilhas** da plataforma são de autoria do **Mestre fundador**, autor
deste repositório: **[Robô Educa](06-robo-educa.md)** (1ª) e
**[Batalha de Laser](07-batalha-de-laser.md)** (2ª), ambas do Poder da IA e Robótica.

O **acervo de 298 livros do projeto Include (Campus Party)**, doado pelo
**Goethe-Institut** — um dos primeiros Apoiadores da plataforma —, é **material de apoio
dessas duas trilhas** e está **vinculado ao MVP do
[Case 01](10-case-01-guerreira-zeferina.md#5-o-acervo-include-neste-mvp)**. Inventário em
[02 §3](02-conceito-do-jogo-e-gamificacao.md#acervo-didático-de-apoio--coleção-include-goethe-institut);
guarda, decisão sobre doação x reaproveitamento e estratégia de conservação em
[05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação).

## Como ler

- **[Proposta]** marca ideias ainda **não decididas** pelo fundador — avalie e adote se
  fizer sentido. Todo o resto é definição vigente do projeto.
- Links entre documentos conectam decisões que se sustentam mutuamente.
