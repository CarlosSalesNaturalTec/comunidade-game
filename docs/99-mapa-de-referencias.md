# 99 — Mapa de Referências (orientação para IA)

> **Esta página não é leitura para humanos.** Os demais documentos da pasta `/docs` foram
> deliberadamente limpos de referências cruzadas para ficarem legíveis por pessoas. Toda a
> relação entre documentos — fonte única de cada assunto, dependências e rastreabilidade para
> os PRDs — está consolidada aqui, para orientar agentes de IA que leiam, revisem ou derivem
> artefatos a partir desta documentação.

## 1. Regra de fonte única

Cada assunto tem **um** documento normativo. Alterar o assunto significa alterar esse
documento. Os demais, quando precisam citar o assunto, resumem em uma frase e **nunca
repetem a regra completa** — repetição é o defeito que esta documentação combate.

| Assunto                                                                                                                                                                                                                                                                               | Fonte única |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| Visão, valores, causas, objetivos, público-alvo, fundador, transparência sobre IA                                                                                                                                                                                                     | 01          |
| Personas, solicitação de participação, Comunidades Virtuais (conceito e regras de coleta), poderes, trilhas, atividades e desafios, criações originais, equipes, batalhas, recompensas, manual do Guerreiro(a)                                                                        | 02          |
| Princípios de arquitetura, organização do repositório, stack e hospedagem, canais, as 8 aplicações, licenças, LGPD da plataforma                                                                                                                                                      | 03          |
| Economia de recursos, moeda da plataforma, livro-razão, pessoa jurídica, receitas, titularidade dos dados publicados, desafios extras (regras completas), impacto social, aderência à Agenda 2030 e indicadores de cobertura                                                          | 04          |
| Pontos de apoio, acervo didático (inventário, regime misto, guarda), roteiro do encontro, Quiz ao Vivo, formação de multiplicadores, replicabilidade, fases do piloto                                                                                                                 | 05          |
| Trilha 1 — Robô Educa                                                                                                                                                                                                                                                                 | 06          |
| Trilha 2 — Batalha de Laser                                                                                                                                                                                                                                                           | 07          |
| Requisitos por PRD (**único documento extenso entre os 01–15**)                                                                                                                                                                                                                       | 08          |
| Requisitos de produto por aplicação (**derivados — nenhum PRD é fonte única**)                                                                                                                                                                                                        | `prds/`     |
| Decisões pendentes e propostas                                                                                                                                                                                                                                                        | 09          |
| Case 01 — Guerreira Zeferina, Ciclo 01                                                                                                                                                                                                                                                | 10          |
| Motor do jogo: anatomia da trilha, taxonomia, pontuação, níveis, badges, reflexos no ecossistema, etiqueta ODS da trilha                                                                                                                                                              | 11          |
| Guia do Apoiador (documento **derivado**, sem regra própria)                                                                                                                                                                                                                          | 12          |
| Código de Conduta do Guerreiro(a)                                                                                                                                                                                                                                                     | 13          |
| Gamificação do Apoiador: níveis de necessidade, modalidades de apoio, perfis PF e PJ, missão do Apoiador, níveis de sustento, selos, técnicas admitidas e vedadas, portas de entrada por modalidade                                                                                   | 14          |
| Identidade visual das aplicações: paleta, tipografia, medida, marcos de largura, acessibilidade (WCAG AA), temperamentos, sistema de avatar, forma da carta, emblema de nível, silhueta de badge, glifo de poder, sistema de ícone, gráfico de série, fichas de ponto e moeda, tokens | 15          |

## 2. Papel e dependência dos documentos

| Doc   | Tipo                                 | Depende de             | Alimenta         |
| ----- | ------------------------------------ | ---------------------- | ---------------- |
| index | Índice (home do site)                | —                      | —                |
| 01    | Normativo (fundação)                 | —                      | 02, 03, 12, 13   |
| 02    | Normativo (conceito)                 | 01                     | 03, 05, 08, 11   |
| 03    | Normativo (técnico)                  | 02                     | 08               |
| 04    | Normativo (econômico)                | 02                     | 08, 12           |
| 05    | Normativo (operação)                 | 02, 04                 | 08, 10           |
| 06    | Normativo (conteúdo)                 | 02                     | 03 §4, 08, 10    |
| 07    | Normativo (conteúdo)                 | 02, 06                 | 08, 10           |
| 08    | **Derivado** — requisitos            | 01–07, 11, 14          | PRDs a gerar     |
| 09    | Pauta                                | todos                  | 08               |
| 10    | Normativo (case)                     | 02–08, 11              | 08, 09           |
| 11    | Normativo (motor)                    | 02                     | 08               |
| 12    | **Derivado** — comunicação           | 01, 02, 04, 05, 10, 14 | —                |
| 13    | Normativo (conduta)                  | 01, 02                 | 05               |
| 14    | Normativo (apoio)                    | 02, 04, 11             | 08, 12           |
| 15    | Normativo (visual)                   | 01, 02, 03, 11         | `prds/`          |
| prds/ | **Derivado** — requisitos de produto | 08, 01–07, 11, 13–15   | `openspec/` (§9) |

