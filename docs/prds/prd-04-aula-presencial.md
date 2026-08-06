# PRD-04 — App 01: Aula presencial (onboarding, trilhas e equipes)

## 1. Identificação

| Campo            | Valor                                                          |
| ---------------- | -------------------------------------------------------------- |
| PRD              | PRD-04                                                         |
| Aplicação        | App 01 — Aula presencial (onboarding, trilhas e equipes)       |
| Onda             | 2                                                              |
| Situação         | em revisão                                                     |
| Versão e data    | v2 — 2026-08-06                                                |
| Depende de       | PRD-01, PRD-02; o caminho das trilhas depende também do PRD-09 |
| Documentos-fonte | 02 §§1, 5, 9, 03 §§1.1, 3, 4, 12, 05 §§4, 5, 06 §3, 11 §§4, 5  |

## 2. Contexto e objetivo

O App 01 é **a aplicação da aula presencial**, usada pelos próprios Guerreiros e Guerreiras. Ao
abrir, ela pergunta o que a pessoa quer:

- **Onboarding**, de uso individual: **cadastrar quem chega pela primeira vez** e **registrar a
  presença de quem já é da casa** — por voz ou por chat, sem formulário, com a IA conduzindo e
  confirmando cada dado.
- **Trilhas**, de uso em equipe: o ponto de trilha em que a equipe está, o conteúdo e a
  atividade do dia, o Quiz ao Vivo e o assistente de trilhas.

O onboarding roda **continuamente durante o encontro**, não só na abertura, porque a dinâmica
da aula é assíncrona: os Guerreiros e Guerreiras chegam em ritmos diferentes e a porta fica
aberta. Nada disso funciona sozinho — o App 01 só abre dentro da janela de uma **aula agendada
na App 03**, e é dela que sai a comunidade de quem se cadastra naquele momento.

A aula presencial tem **dois ou mais aparelhos, um por equipe**: é neles que a turma trabalha a
trilha e responde ao quiz. As **equipes são formadas pelos próprios Guerreiros e Guerreiras**,
aqui, e valem para aquela aula. Fora do encontro presencial — nas aulas remotas e no uso
cotidiano — quem atende é a App 05 (PRD-05).

Entregue o App 01, o Ciclo 01 ganha o dado que sustenta a hipótese **H1**: quantos Guerreiros e
Guerreiras entram, quantos voltam e com que frequência. Sem ele, a presença vira lista de papel
e o cadastro vira digitação de terceiro — que é justamente o que a entrada por nick e imagem
existe para impedir.

## 3. Escopo

### 3.1 Dentro do escopo

#### Caminho do onboarding (individual)

- Tela inicial Mobile First com a escolha entre **onboarding** e **trilhas**; no onboarding,
  dois caminhos: **começar por áudio** e **começar por texto**.
- Conversa conduzida por IA, tolerante a respostas fora de ordem, capaz de repetir e confirmar.
- Abertura da sessão de trabalho: identificação da aula vigente e, havendo mais de uma no mesmo
  horário, pergunta única sobre em qual comunidade a aplicação está operando.
- Bloqueio da aplicação fora da janela de qualquer aula agendada.
- Verificação da **condição de funcionamento**: câmera no aparelho e Mestre ou Admin presente.
- Cadastro do novo Guerreiro(a): nome, nick, forma de tratamento, data de nascimento ou idade e
  características do avatar.
- Conferência da **unicidade do nick** na conversa, com sugestão de variações.
- Captura da imagem e geração do _template_ biométrico, com descarte imediato da fotografia.
- Registro do consentimento do responsável, com data, hora e quem testemunhou.
- Caminho da criança sem o responsável: cadastro sem imagem, com intervenção do Mestre ou Admin.
- Identificação do Guerreiro(a) já cadastrado por **nick e imagem** e registro automático da
  presença na atividade, presencial ou on-line.
- Confirmação manual pelo Mestre ou Admin quando a identificação falha.
- Fila local de presença com a rede fora, sincronizada quando ela volta.
- Aviso visível do que se coleta, com acesso à área detalhada de direitos.

#### Caminho das trilhas (em equipe)

- Entrada do Guerreiro(a) por **nick e imagem**.
- **Formação da equipe pelos próprios Guerreiros e Guerreiras**: criar, entrar e sair, com o
  limite de cinco integrantes e o de um familiar de 17 anos ou mais. A equipe vale para a aula
  em andamento e **encerra com ela**.
- Participação em **mais de uma equipe** no encontro e em **uma única** na partida de quiz.
- **Ponto de trilha da equipe**: onde ela está, o conteúdo e a atividade do dia.
- **Assistente de trilhas por voz ou texto**: quiz e explicação de conceitos das trilhas, no
  corpus fechado que os Mestres cadastraram.
- **Quiz ao Vivo:** recebimento da pergunta e envio da resposta pelo aparelho da equipe.

### 3.2 Fora do escopo

- Guarda do _template_ e conferência dele no login das demais aplicações: é o PRD-01.
- Cadastro do responsável e vínculo com os Guerreiros e Guerreiras: App 03 e App 09.
- Anexo da digitalização do termo assinado: App 03, porque quem opera a câmera na porta da aula
  não é quem arquiva documento.
- Agenda das aulas, conferência e ajuste das presenças recebidas: App 03.
- Abertura e condução da partida de Quiz ao Vivo, com o vínculo aparelho–equipe: App 03
  (PRD-02). Aqui a equipe só recebe a pergunta e responde.
