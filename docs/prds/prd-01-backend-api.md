# PRD-01 — Backend API (núcleo)

## 1. Identificação

| Campo            | Valor                                                      |
| ---------------- | ---------------------------------------------------------- |
| PRD              | PRD-01                                                     |
| Aplicação        | — (núcleo consumido pelas oito aplicações e por terceiros) |
| Onda             | 1                                                          |
| Situação         | aprovado                                                   |
| Versão e data    | v8 — 2026-08-06                                            |
| Depende de       | PRD-07, PRD-08                                             |
| Documentos-fonte | 02, 03 §§1–3, 5, 9, 11 e 12, 04, 11                        |

## 2. Contexto e objetivo

As oito aplicações não conversam entre si: todas conversam com este núcleo. Ele guarda o
modelo de domínio inteiro — personas, trilhas, atividades, pontos, território, livro-razão —,
decide **quem pode escrever o quê** e serve leitura pública sem autenticação.

Este PRD fecha a Onda 1 consolidando o que os dois anteriores definiram: o domínio do
território (PRD-08) e o do livro-razão (PRD-07) entram aqui como parte do mesmo modelo, com as
mesmas regras, sem duplicação.

No Ciclo 01, entregue este núcleo, a gestão cadastra e opera, o Mestre publica trilha, o
Guerreiro(a) realiza e pontua, o responsável autoriza, o Apoiador aporta e o visitante vê tudo
o que é público — cada um pela sua aplicação, todos sobre a mesma verdade.

## 3. Escopo

### 3.1 Dentro do escopo

- Modelo de domínio completo, incluindo as entidades definidas nos PRD-07 e PRD-08.
- Autenticação por persona: **nick e imagem** para o Guerreiro(a), **login social** para os
  adultos e credencial de usuário e senha provisória criada por Admin ou Mestre como exceção.
- Guarda do _template_ biométrico do Guerreiro(a), gerado no onboarding, e sua conferência no
  login.
- Cadastro do responsável por Admin ou Mestre e vínculo com os Guerreiros e Guerreiras já
  cadastrados.
- Sessão curta para o Guerreiro(a), adequada a aparelho compartilhado.
- Papéis e permissões: Admin, Mestre, Guerreiro(a), Responsável, Apoiador e Visitante.
- Convenções da API: versionamento em `/v1`, formato de erro, paginação e filtros.
- Rotas de consulta públicas, sem autenticação, para vitrine, rankings e painéis.
- Filtro por comunidade em toda consulta, com a plataforma em **instância única**.
- Registro de auditoria de toda escrita: quem, o quê, quando.
- Suporte a aplicações de terceiros sobre as rotas públicas.

### 3.2 Fora do escopo

- Interface de qualquer aplicação — cada uma tem o seu PRD.
- Regras de pontuação, cadência de coleta e valoração de aporte: já normatizadas nos
  documentos 11, 02 e 04 e detalhadas nos PRD-08 e PRD-07.
- Captura da imagem e conversa de cadastro: são da App 01 (PRD-04). Aqui ficam apenas a guarda
  do _template_, a conferência no login e a alternativa para quem recusa a biometria.
- Escolha do provedor de reconhecimento facial e do lugar onde o _template_ é extraído
  (dispositivo × servidor): pendência registrada no documento 09.
- Telemetria da Batalha de Laser (PRD-10) e personalização por IA (PRD-11).
- Escolha de linguagem, framework e banco de dados — decisão de implementação, ainda pendente.

## 4. Personas e permissões

| Persona      | Escreve                                                                                                                                                                                                                                       | Lê                                                                       |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Admin        | Tudo: cadastros, aprovações, lançamentos, ledger, comunidades                                                                                                                                                                                 | Tudo                                                                     |
| Mestre       | Suas trilhas e conteúdos, lançamentos e pontuação negativa das suas atividades, condução do Quiz ao Vivo das suas aulas, auditoria de coleta, aprovação de local, aportes seus, cadastro de responsável e vínculo com Guerreiros e Guerreiras | O que é público, suas turmas e o **painel do dia** na App 03, em leitura |
| Guerreiro(a) | Seus registros de coleta, suas criações, suas sugestões, recompensas recebidas nos marcos, a **equipe que forma na aula** e a resposta de quiz da equipe                                                                                      | Seus dados, as equipes da aula em andamento e o que é público            |
| Responsável  | Consentimentos, autorizações, solicitações e propostas                                                                                                                                                                                        | Os Guerreiros e Guerreiras sob sua responsabilidade e o que é público    |
| Apoiador     | Propostas de desafio extra, documentos comprobatórios, propostas de evolução                                                                                                                                                                  | Seus aportes, efetividade agregada e o que é público                     |
| Visitante    | Solicitação de participação, pela rota pública da vitrine                                                                                                                                                                                     | Somente o que é público                                                  |