**Divisão 02 × 11 (a confusão mais provável):** o doc 02 define **o que são** os elementos
do jogo; o doc 11 define **como eles se ligam e quanto valem**. Tabelas de pontuação,
níveis, badges e taxonomia existem **apenas no doc 11**.

**Divisão 11 × 14:** o doc 11 é fonte única do motor de pontos, níveis e badges **do
Guerreiro(a)**. Os níveis de sustento e os selos **do Apoiador** — que correm em moedas, não
em pontos — ficam **apenas no doc 14**.

**Divisão 11 × 15:** o doc 11 diz **o que** cada card mostra e **como o território cresce**
conforme o dado chega; o doc 15 diz **como isso se parece** — paleta, tipografia, moldura,
silhueta de badge, emblema de nível, glifo de poder e gráfico de série. Composição de card e
mapa dado → elemento visual ficam **apenas no doc 11**; cor, forma e medida ficam **apenas no
doc 15**.

## 3. Conceitos e onde vivem

| Conceito                                                                   | Definido em                                | Citado (sem redefinir) em      |
| -------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------ |
| Ciclo de evolução positiva                                                 | 01 §1                                      | 12                             |
| Protagonismo dos Guerreiros e Guerreiras / criação original                | 01 §3 (valor) e 02 §4 (mecânica)           | 03, 05, 06, 07, 08, 11, 12, 13 |
| Transparência sobre uso de IA                                              | 01 §7                                      | 03, 08, 10, 12, 13             |
| Adesão em duas etapas (cadastro livre × divulgação autorizada)             | 03 §12                                     | 01, 02, 08, 09, 10             |
| Autorização única do responsável (divulgação e captação)                   | 03 §12                                     | 02 §§1, 9, 03 §9, 08, 09       |
| Comunidade Virtual (criação, vínculo, granularidade)                       | 02 §1                                      | 03, 05, 08, 10, 11             |
| Série temporal de coleta e pontuação recorrente                            | 02 §1                                      | 03, 06, 07, 08, 11             |
| Guarda permanente com coletor identificado / anonimização na saída         | 02 §1                                      | 03 §12, 08, 09                 |
| Base legal do dado de território (duas camadas) e revogação                | 03 §12.1                                   | 02 §1, 08, 09, 13              |
| Prazos de guarda e fim do vínculo                                          | 03 §12.2                                   | 02 §1, 03 §§3.3, 7, 08, 09     |
| Periodicidade das auditorias por amostragem                                | 03 §11 (corpus e trilhas) e 02 §1 (coleta) | 03 §5, 08, 09                  |
| Regra "toda trilha coleta dados reais"                                     | 02 §3                                      | 06, 07, 08, 10, 11             |
| Poder do Território                                                        | 02 §2                                      | 08, 11                         |
| Governança de personas (só Guerreiro(a) tem autocadastro)                  | 02 §1                                      | 01, 05, 08                     |
| Cadastro do responsável e vínculo com os Guerreiros e Guerreiras           | 02 §1                                      | 03 §§1.1, 5, 9, 11, 08, 09     |
| Autenticação por persona (nick e imagem; Apps 04 e 06 sem login)           | 03 §1.1                                    | 02, 08, 09                     |
| Credencial de dispositivo do sensor                                        | 03 §1.1                                    | 02 §1, 08                      |
| Solicitação de participação como Mestre ou Apoiador                        | 02 §1                                      | 03 §§5, 8, 08, 12              |
| Equipes (grupo livre até 5, formadas no App 01; da aula e da trilha)       | 02 §5                                      | 03 §§4, 5, 08, 11 §4           |
| Comunidade do onboarding vinda da aula agendada                            | 02 §1                                      | 01, 03 §§3, 5, 08, 10          |
| Guerreiro(a) como termo da persona primária                                | 02 §1                                      | 01, 03, 08, 09                 |
| Moeda da plataforma (1 moeda = R$ 10,00; escala fixa por ciclo)            | 04 §1                                      | 03 §8, 08, 11 §8.2, 12         |
| Entrega de dados (gratuita, íntegra e aprovada por Admin)                  | 03 §12.3                                   | 04 §2, 08, 09                  |
| Produção executiva (tempo do fundador e dos Admins, por absorção)          | 04 §1                                      | 08, 09, 10 §4.3                |
| Recortes da vitrine (sociedade civil, pesquisadores, gestores)             | 03 §8                                      | 04 §4, 08, 09                  |
| Nome do projeto e endereço canônico da plataforma                          | 01 §1                                      | 03 §1, 09                      |
| Vitrine na raiz do domínio e botão "Entrar" por persona                    | 03 §§1, 8                                  | 08                             |
| Área do gestor público (para que serve ao município e ao estado)           | 03 §8                                      | 04 §4, 08                      |
| Granularidade da saída pública (agrega até o bairro)                       | 02 §1                                      | 03 §§8, 12, 08, 09             |
| Novidade dos favoritos (cinco fatos, 30 dias; só na App 08)                | 03 §10                                     | 02 §1, 03 §8, 08               |
| Proteção das rotas públicas (limite por origem, atraso)                    | 03 §8                                      | 02 §1, 08                      |
| Aviso de LGPD visível nas aplicações e área detalhada                      | 03 §12                                     | 08, 09                         |
| Área do Apoiador (App 08) e registro de propostas                          | 03 §10                                     | 04, 08, 09, 12                 |
| Efetividade do apoio (painel vivo, agregado e por avatar)                  | 04 §3                                      | 03 §10, 08, 12                 |
| Aporte pela App 08 em dinheiro; material e serviço pelo Admin              | 02 §1 e 03 §10                             | 04 §2, 08                      |
| Pré-cadastro do Apoiador (aporte declarado e comprovante)                  | 02 §1 e 03 §10                             | 04 §2, 08                      |
| Identidade do Apoiador (avatar, nick, moldura e piso de 10 moedas)         | 11 §8.2                                    | 02 §1, 03 §§8, 10, 08          |
| Paleta, tipografia, medida, marcos de largura e tokens das aplicações      | 15 §§3, 4, 12                              | 03 §8                          |
| Acessibilidade digital das aplicações (WCAG 2.2 AA)                        | 15 §5                                      | 09, `prds/` §10 de cada um     |
| Temperamentos Operação e Arena                                             | 15 §6                                      | 03 §2                          |
| Sistema de avatar do Guerreiro(a) e avatar padrão do projeto               | 15 §7                                      | 02 §1, 03 §3.2, 11 §8.2        |
| Forma da carta, emblema de nível, silhueta de badge e glifo de poder       | 15 §8                                      | 02 §2, 11 §§7, 8.2             |
| Fichas de ponto, ponto extra e moeda                                       | 15 §9                                      | 04 §1, 11 §5                   |
| Sistema de ícone e gráfico de série das aplicações                         | 15 §11                                     | 11 §8.3                        |
| Área do Mestre (App 09) — autoria e operação                               | 03 §11                                     | 02, 05, 08, 09                 |
| Publicação da trilha (sem aprovação prévia, travas e conteúdo)             | 03 §11                                     | 02, 05, 08, 11                 |
| Atividade da missão (modalidade e formato)                                 | 11 §§2.1, 4                                | 02, 03 §11, 08                 |
| Modelo de missão (produção, sondagem, retomada, obrigatoriedade)           | 11 §2.2                                    | 02 §§3, 4, 03 §§4, 7, 11       |
| Hipóteses do Ciclo 01 (H1 a H5) e como cada uma se verifica                | 10 §3                                      | 08, 09, `prds/`                |
| Leitura da produção do Guerreiro(a) e devolutiva construtiva               | 03 §§4, 7 e 11 §2.2                        | 02 §4, 09                      |
| Auxílio de IA na autoria da trilha (estrutura, não conteúdo)               | 03 §11                                     | 01 §7, 09                      |
| Recompensa conquistada em marco da trilha                                  | 02 §8                                      | 03 §7, 08, 11 §2.1, 12         |
| Acompanhamento por nick e favoritos (só do Apoiador)                       | 02 §1 e 03 §10                             | 03 §8, 04 §3, 08, 12           |
| Licença do código (AGPL)                                                   | 03 §1                                      | 01, 08                         |
| Licença do conteúdo educacional (CC BY-SA)                                 | 03 §1                                      | 01, 08, 09                     |
| Regra de lastro (atividade só com recurso provido)                         | 04 §1                                      | 02, 05, 10, 11, 12             |
| Poder Sustentador                                                          | 04 §1                                      | 02, 12, 14                     |
| Cobertura parcial da necessidade de recurso                                | 04 §1                                      | 08, 12, 14                     |
| Escadas de valores sugeridos (pessoa física e pessoa jurídica)             | 04 §2                                      | 02 §1, 08, 12, 14              |
| Níveis de necessidade da plataforma (Existir a Permanecer)                 | 14 §2                                      | 04 §1, 08, 12                  |
| Modalidades de apoio e portas de entrada por modalidade                    | 14 §§3, 10                                 | 02 §1, 03 §§8, 10, 08, 12      |
| Perfil pessoa física e pessoa jurídica do Apoiador                         | 14 §4                                      | 02 §1, 04 §2, 08               |
| Missão do Apoiador (individual e coletiva)                                 | 14 §§5, 6                                  | 04 §1, 08, 12                  |
| Níveis de sustento e selos do Apoiador                                     | 14 §§7, 8                                  | 02 §1, 11 §§3, 8.2, 08, 12     |
| Técnicas de gamificação admitidas e vedadas no apoio                       | 14 §9                                      | 04, 08, 12                     |
| Apoio em código como aporte (**proposta**)                                 | 04 §1 e 14 §3                              | 03 §1, 08, 09, 11 §8.4         |
| Desafios extras (aberto e direcionado)                                     | 04 §3                                      | 02, 08, 11, 12                 |
| Acervo Include e kits MDF (inventário, regime misto, guarda)               | 05 §3                                      | 02, 04, 09, 10                 |
| Encontro assíncrono                                                        | 05 §4                                      | 03, 08, 11                     |
| Quiz ao Vivo                                                               | 05 §5                                      | 03, 08, 11                     |
| Mestre Aprendiz (nível 5) e multiplicadores                                | 11 §6 (motor) e 05 §6 (operação)           | 02, 08                         |
| Níveis, badges, tabela de pontos, taxonomia de atividades                  | 11 §§4–7                                   | 02, 08                         |
| Nível como percurso da trilha (gates dos níveis 1 a 5)                     | 11 §6                                      | 02 §7, 08                      |
| Integridade dos pontos (travas antifraude)                                 | 11 §5.1                                    | 02 §1, 05 §5                   |
| Canal de sugestões do Guerreiro(a) (formato, prazo e crédito)              | 03 §7                                      | 11 §§5, 7, 13 §5               |
| Apoio escolar por assistente de voz, com corpus fechado e IA               | 03 §7                                      | 03 §§4, 5, 11, 08, 10 §4.3     |
| Personalização por IA (sessão, reescrita no corpus, ponte)                 | 03 §7.1                                    | 03 §§4, 9, 12.2, 08            |
| Reparação que zera a ocorrência de conduta                                 | 13 §3                                      | 11 §5                          |
| Regras da partida do Quiz ao Vivo (resposta da equipe, acerto e desempate) | 05 §5                                      | 03 §§4, 5, 11, 08, 11 §5       |
| Contrato dos jogos (somente leitura: lê progresso e nada escreve)          | 11 §8.4                                    | 03 §6, 08                      |
| LGPD, avatares e imagem do Guerreiro(a)                                    | 03 §§3.3, 12                               | 02, 08, 09, 13                 |
| Etiqueta ODS da trilha (descritiva, sem ponto; trava do Ciclo 02)          | 11 §2.1                                    | 01 §4, 04 §§3, 4, 08, 09, 12   |
| Aderência à Agenda 2030, meta 17.18 e ressalva do ODS 18                   | 04 §4                                      | 01 §4, 08, 09, 11 §8.1, 12     |

