# PRD-11 — Personalização por IA

## 1. Identificação

| Campo            | Valor                                                     |
| ---------------- | --------------------------------------------------------- |
| PRD              | PRD-11                                                    |
| Aplicação        | — (comportamento das Apps 05, 01, 07, 09 e do núcleo)     |
| Onda             | 5                                                         |
| Situação         | aprovado                                                  |
| Versão e data    | v1 — 2026-08-08                                           |
| Depende de       | PRD-01, PRD-04                                            |
| Documentos-fonte | 02 §§2, 3, 4; 03 §§4, 7, 7.1, 9, 11, 12; 11 §§2.1, 2.2, 6 |

## 2. Contexto e objetivo

A plataforma atende de uma vez criança de 6 anos e adolescente de 16, na mesma trilha e no
mesmo ponto de apoio, e a progressão é por nível de dificuldade, nunca por idade. Sem
adaptação, o conteúdo escrito para o meio do grupo perde as duas pontas. Este PRD define como
a IA fecha essa distância sem construir dossiê de criança.

O desenho tem uma trava e uma liberdade. A trava: **a adaptação vive na sessão e é descartada
ao encerrá-la** — a plataforma não infere nem guarda ritmo, dificuldade ou interesse, e o que
alimenta a personalização é o que já existe por outra finalidade (sondagem, missões
concluídas, pontos, poderes, badges, nível e trilhas). A liberdade: dentro do **corpus fechado
que os Mestres cadastraram**, a IA pode reordenar o percurso, escolher o exemplo, reformular a
explicação no vocabulário do Guerreiro(a) e usar o poder que ele já domina para ensinar o que
ele ainda não domina.

Entregue este PRD no Ciclo 01, o Guerreiro(a) abre a App 05 e a tela já sabe qual é a próxima
missão e por quê; pede "explica de novo" e recebe a mesma matéria do Mestre em outras
palavras, marcada como texto gerado por IA; e o responsável, na App 07, vê o que sustenta cada
recomendação e desliga tudo com um toque, sem que a criança perca uma linha de conteúdo.

## 3. Escopo

### 3.1 Dentro do escopo

- **Contexto de sessão**: como é montado, o que entra nele, quanto dura e como é descartado.
- **Recomendação da próxima missão** na App 05, dentro do que o Mestre publicou na trilha.
- **Reescrita da explicação** do conteúdo cadastrado, sem sair do corpus fechado, com marcação
  visível de texto gerado por IA.
- **Ponte interdisciplinar**: usar o poder já dominado como exemplo e analogia, direto na
  App 05.
- **Filtros de segurança no nível mais restritivo** em toda interação personalizada.
- **Motivo da recomendação** em linguagem simples, na App 05 e na App 07.
- **Chave de personalização por Guerreiro(a)**: quem liga, quem desliga, com que efeito nas
  Apps 05 e 01, e o registro versionado do ato.
- **Auditoria por amostragem** da reescrita pelo Admin, com despublicação do conteúdo de
  origem.
- **Contadores de custo e demanda de IA**, sem nenhum dado pessoal.
- **Comportamento da personalização na App 01**, no aparelho compartilhado da equipe.

### 3.2 Fora do escopo

- **Perfil persistente do Guerreiro(a)**: decidido que não existe — não é adiamento, é
  desenho.
- **Geração de conteúdo novo pela IA**: autoria é do Mestre, e o corpus é fechado.
- **Escolha do modelo**: já decidida — Google Gemini em todo o Ciclo 01.
- **Auxílio de IA na autoria da trilha** (App 09): já está no PRD-09, e monta estrutura, não
  conteúdo.
- **Assistente da Área do Apoiador Desenvolvedor**: é da vitrine, PRD-03, e não trata de
  criança.
- **Personalização da vitrine**: o visitante não é perfilado, nem por cookie nem por servidor.
- **Recomendação entre ciclos ou entre comunidades**: no Ciclo 01 há uma comunidade e duas
  trilhas.
- **Visão computacional para análise de movimentos de capoeira**: ciclo futuro, com a trilha.
- **Biometria facial do App 01**: não é modelo de linguagem, tem pendência própria.

## 4. Personas e permissões