Regra geral: **leitura pública é aberta; escrita é sempre autenticada e auditada.**

## 5. Jornadas principais

### 5.1 Guerreiro(a) entra pelo aparelho compartilhado

1. O Guerreiro(a) informa o **nick** e captura a **imagem** pela câmera do aparelho. É assim em
   **todas** as aplicações do Guerreiro(a), não só na chegada da aula: é o que garante que a
   atividade foi feita pela própria criança.
2. O núcleo confere a imagem contra o _template_ biométrico gravado no onboarding — o nick
   restringe a busca, a imagem confirma — e devolve uma sessão **curta**, que expira sozinha:
   o aparelho é do ponto de apoio, não dele.
3. **Sem câmera não há entrada.** A criança não tem PIN nem senha para substituir a imagem.
4. Enquanto o Guerreiro(a) **não tem imagem gravada** — onboarding feito sem o responsável —,
   quem abre a sessão dele é o Mestre ou um Admin, no encontro, e fica registrado quem
   confirmou. Mesmo caminho para a falha de reconhecimento e para quem recusou a biometria.
5. Imagem que envelheceu ou captura ruim: o Mestre ou um Admin recadastra a imagem de
   referência, e a substituição fica registrada.
6. Toda escrita do Guerreiro(a) é gravada com autoria dele, nunca do aparelho.

### 5.2 Adulto entra por login social

1. Mestre, Apoiador, responsável ou Admin autentica por **login social**.
2. O núcleo associa a conta ao cadastro existente — **login não cria cadastro**: Mestre e
   Apoiador continuam sendo cadastrados por Admin, e o responsável, por Admin ou Mestre.
3. Conta social sem cadastro correspondente recebe recusa; a quem quer ser Mestre ou Apoiador,
   a resposta orienta a usar o formulário de solicitação da vitrine.
4. Quem não tem conta social recebe de um Admin ou Mestre uma credencial de **usuário e senha
   provisória**, com o mesmo vínculo e as mesmas permissões. O usuário não precisa ser e-mail.
5. Nessa credencial, a **troca de senha é obrigatória no primeiro acesso**: enquanto não
   acontece, a sessão só serve para trocar a senha.

### 5.3 Responsável é cadastrado e acessa os seus Guerreiros e Guerreiras

1. O responsável se apresenta **pessoalmente** em atividade presencial, na primeira vez —
   normalmente no primeiro dia de aula da criança, que ele acompanha —, e informa seu e-mail e
   as crianças sob sua responsabilidade.
2. Um Admin (App 03) ou um Mestre (App 09) cadastra o responsável e vincula a ele **qualquer**
   Guerreiro(a) **já cadastrado** no onboarding, declarando o **grau de parentesco**, em texto
   livre, de cada vínculo.
3. O núcleo recusa o vínculo quando o Guerreiro(a) já tem **três responsáveis**.
4. O responsável entra com o **seu** login — social ou usuário e senha — e vê apenas os
   Guerreiros e Guerreiras vinculados a ele.
5. Cada consentimento que concede ou revoga é gravado com autoria, data e hora e versão do
   termo. É a aprovação dele que **libera o cadastro biométrico** do Guerreiro(a) que ainda não
   o tem.

### 5.4 Visitante consulta sem login

1. Qualquer consulta pública responde sem autenticação: vitrine, rankings, painéis de
   comunidade e prestação de contas.
2. A resposta pública nunca traz dado de contato, imagem real de criança, valor em reais nem
   granularidade de território abaixo de rua.

### 5.5 Terceiro constrói sobre a API

1. A aplicação de terceiro consome as rotas públicas de `/v1`.
2. Mudança que quebre contrato abre `/v2`, e `/v1` segue no ar por prazo declarado.

## 6. Requisitos funcionais

