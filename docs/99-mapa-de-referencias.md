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

| Assunto                                                                                                                                                                                                                      | Fonte única |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| Visão, valores, causas, objetivos, público-alvo, fundador, transparência sobre IA                                                                                                                                            | 01          |
| Personas, solicitação de participação, Comunidades Virtuais (conceito e regras de coleta), poderes, trilhas, atividades e desafios, criações originais, equipes, batalhas, recompensas, manual do Guerreiro(a)               | 02          |
| Princípios de arquitetura, canais, as 8 aplicações, licenças, LGPD da plataforma                                                                                                                                             | 03          |
| Economia de recursos, moeda da plataforma, livro-razão, pessoa jurídica, receitas, titularidade dos dados publicados, desafios extras (regras completas), impacto social, aderência à Agenda 2030 e indicadores de cobertura | 04          |
| Pontos de apoio, acervo didático (inventário, regime misto, guarda), roteiro do encontro, Quiz ao Vivo, formação de multiplicadores, replicabilidade, fases do piloto                                                        | 05          |
| Trilha 1 — Robô Educa                                                                                                                                                                                                        | 06          |
| Trilha 2 — Batalha de Laser                                                                                                                                                                                                  | 07          |
| Requisitos por PRD (**único documento extenso entre os 01–13**)                                                                                                                                                              | 08          |
| Requisitos de produto por aplicação (**derivados — nenhum PRD é fonte única**)                                                                                                                                               | `prds/`     |
| Decisões pendentes e propostas                                                                                                                                                                                               | 09          |
| Case 01 — Guerreira Zeferina, Ciclo 01                                                                                                                                                                                       | 10          |
| Motor do jogo: anatomia da trilha, taxonomia, pontuação, níveis, badges, reflexos no ecossistema, etiqueta ODS da trilha                                                                                                     | 11          |
| Guia do Apoiador (documento **derivado**, sem regra própria)                                                                                                                                                                 | 12          |
| Código de Conduta do Guerreiro(a)                                                                                                                                                                                            | 13          |

## 2. Papel e dependência dos documentos

| Doc   | Tipo                                 | Depende de         | Alimenta        |
| ----- | ------------------------------------ | ------------------ | --------------- |
| index | Índice (home do site)                | —                  | —               |
| 01    | Normativo (fundação)                 | —                  | 02, 03, 12, 13  |
| 02    | Normativo (conceito)                 | 01                 | 03, 05, 08, 11  |
| 03    | Normativo (técnico)                  | 02                 | 08              |
| 04    | Normativo (econômico)                | 02                 | 08, 12          |
| 05    | Normativo (operação)                 | 02, 04             | 08, 10          |
| 06    | Normativo (conteúdo)                 | 02                 | 03 §4, 08, 10   |
| 07    | Normativo (conteúdo)                 | 02, 06             | 08, 10          |
| 08    | **Derivado** — requisitos            | 01–07, 11          | PRDs a gerar    |
| 09    | Pauta                                | todos              | 08              |
| 10    | Normativo (case)                     | 02–08, 11          | 08, 09          |
| 11    | Normativo (motor)                    | 02                 | 08              |
| 12    | **Derivado** — comunicação           | 01, 02, 04, 05, 10 | —               |
| 13    | Normativo (conduta)                  | 01, 02             | 05              |
| prds/ | **Derivado** — requisitos de produto | 08, 01–07, 11, 13  | desenvolvimento |

**Divisão 02 × 11 (a confusão mais provável):** o doc 02 define **o que são** os elementos
do jogo; o doc 11 define **como eles se ligam e quanto valem**. Tabelas de pontuação,
níveis, badges e taxonomia existem **apenas no doc 11**.

## 3. Conceitos e onde vivem

