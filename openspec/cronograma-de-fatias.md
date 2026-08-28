# Cronograma de fatias

Plano de execução dos PRDs em fatias. É **nível 3** da hierarquia de autoridade do
`CLAUDE.md`: deriva dos PRDs e não cria requisito, número, prazo nem provedor. Quando o
cronograma discordar de um PRD, o PRD vence e a linha aqui se corrige.

Existe para que a próxima fatia não precise ser redescoberta a cada vez. Com ele, `/opsx:propose`
recebe a fatia pelo número — `/opsx:propose fatia 1 do PRD-13` — e o recorte já está escrito;
`/opsx:explore` deixa de ser passo obrigatório e volta a ser o que o nome diz: pensar antes de
abrir uma change quando algo não está claro.

## Como ler

Uma tabela por PRD, na ordem de construção do documento 99 §9. Colunas:

- **Fatia** — o número que o fundador usa para se referir a ela. Linha sem número não fecha um
  recorte formal do PRD: é pré-requisito técnico ou requisito não funcional que a esteira exigiu.
- **Entrega** — o que a fatia põe de pé, em uma linha.
- **Recorte** — na fatia **em aberto**, os identificadores previstos e a trava, quando houver;
  na **implementada**, o slug da change, onde o recorte real está escrito
  (`openspec/changes/archive/<slug>/`).
- **Situação** — `em aberto`, `em andamento` ou `implementado`.

O recorte de uma fatia em aberto é **previsão**, não contrato: quem escreve a `proposal` confere
contra o PRD e ajusta a linha se divergir. Trava anotada aqui não se resolve dentro de um
artefato do OpenSpec — vai ao fundador.

## Como manter

| Momento                     | O que fazer aqui                                                        |
| --------------------------- | ----------------------------------------------------------------------- |
| Ao abrir a change           | situação da fatia vira `em andamento`                                   |
| Ao arquivar a change        | situação vira `implementado` e a coluna Recorte recebe o slug da change |
| Fatia que mudou de recorte  | corrija a linha; não acrescente parágrafo                               |
| Fatia nova, não prevista    | acrescente a linha no PRD dela, com o recorte                           |
| PRD que entra na fila       | troque a linha "a fatiar" pelas fatias, uma linha cada                  |

Este arquivo é o registro das fatias — as entregues e as que faltam. `docs/prds/index.md`
guarda a **situação de cada PRD**, não as fatias, e não se repete aqui.

## Ordem de construção

A do documento 99 §9, com o piso de dependência de cada PRD. Os quatro PRDs em execução
(PRD-02, PRD-09, PRD-04 e PRD-05) têm o esqueleto de pé e resíduos abertos; PRD-13 é o próximo
da fila que ainda não começou.

---

## PRD-01 — Backend API (núcleo) — implementado

| Fatia | Entrega                                      | Recorte                                              | Situação     |
| ----- | -------------------------------------------- | ---------------------------------------------------- | ------------ |
| —     | Fundação da API e chave de aplicação         | `2026-08-11-fundacao-da-api-e-chave-de-aplicacao`    | implementado |
| —     | Apoio escolar e etiqueta ODS                 | `2026-08-12-apoio-escolar-e-etiqueta-ods`            | implementado |
| —     | Aula, presença e equipe                      | `2026-08-12-aula-presenca-e-equipe`                  | implementado |
| —     | Criação original, nível 5 e badge de autoria | `2026-08-12-criacao-original-nivel-5-e-badge-de-autoria` | implementado |
| —     | Persona, sessão do adulto e permissões       | `2026-08-12-persona-sessao-do-adulto-e-permissoes`   | implementado |
| —     | Poder, trilha, missão e atividade            | `2026-08-12-poder-trilha-missao-e-atividade`         | implementado |
| —     | Pontos, níveis, badges e ponto extra         | `2026-08-12-pontos-niveis-badges-e-ponto-extra`      | implementado |
| —     | Responsável, vínculo e consentimento         | `2026-08-12-responsavel-vinculo-e-consentimento`     | implementado |
| —     | Sessão do Guerreiro(a) e biometria           | `2026-08-12-sessao-do-guerreiro-e-biometria`         | implementado |
| —     | Ciclo de vida da chave de terceiro           | `2026-08-13-ciclo-de-vida-da-chave-de-terceiro`      | implementado |
| —     | Fila única de avaliação                      | `2026-08-13-fila-unica-de-avaliacao`                 | implementado |
| —     | Proteção das rotas públicas                  | `2026-08-13-protecao-das-rotas-publicas`             | implementado |
| —     | Quiz ao Vivo                                 | `2026-08-13-quiz-ao-vivo`                            | implementado |
| —     | Trilha de auditoria                          | `2026-08-13-trilha-de-auditoria`                     | implementado |
| —     | Credencial de dispositivo do sensor          | `2026-08-14-credencial-de-dispositivo-do-sensor`     | implementado |
| —     | Leitura pública da vitrine e dos jogos       | `2026-08-14-leitura-publica-vitrine-e-jogos`         | implementado |
| —     | Consulta paginada das séries                 | `2026-08-15-consulta-paginada-das-series`            | implementado |
| —     | Auditoria e estorno da coleta                | `2026-08-17-auditoria-e-estorno-da-coleta`           | implementado |
| —     | Nick de adulto                               | `2026-08-21-nick-de-adulto`                          | implementado |

