# PRD-01 — Backend API (núcleo)

## 1. Identificação

| Campo            | Valor                                                      |
| ---------------- | ---------------------------------------------------------- |
| PRD              | PRD-01                                                     |
| Aplicação        | — (núcleo consumido pelas nove aplicações e por terceiros) |
| Onda             | 1                                                          |
| Situação         | em revisão                                                 |
| Versão e data    | v1 — 2026-08-02                                            |
| Depende de       | PRD-07, PRD-08                                             |
| Documentos-fonte | 02, 03 §§1–2 e 12, 04, 11                                  |

## 2. Contexto e objetivo

As nove aplicações não conversam entre si: todas conversam com este núcleo. Ele guarda o
modelo de domínio inteiro — personas, trilhas, atividades, pontos, território, livro-razão —,
decide **quem pode escrever o quê** e serve leitura pública sem autenticação.

Este PRD fecha a Onda 1 consolidando o que os dois anteriores definiram: o domínio do
território (PRD-08) e o do livro-razão (PRD-07) entram aqui como parte do mesmo modelo, com as
mesmas regras, sem duplicação.

No Ciclo 01, entregue este núcleo, a gestão cadastra e opera, o Mestre publica trilha, o
jogador realiza e pontua, o responsável autoriza, o Apoiador aporta e o visitante vê tudo o
que é público — cada um pela sua aplicação, todos sobre a mesma verdade.

## 3. Escopo

### 3.1 Dentro do escopo

- Modelo de domínio completo, incluindo as entidades definidas nos PRD-07 e PRD-08.
- Autenticação por persona: **nick e PIN** para o jogador, **login social** para os adultos e
  credencial de e-mail e senha criada por Admin como exceção.
- Sessão curta para o jogador, adequada a aparelho compartilhado.
- Papéis e permissões: Admin, Mestre, Jogador, Responsável, Apoiador e Visitante.
- Convenções da API: versionamento em `/v1`, formato de erro, paginação e filtros.
- Rotas de consulta públicas, sem autenticação, para vitrine, rankings e painéis.
- Filtro por comunidade em toda consulta, com a plataforma em **instância única**.
- Registro de auditoria de toda escrita: quem, o quê, quando.
- Suporte a aplicações de terceiros sobre as rotas públicas.

### 3.2 Fora do escopo

- Interface de qualquer aplicação — cada uma tem o seu PRD.
- Regras de pontuação, cadência de coleta e valoração de aporte: já normatizadas nos
  documentos 11, 02 e 04 e detalhadas nos PRD-08 e PRD-07.
- Telemetria da Batalha de Laser (PRD-10) e personalização por IA (PRD-11).
- Escolha de linguagem, framework e banco de dados — decisão de implementação, ainda pendente.

## 4. Personas e permissões

| Persona     | Escreve                                                                                                          | Lê                                                                       |
| ----------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Admin       | Tudo: cadastros, aprovações, lançamentos, ledger, comunidades                                                    | Tudo                                                                     |
| Mestre      | Suas trilhas e conteúdos, lançamentos das suas atividades, auditoria de coleta, aprovação de local, aportes seus | O que é público, suas turmas e o **painel do dia** na App 03, em leitura |
| Jogador     | Seus registros de coleta, suas criações, suas sugestões, troca de pontos                                         | Seus dados e o que é público                                             |
| Responsável | Consentimentos, autorizações, solicitações e propostas                                                           | Os jogadores sob sua responsabilidade e o que é público                  |
| Apoiador    | Propostas de desafio extra, documentos comprobatórios, propostas de evolução                                     | Seus aportes, efetividade agregada e o que é público                     |
| Visitante   | Solicitação de participação, pela rota pública da vitrine                                                        | Somente o que é público                                                  |

Regra geral: **leitura pública é aberta; escrita é sempre autenticada e auditada.**

## 5. Jornadas principais

### 5.1 Jogador entra pelo aparelho compartilhado

1. O jogador informa **nick e PIN**.
2. O núcleo devolve uma sessão **curta**, que expira sozinha — o aparelho é do ponto de apoio,
   não dele.
