# PRD-01 — Backend API (núcleo)

## 1. Identificação

| Campo            | Valor                                                      |
| ---------------- | ---------------------------------------------------------- |
| PRD              | PRD-01                                                     |
| Aplicação        | — (núcleo consumido pelas oito aplicações e por terceiros) |
| Onda             | 1                                                          |
| Situação         | aprovado                                                   |
| Versão e data    | v14 — 2026-08-10                                           |
| Depende de       | PRD-07, PRD-08                                             |
| Documentos-fonte | 02, 03 §§1–3, 5, 8, 9, 11 e 12, 04, 11                     |

## 2. Contexto e objetivo

As oito aplicações não conversam entre si: todas conversam com este núcleo. Ele guarda o
modelo de domínio inteiro — personas, trilhas, atividades, pontos, território, livro-razão —,
decide **quem pode escrever o quê** e serve leitura pública sem login de pessoa — sempre
mediante a chave da aplicação que faz a chamada.

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
- **Chave de aplicação**: emissão, conferência em toda chamada, cota e revogação. Nenhuma
  rota responde sem chave válida, nem as de consulta pública.
- Rotas de consulta públicas — **sem login de pessoa**, com a chave da aplicação — para
  vitrine, rankings e painéis.
- Registro da **solicitação de chave** feita na Área do Apoiador Desenvolvedor, com o prazo de
  30 dias para a apresentação da URL e a revogação automática de quem não apresenta.
- Registro da **solicitação de dados** de pesquisadores e gestores públicos, com a entrega
  liberada apenas após aprovação de Admin e sempre anonimizada.
- Filtro por comunidade em toda consulta, com a plataforma em **instância única**.
- Registro de auditoria de toda escrita: quem, o quê, quando.
- Suporte a aplicações de terceiros sobre as rotas públicas, cada uma com a sua chave.

### 3.2 Fora do escopo

- Interface de qualquer aplicação — cada uma tem o seu PRD.
- Regras de pontuação, cadência de coleta e valoração de aporte: já normatizadas nos
  documentos 11, 02 e 04 e detalhadas nos PRD-08 e PRD-07.
- Captura da imagem, conversa de cadastro e **geração do descritor no aparelho**: são da App 01
  (PRD-04). Aqui ficam a guarda do _template_, a comparação no login e a alternativa para quem
  recusa a biometria.
- **Exclusão do _template_** ao fim do vínculo ou a pedido do responsável: é do PRD-13, que já
  trata dos pedidos do titular. Aqui ficam a guarda, a conferência e o recadastro.
- Telemetria da Batalha de Laser (PRD-10) e personalização por IA (PRD-11).

## 4. Personas e permissões

| Persona      | Escreve                                                                                                                                                                                                                                                                                                                                                  | Lê                                                                       |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Admin        | Tudo: cadastros, aprovações, lançamentos, ledger, comunidades                                                                                                                                                                                                                                                                                            | Tudo                                                                     |
| Mestre       | Suas trilhas e conteúdos, lançamentos e pontuação negativa das suas atividades, condução do Quiz ao Vivo das suas aulas, auditoria de coleta, aprovação de local, aportes seus, cadastro de responsável e vínculo com Guerreiros e Guerreiras, confirmação de identidade do Guerreiro(a), cadastro biométrico dele e **homologação da equipe da trilha** | O que é público, suas turmas e o **painel do dia** na App 03, em leitura |
| Guerreiro(a) | Seus registros de coleta, suas criações, suas sugestões, recompensas recebidas nos marcos, as **equipes que forma — a da aula e a da trilha** — e a resposta de quiz da equipe                                                                                                                                                                           | Seus dados, as equipes da aula em andamento e o que é público            |
| Responsável  | Consentimentos, autorizações, solicitações e propostas                                                                                                                                                                                                                                                                                                   | Os Guerreiros e Guerreiras sob sua responsabilidade e o que é público    |
| Apoiador     | Aportes declarados, cobertura de missão, propostas de desafio extra, documentos comprobatórios, propostas de evolução                                                                                                                                                                                                                                    | Seus aportes, efetividade agregada e o que é público                     |
| Visitante    | Solicitação de participação, de dados e de chave, pelas rotas públicas da vitrine                                                                                                                                                                                                                                                                        | Somente o que é público                                                  |

Regra geral: **leitura pública dispensa login de pessoa, nunca a chave da aplicação; escrita
é sempre autenticada e auditada.**

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

1. Qualquer consulta pública responde **sem login de pessoa**: vitrine, rankings, painéis de
   comunidade e prestação de contas.
2. A chamada chega com a **chave da aplicação** que a fez — a vitrine e o jogo carregam a sua,
   emitida na implantação. **Sem chave válida o núcleo responde 401**, e o visitante segue
   anônimo em qualquer dos casos.
3. A resposta pública nunca traz dado de contato, imagem real de criança, valor em reais nem
   granularidade de território abaixo de rua.

### 5.5 Terceiro constrói sobre a API

1. O interessado pede a chave na **Área do Apoiador Desenvolvedor**, na vitrine (PRD-03).
2. Um Admin avalia o pedido na App 03 (PRD-02); aprovado, o núcleo **emite a chave** e devolve
   o segredo uma única vez, com o prazo de apresentação já contado.
3. A aplicação de terceiro consome as rotas públicas de `/v1` **apresentando a chave em toda
   chamada**; sem ela, 401.
4. O solicitante tem **30 dias para apresentar a URL** do jogo ou da aplicação construída.
   Apresentada, a chave passa a vigente por prazo indeterminado e a aplicação fica apta a ser
   homologada como aporte em código.
5. **Vencido o prazo sem URL, o núcleo revoga a chave** — a chamada seguinte recebe 401 — e o
   interessado pode solicitar outra a qualquer tempo.