| Persona      | O que faz nesta área                                                                             | O que não pode fazer                                                                  |
| ------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| Guerreiro(a) | Recebe a missão sugerida e a explicação adaptada; pede reformulação; vê o motivo da recomendação | Ligar ou desligar a própria personalização; ver o que a IA usou de outro Guerreiro(a) |
| Responsável  | Vê o que alimenta a personalização e o motivo vigente; liga e desliga a qualquer tempo           | Alterar a ordem das missões ou o conteúdo do corpus                                   |
| Mestre       | Cadastra o corpus, único insumo da reescrita; vê a marcação nos textos gerados a partir do seu   | Editar o texto reescrito de uma sessão: ele não existe depois dela                    |
| Admin        | Audita a reescrita por amostragem e despublica o conteúdo de origem, com motivo                  | Cadastrar corpus; ligar ou desligar a personalização de um Guerreiro(a)               |
| Equipe       | No App 01, recebe explicação adaptada ao conjunto, no aparelho compartilhado                     | Receber reescrita quando algum integrante estiver com a personalização desligada      |

## 5. Jornadas principais

### 5.1 Guerreiro(a) abre a App 05 e recebe a próxima missão

1. O Guerreiro(a) entra por nick e imagem; a sessão abre.
2. O núcleo monta o **contexto da sessão** com o que já está gravado: trilhas em curso, missão
   de sondagem, missões concluídas e pendentes, poderes, badges, nível e pontos.
3. A tela inicial abre na **missão sugerida**, com o motivo em uma frase — "vem depois da
   missão que você concluiu ontem e usa o Poder da IA e Robótica, que é o seu mais forte".
4. A sugestão respeita a ordem e as travas que o Mestre publicou: missão bloqueada não é
   sugerida, e obrigatória vem antes de opcional.
5. **Exceção — personalização desligada:** a tela abre na próxima missão da ordem publicada,
   com o motivo "esta é a próxima missão da trilha".
6. **Exceção — trilha recém-aberta:** sem missão concluída, a sugerida é a de sondagem, que é
   a primeira de toda trilha.

### 5.2 Guerreiro(a) pede a explicação de outro jeito

1. Na missão, o Guerreiro(a) lê o conteúdo cadastrado pelo Mestre e aciona "explica de outro
   jeito".
2. A IA **reformula o mesmo conteúdo** no vocabulário e no interesse do Guerreiro(a), sem
   acrescentar matéria que não esteja no corpus.
3. O texto aparece **marcado como gerado por IA**, com o conteúdo original a um toque de
   distância.
4. **Exceção — nada a reformular:** não havendo conteúdo cadastrado para a missão, a aplicação
   diz que o Mestre ainda não publicou o material e orienta procurá-lo no encontro.
5. **Exceção — personalização desligada:** a ação não é oferecida, e o conteúdo original do
   Mestre é o que se lê.

### 5.3 Ponte interdisciplinar

1. O Guerreiro(a) trava numa missão de um poder em que tem nível baixo.
2. A IA identifica, entre os poderes que ele **já domina**, o que serve de analogia — explicar
   variável para quem domina rima, ou circuito para quem domina o Poder do Território.
3. A explicação sai com a ponte embutida e marcada como texto gerado por IA.
4. A ponte é **exemplo e analogia**, nunca missão nova: virar conteúdo de trilha continua
   sendo autoria do Mestre, na App 09.
5. **Exceção — nenhum poder com nível suficiente:** a explicação sai sem ponte, e nada é dito
   sobre o que falta ao Guerreiro(a).

### 5.4 A sessão encerra e o contexto some

1. A sessão encerra pelo botão de sair, pelos **10 minutos de inatividade** do aparelho
   compartilhado ou pelo fechamento da aplicação.
2. O **contexto de personalização é descartado**: nada do que a IA montou naquela conversa é
   gravado.
3. Permanecem apenas os registros que já têm norma própria: a **transcrição** da consulta ao
   assistente, com os prazos vigentes, e os **contadores de uso**, sem dado pessoal.
4. Na sessão seguinte, o contexto é montado de novo a partir do que está gravado — não há
   memória entre sessões.

### 5.5 Responsável vê e desliga na App 07

1. O responsável abre a App 07 e o Guerreiro(a) sob sua responsabilidade.
2. Vê **o que alimenta a personalização** — a lista dos dados já armazenados que entram no
   contexto — e a **recomendação vigente com o seu motivo**, em linguagem simples.
3. A tela diz, sem rodeio, que **nada é inferido nem guardado** sobre a criança e que o
   contexto morre com a sessão.
