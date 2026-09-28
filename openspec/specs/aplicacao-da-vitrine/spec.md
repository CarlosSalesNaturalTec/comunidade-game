# aplicacao-da-vitrine Specification

## Purpose
A App 06 é a cara pública do projeto e a raiz do domínio da plataforma: a única superfície que
qualquer pessoa alcança sem se identificar, e que por isso não guarda nada de quem visita. Esta
capacidade cobre como a vitrine se apresenta sem login nem cadastro, como ela se identifica ao
núcleo mantendo o visitante anônimo, o que ela deliberadamente não faz — cookie, rastreador,
publicidade, preferência de visitante e autenticação —, os três recortes de leitura como
navegação e o botão "Entrar", que encaminha cada persona à aplicação dela.

## Requirements

### Requirement: A vitrine é pública, abre na raiz do domínio e não tem área restrita

A App 06 SHALL abrir inteira **sem login e sem cadastro**, servida na **raiz do domínio** da
plataforma. NEVER SHALL oferecer tela de cadastro, de área restrita ou de sessão própria, e
NEVER SHALL escrever qualquer coisa sobre um Guerreiro(a). (`RF-03-01`, `RN-03-01`)

#### Scenario: Visitante abre a vitrine

- **WHEN** alguém abre o endereço da raiz do domínio
- **THEN** a vitrine se apresenta inteira, sem pedir login nem cadastro

#### Scenario: Não há área restrita por onde entrar

- **WHEN** o visitante percorre a vitrine
- **THEN** nenhuma tela oferece cadastro, área restrita ou sessão da própria vitrine

### Requirement: A vitrine se identifica por chave de aplicação e o visitante segue anônimo

Toda chamada da App 06 ao núcleo SHALL levar a **chave da própria aplicação**, e NEVER SHALL
levar credencial de persona: a vitrine não tem persona autenticada. (`RN-03-33`)

#### Scenario: A aplicação se identifica com a própria chave

- **WHEN** a App 06 chama uma rota de dados do núcleo
- **THEN** a chamada leva a chave da App 06, e não a de outra aplicação

#### Scenario: Nenhuma chamada carrega credencial de persona

- **WHEN** a App 06 chama qualquer rota do núcleo
- **THEN** a chamada não leva credencial de persona alguma

### Requirement: A vitrine não guarda nada do visitante, no servidor ou no aparelho

A App 06 NEVER SHALL instalar cookie de rastreio, rastreador ou perfilamento do visitante, para
finalidade nenhuma, e NEVER SHALL guardar no aparelho preferência, escolha ou histórico de quem
visita. Havendo medição de audiência, ela SHALL ser agregada e sem identificador de visitante.
(`RF-03-51`, `RN-03-22`, PRD-03 §10)

#### Scenario: Nada é gravado no aparelho depois de uma visita inteira

- **WHEN** o visitante navega pela vitrine, troca de recorte e abre a pergunta do "Entrar"
- **THEN** nada da visita fica guardado no aparelho

#### Scenario: Nenhum rastreador de terceiro é carregado

- **WHEN** a vitrine carrega
- **THEN** nenhum cookie de rastreio, rastreador ou perfilamento é instalado

### Requirement: A vitrine não veicula publicidade nem patrocínio

A App 06 NEVER SHALL exibir publicidade ou patrocínio, e NEVER SHALL reservar espaço de tela
para eles. (`RF-03-50`, `RN-03-21`)

#### Scenario: Nenhuma tela traz anúncio

- **WHEN** o visitante percorre a vitrine
- **THEN** nenhuma tela exibe publicidade ou patrocínio, nem espaço reservado a eles

### Requirement: A vitrine oferece os três recortes de leitura, com sociedade civil como padrão

A App 06 SHALL oferecer os **três recortes de leitura** — sociedade civil, pesquisadores e
gestores públicos — e SHALL abrir no recorte **sociedade civil** sem que o visitante escolha
nada. (`RF-03-25`)

