# 03 — Plataforma e Arquitetura

## 1. Princípios de arquitetura

1. **Backend em forma de API** — para que os mais diversos frontends **e aplicações de
   terceiros** possam acessá-lo.
2. **Rotas de consulta abertas** — leituras públicas (vitrine, rankings, batalhas) não exigem
   autenticação. Escrita e gestão exigem.
3. **Frontends independentes** — em **domínios diferentes**, evoluindo desacoplados do
   backend.
4. **Open Source** — todo o código-fonte é aberto, para permitir replicação por qualquer
   comunidade. O **conteúdo educacional publicado sai sob CC BY-SA**: qualquer um usa e
   adapta, creditando o Mestre autor, e o derivado herda a mesma licença.
5. **Registro de custos em tudo** — toda ação com custo (aula, lanche, hospedagem,
   prestadores) é computada e atribuída a um personagem; a arquitetura precisa suportar esse
   livro-razão desde o início.
6. **Dados do território como cidadão de primeira classe** — o modelo de dados precisa
   acomodar **séries temporais georreferenciadas** desde o início, com **guarda permanente**.
7. **Web App responsivo, Mobile First** — nesta etapa, **toda** aplicação é entregue como Web
   App projetado primeiro para o celular. Sem aplicativos nativos e sem aplicações construídas
   sobre plataformas de mensageria de terceiros.
8. **Plataforma em evolução contínua, com Guerreiros e Guerreiras, Mestres e Apoiadores** — os
   três propõem melhorias, e os Guerreiros e Guerreiras ainda alteram o código do jogo como
   atividade de trilha; a arquitetura precisa comportar essa evolução permanente.
9. **Construção assistida por IA, sob direção humana** — os artefatos da plataforma são
   construídos com auxílio de ferramentas de IA; a idealização, o contexto humano e social e
   as decisões são humanas, e a transparência sobre esse uso é pública.
10. **Uma instância para todas as comunidades** — a Comunidade Virtual é um vínculo nos
    registros, não uma cópia da plataforma. É o que permite comparar territórios e somar o
    aporte de quem sustenta mais de uma comunidade; em troca, toda consulta filtra por
    comunidade.
11. **API versionada na rota**, começando em `/v1`. Quebra de contrato abre uma versão nova,
    e a anterior segue no ar por prazo declarado.

### 1.1 Como cada persona entra

| Persona                      | Como autentica                                                                                                                                                                                            |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Guerreiro(a)**             | **Nick + imagem**, em **todas** as aplicações: o nick localiza, a imagem confirma contra o _template_ biométrico gravado no onboarding; sessão curta, porque o aparelho do ponto de apoio é compartilhado |
| **Mestre, Apoiador e Admin** | **Login social (Google)**                                                                                                                                                                                 |
| **Responsável**              | **Login social (Google)** ou **usuário e senha** criados por Admin ou Mestre                                                                                                                              |

- **Não há PIN, senha nem pergunta secreta para a criança, e sem câmera não há entrada.** É a
  imagem que garante que quem faz a atividade é a própria criança, e não um terceiro.
- **Enquanto o Guerreiro(a) não tem imagem gravada** — onboarding feito sem o responsável —,
  quem abre a sessão dele é o Mestre ou um Admin, no encontro. Vale igualmente para a falha de
  reconhecimento e para quem recusou a biometria: a criança resolve com quem está na sala.
- **Login não cria cadastro.** Conta social ou usuário sem cadastro prévio recebe recusa.
- **Quem não tem conta Google** recebe uma credencial de **usuário e senha provisória**, criada
  por Admin ou Mestre, com **troca de senha obrigatória no primeiro acesso**. O usuário não
  precisa ser e-mail — um nome simples basta (ex.: `Pai_aluno_Maria`). O login social é o
  caminho normal; esta é a exceção que impede alguém de ficar de fora.
- **O responsável tem login próprio**, vinculado a um ou mais Guerreiros e Guerreiras — é o que
  dá autoria clara ao consentimento e separa o que é dele do que é da criança.

**[Proposta]** Documentar a API com OpenAPI/Swagger desde o primeiro endpoint — condição
prática para que aplicações de terceiros e novos frontends realmente surjam.

## 2. Canais e meios de acesso

> **Definição vigente desta etapa:** **todas as aplicações são Web Apps responsivos, Mobile
> First**. Não há desenvolvimento sobre WhatsApp nem aplicativos nativos (Android/iOS). O
> navegador do celular é a plataforma-alvo; telas maiores são atendidas pela mesma aplicação.

| Canal                                 | Uso                                                                                                      |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Web App responsivo (Mobile First)** | Canal único de todas as aplicações                                                                       |
| **Smartphone / tablet**               | Dispositivo primário — é para ele que as telas são projetadas                                            |
| **PC / Notebook**                     | O mesmo Web App em telas maiores; uso típico da gestão                                                   |
| **Embarcados**                        | Raspberry Pi, NodeMCU, vestíveis. São o **hardware das atividades**, não um canal de acesso à plataforma |
| **Redes sociais**                     | Presença institucional e divulgação — não são canal de uso da plataforma                                 |