4. Aciona **desligar a personalização**; o efeito é imediato nas Apps 05 e 01.
5. O ato entra versionado, com quem operou, data e hora, e pode ser revertido a qualquer
   tempo.
6. **Exceção — mais de um responsável:** vale a mesma regra da autorização única — qualquer um
   desliga e **a recusa prevalece**; religar exige que nenhum dos vinculados esteja em recusa.
7. **Exceção — responsável sem smartphone:** o ato é feito por atendimento assistido ou termo
   impresso digitalizado, versionado em nome dele, como todo ato da App 07.

### 5.6 Aula presencial, no aparelho da equipe

1. A equipe entra no App 01 e abre a missão do dia no aparelho compartilhado.
2. O contexto da sessão é **da equipe**, montado apenas com o que é comum: a trilha, a missão
   do dia e o conteúdo cadastrado.
3. **Nenhum dado individual de integrante entra no contexto da equipe** — nem nível, nem
   pontos, nem histórico —, porque a tela é vista por todos.
4. **Exceção — integrante com personalização desligada:** vale o mais restritivo, e a equipe lê
   o conteúdo original do Mestre naquele aparelho.
5. A ponte interdisciplinar **não opera na App 01**: ela depende do poder individual, que não
   entra no contexto da equipe.

### 5.7 Pergunta que os filtros barram

1. O Guerreiro(a) pergunta algo impróprio, sensível ou sobre pessoas.
2. Os filtros de segurança, no nível mais restritivo, barram a resposta.
3. A aplicação recusa em linguagem acolhedora e orienta procurar um Mestre no encontro.
4. A recusa é registrada como consulta recusada, restrita à gestão, com a retenção já
   definida.
5. A personalização **não muda de comportamento** por causa da recusa: não há traço a ajustar.

### 5.8 Admin audita a reescrita

1. O Admin abre a amostragem de reescritas no painel de auditoria da App 03.
2. Vê a **consulta transcrita, o conteúdo de origem e o texto entregue**, lado a lado.
3. Encontrando desvio — matéria que não está no corpus, tom impróprio, erro conceitual —,
   **despublica o conteúdo de origem** com motivo, e o Mestre é notificado na fila da App 09.
4. Despublicado o conteúdo, ele deixa de alimentar reescrita e recomendação na hora.
5. **Exceção:** o Admin não corrige o texto reescrito. Ele não existe fora da sessão — o que se
   corrige é a fonte.

## 6. Requisitos funcionais

### 6.1 Contexto de sessão

| ID         | Requisito                                                                                           | Prioridade |
| ---------- | --------------------------------------------------------------------------------------------------- | ---------- |
| `RF-11-01` | Núcleo monta o contexto da sessão a partir apenas de dados já gravados por outra finalidade         | essencial  |
| `RF-11-02` | Contexto inclui trilhas em curso, sondagem, missões concluídas e pendentes, poderes, badges e nível | essencial  |
| `RF-11-03` | Contexto é descartado ao encerrar a sessão, por saída, inatividade ou fechamento da aplicação       | essencial  |
| `RF-11-04` | Aplicação não grava nenhum traço inferido de ritmo, dificuldade ou interesse do Guerreiro(a)        | essencial  |
| `RF-11-05` | Sessão seguinte remonta o contexto do zero, sem memória da anterior                                 | essencial  |
| `RF-11-06` | Contexto da App 01 é da equipe e não carrega dado individual de nenhum integrante                   | essencial  |

### 6.2 Recomendação da próxima missão

| ID         | Requisito                                                                                       | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------------- | ---------- |
| `RF-11-07` | App 05 abre na missão sugerida pela personalização, dentro do que o Mestre publicou             | essencial  |
| `RF-11-08` | Recomendação nunca sugere missão bloqueada nem inverte trava declarada pelo Mestre              | essencial  |
| `RF-11-09` | Recomendação apresenta missão obrigatória antes de opcional no mesmo estágio                    | essencial  |
| `RF-11-10` | Cada recomendação vem acompanhada do motivo, em uma frase e em linguagem simples                | essencial  |
| `RF-11-11` | Trilha sem missão concluída recomenda a missão de sondagem                                      | essencial  |
| `RF-11-12` | Personalização desligada abre na próxima missão da ordem publicada, com o motivo correspondente | essencial  |
| `RF-11-13` | Recomendação considera a cadência de retomada declarada pelo Mestre na revisão espaçada         | desejável  |

### 6.3 Reescrita da explicação

