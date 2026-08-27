# PRDs — Documentos de Requisitos de Produto

Esta pasta reúne os **PRDs** (_Product Requirements Documents_) do Comunidade Game, derivados
do documento 08 e escritos um a um, na ordem das ondas abaixo. Cada PRD segue o
[modelo de PRD](00-modelo-de-prd.md) e vale para o **Ciclo 01** (Guerreira Zeferina,
ago–dez/2026).

O PRD é artefato **derivado**: ele aplica as regras dos documentos 01–15 e não cria regra
própria. As regras de escrita, o fluxo de decisão das pendências e o processo de entrega estão
no `CLAUDE.md`, na raiz do repositório; o mapa de dependências entre PRDs está no documento 99.

Este arquivo é um **índice**, não um histórico narrado: registra a situação de cada PRD e a
lista das fatias entregues, uma linha por change. O requisito, a decisão e o porquê de cada
fatia estão no `proposal.md` e no `design.md` dela, em `openspec/changes/archive/<nome>`;
decisão nova tomada durante a implementação está em
`docs/09-topicos-em-aberto-e-sugestoes.md` §1; o que falta de cada PRD está na sua própria
§14. Nenhum dos três é repetido aqui — ao fechar uma fatia, some **uma linha** de tabela,
nunca um parágrafo novo.

## Situação da esteira

| PRD                                       | Assunto                                | Aplicação | Onda | Situação     |
| ----------------------------------------- | -------------------------------------- | --------- | ---- | ------------ |
| [PRD-08](prd-08-comunidades-virtuais.md)  | Comunidades Virtuais e território      | —         | 1    | implementado |
| [PRD-07](prd-07-economia-e-ledger.md)     | Economia de recursos e ledger          | —         | 1    | implementado |
| [PRD-01](prd-01-backend-api.md)           | Backend API (núcleo)                   | —         | 1    | implementado |
| [PRD-02](prd-02-frontend-de-gestao.md)    | Frontend de gestão                     | App 03    | 2    | aprovado     |
| [PRD-04](prd-04-aula-presencial.md)       | Aula presencial (onboarding e trilhas) | App 01    | 2    | aprovado     |
| [PRD-09](prd-09-area-do-mestre.md)        | Área do Mestre (autoria e operação)    | App 09    | 3    | aprovado     |
| [PRD-05](prd-05-area-do-guerreiro.md)     | Área do Guerreiro(a)                   | App 05    | 3    | aprovado     |
| [PRD-13](prd-13-area-dos-responsaveis.md) | Área dos pais e responsáveis           | App 07    | 4    | aprovado     |
| [PRD-03](prd-03-vitrine-publica.md)       | Vitrine pública                        | App 06    | 4    | aprovado     |
| [PRD-14](prd-14-area-do-apoiador.md)      | Área do Apoiador                       | App 08    | 5    | aprovado     |
| [PRD-10](prd-10-batalhas.md)              | Batalhas e eventos presenciais         | —         | 5    | aprovado     |
| [PRD-12](prd-12-jogo-em-javascript.md)    | App 04: Jogo em JavaScript             | App 04    | 5    | aprovado     |
| [PRD-11](prd-11-personalizacao-por-ia.md) | Personalização por IA                  | —         | 5    | aprovado     |

Situações possíveis: **não iniciado**, **em elicitação**, **em redação**, **em revisão**,
**aprovado** e **implementado**. O link para o documento aparece nesta tabela quando ele entra
na pasta.

A coluna **Onda** é a ordem em que os PRDs foram **escritos**, e o motivo de cada onda está
no documento 08. Ela não é a ordem em que o código entra: essa está no documento 99 §9.

O **PRD-06 — Assistente por voz e Modo Ouvinte** foi extinto: o App 02 passou a fazer parte do
App 01 e o Modo Ouvinte saiu do produto. O que restou dele está no PRD-04.

## Fatias entregues

Uma linha por change arquivada em `openspec/changes/archive/`, na ordem em que fechou. "Fatia
N" é o número que o fundador usa para se referir a ela; change sem número não fecha um recorte
formal do PRD — é pré-requisito técnico ou requisito não funcional que a mesma esteira exigiu.

### PRD-01 — Backend API (núcleo) — implementado

- `2026-08-11-fundacao-da-api-e-chave-de-aplicacao`
- `2026-08-12-apoio-escolar-e-etiqueta-ods`
- `2026-08-12-aula-presenca-e-equipe`
- `2026-08-12-criacao-original-nivel-5-e-badge-de-autoria`
- `2026-08-12-persona-sessao-do-adulto-e-permissoes`
- `2026-08-12-poder-trilha-missao-e-atividade`
- `2026-08-12-pontos-niveis-badges-e-ponto-extra`
- `2026-08-12-responsavel-vinculo-e-consentimento`
- `2026-08-12-sessao-do-guerreiro-e-biometria`
- `2026-08-13-ciclo-de-vida-da-chave-de-terceiro`
- `2026-08-13-fila-unica-de-avaliacao`
- `2026-08-13-protecao-das-rotas-publicas`
- `2026-08-13-quiz-ao-vivo`
- `2026-08-13-trilha-de-auditoria`
- `2026-08-14-credencial-de-dispositivo-do-sensor`
- `2026-08-14-leitura-publica-vitrine-e-jogos`
- `2026-08-15-consulta-paginada-das-series`
- `2026-08-17-auditoria-e-estorno-da-coleta`
- `2026-08-21-nick-de-adulto`

### PRD-08 — Comunidades Virtuais e território — implementado

