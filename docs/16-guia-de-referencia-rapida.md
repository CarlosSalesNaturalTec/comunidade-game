# 16 — Guia de Referência Rápida

> **Sequência de telas, não regra.** Este documento diz em que aplicação, em que aba e em que
> ordem cada persona opera a plataforma, e o que trava quando um passo é pulado. É documento
> **derivado**: nenhuma regra nasce aqui. O porquê de cada mecânica está nos documentos 02, 04,
> 05, 11, 13 e 14; os requisitos, nos PRDs.

Serve a dois usos: o primeiro percurso de ponta a ponta em um ambiente novo e a consulta de
quem já opera e esqueceu onde fica alguma coisa.

## 1. A ordem que não se inverte

Cada aplicação tem endereço próprio e sessão própria — não há estado compartilhado entre elas.
Uma identidade social viva pertence a **uma** persona: quem já é Admin não abre sessão de
Mestre com o mesmo e-mail.

```text
  APP 03 — gestão .............. Admin
    Comunidade Virtual ──┐
    Poder ───────────────┤  nada de Guerreiro(a) nem de trilha
    Ponto de Apoio ──────┤  existe antes destes quatro
    Aula na agenda ──────┘
    persona Mestre ──────────────┐
    persona Apoiador ────────┐   │
                             │   ▼
                             │  APP 09 — Mestre
                             │    trilha: sondagem + coleta + culminância
                             │    publica ──────────┐
                             │                      │
                             │  APP 01 — aula ......│. estação do Mestre
                             │    cadastra Guerreiro(a) e responsável
                             │           │          │
                             │           ▼          ▼
                             │  APP 07     APP 05 — Guerreiro(a)
                             │  responsável  inscrição → sondagem →
                             │               missões → criação original
                             │                      │
                             ▼                      ▼
                          APP 08              APP 09 — o Mestre autor
                          Apoiador            valida a criação original
```

| Para existir           | Precisa antes                                         |
| ---------------------- | ----------------------------------------------------- |
| Guerreiro(a)           | uma Comunidade Virtual — o vínculo é a exatamente uma |
| Trilha                 | um poder ativo e a persona do Mestre autor            |
| Aula                   | uma comunidade e um ponto de apoio                    |
| Desafio de coleta      | um tipo de coleta ativo no catálogo (ver §8)          |
| Série de coleta aberta | um local do território no nível que o desafio exige   |
| Publicação da trilha   | sondagem, desafio de coleta e culminância — as três   |
| Sessão do Guerreiro(a) | template facial gravado, ou um Mestre que o confirme  |

## 2. Admin — App 03, Gestão

Entra por login social. A persona Admin do fundador nasce na semeadura do ambiente; Admin novo
só por outro Admin, em **Personas → Admins → Incluir Admin**.

Abas: Comunidades · Poderes · Pontos de Apoio · Acervo · Agenda · Recursos · Atividades ·
Personas · Território · Filas · Chaves · Painel do dia · Lançamentos · Quiz ao Vivo ·
Encerramento do ciclo · Direitos e dados.

| #   | Passo               | Onde                                  | O que trava se faltar                                 |
| --- | ------------------- | ------------------------------------- | ----------------------------------------------------- |
| 1   | Comunidade Virtual  | Comunidades → Nova Comunidade Virtual | tudo: Guerreiro(a), ponto de apoio, aula e território |
| 2   | Poder               | Poderes → novo poder                  | a trilha, que pertence a um poder                     |
| 3   | Ponto de Apoio      | Pontos de Apoio → Novo Ponto de Apoio | o agendamento da aula                                 |
| 4   | Local do território | Território → Novo local               | a abertura de série de coleta pelo Guerreiro(a)       |
| 5   | Aula                | Agenda → Nova Aula                    | a estação da App 01                                   |
| 6   | Persona do Mestre   | Personas → Mestres                    | a autoria da trilha                                   |
| 7   | Persona do Apoiador | Personas → Apoiadores                 | a App 08                                              |