- Autoria da trilha, do conteúdo e do banco de perguntas: App 09 (PRD-09).
- Escolha do provedor de IA e de reconhecimento facial: pendência do documento 09.
- **Apoio às atividades escolares**, coleta de dados do território, ranking, recompensas e
  canal de sugestões: são a App 05 (PRD-05), que atende as aulas remotas e o uso cotidiano.
- **Captação do áudio ambiente da aula**: o antigo Modo Ouvinte **saiu do produto**.
- Troca de comunidade do Guerreiro(a): fora do Ciclo 01.

## 4. Personas e permissões

| Persona               | O que faz nesta aplicação                                                                                       | O que não pode fazer                                                                                      |
| --------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Guerreiro(a) novo     | Conversa com a IA, informa seus dados, escolhe o nick e o avatar, tem a imagem captada com o responsável        | Informar a comunidade, escolher a aula, cadastrar-se fora da janela de uma aula                           |
| Guerreiro(a) já ativo | Informa o nick, captura a imagem e tem a presença registrada; forma equipe, trabalha a trilha e joga o quiz     | Registrar presença de outra pessoa; alterar cadastro por aqui; editar equipe alheia                       |
| Responsável           | Assiste ao cadastro, assina o termo impresso e autoriza a captura da imagem                                     | Operar a aplicação; não tem tela própria aqui                                                             |
| Mestre ou Admin       | Abre a sessão de trabalho, testemunha o consentimento, confirma identidade e presença quando o app não consegue | Cadastrar responsável por aqui; alterar presença já registrada ou composição de equipe — isso é na App 03 |

O **onboarding não tem login próprio**: quem opera é a dupla que está na sala. O Mestre ou Admin
autentica-se uma vez, ao abrir a sessão de trabalho do aparelho, e a partir daí a conversa é do
Guerreiro(a). O **caminho das trilhas exige sessão do Guerreiro(a)**, aberta por nick e imagem
dentro da mesma sessão de trabalho do aparelho.

## 5. Jornadas principais

### 5.1 Abrir a sessão de trabalho do aparelho

1. O Mestre ou o Admin abre o App 01 no aparelho do ponto de apoio e autentica-se.
2. A aplicação consulta as **aulas vigentes** para a data e a hora correntes.
3. Não havendo nenhuma, ela avisa em uma frase que não há aula agendada e **não abre**.
4. Havendo **uma**, ela assume a comunidade daquela aula e segue.
5. Havendo **mais de uma** — aulas presenciais em comunidades diferentes no mesmo horário —, ela
   pergunta **uma única vez** em qual está operando e usa essa escolha até o fim da sessão.
6. A aplicação verifica a **câmera** do aparelho. Sem câmera, não há onboarding: a mensagem
   orienta a usar outro aparelho.
7. A tela inicial fica aberta, com os dois caminhos — **onboarding** e **trilhas** —, pronta
   para o próximo que chegar.

### 5.2 Novo Guerreiro(a), com o responsável presente

1. A criança escolhe **áudio** ou **chat** e a IA se apresenta em linguagem simples, dizendo o
   que vai perguntar e por quê.
2. A conversa coleta, em qualquer ordem: **nome**, **nick**, **forma de tratamento**
   (Guerreiro ou Guerreira), **data de nascimento ou idade** e **características do avatar**.
3. A cada dado, a IA **repete e confirma**. Resposta fora de ordem é aceita e encaixada no
   campo certo; dado que falta é perguntado de novo ao final.
4. Nick já usado é recusado na hora, com **sugestão de variações** — o nick é único em toda a
   plataforma e é ele que localiza a pessoa na entrada.
5. Idade fora da faixa de **6 a 16 anos** interrompe o cadastro e chama o Mestre ou o Admin.
6. Confirmados os dados, a aplicação apresenta o **termo de consentimento** para a captura da
   imagem — exibido na tela e **lido em voz alta** na modalidade áudio.
7. O responsável **assina o termo impresso**, ali no encontro. O Mestre ou o Admin confirma na
   aplicação que o termo foi assinado e fica registrado como **testemunha**.
8. Só então a câmera captura a imagem. O aparelho envia a captura, o _template_ é gerado e a
   **fotografia original é descartada**.
9. O cadastro é criado **ativo**, vinculado à comunidade da aula vigente, e a **presença do dia
   é registrada** no mesmo ato.
10. A IA fecha a conversa dizendo o nick escolhido e como a criança vai entrar da próxima vez:
    **nick e foto, sem senha**.
11. A digitalização do termo assinado é anexada ao cadastro depois, pela gestão, na App 03. Até
    o anexo existir, a pendência aparece no painel do dia.

### 5.3 Novo Guerreiro(a), sem o responsável

1. Mesma conversa da jornada 5.2 até a confirmação dos dados.
2. Chegando à captura da imagem, a aplicação **não a executa**: sem responsável presente não há
   consentimento, e sem consentimento não há biometria.
3. O Mestre ou o Admin confirma na aplicação que a criança está na sala e o cadastro é criado
   **ativo, sem imagem**, com registro de quem confirmou.
4. O Guerreiro(a) participa de tudo. Enquanto não tiver imagem gravada, quem abre a sessão dele
   nas aplicações é o Mestre ou um Admin, no encontro.
5. Quando o responsável comparecer e aprovar a participação, a captura é feita pelo mesmo
   caminho da jornada 5.2, a partir do passo 6.

### 5.4 Presença de Guerreiro(a) já cadastrado

1. A criança informa o **nick**, por voz ou por texto.
2. A câmera captura a imagem e a aplicação a compara com o _template_ **daquele nick** — o nick
   restringe a busca, a imagem confirma.
3. Reconhecida, a **presença é registrada automaticamente** na atividade da aula vigente, e a
   tela devolve a confirmação em poucos segundos.