## 4. Aplicações → PRDs

As oito aplicações desta etapa (doc 03 §2.1) correspondem aos PRDs do doc 08:

| Aplicação                             | PRD    |
| ------------------------------------- | ------ |
| App 01 — Aula presencial              | PRD-04 |
| App 03 — Gestão administrativa        | PRD-02 |
| App 04 — Jogo em JavaScript           | PRD-12 |
| App 05 — Área do Guerreiro(a)         | PRD-05 |
| App 06 — Vitrine pública              | PRD-03 |
| App 07 — Área dos pais e responsáveis | PRD-13 |
| App 08 — Área do Apoiador             | PRD-14 |
| App 09 — Área do Mestre               | PRD-09 |

PRDs sem aplicação dedicada: **PRD-01** (Backend API), **PRD-07** (ledger), **PRD-08**
(Comunidades Virtuais), **PRD-10** (batalhas) e **PRD-11** (personalização por IA). O
**PRD-06** foi extinto: o App 02 passou a ser parte do App 01 (PRD-04).

## 5. Matriz de rastreabilidade — conceito → PRDs

| Conceito                                    | Definição                 | PRDs                               |
| ------------------------------------------- | ------------------------- | ---------------------------------- |
| Trilha e missões                            | 02 §3 + 11 §2             | PRD-01, 09, 05                     |
| Conteúdo e bibliografia por missão          | 05 §3 + 11 §2             | PRD-09, 07                         |
| Atividades e taxonomia                      | 02 §4 + 11 §§2.1, 4       | PRD-09, 01, 02, 05                 |
| Acompanhamento por nick e favoritos         | 02 §1 + 03 §10            | PRD-14, 03, 01                     |
| Desafios de desbloqueio                     | 02 §2                     | PRD-01, 09, 05                     |
| Desafio de coleta (série temporal)          | 02 §1                     | PRD-01, 08, 05, 06                 |
| Desafios extras (abertos e direcionados)    | 04 §3                     | PRD-01, 02, 07, 09                 |
| Encontros presenciais (dinâmica assíncrona) | 05 §4                     | PRD-02, 04                         |
| Quiz ao Vivo                                | 05 §5                     | PRD-02, 04, 09                     |
| Batalhas e telemetria                       | 02 §6 + 07                | PRD-10, 01, 09, 02, 04             |
| Culminância e criação original              | 02 §4                     | PRD-01, 02, 03, 05, 09, 12, 10     |
| Motor de pontuação                          | 11 §5                     | PRD-01, 02, 05, 09                 |
| Níveis 1–5 / Mestre Aprendiz                | 11 §6                     | PRD-01, 05                         |
| Badges                                      | 11 §7                     | PRD-01, 03, 05, 12                 |
| Recompensa conquistada em marco             | 02 §8 + 11 §2.1           | PRD-09, 01, 05, 07                 |
| Vitrine e rankings                          | 03 §8 + 11 §8.1           | PRD-03                             |
| Granularidade da saída pública              | 02 §1 + 03 §12            | PRD-03, 08, 01                     |
| Cards e páginas individuais dos personagens | 11 §8.2                   | PRD-03, 12                         |
| Pré-cadastro e identidade do Apoiador       | 02 §1 + 03 §10 + 11 §8.2  | PRD-14, 03, 02, 01, 07             |
| Solicitação de Mestre ou Apoiador           | 02 §1 + 03 §8             | PRD-03, 02, 01                     |
| Equipes                                     | 02 §5 + 11 §4             | PRD-04, 01, 02, 05                 |
| Comunidade do onboarding vinda da aula      | 02 §1 + 03 §3             | PRD-04, 02, 01, 08                 |
| Moeda da plataforma                         | 04 §1                     | PRD-07, 03, 01                     |
| Entrega de dados sob solicitação aprovada   | 03 §12.3                  | PRD-03, 02, 01, 13                 |
| Produção executiva como aporte por absorção | 04 §1                     | PRD-07, 02                         |
| Representação visual da comunidade          | 11 §8.3                   | PRD-08, 03                         |
| Identidade visual das aplicações            | 15                        | PRD-02, 03, 04, 05, 09, 12, 13, 14 |
| Sistema de avatar do Guerreiro(a)           | 15 §7                     | PRD-04, 05, 03, 12                 |
| Acessibilidade digital (WCAG 2.2 AA)        | 15 §5                     | todos os PRDs de aplicação         |
| Contrato dos jogos                          | 11 §8.4                   | PRD-12, 01, 10, 03                 |
| Chave de aplicação e Área do Desenvolvedor  | 03 §§1, 8 + 14 §3         | PRD-03, 01, 02, 12                 |
| Distribuição da trilha no ciclo             | 11 §2.4 + 10 §5           | PRD-09, 02                         |
| Modelo de missão e template de autoria      | 11 §2.2 + 03 §11          | PRD-09, 05, 04, 01                 |
| Produção do Guerreiro(a) e devolutiva       | 11 §2.2 + 03 §§4, 7       | PRD-05, 04, 09, 01                 |
| Sugestões e propostas de evolução           | 03 §§7, 9, 10, 11 + 13 §5 | PRD-01, 02, 05, 09, 13, 14         |
| Apoio às atividades escolares               | 03 §7                     | PRD-05, 09, 01                     |
| Personalização por IA                       | 03 §7.1                   | PRD-11, 05, 04, 13, 09, 01         |
| Área do Apoiador                            | 03 §10 + 04 §3            | PRD-14, 07, 02                     |
| Missões, níveis de sustento e selos         | 14 §§5–8                  | PRD-14, 03, 07, 02, 01             |
| Portas de entrada por modalidade de apoio   | 14 §§3, 10 + 02 §1        | PRD-03, 14, 02, 01                 |
| Área do Mestre                              | 03 §11 + 02 §1            | PRD-09, 02, 01                     |
| Acervo didático (patrimônio e doação)       | 05 §3                     | PRD-07, 02, 05, 09                 |
| Área do responsável e consentimentos        | 03 §9                     | PRD-13, 01, 02                     |
| Etiqueta ODS e cobertura da Agenda 2030     | 11 §2.1 + 04 §4           | PRD-09, 01, 08, 03, 14             |