| ID         | Requisito                                                                                 | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------- | ---------- |
| `RF-11-14` | Guerreiro(a) aciona "explica de outro jeito" e recebe o mesmo conteúdo reformulado        | essencial  |
| `RF-11-15` | Reescrita não acrescenta matéria que não esteja no corpus cadastrado pelos Mestres        | essencial  |
| `RF-11-16` | Todo texto reescrito é apresentado com marcação visível de conteúdo gerado por IA         | essencial  |
| `RF-11-17` | Conteúdo original do Mestre fica acessível a um toque, ao lado da versão reescrita        | essencial  |
| `RF-11-18` | Missão sem conteúdo cadastrado recusa a reescrita e orienta procurar o Mestre no encontro | essencial  |
| `RF-11-19` | Personalização desligada não oferece a ação de reescrita                                  | essencial  |
| `RF-11-20` | Reescrita respeita a licença do conteúdo: a autoria creditada continua sendo a do Mestre  | essencial  |

### 6.4 Ponte interdisciplinar

| ID         | Requisito                                                                                    | Prioridade |
| ---------- | -------------------------------------------------------------------------------------------- | ---------- |
| `RF-11-21` | IA identifica, entre os poderes já dominados, o que serve de analogia para a missão em curso | essencial  |
| `RF-11-22` | Ponte entra na explicação como exemplo e analogia, nunca como missão ou conteúdo novo        | essencial  |
| `RF-11-23` | Nenhum poder com nível suficiente entrega a explicação sem ponte, sem apontar o que falta    | essencial  |
| `RF-11-24` | Ponte não opera na App 01, cujo contexto é da equipe                                         | essencial  |

### 6.5 Segurança e recusa

| ID         | Requisito                                                                                    | Prioridade |
| ---------- | -------------------------------------------------------------------------------------------- | ---------- |
| `RF-11-25` | Filtros de segurança operam no nível mais restritivo em toda interação personalizada         | essencial  |
| `RF-11-26` | Interação barrada recebe recusa em linguagem acolhedora e a orientação de procurar um Mestre | essencial  |
| `RF-11-27` | Recusa não altera o comportamento da personalização, porque não há traço a ajustar           | essencial  |
| `RF-11-28` | Aplicação exibe aviso visível de que aquela tela usa IA e do que ela usa para adaptar        | essencial  |

### 6.6 Controle do responsável (App 07)

| ID         | Requisito                                                                                       | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------------- | ---------- |
| `RF-11-29` | App 07 lista os dados já armazenados que alimentam a personalização do Guerreiro(a)             | essencial  |
| `RF-11-30` | App 07 mostra a recomendação vigente e o seu motivo, em linguagem simples                       | essencial  |
| `RF-11-31` | App 07 declara que nada é inferido nem guardado e que o contexto morre com a sessão             | essencial  |
| `RF-11-32` | Responsável liga e desliga a personalização, com efeito imediato nas Apps 05 e 01               | essencial  |
| `RF-11-33` | Ato de ligar ou desligar entra versionado, com quem operou, data e hora                         | essencial  |
| `RF-11-34` | Qualquer responsável vinculado desliga, e religar exige que nenhum deles esteja em recusa       | essencial  |
| `RF-11-35` | Desligamento por atendimento assistido ou termo impresso, versionado em nome do responsável     | essencial  |
| `RF-11-36` | Desligada a personalização, nenhum conteúdo ou missão deixa de estar disponível ao Guerreiro(a) | essencial  |

### 6.7 Auditoria e medição

| ID         | Requisito                                                                                   | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------- | ---------- |
| `RF-11-37` | Admin audita por amostragem consulta transcrita, conteúdo de origem e texto entregue        | essencial  |
| `RF-11-38` | Admin despublica o conteúdo de origem com motivo, e o Mestre é notificado na fila da App 09 | essencial  |
| `RF-11-39` | Conteúdo despublicado deixa de alimentar reescrita e recomendação imediatamente             | essencial  |
| `RF-11-40` | Núcleo registra contadores de chamadas, tokens e custo de IA, sem nenhum dado pessoal       | essencial  |
| `RF-11-41` | Painel da App 03 mostra a demanda e o custo de IA do ciclo, para dimensionar o seguinte     | desejável  |
| `RF-11-42` | Aplicação não impõe teto de uso da personalização no Ciclo 01                               | essencial  |

## 7. Regras de negócio

