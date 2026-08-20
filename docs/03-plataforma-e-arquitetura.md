# 03 — Plataforma e Arquitetura

## 1. Princípios de arquitetura

1. **Backend em forma de API** — para que os mais diversos frontends **e aplicações de
   terceiros** possam acessá-lo. A aplicação de terceiro pede a chave na **Área do Apoiador
   Desenvolvedor**, na vitrine (§8).
2. **Toda aplicação que consome a API se identifica por chave**, inclusive as do próprio
   projeto, que recebem a sua na implantação — **uma por aplicação e por ambiente**, para que
   chave de desenvolvimento não abra produção. **Sem chave válida a API não responde**, e a
   exigência alcança **toda rota de dados sob o prefixo de versão**, inclusive as de consulta
   pública. O que a leitura pública dispensa é o **login da pessoa**: o visitante da vitrine e
   do jogo não se identifica — quem se identifica é a aplicação. Escrita e gestão exigem, além
   da chave, a credencial da persona.
   O núcleo responde a **qualquer origem** (`*`), **sem cookie credenciado** — a chave e a
   credencial da persona viajam em cabeçalho. A proteção está nelas, na cota por chave e no
   freio por origem (§8), não no navegador: restringir origem não barra chamada feita fora
   dele e contrariaria o princípio 1.
3. **Frontends independentes** — em **endereços próprios**, evoluindo desacoplados do backend.
   A **vitrine ocupa a raiz** do domínio da plataforma — **`comunidadegame.org`** —: é por ela
   que qualquer pessoa chega, e é dela que o botão **Entrar** encaminha cada persona à sua
   aplicação. As demais ficam em subdomínio, um por aplicação, e o núcleo no seu:

   | Endereço                         | Aplicação                |
   | -------------------------------- | ------------------------ |
   | `comunidadegame.org`             | App 06 — vitrine         |
   | `api.comunidadegame.org`         | Backend API              |
   | `aula.comunidadegame.org`        | App 01 — aula presencial |
   | `gestao.comunidadegame.org`      | App 03 — gestão          |
   | `jogo.comunidadegame.org`        | App 04 — jogo            |
   | `minhaarea.comunidadegame.org`   | App 05 — Guerreiro(a)    |
   | `responsavel.comunidadegame.org` | App 07 — responsáveis    |
   | `apoiador.comunidadegame.org`    | App 08 — apoiador        |
   | `mestre.comunidadegame.org`      | App 09 — mestre          |

   A App 05 é **`minhaarea`**, não `guerreiro`: o endereço não fixa o gênero da persona
   primária, tratada por Guerreiro ou Guerreira (documento 02).

4. **Open Source** — todo o código-fonte é aberto, para permitir replicação por qualquer
   comunidade. O **código sai sob AGPL**: quem replica a plataforma e a oferece pela rede
   abre também as suas modificações, e é isso que impede alguém de fechar como serviço
   privado o que a comunidade construiu. Quem apenas **consome a API** com aplicação própria
   não é alcançado pela licença — usar a API pela rede não torna a aplicação derivada. O
   **conteúdo educacional publicado sai sob CC BY-SA**: qualquer um usa e adapta, creditando
   o Mestre autor, e o derivado herda a mesma licença. Código e conteúdo seguem, cada um na
   sua régua, o mesmo princípio de compartilhar igual. O **titular do direito autoral do
   código é a pessoa jurídica vinculada ao projeto** (documento 04), que é quem responde por
   ele e quem poderia relicenciá-lo. Para manter essa titularidade íntegra, **toda
   contribuição externa entra por CLA**, com cessão dos direitos patrimoniais à pessoa
   jurídica; sem CLA assinado, o _pull request_ não é integrado.
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
   as decisões são humanas, e a transparência sobre esse uso é pública. No Ciclo 01 a
   construção usa os modelos **Claude 5 e Sonnet 5**, da Anthropic — uso distinto do Gemini,
   que atende as pessoas na plataforma (§1.12). A nota pública declara os dois (documento 01).
10. **Uma instância para todas as comunidades** — a Comunidade Virtual é um vínculo nos
    registros, não uma cópia da plataforma. É o que permite comparar territórios e somar o
    aporte de quem sustenta mais de uma comunidade; em troca, toda consulta filtra por
    comunidade.
11. **API versionada na rota**, começando em `/v1`. Quebra de contrato abre uma versão nova, e
    a anterior segue no ar por **180 dias** contados da abertura da seguinte — parâmetro
    declarado na implantação, como o prazo de apresentação da URL da chave (§8).
12. **Modelos de IA do Ciclo 01: Google Gemini.** Toda funcionalidade que precisar de modelo
    de IA neste ciclo é atendida por modelos **Gemini** — assistente do Guerreiro(a), leitura
    da produção e assistente da Área do Apoiador Desenvolvedor —, com o custo lançado no
    livro-razão como recurso de _cloud_. O consumo é feito pela **API do Gemini**, de
    **endpoint global**: no Ciclo 01 a região de processamento não é escolhida, porque o
    Vertex AI, que a permite escolher, custaria o _free tier_ que sustenta o ciclo — a
    revisão fica para o Ciclo 02 (documento 09). A **biometria facial do App 01 não usa
    modelo de linguagem** e é resolvida no próprio aparelho (§3.3).
13. **Stack e hospedagem do Ciclo 01.** O Backend API é escrito em **Python 3.12 com FastAPI**
    e roda em **Cloud Run**; o banco é **Cloud SQL para PostgreSQL com PostGIS**, onde ficam
    também as **séries temporais do território**, particionadas por tempo; os arquivos de
    missão vão para o **Cloud Storage**. Tudo na região **`southamerica-east1`** (São Paulo).
    São **dois ambientes**: **desenvolvimento**, em contêiner local com banco próprio, e
    **produção**, no Cloud Run. Contêiner e banco são portáteis — outra comunidade replica a
    plataforma fora do Google Cloud. O custo entra no livro-razão como recurso de _cloud_,
    **aportado por absorção pelo Admin e Mestre fundador** neste ciclo. Em produção o Cloud Run
    roda **sem escala horizontal** no Ciclo 01 — no máximo um contêiner de cada vez —, porque o
    freio das rotas públicas conta em memória (§8) e cada contêiner a mais multiplicaria o
    limite. Não confundir com o princípio 10: lá "instância única" é uma base para todas as
    comunidades; aqui é quantos contêineres atendem ao mesmo tempo.

    Os **sete frontends** são **React com TypeScript sobre Vite**, exceto a **vitrine
    (App 06)**, escrita em **Astro** por ser a única indexável por buscadores — as outras seis
    são inteiramente autenticadas e nada têm a indexar. Todas geram **saída estática**, servida
    pelo **Firebase Hosting**, um site por aplicação e por ambiente: sem runtime de servidor, o
    custo cabe no free tier que sustenta o ciclo e qualquer comunidade serve os arquivos onde
    quiser.