O conceito **"Converse com seu robô"** perpassa os dispositivos: o assistente do aluno deve
estar acessível a partir de qualquer navegador e conversar com os dispositivos embarcados
construídos nas oficinas.

Formato único de entrega: **uma base de código, sem loja de aplicativos, sem atualização pelo
usuário e sem tráfego de dados de crianças por plataformas de terceiros**.

### 2.1 As oito aplicações desta etapa

| #          | Aplicação                                                                                          | Público                                      | Seção   |
| ---------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------- | ------- |
| **App 01** | **Aula presencial** — onboarding do Guerreiro(a) e, em equipe, o conteúdo das trilhas              | Guerreiros e Guerreiras (na aula presencial) | §§3 e 4 |
| **App 03** | **Gestão administrativa** — CRUDs, lançamentos manuais e painéis do dia                            | Admins e Mestres                             | §5      |
| **App 04** | **Jogo em JavaScript** — sobre a base de personagens da plataforma                                 | Guerreiros e Guerreiras                      | §6      |
| **App 05** | **Área do Guerreiro(a)** — guia e apoio nas trilhas                                                | Guerreiros e Guerreiras                      | §7      |
| **App 06** | **Vitrine pública** — apresentação da plataforma, sem login                                        | Público geral                                | §8      |
| **App 07** | **Área dos pais e responsáveis** — evolução do Guerreiro(a), solicitações e transparência de dados | Pais e responsáveis                          | §9      |
| **App 08** | **Área do Apoiador** — aportes, desafios extras, efetividade e propostas                           | Apoiadores cadastrados                       | §10     |
| **App 09** | **Área do Mestre** — autoria de trilhas e conteúdos, suas turmas e lançamentos                     | Mestres cadastrados                          | §11     |

A numeração é histórica: o antigo **App 02 — Assistente por voz e Modo Ouvinte** foi
**incorporado ao App 01**, e o número 02 não é reaproveitado.

## 3. App 01 — Aula presencial: onboarding e presença

O App 01 é **a aplicação da aula presencial**, usada pelos próprios Guerreiros e Guerreiras. Ao
abrir, ela pergunta qual dos dois caminhos a pessoa quer:

- **Onboarding** — cadastro e registro de presença, de **uso individual**. É esta seção.
- **Trilhas** — conteúdo, equipes, quiz e assistente, de **uso em equipe** (§4).

Esta seção trata do primeiro caminho, que resolve dois problemas com a mesma jornada:
**cadastrar novos Guerreiros e Guerreiras** e **registrar a presença** dos já cadastrados — por
conversa, sem formulário.

> O onboarding **roda continuamente** durante o encontro, e não apenas na abertura, porque a
> dinâmica da aula é assíncrona.

### 3.1 Jornada

```text
[Tela inicial do App 01]
   ├── botão "TRILHAS"  → uso em equipe (§4)
   └── botão "ONBOARDING"
             │
             ▼
   [Tela de Boas-Vindas]
   ├── botão "Começar com ÁUDIO"  ──┐
   └── botão "Começar com CHAT"   ──┤
                                    ▼
                    [Interação cognitiva com IA]
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
            Guerreiro(a) NOVO                    Guerreiro(a) JÁ CADASTRADO
     nome, nick, nascimento/idade,        captura da imagem + nick
     avatar + imagem, se o                → comparação com a base
     responsável estiver junto                      │
                    │                               ▼
                    ▼                      presença registrada
            cadastro criado +              automaticamente
            presença registrada
```

### 3.2 Requisitos funcionais

**Tela inicial** — layout Mobile First, alto contraste, poucos elementos. Primeiro a escolha
entre **onboarding** e **trilhas**; escolhido o onboarding, dois botões: **começar por áudio** e
**começar por texto (chat)**. Ambos levam ao mesmo fluxo cognitivo.

**Interação cognitiva** — conduzida por **IA**: conversa natural, tolerante a respostas fora
de ordem, capaz de repetir e confirmar dados. Na modalidade áudio, captação e reprodução via
`navigator.mediaDevices.getUserMedia`, reconhecimento de fala e síntese de voz — mesma base
técnica do Robô Educa. Na modalidade chat, a mesma conversa em texto, para ambientes
barulhentos ou Guerreiros e Guerreiras que preferem digitar.

**Captura de imagem** — pela câmera do dispositivo, com **finalidade única: identificar o
Guerreiro(a)**, o que abrange o registro de presença e a autenticação dele nas aplicações. É o
_template_ gerado nesta captura que faz as vezes de senha, já que a criança não tem PIN nem
senha. Não é avatar, não vai para a vitrine, não aparece em ranking, não é compartilhada.

**Condição de funcionamento** — o App 01 exige **câmera no aparelho** e um **Mestre ou Admin
presente**. Faltando um dos dois, o onboarding não acontece: é o encontro presencial que dá
garantia ao cadastro.

**A criança comparece com o responsável no primeiro dia de aula.** É nesse encontro que o
responsável é cadastrado (documento 02) e autoriza a biometria. Vindo a criança sozinha, o
onboarding é feito com intervenção do Mestre ou de um Admin e **sem registro de imagem** — o
Guerreiro(a) fica ativo e participa das atividades, entrando com a confirmação de quem está na
sala. **Assim que o responsável aprova a participação, a imagem é registrada** e o Guerreiro(a)
passa a entrar sozinho.