## PRD-08 — Comunidades Virtuais e território — implementado

| Fatia | Entrega                                    | Recorte                                              | Situação     |
| ----- | ------------------------------------------ | ---------------------------------------------------- | ------------ |
| —     | Comunidade Virtual e locais                | `2026-08-14-comunidade-virtual-e-locais`             | implementado |
| —     | Série, registro e pontuação da coleta      | `2026-08-14-serie-registro-e-pontuacao-da-coleta`    | implementado |
| —     | Solicitação de local                       | `2026-08-14-solicitacao-de-local`                    | implementado |
| —     | Tipo e desafio de coleta                   | `2026-08-14-tipo-e-desafio-de-coleta`                | implementado |
| —     | Ciclo de vida da série                     | `2026-08-15-ciclo-de-vida-da-serie`                  | implementado |
| —     | Exportação do território e ODS das séries  | `2026-08-15-exportacao-do-territorio-e-ods-das-series` | implementado |
| —     | Leitura pública do território              | `2026-08-15-leitura-publica-do-territorio`           | implementado |
| —     | Lista pública de comunidades               | `2026-08-17-lista-publica-de-comunidades`            | implementado |

## PRD-07 — Economia de recursos e ledger — implementado

| Fatia | Entrega                                      | Recorte                                              | Situação     |
| ----- | -------------------------------------------- | ---------------------------------------------------- | ------------ |
| 1     | Ponto de apoio e tabela de referência        | `2026-08-18-ponto-de-apoio-e-tabela-de-referencia`   | implementado |
| 2     | Aporte, lançamento e saldo                   | `2026-08-18-aporte-lancamento-e-saldo`               | implementado |
| 3     | Reserva e ciclo de vida da aula              | `2026-08-18-reserva-e-ciclo-de-vida-da-aula`         | implementado |
| 4     | Necessidade publicada                        | `2026-08-18-necessidade-publicada`                   | implementado |
| 5     | Poder sustentador e prestação de contas      | `2026-08-18-poder-sustentador-e-prestacao-de-contas` | implementado |
| 6     | Ressarcimento do aporte absorvido            | `2026-08-18-ressarcimento-do-aporte-absorvido`       | implementado |
| 7     | Tabela de pontos extras e catálogo avulso    | `2026-08-18-tabela-de-pontos-extras-e-catalogo-avulso` | implementado |
| 8     | Troca de recompensa avulsa                   | `2026-08-19-troca-de-recompensa-avulsa`              | implementado |
| 9     | Tombamento e ficha de vida                   | `2026-08-19-tombamento-e-ficha-de-vida`              | implementado |
| 10    | Recompensa de marco e entrega                | `2026-08-19-recompensa-de-marco-e-entrega`           | implementado |
| —     | Desativação do ponto de apoio                | `2026-08-21-desativacao-do-ponto-de-apoio`           | implementado |

Fora do escopo entregue: **conferência de inventário** (`RF-07-20`) voltou ao documento 09 como
pendência; **desafio extra** espera a entidade `DesafioExtra`; **empréstimo de bancada** e
**reposição solidária** saíram do escopo.

---

## PRD-02 — Frontend de gestão (App 03)