#### Scenario: A vitrine abre no recorte padrão

- **WHEN** o visitante abre a vitrine sem escolher recorte
- **THEN** ele está no recorte sociedade civil

#### Scenario: Os outros dois recortes estão alcançáveis

- **WHEN** o visitante procura outro recorte
- **THEN** pesquisadores e gestores públicos estão oferecidos na navegação

### Requirement: Trocar de recorte é navegação, e não cria área restrita nem coleta dado

A troca de recorte SHALL mudar a porta de entrada e a ordem do que é apresentado, e NEVER SHALL
mudar o conteúdo público disponível nem o direito de acesso. NEVER SHALL criar área restrita,
pedir cadastro, coletar dado do visitante ou guardar o recorte escolhido. (`RF-03-26`,
`RF-03-51`, `RN-03-22`)

#### Scenario: O recorte não muda o direito de acesso

- **WHEN** o visitante troca do recorte sociedade civil para pesquisadores
- **THEN** ele segue na mesma vitrine pública, sem cadastro e sem nada bloqueado

#### Scenario: O recorte escolhido não sobrevive à visita

- **WHEN** o visitante troca de recorte e volta à vitrine depois
- **THEN** a vitrine abre outra vez no recorte sociedade civil

### Requirement: O botão "Entrar" fica sempre visível e pergunta qual persona está entrando

A App 06 SHALL manter o botão **"Entrar"** visível em toda tela pública, e ao ser acionado ele
SHALL perguntar **quem está entrando**, apresentando as personas que têm aplicação: Guerreiro(a),
responsável, Mestre, Apoiador, gestão e o **aparelho da aula**. (`RF-03-58`, PRD-03 §5.9)

#### Scenario: O botão está em toda tela

- **WHEN** o visitante está em qualquer tela pública da vitrine
- **THEN** o botão "Entrar" está visível

#### Scenario: O botão pergunta antes de encaminhar

- **WHEN** o visitante aciona "Entrar"
- **THEN** a vitrine pergunta qual persona está entrando, sem encaminhar ninguém antes da
  resposta

### Requirement: Cada persona é encaminhada à sua aplicação, e a vitrine nunca autentica

Escolhida a persona, a App 06 SHALL encaminhar o visitante ao endereço da aplicação dela —
Guerreiro(a) à App 05, responsável à App 07, Mestre à App 09, Apoiador à App 08, gestão à App 03
e o aparelho da aula à App 01. A vitrine NEVER SHALL conferir nick, imagem, login social, senha
ou qualquer credencial: quem autentica é a aplicação de destino. (`RF-03-59`, `RN-03-27`)

#### Scenario: A persona escolhida chega à aplicação dela

- **WHEN** o visitante declara que é Mestre
- **THEN** ele é encaminhado ao endereço da App 09

#### Scenario: Nenhum campo de credencial existe na vitrine

- **WHEN** o visitante percorre a pergunta do "Entrar" inteira
- **THEN** nenhuma tela pede nick, imagem, senha ou login

### Requirement: A escolha de persona não é guardada

A App 06 NEVER SHALL guardar a persona escolhida, no servidor ou no aparelho: quem volta SHALL
encontrar a mesma pergunta. (`RF-03-60`, `RN-03-22`)

#### Scenario: A pergunta se repete na visita seguinte

- **WHEN** o visitante já escolheu uma persona antes e abre a vitrine outra vez
- **THEN** o "Entrar" pergunta novamente qual persona está entrando, sem escolha pré-marcada

### Requirement: Nenhuma tela de entrada revela nick, conta ou existência de cadastro

As telas do "Entrar" NEVER SHALL apresentar lista de nicks, sugestão, completação ou qualquer
confirmação de que uma conta existe ou não existe na plataforma. (`RF-03-61`)

#### Scenario: A entrada não lista quem existe

- **WHEN** o visitante escolhe a persona Guerreiro(a)
- **THEN** nenhum nick, conta ou cadastro é apresentado ou confirmado