| ID         | Regra                                                                                             | Invariante | Fonte        |
| ---------- | ------------------------------------------------------------------------------------------------- | ---------- | ------------ |
| `RN-11-01` | A adaptação vive na sessão e é descartada ao encerrá-la                                           | 22         | 03 §7.1      |
| `RN-11-02` | A plataforma não infere nem guarda traço de ritmo, dificuldade ou interesse do Guerreiro(a)       | 22         | 03 §7.1      |
| `RN-11-03` | O insumo da personalização é só o que já está gravado por outra finalidade                        | 22         | 03 §7.1      |
| `RN-11-04` | A IA reescreve dentro do corpus fechado e nunca cria conteúdo novo                                | 22         | 03 §§7, 7.1  |
| `RN-11-05` | Todo texto reescrito é marcado como gerado por IA, com o original acessível                       | 22         | 03 §7.1      |
| `RN-11-06` | A autoria do conteúdo é do Mestre, e a reescrita não a transfere nem a divide                     | —          | 03 §§1, 11   |
| `RN-11-07` | A ponte interdisciplinar é exemplo e analogia; virar missão é autoria do Mestre                   | —          | 03 §§7.1, 11 |
| `RN-11-08` | A recomendação não inverte trava nem ordem declarada pelo Mestre na trilha                        | 5          | 11 §§2.2, 6  |
| `RN-11-09` | Só a missão obrigatória conta no percurso do nível, e a recomendação a apresenta primeiro         | 18         | 11 §6        |
| `RN-11-10` | A progressão que a recomendação segue é por nível de dificuldade, nunca por idade                 | 2          | 02 §3        |
| `RN-11-11` | Filtros de segurança no nível mais restritivo em toda interação com criança                       | —          | 03 §7        |
| `RN-11-12` | Desligar a personalização não tira conteúdo nem exclui o Guerreiro(a) de nenhuma atividade        | 11         | 03 §§7.1, 9  |
| `RN-11-13` | Qualquer responsável vinculado desliga, e a recusa prevalece                                      | 11         | 03 §9        |
| `RN-11-14` | O corpus é cadastrado só pelo Mestre; o Admin audita por amostragem e despublica com motivo       | —          | 03 §§7, 11   |
| `RN-11-15` | A leitura automática segue sendo hipótese: a personalização não lança resultado nem credita ponto | 19         | 11 §2.2      |
| `RN-11-16` | O contexto da App 01 é da equipe e não carrega dado individual, porque a tela é de todos          | 15         | 03 §4        |
| `RN-11-17` | Do áudio guarda-se só a transcrição, com os prazos já definidos                                   | —          | 03 §12.2     |
| `RN-11-18` | Não há teto de uso no Ciclo 01; o consumo é aporte por absorção do Admin e Mestre fundador        | 9          | 03 §7        |
| `RN-11-19` | Contadores de custo e demanda de IA são permanentes e não carregam dado pessoal                   | —          | 03 §12.2     |
| `RN-11-20` | A vitrine não personaliza nada: o visitante não é perfilado, nem no servidor nem no aparelho      | —          | 03 §8        |
| `RN-11-21` | Toda funcionalidade de IA do Ciclo 01 usa Google Gemini                                           | —          | 03 §1        |

## 8. Modelo de dados

A personalização é quase toda **sem persistência**: o que ela produz vive na memória da
requisição e morre com a sessão. Uma única entidade nova entra no núcleo — a chave que o
responsável controla — e ela descreve **uma decisão do responsável**, não um traço da criança.

```text
PERSISTIDO (PRD-01)                 NÃO PERSISTIDO (existe só na sessão)
PreferenciaDePersonalizacao         ContextoDeSessao
ConsultaAoAssistente (PRD-04/05)    RecomendacaoDeMissao
ContadorDeUsoDeIA                   TextoReescrito
                                    PonteInterdisciplinar
```

| Entidade                      | Atributos essenciais                                                                                                              |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `PreferenciaDePersonalizacao` | Guerreiro(a), situação (ligada ou desligada), responsável que operou, forma (App 07, atendimento assistido ou termo), data e hora |
| `ContadorDeUsoDeIA`           | finalidade (recomendação, reescrita, ponte, apoio escolar), chamadas, tokens, custo estimado, período — sem dado pessoal          |
| `ContextoDeSessao`            | sessão, trilhas em curso, missões concluídas e pendentes, poderes, badges, nível — **volátil**                                    |
| `RecomendacaoDeMissao`        | missão sugerida e motivo — **calculada na leitura, nunca gravada**                                                                |
| `TextoReescrito`              | conteúdo de origem, texto entregue, marcação de IA — **descartado com a sessão**                                                  |