## 6. Invariantes — coerências que qualquer edição precisa preservar

Contradizer qualquer item abaixo é erro de documentação, não variação de redação:

1. **Oito aplicações**, todas **Web Apps responsivos, Mobile First**. Sem app nativo, sem
   aplicação sobre WhatsApp ou outra mensageria de terceiros. O antigo App 02 foi incorporado
   ao **App 01**, a aplicação da aula presencial, e o número 02 não é reaproveitado.
2. **Faixa etária 6 a 16 anos**; progressão por **nível de dificuldade, nunca por idade**.
3. **Só o Guerreiro(a) tem autocadastro.** Mestres e Apoiadores são cadastrados por Admin, com
   artefato comprobatório; responsáveis, por Admin ou Mestre, depois de se apresentarem
   pessoalmente; a solicitação pela vitrine é apenas pedido de avaliação, nunca cadastro;
   novos Admins entram manualmente por outro Admin. **Login não cria cadastro.**
4. **Comunidade Virtual é criada vazia por Admin**; todo Guerreiro(a) é vinculado a exatamente
   uma, pela **comunidade da aula agendada** em que se cadastra — e sem aula agendada o App 01
   não opera. **No Ciclo 01 não há troca de comunidade.**
5. **Toda trilha abre com missão de sondagem, tem ao menos um desafio de coleta de dados
   reais** e termina em **criação original** apresentada publicamente, com autoria creditada.
   As três são trava de publicação da trilha, não recomendação; a etiqueta ODS se junta a elas
   a partir do Ciclo 02, no nível da trilha (§20).