4. Presença já registrada no mesmo encontro não é duplicada: a aplicação avisa que ela já
   existe e volta à tela inicial.
5. Guerreiro(a) **sem _template_ gravado** — cadastro feito sem o responsável, ou biometria
   recusada — segue direto para a confirmação humana da jornada 5.5, sem tentativa de captura.

### 5.5 Falha de identificação

1. Não reconhecida a imagem, a aplicação **não diz se o nick existe** e oferece nova tentativa.
2. Persistindo a falha, ela chama o Mestre ou o Admin, que **confirma a identidade** da criança
   e registra a presença, com o nome de quem confirmou.
3. Captura ruim ou imagem que envelheceu: o Mestre ou o Admin recadastra a imagem de
   referência, e a substituição fica registrada.
4. Em nenhuma hipótese a falha deixa o Guerreiro(a) fora da aula.

### 5.6 Rede fora

1. Caindo a rede, a aplicação avisa na tela que está operando **sem conexão**.
2. A **presença** continua sendo registrada: o Mestre ou o Admin confirma a criança pelo nick e
   o registro entra na **fila local**.
3. **Cadastro novo e reconhecimento facial ficam indisponíveis** enquanto não houver rede —
   nenhuma imagem de criança fica guardada no aparelho compartilhado.
4. Voltando a rede, a fila sincroniza sozinha, preservando **a hora do fato**, não a do envio.
5. Registro que falhar na sincronização aparece para a gestão como pendência do painel do dia.
6. No caminho das trilhas, o **conteúdo já carregado continua legível**; formação de equipe,
   assistente e resposta de quiz **exigem rede** e voltam quando ela volta.

### 5.7 Formar a equipe da aula

1. O Guerreiro(a) entra pelo caminho **trilhas**, com nick e imagem.
2. A tela mostra as **equipes já formadas naquela aula**, por avatar e nick, e o botão de criar
   uma nova.
3. Criando, ele nomeia a equipe e ela nasce com ele dentro; entrando em uma existente, o
   ingresso é imediato — não há aprovação, a formação é livre.
4. A aplicação recusa o **sexto integrante** e o **segundo familiar de 17 anos ou mais**.
5. O Guerreiro(a) pode integrar **mais de uma equipe** no mesmo encontro e sair de qualquer uma
   enquanto a aula durar.
6. **Encerrada a aula, as equipes se encerram com ela**: o histórico do que a equipe realizou
   permanece; a composição não é reaproveitada no encontro seguinte.

### 5.8 Trabalhar a trilha com a equipe

1. Escolhida a equipe do momento, o aparelho mostra **em que ponto de trilha ela está**, o
   conteúdo daquele ponto e a atividade do dia.
2. A equipe conversa com o **assistente de trilhas**, por voz ou por texto: pede explicação de
   um conceito ou responde ao quiz do ponto.
3. O assistente responde **apenas a partir do corpus cadastrado pelos Mestres**. Fora dele,
   diz que o assunto ainda não está no material e orienta procurar um Mestre no encontro.
4. Pergunta sobre **tarefa escolar** recebe a mesma orientação: esse apoio é da App 05.
5. O **áudio da pergunta é descartado** assim que transcrito; guarda-se apenas a transcrição.
6. O microfone abre ao toque do botão de falar e **fecha ao fim da fala** — a aplicação não
   escuta a aula.

### 5.9 Jogar o Quiz ao Vivo

1. O Mestre abre a partida na App 03 e **vincula um aparelho a cada equipe**.
2. Vinculado o aparelho, o App 01 fixa **uma única equipe** para aquele Guerreiro(a) na
   partida, mesmo que ele integre outras no encontro.
3. A pergunta aparece **simultaneamente** em todos os aparelhos da partida.
4. A equipe se consulta e responde pelo seu aparelho; a resposta vale para **todos os
   integrantes** e a segunda tentativa é recusada.
5. O resultado da pergunta aparece quando quem conduz a partida o libera.
6. Equipe sem aparelho responde pelo aparelho do Mestre — falta de celular não tira ninguém da
   partida.

## 6. Requisitos funcionais

### 6.1 Onboarding e presença