- `2026-08-14-comunidade-virtual-e-locais`
- `2026-08-14-serie-registro-e-pontuacao-da-coleta`
- `2026-08-14-solicitacao-de-local`
- `2026-08-14-tipo-e-desafio-de-coleta`
- `2026-08-15-ciclo-de-vida-da-serie`
- `2026-08-15-exportacao-do-territorio-e-ods-das-series`
- `2026-08-15-leitura-publica-do-territorio`
- `2026-08-17-lista-publica-de-comunidades`

### PRD-07 — Economia de recursos e ledger — implementado (10 fatias)

- Fatia 1 — `2026-08-18-ponto-de-apoio-e-tabela-de-referencia`
- Fatia 2 — `2026-08-18-aporte-lancamento-e-saldo`
- Fatia 3 — `2026-08-18-reserva-e-ciclo-de-vida-da-aula`
- Fatia 4 — `2026-08-18-necessidade-publicada`
- Fatia 5 — `2026-08-18-poder-sustentador-e-prestacao-de-contas`
- Fatia 6 — `2026-08-18-ressarcimento-do-aporte-absorvido`
- Fatia 7 — `2026-08-18-tabela-de-pontos-extras-e-catalogo-avulso`
- Fatia 8 — `2026-08-19-troca-de-recompensa-avulsa`
- Fatia 9 — `2026-08-19-tombamento-e-ficha-de-vida`
- Fatia 10 — `2026-08-19-recompensa-de-marco-e-entrega`
- `2026-08-21-desativacao-do-ponto-de-apoio` (fora das dez fatias, pendência do documento 09
  fechada depois)

Resíduos fora do escopo do PRD-07: a **conferência de inventário** (`RF-07-20`) voltou ao
documento 09 como pendência de decisão; o **desafio extra** espera a entidade `DesafioExtra`
e entra pela fatia do PRD-09 ou do PRD-14 que a definir; **empréstimo de bancada e reposição
solidária** saíram do escopo.

### PRD-02 — Frontend de gestão (App 03) — aprovado (8 fatias)

- Fatia 1 — `2026-08-19-esqueleto-da-gestao-e-cadastro-de-comunidade`
- `2026-08-20-fontes-proprias-e-camada-visual-comum` (requisito não funcional, PRD-02 §10)
- `2026-08-20-implantacao-da-app-03-e-do-nucleo` (infraestrutura de implantação)
- Fatia 2 — `2026-08-21-cadastro-de-personas`
- `2026-08-21-agenda-da-aula-e-ponto-de-apoio` (segunda metade da fatia 1: agenda da aula)
- `2026-08-21-guardas-da-conferencia-e-da-implantacao` (requisito não funcional, PRD-02 §10)
- Fatia 3 — `2026-08-22-avaliacao-da-participacao-e-do-pre-cadastro`
- Fatia 4 — `2026-08-22-avaliacao-de-dados-de-chave-e-de-sugestao`
- Fatia 5 — `2026-08-22-catalogo-de-poderes-e-tela-da-gestao`
- Fatia 6 — `2026-08-25-conducao-da-partida-de-quiz`
- Fatia 7 — `2026-08-25-painel-do-dia-e-anexo-do-termo`
- Fatia 8 — `2026-08-26-esqueleto-da-area-do-guerreiro-e-fim-de-ciclo` (também fatia 1 do
  PRD-05)

### PRD-09 — Área do Mestre (App 09) — aprovado (6 fatias)

- Fatia 1 — `2026-08-22-esqueleto-da-area-do-mestre-e-autoria-da-trilha`
- Fatia 2 — `2026-08-22-culminancia-e-publicacao-da-trilha`
- Fatia 3 — `2026-08-23-etiqueta-ods-da-trilha-e-da-missao`
- Fatia 4 — `2026-08-23-minhas-turmas-e-lancamentos-do-mestre`
- Fatia 5 — `2026-08-23-banco-do-quiz-ao-vivo`
- Fatia 6 — `2026-08-25-conteudo-e-bibliografia-da-missao`

### PRD-04 — Aula presencial (App 01) — aprovado (7 fatias)

- Fatia 1 — `2026-08-24-esqueleto-da-aula-presencial-e-equipe-da-aula`
- Fatia 2 — `2026-08-24-cadastro-do-guerreiro-no-encontro`
- Fatia 3 — `2026-08-24-responsavel-consentimento-e-captura-da-imagem`
- Fatia 4 — `2026-08-24-entrada-por-reconhecimento-e-falha-de-identificacao`
- Fatia 5 — `2026-08-25-troca-por-recompensa-avulsa-no-encontro`
- Fatia 6 — `2026-08-25-aparelho-da-equipe-no-quiz`
- Fatia 7 — `2026-08-25-programacao-do-encontro-e-missao-da-equipe`

### PRD-05 — Área do Guerreiro(a) (App 05) — aprovado (5 fatias)

- Fatia 1 — `2026-08-26-esqueleto-da-area-do-guerreiro-e-fim-de-ciclo` (também fatia 8 do
  PRD-02)
- Fatia 2 — `2026-08-26-coleta-do-territorio-na-area-do-guerreiro`
- Fatia 3 — `2026-08-26-carteira-catalogo-conquistas-e-ranking`
- Fatia 4 — `2026-08-27-inscricao-na-trilha-guia-e-desbloqueio` (também atende `RF-09-26` do
  PRD-09, fatia avulsa)
- Fatia 5 — `2026-08-27-criacao-original-e-portfolio` (também atende `RF-09-30` a `RF-09-34` do
  PRD-09, fatia avulsa)

O escopo do PRD-05 foi revisto na v4 (2026-08-26): **acervo do Guerreiro(a)**, **apoio às
atividades escolares por assistente de voz** e **canal de sugestões** passaram para o Ciclo 02
(documento 09; PRD-05 §3.2).

### Infraestrutura transversal (sem PRD)

- `2026-08-18-isolamento-transacional-dos-testes`