| Fatia | Entrega                                            | Recorte                                                                                           | Situação     |
| ----- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------ |
| 1     | Esqueleto da gestão e cadastro de comunidade       | `2026-08-19-esqueleto-da-gestao-e-cadastro-de-comunidade`                                          | implementado |
| —     | Fontes próprias e camada visual comum              | `2026-08-20-fontes-proprias-e-camada-visual-comum`                                                 | implementado |
| —     | Implantação da App 03 e do núcleo                  | `2026-08-20-implantacao-da-app-03-e-do-nucleo`                                                     | implementado |
| 2     | Cadastro de personas                               | `2026-08-21-cadastro-de-personas`                                                                  | implementado |
| —     | Agenda da aula e ponto de apoio                    | `2026-08-21-agenda-da-aula-e-ponto-de-apoio`                                                       | implementado |
| —     | Guardas da conferência e da implantação            | `2026-08-21-guardas-da-conferencia-e-da-implantacao`                                               | implementado |
| 3     | Avaliação da participação e do pré-cadastro        | `2026-08-22-avaliacao-da-participacao-e-do-pre-cadastro`                                           | implementado |
| 4     | Avaliação de dados de chave e de sugestão          | `2026-08-22-avaliacao-de-dados-de-chave-e-de-sugestao`                                             | implementado |
| 5     | Catálogo de poderes e tela da gestão               | `2026-08-22-catalogo-de-poderes-e-tela-da-gestao`                                                  | implementado |
| 6     | Condução da partida de quiz                        | `2026-08-25-conducao-da-partida-de-quiz`                                                           | implementado |
| 7     | Painel do dia e anexo do termo                     | `2026-08-25-painel-do-dia-e-anexo-do-termo`                                                        | implementado |
| 8     | Esqueleto da Área do Guerreiro(a) e fim de ciclo   | `2026-08-26-esqueleto-da-area-do-guerreiro-e-fim-de-ciclo` (também fatia 1 do PRD-05)              | implementado |
| 9     | Território na gestão                               | `2026-08-27-territorio-na-gestao`                                                                  | implementado |
| 10    | Lançamentos, conduta e ajuste                      | `2026-08-27-lancamentos-conduta-e-ajuste`                                                                                                                                        | implementado |
| 11    | Aporte, necessidade e atividade avulsa na gestão   | `aporte-necessidade-e-atividade-avulsa-na-gestao` — `RF-02-29`, `RF-02-31`, `RF-02-32`, `RF-02-57`, `RF-02-58`, `RF-02-67` | implementado |
| 12    | Acervo e patrimônio na gestão                      | `RF-02-52`, `RF-02-53`, `RF-02-55`, `RF-02-96`, `RN-02-18`                                         | em aberto    |
| 13    | Auditoria da trilha, trilha de auditoria e aviso   | `RF-02-63`, `RF-02-64`, `RF-02-70`, `RN-02-23`, `RN-02-24`                                         | em aberto    |
| 14    | Fila de solicitações do responsável                | `RF-02-23`, `RF-02-24`, `RF-02-66` — entra junto da fatia 4 do PRD-13, que origina a solicitação   | em aberto    |
| 15    | Desafio extra na gestão                            | `RF-02-27`, `RF-02-28`, `RN-02-10`, `RN-02-11` — **trava:** entidade `DesafioExtra` (PRD-14 §8)    | em aberto    |
| 16    | Vitrine institucional e Apoiador na gestão         | `RF-02-80`, `RF-02-85` — depende do PRD-14 (cadastro de Apoiador) e do PRD-03 (vitrine)            | em aberto    |
| 17    | Auditoria do corpus de apoio escolar               | `RF-02-74` a `RF-02-76` — **a confirmar:** o cadastro do corpus foi ao Ciclo 02 (PRD-09 §3.2); a auditoria dele segue junto? | em aberto    |

Fora do cronograma: `RF-02-54` foi retirado e o identificador não se reaproveita; `RF-02-94`
passou ao PRD-04 como `RF-04-62`; `RF-02-56` (conferência de inventário) está travado pela
mesma pendência do `RF-07-20`, no documento 09.

## PRD-09 — Área do Mestre (App 09)