| ID         | Requisito                                                                                                                | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------------------------------------ | ---------- |
| `RF-04-01` | Tela inicial oferece a escolha entre onboarding e trilhas e, no onboarding, entre áudio e texto                          | essencial  |
| `RF-04-02` | Aplicação abre somente dentro da janela de uma aula agendada para a data e a hora correntes                              | essencial  |
| `RF-04-03` | Havendo mais de uma aula vigente, a aplicação pergunta uma única vez em qual comunidade opera                            | essencial  |
| `RF-04-04` | Aplicação verifica a presença de câmera e bloqueia o onboarding quando não há                                            | essencial  |
| `RF-04-05` | Sessão de trabalho do aparelho é aberta por Mestre ou Admin autenticado                                                  | essencial  |
| `RF-04-06` | IA conduz a conversa aceitando respostas fora de ordem, repetindo e confirmando cada dado                                | essencial  |
| `RF-04-07` | Cadastro coleta nome, nick, forma de tratamento, data de nascimento ou idade e características do avatar                 | essencial  |
| `RF-04-08` | Aplicação recusa nick já existente e sugere variações antes de concluir o cadastro                                       | essencial  |
| `RF-04-09` | Idade fora da faixa de 6 a 16 anos interrompe o cadastro e aciona o Mestre ou o Admin                                    | essencial  |
| `RF-04-10` | Aplicação vincula o novo cadastro à comunidade da aula vigente, sem perguntá-la                                          | essencial  |
| `RF-04-11` | Termo de consentimento é exibido na tela e lido em voz alta na modalidade áudio                                          | essencial  |
| `RF-04-12` | Mestre ou Admin confirma na aplicação a assinatura do termo impresso e fica registrado como testemunha                   | essencial  |
| `RF-04-13` | Captura da imagem só ocorre depois do registro do consentimento, com o responsável presente                              | essencial  |
| `RF-04-14` | Fotografia original é descartada assim que o _template_ biométrico é gerado                                              | essencial  |
| `RF-04-15` | Cadastro sem o responsável é criado ativo e sem imagem, com registro de quem confirmou                                   | essencial  |
| `RF-04-16` | Aplicação captura a imagem do Guerreiro(a) já cadastrado assim que o responsável aprova a participação                   | essencial  |
| `RF-04-17` | Novo cadastro nasce ativo e registra a presença do dia no mesmo ato                                                      | essencial  |
| `RF-04-18` | Guerreiro(a) já cadastrado informa o nick, captura a imagem e tem a presença registrada automaticamente                  | essencial  |
| `RF-04-19` | Presença já registrada no mesmo encontro não é duplicada                                                                 | essencial  |
| `RF-04-20` | Falha de identificação oferece nova tentativa sem revelar se o nick existe                                               | essencial  |
| `RF-04-21` | Mestre ou Admin confirma a identidade e registra a presença quando a identificação falha, com registro de quem confirmou | essencial  |
| `RF-04-22` | Mestre ou Admin recadastra a imagem de referência a partir da própria aplicação                                          | desejável  |
| `RF-04-23` | Sem rede, a presença confirmada pelo Mestre ou Admin entra em fila local e sincroniza depois                             | essencial  |
| `RF-04-24` | Sem rede, cadastro novo e reconhecimento facial ficam indisponíveis, com aviso na tela                                   | essencial  |
| `RF-04-25` | Sincronização preserva a hora do fato, não a do envio, e não duplica registro reenviado                                  | essencial  |
| `RF-04-26` | Aplicação exibe aviso discreto do que coleta, com acesso à área detalhada de direitos                                    | essencial  |
| `RF-04-27` | Aplicação encerra a conversa dizendo ao Guerreiro(a) como ele entrará da próxima vez                                     | desejável  |
| `RF-04-28` | Aplicação volta à tela inicial ao fim de cada atendimento, pronta para o próximo que chegar                              | essencial  |

### 6.2 Trilhas e equipes

| ID         | Requisito                                                                                                     | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------------------------- | ---------- |
| `RF-04-29` | Caminho das trilhas abre sessão do Guerreiro(a) por nick e imagem                                             | essencial  |
| `RF-04-30` | Guerreiro(a) cria equipe da aula, entra em equipe existente e sai dela, sem aprovação de terceiro             | essencial  |
| `RF-04-31` | Aplicação recusa o sexto integrante e o segundo familiar de 17 anos ou mais                                   | essencial  |
| `RF-04-32` | Equipe é vinculada à aula em andamento e se encerra com ela, preservando o histórico realizado                | essencial  |
| `RF-04-33` | Guerreiro(a) integra mais de uma equipe no mesmo encontro                                                     | essencial  |
| `RF-04-34` | Tela mostra as equipes da aula por avatar e nick, sem qualquer dado pessoal                                   | essencial  |
| `RF-04-35` | Aplicação mostra à equipe o ponto de trilha em que está, o conteúdo e a atividade do dia                      | essencial  |
| `RF-04-36` | Assistente de trilhas responde por voz ou texto, apenas a partir do corpus cadastrado pelos Mestres           | essencial  |
| `RF-04-37` | Pergunta fora do corpus recebe recusa explicada, com orientação de procurar um Mestre no encontro             | essencial  |
| `RF-04-38` | Pergunta de tarefa escolar é encaminhada à App 05, sem ser respondida aqui                                    | essencial  |
| `RF-04-39` | Microfone abre por ação do Guerreiro(a) e fecha ao fim da fala; não há captação do áudio ambiente             | essencial  |
| `RF-04-40` | Áudio da pergunta é descartado assim que transcrito; guarda-se apenas a transcrição                           | essencial  |
| `RF-04-41` | Aparelho vinculado à equipe recebe a pergunta da partida simultaneamente aos demais                           | essencial  |
| `RF-04-42` | Na partida, o Guerreiro(a) joga por uma única equipe, ainda que integre outras no encontro                    | essencial  |
| `RF-04-43` | Aparelho envia uma única resposta por pergunta, válida para todos os integrantes, e recusa a segunda          | essencial  |
| `RF-04-44` | Resultado da pergunta aparece para a equipe quando quem conduz a partida o libera                             | essencial  |
| `RF-04-45` | Sem rede, o conteúdo já carregado continua legível; equipe, assistente e resposta de quiz ficam indisponíveis | essencial  |

## 7. Regras de negócio