6. Chave revogada não desfaz nada: como o terceiro só lê, não há escrita a reverter.
7. Mudança que quebre contrato abre `/v2`, e `/v1` segue no ar por prazo declarado.

## 6. Requisitos funcionais

| ID         | Requisito                                                                                                                                                                                       | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `RF-01-01` | Núcleo expõe todas as rotas sob prefixo de versão, começando em `/v1`                                                                                                                           | essencial  |
| `RF-01-02` | Rotas de consulta pública respondem **sem login de pessoa**, mediante chave da aplicação                                                                                                        | essencial  |
| `RF-01-03` | Toda rota de escrita exige autenticação e registra autoria, data e hora                                                                                                                         | essencial  |
| `RF-01-04` | Guerreiro(a) autentica com nick e imagem e recebe sessão de duração curta                                                                                                                       | essencial  |
| `RF-01-05` | Núcleo recebe o descritor gerado no aparelho, guarda o _template_ cifrado e o confere no login, sem devolvê-lo                                                                                  | essencial  |
| `RF-01-06` | Mestre ou Admin confirma a identidade do Guerreiro(a) e abre a sessão dele quando não há _template_ gravado, o reconhecimento falha ou a biometria foi recusada, com registro de quem confirmou | essencial  |
| `RF-01-07` | Núcleo grava o _template_ do Guerreiro(a) cadastrado sem imagem assim que o responsável aprova a participação                                                                                   | essencial  |
| `RF-01-08` | Mestre ou Admin recadastra a imagem de referência do Guerreiro(a), com registro de quem recadastrou                                                                                             | essencial  |
| `RF-01-09` | Adulto autentica por login social vinculado a cadastro existente                                                                                                                                | essencial  |
| `RF-01-10` | Login social ou usuário sem cadastro correspondente é recusado, sem criar persona                                                                                                               | essencial  |
| `RF-01-61` | Núcleo semeia na implantação a persona Admin do fundador, com a identidade social declarada, sem passar por outro Admin                                                                         | essencial  |
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
| `RF-01-62` | Núcleo mantém o catálogo de poderes, cadastrado por Admin, a que a trilha se vincula                                                                                                            | essencial  |
| `RF-01-21` | Núcleo mantém pontos, níveis e badges por trilha ou poder, derivados das realizações                                                                                                            | essencial  |
| `RF-01-22` | Núcleo expõe aos jogos **apenas leitura** de progresso, sem nenhuma rota de escrita — crédito, débito ou resultado de partida                                                                   | essencial  |
| `RF-01-56` | Núcleo mantém o ponto extra em duas contas: acumulado, que só cresce, e saldo disponível, que debita na troca                                                                                   | essencial  |
| `RF-01-57` | Núcleo nunca debita ponto regular, em nenhuma operação                                                                                                                                          | essencial  |
| `RF-01-58` | Núcleo recusa troca que deixaria o saldo disponível negativo                                                                                                                                    | essencial  |
| `RF-01-59` | Núcleo expõe aos jogos o acumulado de pontos extras, nunca o saldo disponível                                                                                                                   | essencial  |
| `RF-01-60` | Núcleo mantém o catálogo avulso e as trocas definidos no PRD-07                                                                                                                                 | essencial  |
| `RF-01-23` | Núcleo mantém as entidades do território definidas no PRD-08                                                                                                                                    | essencial  |
| `RF-01-24` | Núcleo mantém as entidades do livro-razão definidas no PRD-07                                                                                                                                   | essencial  |
| `RF-01-25` | Núcleo mantém solicitação de participação, sugestões e propostas em fila única de avaliação                                                                                                     | essencial  |
| `RF-01-26` | Núcleo mantém criação original com autoria creditada por toda a vida do registro                                                                                                                | essencial  |
| `RF-01-46` | Núcleo mantém a solicitação de dados de pesquisador ou gestor público, com finalidade declarada e desfecho                                                                                      | essencial  |
| `RF-01-47` | Núcleo só libera o conjunto de dados depois da aprovação de um Admin, sempre anonimizado                                                                                                        | essencial  |
| `RF-01-66` | Núcleo exporta o conjunto aprovado em CSV para as séries, GeoJSON para a geometria e um dicionário de dados com campo, unidade, cadência e origem                                               | essencial  |
| `RF-01-48` | Núcleo recusa com 401 toda chamada sem chave de aplicação válida, inclusive nas rotas de consulta pública                                                                                       | essencial  |
| `RF-01-49` | Núcleo registra a solicitação de chave feita na Área do Apoiador Desenvolvedor, com solicitante, o que pretende construir e situação                                                            | essencial  |
| `RF-01-50` | Núcleo emite a chave após aprovação de Admin e devolve o segredo uma única vez, guardando apenas o seu resumo criptográfico                                                                     | essencial  |
| `RF-01-51` | Núcleo conta 30 dias da emissão para a apresentação da URL e registra a URL apresentada                                                                                                         | essencial  |
| `RF-01-52` | Núcleo revoga automaticamente a chave cujo prazo de apresentação vence sem URL                                                                                                                  | essencial  |
| `RF-01-53` | Núcleo permite a um Admin revogar chave a qualquer tempo, com motivo e autoria registrados                                                                                                      | essencial  |
| `RF-01-54` | Núcleo emite na implantação uma chave por aplicação do próprio projeto e por ambiente, sem prazo de apresentação                                                                                | essencial  |
| `RF-01-55` | Núcleo aplica às chamadas de leitura a cota da faixa da chave — do projeto ou de terceiro — e responde 429 ao excedê-la                                                                         | desejável  |
| `RF-01-65` | Núcleo freia por origem a consulta por nick e o envio dos formulários de participação e de dados, com atraso progressivo, e agrupa a origem por resumo do IP mantido só em memória              | essencial  |
| `RF-01-35` | Núcleo mantém as entidades do apoio escolar — disciplina, conteúdo do corpus e consulta                                                                                                         | essencial  |
| `RF-01-36` | Núcleo mantém a resposta de quiz por equipe e pergunta, com o momento de chegada                                                                                                                | essencial  |
| `RF-01-37` | Equipe da aula é criada pelo Guerreiro(a), vinculada a uma aula, e encerra com ela sem ser reaproveitada                                                                                        | essencial  |
| `RF-01-63` | Equipe da trilha é formada pelos Guerreiros e Guerreiras e homologada pelo Mestre em encontro presencial, e a composição fica fixa a partir da homologação                                      | essencial  |
| `RF-01-64` | Núcleo credita a criação original a cada integrante da equipe da trilha que a entregou, guardando o papel de cada um                                                                            | essencial  |
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