6. **A coleta pontua de forma recorrente enquanto a série estiver ativa**; interrompida,
   cessa o cômputo sem perder os pontos já creditados.
7. **Dados do território: guarda permanente com o coletor identificado**; anonimização
   apenas **na saída**. A **revogação do consentimento pelo responsável despersonaliza** o
   registro — rompe o vínculo de autoria e destrói o mapeamento —, **nunca o apaga**.
8. **O App 04 (jogo) é público, sem login de pessoa e somente leitura.** A **chave de acesso
   à API é da aplicação, não do visitante**: o App 04 carrega a sua e ninguém se identifica
   para jogar. Ele lê o progresso do
   Guerreiro(a) para montar o personagem — pontos regulares, pontos extras, poderes, badges e
   níveis — e **não escreve nada de volta**: não credita, não debita e não registra resultado
   de partida. Não existe endpoint de escrita para jogos. Dos pontos extras o jogo lê o
   **acumulado, nunca o saldo disponível**: trocar por recompensa avulsa **não enfraquece o
   personagem**. O personagem é escolhido **estritamente entre os Guerreiros e Guerreiras com
   divulgação autorizada**, como na vitrine.
9. **Nenhuma atividade acontece sem lastro** de recursos providos por Mestre ou Apoiador. Vale
   igualmente para a **recompensa avulsa** do catálogo e para a recompensa do **desafio
   extra**, providas antes de entrar no catálogo ou de o desafio publicar.