14. **Repositório único (_monorepo_)** — o Backend API, as oito aplicações, os jogos, a
    documentação e os artefatos de implementação vivem no mesmo repositório, com uma pasta
    por aplicação (§1.2). É organização do código, não acoplamento: cada frontend continua
    com implantação e endereço próprios (princípio 3). Um repositório só é o que faz a
    replicação por outra comunidade caber num `git clone` (princípio 4).

### 1.1 Como cada persona entra

| Persona                      | Como autentica                                                                                                                                                                                                 |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Guerreiro(a)**             | **Nick + imagem**, em **toda aplicação com login**: o nick localiza, a imagem confirma contra o _template_ biométrico gravado no onboarding; sessão curta, porque o aparelho do ponto de apoio é compartilhado |
| **Mestre, Apoiador e Admin** | **Login social (Google)**                                                                                                                                                                                      |
| **Responsável**              | **Login social (Google)** ou **usuário e senha** criados por Admin ou Mestre                                                                                                                                   |

- **Duas aplicações não têm login:** a **vitrine (App 06)** e o **jogo (App 04)** são abertos a
  qualquer visitante e só leem dados já públicos. Ninguém se identifica para usá-las — a
  **chave da API é da aplicação, não da pessoa**: as duas carregam a sua e o visitante segue
  anônimo.
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
- **O sensor construído pelo Guerreiro(a) entra por credencial de dispositivo**, emitida e
  revogada por **Admin ou pelo Mestre autor do desafio** da série, com identificador e segredo
  vinculados ao Guerreiro(a) e à série que ele alimenta. Ela é **do aparelho, nunca da
  criança**, e não amplia direito, como a chave da aplicação: não abre sessão, não lê dado
  algum e só registra medição na série a que está presa. O segredo é devolvido uma única vez,
  a revogação exige motivo e autoria e a credencial **cai ao encerramento da série** que ela
  alimenta — o aparelho não sobrevive à medição que o justificava.
- **A credencial é o próprio registro do aparelho**: guarda o identificador dele e a trilha em
  que foi construído, e não há cadastro de dispositivo além dela. Aparelho que alimenta mais de
  uma série tem **uma credencial por série**, todas com o mesmo identificador — e nunca duas
  vivas para a mesma série.

A API é documentada em **OpenAPI/Swagger desde o primeiro _endpoint_** — condição prática para
que aplicações de terceiros e novos frontends realmente surjam. O schema e a interface ficam
**fora do prefixo de versão e abertos**, sem chave: quem ainda não tem uma precisa ler o
contrato para decidir pedi-la (§8). Descrevem rotas e não devolvem conteúdo, de modo que a
exigência de chave do princípio 2, que alcança os dados sob `/v1`, segue inteira.

### 1.2 Organização do repositório

Uma pasta por aplicação, com o número da aplicação no nome — o mesmo número usado neste
documento e nos PRDs, para que ninguém precise traduzir nomenclatura:

```text
comunidade-game/
├─ backend/                     Backend API — o núcleo que todas consomem
├─ apps/
│  ├─ app-01-aula-presencial/
│  ├─ app-03-gestao/
│  ├─ app-05-guerreiro/
│  ├─ app-06-vitrine/
│  ├─ app-07-responsaveis/
│  ├─ app-08-apoiador/
│  └─ app-09-mestre/
├─ jogos/
│  └─ app-04-arena/             jogo em Phaser; novo jogo entra como irmão
├─ comum/                       o que as oito compartilham — tokens e carta
├─ docs/                        documentação do produto — o site MkDocs
└─ openspec/                    artefatos de implementação
```

A pasta `comum/` é irmã de `apps/` e de `jogos/` porque o jogo consome os mesmos tokens: o
compartilhado não pode morar dentro de uma das aplicações que o consomem.

O jogo fica fora de `apps/` por dois motivos: a API aberta admite **outros jogos** sobre o
mesmo contrato (documento 11), e é o código que o Guerreiro(a) altera como atividade de
trilha — separar deixa claro o que se pode mexer.

Pasta de código nova nasce com a **verificação automática dela no CI**, na mesma esteira que
já roda para a documentação; a regra de entrega está no `CONTRIBUTING.md`.

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
| **App 04** | **Jogo em JavaScript** — sobre a base de personagens da plataforma                                 | Público geral, sem login                     | §6      |
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
senha. Não é avatar, não vai para a vitrine, não aparece em ranking, não é compartilhada. O
_template_ nasce **no próprio aparelho**, e a fotografia não trafega (§3.3).

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

**A sessão de trabalho do aparelho é a janela da aula agendada.** O Mestre ou Admin autentica o
aparelho ao abrir a aula, e ele opera até o horário final declarado no agendamento; encerrada a
aula, o aparelho exige nova autenticação. Não há prazo próprio a calibrar: quem delimita é o
agendamento que já rege o funcionamento do App 01.

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
- **Minimização, com o processamento no aparelho**: o _template_ biométrico — representação
  matemática não reversível — é gerado **no navegador do próprio aparelho**, pela biblioteca
  aberta **Human**, na ordem **prova de vivacidade e, depois, descritor facial**. Ao núcleo
  vai **apenas o descritor**: a fotografia não trafega e é descartada na geração. A plataforma
  não recebe nem guarda rosto de criança.
- **Comparação sempre no núcleo**: o aparelho gera o descritor e **nunca recebe** o _template_
  guardado — nenhuma rota o devolve. Como o descritor nasce em código que roda no aparelho, a
  garantia da entrada é **também** presencial: o App 01 só opera com aula agendada, em
  aparelho do ponto de apoio e com Mestre ou Admin presente (§3.2).
- **Segurança**: o _template_ é guardado **cifrado**, com a chave de cifragem no **Secret
  Manager**, lida na subida do serviço — a cifra roda no próprio núcleo, sem chamada externa a
  cada entrada, e trocar de hospedagem só troca de onde a chave vem. **Todo acesso ao
  _template_ é auditado**, inclusive cada comparação de login, com guarda permanente.
- **Retenção**: o _template_ é guardado enquanto durar o vínculo do Guerreiro(a) com o projeto
  e excluído automaticamente ao fim dele, ou a pedido do responsável, nos prazos da §12.2.

