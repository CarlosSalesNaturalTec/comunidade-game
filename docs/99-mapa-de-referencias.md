# 99 — Mapa de Referências (orientação para IA)

> **Esta página não é leitura para humanos.** Os demais documentos da pasta `/docs` foram
> deliberadamente limpos de referências cruzadas para ficarem legíveis por pessoas. Toda a
> relação entre documentos — fonte única de cada assunto, dependências e rastreabilidade
> para os PRDs — está consolidada aqui, para orientar agentes de IA que leiam, revisem ou
> derivem artefatos a partir desta documentação.

## 1. Regra de fonte única

Cada assunto tem **um** documento normativo. Alterar o assunto significa alterar esse
documento. Os demais, quando precisam citar o assunto, resumem em uma frase e **nunca
repetem a regra completa** — repetição é o defeito que esta documentação combate.

| Assunto                                                                                                                                                                                                   | Fonte única |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| Visão, valores, causas, objetivos, público-alvo, fundador, transparência sobre IA                                                                                                                         | 01          |
| Personas, solicitação de participação, Comunidades Virtuais (conceito e regras de coleta), poderes, trilhas, atividades e desafios, criações originais, equipes, batalhas, recompensas, manual do jogador | 02          |
| Princípios de arquitetura, canais, as 8 aplicações, LGPD da plataforma                                                                                                                                    | 03          |
| Economia de recursos, moeda da plataforma, livro-razão, pessoa jurídica, receitas, titularidade dos dados publicados, desafios extras (regras completas), impacto social                                  | 04          |
| Pontos de apoio, acervo didático (inventário, regime misto, guarda), roteiro do encontro, Quiz ao Vivo, formação de multiplicadores, replicabilidade, fases do piloto                                     | 05          |
| Trilha 1 — Robô Educa                                                                                                                                                                                     | 06          |
| Trilha 2 — Batalha de Laser                                                                                                                                                                               | 07          |
| Requisitos por PRD (**único documento com detalhamento extenso**)                                                                                                                                         | 08          |
| Decisões pendentes e propostas                                                                                                                                                                            | 09          |
| Case 01 — Guerreira Zeferina, Ciclo 01                                                                                                                                                                    | 10          |
| Motor do jogo: anatomia da trilha, taxonomia, pontuação, níveis, badges, reflexos no ecossistema                                                                                                          | 11          |
| Guia do Apoiador (documento **derivado**, sem regra própria)                                                                                                                                              | 12          |
| Código de Conduta do jogador                                                                                                                                                                              | 13          |

## 2. Papel e dependência dos documentos

| Doc   | Tipo                       | Depende de         | Alimenta       |
| ----- | -------------------------- | ------------------ | -------------- |
| index | Índice (home do site)      | —                  | —              |
| 01    | Normativo (fundação)       | —                  | 02, 03, 12, 13 |
| 02    | Normativo (conceito)       | 01                 | 03, 05, 08, 11 |
| 03    | Normativo (técnico)        | 02                 | 08             |
| 04    | Normativo (econômico)      | 02                 | 08, 12         |
| 05    | Normativo (operação)       | 02, 04             | 08, 10         |
| 06    | Normativo (conteúdo)       | 02                 | 03 §4, 08, 10  |
| 07    | Normativo (conteúdo)       | 02, 06             | 08, 10         |
| 08    | **Derivado** — requisitos  | 01–07, 11          | PRDs a gerar   |
| 09    | Pauta                      | todos              | 08             |
| 10    | Normativo (case)           | 02–08, 11          | 08, 09         |
| 11    | Normativo (motor)          | 02                 | 08             |
| 12    | **Derivado** — comunicação | 01, 02, 04, 05, 10 | —              |
| 13    | Normativo (conduta)        | 01, 02             | 05             |

**Divisão 02 × 11 (a confusão mais provável):** o doc 02 define **o que são** os elementos
do jogo; o doc 11 define **como eles se ligam e quanto valem**. Tabelas de pontuação,
níveis, badges e taxonomia existem **apenas no doc 11**.

## 3. Conceitos e onde vivem