10. **Nenhum contato direto entre Apoiador e Guerreiro(a)**; toda interação adulto–criança é
    mediada pela plataforma.
11. **Nenhuma recusa de consentimento exclui o Guerreiro(a) da atividade** — sempre há
    alternativa equivalente.
12. **Guerreiros e Guerreiras aparecem publicamente só por avatar e nick.** A imagem do
    onboarding tem finalidade única de identificar o Guerreiro(a) — presença e autenticação — e
    nunca é exibida. **Toda superfície pública** — vitrine, cards, rankings públicos, portfólio
    e App 04 — mostra apenas quem tem **divulgação autorizada**. O **ranking interno da App 05
    é a única exceção declarada**: por ser tela logada, sem público externo, ele mostra a turma
    inteira.
13. **Ciclo 01 = ago–dez/2026, Guerreira Zeferina, trilhas 1 e 2 apenas.** Rima, Capoeira,
    Redes, PNED/BNCC e Soft Skills são ciclo futuro.
14. **Detalhamento extenso só no doc 08 e nos PRDs.** Os documentos 01–07 e 09–15 são
    sintéticos.
15. **Equipe é grupo livre de até 5 pessoas**, formada pelos próprios Guerreiros e Guerreiras
    no App 01, em dois tempos de vida: a **da aula**, válida para aquela aula presencial, e a
    **da trilha**, fixa depois de homologada pelo Mestre e sujeito da criação original. O
    Guerreiro(a) pode integrar várias e pontua em todas em que colabora — **uma só na partida
    de Quiz ao Vivo** —; no máximo **1 familiar com 17 anos ou mais**. Cada integrante **declara
    o seu papel na formação da equipe**, e ele vale para o encontro. A gestão não forma nem
    edita composição: o Mestre apenas **homologa a equipe da trilha, na App 03**.
16. **Aporte aparece publicamente em moedas da plataforma, nunca em reais.** Reais só aparecem
    na tela onde se paga, sempre ao lado do equivalente em moedas.
17. **Os dados produzidos pela plataforma são gratuitos.** A vitrine mostra a visão macro e
    agregada, que **para no bairro**; o conjunto na íntegra, sempre anonimizado e podendo
    descer a rua, condomínio, bloco e quadra, vai a pesquisadores e gestores públicos
    **mediante solicitação prévia e aprovação de um Admin**.
18. **Só a missão obrigatória conta no percurso do nível.** A opcional pontua e pode render
    badge, mas fica fora do denominador dos níveis 2, 3 e 4.