| ID         | Requisito                                                                                                                                                                                       | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `RF-01-01` | Núcleo expõe todas as rotas sob prefixo de versão, começando em `/v1`                                                                                                                           | essencial  |
| `RF-01-02` | Rotas de consulta pública respondem sem autenticação                                                                                                                                            | essencial  |
| `RF-01-03` | Toda rota de escrita exige autenticação e registra autoria, data e hora                                                                                                                         | essencial  |
| `RF-01-04` | Guerreiro(a) autentica com nick e imagem e recebe sessão de duração curta                                                                                                                       | essencial  |
| `RF-01-05` | Núcleo guarda o _template_ biométrico do Guerreiro(a) e o confere no login, sem devolvê-lo                                                                                                      | essencial  |
| `RF-01-06` | Mestre ou Admin confirma a identidade do Guerreiro(a) e abre a sessão dele quando não há _template_ gravado, o reconhecimento falha ou a biometria foi recusada, com registro de quem confirmou | essencial  |
| `RF-01-07` | Núcleo grava o _template_ do Guerreiro(a) cadastrado sem imagem assim que o responsável aprova a participação                                                                                   | essencial  |
| `RF-01-08` | Mestre ou Admin recadastra a imagem de referência do Guerreiro(a), com registro de quem recadastrou                                                                                             | essencial  |
| `RF-01-09` | Adulto autentica por login social vinculado a cadastro existente                                                                                                                                | essencial  |
| `RF-01-10` | Login social ou usuário sem cadastro correspondente é recusado, sem criar persona                                                                                                               | essencial  |
| `RF-01-11` | Admin ou Mestre cria credencial de usuário e senha provisória para adulto sem conta social                                                                                                      | essencial  |
| `RF-01-12` | Credencial provisória exige troca de senha no primeiro acesso, antes de qualquer outra operação                                                                                                 | essencial  |
| `RF-01-13` | Admin ou Mestre cadastra responsável e vincula a ele quem já está cadastrado, com grau de parentesco                                                                                            | essencial  |
| `RF-01-14` | Núcleo recusa o vínculo que passaria de três responsáveis para o mesmo Guerreiro(a)                                                                                                             | essencial  |
| `RF-01-15` | Responsável autentica com login próprio e enxerga apenas os Guerreiros e Guerreiras vinculados                                                                                                  | essencial  |
| `RF-01-16` | Núcleo aplica a matriz de permissões por papel em toda operação                                                                                                                                 | essencial  |
| `RF-01-17` | Mestre lê o painel do dia e conduz o Quiz ao Vivo das suas aulas, sem escrever nas demais rotas de gestão                                                                                       | essencial  |
| `RF-01-18` | Toda consulta de dado de comunidade aceita e aplica filtro por comunidade                                                                                                                       | essencial  |
| `RF-01-19` | Núcleo mantém as entidades de personas, vínculos e consentimentos versionados                                                                                                                   | essencial  |
| `RF-01-20` | Núcleo mantém as entidades de trilha, missão, atividade, equipe, presença e resultado                                                                                                           | essencial  |
| `RF-01-21` | Núcleo mantém pontos, níveis e badges por trilha ou poder, derivados das realizações                                                                                                            | essencial  |
| `RF-01-22` | Núcleo expõe leitura de progresso e **débito** de pontos, sem nenhuma rota de crédito para jogos                                                                                                | essencial  |
| `RF-01-23` | Núcleo mantém as entidades do território definidas no PRD-08                                                                                                                                    | essencial  |
| `RF-01-24` | Núcleo mantém as entidades do livro-razão definidas no PRD-07                                                                                                                                   | essencial  |
| `RF-01-25` | Núcleo mantém solicitação de participação, sugestões e propostas em fila única de avaliação                                                                                                     | essencial  |
| `RF-01-26` | Núcleo mantém criação original com autoria creditada por toda a vida do registro                                                                                                                | essencial  |
| `RF-01-35` | Núcleo mantém as entidades do apoio escolar — disciplina, conteúdo do corpus e consulta                                                                                                         | essencial  |
| `RF-01-36` | Núcleo mantém a resposta de quiz por equipe e pergunta, com o momento de chegada                                                                                                                | essencial  |
| `RF-01-37` | Equipe é criada pelo Guerreiro(a), vinculada a uma aula, e encerra com ela sem ser reaproveitada                                                                                                | essencial  |
| `RF-01-38` | Núcleo recusa o sexto integrante e o segundo familiar de 17 anos ou mais na mesma equipe                                                                                                        | essencial  |
| `RF-01-39` | Núcleo aceita o Guerreiro(a) em várias equipes da aula e em uma só por partida de quiz                                                                                                          | essencial  |
| `RF-01-40` | Núcleo mantém a etiqueta ODS da trilha — objetivo de 1 a 18, com meta opcional — declarada pelo Mestre autor                                                                                    | essencial  |
| `RF-01-45` | Núcleo aceita etiqueta própria de uma missão, sempre opcional, que prevalece sobre a da trilha nos vínculos dela                                                                                | essencial  |
| `RF-01-41` | Núcleo propaga a etiqueta da missão, ou a da trilha na falta dela, para o desafio de coleta e para o desafio extra vinculados                                                                   | essencial  |
| `RF-01-42` | Núcleo agrega a cobertura de ODS por trilha, poder, comunidade e ciclo, derivada das etiquetas declaradas                                                                                       | essencial  |
| `RF-01-43` | Núcleo expõe a cobertura de ODS em rota pública, sempre agregada por comunidade e ciclo                                                                                                         | essencial  |
| `RF-01-44` | Núcleo recusa, a partir do Ciclo 02, publicar trilha sem ao menos uma etiqueta ODS                                                                                                              | essencial  |
| `RF-01-27` | Erro segue formato único, com código, mensagem em linguagem simples e campo em falta                                                                                                            | essencial  |
| `RF-01-28` | Listagens são paginadas e aceitam filtro por comunidade, período e persona                                                                                                                      | essencial  |
| `RF-01-29` | Núcleo registra trilha de auditoria consultável das ações de Admin                                                                                                                              | essencial  |
| `RF-01-30` | Núcleo documenta as rotas públicas para uso por aplicações de terceiros                                                                                                                         | desejável  |
| `RF-01-31` | Versão anterior da API segue disponível por prazo declarado após a abertura da seguinte                                                                                                         | desejável  |
| `RF-01-32` | Núcleo deriva a disponibilidade do App 01 da aula agendada para a data e o horário correntes                                                                                                    | essencial  |
| `RF-01-33` | Núcleo responde à consulta pública por **nick exato**, apenas de Guerreiro(a) com divulgação autorizada                                                                                         | essencial  |
| `RF-01-34` | Núcleo não expõe listagem, busca parcial nem sugestão de nicks de Guerreiros e Guerreiras                                                                                                       | essencial  |