Ao cadastrar a comunidade, a **granularidade máxima** limita até que nível o território desce.
O local do passo 4 precisa existir **no mesmo nível** que o desafio de coleta vier a exigir —
se o desafio pedir rua e só houver bairro cadastrado, o Guerreiro(a) não abre a série.

**Mestre e Apoiador exigem ao menos um artefato comprobatório**, que é um endereço declarado —
currículo, portfólio, rede social —, nunca arquivo anexado. Sem ele o cadastro é recusado. O
e-mail informado vira a credencial de login social daquela persona: precisa ser o e-mail da
conta Google com que a pessoa vai entrar.

O Mestre nasce **sem nick** e o define sozinho no primeiro acesso. Nenhuma rota sugere um.

Filas que o Admin despacha, em **Filas**: solicitação de participação, dados de chave,
sugestão, desafio extra, homologação de aporte e solicitação do responsável.

## 3. Mestre — App 09, Área do Mestre

Entra por login social, com o e-mail que o Admin cadastrou. No primeiro acesso, **Meu perfil**
para definir o nick.

Abas: Minhas trilhas · Minhas turmas · Banco do Quiz · Desafios a julgar · Criações a validar ·
Território · Desafios extras · Propostas · Recursos · Responsáveis · Meu perfil · Direitos e
dados.

| #   | Passo                   | Onde                                        | Observação                                  |
| --- | ----------------------- | ------------------------------------------- | ------------------------------------------- |
| 1   | Nick                    | Meu perfil                                  | uma vez, no primeiro acesso                 |
| 2   | Criar a trilha          | Minhas trilhas → nova trilha                | nome, objetivo, área e poder                |
| 3   | Missão de sondagem      | trilha → nova missão, marcada como sondagem | **trava de publicação**                     |
| 4   | Demais missões          | trilha → nova missão                        | ordem, dificuldade, obrigatória ou opcional |
| 5   | Conteúdo e bibliografia | missão → conteúdo                           | opcional                                    |
| 6   | Desafio de desbloqueio  | missão → desbloqueio                        | quiz ou prático; o prático o Mestre julga   |
| 7   | Desafio de coleta       | missão → novo desafio de coleta             | **trava de publicação** — ver §8            |
| 8   | Culminância             | trilha → culminância                        | **trava de publicação**                     |
| 9   | Publicar                | trilha → publicar                           | as três travas conferidas de uma vez        |

A recusa da publicação nomeia **todas** as travas que faltam, não a primeira. Só o Mestre autor
escreve, publica e republica a própria trilha; outro Mestre recebe 403 e o Admin não edita
trilha alheia — ele só despublica, sempre com motivo.

A etiqueta ODS não fica no formulário: declara-se na própria tela da trilha, depois de criada.

O desafio de coleta pede tipo, cadência, vigência com início e fim, granularidade exigida e
quantos registros pontuam por período. O tipo vem do catálogo, e o Mestre nunca cria um.

Ao longo do ciclo, o Mestre volta em **Desafios a julgar** (desbloqueios práticos),
**Criações a validar** (a culminância entregue) e **Minhas turmas** (lançamentos e o painel
do dia).

Em **Responsáveis** o Mestre cadastra um responsável, cria o vínculo com o Guerreiro(a) e emite
a credencial provisória dele — o mesmo fluxo que a gestão oferece.

## 4. A estação da aula — App 01, Aula presencial

Não é persona: é o aparelho do encontro, operado por um Mestre sob **sessão de trabalho**. Um
aparelho, muitos Guerreiros e Guerreiras.