### Requirement: Quem não tem cadastro recebe a orientação da sua persona, sem promessa de acesso

Para cada persona, a App 06 SHALL oferecer a orientação de quem **ainda não tem cadastro**, e
NEVER SHALL prometer acesso: entrar não cria cadastro. A orientação SHALL ser a da própria
persona — **pré-cadastro da App 08** para quem quer ser Apoiador, **formulário de participação da
vitrine** para quem quer ser Mestre, e **procurar a gestão no encontro** para responsável e
Guerreiro(a). Enquanto o formulário de participação não existir na vitrine, a orientação do
Mestre SHALL nomear o caminho em texto, e NEVER SHALL apresentar link que não resolve.
(`RF-03-62`, PRD-03 §5.9)

#### Scenario: Quem quer ser Apoiador é levado ao pré-cadastro

- **WHEN** o visitante declara que é Apoiador e diz que não tem cadastro
- **THEN** a orientação o leva ao pré-cadastro da App 08

#### Scenario: Responsável e Guerreiro(a) são orientados a procurar a gestão

- **WHEN** o visitante declara que é responsável, ou Guerreiro(a), e diz que não tem cadastro
- **THEN** a orientação é procurar a gestão no encontro, sem promessa de acesso

#### Scenario: A orientação do Mestre não oferece link quebrado

- **WHEN** o visitante declara que quer ser Mestre e o formulário de participação ainda não
  existe na vitrine
- **THEN** a orientação nomeia o formulário em texto, sem link

### Requirement: A seção de Guerreiros e Guerreiras apresenta cards que rotacionam a cada 5 segundos

A App 06 SHALL apresentar, no recorte sociedade civil, a seção **Guerreiros e Guerreiras** com
os cards de quem tem autorização vigente, e os cards SHALL **rotacionar a cada 5 segundos**. A
rotação SHALL parar quando o aparelho declarar `prefers-reduced-motion`, e NEVER SHALL ser a
**única via** ao conteúdo: quem não espera a rotação SHALL alcançar os mesmos Guerreiros e
Guerreiras pela navegação da própria seção. (`RF-03-02`, `RF-03-04`, documento 15 §§5, 8.1)

#### Scenario: Os cards rotacionam sozinhos

- **WHEN** o visitante abre a vitrine e permanece na seção de Guerreiros e Guerreiras
- **THEN** os cards trocam a cada 5 segundos, sem que ele acione nada

#### Scenario: Quem pede menos movimento não vê rotação

- **WHEN** o aparelho do visitante declara preferência por movimento reduzido
- **THEN** os cards não rotacionam, e todos seguem alcançáveis

#### Scenario: A rotação não é a única via ao conteúdo

- **WHEN** o visitante quer ver um card que ainda não entrou na rotação
- **THEN** ele o alcança pela navegação da seção, sem esperar a troca

### Requirement: Cada card abre a página individual, em endereço próprio

Cada card SHALL abrir a **página individual** do Guerreiro(a), em **endereço próprio**,
compartilhável e alcançável diretamente. A página SHALL detalhar a trajetória nas trilhas, os
badges e níveis por poder e o portfólio de criações originais com a autoria, na composição do
documento 11 §8.2. (`RF-03-03`, PRD-03 §5.1)

#### Scenario: O card leva à página

- **WHEN** o visitante aciona um card de Guerreiro(a)
- **THEN** a página individual daquele Guerreiro(a) abre, em endereço próprio

#### Scenario: O endereço direto resolve

- **WHEN** alguém abre diretamente o endereço da página de um Guerreiro(a) com autorização
  vigente
- **THEN** a página abre com a composição do documento 11 §8.2

### Requirement: Card e página exibem só avatar, nick, badges, poderes e desempenho