| Conceito                                                           | Definido em                                | Citado (sem redefinir) em      |
| ------------------------------------------------------------------ | ------------------------------------------ | ------------------------------ |
| Ciclo de evolução positiva                                         | 01 §1                                      | 12                             |
| Protagonismo dos Guerreiros e Guerreiras / criação original        | 01 §3 (valor) e 02 §4 (mecânica)           | 03, 05, 06, 07, 08, 11, 12, 13 |
| Transparência sobre uso de IA                                      | 01 §7                                      | 03, 08, 10, 12, 13             |
| Adesão em duas etapas (cadastro livre × divulgação autorizada)     | 03 §12                                     | 01, 02, 08, 09, 10             |
| Autorização única do responsável (divulgação e captação)           | 03 §12                                     | 02 §§1, 9, 03 §9, 08, 09       |
| Comunidade Virtual (criação, vínculo, granularidade)               | 02 §1                                      | 03, 05, 08, 10, 11             |
| Série temporal de coleta e pontuação recorrente                    | 02 §1                                      | 03, 06, 07, 08, 11             |
| Guarda permanente com coletor identificado / anonimização na saída | 02 §1                                      | 03 §12, 08, 09                 |
| Base legal do dado de território (duas camadas) e revogação        | 03 §12.1                                   | 02 §1, 08, 09, 13              |
| Prazos de guarda e fim do vínculo                                  | 03 §12.2                                   | 02 §1, 03 §§3.3, 7, 08, 09     |
| Periodicidade das auditorias por amostragem                        | 03 §11 (corpus e trilhas) e 02 §1 (coleta) | 03 §5, 08, 09                  |
| Regra "toda trilha coleta dados reais"                             | 02 §3                                      | 06, 07, 08, 10, 11             |
| Poder do Território                                                | 02 §2                                      | 08, 11                         |
| Governança de personas (só Guerreiro(a) tem autocadastro)          | 02 §1                                      | 01, 05, 08                     |
| Cadastro do responsável e vínculo com os Guerreiros e Guerreiras   | 02 §1                                      | 03 §§1.1, 5, 9, 11, 08, 09     |
| Autenticação por persona (nick e imagem; Apps 04 e 06 sem login)   | 03 §1.1                                    | 02, 08, 09                     |
| Solicitação de participação como Mestre ou Apoiador                | 02 §1                                      | 03 §§5, 8, 08, 12              |
| Equipes (grupo livre até 5, formadas no App 01, válidas na aula)   | 02 §5                                      | 03 §§4, 5, 08, 11 §4           |
| Comunidade do onboarding vinda da aula agendada                    | 02 §1                                      | 01, 03 §§3, 5, 08, 10          |
| Guerreiro(a) como termo da persona primária                        | 02 §1                                      | 01, 03, 08, 09                 |
| Moeda da plataforma (1 moeda = R$ 100,00; vitrine em moedas)       | 04 §1                                      | 03 §8, 08, 11 §8.2, 12         |
| Entrega de dados (gratuita, íntegra e aprovada por Admin)          | 03 §12.3                                   | 04 §2, 08, 09                  |
| Produção executiva (tempo do fundador e dos Admins, por absorção)  | 04 §1                                      | 08, 09, 10 §4.3                |
| Recortes da vitrine (sociedade civil, pesquisadores, gestores)     | 03 §8                                      | 04 §4, 08, 09                  |
| Granularidade da saída pública (agrega até o bairro)               | 02 §1                                      | 03 §§8, 12, 08, 09             |
| Novidade dos favoritos (cinco fatos, 30 dias; só na App 08)        | 03 §10                                     | 02 §1, 03 §8, 08               |
| Proteção das rotas públicas (limite por origem, atraso)            | 03 §8                                      | 02 §1, 08                      |
| Aviso de LGPD visível nas aplicações e área detalhada              | 03 §12                                     | 08, 09                         |
| Área do Apoiador (App 08) e registro de propostas                  | 03 §10                                     | 04, 08, 09, 12                 |
| Pré-cadastro do Apoiador (aporte declarado e comprovante)          | 02 §1 e 03 §10                             | 04 §2, 08                      |
| Identidade pública do Apoiador (avatar, nick, moldura do card)     | 11 §8.2                                    | 02 §1, 03 §§8, 10, 08          |
| Área do Mestre (App 09) — autoria e operação                       | 03 §11                                     | 02, 05, 08, 09                 |
| Publicação da trilha (sem aprovação prévia, travas e conteúdo)     | 03 §11                                     | 02, 05, 08, 11                 |
| Atividade da missão (modalidade e formato)                         | 11 §§2.1, 4                                | 02, 03 §11, 08                 |
| Modelo de missão (produção, sondagem, retomada, obrigatoriedade)   | 11 §2.2                                    | 02 §§3, 4, 03 §§4, 7, 11       |
| Hipóteses do Ciclo 01 (H1 a H5) e como cada uma se verifica        | 10 §3                                      | 08, 09, `prds/`                |
| Leitura da produção do Guerreiro(a) e devolutiva construtiva       | 03 §§4, 7 e 11 §2.2                        | 02 §4, 09                      |
| Auxílio de IA na autoria da trilha (estrutura, não conteúdo)       | 03 §11                                     | 01 §7, 09                      |
| Recompensa conquistada em marco da trilha                          | 02 §8                                      | 03 §7, 08, 11 §2.1, 12         |
| Acompanhamento por nick e favoritos (só do Apoiador)               | 02 §1 e 03 §10                             | 03 §8, 04 §3, 08, 12           |
| Licença do conteúdo educacional (CC BY-SA)                         | 03 §1                                      | 01, 08, 09                     |
| Regra de lastro (atividade só com recurso provido)                 | 04 §1                                      | 02, 05, 10, 11, 12             |
| Poder Econômico                                                    | 04 §1                                      | 02, 12                         |
| Desafios extras (aberto e direcionado)                             | 04 §3                                      | 02, 08, 11, 12                 |
| Acervo Include e kits MDF (inventário, regime misto, guarda)       | 05 §3                                      | 02, 04, 09, 10                 |
| Encontro assíncrono                                                | 05 §4                                      | 03, 08, 11                     |
| Quiz ao Vivo                                                       | 05 §5                                      | 03, 08, 11                     |
| Mestre Aprendiz (nível 5) e multiplicadores                        | 11 §6 (motor) e 05 §6 (operação)           | 02, 08                         |
| Níveis, badges, tabela de pontos, taxonomia de atividades          | 11 §§4–7                                   | 02, 08                         |
| Nível como percurso da trilha (gates dos níveis 1 a 5)             | 11 §6                                      | 02 §7, 08                      |
| Integridade dos pontos (travas antifraude)                         | 11 §5.1                                    | 02 §1, 05 §5                   |
| Canal de sugestões do Guerreiro(a) (formato, prazo e crédito)      | 03 §7                                      | 11 §§5, 7, 13 §5               |
| Apoio escolar por assistente de voz, com corpus fechado e IA       | 03 §7                                      | 03 §§4, 5, 11, 08, 10 §4.3     |
| Reparação que zera a ocorrência de conduta                         | 13 §3                                      | 11 §5                          |
| Regras da partida do Quiz ao Vivo (aparelho, acerto e desempate)   | 05 §5                                      | 03 §§4, 5, 11, 08, 11 §5       |
| Contrato dos jogos (somente leitura: lê progresso e nada escreve)  | 11 §8.4                                    | 03 §6, 08                      |
| LGPD, avatares e imagem do Guerreiro(a)                            | 03 §§3.3, 12                               | 02, 08, 09, 13                 |
| Etiqueta ODS da trilha (descritiva, sem ponto; trava do Ciclo 02)  | 11 §2.1                                    | 01 §4, 04 §§3, 4, 08, 09, 12   |
| Aderência à Agenda 2030, meta 17.18 e ressalva do ODS 18           | 04 §4                                      | 01 §4, 08, 09, 11 §8.1, 12     |

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