3. Esquecido o PIN, o Mestre ou um Admin redefine na hora, no encontro; o novo PIN é entregue
   ao jogador e a redefinição fica registrada.
4. Toda escrita do jogador é gravada com autoria dele, nunca do aparelho.

### 5.2 Adulto entra por login social

1. Mestre, Apoiador, responsável ou Admin autentica por **login social**.
2. O núcleo associa a conta ao cadastro existente — **login não cria cadastro**: Mestre e
   Apoiador continuam sendo cadastrados por Admin.
3. Conta social sem cadastro correspondente recebe recusa, com a orientação de usar o
   formulário de solicitação da vitrine.
4. Quem não tem conta social recebe de um Admin uma credencial de e-mail e senha, com o mesmo
   vínculo e as mesmas permissões.

### 5.3 Responsável acessa os seus jogadores

1. O responsável entra com o **seu** login.
2. Vê apenas os jogadores vinculados a ele, vínculo conferido por Admin.
3. Cada consentimento que concede ou revoga é gravado com autoria, data e hora e versão do
   termo.

### 5.4 Visitante consulta sem login

1. Qualquer consulta pública responde sem autenticação: vitrine, rankings, painéis de
   comunidade e prestação de contas.
2. A resposta pública nunca traz dado de contato, imagem real de criança, valor em reais nem
   granularidade de território abaixo de rua.

### 5.5 Terceiro constrói sobre a API

1. A aplicação de terceiro consome as rotas públicas de `/v1`.
2. Mudança que quebre contrato abre `/v2`, e `/v1` segue no ar por prazo declarado.

## 6. Requisitos funcionais

| ID         | Requisito                                                                                        | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------------ | ---------- |
| `RF-01-01` | Núcleo expõe todas as rotas sob prefixo de versão, começando em `/v1`                            | essencial  |
| `RF-01-02` | Rotas de consulta pública respondem sem autenticação                                             | essencial  |
| `RF-01-03` | Toda rota de escrita exige autenticação e registra autoria, data e hora                          | essencial  |
| `RF-01-04` | Jogador autentica com nick e PIN e recebe sessão de duração curta                                | essencial  |
| `RF-01-05` | Mestre ou Admin redefine o PIN de um jogador, com registro de quem redefiniu                     | essencial  |
| `RF-01-06` | Adulto autentica por login social vinculado a cadastro existente                                 | essencial  |
| `RF-01-07` | Login social sem cadastro correspondente é recusado, sem criar persona                           | essencial  |
| `RF-01-08` | Admin cria credencial de e-mail e senha para adulto sem conta social                             | essencial  |
| `RF-01-09` | Responsável autentica com login próprio e enxerga apenas os jogadores vinculados                 | essencial  |
| `RF-01-10` | Núcleo aplica a matriz de permissões por papel em toda operação                                  | essencial  |
| `RF-01-11` | Mestre lê o painel do dia sem poder escrever nas rotas de gestão                                 | essencial  |
| `RF-01-12` | Toda consulta de dado de comunidade aceita e aplica filtro por comunidade                        | essencial  |
| `RF-01-13` | Núcleo mantém as entidades de personas, vínculos e consentimentos versionados                    | essencial  |
| `RF-01-14` | Núcleo mantém as entidades de trilha, ponto de trilha, atividade, equipe, presença e resultado   | essencial  |
| `RF-01-15` | Núcleo mantém pontos, níveis e badges por trilha ou poder, derivados das realizações             | essencial  |
| `RF-01-16` | Núcleo expõe leitura de progresso e **débito** de pontos, sem nenhuma rota de crédito para jogos | essencial  |
| `RF-01-17` | Núcleo mantém as entidades do território definidas no PRD-08                                     | essencial  |
| `RF-01-18` | Núcleo mantém as entidades do livro-razão definidas no PRD-07                                    | essencial  |
| `RF-01-19` | Núcleo mantém solicitação de participação, sugestões e propostas em fila única de avaliação      | essencial  |
| `RF-01-20` | Núcleo mantém criação original com autoria creditada por toda a vida do registro                 | essencial  |
| `RF-01-21` | Erro segue formato único, com código, mensagem em linguagem simples e campo em falta             | essencial  |
| `RF-01-22` | Listagens são paginadas e aceitam filtro por comunidade, período e persona                       | essencial  |
| `RF-01-23` | Núcleo registra trilha de auditoria consultável das ações de Admin                               | essencial  |
| `RF-01-24` | Núcleo documenta as rotas públicas para uso por aplicações de terceiros                          | desejável  |
| `RF-01-25` | Versão anterior da API segue disponível por prazo declarado após a abertura da seguinte          | desejável  |