| ID         | Regra                                                                                                       | Invariante | Fonte         |
| ---------- | ----------------------------------------------------------------------------------------------------------- | ---------- | ------------- |
| `RN-04-01` | Sem aula agendada para a data e o horário, o App 01 não opera                                               | 4          | 02 §1         |
| `RN-04-02` | O Guerreiro(a) nunca informa a comunidade: ela vem da aula vigente                                          | 4          | 02 §1         |
| `RN-04-03` | Sem câmera no aparelho e sem Mestre ou Admin presente, não há onboarding                                    | —          | 03 §3.2       |
| `RN-04-04` | O Guerreiro(a) é a única persona com autocadastro                                                           | 3          | 02 §1         |
| `RN-04-05` | O nick é único em toda a plataforma                                                                         | —          | 02 §1         |
| `RN-04-06` | A imagem tem finalidade única: identificar o Guerreiro(a) — presença e autenticação                         | 12         | 03 §3.3       |
| `RN-04-07` | Sem termo assinado pelo responsável presente não há captura de imagem                                       | 11         | 03 §3.3       |
| `RN-04-08` | A fotografia original é apagada assim que o _template_ é gerado                                             | 12         | 03 §3.3       |
| `RN-04-09` | Recusar a biometria não exclui ninguém: a confirmação humana no encontro é a alternativa equivalente        | 11         | 03 §3.3       |
| `RN-04-10` | O cadastro nasce ativo sem autorização do responsável; ela só é exigida para a divulgação pública do perfil | —          | 03 §12        |
| `RN-04-11` | A faixa etária dos Guerreiros e Guerreiras é de 6 a 16 anos                                                 | 2          | 02 §1         |
| `RN-04-12` | Nenhuma imagem de criança fica armazenada no aparelho compartilhado                                         | 12         | 03 §§3.3, 3.4 |
| `RN-04-13` | A presença é do fato, não do envio: a fila local preserva a hora em que a criança chegou                    | —          | 03 §3.4       |
| `RN-04-14` | Nenhuma tela da aplicação exibe a imagem de um Guerreiro(a) para outro                                      | 12         | 03 §12        |
| `RN-04-15` | A equipe é formada pelos próprios Guerreiros e Guerreiras e vale para aquela aula presencial                | 15         | 02 §5         |
| `RN-04-16` | A equipe tem até 5 integrantes e no máximo 1 familiar de 17 anos ou mais                                    | 15         | 02 §5         |
| `RN-04-17` | O Guerreiro(a) integra várias equipes, mas joga a partida de quiz por uma só                                | 15         | 02 §5, 05 §5  |
| `RN-04-18` | A gestão não forma nem edita equipe: acompanha as do dia no painel da App 03                                | —          | 03 §5         |
| `RN-04-19` | O assistente responde apenas a partir do corpus fechado cadastrado pelos Mestres                            | —          | 03 §§4, 7     |
| `RN-04-20` | A aplicação não capta o áudio ambiente da aula; só o áudio dirigido ao assistente                           | —          | 03 §4         |
| `RN-04-21` | Do áudio do assistente guarda-se apenas a transcrição                                                       | —          | 03 §7         |
| `RN-04-22` | Uma resposta por equipe e pergunta, válida para todos os integrantes                                        | —          | 05 §5         |

## 8. Modelo de dados

No caminho do onboarding a aplicação **escreve nas entidades que o PRD-01 já mantém**. O
caminho das trilhas **acrescenta duas entidades** ao núcleo — `RespostaDeQuiz` e
`ConsultaAoAssistente` — e escreve em `Equipe`, que o núcleo já mantém. O que existe só no
aparelho é a **fila local**, que não é entidade do domínio e não sobrevive à sincronização.

```text
CONSOME                        ESCREVE
Aula/Agenda (vigente)          Guerreiro(a)          — cadastro novo
ComunidadeVirtual              Credencial            — template biométrico
Trilha / PontoDeTrilha         Consentimento         — termo, testemunha, data e hora
PartidaDeQuiz                  Presenca              — registro do encontro
PerguntaDeQuiz                 Auditoria             — quem confirmou o quê
Corpus de apoio (App 09)       Equipe                — formada na aula, encerra com ela
                               RespostaDeQuiz        [entidade nova]
                               ConsultaAoAssistente  [entidade nova]
```

| Entidade               | O que esta aplicação grava                                                                                    |
| ---------------------- | ------------------------------------------------------------------------------------------------------------- |
| `Guerreiro(a)`         | nome, nick, forma de tratamento, nascimento ou idade, avatar, comunidade da aula, situação ativa              |
| `Credencial`           | _template_ biométrico cifrado, criado a partir da captura; a fotografia não é persistida                      |
| `Consentimento`        | responsável, Guerreiro(a), tipo (captura biométrica), versão do termo, decisão, testemunha, data e hora       |
| `Presenca`             | Guerreiro(a), aula, hora do fato, forma do registro (reconhecimento ou confirmação humana), quem confirmou    |
| `Equipe`               | nome, aula a que pertence, integrantes com o papel de cada um, momento de formação e de encerramento          |
| `RespostaDeQuiz`       | partida, pergunta, equipe, aparelho vinculado, alternativa escolhida, momento de chegada no servidor, acerto  |
| `ConsultaAoAssistente` | Guerreiro(a) ou equipe, assistente (trilhas ou apoio escolar), transcrição da pergunta e da resposta, momento |

Regras do modelo:

- `Equipe` **pertence a uma aula**: encerrada a aula, ela é fechada e não é reaproveitada; o
  que a equipe realizou permanece ligado a ela e a cada integrante.
- `RespostaDeQuiz` é única por equipe e por pergunta; a segunda tentativa é recusada.
- `ConsultaAoAssistente` guarda **apenas a transcrição** — o áudio não é persistido. É a mesma
  entidade que a App 05 usa para o apoio escolar (PRD-05).
- `Consentimento` e `Auditoria` são somente inserção — revogação é registro novo.
- A fila local guarda **apenas presença**, nunca imagem, e é descartada assim que sincroniza.

## 9. Contratos de API

As convenções são as do PRD-01 — prefixo `/v1`, erro em formato único, data e hora com fuso.
A **sessão de trabalho do aparelho**, aberta pelo Mestre ou Admin presente, é o que autentica a
escrita: o cadastro continua sendo **autocadastro do Guerreiro(a)**, feito na presença deles.