#### Novo Guerreiro(a) — dados coletados

| Dado                        | Uso                                                                                                                                |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Nome                        | Identificação interna e comunicação com responsáveis                                                                               |
| Nick                        | Identidade pública do Guerreiro(a)                                                                                                 |
| Forma de tratamento         | Como a plataforma o chama: **Guerreiro** ou **Guerreira**, à escolha da pessoa                                                     |
| Data de nascimento ou idade | Adequação de conteúdo e faixa (6 a 16 anos)                                                                                        |
| Características do avatar   | Geração do avatar público                                                                                                          |
| Imagem                      | **Exclusivamente** identificar o Guerreiro(a) depois: presença e autenticação. Só é captada com o responsável presente e de acordo |

**Vínculo com a Comunidade Virtual (regra vigente).** O Guerreiro(a) **não informa a
comunidade**: ela vem da **aula em andamento**. Cada aula é cadastrada na App 03 com
comunidade, data, horário inicial e final, e o App 01 identifica sozinho, pela data e hora,
qual é a aula e a que comunidade vincular o cadastro. **Sem aula agendada para aquele momento,
o App 01 não opera** — é o que simplifica a conversa de cadastro e garante que nenhum
Guerreiro(a) exista sem comunidade.

Havendo, na mesma data e horário, **aulas presenciais em comunidades diferentes**, o App 01
pergunta **uma vez, ao abrir**, em qual delas está operando, e usa essa escolha até o fim da
sessão de trabalho.

Ao final, o Guerreiro(a) já está **ativo** e pode participar das atividades — sem exigência de
autorização do responsável nesta etapa.

#### Guerreiro(a) já cadastrado — registro de presença

1. Captura da imagem na chegada.
2. Comparação com a base **combinada ao nick informado** (dois fatores: o nick restringe a
   busca, a imagem confirma).
3. Presença registrada automaticamente na atividade — presencial ou on-line.
4. Falha na identificação cai para confirmação manual por Admin/Mestre — nunca deixa o
   Guerreiro(a) de fora da aula.

### 3.3 Requisitos de proteção de dados (LGPD aplicada)

A imagem é **dado pessoal sensível de criança e adolescente**. Regras obrigatórias:

- **Finalidade declarada e única**: identificar o Guerreiro(a) — registro de presença e
  autenticação nas aplicações. Qualquer outro uso exige nova base legal e novo consentimento.
- **Consentimento informado** do responsável para a captura e o tratamento biométrico, colhido
  em **termo impresso, assinado pelo responsável presente no encontro**, antes da captura. O
  App 01 registra o consentimento com data, hora e quem testemunhou; a **digitalização do termo
  assinado é anexada ao cadastro pela gestão**, e o anexo em falta aparece como pendência no
  painel do dia. **Sem termo assinado não há captura** — e é por isso que o cadastro biométrico
  só acontece depois que o responsável aprova a participação.
- **Minimização**: a **fotografia original é apagada assim que o _template_ biométrico**
  (representação matemática não reversível) é gerado. A plataforma não guarda rosto de criança.
- **Segurança**: armazenamento criptografado, acesso restrito e auditado.
- **Retenção**: o _template_ é guardado enquanto durar o vínculo do Guerreiro(a) com o projeto
  e excluído automaticamente ao fim dele, ou a pedido do responsável.

> **A definir:** prazo, em dias, entre o fim do vínculo e a exclusão automática do _template_.

- **Direito de recusa**: quem não autoriza a imagem tem **alternativa equivalente** — nick mais
  confirmação do Mestre ou de um Admin, **no encontro**, tanto para registrar presença quanto
  para entrar nas aplicações. Recusar biometria nunca pode significar exclusão da atividade.
- **Transparência**: política de privacidade em linguagem simples — para o responsável **e
  para a criança**.

### 3.4 Requisitos não funcionais

- Funcionar em **rede instável** e em aparelhos modestos, com fila local de sincronização.
- **Rede fora:** a **presença** entra na fila local, confirmada pelo Mestre ou por um Admin
  pelo nick, e sincroniza quando a rede voltar. **Cadastro novo e reconhecimento facial exigem
  rede** — nenhuma imagem de criança fica guardada no aparelho compartilhado.
- Registro de presença de Guerreiro(a) conhecido em **poucos segundos** — a aula não pode
  travar na porta.
- Acessibilidade: a modalidade áudio atende quem ainda não lê com fluência e pessoas com
  deficiência visual.

## 4. App 01 — Aula presencial: trilhas, equipes e assistente

O segundo caminho do App 01 é o que a turma usa durante o encontro: **o conteúdo das trilhas,
em equipe**. A aula presencial tem **dois ou mais aparelhos, um por equipe** — o mesmo aparelho
em que a equipe acompanha o ponto de trilha, responde ao Quiz ao Vivo e conversa com o
assistente. A entrada é a de sempre: **nick e imagem** (§1.1).

### 4.1 Equipes formadas na hora

**As equipes são formadas pelos próprios Guerreiros e Guerreiras, aqui no App 01**, e valem
para **aquela aula**: começam e terminam com o encontro. Tamanho, composição e a regra do
familiar seguem o documento 02. A gestão **não forma nem edita equipe** — vê as equipes do dia
no painel da App 03.