| #   | Passo                      | Onde                          | Observação                                   |
| --- | -------------------------- | ----------------------------- | -------------------------------------------- |
| 1   | Abrir a sessão de trabalho | entrada de trabalho           | o Mestre autentica o aparelho, não a criança |
| 2   | Cadastrar o Guerreiro(a)   | cadastro                      | nick, nascimento e comunidade; 6 a 16 anos   |
| 3   | Responsável                | passo seguinte do mesmo fluxo | cadastro, vínculo e credencial provisória    |
| 4   | Termo                      | passo seguinte                | consentimento da captura                     |
| 5   | Captura da imagem          | passo seguinte                | só aparece se o aparelho tiver câmera        |
| 6   | Entrada por reconhecimento | tela inicial                  | Guerreiro(a) já com template entra sozinho   |

O cadastro é o **único** autocadastro da plataforma: a persona nasce sem adulto como criador
dela, autenticada pela sessão de trabalho. Sem sessão de trabalho aberta, não há cadastro.

Sem câmera, o fluxo fecha sem template — e aí a entrada daquele Guerreiro(a) sai por
confirmação humana, na App 05. A recusa da biometria pelo responsável não fecha porta
nenhuma: a sessão aberta por confirmação vale como qualquer outra.

A estação também conduz a programação do encontro, as equipes, a partida do Quiz ao Vivo, a
entrega da produção da missão e o momento de troca por recompensa avulsa.

## 5. Guerreiro(a) — App 05, Minha Área

Entra por **nick e rosto**. Sem template gravado, ou quando o reconhecimento falha, um Mestre
ou Admin em sessão confirma pelo nick e a sessão abre igual.

Abas: Coleta do território · Minha carteira · Trilha · Desafios e equipes.

| #   | Passo                       | Onde                          | Observação                                         |
| --- | --------------------------- | ----------------------------- | -------------------------------------------------- |
| 1   | Escolher o poder            | Trilha → Escolher outro poder | filtra as trilhas publicadas                       |
| 2   | Inscrever-se na trilha      | Trilha → guia                 | a inscrição não se desfaz, e não obriga a concluir |
| 3   | Sondagem                    | Trilha → guia                 | abre a trilha e não define nível                   |
| 4   | Desbloquear a missão        | Trilha → guia                 | quiz responde na hora; prático espera o Mestre     |
| 5   | Entregar a produção         | missão → entrega              | texto, fala ou foto do manuscrito                  |
| 6   | Ler a devolutiva            | Trilha → Retomadas            | devolutiva não credita ponto                       |
| 7   | Abrir série de coleta       | Coleta do território          | escolhe o desafio e o local do nível exigido       |
| 8   | Registrar medição           | Coleta do território → série  | conforme a cadência do desafio                     |
| 9   | Entregar a criação original | Trilha → culminância          | texto, imagem, vídeo, arquivo ou link              |

**Progresso** mostra o percurso: só missão obrigatória conta para o nível. **Minha carteira**
reúne pontos, poderes, conquistas, ranking e a troca por recompensa. **Desafios e equipes**
traz os desafios extras vigentes e as equipes de que participa.

O passo 9 é o fecho da trilha. Quem valida ou devolve é o **Mestre autor** daquela trilha, em
Criações a validar — nenhum outro Mestre, e nunca o Admin.

## 6. Responsável — App 07, Área dos Responsáveis

Entra por **usuário e senha provisória**, emitida pela gestão ou pelo Mestre no cadastro do
vínculo. A senha provisória vale para **um** acesso e trava todas as telas até ser trocada: só
a tela de troca responde.

Abas: Evolução · Autorização · Transparência · Termo · Solicitações · Propostas · Imagem do
onboarding.

| Aba                  | Para quê                                           |
| -------------------- | -------------------------------------------------- |
| Evolução             | acompanhar o percurso do vinculado                 |
| Autorização          | a autorização única de divulgação e captação       |
| Termo                | o termo de biometria e o anexo dele                |
| Transparência        | que dados existem e o histórico de quem os acessou |
| Solicitações         | pedidos de direitos sobre os dados do vinculado    |
| Propostas            | propostas e avisos dirigidos ao responsável        |
| Imagem do onboarding | a imagem capturada no encontro                     |