19. **Toda atividade exige produção do Guerreiro(a)** — escrever, falar ou construir. A
    leitura automática dessa produção é **hipótese, nunca resultado**: quem lança o resultado
    é o Mestre.
20. **A etiqueta ODS é descritiva**: não pontua, não é poder e **nunca é atributo de um
    Guerreiro(a)** — a cobertura sai agregada por comunidade e por ciclo. Ela é **da trilha**:
    **opcional no Ciclo 01** e **obrigatória a partir do Ciclo 02**, quando **ao menos um
    objetivo por trilha** passa a ser a **quarta trava de publicação**. Etiquetar a missão é
    **opcional em qualquer ciclo** e nunca trava. O **ODS 18** é citado como **adoção
    voluntária do Brasil**, jamais como objetivo oficial da ONU.
21. **O Apoiador não pontua.** A progressão de quem apoia corre em **moedas, selos e níveis
    de sustento**; ponto é do Guerreiro(a) e nasce de realização. **Nenhum aporte compra
    vantagem**: moeda alguma abre dado de criança, canal de contato, prioridade pedagógica ou
    aprovação mais rápida de desafio, e **não há ranking de apoiadores por dinheiro**. A
    **missão do Apoiador** não se confunde com a missão da trilha nem com o desafio extra, e
    **só se conclui com aporte homologado por Admin**.
22. **A personalização por IA adapta na sessão e não perfila a criança.** Nenhum traço de
    ritmo, dificuldade ou interesse é inferido ou guardado, e o contexto é **descartado ao
    encerrar a sessão**. A IA **recomenda e reescreve dentro do corpus fechado** do Mestre,
    marcando o texto gerado, e **nunca cria conteúdo novo**. O responsável a desliga a
    qualquer tempo, e desligá-la não tira conteúdo nem exclui ninguém da atividade. A chave
    dele vale na **App 05**, tela individual: **não alcança a tela coletiva do App 01**, onde a
    reescrita sempre opera e o contexto não carrega dado individual de ninguém.
23. **Ponto regular nunca se gasta; só o extra se troca.** O regular alimenta níveis e ranking
    e não é debitado em nenhuma hipótese. O extra tem **duas contas** — o **acumulado**, que só
    cresce e é o que as superfícies públicas leem, e o **saldo disponível**, que debita na
    troca e **nunca fica negativo**. A troca alcança **só a recompensa avulsa** do catálogo:
    **recompensa de marco jamais é comprada**. O preço em pontos **não deriva** do valor em
    moedas nem em reais.
24. **As oito aplicações têm uma identidade visual só**, com dois temperamentos — Operação e
    Arena — que mudam densidade, raio e presença de ilustração, **nunca a marca nem a paleta**,
    e que valem para a **aplicação inteira**, jamais por região de uma tela.
    O piso de acessibilidade é **WCAG 2.2 AA** em todas elas, e **a cor jamais carrega
    significado sozinha**: sempre acompanhada de glifo, forma, numeral ou rótulo. **Ponto
    regular, ponto extra e moeda nunca se confundem na tela** — cada um com glifo, ficha e
    rótulo próprios.

## 7. Como esta documentação deve ser editada

As regras de redação e revisão (concisão, não duplicar, onde detalhar, como marcar
proposta e pendência) estão em **`CLAUDE.md`**, na raiz do repositório. Toda alteração de
texto nesta pasta segue aquele documento — e toda alteração que mude a relação entre
documentos precisa atualizar **esta** página.

Restrições mecânicas impostas pela esteira de CI (markdownlint, Prettier, Lychee e MkDocs),
que valem para qualquer edição:

- Linha de até 95 caracteres fora de tabelas e blocos de código; blocos sempre com
  linguagem declarada (diagramas ASCII usam `text`); negrito não substitui título.
- `docs/index.md` é a home do site e o **único** documento que linka os demais.
- **Arquivo novo ou renomeado em `docs/` precisa entrar na `nav` do `mkdocs.yml`**, senão o
  build `--strict` falha. Vale igualmente para `docs/prds/`.
- `npm run fix` corrige automaticamente o que for corrigível de formatação.

## 8. PRDs — arquivos, dependências e governança

Os PRDs ficam em `docs/prds/`, um arquivo por PRD, nomeado `prd-XX-<assunto>.md`. A pasta tem
ainda `index.md` (situação de cada PRD) e `00-modelo-de-prd.md` (estrutura obrigatória).

O PRD é **derivado**: aplica as regras dos documentos 01–15 e nunca é fonte única de nenhuma
delas. Decisão nova tomada durante a escrita de um PRD é gravada primeiro no documento-fonte
do assunto (§1) e movida no documento 09 para "Já decididos"; só então o PRD a aplica. Regra
que existe apenas dentro de um PRD está no lugar errado.