| ID         | Regra                                                                                                                               | Invariante | Fonte       |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------- | ---------- | ----------- |
| `RN-01-01` | Só o Guerreiro(a) tem autocadastro; Mestre e Apoiador são cadastrados por Admin, e o responsável por Admin ou Mestre                | 3          | 02 §1       |
| `RN-01-02` | Novo Admin só entra por inclusão manual de outro Admin                                                                              | 3          | 02 §1       |
| `RN-01-03` | Solicitação de participação não cria cadastro nem acesso                                                                            | 3          | 02 §1       |
| `RN-01-04` | Login não cria persona: autentica quem já tem cadastro                                                                              | 3          | 03 §1.1     |
| `RN-01-05` | Todo Guerreiro(a) tem vínculo obrigatório a exatamente uma comunidade                                                               | 4          | 02 §1       |
| `RN-01-06` | Pontos só vêm de realização; o App 04 apenas lê e não tem nenhuma rota de escrita                                                   | 8          | 11 §§1, 8.4 |
| `RN-01-07` | Nenhuma atividade é agendável sem lastro dos recursos                                                                               | 9          | 04 §1       |
| `RN-01-08` | Dado do território tem guarda permanente com coletor identificado                                                                   | 7          | 02 §1       |
| `RN-01-09` | Anonimização se aplica na saída, nunca no armazenamento                                                                             | 7          | 02 §1       |
| `RN-01-10` | Guerreiro(a) aparece publicamente só por avatar e nick, e só com autorização do responsável                                         | 12         | 03 §12      |
| `RN-01-11` | Rota pública nunca devolve dado de contato, valor em reais ou imagem real de criança                                                | 10, 16     | 03 §12      |
| `RN-01-12` | Consentimento é versionado, com autoria, data e hora                                                                                | 11         | 03 §12      |
| `RN-01-13` | Criação original carrega o autor por toda a vida do registro                                                                        | 5          | 02 §4       |
| `RN-01-14` | O _template_ biométrico é guardado cifrado, com acesso auditado, e nenhuma rota o devolve nem devolve a imagem original             | 12         | 03 §3.3     |
| `RN-01-15` | A imagem do Guerreiro(a) serve só para identificá-lo — presença e autenticação; outro uso exige nova base legal                     | 12         | 03 §3.3     |
| `RN-01-16` | Recusar a biometria não impede o acesso: a confirmação do Mestre ou Admin, no encontro, é a alternativa equivalente                 | 11         | 03 §3.3     |
| `RN-01-17` | O _template_ só é gravado com consentimento do responsável registrado                                                               | 11         | 03 §3.3     |
| `RN-01-18` | Senha provisória é guardada com hash, vale para um único acesso e é trocada pelo próprio adulto                                     | —          | 03 §1.1     |
| `RN-01-19` | Cada Guerreiro(a) tem no máximo três responsáveis vinculados, com grau de parentesco em texto livre                                 | 3          | 02 §1       |
| `RN-01-20` | Responsável só é vinculado a Guerreiro(a) já cadastrado no onboarding                                                               | 3          | 02 §1       |
| `RN-01-21` | Recusa de consentimento nunca exclui o Guerreiro(a) da atividade                                                                    | 11         | 03 §12      |
| `RN-01-22` | O nick é chave de acompanhamento público, cedido pela família: o núcleo nunca o descobre nem o sugere a um adulto                   | 12         | 02 §1       |
| `RN-01-23` | A etiqueta ODS não entra em ponto, nível ou badge; é opcional no Ciclo 01 e obrigatória na trilha a partir do Ciclo 02              | 20         | 11 §2.1     |
| `RN-01-50` | O badge de protagonismo é o único global; todos os demais se vinculam a uma trilha ou a um poder                                    | —          | 11 §7       |
| `RN-01-24` | A cobertura de ODS nunca é atributo de um Guerreiro(a): agrega por trilha, poder, comunidade e ciclo                                | 20         | 11 §2.1     |
| `RN-01-25` | Solicitação de dados não cria cadastro nem acesso, e a entrega exige aprovação registrada de Admin                                  | 17         | 03 §12.3    |
| `RN-01-26` | Saída pública agrega até o bairro; rua e abaixo só na entrega aprovada por Admin                                                    | 7, 17      | 02 §1       |
| `RN-01-47` | O conjunto entregue é licenciado em CC BY-SA, com crédito à comunidade que produziu o dado                                          | 17         | 03 §12.3    |
| `RN-01-49` | Solicitação de dados responde no mesmo prazo de 7 dias de toda solicitação da plataforma                                            | —          | 03 §12.3    |
| `RN-01-48` | Admin aprova com solicitante identificado, finalidade declarada e compromisso de não reidentificação, e registra o motivo da recusa | 17         | 03 §12.3    |
| `RN-01-27` | Rota pública tem limite por origem e janela, com atraso progressivo, sem exigir cadastro do visitante                               | —          | 03 §8       |
| `RN-01-45` | A origem do freio nunca é gravada: agrupa-se por resumo do IP, mantido só pela janela e em memória                                  | —          | 03 §8       |
| `RN-01-46` | Solicitação de chave não tem freio por origem, porque nova solicitação é sempre possível                                            | —          | 03 §8       |
| `RN-01-28` | Pré-cadastro de Apoiador não cria cadastro nem acesso: quem valida o comprovante e cadastra é um Admin                              | 3          | 02 §1       |
| `RN-01-29` | A plataforma não coleta CPF, CNPJ nem documento de identidade de quem aporta                                                        | —          | 02 §1       |
| `RN-01-30` | O nick do Apoiador é único em toda a plataforma, como o do Guerreiro(a)                                                             | —          | 02 §1       |
| `RN-01-31` | Aporte declarado só credita moedas e vai ao card público depois de homologado por Admin                                             | 16         | 04 §2       |
| `RN-01-32` | Sem chave válida nenhuma rota de dados sob `/v1` responde, nem em consulta pública; o schema OpenAPI, fora do prefixo, é aberto     | —          | 03 §1       |
| `RN-01-33` | A chave é da aplicação, nunca da pessoa: ela não identifica nem autoriza visitante algum                                            | 8          | 03 §1.1     |
| `RN-01-34` | Chave não amplia direito: quem só lê continua só lendo, e escrita segue exigindo credencial de persona                              | 8          | 03 §1       |
| `RN-01-35` | O segredo da chave é devolvido uma única vez e nunca é recuperável depois                                                           | —          | 03 §1       |
| `RN-01-36` | Chave de terceiro sem URL apresentada em 30 dias é revogada, e nova solicitação é sempre possível                                   | —          | 03 §8       |
| `RN-01-37` | Solicitação de chave não cria cadastro nem persona, como as demais solicitações públicas                                            | 3          | 02 §1       |
| `RN-01-38` | Ponto regular nunca se gasta; só o saldo de pontos extras é debitado                                                                | 23         | 11 §5       |
| `RN-01-39` | O acumulado de pontos extras só cresce; a troca debita apenas o saldo disponível                                                    | 23         | 11 §5       |
| `RN-01-40` | O saldo disponível nunca fica negativo                                                                                              | 23         | 11 §5       |
| `RN-01-41` | Nenhuma rota de jogo expõe o saldo disponível de pontos extras                                                                      | 8          | 11 §§5, 8.4 |
| `RN-01-42` | A trilha é bem comum da plataforma: não se vincula a comunidade, e o filtro por comunidade recai sobre o percurso, não sobre ela    | —          | 02 §3       |
| `RN-01-43` | O poder é cadastrado por Admin, e só poder de Guerreiro(a) recebe trilha                                                            | 21         | 02 §2       |
| `RN-01-44` | A equipe da trilha é uma por trilha percorrida e, homologada pelo Mestre, não recebe nem perde integrante                           | 15         | 02 §5       |

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
                    SolicitacaoDeDados         Local                Aporte
                    SolicitacaoDeChave         SerieDeColeta        Lancamento
                    SolicitacaoDoResponsavel   RegistroDeColeta     ItemPatrimonial
                                                                    ItemDeCatalogoAvulso
                                                                    Troca
                    SugestaoOuProposta
                    Favorito                   APOIO (PRD-14)
                    ChaveDeAplicacao           MissaoDoApoiador
                    Auditoria                  SeloDoApoiador

                    APOIO ESCOLAR (PRD-05)     BATALHA (PRD-10)
                    DisciplinaDeApoio          ArtefatoDeBatalha
                    ConteudoDeApoio            PartidaDeBatalha
                    ConsultaDeApoio            ParticipacaoNaPartida
                                               EventoDeTelemetria
                                               ConferenciaDeSeguranca
