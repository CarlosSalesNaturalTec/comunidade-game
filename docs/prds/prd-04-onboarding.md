# PRD-04 — App 01: Onboarding (cadastro e registro de presença)

## 1. Identificação

| Campo            | Valor                                                 |
| ---------------- | ----------------------------------------------------- |
| PRD              | PRD-04                                                |
| Aplicação        | App 01 — Onboarding (cadastro e registro de presença) |
| Onda             | 2                                                     |
| Situação         | aprovado                                              |
| Versão e data    | v1 — 2026-08-04                                       |
| Depende de       | PRD-01, PRD-02                                        |
| Documentos-fonte | 02 §§1, 9, 03 §§1.1, 3, 12, 06 §3                     |

## 2. Contexto e objetivo

O App 01 é a porta do encontro. Ele resolve dois problemas com a mesma conversa: **cadastrar
quem chega pela primeira vez** e **registrar a presença de quem já é da casa** — por voz ou por
chat, sem formulário, com a IA conduzindo e confirmando cada dado.

Ele roda **continuamente durante o encontro**, não só na abertura, porque a dinâmica da aula é
assíncrona: os Guerreiros e Guerreiras chegam em ritmos diferentes e a porta fica aberta. Nada
disso funciona sozinho — o App 01 só abre dentro da janela de uma **aula agendada na App 03**,
e é dela que sai a comunidade de quem se cadastra naquele momento.

Entregue o App 01, o Ciclo 01 ganha o dado que sustenta a hipótese **H1**: quantos Guerreiros e
Guerreiras entram, quantos voltam e com que frequência. Sem ele, a presença vira lista de papel
e o cadastro vira digitação de terceiro — que é justamente o que a entrada por nick e imagem
existe para impedir.

## 3. Escopo

### 3.1 Dentro do escopo

- Tela inicial Mobile First com dois caminhos: **começar por áudio** e **começar por texto**.
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

### 3.2 Fora do escopo

- Guarda do _template_ e conferência dele no login das demais aplicações: é o PRD-01.
- Cadastro do responsável e vínculo com os Guerreiros e Guerreiras: App 03 e App 09.
- Anexo da digitalização do termo assinado: App 03, porque quem opera a câmera na porta da aula
  não é quem arquiva documento.
- Agenda das aulas, conferência e ajuste das presenças recebidas: App 03.
- Escolha do provedor de IA e de reconhecimento facial: pendência do documento 09.
- Modo Conversa e Modo Ouvinte: são a App 02, ainda que compartilhem a base técnica de áudio.
- Troca de comunidade do Guerreiro(a): fora do Ciclo 01.

## 4. Personas e permissões

| Persona               | O que faz nesta aplicação                                                                                       | O que não pode fazer                                                              |
| --------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Guerreiro(a) novo     | Conversa com a IA, informa seus dados, escolhe o nick e o avatar, tem a imagem captada com o responsável        | Informar a comunidade, escolher a aula, cadastrar-se fora da janela de uma aula   |
| Guerreiro(a) já ativo | Informa o nick, captura a imagem e tem a presença registrada                                                    | Registrar presença de outra pessoa; alterar cadastro por aqui                     |
| Responsável           | Assiste ao cadastro, assina o termo impresso e autoriza a captura da imagem                                     | Operar a aplicação; não tem tela própria aqui                                     |
| Mestre ou Admin       | Abre a sessão de trabalho, testemunha o consentimento, confirma identidade e presença quando o app não consegue | Cadastrar responsável por aqui; alterar presença já registrada — isso é na App 03 |

A aplicação **não tem login próprio**: quem opera é a dupla que está na sala. O Mestre ou Admin
autentica-se uma vez, ao abrir a sessão de trabalho do aparelho, e a partir daí a conversa é do
Guerreiro(a).

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
7. A tela de boas-vindas fica aberta, com os botões de áudio e de chat, pronta para o próximo
   que chegar.

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

## 6. Requisitos funcionais

| ID         | Requisito                                                                                                                | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------------------------------------ | ---------- |
| `RF-04-01` | Tela inicial oferece dois caminhos equivalentes: começar por áudio e começar por texto                                   | essencial  |
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

## 8. Modelo de dados

A aplicação **não cria entidade nova**: ela escreve nas entidades que o PRD-01 já mantém. O que
existe só aqui é a **fila local do aparelho**, que não é entidade do domínio e não sobrevive à
sincronização.

```text
CONSOME                        ESCREVE
Aula/Agenda (vigente)          Guerreiro(a)   — cadastro novo
ComunidadeVirtual              Credencial     — template biométrico
                               Consentimento  — termo, testemunha, data e hora
                               Presenca       — registro do encontro
                               Auditoria      — quem confirmou o quê
```

| Entidade        | O que esta aplicação grava                                                                                 |
| --------------- | ---------------------------------------------------------------------------------------------------------- |
| `Guerreiro(a)`  | nome, nick, forma de tratamento, nascimento ou idade, avatar, comunidade da aula, situação ativa           |
| `Credencial`    | _template_ biométrico cifrado, criado a partir da captura; a fotografia não é persistida                   |
| `Consentimento` | responsável, Guerreiro(a), tipo (captura biométrica), versão do termo, decisão, testemunha, data e hora    |
| `Presenca`      | Guerreiro(a), aula, hora do fato, forma do registro (reconhecimento ou confirmação humana), quem confirmou |