- O Guerreiro(a) pode integrar **mais de uma equipe** no mesmo encontro.
- **No Quiz ao Vivo, uma só**: a partida é simultânea e a resposta do aparelho vale para todos
  os integrantes da equipe.

### 4.2 Conteúdo da trilha, quiz e assistente

Arquitetura: **JavaScript no frontend + IA no backend**, a mesma base técnica do Robô Educa. A
equipe vê **em que ponto de trilha está**, o conteúdo e a atividade do dia, e conversa com o
assistente **por voz ou por texto**: quiz e explicação de conceitos das trilhas. O assistente
segue **o mesmo desenho do assistente da App 05** (§7): modelo **LLM Google Gemini**, **corpus
fechado** no conteúdo que os Mestres cadastraram, guardrails educacionais, filtros de segurança
no nível mais restritivo e **guarda apenas da transcrição**, com o áudio descartado.

No **Quiz ao Vivo**, é por aqui que a equipe recebe a pergunta e envia a resposta; as regras da
partida estão no documento 05.

O **apoio às atividades escolares** não fica aqui: é atendido pelo assistente da App 05.

**A aplicação não escuta a aula.** O microfone só abre quando o Guerreiro(a) fala com o
assistente e fecha quando ele termina — não há captação do áudio ambiente nem transcrição da
conversa da turma.

## 5. App 03 — Gestão administrativa

Aplicação autenticada, para Admins e — conforme permissão — Mestres:

- **CRUDs de personas e catálogo**: Guerreiros e Guerreiras, mestres, apoiadores, responsáveis,
  admins, comunidades virtuais e poderes.
- **Cadastro de responsáveis e vínculo com os Guerreiros e Guerreiras** — e-mail da conta
  Google ou credencial de usuário e senha provisória, grau de parentesco e no máximo três
  responsáveis por Guerreiro(a). O Mestre faz o mesmo cadastro pela App 09.
- **Criação das Comunidades Virtuais** — **exclusiva de Admins**, nascendo vazias.
- **Agenda das aulas com comunidade, data, horário inicial e final** — é ela que **habilita o
  App 01**: sem aula agendada para o momento, não há onboarding, e é dela que sai a comunidade
  a que o novo Guerreiro(a) é vinculado.
- **Vínculo do Guerreiro(a) à comunidade** — conferência do vínculo herdado da aula. A
  **transferência entre comunidades** existe no modelo, com registro da data, mas **não é
  operada no Ciclo 01**.
- **Cadastro de Mestres e Apoiadores** — exclusivo de Admins, com anexação dos artefatos
  comprobatórios, do currículo, do portfólio e dos links de redes sociais.
- **Fila de solicitações de participação** como Mestre ou Apoiador, vindas do formulário
  público da App 06.
- **Cadastro dos locais do território** e **fila de solicitações de novo local** vindas da
  App 05, com alerta das solicitações em aberto — o Mestre da trilha também pode aprová-las,
  pela App 09.
- **Inclusão manual de novos Admins** por um Admin existente.
- **Leitura das equipes do dia**, formadas pelos próprios Guerreiros e Guerreiras no App 01 —
  a gestão acompanha no painel e **não altera composição**.
- **Cadastro de atividades** com pontuação, recompensas e recursos necessários.
- **Agenda de aulas** (on-line e presenciais) e atividades previstas.
- **Lançamento de atividades realizadas**: data, mentores, Guerreiros e Guerreiras e
  resultados.
- **Registro de presença** — automático via onboarding e ajustável manualmente.
- **Entradas manuais do dia**: presença, infrações ocorridas nas aulas e pontuação extra ao
  Guerreiro(a) que ajudou o colega.
- **Lançamento de pontuação negativa** — o Mestre também lança, pela App 09, com motivo
  registrado e sem revisão de outro Admin.
- **Gestão de recursos** necessários às atividades (aportes e baixa de consumo).
- **Aprovação de desafios extras** propostos pelos Apoiadores na App 08, após validação
  pedagógica do Mestre da trilha.
- **Painéis do dia** — visão operacional do encontro em andamento: presenças confirmadas,
  atividade prevista, recursos providos e lançamentos pendentes.
- **Condução do Quiz ao Vivo** — as perguntas vêm do banco que o Mestre curador cadastra na
  App 09. **Quem conduz a partida é quem está ministrando a aula**: o Mestre da aula ou um
  Admin.
- **Atendimento às solicitações dos responsáveis** vindas da App 07, com registro de quem
  tratou e quando.
- **Fila de avaliação das sugestões e propostas** vindas das Apps 05, 07, 08 e 09, com status
  e retorno a quem propôs.
- **Auditoria por amostragem do conteúdo de apoio escolar** cadastrado pelos Mestres, com
  despublicação motivada — o Admin confere, não cadastra. A conferência é **mensal**, cobrindo
  ao menos **10% do conteúdo novo do mês** e **100% das disciplinas que geraram recusa** do
  filtro de segurança; as trilhas publicadas são auditadas no mesmo ato e na mesma cadência.

A autoria de trilhas e conteúdos e as validações pedagógicas são do Mestre e vivem na App 09;
esta aplicação continua sendo a da **gestão** — cadastros, lançamentos, aprovações de Admin e
painéis do dia.