O que é imutável: `PreferenciaDePersonalizacao` é **somente inserção** — cada mudança é um
registro novo, e a situação vigente é o último. Ligar e desligar precisa ter histórico
consultável, porque é ato do responsável.

Consequência do descarte, e ela precisa estar dita: **não há histórico de recomendações**. A
App 07 mostra a recomendação **vigente**, recalculada no momento da leitura, e não a lista do
que foi sugerido ao longo do ciclo — guardar essa lista seria guardar exatamente o registro de
comportamento que a decisão de escopo afastou.

`ConsultaAoAssistente`, `ConteudoDeApoio`, `Trilha`, `Missao`, `Poder`, `Badge` e `Nivel` são
do núcleo e aqui apenas referenciadas. Nenhuma delas ganha atributo novo.

## 9. Contratos de API

| Método | Rota                                  | Autenticação | Descrição                                                                 |
| ------ | ------------------------------------- | ------------ | ------------------------------------------------------------------------- |
| GET    | `/v1/eu/proxima-missao`               | Guerreiro(a) | Missão sugerida e o motivo, já respeitando a chave de personalização      |
| POST   | `/v1/eu/missoes/{id}/explicacao`      | Guerreiro(a) | Reformula o conteúdo da missão dentro do corpus; devolve marcado como IA  |
| GET    | `/v1/eu/personalizacao`               | Guerreiro(a) | Situação da chave e o que alimenta a adaptação, para o aviso na tela      |
| GET    | `/v1/guerreiros/{id}/personalizacao`  | Responsável  | Insumos, recomendação vigente com motivo e histórico de ligar e desligar  |
| POST   | `/v1/guerreiros/{id}/personalizacao`  | Responsável  | Liga ou desliga, com a forma do ato; devolve a situação vigente           |
| POST   | `/v1/aulas/{id}/explicacao`           | Equipe       | Reformulação no contexto da equipe, recusada se algum integrante desligou |
| GET    | `/v1/admin/personalizacao/amostragem` | Admin        | Amostra de consulta, conteúdo de origem e texto entregue, para auditoria  |
| GET    | `/v1/admin/metricas-ia`               | Admin        | Contadores de chamadas, tokens e custo por finalidade, sem dado pessoal   |

As rotas de consulta ao assistente — `/v1/apoio-escolar/consultas` e
`/v1/assistente/trilhas/consultas` — já estão nos PRD-05 e PRD-04 e não mudam aqui: o que este
PRD acrescenta é que a resposta delas passa pelo mesmo contexto de sessão e pela mesma chave
de personalização.

Erros previstos: reescrita de missão sem conteúdo cadastrado (422, dizendo que o Mestre ainda
não publicou); reescrita com a personalização desligada (409, com o conteúdo original no
corpo); reescrita no aparelho da equipe com integrante desligado (409, mesma resposta);
consulta de personalização de Guerreiro(a) fora da responsabilidade de quem pede (403);
tentativa de o próprio Guerreiro(a) ligar ou desligar a chave (403); pedido de histórico de
recomendações (404, com a explicação de que ele não existe por desenho).

## 10. Requisitos não funcionais

- **A personalização nunca é condição de uso.** Modelo fora do ar, cota estourada ou rede
  instável degradam para o conteúdo original do Mestre, sem tela de erro que trave a missão.
- **Tempo de resposta**: a missão sugerida abre com a tela, sem espera perceptível — ela sai do
  que já está gravado. Só a reescrita e a ponte chamam o modelo, e ambas são acionadas pelo
  Guerreiro(a), nunca automáticas.
- **Rede instável**: o conteúdo original é o que fica em cache legível; a reescrita exige rede
  e volta quando ela volta, como o assistente.
- **Celular modesto**: nada de processamento de modelo no aparelho; a chamada é do backend.
- **Aparelho compartilhado do ponto de apoio**: encerrada a sessão por saída ou pelos 10
  minutos de inatividade, o contexto da criança anterior não existe mais para a próxima.
- **Acessibilidade e linguagem simples**: motivo da recomendação em uma frase que uma criança
  de 6 anos entenda; marcação de IA legível por leitor de tela, não apenas por cor ou ícone.