- **Direito de recusa**: quem não autoriza a imagem tem **alternativa equivalente** — nick mais
  confirmação do Mestre ou de um Admin, **no encontro**, tanto para registrar presença quanto
  para entrar nas aplicações. Recusar biometria nunca pode significar exclusão da atividade.
- **Transparência**: política de privacidade em linguagem simples — para o responsável **e
  para a criança**.

### 3.4 Requisitos não funcionais

- Funcionar em **rede instável** e em aparelhos modestos, com fila local de sincronização.
- **Rede fora:** a **presença** entra na fila local, confirmada pelo Mestre ou por um Admin
  pelo nick, e sincroniza quando a rede voltar. **Cadastro novo e reconhecimento facial exigem
  rede**: o descritor nasce no aparelho, mas a comparação é no núcleo, e nem imagem nem
  _template_ de criança ficam guardados no aparelho compartilhado.
- Registro de presença de Guerreiro(a) conhecido em **poucos segundos** — a aula não pode
  travar na porta.
- Acessibilidade: a modalidade áudio atende quem ainda não lê com fluência e pessoas com
  deficiência visual.

## 4. App 01 — Aula presencial: trilhas, equipes e assistente

O segundo caminho do App 01 é o que a turma usa durante o encontro: **o conteúdo das trilhas,
em equipe**. A aula presencial tem **um aparelho por equipe**, em quantidade que varia a cada
encontro — o mesmo aparelho em que a equipe acompanha a missão da trilha, responde ao Quiz ao
Vivo e conversa com o assistente. A entrada é a de sempre: **nick e imagem** (§1.1).

### 4.1 Equipes formadas na hora

**As equipes são formadas pelos próprios Guerreiros e Guerreiras, aqui no App 01**, e valem
para **aquela aula**: começam e terminam com o encontro. Tamanho, composição e a regra do
familiar seguem o documento 02. A gestão **não forma nem edita equipe** — vê as equipes do dia
no painel da App 03.

- O Guerreiro(a) pode integrar **mais de uma equipe** no mesmo encontro e nas demais atividades
  presenciais.
- **No Quiz ao Vivo, cada Guerreiro(a) joga por uma única equipe** — a partida é simultânea e a
  resposta do aparelho vale para todos os integrantes. A disputa continua sendo entre **várias
  equipes**; o que é único é a equipe de cada jogador.

### 4.2 Conteúdo da trilha, quiz e assistente

Arquitetura: **JavaScript no frontend + IA no backend**, a mesma base técnica do Robô Educa. A
equipe vê **em que missão da trilha está**, o conteúdo e a atividade do dia, e conversa com o
assistente **por voz ou por texto**: quiz e explicação de conceitos das trilhas. O assistente
segue **o mesmo desenho do assistente da App 05** (§7): modelo **LLM Google Gemini**, **corpus
fechado** no conteúdo que os Mestres cadastraram, guardrails educacionais, filtros de segurança
no nível mais restritivo e **guarda apenas da transcrição**, com o áudio descartado. A
personalização também segue o desenho de §7.1 — adapta na sessão, reescreve dentro do corpus e
marca o texto gerado por IA.

A equipe também **entrega aqui a produção da missão do dia**, por escrita, fala ou foto do que
fez à mão, com a mesma regra da App 05 (§7): devolutiva construtiva, foto e áudio descartados
na leitura, resultado lançado pelo Mestre.

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

**Acesso do Mestre a esta aplicação:** **leitura do painel do dia**, **condução do Quiz ao
Vivo das aulas que ministra** e **homologação da equipe da trilha** das suas trilhas, ato
presencial que ele pratica no mesmo encontro (documento 02 §5). Fora isso, tudo o que ele
escreve continua na App 09.

## 6. App 04 — Jogo em JavaScript

Jogo executado no navegador, construído sobre a **base de personagens da plataforma**: os
avatares, poderes, badges e níveis já conquistados são os elementos do jogo.