## 7. Regras de negócio

| ID         | Regra                                                                                  | Invariante | Fonte       |
| ---------- | -------------------------------------------------------------------------------------- | ---------- | ----------- |
| `RN-01-01` | Só o Jogador tem autocadastro; Mestre e Apoiador são cadastrados por Admin             | 3          | 02 §1       |
| `RN-01-02` | Novo Admin só entra por inclusão manual de outro Admin                                 | 3          | 02 §1       |
| `RN-01-03` | Solicitação de participação não cria cadastro nem acesso                               | 3          | 02 §1       |
| `RN-01-04` | Login não cria persona: autentica quem já tem cadastro                                 | 3          | 03 §1.1     |
| `RN-01-05` | Todo jogador tem vínculo obrigatório a exatamente uma comunidade                       | 4          | 02 §1       |
| `RN-01-06` | Pontos só vêm de realização; o App 04 debita e nunca credita                           | 8          | 11 §§1, 8.4 |
| `RN-01-07` | Nenhuma atividade é agendável sem lastro dos recursos                                  | 9          | 04 §1       |
| `RN-01-08` | Dado do território tem guarda permanente com coletor identificado                      | 7          | 02 §1       |
| `RN-01-09` | Anonimização se aplica na saída, nunca no armazenamento                                | 7          | 02 §1       |
| `RN-01-10` | Jogador aparece publicamente só por avatar e nick, e só com autorização do responsável | 12         | 03 §12      |
| `RN-01-11` | Rota pública nunca devolve dado de contato, valor em reais ou imagem real de criança   | 10, 16     | 03 §12      |
| `RN-01-12` | Consentimento é versionado, com autoria, data e hora                                   | 11         | 03 §12      |
| `RN-01-13` | Criação original carrega o autor por toda a vida do registro                           | 5          | 02 §4       |
| `RN-01-14` | O PIN é guardado com hash, nunca em texto legível, e não circula por e-mail            | —          | 03 §12      |
| `RN-01-15` | Recusa de consentimento nunca exclui o jogador da atividade                            | 11         | 03 §12      |

## 8. Modelo de dados

O domínio se organiza em cinco blocos. Território e economia são os modelos dos PRD-08 e
PRD-07, aqui apenas referenciados — este PRD não os redefine.

```text
IDENTIDADE          GAMIFICAÇÃO           OPERAÇÃO
Jogador             Poder                 Aula/Agenda
Mestre              Trilha                Presença
Apoiador            PontoDeTrilha         Resultado
Admin               Atividade             Equipe
Responsavel         DesafioDeDesbloqueio  Batalha
VinculoResponsavel  DesafioExtra          PerguntaDeQuiz
Credencial          Ponto/Nivel/Badge     PartidaDeQuiz
Consentimento       CriacaoOriginal
Sessao
                    PARTICIPAÇÃO          TERRITÓRIO (PRD-08)    ECONOMIA (PRD-07)
                    SolicitacaoDeParticipacao  ComunidadeVirtual  TipoDeRecurso
                    SugestaoOuProposta         Local              Aporte
                    Auditoria                  SerieDeColeta      Lancamento
                                               RegistroDeColeta   ItemPatrimonial
```