O card e a página do Guerreiro(a) SHALL exibir **avatar, nick, badges, poderes com níveis e
desempenho**, mais as criações originais que a variante do documento 11 §8.2 pede. NEVER SHALL
exibir imagem real, nome civil, rede social, canal de contato ou qualquer outro dado da criança,
em tela nenhuma da vitrine. A vitrine NEVER SHALL oferecer canal de contato com o Guerreiro(a)
ou com a família dele. (`RF-03-05`, `RF-03-06`, `RN-03-04`, `RN-03-05`, invariantes 10 e 12 do
documento 99 §6)

Faltando à leitura o que a variante exige, a carta NEVER SHALL ser apresentada pela metade: a
tela SHALL dizer em uma frase o que tem, como o documento 11 §8.2 determina.

#### Scenario: O card mostra só o que é permitido

- **WHEN** o visitante vê um card de Guerreiro(a)
- **THEN** ele vê avatar, nick, badges, poderes e desempenho, e nenhuma imagem real, nome civil,
  rede social ou contato

#### Scenario: A página não abre canal de contato

- **WHEN** o visitante percorre a página individual inteira
- **THEN** nenhuma tela oferece falar com o Guerreiro(a) ou com a família dele

#### Scenario: Carta incompleta não se apresenta

- **WHEN** a leitura não devolve o que a variante Guerreiro(a) exige
- **THEN** a carta não é apresentada, e a tela diz em uma frase o que tem

### Requirement: A busca é por nick exato, sem lista, sugestão ou completação

A App 06 SHALL oferecer busca por **nick exato**, e NEVER SHALL oferecer sugestão, completação,
lista de nicks ou contagem de resultados parecidos. Havendo autorização vigente, a busca SHALL
levar à página pública daquele Guerreiro(a). (`RF-03-11`, `RF-03-12`, `RN-03-06`, PRD-03 §5.6)

#### Scenario: Nick exato leva à página

- **WHEN** o visitante digita o nick exato de um Guerreiro(a) com autorização vigente
- **THEN** a página pública dele abre

#### Scenario: A busca não sugere nem completa

- **WHEN** o visitante digita parte de um nick
- **THEN** nenhuma sugestão, completação ou lista de nicks é apresentada

### Requirement: Nick inexistente e nick sem autorização recebem a mesma resposta

A App 06 SHALL apresentar **a mesma resposta** de "não encontrado" para nick inexistente e para
nick sem autorização de divulgação vigente, sem revelar qual dos dois casos ocorreu — na busca e
no endereço direto da página. (`RF-03-11`, `RN-03-07`, PRD-03 §§5.6, 5.7)

#### Scenario: Os dois casos respondem igual

- **WHEN** o visitante busca um nick que não existe, e depois um nick sem autorização vigente
- **THEN** as duas respostas são idênticas, e nenhuma diz qual caso ocorreu

#### Scenario: O endereço direto também não distingue

- **WHEN** alguém abre o endereço da página de um nick sem autorização vigente
- **THEN** a tela responde "não encontrado", como responderia a um nick inexistente

### Requirement: Quem não tem autorização vigente não aparece, e a revogação o retira na leitura seguinte

A App 06 NEVER SHALL exibir em card, página, portfólio ou ranking um Guerreiro(a) sem
autorização de divulgação vigente. Revogada a autorização, ele SHALL desaparecer das quatro
superfícies **na leitura seguinte**, e o endereço direto da página dele SHALL responder "não
encontrado". A vitrine NEVER SHALL guardar em cache no aparelho o que leu de um Guerreiro(a), de
modo que a revogação não sobreviva à leitura seguinte. (`RF-03-13`, `RF-03-14`, `RN-03-02`,
`RN-03-03`, `RN-03-22`, PRD-03 §5.7)

#### Scenario: Sem autorização, não aparece em lugar nenhum

- **WHEN** um Guerreiro(a) não tem autorização vigente
- **THEN** ele não está em card, página, portfólio nem ranking, nem por endereço direto

#### Scenario: A revogação vale na leitura seguinte