Imutabilidade: `Consentimento` e `Auditoria` são somente inserção — revogação é registro novo.
A fila local guarda **apenas presença**, nunca imagem, e é descartada assim que sincroniza.

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

Erros previstos: nenhuma aula vigente (200 com lista vazia — é o que mantém a aplicação
fechada); nick já usado (422, com as variações sugeridas no corpo); idade fora da faixa (422);
imagem não reconhecida (401, sem revelar se o nick existe); captura sem consentimento registrado
(422); presença duplicada no mesmo encontro (409); reenvio da fila local já processado (200, sem
duplicar o registro).

## 10. Requisitos não funcionais

- Web App responsivo **Mobile First**, com alto contraste e poucos elementos por tela — ele é
  operado de pé, na porta da aula.
- Registro de presença de Guerreiro(a) conhecido em **poucos segundos**: a fila na porta é o
  limite prático, e a confirmação humana é a saída quando o reconhecimento demora.
- Funcionamento em **aparelho modesto e rede instável**, com fila local de presença.
- Uso em **aparelho compartilhado** do ponto de apoio: nenhum dado do atendimento anterior
  permanece na tela, e a aplicação volta sozinha ao início.
- Modalidade áudio em **pt-BR**, com captação e reprodução via
  `navigator.mediaDevices.getUserMedia`, reconhecimento de fala e síntese de voz — mesma base
  técnica do Robô Educa.
- Acessibilidade: a modalidade áudio atende quem ainda não lê com fluência e pessoas com
  deficiência visual; a modalidade chat atende sala barulhenta e quem prefere digitar.
- Linguagem simples, adequada a criança de 6 anos, sem jargão e sem termo em inglês.
- Filtros de segurança de conteúdo no nível mais restritivo em toda interação da IA.
- Código aberto.

## 11. LGPD e proteção da criança

| Dado coletado                  | Finalidade                        | Base legal                   | Retenção                         | Quem acessa                      |
| ------------------------------ | --------------------------------- | ---------------------------- | -------------------------------- | -------------------------------- |
| Imagem captada                 | Gerar o _template_ biométrico     | consentimento do responsável | descartada na geração            | ninguém: não é persistida        |
| _Template_ biométrico          | Presença e autenticação           | consentimento do responsável | enquanto durar o vínculo         | ninguém: só a comparação interna |
| Nome                           | Identificação interna             | consentimento                | enquanto durar o vínculo         | gestão e responsável             |
| Nick e forma de tratamento     | Identidade pública                | consentimento                | enquanto durar o vínculo         | qualquer visitante               |
| Data de nascimento ou idade    | Faixa etária e nível da atividade | consentimento                | enquanto durar o vínculo         | gestão e responsável             |
| Características do avatar      | Geração do avatar público         | consentimento                | enquanto durar o vínculo         | qualquer visitante               |
| Áudio ou texto da conversa     | Conduzir o cadastro               | consentimento                | descartado ao fim do atendimento | ninguém depois do atendimento    |
| Termo assinado (digitalização) | Prova do consentimento            | obrigação legal              | permanente                       | gestão e responsável             |
| Presença                       | Registro da participação          | consentimento                | enquanto durar o vínculo         | gestão e responsável             |

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

**Hipótese sustentada:** o App 01 é o instrumento de medida de **H1** (documento 10) — quantos
Guerreiros e Guerreiras se cadastram e com que frequência voltam. Ele passa a medir cadastros
por encontro, presenças por Guerreiro(a) e a taxa de identificação automática contra confirmação
humana — esta última é o número que diz se a entrada por imagem funciona na prática.

## 13. Decisões tomadas neste PRD

| Decisão                                                                                 | Gravada em | Linha do doc 09 |
| --------------------------------------------------------------------------------------- | ---------- | --------------- |
| Fotografia original apagada assim que o _template_ é gerado                             | 03 §3.3    | Já decididos    |
| _Template_ guardado enquanto durar o vínculo, excluído ao fim dele ou a pedido          | 03 §3.3    | Já decididos    |
| Consentimento biométrico em termo impresso assinado, com testemunha e anexo pela gestão | 03 §3.3    | Já decididos    |
| Nick único em toda a plataforma, com sugestão de variações no cadastro                  | 02 §1      | Já decididos    |
| Rede fora: presença na fila local; cadastro e reconhecimento exigem rede                | 03 §3.4    | Já decididos    |

A decisão do consentimento em papel acrescentou a **testemunha** e o **anexo do termo** ao
`Consentimento` do PRD-01, e o acompanhamento do anexo pendente à App 03 (PRD-02).

## 14. Pendências que permanecem

- **Provedor de IA e de reconhecimento facial**, com a decisão de processar no dispositivo ou na
  nuvem. Não altera os requisitos deste PRD, mas define custo, latência e exposição do dado.
- **Prazo, em dias, entre o fim do vínculo e a exclusão automática do _template_** — lembrando
  que apagar o _template_ apaga também a credencial de acesso do Guerreiro(a).
- **Duração da sessão de trabalho do aparelho** antes de exigir nova autenticação do Mestre ou
  Admin, a calibrar no primeiro encontro real.
- **Roteiro final da conversa**: este PRD fixa os dados obrigatórios, a ordem livre e as
  confirmações; o texto exato das falas da IA é escrito na implementação e validado com o Mestre
  fundador antes da primeira turma.
- **Termo de consentimento**: a redação do documento impresso precisa existir antes da primeira
  aula com onboarding.

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