| PRD    | Arquivo                           | Depende de     | Documentos-fonte       |
| ------ | --------------------------------- | -------------- | ---------------------- |
| PRD-01 | `prd-01-backend-api.md`           | PRD-07, PRD-08 | 02, 03, 04, 11         |
| PRD-02 | `prd-02-frontend-de-gestao.md`    | PRD-01         | 02, 03, 04, 05         |
| PRD-03 | `prd-03-vitrine-publica.md`       | PRD-01, PRD-13 | 02, 03, 04, 11         |
| PRD-04 | `prd-04-aula-presencial.md`       | PRD-01, PRD-02 | 02, 03, 05, 06, 11     |
| PRD-05 | `prd-05-area-do-guerreiro.md`     | PRD-01, PRD-09 | 02, 03, 05, 11         |
| PRD-07 | `prd-07-economia-e-ledger.md`     | PRD-08         | 04, 05                 |
| PRD-08 | `prd-08-comunidades-virtuais.md`  | —              | 02, 03, 11             |
| PRD-09 | `prd-09-area-do-mestre.md`        | PRD-01         | 02, 03, 05, 06, 07, 11 |
| PRD-10 | `prd-10-batalhas.md`              | PRD-01, PRD-09 | 02, 07, 11             |
| PRD-11 | `prd-11-personalizacao-por-ia.md` | PRD-01, PRD-04 | 02, 03, 11             |
| PRD-12 | `prd-12-jogo-em-javascript.md`    | PRD-01, PRD-03 | 02, 03, 04, 11         |
| PRD-13 | `prd-13-area-dos-responsaveis.md` | PRD-01, PRD-02 | 02, 03, 10             |
| PRD-14 | `prd-14-area-do-apoiador.md`      | PRD-07, PRD-02 | 02, 03, 04, 11, 12, 14 |

A correspondência entre as oito aplicações e os PRDs está na §4; a ordem de elaboração e o
motivo de cada onda estão no documento 08.

## 9. Implementação — artefatos do OpenSpec

O desenvolvimento é conduzido pelo framework de _Spec-Driven Development_ **OpenSpec**. Os
artefatos de cada _change_ — `proposal`, `specs`, `design` e `tasks` — ficam em
`openspec/changes/<change>/` e são **derivados dos PRDs**: aplicam requisitos identificados
(`RF-XX-nn`, `RN-XX-nn`) e nunca criam regra própria.

A ordem de autoridade é: documentos 01–15 e 99 → `docs/prds/` → artefatos do OpenSpec →
código. Conflito resolve-se sempre pelo nível superior. Decisão nova tomada durante a
implementação é gravada no documento-fonte (§1), movida no documento 09 e aplicada ao PRD
antes de virar código.

O contexto e as regras entregues aos agentes estão em `openspec/config.yaml`; o processo de
trabalho e a entrega estão no `CLAUDE.md`. A pasta `openspec/` fica fora do site MkDocs e
fora do lint de documentação.

A ordem em que o **código** entra é a tabela abaixo, uma entrega aprovada antes da seguinte.
Ela não é a ordem de elaboração do documento 08, que registra em que sequência os PRDs foram
**escritos**: a dependência que pôs PRD-08 e PRD-07 antes do PRD-01 na escrita já foi quitada
— o PRD-01 absorveu as entidades de ambos em `RF-01-23` e `RF-01-24` — e em execução a seta
se inverte, porque território e ledger só operam sobre a autenticação, a chave de aplicação e
o filtro por comunidade do núcleo.

| Nº  | PRD    | Entrega                        | Liberado a partir de |
| --- | ------ | ------------------------------ | -------------------- |
| 1   | PRD-01 | Backend API — núcleo           | —                    |
| 2   | PRD-08 | Território e séries temporais  | 1                    |
| 3   | PRD-07 | Economia e livro-razão         | 2                    |
| 4   | PRD-02 | App 03 — frontend de gestão    | 1                    |
| 5   | PRD-09 | App 09 — Área do Mestre        | 1                    |
| 6   | PRD-04 | App 01 — aula presencial       | 4                    |
| 7   | PRD-05 | App 05 — Área do Guerreiro(a)  | 5                    |
| 8   | PRD-13 | App 07 — Área dos responsáveis | 4                    |
| 9   | PRD-14 | App 08 — Área do Apoiador      | 4                    |
| 10  | PRD-03 | App 06 — vitrine pública       | 8                    |
| 11  | PRD-10 | Batalhas e eventos presenciais | 5                    |
| 12  | PRD-11 | Personalização por IA          | 6                    |
| 13  | PRD-12 | App 04 — jogo em JavaScript    | 10                   |

A coluna "liberado a partir de" traduz a dependência da §8 em número de ordem: é o piso, e
nenhum PRD entra antes dele. A posição exata acima desse piso é escolha da gestão. O PRD-01
é fatiado em changes menores; os demais são fatiados conforme o tamanho.