```

| Entidade                    | Atributos essenciais                                                                                                                                                                                                                                       |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Credencial`                | persona, tipo (biometria, login social, usuário e senha), identificador, segredo (_template_ cifrado ou hash), criada por, troca pendente, ativa                                                                                                           |
| `Sessao`                    | persona, início, expiração, origem (aplicação), como autenticou, quem confirmou, encerrada em                                                                                                                                                              |
| `VinculoResponsavel`        | responsável, Guerreiro(a), grau de parentesco, cadastrado por (Admin ou Mestre), início, fim                                                                                                                                                               |
| `Consentimento`             | responsável, Guerreiro(a), tipo, versão do termo, decisão, data e hora, testemunha (Mestre ou Admin), anexo do termo assinado, origem (própria, assistida ou impressa), quem operou                                                                        |
| `SolicitacaoDoResponsavel`  | protocolo, responsável, Guerreiro(a), tipo, texto, situação, prazo, quem tratou, desfecho e data                                                                                                                                                           |
| `SolicitacaoDeDados`        | solicitante, instituição, e-mail, finalidade declarada, recorte pedido, situação, prazo, quem avaliou, desfecho, data e o que foi entregue                                                                                                                 |
| `SolicitacaoDeChave`        | solicitante, e-mail, instituição opcional, o que pretende construir, situação, prazo de avaliação, quem avaliou, parecer, data e a chave emitida                                                                                                           |
| `ChaveDeAplicacao`          | aplicação, ambiente, natureza (do projeto ou de terceiro), resumo criptográfico do segredo, emitida por, emitida em, prazo de apresentação, URL apresentada, cota, situação (vigente, revogada), revogada por, motivo e data                               |
| `EtiquetaODS`               | trilha ou missão, objetivo (1 a 18), meta opcional (`4.7`, `13.3`, `17.18`), declarada por, data                                                                                                                                                           |
| `Equipe`                    | vínculo — aula **ou** trilha, nunca os dois —, criada por, integrantes com o papel de cada um, e, na equipe da trilha, quem homologou e quando                                                                                                             |
| `SolicitacaoDeParticipacao` | nome ou razão social, e-mail, WhatsApp, pretensão, apresentação, instituição e links opcionais, aporte declarado (necessidade, valor sugerido ou livre), comprovante anexado, situação, prazo, quem avaliou, parecer, data                                 |
| `SugestaoOuProposta`        | autor e persona, alvo (atividade, trilha ou plataforma), texto — a transcrição, quando o registro veio em áudio —, situação (recebida, em avaliação, adotada, não adotada), prazo, quem avaliou, motivo do retorno em linguagem simples e data do desfecho |
| `Apoiador`                  | identidade, avatar (próprio a partir de 10 moedas acumuladas; padrão do projeto abaixo do piso), nick único, artefatos comprobatórios, Poder Sustentador derivado dos aportes homologados                                                                  |
| `Auditoria`                 | autor, papel, ação, entidade afetada, data e hora, origem                                                                                                                                                                                                  |