| Entidade             | Atributos essenciais                                                                      |
| -------------------- | ----------------------------------------------------------------------------------------- |
| `Credencial`         | persona, tipo (PIN, login social, e-mail e senha), identificador, hash, criada por, ativa |
| `Sessao`             | persona, início, expiração, origem (aplicação), encerrada em                              |
| `VinculoResponsavel` | responsável, jogador, conferido por Admin, início, fim                                    |
| `Consentimento`      | responsável, jogador, tipo, versão do termo, decisão, data e hora                         |
| `Auditoria`          | autor, papel, ação, entidade afetada, data e hora, origem                                 |

Imutabilidade: `Consentimento` e `Auditoria` são **somente inserção**. Revogação é um novo
registro, não a edição do anterior — é o que permite responder "o que valia naquela data".

## 9. Contratos de API

Convenções válidas para todas as rotas:

| Aspecto      | Definição                                                               |
| ------------ | ----------------------------------------------------------------------- |
| Versão       | prefixo `/v1` em toda rota                                              |
| Autenticação | token de sessão no cabeçalho; ausência dele só é aceita em rota pública |
| Erro         | corpo único com código, mensagem em linguagem simples e campo em falta  |
| Listagem     | paginada, com filtros de comunidade, período e persona                  |
| Data e hora  | sempre com fuso, e a data do fato nunca é substituída pela do registro  |

| Método | Rota                     | Autenticação    | Descrição                                      |
| ------ | ------------------------ | --------------- | ---------------------------------------------- |
| POST   | `/v1/sessoes/jogador`    | pública         | Autentica com nick e PIN e abre sessão curta   |
| POST   | `/v1/sessoes/social`     | pública         | Autentica adulto por login social              |
| POST   | `/v1/sessoes/credencial` | pública         | Autentica adulto por e-mail e senha            |
| DELETE | `/v1/sessoes/atual`      | autenticada     | Encerra a sessão                               |
| POST   | `/v1/jogadores/{id}/pin` | Mestre ou Admin | Redefine o PIN, com registro de quem redefiniu |
| POST   | `/v1/credenciais`        | Admin           | Cria credencial de e-mail e senha              |
| GET    | `/v1/eu`                 | autenticada     | Persona, papéis e permissões da sessão         |
| GET    | `/v1/vitrine/...`        | pública         | Consultas públicas de vitrine e rankings       |
| GET    | `/v1/auditoria`          | Admin           | Trilha de auditoria das ações de gestão        |

As rotas de domínio — território, ledger, trilhas, atividades — estão nos PRDs que as definem
e seguem estas mesmas convenções.

Erros previstos: PIN incorreto (401, sem revelar se o nick existe); login social sem cadastro
(403, com orientação de solicitar participação pela vitrine); escrita sem permissão do papel
(403); sessão expirada (401); filtro de comunidade ausente onde é obrigatório (422).

## 10. Requisitos não funcionais

- Sessão do jogador curta o bastante para o aparelho compartilhado e longa o bastante para
  atravessar uma atividade sem reautenticar.
- Consulta pública cacheável e tolerante a pico de acesso em dia de culminância.
- Escrita tolerante a rede instável: cliente pode reenviar sem duplicar o registro.
- Armazenamento capaz de guardar **séries temporais com retenção permanente**.
- Documentação das rotas públicas legível por quem não participou do projeto.
- Código aberto, em pt-BR, com mensagens de erro em linguagem simples.

## 11. LGPD e proteção da criança

| Dado                       | Finalidade                   | Base legal        | Retenção                 | Quem acessa             |
| -------------------------- | ---------------------------- | ----------------- | ------------------------ | ----------------------- |
| Nick e PIN do jogador      | Autenticação                 | consentimento     | enquanto durar o vínculo | o próprio; hash na base |
| Nome e data de nascimento  | Identificação e faixa etária | consentimento     | enquanto durar o vínculo | gestão e responsável    |
| Conta social do adulto     | Autenticação                 | consentimento     | enquanto durar o vínculo | gestão e o próprio      |
| Consentimentos versionados | Prova do que foi autorizado  | obrigação legal   | permanente               | gestão e responsável    |
| Auditoria de escrita       | Rastreabilidade das ações    | interesse público | permanente               | Admin                   |