- **WHEN** o responsável revoga a autorização e o visitante recarrega a vitrine
- **THEN** o Guerreiro(a) já não aparece em nenhuma das quatro superfícies

#### Scenario: A criação em equipe permanece com os demais autores

- **WHEN** um dos creditados de uma criação em equipe tem a autorização revogada
- **THEN** a vitrine apresenta o que o núcleo devolver, sem citar o revogado

### Requirement: A repetição da busca encontra espera crescente explicada, sem CAPTCHA nem cadastro

Freada a origem pela repetição da busca por nick, a App 06 SHALL explicar em **linguagem
simples** o motivo e **quanto tempo falta esperar**, com o tempo que o núcleo devolveu. NEVER
SHALL pedir CAPTCHA, cadastro ou login para seguir, e NEVER SHALL guardar no aparelho qualquer
marca de quem foi freado. (`RF-03-36`, `RF-03-37`, `RN-03-08`, `RN-03-34`, PRD-03 §§5.6, 12)

#### Scenario: A espera é explicada

- **WHEN** o visitante repete a busca por nick até ser freado
- **THEN** a tela diz por que houve a espera e quanto tempo falta, em linguagem simples

#### Scenario: A espera não pede nada do visitante

- **WHEN** o visitante está esperando o freio passar
- **THEN** nenhuma tela pede CAPTCHA, cadastro ou login

### Requirement: O portfólio público exibe as criações autorizadas com trilha, data e autoria

A App 06 SHALL exibir o **portfólio** das criações originais autorizadas, cada uma com a
**trilha** de que nasceu, a **data** em que foi validada e a **autoria por nick** de cada
creditado. NEVER SHALL exibir criação cujo creditado não tenha autorização vigente. O portfólio
SHALL sair **sem título** enquanto a criação original não tiver esse campo no modelo. (`RF-03-08`,
`RN-03-02`, decisão do fundador, 2026-09-28)

#### Scenario: A criação aparece com trilha, data e autoria

- **WHEN** o visitante abre o portfólio
- **THEN** cada criação traz a trilha, a data de validação e o nick de cada autor creditado

#### Scenario: O portfólio não exibe quem não autorizou

- **WHEN** uma criação tem creditado sem autorização vigente
- **THEN** ela não aparece no portfólio

### Requirement: O ranking público exibe só pontos regulares e só quem autorizou

A App 06 SHALL exibir o ranking público com **apenas pontos regulares** e **apenas** Guerreiros
e Guerreiras com autorização de divulgação vigente. NEVER SHALL exibir ponto extra, saldo de
moedas ou valor em reais no ranking. (`RF-03-09`, `RN-03-02`, invariante 16 do documento 99 §6)

#### Scenario: O ranking é de ponto regular

- **WHEN** o visitante abre o ranking
- **THEN** a pontuação exibida é a de pontos regulares, e nenhuma outra

#### Scenario: Quem não autorizou não está no ranking

- **WHEN** um Guerreiro(a) sem autorização vigente teria posição no ranking
- **THEN** ele não aparece, e a numeração exibida não deixa buraco

### Requirement: A seção de poderes apresenta cada poder com as trilhas dele

A App 06 SHALL apresentar a seção **poderes**, com cada poder e as **trilhas** vinculadas a ele,
e a página do poder com as mesmas trilhas. Os **Mestres responsáveis** do documento 11 §8.2
NEVER SHALL ser prometidos nem apresentados vazios enquanto a rota de Mestres não existir: a
seção sai sem eles. (`RF-03-02`, decisão do fundador, 2026-09-28)

#### Scenario: O poder aparece com as trilhas

- **WHEN** o visitante abre a seção de poderes
- **THEN** cada poder aparece com as trilhas vinculadas a ele

#### Scenario: A seção não promete o que ainda não tem

- **WHEN** o visitante abre a página de um poder
- **THEN** nenhum espaço vazio ou promessa de Mestres responsáveis é apresentado