A `Aula/Agenda` carrega **comunidade, data, horário inicial e final**: é dela que o App 01 tira
a comunidade do novo cadastro, e é a existência dela que habilita o onboarding naquele momento.
Não há parâmetro de liberação separado.

A `Equipe` tem **dois tempos de vida**, definidos no documento 02 §5: a da aula, que termina com
ela, e a da trilha, fixa depois de homologada e sujeito da criação original. É a mesma entidade,
com o vínculo declarando qual das duas ela é.

`DesafioExtra`, `Favorito`, `MissaoDoApoiador` e `SeloDoApoiador` são do Apoiador e têm os
atributos definidos no PRD-14. `Favorito` existe **apenas na App 08**, e nenhuma outra aplicação
guarda preferência de quem lê. **`MissaoDoApoiador` não é `Missao`**: aquela é o chamado de
sustento dirigido ao adulto, esta é a unidade de progressão da trilha do Guerreiro(a) — as duas
convivem no domínio e nunca se substituem. O **nível de sustento é derivado** das missões
concluídas, como o Poder Sustentador é derivado dos aportes; nenhum dos dois é armazenado.

`Conteudo`, `BibliografiaDaMissao`, `Culminancia`, `RecompensaDeMarco` e `SugestaoDeEstrutura`
entram pela autoria de trilha e têm os
atributos definidos no PRD-09. A `Culminancia` é o que torna verificável a regra de que toda
trilha termina em criação original: sem ela, a trilha não é publicável.

A `Batalha`, que aqui só existia como nome no bloco de operação, tem os atributos definidos no
PRD-10, junto com as entidades da partida. Nenhuma delas abre exceção ao contrato dos jogos: a
partida física **lança atividade realizada**, e é a atividade que credita pontos.

Imutabilidade: `Consentimento` e `Auditoria` são **somente inserção**. Revogação é um novo
registro, não a edição do anterior — é o que permite responder "o que valia naquela data".

## 9. Contratos de API

Convenções válidas para todas as rotas:

| Aspecto      | Definição                                                               |
| ------------ | ----------------------------------------------------------------------- |
| Versão       | prefixo `/v1` em toda rota                                              |
| Chave        | **obrigatória em toda rota**, inclusive nas públicas; sem ela, 401      |
| Autenticação | token de sessão no cabeçalho; ausência dele só é aceita em rota pública |
| Erro         | corpo único com código, mensagem em linguagem simples e campo em falta  |
| Listagem     | paginada, com filtros de comunidade, período e persona                  |
| Data e hora  | sempre com fuso, e a data do fato nunca é substituída pela do registro  |

| Método | Rota                                | Autenticação    | Descrição                                                            |
| ------ | ----------------------------------- | --------------- | -------------------------------------------------------------------- |
| POST   | `/v1/sessoes/guerreiro`             | pública         | Autentica com nick e imagem e abre sessão curta                      |
| POST   | `/v1/sessoes/guerreiro/confirmacao` | Mestre ou Admin | Abre a sessão do Guerreiro(a) por confirmação humana                 |
| POST   | `/v1/sessoes/social`                | pública         | Autentica adulto por login social                                    |
| POST   | `/v1/sessoes/credencial`            | pública         | Autentica adulto por usuário e senha                                 |
| DELETE | `/v1/sessoes/atual`                 | autenticada     | Encerra a sessão                                                     |
| POST   | `/v1/guerreiros/{id}/descritor`     | Mestre ou Admin | Grava ou recadastra o _template_ a partir do descritor, com registro |
| POST   | `/v1/credenciais`                   | Admin ou Mestre | Cria credencial de usuário e senha provisória                        |
| POST   | `/v1/credenciais/senha`             | autenticada     | Troca a senha; obrigatória no primeiro acesso                        |
| POST   | `/v1/responsaveis`                  | Admin ou Mestre | Cadastra responsável, sem criar acesso além dele                     |
| POST   | `/v1/responsaveis/{id}/vinculos`    | Admin ou Mestre | Vincula Guerreiro(a) ao responsável, com grau de parentesco          |
| GET    | `/v1/eu`                            | autenticada     | Persona, papéis e permissões da sessão                               |
| GET    | `/v1/vitrine/...`                   | pública         | Consultas públicas de vitrine e rankings                             |
| GET    | `/v1/vitrine/guerreiros/{nick}`     | pública         | Perfil público por nick exato, se houver divulgação autorizada       |
| GET    | `/v1/vitrine/ods/cobertura`         | pública         | Cobertura de ODS agregada por comunidade e ciclo                     |
| POST   | `/v1/solicitacoes-de-dados`         | pública         | Registra pedido do conjunto de dados, sem criar cadastro             |
| POST   | `/v1/solicitacoes-de-participacao`  | pública         | Registra o pedido; do Apoiador, com aporte e comprovante             |
| PUT    | `/v1/eu/apoiador/identidade`        | Apoiador        | Define ou troca o nick e, acima do piso de moedas, o avatar          |
| GET    | `/v1/auditoria`                     | Admin           | Trilha de auditoria das ações de gestão                              |
| POST   | `/v1/solicitacoes-de-chave`         | pública         | Registra pedido de chave feito na Área do Apoiador Desenvolvedor     |
| POST   | `/v1/chaves`                        | Admin           | Emite a chave da solicitação aprovada e devolve o segredo uma vez    |
| POST   | `/v1/chaves/{id}/url`               | pública         | Apresenta a URL do que foi construído, dentro dos 30 dias            |
| DELETE | `/v1/chaves/{id}`                   | Admin           | Revoga a chave, com motivo e autoria                                 |
| GET    | `/v1/chaves`                        | Admin           | Chaves emitidas, com prazo, URL apresentada e situação               |