## 7. Regras de negócio

| ID         | Regra                                                                                                                   | Invariante | Fonte       |
| ---------- | ----------------------------------------------------------------------------------------------------------------------- | ---------- | ----------- |
| `RN-01-01` | Só o Guerreiro(a) tem autocadastro; Mestre e Apoiador são cadastrados por Admin, e o responsável por Admin ou Mestre    | 3          | 02 §1       |
| `RN-01-02` | Novo Admin só entra por inclusão manual de outro Admin                                                                  | 3          | 02 §1       |
| `RN-01-03` | Solicitação de participação não cria cadastro nem acesso                                                                | 3          | 02 §1       |
| `RN-01-04` | Login não cria persona: autentica quem já tem cadastro                                                                  | 3          | 03 §1.1     |
| `RN-01-05` | Todo Guerreiro(a) tem vínculo obrigatório a exatamente uma comunidade                                                   | 4          | 02 §1       |
| `RN-01-06` | Pontos só vêm de realização; o App 04 debita e nunca credita                                                            | 8          | 11 §§1, 8.4 |
| `RN-01-07` | Nenhuma atividade é agendável sem lastro dos recursos                                                                   | 9          | 04 §1       |
| `RN-01-08` | Dado do território tem guarda permanente com coletor identificado                                                       | 7          | 02 §1       |
| `RN-01-09` | Anonimização se aplica na saída, nunca no armazenamento                                                                 | 7          | 02 §1       |
| `RN-01-10` | Guerreiro(a) aparece publicamente só por avatar e nick, e só com autorização do responsável                             | 12         | 03 §12      |
| `RN-01-11` | Rota pública nunca devolve dado de contato, valor em reais ou imagem real de criança                                    | 10, 16     | 03 §12      |
| `RN-01-12` | Consentimento é versionado, com autoria, data e hora                                                                    | 11         | 03 §12      |
| `RN-01-13` | Criação original carrega o autor por toda a vida do registro                                                            | 5          | 02 §4       |
| `RN-01-14` | O _template_ biométrico é guardado cifrado, com acesso auditado, e nenhuma rota o devolve nem devolve a imagem original | 12         | 03 §3.3     |
| `RN-01-15` | A imagem do Guerreiro(a) serve só para identificá-lo — presença e autenticação; outro uso exige nova base legal         | 12         | 03 §3.3     |
| `RN-01-16` | Recusar a biometria não impede o acesso: a confirmação do Mestre ou Admin, no encontro, é a alternativa equivalente     | 11         | 03 §3.3     |
| `RN-01-17` | O _template_ só é gravado com consentimento do responsável registrado                                                   | 11         | 03 §3.3     |
| `RN-01-18` | Senha provisória é guardada com hash, vale para um único acesso e é trocada pelo próprio adulto                         | —          | 03 §1.1     |
| `RN-01-19` | Cada Guerreiro(a) tem no máximo três responsáveis vinculados, com grau de parentesco em texto livre                     | 3          | 02 §1       |
| `RN-01-20` | Responsável só é vinculado a Guerreiro(a) já cadastrado no onboarding                                                   | 3          | 02 §1       |
| `RN-01-21` | Recusa de consentimento nunca exclui o Guerreiro(a) da atividade                                                        | 11         | 03 §12      |
| `RN-01-22` | O nick é chave de acompanhamento público, cedido pela família: o núcleo nunca o descobre nem o sugere a um adulto       | 12         | 02 §1       |
| `RN-01-23` | A etiqueta ODS não entra em ponto, nível ou badge; é opcional no Ciclo 01 e obrigatória na trilha a partir do Ciclo 02  | 20         | 11 §2.1     |
| `RN-01-24` | A cobertura de ODS nunca é atributo de um Guerreiro(a): agrega por trilha, poder, comunidade e ciclo                    | 20         | 11 §2.1     |