- **Mobile First, responsivo, pt-BR, código aberto**, como o restante da plataforma.
- **Custo observável**: contadores por finalidade, para separar o que a personalização consome
  do que o apoio escolar consome.

## 11. LGPD e proteção da criança

| Dado coletado                     | Finalidade                                     | Base legal    | Retenção                         | Quem acessa                          |
| --------------------------------- | ---------------------------------------------- | ------------- | -------------------------------- | ------------------------------------ |
| Contexto de personalização        | Adaptar missão, exemplo e explicação na sessão | consentimento | **descartado ao fim da sessão**  | ninguém: não é persistido            |
| Situação da chave e quem a operou | Provar a decisão do responsável                | consentimento | enquanto durar o vínculo         | gestão, responsável e o próprio      |
| Transcrição da consulta           | Melhorar o conteúdo e auditar o uso da IA      | consentimento | prazos já vigentes na plataforma | gestão e Mestre da trilha            |
| Contadores de uso e custo de IA   | Dimensionar o ciclo seguinte                   | —             | permanente                       | gestão — **sem nenhum dado pessoal** |

- **Não há perfil de menor.** É o ponto central deste PRD: a plataforma não constrói, não
  guarda e não entrega dossiê comportamental de criança, porque nenhum é criado. O que existe é
  o registro de realização — missão, ponto, badge — que a criança e a família já veem.
- **Consentimento**: a personalização está coberta pela autorização única do responsável, que
  já abrange a captação da produção. O que este PRD acrescenta é a **chave de desligamento
  isolada**, para que recusar a adaptação não exija recusar o resto.
- **Alternativa equivalente**: desligada a personalização, o Guerreiro(a) tem o mesmo conteúdo,
  as mesmas missões e a mesma pontuação. Nada some, nada atrasa.
- **Aviso na aplicação**: a tela que usa IA diz que usa, diz o que usa para adaptar e leva à
  área detalhada, como toda coleta na plataforma.
- **Marcação do texto gerado** é proteção e é pedagogia: a plataforma ensina letramento crítico
  sobre IA e não pode entregar texto de máquina como se fosse do Mestre.
- **Filtros no nível mais restritivo** em toda interação, e a recusa nunca é usada para ajustar
  o comportamento da IA com aquela criança — não há traço a ajustar.
- **Acesso, correção e exclusão**: seguem a fila da App 07. A correção do que a personalização
  usa é a correção do dado de origem; não há campo inferido a corrigir.
- **Nenhum dado de criança sai para treinar modelo.** O uso é de inferência, com o corpus e o
  contexto enviados na chamada, e o Ciclo 01 não autoriza retenção pelo provedor para treino.

## 12. Critérios de aceite e métricas

- Aberta a App 05, a tela inicial mostra a missão sugerida e um motivo em uma frase, e a missão
  sugerida nunca é uma que o Mestre deixou bloqueada.
- Encerrada a sessão e aberta outra, a recomendação é recalculada e nenhum vestígio da conversa
  anterior aparece — verificável pela ausência de registro no banco, não só na tela.
- Inspecionado o banco depois de uma sessão inteira de uso, não existe nenhum campo com ritmo,
  dificuldade ou interesse inferido do Guerreiro(a).
- Acionada a reescrita, o texto entregue é conferível contra o conteúdo de origem e não
  contém matéria fora do corpus; a marcação de IA está visível e é lida por leitor de tela.
- Missão sem conteúdo cadastrado recusa a reescrita com a mensagem que orienta procurar o
  Mestre.
- Guerreiro(a) sem nenhum poder de nível suficiente recebe a explicação sem ponte, e a tela não
  diz nada sobre o que falta a ele.
- O responsável desliga a personalização na App 07 e, na sessão seguinte do Guerreiro(a), a
  App 05 abre na ordem publicada, sem a ação de reescrita e com todo o conteúdo disponível.
- Havendo dois responsáveis e um deles em recusa, a tentativa de religar é recusada com o
  motivo.
- No aparelho da equipe com um integrante desligado, a reescrita é recusada e a equipe lê o
  conteúdo original.
- A auditoria por amostragem mostra consulta, origem e entrega lado a lado, e despublicar o
  conteúdo de origem tira a reescrita do ar na consulta seguinte.
- O painel de custo de IA fecha o consumo do ciclo por finalidade sem exibir um único nick.