| Conceito                                                           | Definido em                      | Citado (sem redefinir) em      |
| ------------------------------------------------------------------ | -------------------------------- | ------------------------------ |
| Ciclo de evolução positiva                                         | 01 §1                            | 12                             |
| Protagonismo dos jogadores / criação original                      | 01 §3 (valor) e 02 §4 (mecânica) | 03, 05, 06, 07, 08, 11, 12, 13 |
| Transparência sobre uso de IA                                      | 01 §7                            | 03, 08, 10, 12, 13             |
| Adesão em duas etapas (cadastro livre × divulgação autorizada)     | 03 §11                           | 01, 02, 08, 09, 10             |
| Comunidade Virtual (criação, vínculo, granularidade)               | 02 §1                            | 03, 05, 08, 10, 11             |
| Série temporal de coleta e pontuação recorrente                    | 02 §1                            | 03, 06, 07, 08, 11             |
| Guarda permanente com coletor identificado / anonimização na saída | 02 §1                            | 03 §11, 08, 09                 |
| Regra "toda trilha coleta dados reais"                             | 02 §3                            | 06, 07, 08, 10, 11             |
| Poder do Território                                                | 02 §2                            | 08, 11                         |
| Governança de personas (só Jogador tem autocadastro)               | 02 §1                            | 01, 05, 08                     |
| Solicitação de participação como Mestre ou Apoiador                | 02 §1                            | 03 §§5, 8, 08, 12              |
| Equipes (grupo livre até 5, várias por jogador, 1 familiar 17+)    | 02 §5                            | 03 §5, 08, 11 §4               |
| Comunidade default do onboarding                                   | 02 §1                            | 01, 03 §§3, 5, 08, 10          |
| Moeda da plataforma (1 moeda = R$ 100,00; vitrine em moedas)       | 04 §1                            | 03 §8, 08, 11 §8.2, 12         |
| Coproprietariedade dos dados publicados e monetização (50% / 50%)  | 04 §2                            | 03 §11, 08, 09                 |
| Aviso de LGPD visível nas aplicações e área detalhada              | 03 §11                           | 08, 09                         |
| Área do Apoiador (App 08) e registro de propostas                  | 03 §10                           | 04, 08, 09, 12                 |
| Regra de lastro (atividade só com recurso provido)                 | 04 §1                            | 02, 05, 10, 11, 12             |
| Poder Econômico                                                    | 04 §1                            | 02, 12                         |
| Desafios extras (aberto e direcionado)                             | 04 §3                            | 02, 08, 11, 12                 |
| Acervo Include e kits MDF (inventário, regime misto, guarda)       | 05 §3                            | 02, 04, 09, 10                 |
| Encontro assíncrono                                                | 05 §4                            | 03, 08, 11                     |
| Quiz ao Vivo                                                       | 05 §5                            | 03, 08, 11                     |
| Mestre Aprendiz (nível 5) e multiplicadores                        | 11 §6 (motor) e 05 §6 (operação) | 02, 08                         |
| Níveis, badges, tabela de pontos, taxonomia de atividades          | 11 §§4–7                         | 02, 08                         |
| Contrato dos jogos (lê progresso, debita, nunca credita)           | 11 §8.4                          | 03 §6, 08                      |
| LGPD, avatares, foto de presença, Modo Ouvinte                     | 03 §§3.3, 4, 11                  | 02, 08, 09, 13                 |

## 4. Aplicações → PRDs

As oito aplicações desta etapa (doc 03 §2.1) correspondem aos PRDs do doc 08:

| Aplicação                                  | PRD    |
| ------------------------------------------ | ------ |
| App 01 — Onboarding                        | PRD-04 |
| App 02 — Assistente por voz e Modo Ouvinte | PRD-06 |
| App 03 — Gestão administrativa             | PRD-02 |
| App 04 — Jogo em JavaScript                | PRD-12 |
| App 05 — Área do Jogador                   | PRD-05 |
| App 06 — Vitrine pública                   | PRD-03 |
| App 07 — Área dos pais e responsáveis      | PRD-13 |
| App 08 — Área do Apoiador                  | PRD-14 |

PRDs sem aplicação dedicada: **PRD-01** (Backend API), **PRD-07** (ledger), **PRD-08**
(Comunidades Virtuais), **PRD-09** (autoria de trilhas), **PRD-10** (batalhas), **PRD-11**
(personalização por IA).

## 5. Matriz de rastreabilidade — conceito → PRDs