## 8. Modelo de dados

O domínio se organiza em cinco blocos. Território e economia são os modelos dos PRD-08 e
PRD-07, aqui apenas referenciados — este PRD não os redefine.

```text
IDENTIDADE          GAMIFICAÇÃO           OPERAÇÃO
Guerreiro(a)             Poder                 Aula/Agenda
Mestre              Trilha                Presença
Apoiador            Missao                Resultado
Admin               Atividade             Equipe
Responsavel         DesafioDeDesbloqueio  Batalha
VinculoResponsavel  DesafioExtra          PerguntaDeQuiz
Credencial          Ponto/Nivel/Badge     PartidaDeQuiz
Consentimento       CriacaoOriginal       RespostaDeQuiz
Sessao              Conteudo
                    BibliografiaDaMissao
                    Culminancia
                    RecompensaDeMarco
                    SugestaoDeEstrutura
                    ProducaoDaMissao
                    EtiquetaODS
                    PARTICIPAÇÃO               TERRITÓRIO (PRD-08)  ECONOMIA (PRD-07)
                    SolicitacaoDeParticipacao  ComunidadeVirtual    TipoDeRecurso
                    SolicitacaoDoResponsavel   Local                Aporte
                    SugestaoOuProposta         SerieDeColeta        Lancamento
                    Auditoria                  RegistroDeColeta     ItemPatrimonial

                    APOIO ESCOLAR (PRD-05)
                    DisciplinaDeApoio
                    ConteudoDeApoio
                    ConsultaDeApoio
```