- O PIN é guardado com **hash** e nunca circula por e-mail ou mensagem.
- **Adesão em duas etapas**: o cadastro livre permite participar; a divulgação pública do
  perfil depende de autorização do responsável, registrada como consentimento versionado.
- O responsável consulta, pela App 07, **quem acessou** os dados da criança — a trilha de
  auditoria existe também para isso.
- Nenhuma rota pública devolve imagem real, nome civil ou contato de criança.

## 12. Critérios de aceite e métricas

- Consulta pública de vitrine responde sem token e sem qualquer dado restrito.
- Jogador autenticado em um aparelho continua com a sessão do outro jogador encerrada ao
  expirar o tempo, sem vazamento entre sessões.
- Login social de conta sem cadastro é recusado e **nenhuma persona é criada**.
- Mestre que tenta escrever em rota de gestão recebe 403, e a leitura do painel do dia
  responde normalmente.
- Toda escrita bem-sucedida gera registro de auditoria com autor, papel e data e hora.
- Revogação de consentimento cria novo registro, e o anterior continua consultável.
- Nenhuma rota de crédito de pontos existe para o App 04 — a tentativa devolve 404.

Este PRD não sustenta hipótese própria: ele é a condição para que H1, H2 e H3 sejam medidas
pelas aplicações que as verificam.

## 13. Decisões tomadas neste PRD

| Decisão                                                                      | Gravada em | Doc 09       |
| ---------------------------------------------------------------------------- | ---------- | ------------ |
| Instância única, com a comunidade como vínculo nos registros                 | 03 §1      | Já decididos |
| API versionada na rota, a partir de `/v1`                                    | 03 §1      | Já decididos |
| Jogador entra com nick e PIN, redefinido por Mestre ou Admin                 | 03 §1.1    | Já decididos |
| Adultos entram por login social                                              | 03 §1.1    | Já decididos |
| Credencial de e-mail e senha criada por Admin para quem não tem conta social | 03 §1.1    | Já decididos |
| Responsável tem login próprio, vinculado a um ou mais jogadores              | 03 §1.1    | Já decididos |
| Mestre acessa a App 03 apenas em leitura do painel do dia                    | 03 §5      | Já decididos |

## 14. Pendências que permanecem

- **Stack do backend**: linguagem, framework e banco de dados, incluindo o armazenamento das
  séries temporais do território. É decisão de implementação e não altera os requisitos.
- **Instituição com mais de um usuário** no mesmo cadastro de Apoiador, e como se registra
  quem agiu em nome dela.
- **Prazo de disponibilidade da versão anterior** da API depois que uma nova abrir.
- **Duração exata da sessão** do jogador, a calibrar no primeiro encontro real.
- **Quem pode lançar pontuação negativa** e com que auditoria — questão em aberto do PRD-02,
  que este núcleo apenas registra.

## 15. Rastreabilidade

| Requisito               | Origem                                     |
| ----------------------- | ------------------------------------------ |
| `RF-01-01`, `RF-01-25`  | 03 §1 (API versionada)                     |
| `RF-01-02` e `RF-01-03` | 03 §1 (rotas abertas, escrita autenticada) |
| `RF-01-04` a `RF-01-09` | 03 §1.1 (como cada persona entra)          |
| `RF-01-10` e `RF-01-11` | 03 §§5, 11 (fronteira App 03 × App 09)     |
| `RF-01-12`              | 03 §1 (instância única)                    |
| `RF-01-13`              | 03 §12 (LGPD e consentimentos)             |
| `RF-01-14` e `RF-01-15` | 02 §§3–5 e 11 §§2, 4–7                     |
| `RF-01-16`              | 11 §8.4 (contrato dos jogos)               |
| `RF-01-17`              | PRD-08                                     |
| `RF-01-18`              | PRD-07                                     |
| `RF-01-19` e `RF-01-20` | 02 §§1, 4 e 03 §§7, 9–11                   |
| `RF-01-21` a `RF-01-24` | 03 §1 (princípios de arquitetura)          |