| Conceito                                    | Definição             | PRDs                           |
| ------------------------------------------- | --------------------- | ------------------------------ |
| Trilha e pontos de trilha                   | 02 §3 + 11 §2         | PRD-01, 09, 05                 |
| Conteúdo e bibliografia por ponto           | 05 §3 + 11 §2         | PRD-09, 07                     |
| Atividades e taxonomia                      | 02 §4 + 11 §4         | PRD-01, 02, 05                 |
| Desafios de desbloqueio                     | 02 §2                 | PRD-01, 09, 05                 |
| Desafio de coleta (série temporal)          | 02 §1                 | PRD-01, 08, 05, 06             |
| Desafios extras (abertos e direcionados)    | 04 §3                 | PRD-01, 02, 07, 09             |
| Encontros presenciais (dinâmica assíncrona) | 05 §4                 | PRD-02, 04, 05                 |
| Quiz ao Vivo                                | 05 §5                 | PRD-02, 05, 09                 |
| Batalhas e telemetria                       | 02 §6 + 07            | PRD-10, 01                     |
| Culminância e criação original              | 02 §4                 | PRD-01, 02, 03, 05, 09, 12, 10 |
| Motor de pontuação                          | 11 §5                 | PRD-01, 02, 05                 |
| Níveis 1–5 / Mestre Aprendiz                | 11 §6                 | PRD-01, 05                     |
| Badges                                      | 11 §7                 | PRD-01, 03, 05, 12             |
| Recompensas e troca de pontos               | 02 §8                 | PRD-01, 05, 07                 |
| Vitrine e rankings                          | 03 §8 + 11 §8.1       | PRD-03                         |
| Cards e páginas individuais dos personagens | 11 §8.2               | PRD-03, 12                     |
| Solicitação de Mestre ou Apoiador           | 02 §1 + 03 §8         | PRD-03, 02, 01                 |
| Equipes                                     | 02 §5 + 11 §4         | PRD-01, 02, 05                 |
| Comunidade default do onboarding            | 02 §1 + 03 §3         | PRD-04, 02, 01, 08             |
| Moeda da plataforma                         | 04 §1                 | PRD-07, 03, 01                 |
| Coproprietariedade dos dados publicados     | 04 §2                 | PRD-01, 07, 13                 |
| Representação visual da comunidade          | 11 §8.3               | PRD-08, 03                     |
| Contrato dos jogos                          | 11 §8.4               | PRD-12, 01, 10                 |
| Distribuição da trilha no ciclo             | 11 §2.3 + 10 §5       | PRD-09, 02                     |
| Sugestões e propostas de evolução           | 03 §§7, 9, 10 + 13 §5 | PRD-01, 02, 05, 13, 14         |
| Área do Apoiador                            | 03 §10 + 04 §3        | PRD-14, 07, 02                 |
| Acervo didático (patrimônio e doação)       | 05 §3                 | PRD-07, 02, 05, 09             |
| Área do responsável e consentimentos        | 03 §9                 | PRD-13, 01, 02                 |

## 6. Invariantes — coerências que qualquer edição precisa preservar

Contradizer qualquer item abaixo é erro de documentação, não variação de redação:

1. **Oito aplicações**, todas **Web Apps responsivos, Mobile First**. Sem app nativo, sem
   aplicação sobre WhatsApp ou outra mensageria de terceiros.
2. **Faixa etária 6 a 16 anos**; progressão por **nível de dificuldade, nunca por idade**.
3. **Só o Jogador tem autocadastro.** Mestres e Apoiadores são cadastrados por Admin, com
   artefato comprobatório; a solicitação pela vitrine é apenas pedido de avaliação, nunca
   cadastro; novos Admins entram manualmente por outro Admin.
4. **Comunidade Virtual é criada vazia por Admin**; todo jogador é vinculado a exatamente
   uma, pela **comunidade default** que o Admin define — e sem ela o App 01 não opera.
5. **Toda trilha tem ao menos um desafio de coleta de dados reais** e termina em
   **criação original** apresentada publicamente, com autoria creditada.
6. **A coleta pontua de forma recorrente enquanto a série estiver ativa**; interrompida,
   cessa o cômputo sem perder os pontos já creditados.
7. **Dados do território: guarda permanente com o coletor identificado**; anonimização
   apenas **na saída**.
8. **O App 04 (jogo) consome pontos e nunca os gera.** Não existe endpoint de crédito para
   jogos.
9. **Nenhuma atividade acontece sem lastro** de recursos providos por Mestre ou Apoiador.
10. **Nenhum contato direto entre Apoiador e jogador**; toda interação adulto–criança é
    mediada pela plataforma.
11. **Nenhuma recusa de consentimento exclui o jogador da atividade** — sempre há
    alternativa equivalente.
12. **Jogadores aparecem publicamente só por avatar e nick.** A foto do onboarding tem
    finalidade única de presença.
13. **Ciclo 01 = ago–dez/2026, Guerreira Zeferina, trilhas 1 e 2 apenas.** Rima, Capoeira,
    Redes, PNED/BNCC e Soft Skills são ciclo futuro.
14. **Detalhamento extenso só no doc 08.** Os demais documentos são sintéticos.
15. **Equipe é grupo livre de até 5 pessoas**, cadastrada por Admin; o jogador pode integrar
    várias e pontua em todas em que colabora; no máximo **1 familiar com 17 anos ou mais**.
16. **Aporte aparece publicamente em moedas da plataforma, nunca em reais.**
17. **Dados publicados têm coproprietariedade** entre a entidade responsável e o jogador que
    os gerou; monetizados, remuneram ambos.

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
  build `--strict` falha.
- `npm run fix` corrige automaticamente o que for corrigível de formatação.