**"Pública" nesta coluna significa "sem credencial de persona"** — a chave da aplicação
continua obrigatória em todas elas. Nenhuma rota deste PRD responde sem chave válida.

As rotas de domínio — território, ledger, trilhas, atividades — estão nos PRDs que as definem
e seguem estas mesmas convenções, chave incluída.

Erros previstos: chave ausente, inválida ou revogada (**401**, sem detalhar qual dos três
ocorreu); imagem não reconhecida (401, sem revelar se o nick existe, e com a orientação
de chamar o Mestre); login social ou usuário sem cadastro (403, com orientação de solicitar
participação pela vitrine); senha provisória ainda não trocada (403 em qualquer rota que não
seja a da troca); quarto vínculo de responsável para o mesmo Guerreiro(a) (422); cadastro de
imagem sem consentimento do responsável registrado (422); escrita sem permissão do papel (403);
sessão expirada (401); filtro de comunidade ausente onde é obrigatório (422); apresentação de
URL depois de vencido o prazo (422, com a orientação de solicitar nova chave); excesso de
consultas ou de envios na rota pública (429, com o tempo de espera).

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

| Dado                         | Finalidade                          | Base legal                   | Retenção                 | Quem acessa                      |
| ---------------------------- | ----------------------------------- | ---------------------------- | ------------------------ | -------------------------------- |
| Nick do Guerreiro(a)         | Identificação pública               | consentimento                | enquanto durar o vínculo | qualquer visitante               |
| _Template_ biométrico        | Presença e autenticação             | consentimento do responsável | enquanto durar o vínculo | ninguém: só a comparação interna |
| Nome e data de nascimento    | Identificação e faixa etária        | consentimento                | enquanto durar o vínculo | gestão e responsável             |
| Conta social do adulto       | Autenticação                        | consentimento                | enquanto durar o vínculo | gestão e o próprio               |
| Usuário e senha do adulto    | Autenticação sem conta social       | consentimento                | enquanto durar o vínculo | o próprio; hash na base          |
| Vínculo e grau de parentesco | Provar quem responde pela criança   | consentimento                | enquanto durar o vínculo | gestão e o próprio               |
| Consentimentos versionados   | Prova do que foi autorizado         | obrigação legal              | permanente               | gestão e responsável             |
| Auditoria de escrita         | Rastreabilidade das ações           | interesse público            | permanente               | Admin                            |
| Acesso ao _template_         | Rastreabilidade do uso da biometria | interesse público            | permanente               | Admin                            |

- O _template_ é guardado **cifrado**, a senha com **hash**, e nenhuma rota devolve um nem
  outro. A imagem original não é a credencial: o que autentica é o _template_. Ela tampouco
  **chega ao núcleo** — o descritor é gerado no aparelho (PRD-04).
- **O _template_ só nasce com o consentimento do responsável.** Até lá — criança que fez o
  onboarding sozinha — o Guerreiro(a) participa igual, e quem abre a sessão dele é o Mestre ou
  um Admin, no encontro. Mesma saída para quem recusa a biometria.
- **Adesão em duas etapas**: o cadastro livre permite participar; a divulgação pública do
  perfil depende de autorização do responsável, registrada como consentimento versionado.
- O responsável consulta, pela App 07, **quem acessou** os dados da criança — a trilha de
  auditoria existe também para isso.
- Nenhuma rota pública devolve imagem real, nome civil ou contato de criança.

## 12. Critérios de aceite e métricas

- Consulta pública de vitrine responde **sem token de sessão** e sem qualquer dado restrito,
  desde que a chamada traga chave de aplicação válida.
- A mesma consulta **sem chave** devolve 401, e a resposta não diferencia chave ausente,
  inválida e revogada.
- Chave emitida devolve o segredo **uma única vez**; uma segunda leitura da mesma chave não o
  recupera, e a base guarda apenas o resumo criptográfico.
- Chave de terceiro cujo prazo de 30 dias vence sem URL apresentada passa a devolver 401 na
  chamada seguinte, sem intervenção humana.
- URL apresentada dentro do prazo mantém a chave vigente e fica registrada com data e hora.
- Chave revogada por Admin registra motivo e autoria, e a aplicação perde o acesso na chamada
  seguinte.
- Guerreiro(a) autenticado em um aparelho continua com a sessão do outro Guerreiro(a) encerrada
  ao expirar o tempo, sem vazamento entre sessões.
- Guerreiro(a) entra informando nick e imagem, sem nenhum PIN ou senha em nenhuma tela.
- Imagem não reconhecida devolve 401 sem dizer se o nick existe, e a confirmação do Mestre
  abre a sessão em seguida, com o nome de quem confirmou no registro.
- Nenhuma resposta da API devolve o _template_ biométrico nem a imagem do Guerreiro(a).
- Nenhuma rota do núcleo aceita imagem de Guerreiro(a): a gravação do _template_ recebe
  descritor, e o envio de imagem é recusado.
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
- Equipe da trilha homologada recusa entrada e saída de integrante, e a composição registrada
  na homologação é a que credita a criação original.
- Segundo pedido de equipe da trilha para o mesmo Guerreiro(a) na mesma trilha é recusado.
- Criação original validada credita cada integrante da equipe da trilha, e o registro guarda o
  papel de cada um.