| Fatia | Entrega                                          | Recorte                                                                                                    | Situação     |
| ----- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- | ------------ |
| 1     | Esqueleto da Área do Mestre e autoria da trilha  | `2026-08-22-esqueleto-da-area-do-mestre-e-autoria-da-trilha`                                                | implementado |
| 2     | Culminância e publicação da trilha               | `2026-08-22-culminancia-e-publicacao-da-trilha`                                                             | implementado |
| 3     | Etiqueta ODS da trilha e da missão               | `2026-08-23-etiqueta-ods-da-trilha-e-da-missao`                                                             | implementado |
| 4     | Minhas turmas e lançamentos do Mestre            | `2026-08-23-minhas-turmas-e-lancamentos-do-mestre`                                                          | implementado |
| 5     | Banco do Quiz ao Vivo                            | `2026-08-23-banco-do-quiz-ao-vivo`                                                                          | implementado |
| 6     | Conteúdo e bibliografia da missão                | `2026-08-25-conteudo-e-bibliografia-da-missao`                                                              | implementado |
| 7     | Desafio de coleta e auditoria por amostragem     | `RF-09-27`, `RF-09-28`, `RF-09-35`, `RN-09-21`                                                              | em aberto    |
| 8     | Solicitação de local e proposta na fila única    | `RF-09-53` a `RF-09-55`                                                                                     | em aberto    |
| 9     | Necessidade, absorção e ressarcimento do Mestre  | `RF-09-56` a `RF-09-60`, `RN-09-12`, `RN-09-13`, `RN-09-23`                                                 | em aberto    |
| 10    | Responsável e credencial provisória pelo Mestre  | `RF-09-62` a `RF-09-65`, `RN-09-15`                                                                         | em aberto    |
| 11    | Perfil do Mestre, prova de habilidade e aviso    | `RF-09-66` a `RF-09-68`, `RN-09-14`                                                                         | em aberto    |
| 12    | Template da missão por IA                        | `RF-09-85` a `RF-09-91`, `RF-09-95`, `RN-09-33`, `RN-09-34`                                                 | em aberto    |
| 13    | Recompensa por desbloqueio e duplicação de trilha | `RF-09-13`, `RF-09-84`, `RF-09-75`                                                                         | em aberto    |
| 14    | Trilha de auditoria das escritas do Mestre       | `RF-09-48`                                                                                                  | em aberto    |
| 15    | Desafio extra na Área do Mestre                  | `RF-09-51`, `RF-09-52`, `RN-09-11`, `RN-09-40` a `RN-09-42` — **trava:** entidade `DesafioExtra` (PRD-14 §8) | em aberto    |

Ciclo 02, fora do Ciclo 01: `RF-09-61` (empréstimo do acervo permanente), `RF-09-96` e
`RF-09-97` (recusa de trilha sem etiqueta ODS), `RN-09-35` e o **apoio escolar** — `RF-09-77` a
`RF-09-79` —, que acompanha o assistente da App 05 (decisão do fundador, 2026-08-27,
documento 09 §1).

## PRD-04 — Aula presencial (App 01)

| Fatia | Entrega                                              | Recorte                                                                        | Situação     |
| ----- | ---------------------------------------------------- | -------------------------------------------------------------------------------- | ------------ |
| 1     | Esqueleto da aula presencial e equipe da aula        | `2026-08-24-esqueleto-da-aula-presencial-e-equipe-da-aula`                       | implementado |
| 2     | Cadastro do Guerreiro(a) no encontro                 | `2026-08-24-cadastro-do-guerreiro-no-encontro`                                   | implementado |
| 3     | Responsável, consentimento e captura da imagem       | `2026-08-24-responsavel-consentimento-e-captura-da-imagem`                       | implementado |
| 4     | Entrada por reconhecimento e falha de identificação  | `2026-08-24-entrada-por-reconhecimento-e-falha-de-identificacao`                 | implementado |
| 5     | Troca por recompensa avulsa no encontro              | `2026-08-25-troca-por-recompensa-avulsa-no-encontro`                             | implementado |
| 6     | Aparelho da equipe no quiz                           | `2026-08-25-aparelho-da-equipe-no-quiz`                                          | implementado |
| 7     | Programação do encontro e missão da equipe           | `2026-08-25-programacao-do-encontro-e-missao-da-equipe`                          | implementado |
| 8     | Equipe da trilha formada e homologada no encontro    | `RF-04-61`, `RF-04-62`, `RN-04-17`, `RN-04-22`                                   | em aberto    |
| 9     | Entrega da produção da missão e devolutiva           | `RF-04-45` a `RF-04-47`, `RN-04-31`                                              | em aberto    |
| 10    | Assistente de trilhas no encontro                    | `RF-04-36` a `RF-04-40`, `RN-04-19` a `RN-04-21` — o corpus é o conteúdo da missão (documento 03 §4.2), entregue na fatia 6 do PRD-09; não é o apoio escolar | em aberto    |
| 11    | Fila local sem rede                                  | `RF-04-23` a `RF-04-25`, `RN-04-13`                                              | em aberto    |
| 12    | Aviso de coleta e encerramento do cadastro           | `RF-04-26`, `RF-04-27`                                                           | em aberto    |

`RN-04-26` (recompensa de marco não se troca) é regra da fatia 5, já entregue; confira na fatia
que a tocar em vez de abrir recorte próprio.

## PRD-05 — Área do Guerreiro(a) (App 05)