| Método | Rota                             | Autenticação     | Uso nesta aplicação                                       |
| ------ | -------------------------------- | ---------------- | --------------------------------------------------------- |
| GET    | `/v1/aulas/vigentes`             | pública          | Descobrir a aula e a comunidade do momento                |
| GET    | `/v1/guerreiros/nick/disponivel` | pública          | Conferir a unicidade do nick durante a conversa           |
| POST   | `/v1/guerreiros`                 | sessão do App 01 | Criar o cadastro, já vinculado à comunidade da aula       |
| POST   | `/v1/consentimentos`             | sessão do App 01 | Registrar o termo assinado, com testemunha, data e hora   |
| POST   | `/v1/guerreiros/{id}/imagem`     | sessão do App 01 | Enviar a captura para geração do _template_               |
| POST   | `/v1/aulas/{id}/presencas`       | sessão do App 01 | Registrar presença, por reconhecimento ou confirmação     |
| POST   | `/v1/sessoes/guerreiro`          | pública          | Conferir nick e imagem na chegada de quem já é cadastrado |

Rotas do caminho das trilhas, todas autenticadas na **sessão do Guerreiro(a)**:

| Método | Rota                                  | Uso nesta aplicação                                             |
| ------ | ------------------------------------- | --------------------------------------------------------------- |
| GET    | `/v1/aulas/{id}/equipes`              | Listar as equipes já formadas na aula, por avatar e nick        |
| POST   | `/v1/aulas/{id}/equipes`              | Criar equipe da aula, com quem a criou como primeiro integrante |
| POST   | `/v1/equipes/{id}/integrantes`        | Entrar em uma equipe existente                                  |
| DELETE | `/v1/equipes/{id}/integrantes/eu`     | Sair da equipe                                                  |
| GET    | `/v1/equipes/{id}/ponto-de-trilha`    | Ponto de trilha da equipe, com o conteúdo e a atividade do dia  |
| POST   | `/v1/assistente/trilhas/consultas`    | Perguntar ao assistente de trilhas e gravar a transcrição       |
| GET    | `/v1/partidas-de-quiz/{id}/pergunta`  | Receber a pergunta em andamento no aparelho da equipe           |
| POST   | `/v1/partidas-de-quiz/{id}/respostas` | Enviar a resposta da equipe pelo aparelho vinculado             |

Erros previstos: nenhuma aula vigente (200 com lista vazia — é o que mantém a aplicação
fechada); nick já usado (422, com as variações sugeridas no corpo); idade fora da faixa (422);
imagem não reconhecida (401, sem revelar se o nick existe); captura sem consentimento registrado
(422); presença duplicada no mesmo encontro (409); reenvio da fila local já processado (200, sem
duplicar o registro); sexto integrante ou segundo familiar de 17 anos ou mais na equipe (422);
equipe de aula já encerrada (409); segunda resposta da mesma equipe para a mesma pergunta (409);
resposta de Guerreiro(a) que já joga por outra equipe na mesma partida (409); pergunta fora do
corpus (200, com a recusa explicada no corpo).

## 10. Requisitos não funcionais

- Web App responsivo **Mobile First**, com alto contraste e poucos elementos por tela — ele é
  operado de pé, na porta da aula.
- Registro de presença de Guerreiro(a) conhecido em **poucos segundos**: a fila na porta é o
  limite prático, e a confirmação humana é a saída quando o reconhecimento demora.
- Funcionamento em **aparelho modesto e rede instável**, com fila local de presença.
- Uso em **aparelho compartilhado** do ponto de apoio: nenhum dado do atendimento anterior
  permanece na tela, e a aplicação volta sozinha ao início.
- **Um aparelho por equipe**, dois no mínimo na aula, com troca rápida de sessão do
  Guerreiro(a) — é o mesmo aparelho do onboarding, em outro caminho.
- **Sincronização em tempo real** na partida de quiz, com desempate por ordem de chegada da
  resposta no servidor e tolerância a rede instável.
- Modalidade áudio em **pt-BR**, com captação e reprodução via
  `navigator.mediaDevices.getUserMedia`, reconhecimento de fala e síntese de voz — mesma base
  técnica do Robô Educa.
- Acessibilidade: a modalidade áudio atende quem ainda não lê com fluência e pessoas com
  deficiência visual; a modalidade chat atende sala barulhenta e quem prefere digitar.
- Linguagem simples, adequada a criança de 6 anos, sem jargão e sem termo em inglês.
- Filtros de segurança de conteúdo no nível mais restritivo em toda interação da IA.
- Código aberto.

## 11. LGPD e proteção da criança

| Dado coletado                         | Finalidade                                | Base legal                   | Retenção                           | Quem acessa                      |
| ------------------------------------- | ----------------------------------------- | ---------------------------- | ---------------------------------- | -------------------------------- |
| Imagem captada                        | Gerar o _template_ biométrico             | consentimento do responsável | descartada na geração              | ninguém: não é persistida        |
| _Template_ biométrico                 | Presença e autenticação                   | consentimento do responsável | vínculo + 30 dias; 5 dias a pedido | ninguém: só a comparação interna |
| Nome                                  | Identificação interna                     | consentimento                | enquanto durar o vínculo           | gestão e responsável             |
| Nick e forma de tratamento            | Identidade pública                        | consentimento                | enquanto durar o vínculo           | qualquer visitante               |
| Data de nascimento ou idade           | Faixa etária e nível da atividade         | consentimento                | enquanto durar o vínculo           | gestão e responsável             |
| Características do avatar             | Geração do avatar público                 | consentimento                | enquanto durar o vínculo           | qualquer visitante               |
| Áudio ou texto da conversa            | Conduzir o cadastro                       | consentimento                | descartado ao fim do atendimento   | ninguém depois do atendimento    |
| Áudio da pergunta ao assistente       | Gerar a transcrição                       | consentimento                | descartado assim que transcrito    | ninguém: não é persistido        |
| Transcrição da consulta ao assistente | Melhorar o conteúdo e auditar o uso da IA | consentimento                | enquanto durar o vínculo           | gestão e Mestre da trilha        |
| Termo assinado (digitalização)        | Prova do consentimento                    | obrigação legal              | permanente                         | gestão e responsável             |
| Presença                              | Registro da participação                  | consentimento                | enquanto durar o vínculo           | gestão e responsável             |