| Conceito                                    | Definição                 | PRDs                           |
| ------------------------------------------- | ------------------------- | ------------------------------ |
| Trilha e missões                            | 02 §3 + 11 §2             | PRD-01, 09, 05                 |
| Conteúdo e bibliografia por missão          | 05 §3 + 11 §2             | PRD-09, 07                     |
| Atividades e taxonomia                      | 02 §4 + 11 §§2.1, 4       | PRD-09, 01, 02, 05             |
| Acompanhamento por nick e favoritos         | 02 §1 + 03 §10            | PRD-14, 03, 01                 |
| Desafios de desbloqueio                     | 02 §2                     | PRD-01, 09, 05                 |
| Desafio de coleta (série temporal)          | 02 §1                     | PRD-01, 08, 05, 06             |
| Desafios extras (abertos e direcionados)    | 04 §3                     | PRD-01, 02, 07, 09             |
| Encontros presenciais (dinâmica assíncrona) | 05 §4                     | PRD-02, 04                     |
| Quiz ao Vivo                                | 05 §5                     | PRD-02, 04, 09                 |
| Batalhas e telemetria                       | 02 §6 + 07                | PRD-10, 01                     |
| Culminância e criação original              | 02 §4                     | PRD-01, 02, 03, 05, 09, 12, 10 |
| Motor de pontuação                          | 11 §5                     | PRD-01, 02, 05, 09             |
| Níveis 1–5 / Mestre Aprendiz                | 11 §6                     | PRD-01, 05                     |
| Badges                                      | 11 §7                     | PRD-01, 03, 05, 12             |
| Recompensa conquistada em marco             | 02 §8 + 11 §2.1           | PRD-09, 01, 05, 07             |
| Vitrine e rankings                          | 03 §8 + 11 §8.1           | PRD-03                         |
| Granularidade da saída pública              | 02 §1 + 03 §12            | PRD-03, 08, 01                 |
| Cards e páginas individuais dos personagens | 11 §8.2                   | PRD-03, 12                     |
| Pré-cadastro e identidade do Apoiador       | 02 §1 + 03 §10 + 11 §8.2  | PRD-14, 03, 02, 01, 07         |
| Solicitação de Mestre ou Apoiador           | 02 §1 + 03 §8             | PRD-03, 02, 01                 |
| Equipes                                     | 02 §5 + 11 §4             | PRD-04, 01, 02, 05             |
| Comunidade do onboarding vinda da aula      | 02 §1 + 03 §3             | PRD-04, 02, 01, 08             |
| Moeda da plataforma                         | 04 §1                     | PRD-07, 03, 01                 |
| Entrega de dados sob solicitação aprovada   | 03 §12.3                  | PRD-03, 02, 01, 13             |
| Produção executiva como aporte por absorção | 04 §1                     | PRD-07, 02                     |
| Representação visual da comunidade          | 11 §8.3                   | PRD-08, 03                     |
| Contrato dos jogos                          | 11 §8.4                   | PRD-12, 01, 10                 |
| Distribuição da trilha no ciclo             | 11 §2.4 + 10 §5           | PRD-09, 02                     |
| Modelo de missão e template de autoria      | 11 §2.2 + 03 §11          | PRD-09, 05, 04, 01             |
| Produção do Guerreiro(a) e devolutiva       | 11 §2.2 + 03 §§4, 7       | PRD-05, 04, 09, 01             |
| Sugestões e propostas de evolução           | 03 §§7, 9, 10, 11 + 13 §5 | PRD-01, 02, 05, 09, 13, 14     |
| Apoio às atividades escolares               | 03 §7                     | PRD-05, 09, 01                 |
| Área do Apoiador                            | 03 §10 + 04 §3            | PRD-14, 07, 02                 |
| Área do Mestre                              | 03 §11 + 02 §1            | PRD-09, 02, 01                 |
| Acervo didático (patrimônio e doação)       | 05 §3                     | PRD-07, 02, 05, 09             |
| Área do responsável e consentimentos        | 03 §9                     | PRD-13, 01, 02                 |
| Etiqueta ODS e cobertura da Agenda 2030     | 11 §2.1 + 04 §4           | PRD-09, 01, 08, 03, 14         |

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
8. **O App 04 (jogo) é público, sem login e somente leitura.** Ele lê o progresso do
   Guerreiro(a) para montar o personagem — pontos regulares, pontos extras, poderes, badges e
   níveis — e **não escreve nada de volta**: não credita, não debita e não registra resultado
   de partida. Não existe endpoint de escrita para jogos, e **não há saldo de pontos
   consumidos**. O personagem é escolhido **estritamente entre os Guerreiros e Guerreiras com
   divulgação autorizada**, como na vitrine.