| Fatia | Entrega                                             | Recorte                                                                                    | Situação     |
| ----- | --------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------ |
| 1     | Esqueleto da Área do Guerreiro(a) e fim de ciclo    | `2026-08-26-esqueleto-da-area-do-guerreiro-e-fim-de-ciclo` (também fatia 8 do PRD-02)         | implementado |
| 2     | Coleta do território na Área do Guerreiro(a)        | `2026-08-26-coleta-do-territorio-na-area-do-guerreiro`                                        | implementado |
| 3     | Carteira, catálogo, conquistas e ranking            | `2026-08-26-carteira-catalogo-conquistas-e-ranking`                                           | implementado |
| 4     | Inscrição na trilha, guia e desbloqueio             | `2026-08-27-inscricao-na-trilha-guia-e-desbloqueio` (também `RF-09-26`)                       | implementado |
| 5     | Criação original e portfólio                        | `2026-08-27-criacao-original-e-portfolio` (também `RF-09-31` a `RF-09-34`)                    | implementado |
| 6     | Desafios vigentes e equipes de que participa        | `RF-05-19`, `RF-05-22` a `RF-05-24`, `RN-05-15`, `RN-05-22`, `RN-05-23`                       | em aberto    |
| 7     | Produção da missão, devolutiva e retomada           | `RF-05-74` a `RF-05-80`, `RN-05-05`, `RN-05-35` a `RN-05-38`                                  | em aberto    |
| 8     | Desafio extra na Área do Guerreiro(a)               | `RF-05-20`, `RF-05-21` — **trava:** entidade `DesafioExtra` (PRD-14 §8)                       | em aberto    |

Ciclo 02, fora do Ciclo 01 (PRD-05 §3.2): **acervo do Guerreiro(a)** (`RF-05-47` a `RF-05-49`,
`RN-05-19`), **canal de sugestões** (`RF-05-54` a `RF-05-56`, `RN-05-17`) e **apoio escolar por
assistente de voz** (`RF-05-58` a `RF-05-70`, `RN-05-25` a `RN-05-31`). `RF-05-25` a `RF-05-29`
passaram ao PRD-04.

## PRD-13 — Área dos pais e responsáveis (App 07) — próximo da fila

| Fatia | Entrega                                       | Recorte                                                                                                | Situação  |
| ----- | --------------------------------------------- | -------------------------------------------------------------------------------------------------------- | --------- |
| 1     | Esqueleto da App 07, acesso e vínculo         | `RF-13-01` a `RF-13-06`, `RN-13-01` a `RN-13-04` — a credencial provisória vem da fatia 10 do PRD-09       | em aberto |
| 2     | Evolução do Guerreiro(a)                      | `RF-13-07` a `RF-13-12`, `RN-13-20`, `RN-13-21`                                                            | em aberto |
| 3     | Autorização única                             | `RF-13-13` a `RF-13-21`, `RN-13-05` a `RN-13-11`                                                           | em aberto |
| 4     | Solicitações e direitos                       | `RF-13-22` a `RF-13-28`, `RF-13-43`, `RF-13-44`, `RN-13-12` a `RN-13-14`, `RN-13-22` — par da fatia 14 do PRD-02 | em aberto |
| 5     | Transparência, termos e histórico de acessos  | `RF-13-29` a `RF-13-34`, `RN-13-19` — **trava:** falta o texto do termo quanto à entrega de dados (PRD-13 §14) | em aberto |
| 6     | Atendimento assistido, propostas e avisos     | `RF-13-35` a `RF-13-42`, `RN-13-15` a `RN-13-18`                                                           | em aberto |

## PRDs ainda não fatiados

Cada um recebe as suas fatias quando entrar na fila, em uma sessão de fatiamento própria — não
a cada change.

| Ordem (doc 99 §9) | PRD    | Entrega                        | Situação  |
| ----------------- | ------ | ------------------------------ | --------- |
| 9                 | PRD-14 | App 08 — Área do Apoiador      | a fatiar  |
| 10                | PRD-03 | App 06 — vitrine pública       | a fatiar  |
| 11                | PRD-10 | Batalhas e eventos presenciais | a fatiar  |
| 12                | PRD-11 | Personalização por IA          | a fatiar  |
| 13                | PRD-12 | App 04 — jogo em JavaScript    | a fatiar  |

O PRD-14 é o primeiro a fatiar: a entidade `DesafioExtra` que ele define (§8) destrava a fatia
15 do PRD-02, a 15 do PRD-09 e a 8 do PRD-05.

## Infraestrutura transversal (sem PRD)

| Fatia | Entrega                            | Recorte                                        | Situação     |
| ----- | ---------------------------------- | ---------------------------------------------- | ------------ |
| —     | Isolamento transacional dos testes | `2026-08-18-isolamento-transacional-dos-testes` | implementado |