- Toda escrita bem-sucedida gera registro de auditoria com autor, papel e data e hora.
- Revogação de consentimento cria novo registro, e o anterior continua consultável.
- Nenhuma rota de crédito de pontos existe para o App 04 — a tentativa devolve 404.

Este PRD não sustenta hipótese própria: ele é a condição para que H1, H2, H3 e H5 sejam
medidas pelas aplicações que as verificam — no caso de H5, por guardar o resultado da sondagem
e o dos desafios de desbloqueio de cada trilha.

## 13. Decisões tomadas neste PRD

| Decisão                                                                                              | Gravada em        | Doc 09                                       |
| ---------------------------------------------------------------------------------------------------- | ----------------- | -------------------------------------------- |
| Instância única, com a comunidade como vínculo nos registros                                         | 03 §1             | Já decididos                                 |
| API versionada na rota, a partir de `/v1`                                                            | 03 §1             | Já decididos                                 |
| Guerreiro(a) entra com nick e imagem, conferida contra o _template_ do onboarding                    | 03 §1.1           | Já decididos                                 |
| Sem PIN nem senha para a criança, e sem câmera não há entrada                                        | 03 §§1.1, 3.2     | Já decididos                                 |
| Nick e imagem valem em **todas** as aplicações do Guerreiro(a), para garantir que a atividade é dele | 03 §1.1           | Já decididos                                 |
| Falha, ausência de _template_ ou recusa da biometria caem na confirmação humana, no encontro         | 03 §§1.1, 3.3     | Já decididos                                 |
| App 01 exige câmera e Mestre ou Admin presente; sem isso não há onboarding                           | 03 §3.2           | Já decididos                                 |
| Equipe formada pelo Guerreiro(a) no App 01, vinculada à aula e encerrada com ela                     | 02 §5             | Já decididos                                 |
| Criança sem o responsável: onboarding sem imagem, e cadastro biométrico após a aprovação dele        | 03 §§3.2, 3.3     | Já decididos                                 |
| Mestre cadastra e vincula responsável de qualquer Guerreiro(a)                                       | 02 §1, 03 §11     | Já decididos                                 |
| A imagem do onboarding identifica o Guerreiro(a): presença **e** autenticação                        | 03 §§3.2, 3.3, 12 | Já decididos                                 |
| Admin fundador semeado na implantação, único cadastro que não passa por outro Admin                  | 02 §1             | Semeadura do primeiro Admin                  |
| Adultos entram por login social                                                                      | 03 §1.1           | Já decididos                                 |
| Credencial de usuário e senha provisória, criada por Admin ou Mestre, trocada no primeiro acesso     | 03 §1.1           | Já decididos                                 |
| Responsável tem login próprio, vinculado a um ou mais Guerreiros e Guerreiras                        | 03 §1.1           | Já decididos                                 |
| Responsável é cadastrado por Admin ou Mestre, depois de se apresentar pessoalmente                   | 02 §1             | Já decididos                                 |
| No máximo três responsáveis por Guerreiro(a), com grau de parentesco em texto livre                  | 02 §1             | Já decididos                                 |
| Mestre cadastra responsável pela App 09 — única persona que ele cadastra                             | 03 §11            | Já decididos                                 |
| Mestre lê o painel do dia da App 03 e conduz ali o Quiz ao Vivo das suas aulas                       | 03 §5             | Já decididos                                 |
| Toda aplicação se identifica por chave, e sem ela a API não responde                                 | 03 §1             | Já decididos                                 |
| A chave é da aplicação, não da pessoa: consulta pública dispensa login, nunca a chave                | 03 §§1, 1.1       | Já decididos                                 |
| Chave de terceiro pedida na Área do Apoiador Desenvolvedor, com 30 dias para a URL                   | 03 §8             | Já decididos                                 |
| Chave sem URL apresentada no prazo é revogada                                                        | 03 §8             | Já decididos                                 |
| Stack: Python com FastAPI, Cloud SQL para PostgreSQL com PostGIS e Cloud Storage                     | 03 §1             | Já decididos                                 |
| Hospedagem em Cloud Run, região `southamerica-east1`, custo por absorção do fundador                 | 03 §1             | Já decididos                                 |
| Séries temporais do território no próprio PostgreSQL, particionadas por tempo                        | 03 §1             | Já decididos                                 |
| _Template_ biométrico gerado no aparelho; ao núcleo chega só o descritor                             | 03 §3.3           | Já decididos                                 |
| Ponto extra em duas contas: acumulado e saldo disponível; só o saldo debita                          | 11 §5             | Troca de pontos extras por recompensa avulsa |
| Jogos leem o acumulado de pontos extras, nunca o saldo disponível                                    | 11 §5             | Troca de pontos extras por recompensa avulsa |
| Comparação do _template_ permanece no núcleo, que nunca o devolve                                    | 03 §3.3           | Já decididos                                 |
| Chave que cifra o _template_ no Secret Manager, lida na subida, sem chamada externa por login        | 03 §3.3           | Guarda e auditoria do _template_ biométrico  |
| Acesso auditado ao _template_ alcança toda leitura, inclusive cada comparação de login               | 03 §3.3           | Guarda e auditoria do _template_ biométrico  |
| Duração da sessão do Guerreiro(a) e limiar da biometria são parâmetro declarado na implantação       | 03 §§3.2, 3.3     | Parâmetros da entrada do Guerreiro(a)        |
| API documentada em OpenAPI desde o primeiro _endpoint_, com schema aberto fora de `/v1`              | 03 §§1, 1.1       | Documentação da API em OpenAPI               |
| Chave por aplicação e por ambiente; dois ambientes no Ciclo 01, e 16 chaves na implantação           | 03 §§1, 1.13      | Escopo da chave e ambientes do Ciclo 01      |
| Python 3.12 e conjunto de regras do Ruff, com cobertura medida sem limiar que bloqueie               | 03 §1.13          | Ferramentas da esteira de CI do backend      |
| Trilha é bem comum da plataforma; o filtro por comunidade recai sobre o percurso, não sobre ela      | 02 §3             | A trilha é bem comum da plataforma           |
| Catálogo de poderes cadastrado por Admin, e só poder de Guerreiro(a) recebe trilha                   | 02 §2             | Cadastro do catálogo de poderes              |
| Cota de consulta em duas faixas, do projeto e de terceiro, com 429 no excesso                        | 03 §8             | Números da proteção das rotas públicas       |
| Freio por origem na consulta por nick e nos formulários de participação e de dados                   | 03 §8             | Números da proteção das rotas públicas       |
| Origem agrupada por resumo do IP, só em memória, e Cloud Run sem escala horizontal no Ciclo 01       | 03 §§1, 8         | Números da proteção das rotas públicas       |
| Solicitação de chave sem freio por origem, porque nova solicitação é sempre possível                 | 03 §8             | Números da proteção das rotas públicas       |
| Conjunto exportado em CSV, GeoJSON e dicionário de dados, formatos abertos                           | 03 §12.3          | Entrega do conjunto de dados                 |
| Conjunto entregue sob CC BY-SA, com crédito à comunidade que produziu o dado                         | 03 §12.3          | Entrega do conjunto de dados                 |
| Aprovação por solicitante identificado, finalidade declarada e não reidentificação                   | 03 §12.3          | Entrega do conjunto de dados                 |
| Solicitação de dados no mesmo prazo de 7 dias das demais solicitações                                | 03 §12.3          | Entrega do conjunto de dados                 |
| `SugestaoOuProposta` com autor, alvo, texto transcrito, situação, prazo e motivo do retorno          | 03 §§7, 12.2      | Canal de sugestões do Guerreiro(a)           |
| Badge de protagonismo é o único global, porque a proposta é sobre a plataforma inteira               | 11 §7             | Canal de sugestões do Guerreiro(a)           |