**Admin e Mestre não conseguem testar esta aplicação por dentro.** Entrando com qualquer um dos
dois papéis, a App 07 mostra apenas o modo assistido — nem evolução, nem solicitações, nem
transparência, nem histórico de acessos. Para percorrer as sete abas é preciso entrar com a
credencial do próprio responsável.

## 7. Apoiador — App 08, Área do Apoiador

Duas portas: o **pré-cadastro público**, que gera uma solicitação para a gestão avaliar, e o
cadastro direto por Admin em Personas → Apoiadores. Cadastrado, entra por login social.

Abas: Identidade pública · Documentos comprobatórios · Propor desafio extra · Meus desafios ·
Efetividade · Meus aportes · Necessidades em aberto · Missões · Sustento · Declarar aporte ·
Situação das declarações · Acompanhamento · Propostas · Ofertar item · Minhas ofertas ·
Direitos e dados.

| #   | Passo                    | Onde                     | Observação                                      |
| --- | ------------------------ | ------------------------ | ----------------------------------------------- |
| 1   | Identidade pública       | Identidade pública       | nick, perfil PF ou PJ e como aparece na vitrine |
| 2   | Necessidades em aberto   | Necessidades em aberto   | o que o ciclo está pedindo                      |
| 3   | Declarar aporte          | Declarar aporte          | vai para a fila de homologação da gestão        |
| 4   | Situação das declarações | Situação das declarações | acompanha a homologação                         |
| 5   | Missões e sustento       | Missões · Sustento       | missões do Apoiador, níveis de sustento e selos |
| 6   | Desafio extra            | Propor desafio extra     | a gestão publica; ver a limitação na §8         |
| 7   | Acompanhamento           | Acompanhamento           | painel e favoritos: novidades de quem segue     |

O Admin homologa ou recusa a declaração de aporte em **Filas → homologação do aporte**, na
App 03.

## 8. O que ainda não fecha

Três pontos em que o percurso pelas telas para. Não são defeito: são fatia ainda não entregue.
Conferir a situação de cada uma no cronograma de fatias, em `openspec/`.

### Catálogo de tipos de coleta sem tela

O desafio de coleta é uma das três travas da publicação da trilha, e exige um **tipo de coleta
ativo** no catálogo. O cadastro do tipo é ato de Admin, mas **nenhuma tela da App 03 o
oferece** — a App 09 apenas lê a lista. Sem ao menos um tipo cadastrado, nenhuma trilha se
publica.

Enquanto a tela não existe, o Admin cadastra pela API, com a sessão dele:

```bash
curl -X POST https://api.comunidadegame.org/v1/tipos-de-coleta \
  -H "Authorization: Bearer $TOKEN_DO_ADMIN" \
  -H "X-Chave-Aplicacao: $CHAVE" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Pontos de descarte irregular","forma_de_registro":"numero",
       "unidade":"ocorrências","faixa_minima":0,"faixa_maxima":50}'
```

`forma_de_registro` aceita `numero`, `foto` ou `video`. `unidade`, `faixa_minima` e
`faixa_maxima` são opcionais — a faixa é o que marca a medição estranha para auditoria.

O token sai da sessão aberta na App 03: no console do navegador,
`sessionStorage.getItem("comunidade-game:token-de-sessao")`. A chave de aplicação é a que
aquele build da App 03 carrega, e o cabeçalho dela chama-se `X-Chave-Aplicacao`.

### Documentos comprobatórios do Apoiador sem fila

O Apoiador anexa documentos comprobatórios na App 08, e a gestão ainda não tem a fila que os
homologa. O ramo termina na anexação.

### Conclusão de desafio extra sem ato

O desafio extra é proposto pelo Apoiador, publicado pela gestão e aparece para o Guerreiro(a),
mas **não há como registrar a conclusão** — nem atribuir a recompensa, nem creditar os pontos
extras. A entidade existe só para leitura.