- **Consentimento**: termo impresso, assinado pelo responsável presente no encontro, antes da
  captura. A aplicação grava data, hora e quem testemunhou; a gestão anexa a digitalização.
- **Alternativa para quem recusar**: nick mais confirmação do Mestre ou do Admin, no encontro,
  tanto para registrar presença quanto para entrar nas aplicações. Recusar biometria nunca
  significa ficar de fora — e a conversa de cadastro diz isso com essas palavras.
- **Aviso visível**: a tela inicial e a tela de captura indicam, de forma discreta, o que está
  sendo coletado, com um caminho para a área detalhada sobre destino e uso de cada dado.
- **Pedido de acesso, correção ou exclusão**: a aplicação não os atende — ela informa que o
  canal é o responsável, pela App 07, e que o prazo de resposta é de 7 dias.
- A imagem **nunca** é exibida: não vira avatar, não vai para a vitrine, não aparece em ranking
  e não é mostrada a outro Guerreiro(a).
- **Nada da aula é escutado**: o microfone abre por ação do Guerreiro(a) e fecha ao fim da fala.
  Não há captação do áudio ambiente nem transcrição da conversa da turma — o antigo Modo
  Ouvinte saiu do produto, e com ele a pendência de base legal para gravar sala com menores.
- Nas telas de equipe, o Guerreiro(a) vê os colegas **por avatar e nick**, nunca por nome ou
  qualquer outro dado pessoal.

## 12. Critérios de aceite e métricas

- Fora da janela de qualquer aula agendada, a aplicação não abre e explica por quê em uma frase.
- Com duas aulas presenciais vigentes em comunidades diferentes, a aplicação pergunta uma única
  vez e não repete a pergunta no restante da sessão de trabalho.
- Em aparelho sem câmera, a aplicação bloqueia o onboarding e orienta a trocar de aparelho.
- Cadastro concluído com as respostas dadas fora de ordem chega ao mesmo resultado do cadastro
  com as respostas na ordem.
- Nick já existente é recusado antes da conclusão, e as variações sugeridas são aceitas.
- Data de nascimento que resulte em idade fora de 6 a 16 anos não cria cadastro.
- Cadastro criado sem o responsável fica **ativo e sem _template_**, e a captura acontece depois,
  quando o responsável aprova.
- Tentativa de captura sem consentimento registrado é recusada, com mensagem em linguagem simples.
- Concluída a captura, a fotografia original não existe em lugar nenhum — nem no aparelho, nem
  no servidor, nem em log.
- Guerreiro(a) conhecido tem a presença registrada em poucos segundos, informando só o nick e
  olhando para a câmera.
- Segunda passagem do mesmo Guerreiro(a) no mesmo encontro não cria segunda presença.
- Imagem não reconhecida não revela se o nick existe, e a confirmação do Mestre registra a
  presença com o nome de quem confirmou.
- Com a rede desligada, a presença confirmada pelo Mestre entra na fila e aparece na App 03
  depois da sincronização, com a hora em que a criança chegou.
- Com a rede desligada, a tentativa de cadastro novo é recusada com aviso, e nenhuma imagem é
  gravada no aparelho.
- Nenhuma tela mostra dado do atendimento anterior depois que a aplicação volta ao início.
- A tela inicial oferece os dois caminhos, e quem escolhe trilhas sem sessão aberta é levado à
  entrada por nick e imagem, não ao cadastro.
- Equipe formada por um Guerreiro(a) aparece para os demais aparelhos da aula em segundos.
- A sexta pessoa que tenta entrar na equipe é recusada com mensagem em linguagem simples, e o
  segundo familiar de 17 anos ou mais também.
- Guerreiro(a) em duas equipes no encontro joga a partida por uma só, e a tentativa de responder
  pela outra é recusada.
- Encerrada a aula, a equipe é fechada: o encontro seguinte começa sem equipe formada, e o que
  ela realizou continua no histórico de cada integrante.
- Pergunta fora do corpus recebe recusa explicada, e pergunta de tarefa escolar é encaminhada à
  App 05 sem resposta aqui.
- Terminada a fala, o microfone fecha: com o assistente parado, nada é captado da sala.
- Em partida de quiz, a equipe responde uma vez; a segunda tentativa é recusada, e a rede caída
  no meio da pergunta não impede a equipe de continuar.

**Hipótese sustentada:** o App 01 é o instrumento de medida de **H1** (documento 10) — quantos
Guerreiros e Guerreiras se cadastram e com que frequência voltam. Ele passa a medir cadastros
por encontro, presenças por Guerreiro(a) e a taxa de identificação automática contra confirmação
humana — esta última é o número que diz se a entrada por imagem funciona na prática.

## 13. Decisões tomadas neste PRD