**Hipótese que sustenta:** a **H5** (efetividade do ensino da trilha) se verifica comparando a
missão de sondagem com os desafios de desbloqueio. A personalização é a variável que este PRD
introduz nessa comparação: com os contadores por finalidade e a chave de desligamento, o
Ciclo 01 passa a poder observar se quem usou a adaptação avançou diferente de quem não usou.
Não é experimento controlado — é observação declarada, e o PRD não promete mais que isso.

## 13. Decisões tomadas neste PRD

| Decisão                                                                        | Gravada em     | Linha do doc 09                      |
| ------------------------------------------------------------------------------ | -------------- | ------------------------------------ |
| Adapta na sessão e não perfila a criança; contexto descartado ao encerrar      | 03 §7.1        | Limites da personalização por IA     |
| Reescreve dentro do corpus fechado, com marcação de texto gerado por IA        | 03 §7.1        | Alcance da personalização por IA     |
| Ponte interdisciplinar direto ao Guerreiro(a) na App 05                        | 03 §7.1        | Ponte interdisciplinar da IA         |
| Painel, motivo e chave de desligar na App 07, com alternativa equivalente      | 03 §§7.1, 9    | Explicabilidade da IA ao responsável |
| Contexto de personalização entra na tabela de prazos de guarda como descartado | 03 §12.2       | Limites da personalização por IA     |
| A personalização vira invariante da documentação                               | 99 §6, item 22 | —                                    |

A decisão de não perfilar tem uma consequência que este PRD assume por inteiro: **não existe
histórico de recomendações**. A App 07 mostra a recomendação vigente, recalculada na leitura.
Guardar a série do que foi sugerido reconstruiria pela porta dos fundos o registro de
comportamento que a decisão afastou.

A entidade `PreferenciaDePersonalizacao` e os contadores por finalidade de IA foram
acrescentados ao modelo do PRD-01. Nenhuma entidade existente ganhou atributo.

## 14. Pendências que permanecem

- **Personalização no aparelho da equipe** (documento 09): este PRD aplica o critério do mais
  restritivo — um integrante desligado desliga a reescrita naquele aparelho. É a leitura
  coerente com a recusa que prevalece, e segue registrada como pendência porque o fundador
  ainda pode preferir que a chave individual não alcance a tela coletiva.
- **Forma da marcação do texto gerado por IA** (documento 09): que o texto é marcado está
  decidido; o desenho da marca entra junto com a nota de transparência da vitrine.
- **Nota de transparência sobre IA na vitrine** (documento 09): texto final e localização
  seguem abertos, e agora precisam também dizer que a plataforma reescreve conteúdo para
  crianças e não as perfila.
- **Cadência padrão da revisão espaçada** (documento 09): sem o padrão, `RF-11-13` fica
  desejável — a recomendação segue a cadência que cada Mestre declarar, e não há regra
  supletiva.
- **Retenção pelo provedor**: o Ciclo 01 opera em conta Google Gemini PRO, e a configuração que
  desliga a retenção para treino precisa ser conferida na implantação e registrada. É tarefa de
  operação, não decisão de produto.
- **Provedor de reconhecimento facial** (documento 09): segue aberto e fora deste PRD — é
  biometria do App 01, não personalização.

## 15. Rastreabilidade

| Requisito               | Origem                                                                 |
| ----------------------- | ---------------------------------------------------------------------- |
| `RF-11-01` a `RF-11-06` | 03 §7.1 (adaptação na sessão) e 03 §12.2 (descarte e sessão de 10 min) |
| `RF-11-07` a `RF-11-13` | 11 §§2.2, 6 (modelo de missão e percurso do nível) e 03 §7 (guia)      |
| `RF-11-14` a `RF-11-20` | 03 §§7, 7.1 (corpus fechado e reescrita marcada)                       |
| `RF-11-21` a `RF-11-24` | 02 §2 (poderes) e 03 §7.1 (ponte interdisciplinar)                     |
| `RF-11-25` a `RF-11-28` | 03 §§7, 12 (filtros no nível mais restritivo e aviso de coleta)        |
| `RF-11-29` a `RF-11-36` | 03 §§7.1, 9 (explicabilidade, chave e alternativa equivalente)         |
| `RF-11-37` a `RF-11-39` | 03 §§7, 11 (auditoria por amostragem e despublicação)                  |
| `RF-11-40` a `RF-11-42` | 03 §§7, 12.2 (cota, custo e contadores sem dado pessoal)               |