> **Engine definida: [Phaser.js](https://phaser.io/)** — framework de jogos 2D em JavaScript
> que roda no navegador, sem plugin nem instalação, e funciona bem em celular modesto. Escolha
> coerente com Web App / Mobile First e com o objetivo de que o **código seja legível e
> alterável pelos próprios Guerreiros e Guerreiras**.

**Definição vigente — jogo público, sem login, que lê a plataforma e não escreve nada nela.**
Qualquer visitante joga, sem se identificar. O jogador escolhe seu personagem **estritamente
na lista dos Guerreiros e Guerreiras com divulgação autorizada** pelo responsável — a mesma
regra da vitrine —, e o personagem entra na partida com o que aquele Guerreiro(a) já
conquistou: pontos regulares, pontos extras, poderes, badges e níveis. Quanto maior a evolução
no jogo real, mais forte e mais distinto o personagem no App 04.

- **A partida não volta para a plataforma.** Vencer ou perder quantas partidas for **não
  credita, não debita e não registra nada** no perfil do Guerreiro(a) — o jogo não é fonte nem
  destino de pontos.
- Jogar muito **não** sobe ninguém no ranking — o ranking mede aprendizado e realização na
  vida real.
- Elimina, por construção, a principal via de fraude: sem nenhuma escrita, não há o que
  automatizar.
- **Quem não tem divulgação autorizada não vira personagem** — nem para si mesmo. Sem login,
  o jogo não tem como distinguir quem está jogando, e a lista é a mesma para todo visitante.

**Definição vigente — arena de duelo por turnos.** A partida é um duelo curto de um personagem
contra um adversário conduzido pelo computador, em turnos alternados de ataque, habilidade e
defesa. É o gênero que mais expõe a evolução real: cada virtude do Guerreiro(a) vira atributo
visível do personagem, pelo mapa do documento 11. O adversário é dimensionado pelo personagem
escolhido, de modo que a partida segue disputada em qualquer faixa de evolução.

**Joga sem rede e aceita dois jogadores no mesmo aparelho.** O catálogo de personagens fica
guardado no aparelho para a partida rodar offline e é **revalidado a cada reconexão** — sem
rede não se atualiza a lista, mas se joga. O catálogo guardado vale por **7 dias** sem nenhuma
reconexão: vencido o prazo, o jogo pede conexão antes de abrir nova partida, e é esse o teto
da defasagem entre uma revogação de divulgação e o aparelho que ficou fora da rede. O duelo
local entre dois personagens escolhidos atende ao uso nas aulas presenciais e não exige
servidor.

Objetivos: dar utilidade lúdica ao progresso das trilhas; servir de conteúdo do **Poder da IA e
Robótica**, já que alterar o código é atividade de trilha — o Guerreiro(a) é um dos
construtores do próprio jogo; e respeitar a regra de representação por **avatares, nunca
imagens reais**.

## 7. App 05 — Área do Guerreiro(a)

**É a aplicação das aulas remotas** e do uso cotidiano fora do encontro presencial — a aula
presencial é atendida pelo App 01 (§§3 e 4).

Web App de uso cotidiano do Guerreiro(a), com **guia e apoio nas trilhas**: qual é a próxima
missão, o que precisa ser feito, o que já foi conquistado e o que está bloqueado. Reúne a
jornada gamificada — poderes, trilhas, desafios semanais, equipes, ranking, recompensas
conquistadas nos marcos e registro de dados do território.

É também o instrumento de **coleta de dados da Comunidade Virtual**: as séries ativas, quando é
a próxima medição, o que já foi registrado e **quantos pontos aquela série está rendendo**. O
Guerreiro(a) seleciona o local do dado entre os cadastrados e, faltando um, solicita a
inclusão.

**O registro de coleta exige rede: sem ela, fica bloqueado até reconectar.** Não há fila local
como a da presença do App 01 — a entrada na App 05 já depende de rede para a conferência da
imagem, e sem sessão aberta não há a quem atribuir o registro.

É onde o Guerreiro(a) **entrega a produção da missão**: escreve, fala ou fotografa o que fez à
mão. A plataforma lê — com o mesmo **modelo Gemini**, na nuvem — e devolve retorno **sempre
construtivo**, apontando o próximo passo em vez
do erro. **Foto e áudio são descartados na leitura** — guardam-se apenas a transcrição e a
devolutiva —, e **o resultado só existe quando o Mestre o lança**: a leitura automática é
hipótese sobre o aprendizado, nunca nota. Quem não quiser ser fotografado ou gravado entrega
ao Mestre no encontro, sem perder a missão.

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

### 7.1 Personalização por IA

**A plataforma adapta na sessão e não perfila a criança.** O guia da trilha e os assistentes
ajustam o que entregam ao Guerreiro(a) **dentro da sessão em curso**: a conversa daquele
momento e o que ele já conquistou orientam a missão sugerida, o exemplo e a explicação.
**Encerrada a sessão, o contexto é descartado** — a plataforma **não infere nem guarda traço
algum** sobre ritmo, dificuldade ou interesse de quem tem 6 a 16 anos. O que alimenta a
adaptação é o que já existe por outra finalidade: missão de sondagem, missões concluídas,
pontos, poderes, badges, nível e trilhas em curso.

Quatro regras fecham o desenho:

- **Reescreve, não inventa.** A IA reformula a explicação do conteúdo que o Mestre cadastrou,
  no vocabulário e no interesse do Guerreiro(a), **sem sair do corpus fechado**, e o texto
  reescrito é **marcado como gerado por IA**: uma **etiqueta visível no início do bloco**, em
  linguagem simples, com link para a nota de transparência da vitrine (§8). Conteúdo novo
  continua sendo autoria do Mestre.
- **Ponte interdisciplinar na hora.** A IA usa o poder que o Guerreiro(a) **já domina** para
  explicar o que ele ainda não domina, como exemplo e analogia, direto na App 05 e sem passar
  pelo Mestre. Virar missão ou conteúdo de trilha continua sendo autoria do Mestre (§11).
- **Filtros de segurança no nível mais restritivo** em toda interação, como no apoio escolar.
- **Auditoria por amostragem** do Admin sobre a reescrita, com a mesma consequência do corpus:
  despublicar o conteúdo de origem, com motivo.

**O responsável vê e desliga.** A App 07 mostra o que alimenta a personalização e o motivo da
recomendação vigente, e permite **desligá-la** a qualquer tempo (§9). Desligada, o Guerreiro(a)
segue a trilha na ordem publicada e lê a explicação original do Mestre — alternativa
equivalente, nunca exclusão da atividade.

**A chave do responsável não alcança a tela coletiva.** Ela vale na App 05, tela individual do
Guerreiro(a). No App 01 o aparelho é da equipe e a reescrita **sempre opera**: a tela não é de
ninguém em particular, e a personalização ali não perfila criança alguma — adapta na sessão e é
descartada com ela. Um integrante com a chave desligada não desliga a reescrita da equipe.

E é o **canal de sugestões do Guerreiro(a)**: ideias de melhoria para atividades, trilhas e
para a própria plataforma são registradas aqui e caem na fila de avaliação da gestão — o mesmo
mecanismo de evolução pactuada do Código de Conduta, estendido à plataforma inteira. O registro
é feito **em texto ou em áudio de até 60 segundos**, transcrito — uma criança de 6 anos fala
melhor do que escreve. **Registrar não pontua; a proposta adotada rende pontos extras e badge**,
e o retorno acontece em até 7 dias na própria plataforma, com o motivo em linguagem simples
quando não for adotada.

## 8. App 06 — Vitrine pública

Web App de acesso público e **sem login** — a chave da API é da aplicação, não do visitante:

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
- **Formulário de solicitação de dados**, para pesquisadores e gestores públicos, com a mesma
  fila de avaliação (§12.3).
- **Área do Apoiador Desenvolvedor** — a porta de quem quer construir sobre a API. É **seção
  da vitrine**, pública e sem login, não uma nona aplicação. Reúne quatro coisas:

  - **Assistente de chat com IA** — modelo **Google Gemini** — que explica **proativamente**
    como a plataforma está montada, com **corpus fechado** na documentação e no repositório —
    fora deles, não responde. **Toda mensagem termina com uma pergunta de múltipla escolha**
    sobre o próximo passo a conhecer: é o que conduz quem chegou sem saber o que perguntar.
  - **Link para a documentação** publicada com MkDocs.
  - **Formulário de solicitação de chave**, na mesma fila de avaliação dos Admins. Emitida a
    chave, o solicitante tem **30 dias para apresentar a URL** do que construiu; não
    apresentada no prazo, **a chave é revogada**, e nova solicitação é sempre possível. A chave
    de terceiro é sempre de **produção** — desenvolvimento é ambiente das aplicações do
    projeto — e **cada solicitação aprovada rende uma chave**: é a solicitação que identifica a
    chave, não o nome da aplicação, que dois terceiros podem repetir. A emissão entrega ao
    solicitante **o identificador da chave e o segredo** — o identificador é o que ele
    apresenta ao registrar a URL, e o prazo de apresentação é **parâmetro declarado na
    implantação**, com os 30 dias como valor inicial.
  - **Link para o repositório no GitHub.**

  A chave é o que dá acesso à API — **sem ela a plataforma não responde** — e é também o que
  permite homologar a aplicação como aporte em código (documento 14). Ela não amplia direito
  nenhum: o contrato de somente leitura do documento 11 vale igual para toda aplicação de
  terceiro.

- **Aportes exibidos em moedas da plataforma**, nunca em reais (documento 04).
- **Painel público da Comunidade Virtual** — dados do território em **série histórica**, em
  **visão macro**, agregados **até o bairro** e anonimizados (documento 02), abertos à consulta
  da comunidade e de instituições.
- **Portfólio de criações originais** — as criações dos Guerreiros e Guerreiras autorizados,
  com o nick do autor (ou dos autores, em equipe).
- **Sem favoritos e sem qualquer preferência guardada** — nem no servidor, nem no aparelho do
  visitante. Quem pede para favoritar ou acompanhar alguém é levado à **apresentação da Área do
  Apoiador**, com o formulário de solicitação e o caminho de apoio: acompanhar é função de quem
  se cadastra, não da vitrine.
- **Proteção das rotas públicas**: a consulta por nick exato e o envio dos dois formulários têm
  **limite por origem e janela de tempo, com atraso progressivo** a cada repetição — é o que
  barra a varredura de nicks e o envio abusivo. **Sem CAPTCHA**, que é barreira de
  acessibilidade, e **sem cadastro ou coleta de dado do visitante**. Em separado corre a
  **cota de consulta por chave**, em duas faixas, cujo excesso responde **429**. Ela conta
  **só as chamadas de leitura**: a escrita das aplicações do projeto não tem cota, e para a
  chave de terceiro, que é somente leitura, toda chamada entra na conta.

  | Limite                     | Faixa ou superfície              | Valor                        |
  | -------------------------- | -------------------------------- | ---------------------------- |
  | Cota por chave do projeto  | as oito aplicações e os jogos    | 6.000 consultas por hora     |
  | Cota por chave de terceiro | emitida por aprovação de Admin   | 600 consultas por hora       |
  | Consulta por nick          | por origem                       | 30 por 10 minutos            |
  | Envio de formulário        | por origem, participação e dados | 3 por hora                   |
  | Atraso ao exceder          | as duas superfícies por origem   | 2s, dobrando, teto de 15 min |

  A **origem** é o **resumo criptográfico do IP com sal rotativo**, mantido **só em memória**
  pela janela do freio e **nunca gravado em banco** — é o que faz o limite existir sem guardar
  dado do visitante. Por isso o Cloud Run roda **sem escala horizontal** no Ciclo 01 (§1,
  princípio 13): cada contêiner contaria por si, e o limite valeria multiplicado. O serviço
  também **não mantém contêiner ocioso**, e por isso o freio **reinicia a cada partida a
  frio** — contrapartida aceita no Ciclo 01 para o custo caber no _free tier_. O
  **formulário de solicitação de chave não tem freio por origem** — nova solicitação é sempre
  possível —, e o que o protege é a cota da chave da vitrine.

- **Chamada "Quero participar"** em **toda página individual** — Guerreiro(a), Mestre, poder,
  apoiador e comunidade —, levando à **porta da Área do Apoiador**. A chamada é do projeto:
  **nunca vincula o apoio à pessoa exibida na página**.
- **Botão "Entrar"**, sempre visível, que encaminha cada persona à sua aplicação: Guerreiro(a)
  para a App 05, responsável para a App 07, Mestre para a App 09, Apoiador para a App 08,
  gestão para a App 03 e o **aparelho da aula** para a App 01. A vitrine não autentica ninguém
  — quem autentica é a aplicação de destino, na forma de §1.1 —, **não guarda a escolha** e não
  revela quem existe na plataforma. Quem não tem cadastro recebe a orientação da sua persona:
  pré-cadastro do Apoiador, formulário de participação do Mestre e, para o responsável e o
  Guerreiro(a), procurar a gestão no encontro.
- Seções **"Quem somos"** e **"Contatos"**, editáveis pelos Admins. A **nota de transparência
  sobre IA** vive **dentro de "Quem somos"**, e não em seção própria: declara que a plataforma
  é construída com Claude e atende as pessoas com Gemini (documento 01), que a IA **reescreve
  conteúdo do corpus do Mestre para crianças e não as perfila**, e remete à linha "Licenças"
  quanto ao que é gerado com auxílio de IA. É para ela que aponta a etiqueta do texto reescrito
  nas Apps 01 e 05 (§7.1).
- **"Como apoiar"** — canais de doação, incluindo a chave PIX da pessoa jurídica vinculada.
- Identidade visual: a da plataforma, no temperamento **Arena** (documento 15).
- **Vídeo de apresentação**: os irmãos Susy e Otávio, os Rôbróders e o professor Carlos
  Trenell (narrativa da trilha Robô Educa).
- **Sem publicidade e sem patrocínio no Ciclo 01** — e **sem cookie, rastreador ou
  perfilamento** do visitante, para qualquer finalidade (documento 04).

A vitrine é uma só e **sem login**. O que muda por público é o **recorte de leitura** — a porta
de entrada e a ordem do que se mostra primeiro, sobre os mesmos dados públicos:

| Recorte               | Quem chega procurando                | O que a porta abre primeiro                                                                |
| --------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------ |
| **Sociedade civil**   | Conhecer, acompanhar e apoiar        | Narrativa, cards, criações originais, batalhas e "Como apoiar" — é o recorte **padrão**    |
| **Pesquisadores**     | Dado do território para estudo       | Séries históricas por comunidade, com o que se mede, cadência, período e origem do dado    |
| **Gestores públicos** | Evidência sobre o lugar para decidir | Painel do território por comunidade e ciclo e a cobertura da Agenda 2030, com a meta 17.18 |

**Área do gestor público.** O recorte de gestores abre com um bloco em destaque que explica, na
linguagem de quem decide, **para que a plataforma serve ao município e ao estado**: a série
histórica do território por bairro, com metodologia declarada; a cobertura da Agenda 2030 por
comunidade e ciclo; a entrega gratuita do conjunto na íntegra sob solicitação aprovada; e o
código aberto, que permite replicar o modelo em outra comunidade. O mesmo bloco declara os
limites: o dado sai **agregado e anonimizado, nunca por Guerreiro(a)**, e **não substitui
indicador oficial** — é evidência produzida por moradores sobre o próprio lugar.

Nenhum recorte cria área restrita, cadastro ou coleta de dado do visitante, e os três obedecem
à regra de saída de sempre: **agregada e anonimizada, nunca por Guerreiro(a)**. Na vitrine o
dado aparece em **visão macro**; quem precisa do **conjunto na íntegra** o solicita pelo
formulário público, e a entrega segue a regra de §12.3.

## 9. App 07 — Área dos pais e responsáveis

Web App autenticado, **canal oficial da plataforma com a família** — o que resolve a
comunicação da evolução do aluno sem depender de aplicativos de mensageria de terceiros. O
responsável acessa apenas os dados dos Guerreiros e Guerreiras sob sua responsabilidade, com
vínculo conferido por um Admin ou por um Mestre.

| Função                       | O que o responsável faz                                                                                                           |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Evolução do Guerreiro(a)** | Acompanha presença, atividades realizadas, pontos, poderes, badges, nível e progresso nas trilhas                                 |
| **Autorização**              | Concede e **revoga** a autorização única do responsável, que vale para divulgação, imagem em eventos e captação da produção (§12) |
| **Solicitações**             | Pede acesso, correção ou exclusão de dados e solicita esclarecimentos — cada pedido com protocolo e prazo                         |
| **Direitos de recusa**       | Recusa, a qualquer tempo, a **imagem do Guerreiro(a)** captada no onboarding, que tem termo próprio                               |
| **Transparência de dados**   | Vê **quais dados da criança estão armazenados**, para que servem, por quanto tempo ficam e quem os acessou                        |
| **Personalização por IA**    | Vê o que alimenta a personalização e o motivo da recomendação vigente, e **desliga a personalização** a qualquer tempo (§7.1)     |
| **Termos e consentimentos**  | Lê, aceita e consulta o histórico dos termos assinados, com data e hora                                                           |
| **Propostas**                | Registra propostas de evolução da plataforma, na mesma fila de avaliação das sugestões dos Guerreiros e Guerreiras                |

**Regras obrigatórias:**

- **Nenhuma recusa exclui o Guerreiro(a) da atividade.** Todo direito de recusa tem alternativa
  equivalente.
- **A revogação vale para frente e é imediata** na parte pública: o perfil sai da vitrine e
  dos rankings, sem prejuízo da participação.
- **Limite declarado do pedido de exclusão:** os **registros de dados do território** não são
  apagados a pedido — são **despersonalizados**, com o vínculo de autoria rompido e o
  mapeamento destruído (§12.1). Isso precisa estar dito na tela, em linguagem simples, e no
  termo assinado — não descoberto depois.
- **Desligar a personalização não tira conteúdo.** Desligada, o Guerreiro(a) segue a trilha na
  ordem publicada e lê a explicação original do Mestre — é a alternativa equivalente exigida de
  toda recusa (§7.1).
- **A exclusão do _template_ biométrico é avisada antes de acontecer.** Encerrado o vínculo, a
  App 07 exibe ao responsável que o _template_ será apagado, **em que data** e o que isso
  significa caso o Guerreiro(a) volte — nova captura, com novo termo. O aviso vive no canal
  oficial, sem notificação por e-mail, como todo retorno do Ciclo 01.
- **Linguagem simples**, na mesma medida exigida da política de privacidade.
- **Responsável sem smartphone não fica de fora:** o ato pode ser feito por **atendimento
  assistido** — Admin ou Mestre abre a aplicação com ele presente, gravando quem operou e quem
  testemunhou — ou por **termo impresso digitalizado** e anexado pela gestão. Nos dois casos o
  registro entra versionado, em nome do responsável.
- **Sem contato direto com Apoiadores ou terceiros**: a área é canal entre família e
  plataforma, e nada mais.
- Todas as solicitações caem na fila de atendimento da App 03, com registro de tratamento.

**Prazo de resposta: 7 dias** para toda solicitação do responsável. **No Ciclo 01 não há
notificação por e-mail**: o retorno acontece na própria plataforma, na área do responsável.

## 10. App 08 — Área do Apoiador

Web App dos Apoiadores, com uma **porta pública de pré-cadastro** e a área autenticada de quem
já foi cadastrado por um Admin. É onde o apoio deixa de ser um lançamento feito por terceiros e
passa a ter canal próprio:

| Função                        | O que o Apoiador faz                                                                                                                                |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pré-cadastro**              | Identifica-se, escolhe o perfil e o que vai aportar, anexa o comprovante e entra na fila de avaliação                                               |
| **Identidade pública**        | Define o **avatar** — logomarca ou imagem escolhida — e o **nick** que aparecem no seu card                                                         |
| **Meus aportes**              | Acompanha o que aportou, em **moedas**, e o **Poder Sustentador** acumulado                                                                         |
| **Missões**                   | Vê as missões abertas, cobre uma delas e acompanha o **nível de sustento** e os **selos** que conquistou (documento 14)                             |
| **Desafios extras**           | Propõe desafios abertos ou direcionados e acompanha validação do Mestre e aprovação do Admin                                                        |
| **Efetividade do apoio**      | Vê o que os desafios produziram — sempre **agregado e por avatar**                                                                                  |
| **Acompanhamento**            | Vê os **mesmos dados do painel público** e mantém **favoritos** — Guerreiros e Guerreiras pelo nick e Mestres —, com as novidades deles em destaque |
| **Documentos comprobatórios** | Envia currículo, portfólio, redes sociais, termos e comprovantes para o Admin anexar ao seu cadastro                                                |
| **Propostas**                 | Registra propostas de evolução da plataforma, que caem na fila de avaliação da gestão                                                               |

**Regras obrigatórias:**

- **Nenhum contato direto com Guerreiro(a) ou família.** Proposta, entrega e reconhecimento
  seguem mediados pela plataforma; a App 07 não é compartilhada com Apoiadores. **Favoritar é
  leitura**: não abre canal, não avisa a criança e não dá acesso a nada além do que já é público.
- **O que é novidade do favorito**: **criação original publicada, badge novo, nível novo,
  resultado de batalha e trilha nova publicada pelo Mestre**, em destaque por **30 dias** a
  contar da data do fato. **Favoritar existe só aqui** — a vitrine não guarda favorito de
  ninguém.
- **O nick vem da família, nunca da plataforma.** A busca é por nick exato e alcança apenas
  quem tem divulgação autorizada (documento 02).
- **O pré-cadastro não cadastra ninguém.** Ele grava a solicitação, o aporte declarado e o
  comprovante; o cadastro segue **exclusivo de Admin**, que valida o comprovante na App 03.
- **Três formas de aportar no pré-cadastro**: assumir uma das **necessidades publicadas**,
  transferir um **valor sugerido** ou um **valor livre**, os dois últimos pela chave PIX.
- **O aporte feito pela aplicação é em dinheiro**, no pré-cadastro e nos aportes seguintes de
  quem já é cadastrado. Material, serviço e divulgação entram pelo cadastro do Admin na App 03,
  com termo de doação ou registro do material.
- **Comprovante obrigatório no Ciclo 01** — PDF, JPG ou PNG. Não há confirmação automática de
  PIX: quem confere é o Admin.
- **A identificação não usa documento**: nome ou razão social, e-mail e WhatsApp. A plataforma
  não coleta CPF, CNPJ nem documento de identidade.
- **Aprovado o cadastro e homologado o aporte**, o valor vira **moedas** e o card do Apoiador
  passa a aparecer na vitrine com o total em destaque.
- **Avatar e nick são do Apoiador**, definidos aqui e sujeitos à **auditoria por amostragem**
  da gestão, que pode despublicar com motivo. O **avatar próprio exige 10 moedas acumuladas**;
  abaixo do piso a aplicação mostra o avatar padrão e diz quanto falta para trocá-lo.
- Toda proposta de desafio extra segue o fluxo vigente: validação do Mestre da trilha,
  aprovação de Admin e **lastro antes da publicação**.

## 11. App 09 — Área do Mestre

Web App autenticado dos **Mestres cadastrados** por um Admin. É a bancada de trabalho de quem
ensina: o que o Mestre cria e o que ele conduz nas suas atividades.

| Função                    | O que o Mestre faz                                                                                                                     |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Autoria de trilhas**    | Cria trilhas, missões, conteúdos, bibliografia de apoio, **atividades da missão**, quizzes e desafios — inclusive o de coleta          |
| **Template de missão**    | Cadastra o tópico que quer ensinar e recebe a **estrutura da missão** e o que ainda falta nela, conforme o modelo do documento 11      |
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
- **A IA da autoria monta estrutura, não escreve conteúdo.** A partir do tópico cadastrado ela
  propõe o esqueleto da missão e o checklist do que falta — que tipo de exercício cabe ali, se
  há produção do Guerreiro(a), se a retomada está declarada. **O conteúdo é escrito pelo
  Mestre**, que segue sendo o autor creditado na licença CC BY-SA.
- **A trilha publicada vai ao ar sem aprovação prévia.** A curadoria é posterior: o Admin
  audita por amostragem e pode despublicar, do mesmo modo como audita a coleta.
- **A ferramenta recusa publicar trilha sem missão de sondagem, sem desafio de coleta e sem
  culminância com criação original** — as três regras do documento 02 viram trava, não
  recomendação. A criação entregue é validada pelo Mestre autor da trilha.
- **Cada missão nasce declarada obrigatória ou opcional**, e o Mestre diz se o desbloqueio dela
  libera recompensa e em que cadência ela volta para revisão.
- **Conteúdo da missão:** texto formatado, imagens, link externo e upload hospedado
  pela plataforma — **vídeo até 200 MB e arquivo até 20 MB por missão**, com o
  consumo lançado como recurso de _cloud_ no livro-razão.
- **O upload aceita lista fechada de formatos**: vídeo MP4 e WebM, imagem JPG, PNG e WebP,
  áudio MP3 e documento PDF. O que está fora da lista é recusado no envio — o que fecha a porta
  a executável e a formato que o navegador não abre. **O que é enviado não passa por conferência
  prévia**: cai na auditoria mensal por amostragem do Admin, como a trilha e o corpus de apoio,
  e o Admin despublica com motivo.

## 12. Proteção de dados em toda a plataforma (LGPD)

- Guerreiros e Guerreiras são representados **por avatares, nunca por imagens reais**, em toda
  a plataforma.
- Cards de Guerreiros e Guerreiras **sem links para redes sociais nem contato direto**.
- **Adesão em duas etapas:** o cadastro é **livre** (nome, data de nascimento, nick,
  comunidade e características do avatar) e permite participar de todas as atividades; a
  **divulgação pública do histórico e do perfil** só ocorre **após autorização dos pais ou
  responsáveis**, concedida e revogável pela App 07.
- **A autorização do responsável é uma só.** Ela cobre a divulgação do perfil, do histórico e
  das criações originais, o **uso de imagem em fotos e vídeos de eventos** e a **captação da
  produção do Guerreiro(a)** — foto do manuscrito e áudio da fala. Conceder vale para tudo;
  recusar também, sempre com alternativa equivalente. Fica de fora a **biometria do
  onboarding**, de finalidade própria e termo impresso (§3.3).
- A imagem captada no onboarding é **dado sensível de uso restrito**: serve apenas para
  identificar o Guerreiro(a) — presença e autenticação — e **nunca** é exibida publicamente.
- **O ranking interno da App 05 mostra a turma inteira.** É a exceção declarada à regra da
  divulgação autorizada: ali não há público externo — a tela é logada e os colegas já se
  conhecem do encontro presencial —, e deixar de fora quem não tem autorização apagaria a
  criança do ranking da própria turma. **A vitrine e todas as exibições públicas seguem
  restritas a quem tem divulgação autorizada**, sem exceção.
- **Dados do território: guarda permanente com o coletor identificado**, mesmo depois que o
  Guerreiro(a) deixa o projeto — é o que dá procedência à série e preserva o crédito da
  realização. A **anonimização ocorre na saída**: painéis públicos, exportações, pesquisas e
  entregas a instituições recebem dados **anonimizados**, agregados conforme a finalidade
  (§12.3).
- **A origem do freio das rotas públicas não é dado pessoal.** O resumo criptográfico do IP com
  sal rotativo (§8) não identifica ninguém e não se reverte: o sal troca, o resumo vive só na
  memória pela janela do freio e nunca é gravado. Fica fora do alcance da LGPD pela mesma razão
  da camada de medição do território (§12.1). **A conclusão depende do desenho**: sal fixo ou
  resumo gravado a derrubam, e o tratamento passaria a exigir base legal declarada.

### 12.1 Base legal da guarda do dado de território

Duas camadas, e a distinção entre elas é o que sustenta o desenho:

| Camada                   | O que é                                           | Base legal                                                                        |
| ------------------------ | ------------------------------------------------- | --------------------------------------------------------------------------------- |
| **A medição**            | Valor, local, data — dado do **lugar**            | Anonimizada na saída, **fora do alcance da LGPD** enquanto não identifica ninguém |
| **O vínculo de autoria** | Quem coletou — único dado **pessoal** do registro | **Consentimento específico e em destaque do responsável**, revogável              |

- **Titularidade não se transfere.** O titular do vínculo de autoria é o Guerreiro(a); o
  responsável **exerce os direitos** em nome dele. É o máximo que a lei admite nessa direção, e
  é o que o projeto pratica.
- **Revogação despersonaliza, não apaga.** Revogado o consentimento, a plataforma **rompe o
  vínculo de autoria e destrói o mapeamento**: o registro permanece na série com um **código de
  coletor sem correspondência a pessoa alguma**, preservando a consistência da série sem
  preservar dado pessoal. É a resposta concreta ao pedido de exclusão, e o termo diz isso antes
  do aceite.
- **A base de pesquisa entra quando a entidade existir.** A retenção nominal por prazo
  indeterminado só se apoia em pesquisa (LGPD art. 7º, IV e art. 16, II) quando houver
  **pessoa jurídica sem fins lucrativos** com pesquisa na missão institucional — a empresa
  vinculada hoje não se enquadra. Até lá, a camada pessoal se sustenta em consentimento, e é
  por isso que toda entrega a terceiros sai **anonimizada** (§12.3).
- **Risco de reidentificação**: em comunidade pequena, código de coletor somado a data e local
  fino ainda pode apontar uma criança. Por isso a saída pública agrega até o bairro (documento
  02), e rua, condomínio, bloco e quadra só saem nas entregas aprovadas (§12.3).

### 12.2 Prazos de guarda

| Dado                                              | Prazo                                                             |
| ------------------------------------------------- | ----------------------------------------------------------------- |
| Transcrição de consulta respondida (Apps 05 e 01) | **7 dias** vinculada ao Guerreiro(a); depois só disciplina e data |
| Transcrição de consulta recusada pelos filtros    | **Até o fim do ciclo**, restrita à gestão                         |
| Transcrição de sugestão não adotada               | **90 dias** após o retorno a quem sugeriu                         |
| Transcrição de sugestão adotada                   | Permanente, com autoria — é contribuição creditada                |
| Foto e áudio da produção do Guerreiro(a)          | **Descartados na leitura**; ficam a transcrição e a devolutiva    |
| Áudio de qualquer origem                          | **Descartado na transcrição**                                     |
| Contexto de personalização da sessão              | **Descartado ao encerrar a sessão**; nada é inferido nem gravado  |
| Motivo da ocorrência de conduta                   | **Até o fim do ciclo** em que ocorreu; o lançamento é que fica    |
| _Template_ biométrico, fim do vínculo             | **30 dias**, com aviso prévio ao responsável                      |
| _Template_ biométrico, pedido do responsável      | **5 dias**                                                        |
| Métricas de custo e demanda de IA                 | Permanente, **sem nenhum dado pessoal** — só contadores           |

**Fim do vínculo** é o marco desses prazos: ocorre **por pedido do responsável** ou
**automaticamente após 12 meses sem nenhuma atividade registrada** — prazo que cobre o
intervalo entre ciclos sem manter biometria de quem já saiu.

**Ocorrência de conduta**: apaga-se a **descrição da conduta**, não o lançamento. Ao fim do
ciclo — o mesmo marco em que a ocorrência sai do ranking (documento 11) — resta o lançamento
negativo com valor, data e autor, sem o texto que descreve o que a criança fez.

**Sessão em aparelho compartilhado**: encerra por **10 minutos de inatividade**, com aviso um
minuto antes e opção de continuar, além do botão de sair sempre visível. O risco tratado aqui
é a próxima criança ver os dados da anterior.

- **Georreferenciamento sem expor endereço de criança**: a granularidade publicada nunca pode
  permitir inferir onde um Guerreiro(a) específico mora — daí o corte no bairro (documento 02).
- **Aviso visível em toda aplicação:** onde há coleta de dado, o app indica ao usuário — de
  forma discreta e elegante, sem interromper o uso — o que está sendo coletado e quais são os
  seus direitos, com acesso a uma **área detalhada** que explica destino e uso de cada dado.
- A LGPD deve ser considerada em **todos** os módulos e PRDs, não como item pontual.

Vídeos de culminância e fotos de eventos em que Guerreiros e Guerreiras apareçam seguem a
mesma autorização única do responsável, sem termo à parte por divulgação.

### 12.3 Entrega de dados a pesquisadores e gestores públicos

**Definição vigente.** No Ciclo 01 os dados produzidos pela plataforma são disponibilizados
**gratuitamente**, em duas formas:

| Forma                        | Quem acessa                       | O que sai                                          |
| ---------------------------- | --------------------------------- | -------------------------------------------------- |
| **Vitrine pública (App 06)** | Qualquer visitante, sem login     | Visão **macro e agregada**, por comunidade e ciclo |
| **Entrega sob solicitação**  | Pesquisadores e gestores públicos | O **conjunto na íntegra**, anonimizado             |

- A solicitação é **prévia** e depende de **aprovação de um Admin**, que registra quem pediu,
  para que finalidade e o que foi entregue. Sem aprovação não há entrega, e a recusa é
  registrada com motivo. O **prazo de resposta é de 7 dias**, o mesmo de toda solicitação da
  plataforma.
- A entrega é **anonimizada** em qualquer granularidade aprovada: nenhum conjunto sai com
  vínculo de autoria, nome ou nick de Guerreiro(a).
- No Ciclo 01 a **entrega corre fora da plataforma**: o núcleo registra quem pediu, a
  finalidade, a aprovação ou a recusa com motivo e o que foi entregue, e o Admin gera e envia o
  conjunto por canal próprio. Rota de download espera demanda que a justifique.
- O conjunto sai em **CSV** para as séries, com uma tabela por arquivo e cabeçalho declarado,
  **GeoJSON** para a geometria e um **dicionário de dados** que descreve cada campo, a
  unidade, a cadência e a origem. Formatos abertos, legíveis em planilha e em SIG.
- O conjunto é licenciado em **CC BY-SA**, a mesma licença do conteúdo educacional: quem usa
  credita a comunidade que produziu o dado, e o derivado herda a licença.
- O Admin **aprova** o pedido com solicitante identificado, finalidade declarada compatível
  com pesquisa ou política pública e compromisso de não tentar reidentificar ninguém. A
  **recusa** é registrada com motivo, nessas mesmas três frentes.