| Decisão                                                                                 | Gravada em     | Linha do doc 09 |
| --------------------------------------------------------------------------------------- | -------------- | --------------- |
| Fotografia original apagada assim que o _template_ é gerado                             | 03 §3.3        | Já decididos    |
| _Template_ guardado enquanto durar o vínculo, excluído ao fim dele ou a pedido          | 03 §3.3        | Já decididos    |
| Consentimento biométrico em termo impresso assinado, com testemunha e anexo pela gestão | 03 §3.3        | Já decididos    |
| Nick único em toda a plataforma, com sugestão de variações no cadastro                  | 02 §1          | Já decididos    |
| Rede fora: presença na fila local; cadastro e reconhecimento exigem rede                | 03 §3.4        | Já decididos    |
| App 02 incorporado ao App 01, que passa a ser a aplicação da aula presencial            | 03 §§2.1, 3, 4 | Já decididos    |
| Modo Ouvinte removido do produto; a aplicação não capta o áudio ambiente da aula        | 03 §4          | Já decididos    |
| Equipe formada pelos próprios Guerreiros e Guerreiras, válida para aquela aula          | 02 §5          | Já decididos    |
| Uma única equipe por Guerreiro(a) na partida de Quiz ao Vivo                            | 02 §5, 05 §5   | Já decididos    |
| Resposta do Quiz ao Vivo enviada pelo App 01, não mais pela App 05                      | 05 §5          | Já decididos    |
| App 05 como aplicação das aulas remotas e do uso cotidiano                              | 03 §7          | Já decididos    |

A decisão do consentimento em papel acrescentou a **testemunha** e o **anexo do termo** ao
`Consentimento` do PRD-01, e o acompanhamento do anexo pendente à App 03 (PRD-02).

A fusão das duas aplicações moveu para cá a `RespostaDeQuiz`, que estava no PRD-05, e trouxe a
`Equipe` — antes escrita apenas pela App 03 — para o aparelho da aula. A `ConsultaAoAssistente`
nasce aqui e serve também ao apoio escolar da App 05.

## 14. Pendências que permanecem

- **Provedor de IA e de reconhecimento facial**, com a decisão de processar no dispositivo ou na
  nuvem. Não altera os requisitos deste PRD, mas define custo, latência e exposição do dado.
- **Aviso ao responsável antes da exclusão do _template_**: o prazo está decidido — 30 dias
  após o fim do vínculo, ou 5 dias a pedido —, mas a forma do aviso prévio, sem notificação por
  e-mail no Ciclo 01, ainda precisa de desenho.
- **Duração da sessão de trabalho do aparelho** antes de exigir nova autenticação do Mestre ou
  Admin, a calibrar no primeiro encontro real.
- **Roteiro final da conversa**: este PRD fixa os dados obrigatórios, a ordem livre e as
  confirmações; o texto exato das falas da IA é escrito na implementação e validado com o Mestre
  fundador antes da primeira turma.
- **Termo de consentimento**: a redação do documento impresso precisa existir antes da primeira
  aula com onboarding.
- **Entrega em duas etapas**: o caminho do onboarding é da onda 2; o caminho das trilhas só
  opera com trilha, conteúdo e banco de perguntas publicados na App 09 (PRD-09) e com a
  condução da partida na App 03 (PRD-02) — o que a fase 3 do piloto já pressupõe.
- **Papel de cada integrante na equipe**: o documento 02 exige que o registro guarde o papel;
  falta decidir se o papel é escolhido na formação da equipe ou lançado na entrega da atividade.
- **Comportamento do assistente por voz em sala barulhenta**, com a alternativa por texto sempre
  disponível.

## 15. Rastreabilidade

| Requisito               | Origem                                                |
| ----------------------- | ----------------------------------------------------- |
| `RF-04-01`, `RF-04-06`  | 03 §3.2 (tela inicial e interação cognitiva), 06 §3   |
| `RF-04-02` e `RF-04-03` | 02 §1 e 03 §3.2 (comunidade vinda da aula agendada)   |
| `RF-04-04` e `RF-04-05` | 03 §3.2 (condição de funcionamento)                   |
| `RF-04-07`              | 03 §3.2 (dados coletados), 02 §9                      |
| `RF-04-08`              | 02 §1 (nick único)                                    |
| `RF-04-09`              | 02 §1 (faixa de 6 a 16 anos)                          |
| `RF-04-10`              | 02 §1 (vínculo obrigatório à comunidade)              |
| `RF-04-11` a `RF-04-14` | 03 §3.3 (consentimento, minimização e retenção)       |
| `RF-04-15` e `RF-04-16` | 03 §3.2 (criança sem o responsável)                   |
| `RF-04-17` a `RF-04-19` | 03 §3.2 (registro de presença)                        |
| `RF-04-20` a `RF-04-22` | 03 §§1.1, 3.2 (falha de identificação e alternativa)  |
| `RF-04-23` a `RF-04-25` | 03 §3.4 (rede instável e fila local)                  |
| `RF-04-26`              | 03 §12 (aviso visível e área detalhada)               |
| `RF-04-27` e `RF-04-28` | 03 §3 (onboarding contínuo em aparelho compartilhado) |
| `RF-04-29`              | 03 §1.1 (entrada por nick e imagem)                   |
| `RF-04-30` a `RF-04-34` | 02 §5 e 03 §4.1 (equipes formadas na aula)            |
| `RF-04-35`              | 11 §2 (anatomia da trilha), 03 §4.2                   |
| `RF-04-36` a `RF-04-40` | 03 §§4.2, 7 (assistente, corpus fechado e áudio)      |
| `RF-04-41` a `RF-04-44` | 05 §5 (regras da partida de Quiz ao Vivo)             |
| `RF-04-45`              | 03 §3.4 (rede instável)                               |