## 14. Pendências que permanecem

- **Instituição com mais de um usuário** no mesmo cadastro de Apoiador, e como se registra
  quem agiu em nome dela.
- **Base legal do resumo do IP** usado pelo freio das rotas públicas, e se ele merece linha
  própria na tabela de §11, que hoje só lista dado retido.
- **Prazo de disponibilidade da versão anterior** da API depois que uma nova abrir.
- **Prazo de guarda** do registro de infração e de pontuação negativa, dado sensível de
  criança que hoje segue a retenção geral do vínculo.

## 15. Rastreabilidade

| Requisito               | Origem                                            |
| ----------------------- | ------------------------------------------------- |
| `RF-01-01`, `RF-01-31`  | 03 §1 (API versionada)                            |
| `RF-01-02` e `RF-01-03` | 03 §1 (consulta sem login, escrita autenticada)   |
| `RF-01-04` a `RF-01-08` | 03 §§1.1, 3.2 e 3.3 (nick e imagem, alternativa)  |
| `RF-01-09` a `RF-01-12` | 03 §1.1 (como o adulto entra)                     |
| `RF-01-61`              | 02 §1 (o fundador é o primeiro Admin)             |
| `RF-01-13` a `RF-01-15` | 02 §1 e 03 §§1.1, 5, 9, 11 (responsável)          |
| `RF-01-16` e `RF-01-17` | 03 §§5, 11 (fronteira App 03 × App 09)            |
| `RF-01-18`              | 03 §1 (instância única)                           |
| `RF-01-19`              | 03 §12 (LGPD e consentimentos)                    |
| `RF-01-20` e `RF-01-21` | 02 §§3–5 e 11 §§2, 4–7                            |
| `RF-01-62`              | 02 §2 (catálogo de poderes cadastrado por Admin)  |
| `RF-01-22`              | 11 §8.4 (contrato dos jogos)                      |
| `RF-01-23`              | PRD-08                                            |
| `RF-01-24`, `RF-01-60`  | PRD-07                                            |
| `RF-01-56` a `RF-01-59` | 11 §5 (acumulado e saldo disponível de extras)    |
| `RF-01-25` e `RF-01-26` | 02 §§1, 4 e 03 §§7, 9–11                          |
| `RF-01-27` a `RF-01-30` | 03 §1 (princípios de arquitetura)                 |
| `RF-01-32`              | 03 §§3, 5 (App 01 habilitado pela aula agendada)  |
| `RF-01-33` e `RF-01-34` | 02 §1 e 03 §10 (acompanhamento por nick)          |
| `RF-01-35`              | 03 §7 (apoio escolar com corpus fechado)          |
| `RF-01-36`              | 05 §5 e 11 §5 (resposta e pontuação do quiz)      |
| `RF-01-37` a `RF-01-39` | 02 §5 e 05 §5 (equipe formada na aula e quiz)     |
| `RF-01-63`, `RF-01-64`  | 02 §§4, 5 (equipe fixa da trilha e crédito)       |
| `RN-01-44`              | 02 §5 (uma por trilha, fixa após homologação)     |
| `RF-01-40` a `RF-01-45` | 11 §2.1 e 04 §4 (etiqueta ODS e cobertura)        |
| `RF-01-46`, `RF-01-47`  | 03 §12.3 (entrega de dados aprovada por Admin)    |
| `RF-01-66`              | 03 §12.3 (formato, licença e critério da entrega) |
| `RF-01-48`, `RF-01-54`  | 03 §1 (chave obrigatória em toda chamada)         |
| `RF-01-49` a `RF-01-53` | 03 §8 (solicitação, emissão, prazo e revogação)   |
| `RF-01-55`              | 03 §§1, 8 (cota por faixa de chave)               |
| `RF-01-65`              | 03 §§1, 8 (freio por origem e sem escala)         |