| Entidade             | Atributos essenciais                                                                                                                             |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Credencial`         | persona, tipo (biometria, login social, usuário e senha), identificador, segredo (_template_ cifrado ou hash), criada por, troca pendente, ativa |
| `Sessao`             | persona, início, expiração, origem (aplicação), como autenticou, quem confirmou, encerrada em                                                    |
| `VinculoResponsavel` | responsável, Guerreiro(a), grau de parentesco, cadastrado por (Admin ou Mestre), início, fim                                                     |
| `Consentimento`      | responsável, Guerreiro(a), tipo, versão do termo, decisão, data e hora, testemunha (Mestre ou Admin), anexo do termo assinado                    |
| `EtiquetaODS`        | trilha ou missão, objetivo (1 a 18), meta opcional (`4.7`, `13.3`, `17.18`), declarada por, data                                                 |
| `Auditoria`          | autor, papel, ação, entidade afetada, data e hora, origem                                                                                        |

A `Aula/Agenda` carrega **comunidade, data, horário inicial e final**: é dela que o App 01 tira
a comunidade do novo cadastro, e é a existência dela que habilita o onboarding naquele momento.
Não há parâmetro de liberação separado.

`Conteudo`, `BibliografiaDaMissao`, `Culminancia`, `RecompensaDeMarco` e `SugestaoDeEstrutura`
entram pela autoria de trilha e têm os
atributos definidos no PRD-09. A `Culminancia` é o que torna verificável a regra de que toda
trilha termina em criação original: sem ela, a trilha não é publicável.

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

| Método | Rota                                | Autenticação    | Descrição                                                      |
| ------ | ----------------------------------- | --------------- | -------------------------------------------------------------- |
| POST   | `/v1/sessoes/guerreiro`             | pública         | Autentica com nick e imagem e abre sessão curta                |
| POST   | `/v1/sessoes/guerreiro/confirmacao` | Mestre ou Admin | Abre a sessão do Guerreiro(a) por confirmação humana           |
| POST   | `/v1/sessoes/social`                | pública         | Autentica adulto por login social                              |
| POST   | `/v1/sessoes/credencial`            | pública         | Autentica adulto por usuário e senha                           |
| DELETE | `/v1/sessoes/atual`                 | autenticada     | Encerra a sessão                                               |
| POST   | `/v1/guerreiros/{id}/imagem`        | Mestre ou Admin | Grava ou recadastra a imagem de referência, com registro       |
| POST   | `/v1/credenciais`                   | Admin ou Mestre | Cria credencial de usuário e senha provisória                  |
| POST   | `/v1/credenciais/senha`             | autenticada     | Troca a senha; obrigatória no primeiro acesso                  |
| POST   | `/v1/responsaveis`                  | Admin ou Mestre | Cadastra responsável, sem criar acesso além dele               |
| POST   | `/v1/responsaveis/{id}/vinculos`    | Admin ou Mestre | Vincula Guerreiro(a) ao responsável, com grau de parentesco    |
| GET    | `/v1/eu`                            | autenticada     | Persona, papéis e permissões da sessão                         |
| GET    | `/v1/vitrine/...`                   | pública         | Consultas públicas de vitrine e rankings                       |
| GET    | `/v1/vitrine/guerreiros/{nick}`     | pública         | Perfil público por nick exato, se houver divulgação autorizada |
| GET    | `/v1/vitrine/ods/cobertura`         | pública         | Cobertura de ODS agregada por comunidade e ciclo               |
| GET    | `/v1/auditoria`                     | Admin           | Trilha de auditoria das ações de gestão                        |

As rotas de domínio — território, ledger, trilhas, atividades — estão nos PRDs que as definem
e seguem estas mesmas convenções.

Erros previstos: imagem não reconhecida (401, sem revelar se o nick existe, e com a orientação
de chamar o Mestre); login social ou usuário sem cadastro (403, com orientação de solicitar
participação pela vitrine); senha provisória ainda não trocada (403 em qualquer rota que não
seja a da troca); quarto vínculo de responsável para o mesmo Guerreiro(a) (422); cadastro de
imagem sem consentimento do responsável registrado (422); escrita sem permissão do papel (403);
sessão expirada (401); filtro de comunidade ausente onde é obrigatório (422).

## 10. Requisitos não funcionais

- Sessão do Guerreiro(a) curta o bastante para o aparelho compartilhado e longa o bastante para
  atravessar uma atividade sem reautenticar.
- Conferência da imagem em **poucos segundos**, em aparelho modesto e rede instável — a fila
  na porta da aula é o limite prático, e a confirmação humana é a saída quando ela demora.
- Consulta pública cacheável e tolerante a pico de acesso em dia de culminância.
- Escrita tolerante a rede instável: cliente pode reenviar sem duplicar o registro.
- Armazenamento capaz de guardar **séries temporais com retenção permanente**.
- Documentação das rotas públicas legível por quem não participou do projeto.
- Código aberto, em pt-BR, com mensagens de erro em linguagem simples.

## 11. LGPD e proteção da criança

| Dado                         | Finalidade                        | Base legal                   | Retenção                 | Quem acessa                      |
| ---------------------------- | --------------------------------- | ---------------------------- | ------------------------ | -------------------------------- |
| Nick do Guerreiro(a)         | Identificação pública             | consentimento                | enquanto durar o vínculo | qualquer visitante               |
| _Template_ biométrico        | Presença e autenticação           | consentimento do responsável | enquanto durar o vínculo | ninguém: só a comparação interna |
| Nome e data de nascimento    | Identificação e faixa etária      | consentimento                | enquanto durar o vínculo | gestão e responsável             |
| Conta social do adulto       | Autenticação                      | consentimento                | enquanto durar o vínculo | gestão e o próprio               |
| Usuário e senha do adulto    | Autenticação sem conta social     | consentimento                | enquanto durar o vínculo | o próprio; hash na base          |
| Vínculo e grau de parentesco | Provar quem responde pela criança | consentimento                | enquanto durar o vínculo | gestão e o próprio               |
| Consentimentos versionados   | Prova do que foi autorizado       | obrigação legal              | permanente               | gestão e responsável             |
| Auditoria de escrita         | Rastreabilidade das ações         | interesse público            | permanente               | Admin                            |

- O _template_ é guardado **cifrado**, a senha com **hash**, e nenhuma rota devolve um nem
  outro. A imagem original não é a credencial: o que autentica é o _template_.
- **O _template_ só nasce com o consentimento do responsável.** Até lá — criança que fez o
  onboarding sozinha — o Guerreiro(a) participa igual, e quem abre a sessão dele é o Mestre ou
  um Admin, no encontro. Mesma saída para quem recusa a biometria.
- **Adesão em duas etapas**: o cadastro livre permite participar; a divulgação pública do
  perfil depende de autorização do responsável, registrada como consentimento versionado.
- O responsável consulta, pela App 07, **quem acessou** os dados da criança — a trilha de
  auditoria existe também para isso.
- Nenhuma rota pública devolve imagem real, nome civil ou contato de criança.

## 12. Critérios de aceite e métricas

- Consulta pública de vitrine responde sem token e sem qualquer dado restrito.
- Guerreiro(a) autenticado em um aparelho continua com a sessão do outro Guerreiro(a) encerrada
  ao expirar o tempo, sem vazamento entre sessões.
- Guerreiro(a) entra informando nick e imagem, sem nenhum PIN ou senha em nenhuma tela.
- Imagem não reconhecida devolve 401 sem dizer se o nick existe, e a confirmação do Mestre
  abre a sessão em seguida, com o nome de quem confirmou no registro.
- Nenhuma resposta da API devolve o _template_ biométrico nem a imagem do Guerreiro(a).
- Login social ou usuário sem cadastro é recusado e **nenhuma persona é criada**.
- Adulto com senha provisória só consegue trocar a senha; qualquer outra rota devolve 403.
- Tentativa de vincular um quarto responsável ao mesmo Guerreiro(a) é recusada, e os três
  vínculos existentes continuam válidos, cada um com o seu grau de parentesco.
- Guerreiro(a) sem _template_ não entra sozinho, e entra com a confirmação do Mestre; gravado o
  consentimento do responsável, a imagem é registrada e ele passa a entrar sozinho.
- Requisição de sessão de Guerreiro(a) sem imagem é recusada — não há caminho alternativo por
  senha em nenhuma aplicação.
- Mestre que tenta escrever em rota de gestão recebe 403, e a leitura do painel do dia
  responde normalmente.
- Toda escrita bem-sucedida gera registro de auditoria com autor, papel e data e hora.
- Revogação de consentimento cria novo registro, e o anterior continua consultável.
- Nenhuma rota de crédito de pontos existe para o App 04 — a tentativa devolve 404.

Este PRD não sustenta hipótese própria: ele é a condição para que H1, H2, H3 e H5 sejam
medidas pelas aplicações que as verificam — no caso de H5, por guardar o resultado da sondagem
e o dos desafios de desbloqueio de cada trilha.

## 13. Decisões tomadas neste PRD

| Decisão                                                                                              | Gravada em        | Doc 09       |
| ---------------------------------------------------------------------------------------------------- | ----------------- | ------------ |
| Instância única, com a comunidade como vínculo nos registros                                         | 03 §1             | Já decididos |
| API versionada na rota, a partir de `/v1`                                                            | 03 §1             | Já decididos |
| Guerreiro(a) entra com nick e imagem, conferida contra o _template_ do onboarding                    | 03 §1.1           | Já decididos |
| Sem PIN nem senha para a criança, e sem câmera não há entrada                                        | 03 §§1.1, 3.2     | Já decididos |
| Nick e imagem valem em **todas** as aplicações do Guerreiro(a), para garantir que a atividade é dele | 03 §1.1           | Já decididos |
| Falha, ausência de _template_ ou recusa da biometria caem na confirmação humana, no encontro         | 03 §§1.1, 3.3     | Já decididos |
| App 01 exige câmera e Mestre ou Admin presente; sem isso não há onboarding                           | 03 §3.2           | Já decididos |
| Equipe formada pelo Guerreiro(a) no App 01, vinculada à aula e encerrada com ela                     | 02 §5             | Já decididos |
| Criança sem o responsável: onboarding sem imagem, e cadastro biométrico após a aprovação dele        | 03 §§3.2, 3.3     | Já decididos |
| Mestre cadastra e vincula responsável de qualquer Guerreiro(a)                                       | 02 §1, 03 §11     | Já decididos |
| A imagem do onboarding identifica o Guerreiro(a): presença **e** autenticação                        | 03 §§3.2, 3.3, 12 | Já decididos |
| Adultos entram por login social                                                                      | 03 §1.1           | Já decididos |
| Credencial de usuário e senha provisória, criada por Admin ou Mestre, trocada no primeiro acesso     | 03 §1.1           | Já decididos |
| Responsável tem login próprio, vinculado a um ou mais Guerreiros e Guerreiras                        | 03 §1.1           | Já decididos |
| Responsável é cadastrado por Admin ou Mestre, depois de se apresentar pessoalmente                   | 02 §1             | Já decididos |
| No máximo três responsáveis por Guerreiro(a), com grau de parentesco em texto livre                  | 02 §1             | Já decididos |
| Mestre cadastra responsável pela App 09 — única persona que ele cadastra                             | 03 §11            | Já decididos |
| Mestre lê o painel do dia da App 03 e conduz ali o Quiz ao Vivo das suas aulas                       | 03 §5             | Já decididos |

## 14. Pendências que permanecem

- **Provedor de reconhecimento facial** e o lugar da extração do _template_ (dispositivo ×
  servidor), com o prazo de retenção em números — sabendo que apagar o _template_ apaga
  também a credencial de acesso do Guerreiro(a).
- **Stack do backend**: linguagem, framework e banco de dados, incluindo o armazenamento das
  séries temporais do território. É decisão de implementação e não altera os requisitos.
- **Instituição com mais de um usuário** no mesmo cadastro de Apoiador, e como se registra
  quem agiu em nome dela.
- **Prazo de disponibilidade da versão anterior** da API depois que uma nova abrir.
- **Duração exata da sessão** do Guerreiro(a), a calibrar no primeiro encontro real.
- **Prazo de guarda** do registro de infração e de pontuação negativa, dado sensível de
  criança que hoje segue a retenção geral do vínculo.

## 15. Rastreabilidade

| Requisito               | Origem                                           |
| ----------------------- | ------------------------------------------------ |
| `RF-01-01`, `RF-01-31`  | 03 §1 (API versionada)                           |
| `RF-01-02` e `RF-01-03` | 03 §1 (rotas abertas, escrita autenticada)       |
| `RF-01-04` a `RF-01-08` | 03 §§1.1, 3.2 e 3.3 (nick e imagem, alternativa) |
| `RF-01-09` a `RF-01-12` | 03 §1.1 (como o adulto entra)                    |
| `RF-01-13` a `RF-01-15` | 02 §1 e 03 §§1.1, 5, 9, 11 (responsável)         |
| `RF-01-16` e `RF-01-17` | 03 §§5, 11 (fronteira App 03 × App 09)           |
| `RF-01-18`              | 03 §1 (instância única)                          |
| `RF-01-19`              | 03 §12 (LGPD e consentimentos)                   |
| `RF-01-20` e `RF-01-21` | 02 §§3–5 e 11 §§2, 4–7                           |
| `RF-01-22`              | 11 §8.4 (contrato dos jogos)                     |
| `RF-01-23`              | PRD-08                                           |
| `RF-01-24`              | PRD-07                                           |
| `RF-01-25` e `RF-01-26` | 02 §§1, 4 e 03 §§7, 9–11                         |
| `RF-01-27` a `RF-01-30` | 03 §1 (princípios de arquitetura)                |
| `RF-01-32`              | 03 §§3, 5 (App 01 habilitado pela aula agendada) |
| `RF-01-33` e `RF-01-34` | 02 §1 e 03 §10 (acompanhamento por nick)         |
| `RF-01-35`              | 03 §7 (apoio escolar com corpus fechado)         |
| `RF-01-36`              | 05 §5 e 11 §5 (resposta e pontuação do quiz)     |
| `RF-01-37` a `RF-01-39` | 02 §5 e 05 §5 (equipe formada na aula e quiz)    |
| `RF-01-40` a `RF-01-45` | 11 §2.1 e 04 §4 (etiqueta ODS e cobertura)       |