**Acesso do Mestre a esta aplicação:** **leitura do painel do dia** e **condução do Quiz ao
Vivo das aulas que ministra**. Fora isso, tudo o que ele escreve continua na App 09.

## 6. App 04 — Jogo em JavaScript

Jogo executado no navegador, construído sobre a **base de personagens da plataforma**: os
avatares, poderes, badges e níveis já conquistados são os elementos do jogo.

> **Engine sugerida: [Phaser.js](https://phaser.io/)** — framework de jogos 2D em JavaScript
> que roda no navegador, sem plugin nem instalação, e funciona bem em celular modesto. Escolha
> coerente com Web App / Mobile First e com o objetivo de que o **código seja legível e
> alterável pelos próprios Guerreiros e Guerreiras**.

**Definição vigente — o jogo não gera pontuação, apenas a consome.** Os pontos vêm
exclusivamente das atividades propostas pelos Mestres e da coleta de dados do território. O
jogo é um **destino** dos pontos, não uma fonte. Consequências:

- O que se conquista aprendendo (poderes, badges, níveis) **desbloqueia e alimenta** o que o
  Guerreiro(a) pode fazer dentro do jogo.
- Jogar muito **não** sobe ninguém no ranking — o ranking mede aprendizado e realização na
  vida real.
- Elimina, por construção, a principal via de fraude de pontos: não há como automatizar
  cliques para pontuar.

Objetivos: dar utilidade lúdica ao progresso das trilhas; servir de conteúdo do **Poder da IA e
Robótica**, já que alterar o código é atividade de trilha — o Guerreiro(a) é um dos
construtores do próprio jogo; e respeitar a regra de representação por **avatares, nunca
imagens reais**.

> **A definir:** gênero e mecânica do jogo.

## 7. App 05 — Área do Guerreiro(a)

**É a aplicação das aulas remotas** e do uso cotidiano fora do encontro presencial — a aula
presencial é atendida pelo App 01 (§§3 e 4).

Web App de uso cotidiano do Guerreiro(a), com **guia e apoio nas trilhas**: qual é o próximo
ponto, o que precisa ser feito, o que já foi conquistado e o que está bloqueado. Reúne a
jornada gamificada — poderes, trilhas, desafios semanais, equipes, ranking, recompensas
conquistadas nos marcos e registro de dados do território.

É também o instrumento de **coleta de dados da Comunidade Virtual**: as séries ativas, quando é
a próxima medição, o que já foi registrado e **quantos pontos aquela série está rendendo**. O
Guerreiro(a) seleciona o local do dado entre os cadastrados e, faltando um, solicita a
inclusão.

É onde fica o **apoio às atividades escolares**, atendido por um **assistente por voz com IA**
— modelo **LLM Google Gemini** — que responde **exclusivamente a partir das disciplinas e do
conteúdo cadastrados previamente pelos Mestres na App 09**. Quatro exigências formam a regra:

- **Corpus fechado.** Fora do conteúdo cadastrado o assistente não responde: diz que o assunto
  ainda não está no material da plataforma e orienta procurar um Mestre no encontro.
- **Guardrails educacionais.** O assistente explica e conduz ao raciocínio; não entrega tarefa
  pronta, não opina sobre pessoas e não trata de assunto fora das disciplinas cadastradas.
- **Filtros de segurança no nível mais restritivo**, com aviso prévio ao Guerreiro(a) e ao
  responsável e **alternativa equivalente** — perguntar ao Mestre no encontro — para quem
  recusar.
- **Só a transcrição é guardada**: o áudio da pergunta é descartado assim que transcrito,
  pela mesma razão que a fotografia do onboarding é apagada na geração do _template_.

**Quem cadastra e quem confere.** O corpus é cadastrado **apenas pelos Mestres**; o Admin não
cadastra conteúdo de apoio — ele **audita por amostragem** o que o Mestre publicou e pode
despublicar com motivo, exatamente como faz com as trilhas.

**Cota e custo no Ciclo 01.** Não há teto de uso: a demanda e o custo são observados ao longo
do ciclo para dimensionar o ciclo seguinte. O consumo entra no livro-razão como recurso de
_cloud_, **aportado por absorção pelo Admin e Mestre fundador**, começando no _free tier_ da
conta **Google Gemini PRO** e passando a _pay-as-you-go_ quando o uso exigir.

E é o **canal de sugestões do Guerreiro(a)**: ideias de melhoria para atividades, trilhas e
para a própria plataforma são registradas aqui e caem na fila de avaliação da gestão — o mesmo
mecanismo de evolução pactuada do Código de Conduta, estendido à plataforma inteira. O registro
é feito **em texto ou em áudio de até 60 segundos**, transcrito — uma criança de 6 anos fala
melhor do que escreve. **Registrar não pontua; a proposta adotada rende pontos extras e badge**,
e o retorno acontece em até 7 dias na própria plataforma, com o motivo em linguagem simples
quando não for adotada.

## 8. App 06 — Vitrine pública

Web App de acesso público e **sem autenticação**:

- Apresenta **Guerreiros e Guerreiras, Poderes, Mestres, Batalhas, Apoiadores e Comunidades
  Virtuais**, com navegação para seções específicas com cards individuais.
- **Cada card abre a página individual do personagem** — Guerreiro(a), Mestre, poder, apoiador
  ou comunidade —, com a versão detalhada do que o card resume (composição no documento 11).
- **Cards rotativos** com avatares dos Guerreiros e Guerreiras, atualizados a cada 5 segundos.
  Exibem **apenas** avatar, nick, badges, poderes adquiridos e desempenho na plataforma — **sem
  links para redes sociais dos Guerreiros e Guerreiras** nem qualquer canal de contato direto.
- **Página de Mestres e Apoiadores** com **currículo, portfólios, redes sociais e documentos
  comprobatórios externos** — a prova pública de habilidade e de apoio.
- **Formulário de solicitação de participação** como Mestre ou Apoiador, aberto a pessoas e
  instituições: a solicitação é gravada e cai na fila de avaliação dos Admins na App 03.
- **Aportes exibidos em moedas da plataforma**, nunca em reais (documento 04).
- **Painel público da Comunidade Virtual** — dados do território em **série histórica**,
  agregados e anonimizados, abertos à consulta da comunidade e de instituições.
- **Portfólio de criações originais** — as criações dos Guerreiros e Guerreiras autorizados,
  com o nick do autor (ou dos autores, em equipe).
- **Favoritos do visitante** — sem login e sem cadastro, o visitante marca Guerreiros,
  Guerreiras e Mestres como favoritos e a vitrine passa a destacar as novidades deles primeiro.
  A lista fica **no próprio aparelho**: a plataforma não coleta nada do visitante e, trocando de
  aparelho, a lista não vai junto.
- Seções **"Quem somos"** e **"Contatos"**, editáveis pelos Admins — incluindo a **nota de
  transparência sobre IA**.
- **"Como apoiar"** — canais de doação, incluindo a chave PIX da pessoa jurídica vinculada.
- Identidade visual: **background com imagem de comunidade, cores, grafite** — estética de
  território, não corporativa.
- **Vídeo de apresentação**: os irmãos Susy e Otávio, os Rôbróders e o professor Carlos
  Trenell (narrativa da trilha Robô Educa).
- É também o espaço da **publicidade** prevista como fonte de receita — sempre fora das áreas
  de uso das crianças e sem coleta de dados de menores para fins publicitários.

## 9. App 07 — Área dos pais e responsáveis

Web App autenticado, **canal oficial da plataforma com a família** — o que resolve a
comunicação da evolução do aluno sem depender de aplicativos de mensageria de terceiros. O
responsável acessa apenas os dados dos Guerreiros e Guerreiras sob sua responsabilidade, com
vínculo conferido por um Admin ou por um Mestre.

| Função                       | O que o responsável faz                                                                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Evolução do Guerreiro(a)** | Acompanha presença, atividades realizadas, pontos, poderes, badges, nível e progresso nas trilhas                                                       |
| **Solicitações**             | Autoriza ou **revoga** a divulgação pública do perfil; pede correção ou exclusão de dados; solicita esclarecimentos — cada pedido com protocolo e prazo |
| **Direitos de recusa**       | Recusa, a qualquer tempo, a **imagem do Guerreiro(a)** e o uso de imagem em vídeos e fotos de eventos                                                   |
| **Transparência de dados**   | Vê **quais dados da criança estão armazenados**, para que servem, por quanto tempo ficam e quem os acessou                                              |
| **Termos e consentimentos**  | Lê, aceita e consulta o histórico dos termos assinados, com data e hora                                                                                 |
| **Propostas**                | Registra propostas de evolução da plataforma, na mesma fila de avaliação das sugestões dos Guerreiros e Guerreiras                                      |

**Regras obrigatórias:**

- **Nenhuma recusa exclui o Guerreiro(a) da atividade.** Todo direito de recusa tem alternativa
  equivalente.
- **A revogação vale para frente e é imediata** na parte pública: o perfil sai da vitrine e
  dos rankings, sem prejuízo da participação.
- **Limite declarado do pedido de exclusão:** os **registros de dados do território** não são
  apagados a pedido — são **despersonalizados**, com o vínculo de autoria rompido e o
  mapeamento destruído (§12.1). Isso precisa estar dito na tela, em linguagem simples, e no
  termo assinado — não descoberto depois.
- **Linguagem simples**, na mesma medida exigida da política de privacidade.
- **Sem contato direto com Apoiadores ou terceiros**: a área é canal entre família e
  plataforma, e nada mais.
- Todas as solicitações caem na fila de atendimento da App 03, com registro de tratamento.

**Prazo de resposta: 7 dias** para toda solicitação do responsável. **No Ciclo 01 não há
notificação por e-mail**: o retorno acontece na própria plataforma, na área do responsável.

## 10. App 08 — Área do Apoiador

Web App autenticado dos **Apoiadores já cadastrados** por um Admin. É onde o apoio deixa de
ser um lançamento feito por terceiros e passa a ter canal próprio:

| Função                        | O que o Apoiador faz                                                                                                                                |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Meus aportes**              | Acompanha o que aportou, em **moedas**, e o **Poder Econômico** acumulado                                                                           |
| **Desafios extras**           | Propõe desafios abertos ou direcionados e acompanha validação do Mestre e aprovação do Admin                                                        |
| **Efetividade do apoio**      | Vê o que os desafios produziram — sempre **agregado e por avatar**                                                                                  |
| **Acompanhamento**            | Vê os **mesmos dados do painel público** e mantém **favoritos** — Guerreiros e Guerreiras pelo nick e Mestres —, com as novidades deles em destaque |
| **Documentos comprobatórios** | Envia currículo, portfólio, redes sociais, termos e comprovantes para o Admin anexar ao seu cadastro                                                |
| **Propostas**                 | Registra propostas de evolução da plataforma, que caem na fila de avaliação da gestão                                                               |

**Regras obrigatórias:**

- **Nenhum contato direto com Guerreiro(a) ou família.** Proposta, entrega e reconhecimento
  seguem mediados pela plataforma; a App 07 não é compartilhada com Apoiadores. **Favoritar é
  leitura**: não abre canal, não avisa a criança e não dá acesso a nada além do que já é público.
- **O nick vem da família, nunca da plataforma.** A busca é por nick exato, alcança apenas quem
  tem divulgação autorizada e não lista, sugere nem completa nomes.
- **O app não cadastra Apoiador.** O cadastro continua exclusivo de Admin; quem ainda não é
  Apoiador usa o formulário de solicitação da vitrine.
- Toda proposta de desafio extra segue o fluxo vigente: validação do Mestre da trilha,
  aprovação de Admin e **lastro antes da publicação**.

## 11. App 09 — Área do Mestre

Web App autenticado dos **Mestres cadastrados** por um Admin. É a bancada de trabalho de quem
ensina: o que o Mestre cria e o que ele conduz nas suas atividades.

| Função                    | O que o Mestre faz                                                                                                                     |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Autoria de trilhas**    | Cria trilhas, pontos de trilha, conteúdos, bibliografia de apoio, **atividades do ponto**, quizzes e desafios — inclusive o de coleta  |
| **Prova de habilidade**   | Publica os artefatos que comprovam sua habilidade, além de currículo, portfólio e redes sociais                                        |
| **Minhas atividades**     | Acompanha as suas turmas e lança resultados, presenças e méritos das atividades que propôs                                             |
| **Validação pedagógica**  | Valida os desafios extras que os Apoiadores propõem para as suas trilhas, antes da aprovação do Admin                                  |
| **Banco do Quiz ao Vivo** | Cadastra as perguntas das suas aulas e **conduz a partida** das aulas que ministra, pela App 03                                        |
| **Pontuação negativa**    | Lança a pontuação negativa das suas aulas, com motivo registrado e sem revisão de Admin                                                |
| **Necessidades**          | Vê o que falta de recurso para as suas atividades e, se quiser, cobre a falta com **aporte por absorção**                              |
| **Locais do território**  | Aprova as solicitações de novo local dos Guerreiros e Guerreiras das suas trilhas, com alerta das que estão em aberto                  |
| **Responsáveis**          | Cadastra o responsável que se apresentou no encontro e vincula a ele **qualquer** Guerreiro(a) já cadastrado, com o grau de parentesco |
| **Apoio escolar**         | Cadastra as disciplinas e o conteúdo — o corpus fechado que os assistentes das Apps 05 e 01 podem usar; o Admin audita por amostragem  |
| **Propostas**             | Registra propostas de evolução da plataforma, na mesma fila de avaliação da gestão                                                     |
| **Ressarcimento**         | Acompanha a situação do que absorveu; havendo receita, envia a chave PIX por e-mail ao Admin — a plataforma não guarda dado bancário   |

**Regras obrigatórias:**

- **O app não cadastra Mestre.** O cadastro segue exclusivo de Admin, com habilidade
  comprovada; quem ainda não é Mestre usa o formulário de solicitação da vitrine.
- **O Mestre lança apenas o que é seu** — as atividades que propôs e as turmas em que atua.
  Cadastros de personas — salvo o do responsável, que ele cadastra e vincula para qualquer
  Guerreiro(a) —, aprovações privativas de Admin e painéis gerais continuam na App 03.
- **Nenhum modelo ou fluxo pressupõe habilidade técnica de TI**: o Mestre pode ser de humanas,
  artes, esportes ou cultura.
- **A trilha publicada vai ao ar sem aprovação prévia.** A curadoria é posterior: o Admin
  audita por amostragem e pode despublicar, do mesmo modo como audita a coleta.
- **A ferramenta recusa publicar trilha sem desafio de coleta e sem culminância com criação
  original** — as duas regras do documento 02 viram trava, não recomendação. A criação
  entregue é validada pelo Mestre autor da trilha.
- **Conteúdo do ponto de trilha:** texto formatado, imagens, link externo e upload hospedado
  pela plataforma — **vídeo até 200 MB e arquivo até 20 MB por ponto de trilha**, com o
  consumo lançado como recurso de _cloud_ no livro-razão.

## 12. Proteção de dados em toda a plataforma (LGPD)

- Guerreiros e Guerreiras são representados **por avatares, nunca por imagens reais**, em toda
  a plataforma.
- Cards de Guerreiros e Guerreiras **sem links para redes sociais nem contato direto**.
- **Adesão em duas etapas:** o cadastro é **livre** (nome, data de nascimento, nick,
  comunidade e características do avatar) e permite participar de todas as atividades; a
  **divulgação pública do histórico e do perfil** só ocorre **após autorização dos pais ou
  responsáveis**, concedida e revogável pela App 07.
- A imagem captada no onboarding é **dado sensível de uso restrito**: serve apenas para
  identificar o Guerreiro(a) — presença e autenticação — e **nunca** é exibida publicamente.
- **Dados do território: guarda permanente com o coletor identificado**, mesmo depois que o
  Guerreiro(a) deixa o projeto — é o que dá procedência à série e preserva o crédito da
  realização. A **anonimização ocorre na saída**: painéis públicos, exportações, pesquisas e
  entregas a instituições recebem dados **agregados e anonimizados**.

### 12.1 Base legal da guarda do dado de território

Duas camadas, e a distinção entre elas é o que sustenta o desenho:

| Camada                   | O que é                                           | Base legal                                                                        |
| ------------------------ | ------------------------------------------------- | --------------------------------------------------------------------------------- |
| **A medição**            | Valor, local, data — dado do **lugar**            | Anonimizada na saída, **fora do alcance da LGPD** enquanto não identifica ninguém |
| **O vínculo de autoria** | Quem coletou — único dado **pessoal** do registro | **Consentimento específico e em destaque do responsável**, revogável              |

- **Titularidade não se transfere.** O titular do vínculo de autoria é o Guerreiro(a); o
  responsável **exerce os direitos** em nome dele e **recebe a parte monetária** do rateio da
  coproprietariedade. É o máximo que a lei admite nessa direção, e é o que o projeto pratica.
- **Revogação despersonaliza, não apaga.** Revogado o consentimento, a plataforma **rompe o
  vínculo de autoria e destrói o mapeamento**: o registro permanece na série com um **código de
  coletor sem correspondência a pessoa alguma**, preservando a consistência da série sem
  preservar dado pessoal. É a resposta concreta ao pedido de exclusão, e o termo diz isso antes
  do aceite.
- **A base de pesquisa entra quando a entidade existir.** A retenção nominal por prazo
  indeterminado só se apoia em pesquisa (LGPD art. 7º, IV e art. 16, II) quando houver
  **pessoa jurídica sem fins lucrativos** com pesquisa na missão institucional — a empresa
  vinculada hoje não se enquadra. Até lá, a camada pessoal se sustenta em consentimento, e é
  por isso que a criação da entidade é decisão que precede a monetização e a entrega de dados
  a instituições.
- **Risco de reidentificação**: em comunidade pequena, código de coletor somado a data e local
  fino ainda pode apontar uma criança. Toda saída passa por agregação suficiente para que isso
  não ocorra, e a granularidade fina fica restrita a uso interno e a entregas com acordo
  formal.

### 12.2 Prazos de guarda

| Dado                                              | Prazo                                                             |
| ------------------------------------------------- | ----------------------------------------------------------------- |
| Transcrição de consulta respondida (Apps 05 e 02) | **7 dias** vinculada ao Guerreiro(a); depois só disciplina e data |
| Transcrição de consulta recusada pelos filtros    | **Até o fim do ciclo**, restrita à gestão                         |
| Transcrição de sugestão não adotada               | **90 dias** após o retorno a quem sugeriu                         |
| Transcrição de sugestão adotada                   | Permanente, com autoria — é contribuição creditada                |
| Áudio de qualquer origem                          | **Descartado na transcrição**                                     |
| _Template_ biométrico, fim do vínculo             | **30 dias**, com aviso prévio ao responsável                      |
| _Template_ biométrico, pedido do responsável      | **5 dias**                                                        |
| Métricas de custo e demanda de IA                 | Permanente, **sem nenhum dado pessoal** — só contadores           |

**Fim do vínculo** é o marco desses prazos: ocorre **por pedido do responsável** ou
**automaticamente após 12 meses sem nenhuma atividade registrada** — prazo que cobre o
intervalo entre ciclos sem manter biometria de quem já saiu.

**Sessão em aparelho compartilhado**: encerra por **10 minutos de inatividade**, com aviso um
minuto antes e opção de continuar, além do botão de sair sempre visível. O risco tratado aqui
é a próxima criança ver os dados da anterior.

- **Georreferenciamento sem expor endereço de criança**: a granularidade publicada nunca pode
  permitir inferir onde um Guerreiro(a) específico mora.
- **Aviso visível em toda aplicação:** onde há coleta de dado, o app indica ao usuário — de
  forma discreta e elegante, sem interromper o uso — o que está sendo coletado e quais são os
  seus direitos, com acesso a uma **área detalhada** que explica destino e uso de cada dado.
- **Coproprietariedade dos dados publicados**: em produção, a entidade responsável pela
  plataforma é coproprietária, com o Guerreiro(a) que gerou o dado (documento 04).
- A LGPD deve ser considerada em **todos** os módulos e PRDs, não como item pontual.

**[Proposta]** Aplicar o mesmo cuidado a vídeos de culminância e fotos de eventos em que
Guerreiros e Guerreiras apareçam, com consentimento específico do responsável para cada
divulgação.