9. **Nenhuma atividade acontece sem lastro** de recursos providos por Mestre ou Apoiador.
10. **Nenhum contato direto entre Apoiador e Guerreiro(a)**; toda interação adulto–criança é
    mediada pela plataforma.
11. **Nenhuma recusa de consentimento exclui o Guerreiro(a) da atividade** — sempre há
    alternativa equivalente.
12. **Guerreiros e Guerreiras aparecem publicamente só por avatar e nick.** A imagem do
    onboarding tem finalidade única de identificar o Guerreiro(a) — presença e autenticação — e
    nunca é exibida.
13. **Ciclo 01 = ago–dez/2026, Guerreira Zeferina, trilhas 1 e 2 apenas.** Rima, Capoeira,
    Redes, PNED/BNCC e Soft Skills são ciclo futuro.
14. **Detalhamento extenso só no doc 08 e nos PRDs.** Os documentos 01–07 e 09–13 são
    sintéticos.
15. **Equipe é grupo livre de até 5 pessoas**, formada pelos próprios Guerreiros e Guerreiras
    no App 01 e válida para **aquela aula presencial**; o Guerreiro(a) pode integrar várias e
    pontua em todas em que colabora — **uma só na partida de Quiz ao Vivo** —; no máximo
    **1 familiar com 17 anos ou mais**. A gestão não forma nem edita equipe.
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

O PRD é **derivado**: aplica as regras dos documentos 01–13 e nunca é fonte única de nenhuma
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
| PRD-11 | `prd-11-personalizacao-por-ia.md` | PRD-01, PRD-04 | 02, 03                 |
| PRD-12 | `prd-12-jogo-em-javascript.md`    | PRD-01, PRD-05 | 03, 11                 |
| PRD-13 | `prd-13-area-dos-responsaveis.md` | PRD-01, PRD-02 | 02, 03, 10             |
| PRD-14 | `prd-14-area-do-apoiador.md`      | PRD-07, PRD-02 | 03, 04, 12             |

A correspondência entre as oito aplicações e os PRDs está na §4; a ordem de elaboração e o
motivo de cada onda estão no documento 08.
