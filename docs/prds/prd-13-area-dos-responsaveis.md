# PRD-13 — App 07: Área dos pais e responsáveis

## 1. Identificação

| Campo            | Valor                                        |
| ---------------- | -------------------------------------------- |
| PRD              | PRD-13                                       |
| Aplicação        | App 07 — Área dos pais e responsáveis        |
| Onda             | 4                                            |
| Situação         | aprovado                                     |
| Versão e data    | v2 — 2026-08-06                              |
| Depende de       | PRD-01, PRD-02                               |
| Documentos-fonte | 02 §§1, 9, 03 §§1.1, 9, 12, 10 §3, 13 §3, 15 |

## 2. Contexto e objetivo

A App 07 é o **canal oficial da plataforma com a família**. Ela substitui a comunicação por
mensageria de terceiros e reúne em um só lugar o que o responsável precisa: o que a criança
está fazendo, o que a plataforma guarda sobre ela, o que ele autoriza e o que pode pedir.

O que muda na operação do Ciclo 01: depois de se apresentar pessoalmente no primeiro encontro
e ser cadastrado por um Admin ou Mestre, o responsável passa a entrar com login próprio,
acompanha a evolução de cada Guerreiro(a) sob sua responsabilidade, **concede ou revoga a
autorização única** e abre solicitações com protocolo e prazo de 7 dias. Sem esta aplicação a
autorização não tem onde acontecer — e a divulgação pública, que depende dela, não existe.

É também o instrumento de medição da hipótese **H2** do Ciclo 01: quantos responsáveis tomam
conhecimento do tratamento de dados e aceitam os termos. Sem a App 07, H2 é anedota. Nada de
novo se decide aqui sobre o que a criança faz: a jornada dela está nos PRDs 04, 05 e 09, e
esta aplicação apenas a **mostra ao adulto que responde por ela**.

## 3. Escopo

### 3.1 Dentro do escopo

- **Acesso próprio do responsável**, por login social ou por credencial de usuário e senha
  provisória criada pela gestão, com troca obrigatória no primeiro acesso.
- **Lista dos Guerreiros e Guerreiras vinculados**, com o grau de parentesco declarado.
- **Evolução de cada Guerreiro(a)**: presença, atividades realizadas, pontos, poderes, badges,
  nível e progresso nas trilhas.
- **Ocorrências de conduta** lançadas nas aulas, com o motivo e o estado da reparação.
- **Autorização única**: concessão e revogação, com efeito imediato no que é público.
- **Divergência entre responsáveis** resolvida pela prevalência da recusa, com a autorização
  suspensa e sinalizada até a gestão tratar.
- **Transparência de dados**: quais dados da criança estão armazenados, para que servem, por
  quanto tempo ficam e **quem os acessou**.
- **Solicitações com protocolo e status**: acesso, correção, exclusão e esclarecimentos,
  encaminhadas à fila da App 03.
- **Limite declarado do pedido de exclusão** — o registro de território é despersonalizado,
  não apagado —, dito na tela antes do aceite.
- **Termos e consentimentos versionados**, com data, hora e histórico consultável, incluindo a
  declaração de que os dados podem ser entregues anonimizados a pesquisadores e gestores
  públicos.
- **Registro de propostas** de evolução da plataforma, na fila única da gestão.
- **Atendimento assistido e termo impresso** para o responsável sem smartphone.
- **Aviso de coleta de dados** em toda tela que coleta, com acesso à área detalhada.

### 3.2 Fora do escopo

- **Autocadastro do responsável**: o cadastro é ato de Admin (App 03) ou Mestre (App 09).
- **Cadastro e edição do vínculo com o Guerreiro(a)**, inclusive o grau de parentesco — é da
  gestão, no PRD-02.
- **Concessão do consentimento biométrico**: tem termo impresso próprio, assinado no encontro,
  gravada por Admin ou Mestre; a App 07 só oferece a **recusa** (`RF-13-27`) e a leitura do
  estado — nunca a concessão.
- **Tratamento das solicitações**: a resposta é dada na fila da App 03, não nesta aplicação.
- **Qualquer canal com Apoiadores ou terceiros** — inclusive parentes que acompanham a criança
  como Apoiadores, que não têm acesso a esta área.
- **Conteúdo de trilha, atividade e lançamento de resultado**: quem lança é o Mestre.
- **Histórico do apoio escolar e das consultas ao assistente**, restrito à gestão.
- **Notificação por e-mail**: não existe no Ciclo 01; todo retorno acontece na plataforma.
- **Solicitação e entrega de dados a pesquisadores e gestores públicos**: o termo declara que
  ela existe; o pedido e a aprovação são da vitrine (PRD-03) e da App 03 (PRD-02).

## 4. Personas e permissões

| Persona      | O que faz nesta aplicação                                                      | O que não pode fazer                                                     |
| ------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| Responsável  | Acompanha os vinculados, autoriza, revoga, solicita, lê termos e propõe        | Cadastrar-se, criar vínculo, ver criança não vinculada, lançar resultado |
| Admin        | Opera o atendimento assistido e anexa o termo impresso, com o ato em nome dele | Autorizar em nome próprio ou substituir a decisão do responsável         |
| Mestre       | O mesmo do Admin, quando é quem está no encontro                               | O mesmo do Admin                                                         |
| Guerreiro(a) | Nada: a sua jornada é a App 05                                                 | Entrar, conceder ou revogar a própria autorização                        |
| Apoiador     | Nada: acompanha pelo nick cedido pela família, na App 08                       | Entrar, mesmo sendo parente                                              |
| Visitante    | Nada: a aplicação é inteiramente autenticada                                   | Acessar qualquer tela                                                    |

O responsável vê **apenas os Guerreiros e Guerreiras vinculados a ele**. De terceiros, nada —
nem em ranking, nem em equipe, nem em criação de colega.

## 5. Jornadas principais

### 5.1 Primeiro acesso

1. O responsável já foi cadastrado por um Admin (App 03) ou Mestre (App 09), depois de se
   apresentar pessoalmente no primeiro encontro da criança.
2. Ele entra por **login social** ou pela **credencial de usuário e senha provisória** criada
   pela gestão.
3. Tendo senha provisória, a **troca é obrigatória** antes de qualquer outra tela.
4. Login sem cadastro prévio é **recusado**, com a orientação de procurar a gestão no encontro
   — login não cria cadastro.
5. A primeira tela apresenta os **termos vigentes** em linguagem simples e registra a leitura,
   com data e hora.
6. Concluído o acesso, ele vê a lista dos Guerreiros e Guerreiras vinculados, com o grau de
   parentesco declarado no cadastro.

### 5.2 Acompanhar a evolução

1. Escolhido um Guerreiro(a), a tela mostra **presença, atividades realizadas, pontos, poderes,
   badges, nível e progresso** em cada trilha.
2. O nível aparece como **percurso** — quantas missões faltam —, nunca como saldo de pontos.
3. **Ocorrência de conduta** aparece com o motivo, a data e o estado da reparação, quando o
   código pactuado na comunidade previr reparação.
4. Nada da produção da criança é exposto aqui além do que ela entregou e o Mestre validou:
   consulta ao assistente e transcrição de apoio escolar **não aparecem**.
5. Havendo mais de um Guerreiro(a) vinculado, ele alterna entre eles sem sair da aplicação.

### 5.3 Conceder e revogar a autorização

1. A tela da autorização diz, antes de qualquer botão, **o que ela libera**: divulgação do
   perfil, do histórico e das criações, imagem em fotos e vídeos de eventos e captação da
   produção por foto do manuscrito ou áudio.
2. Diz também o que **não** depende dela: a participação nas atividades, que é livre, e a
   biometria do onboarding, que tem termo impresso próprio.
3. O responsável concede. A concessão é gravada com **versão do termo, data e hora**, e o
   perfil passa a aparecer na vitrine e nos rankings públicos.
4. Revogando, o efeito é **imediato**: perfil, criações e elenco do jogo saem do que é público
   na hora, sem prejuízo da participação e sem apagar nada internamente.
5. Revogada a autorização, a criança volta a **entregar a produção ao Mestre no encontro** — a
   alternativa equivalente, que a tela explica no mesmo ato.
6. A revogação **não desfaz o passado**: o que foi publicado enquanto valia a autorização sai
   do ar, e o histórico de consentimentos guarda o que valia em cada data.

### 5.4 Divergência entre responsáveis

1. Qualquer um dos até três responsáveis vinculados concede ou revoga — não há responsável
   principal.
2. Havendo **recusa de um deles**, ela prevalece: a autorização fica **suspensa** e o perfil
   não aparece publicamente.
3. Os demais responsáveis veem o estado suspenso e **quem o motivou**, com data e hora.
4. A suspensão gera uma solicitação na fila da App 03, para a gestão tratar com a família.
5. Enquanto não houver desfecho, o estado suspenso equivale à ausência de autorização.

### 5.5 Pedir acesso, correção ou exclusão

1. O responsável abre a solicitação escolhendo o tipo: **acesso, correção, exclusão ou
   esclarecimento**.
2. Antes de confirmar um pedido de exclusão, a tela mostra o **limite declarado**: os registros
   de dados do território **não são apagados — são despersonalizados**, com o vínculo de
   autoria rompido e o mapeamento destruído.
3. Confirmado, o pedido recebe **protocolo** e entra na fila da App 03, com prazo de 7 dias.
4. Ele acompanha a situação — recebida, em tratamento, atendida ou recusada com motivo — dentro
   da plataforma; **não há e-mail** no Ciclo 01.
5. Passados os 7 dias sem desfecho, a solicitação aparece **em atraso** para ele e para a
   gestão.

### 5.6 Ver quem acessou os dados da criança

1. A tela de transparência lista **quais dados estão armazenados**, para que servem e por
   quanto tempo ficam, em linguagem simples.
2. Abaixo, o histórico de acessos: **data, hora, quem acessou, em que papel e qual dado**.
3. O acesso de rotina do Mestre da turma aparece como tal — a lista não sugere irregularidade
   onde há trabalho normal.
4. Encontrando algo que não entende, ele abre uma solicitação de esclarecimento dali mesmo.

### 5.7 Registrar uma proposta

1. O responsável registra a proposta em texto.
2. Ela entra na **fila única da gestão**, a mesma que recebe as sugestões do Guerreiro(a), do
   Apoiador e do Mestre.
3. Ele acompanha o status até o retorno, com o motivo em linguagem simples quando não adotada.
4. Proposta de responsável **não pontua**: pontos são da criança, e a evolução da plataforma
   não é atividade de trilha.

### 5.8 Responsável sem smartphone

1. No encontro presencial, um Admin ou Mestre abre a aplicação **com o responsável presente** e
   percorre a tela com ele — é o **atendimento assistido**.
2. O ato é gravado **em nome do responsável**, com registro de quem operou e quem testemunhou.
3. Preferindo papel, ele assina o **termo impresso**; a gestão digitaliza e anexa, e o
   consentimento entra versionado do mesmo jeito.
4. Nos dois caminhos o histórico do responsável fica idêntico ao de quem opera sozinho: mesma
   versão de termo, mesma data e hora, mesma força.

## 6. Requisitos funcionais

### 6.1 Acesso e vínculo

| ID         | Requisito                                                                                  | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------ | ---------- |
| `RF-13-01` | Responsável entra por login social ou por credencial de usuário e senha criada pela gestão | essencial  |
| `RF-13-02` | Credencial provisória exige troca de senha antes de qualquer outra tela                    | essencial  |
| `RF-13-03` | Login de conta sem cadastro prévio é recusado, com orientação de procurar a gestão         | essencial  |
| `RF-13-04` | Aplicação lista apenas os Guerreiros e Guerreiras vinculados, com o grau de parentesco     | essencial  |
| `RF-13-05` | Responsável com mais de um vinculado alterna entre eles sem sair da aplicação              | essencial  |
| `RF-13-06` | Aplicação não oferece cadastro de responsável nem criação ou edição de vínculo             | essencial  |

### 6.2 Evolução do Guerreiro(a)

| ID         | Requisito                                                                               | Prioridade |
| ---------- | --------------------------------------------------------------------------------------- | ---------- |
| `RF-13-07` | Painel exibe presença, atividades realizadas, pontos, poderes, badges e nível           | essencial  |
| `RF-13-08` | Progresso da trilha é exibido como percurso: missões concluídas e o que falta           | essencial  |
| `RF-13-09` | Ocorrência de conduta é exibida com motivo, data e estado da reparação                  | essencial  |
| `RF-13-10` | Criações originais validadas aparecem com título, trilha e data                         | essencial  |
| `RF-13-11` | Nenhuma consulta ao assistente ou transcrição de apoio escolar é exibida ao responsável | essencial  |
| `RF-13-12` | Nenhum dado de outra criança aparece, nem em equipe, nem em ranking                     | essencial  |

### 6.3 Autorização única

| ID         | Requisito                                                                                                                                       | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `RF-13-13` | Tela declara o que a autorização libera e o que não depende dela, antes de qualquer ação                                                        | essencial  |
| `RF-13-14` | Responsável concede a autorização única, gravada com versão do termo, data e hora                                                               | essencial  |
| `RF-13-15` | Responsável revoga a autorização a qualquer tempo, com efeito imediato no que é público                                                         | essencial  |
| `RF-13-16` | Revogação retira perfil, criações e elenco do jogo do que é público, sem apagar o registro                                                      | essencial  |
| `RF-13-17` | Recusa de qualquer responsável vinculado suspende a autorização e prevalece sobre a concessão                                                   | essencial  |
| `RF-13-18` | Estado suspenso exibe quem o motivou, com data e hora, aos demais responsáveis                                                                  | essencial  |
| `RF-13-19` | Suspensão por divergência abre, em nome de quem recusou, uma solicitação de esclarecimento — uma só enquanto estiver em aberto por Guerreiro(a) | essencial  |
| `RF-13-20` | Tela informa a alternativa equivalente vigente enquanto não houver autorização                                                                  | essencial  |
| `RF-13-21` | Histórico da autorização mostra cada concessão e revogação, com a versão do termo                                                               | essencial  |

### 6.4 Solicitações e direitos

| ID         | Requisito                                                                                    | Prioridade |
| ---------- | -------------------------------------------------------------------------------------------- | ---------- |
| `RF-13-22` | Responsável abre solicitação de acesso, correção, exclusão ou esclarecimento                 | essencial  |
| `RF-13-23` | Pedido de exclusão exibe o limite da despersonalização do dado de território antes do aceite | essencial  |
| `RF-13-43` | Pedido de exclusão deferido apaga o _template_ biométrico do Guerreiro(a)                    | essencial  |
| `RF-13-44` | Fim do vínculo do Guerreiro(a) apaga o _template_ biométrico, sem depender de pedido         | essencial  |
| `RF-13-24` | Solicitação confirmada recebe protocolo e entra na fila da App 03                            | essencial  |
| `RF-13-25` | Responsável acompanha a situação da solicitação e o prazo de 7 dias                          | essencial  |
| `RF-13-26` | Solicitação sem desfecho em 7 dias aparece em atraso para o responsável                      | essencial  |
| `RF-13-27` | Responsável recusa a imagem captada no onboarding, que tem termo próprio                     | essencial  |
| `RF-13-28` | Recusa registrada nunca exclui o Guerreiro(a) da atividade                                   | essencial  |

### 6.5 Transparência e termos

| ID         | Requisito                                                                                                     | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------------------------- | ---------- |
| `RF-13-29` | Tela lista os dados armazenados da criança, a finalidade e o prazo de guarda de cada um                       | essencial  |
| `RF-13-30` | Histórico de acessos exibe data, hora, quem acessou, em que papel e qual dado                                 | essencial  |
| `RF-13-31` | Responsável abre solicitação de esclarecimento a partir de um acesso listado                                  | desejável  |
| `RF-13-32` | Termos vigentes são exibidos em linguagem simples, com registro da leitura                                    | essencial  |
| `RF-13-33` | Histórico de termos permite consultar a versão que valia em cada data                                         | essencial  |
| `RF-13-34` | Termo declara que os dados podem ser entregues, gratuitos e anonimizados, a pesquisadores e gestores públicos | essencial  |

### 6.6 Atendimento assistido, propostas e avisos

| ID         | Requisito                                                                                 | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------- | ---------- |
| `RF-13-35` | Admin ou Mestre opera a aplicação com o responsável presente, gravando o ato em nome dele | essencial  |
| `RF-13-36` | Ato assistido registra quem operou e quem testemunhou                                     | essencial  |
| `RF-13-37` | Gestão anexa a digitalização do termo impresso, que entra versionado                      | essencial  |
| `RF-13-38` | Consentimento assistido ou impresso tem a mesma força do registrado pelo responsável      | essencial  |
| `RF-13-39` | Responsável registra proposta de evolução da plataforma na fila única da gestão           | essencial  |
| `RF-13-40` | Responsável acompanha o status da proposta, com motivo quando não adotada                 | essencial  |
| `RF-13-41` | Toda tela que coleta dado traz aviso discreto, com acesso à área detalhada                | essencial  |
| `RF-13-42` | Aplicação não oferece nenhum canal de contato com Apoiadores ou terceiros                 | essencial  |

## 7. Regras de negócio

| ID         | Regra                                                                                         | Invariante (doc 99 §6) | Fonte        |
| ---------- | --------------------------------------------------------------------------------------------- | ---------------------- | ------------ |
| `RN-13-01` | O responsável é cadastrado por Admin ou Mestre, nunca por autocadastro                        | 3                      | 02 §1        |
| `RN-13-02` | Login não cria cadastro: conta sem cadastro prévio é recusada                                 | 3                      | 03 §1.1      |
| `RN-13-03` | Cada Guerreiro(a) tem no máximo três responsáveis vinculados                                  | 3                      | 02 §1        |
| `RN-13-04` | O responsável só enxerga os Guerreiros e Guerreiras vinculados a ele                          | 10                     | 03 §9        |
| `RN-13-05` | Uma só autorização cobre divulgação, imagem em eventos e captação da produção                 | —                      | 03 §12       |
| `RN-13-06` | A biometria do onboarding fica fora da autorização única e tem termo impresso próprio         | 12                     | 03 §§3.3, 12 |
| `RN-13-07` | Qualquer responsável vinculado concede ou revoga; a recusa prevalece e suspende a autorização | —                      | 02 §1        |
| `RN-13-08` | A revogação vale para frente e é imediata na parte pública, sem prejuízo da participação      | 11                     | 03 §9        |
| `RN-13-09` | Nenhuma recusa exclui o Guerreiro(a) da atividade: há sempre alternativa equivalente          | 11                     | 03 §9        |
| `RN-13-10` | Consentimento é somente inserção: revogar é registro novo, nunca edição do anterior           | —                      | 03 §12       |
| `RN-13-11` | Sem autorização vigente, o Guerreiro(a) não aparece em vitrine, ranking nem elenco do jogo    | 8, 12                  | 03 §12       |
| `RN-13-12` | O pedido de exclusão despersonaliza o registro de território; não o apaga                     | 7                      | 03 §12.1     |
| `RN-13-22` | O _template_ biométrico é apagado, não despersonalizado: é a exceção ao limite da exclusão    | 12                     | 03 §3.3      |
| `RN-13-13` | A titularidade não se transfere: o responsável exerce os direitos em nome do Guerreiro(a)     | —                      | 03 §12.1     |
| `RN-13-14` | Toda solicitação tem prazo de resposta de 7 dias e desfecho registrado na App 03              | —                      | 03 §9        |
| `RN-13-15` | No Ciclo 01 não há notificação por e-mail: o retorno acontece na plataforma                   | —                      | 03 §9        |
| `RN-13-16` | O ato assistido e o termo impresso são gravados em nome do responsável, com testemunha        | —                      | 03 §9        |
| `RN-13-17` | A aplicação não abre canal com Apoiadores ou terceiros, nem para parentes da criança          | 10                     | 02 §1, 03 §9 |
| `RN-13-18` | Proposta de responsável não pontua: a pontuação é da criança                                  | —                      | 03 §§7, 9    |
| `RN-13-19` | O termo declara a entrega gratuita e anonimizada dos dados, aprovada caso a caso por Admin    | 17                     | 03 §12.3     |
| `RN-13-20` | O histórico de consultas ao assistente é restrito à gestão e não é exibido ao responsável     | —                      | 03 §7        |
| `RN-13-21` | Ocorrência de conduta é visível ao responsável, com o estado da reparação                     | —                      | 13 §3        |

## 8. Modelo de dados

A aplicação **não cria entidade nova**: opera as que o PRD-01 já define. Ela escreve
`Consentimento`, `SolicitacaoDoResponsavel` e `SugestaoOuProposta`, e lê o restante.

```text
ESCREVE (por ato do responsável)        LÊ (definidos em outro PRD)
Consentimento             (PRD-01)      Guerreiro(a) / Presenca      (PRD-01)
SolicitacaoDoResponsavel  (PRD-01)      Resultado / Ponto            (PRD-01)
SugestaoOuProposta        (PRD-01)      Nivel / Badge / Poder        (PRD-01)
                                        VinculoResponsavel           (PRD-01)
                                        Auditoria                    (PRD-01)
                                        CriacaoOriginal              (PRD-09)
                                        Trilha / Missao              (PRD-09)
```

| Entidade                   | Atributos essenciais                                                                                                                                              |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Consentimento`            | responsável, Guerreiro(a), tipo, versão do termo, decisão, data e hora, testemunha, anexo do termo, **origem** (própria, assistida ou impressa) e **quem operou** |
| `SolicitacaoDoResponsavel` | protocolo, responsável, Guerreiro(a), tipo, texto, situação, prazo, quem tratou, desfecho e data                                                                  |
| `VinculoResponsavel`       | responsável, Guerreiro(a), grau de parentesco, cadastrado por, início, fim — leitura apenas                                                                       |

Imutabilidade e derivação:

- `Consentimento` é **somente inserção**. Revogar é gravar decisão nova, o que permite
  responder "o que valia naquela data" sem reconstituição.
- O **estado vigente da autorização** é derivado: vale a decisão mais recente de cada
  responsável vinculado, e **basta uma recusa** para o estado ser _suspenso_.
- Os dois atributos novos do `Consentimento` — origem e quem operou — foram acrescentados ao
  modelo do PRD-01 para sustentar o atendimento assistido.
- `SolicitacaoDoResponsavel` teve os atributos detalhados no PRD-01; a fila e o desfecho são do
  PRD-02.

## 9. Contratos de API

A aplicação segue as convenções do PRD-01 — prefixo `/v1`, token de sessão, erro em corpo
único. O cadastro do responsável e do vínculo é rota de gestão e já está no PRD-01. `POST
/v1/solicitacoes` e `GET /v1/eu/solicitacoes` já estão implementadas no núcleo, pela fatia 14 do
PRD-02 (decisão do fundador, 2026-08-29, documento 09 §1); a fatia 4 desta PRD entrega as telas
da App 07 sobre elas, e nela nasceram as três rotas de recusa da biometria e de fim do vínculo
(decisão do fundador, 2026-09-01, documento 09 §1).

| Método | Rota                                        | Autenticação    | Descrição                                                               |
| ------ | ------------------------------------------- | --------------- | ----------------------------------------------------------------------- |
| GET    | `/v1/eu/guerreiros`                         | Responsável     | Guerreiros e Guerreiras vinculados, com grau de parentesco              |
| GET    | `/v1/eu/guerreiros/{id}/evolucao`           | Responsável     | Presença, atividades, pontos, poderes, badges, nível e progresso        |
| GET    | `/v1/eu/guerreiros/{id}/ocorrencias`        | Responsável     | Ocorrências de conduta, com motivo e estado da reparação                |
| GET    | `/v1/eu/guerreiros/{id}/autorizacao`        | Responsável     | Estado vigente da autorização e histórico de decisões                   |
| POST   | `/v1/eu/guerreiros/{id}/autorizacao`        | Responsável     | Concede ou revoga, gravando a versão do termo                           |
| POST   | `/v1/guerreiros/{id}/autorizacao/assistida` | Admin ou Mestre | Registra o ato em nome do responsável presente, com testemunha          |
| POST   | `/v1/consentimentos/{id}/anexo`             | Admin ou Mestre | Anexa a digitalização do termo impresso assinado                        |
| POST   | `/v1/eu/guerreiros/{id}/biometria/recusa`   | Responsável     | Grava a recusa da biometria e a data do apagamento do _template_        |
| GET    | `/v1/eu/guerreiros/{id}/biometria`          | Responsável     | Estado da captura, decisão do termo e data do apagamento, quando houver |
| POST   | `/v1/guerreiros/{id}/fim-de-vinculo`        | Admin           | Encerra o vínculo do Guerreiro(a) com o projeto, com motivo             |
| GET    | `/v1/eu/guerreiros/{id}/dados`              | Responsável     | Dados armazenados, finalidade e prazo de guarda de cada um              |
| GET    | `/v1/eu/guerreiros/{id}/acessos`            | Responsável     | Quem acessou, em que papel, qual dado e quando                          |
| POST   | `/v1/solicitacoes`                          | Responsável     | Abre solicitação com protocolo e prazo de 7 dias                        |
| GET    | `/v1/eu/solicitacoes`                       | Responsável     | Protocolo, tipo, situação e prazo das próprias solicitações             |
| GET    | `/v1/termos`                                | autenticada     | Termos vigentes e versões anteriores                                    |
| POST   | `/v1/termos/{versao}/leitura`               | Responsável     | Registra a leitura do termo, com data e hora                            |
| POST   | `/v1/sugestoes`                             | Responsável     | Registra proposta na fila única da gestão                               |
| GET    | `/v1/eu/sugestoes`                          | Responsável     | Status das próprias propostas                                           |

A recusa da biometria é rota **separada** da autorização única: a `/v1/eu/guerreiros/{id}/autorizacao`
não alcança a biometria (`RN-13-06`). O fim do vínculo é restrito ao Admin pela matriz de
permissões existente — nenhuma `Operacao` nova.

Erros previstos: consulta a Guerreiro(a) não vinculado (403); concessão quando há recusa
vigente de outro responsável (409, com o estado suspenso e a orientação de procurar a gestão);
revogação sem autorização vigente (409); senha provisória ainda não trocada (403 em qualquer
rota que não seja a da troca); ato assistido sem responsável presente identificado (422);
segunda solicitação idêntica em aberto (409); tentativa de criar vínculo ou cadastrar
responsável (403); tentativa de ler consulta ao assistente ou transcrição de apoio escolar
(403). O **pedido de exclusão é aceito** e respondido como despersonalização — não é erro.

A solicitação da divergência (`RF-13-19`) é aberta pelo próprio núcleo, do tipo
`esclarecimento`, em nome de quem recusou, e não pelo responsável — uma só enquanto estiver em
aberto por Guerreiro(a) (documento 09 §1).

## 10. Requisitos não funcionais

- Web App responsivo **Mobile First**, projetado para o **celular modesto** da família, que
  costuma ser o único aparelho da casa.
- **Linguagem simples de adulto**, no padrão exigido da política de privacidade: sem jargão
  jurídico, sem termo técnico e sem código de erro na tela.
- **Rede instável**: a leitura da evolução tolera queda com o que já foi carregado; a
  concessão e a revogação **exigem rede**, porque geram registro versionado — e a tela diz
  isso, em vez de simular sucesso.
- **Aparelho compartilhado da família**: botão de sair sempre visível e nenhum dado da criança
  em cache depois do encerramento da sessão.
- **Acessibilidade digital** no piso do documento 15 — **WCAG 2.2 AA**: contraste, alvos de
  toque grandes e leitura por voz — parte dos responsáveis tem baixa escolaridade ou pouca
  familiaridade com aplicativos.
- **Uso raro é a condição normal**: o responsável entra poucas vezes no ciclo, e a aplicação
  precisa ser compreensível sem aprendizado acumulado.
- Escrita idempotente: reenviar a mesma concessão por falha de rede não gera dois registros.
- Idioma pt-BR; código aberto.

## 11. LGPD e proteção da criança

| Dado coletado                 | Finalidade                             | Base legal      | Retenção                                      | Quem acessa          |
| ----------------------------- | -------------------------------------- | --------------- | --------------------------------------------- | -------------------- |
| E-mail do responsável         | Identificar e dar acesso à App 07      | consentimento   | enquanto durar o vínculo                      | gestão               |
| Grau de parentesco            | Provar a legitimidade de quem autoriza | obrigação legal | enquanto durar o vínculo                      | gestão               |
| Consentimentos versionados    | Prova do que foi autorizado e quando   | obrigação legal | permanente                                    | gestão e responsável |
| Anexo do termo impresso       | Prova documental da assinatura         | obrigação legal | permanente                                    | gestão               |
| Solicitações e seus desfechos | Atender direitos do titular            | obrigação legal | permanente                                    | gestão e responsável |
| Proposta registrada           | Evolução da plataforma                 | consentimento   | 90 dias após o retorno; permanente se adotada | gestão               |
| Registro de leitura do termo  | Medir a hipótese H2 e provar ciência   | obrigação legal | permanente                                    | gestão e responsável |

- **Consentimento**: a autorização é **uma só** e a tela declara o que ela libera antes de
  qualquer botão. Conceder vale para tudo; recusar também.
- **Alternativa a quem recusa**: a criança participa igual, entrega a produção ao Mestre no
  encontro e não aparece publicamente. **Recusa não exclui de nada.**
- **Titularidade**: o titular é o Guerreiro(a); o responsável **exerce os direitos** em nome
  dele.
- **Limite da exclusão**: o dado de território é **despersonalizado, não apagado**, e isso é
  dito na tela e no termo antes do aceite — não descoberto depois. O _template_ biométrico é a
  exceção: ele é **apagado**, no pedido de exclusão e ao fim do vínculo.
- **Transparência de acesso**: o responsável vê **quem acessou** os dados da criança, com data,
  hora, papel e dado — a trilha de auditoria do PRD-01 exposta a quem responde pela criança.
- **Dado de outra criança nunca aparece**, nem em equipe, nem em ranking, nem em criação
  coletiva: o que é de terceiro é reduzido a avatar e nick.
- **O que a criança faz sozinha continua dela**: consultas ao assistente e transcrições de
  apoio escolar ficam restritas à gestão. Transparência com a família não é vigilância sobre a
  criança.
- **Aviso visível** em toda tela que coleta, com acesso à área detalhada sobre destino e uso.

## 12. Critérios de aceite e métricas

- Responsável cadastrado entra por login social; quem tem senha provisória é obrigado a
  trocá-la antes de ver qualquer dado.
- Conta social sem cadastro prévio é recusada, com a orientação de procurar a gestão.
- Responsável com dois vinculados vê os dois e alterna entre eles; um terceiro Guerreiro(a) não
  vinculado não aparece nem por busca.
- Concessão registrada faz o perfil aparecer na vitrine; revogação o retira **na mesma sessão**,
  junto com criações e elenco do jogo.
- Revogada a autorização, a App 05 passa a oferecer a entrega ao Mestre como alternativa, e a
  criança não perde missão.
- Recusa de um responsável quando outro já havia concedido deixa o estado **suspenso**, retira
  o perfil do público e abre solicitação para a gestão.
- Pedido de exclusão exibe o texto da despersonalização antes do aceite; confirmado, recebe
  protocolo e o registro de território permanece na série sem apontar pessoa.
- Solicitação sem desfecho em 7 dias aparece em atraso para o responsável e na fila da App 03.
- Histórico de acessos mostra o acesso do Mestre da turma com data, hora e dado consultado.
- Nenhuma tela exibe consulta ao assistente, transcrição de apoio escolar ou dado de outra
  criança.
- Ato assistido registrado por um Mestre aparece no histórico **em nome do responsável**, com
  quem operou e quem testemunhou.
- Termo impresso digitalizado e anexado produz o mesmo estado de autorização que o registro
  feito pelo responsável no aparelho.

Hipóteses do Ciclo 01 (documento 10): este PRD **sustenta H2** e é o único instrumento que a
mede — número de autorizações concedidas sobre o número de Guerreiros e Guerreiras ativos, com
o registro de leitura do termo provando o "tomar conhecimento". Ele também **isola H1 de H2**:
como a participação não depende da autorização, a recusa da família não contamina a medição da
adesão da criança.

## 13. Decisões tomadas neste PRD

| Decisão                                                                                                            | Gravada em | Linha do doc 09                                                            |
| ------------------------------------------------------------------------------------------------------------------ | ---------- | -------------------------------------------------------------------------- |
| Autorização única do responsável, cobrindo divulgação, eventos e produção                                          | 03 §§9, 12 | Autorização única do responsável                                           |
| Qualquer responsável autoriza ou revoga, e a recusa prevalece                                                      | 02 §1      | Quem autoriza entre os responsáveis                                        |
| Atendimento assistido e termo impresso para quem não tem smartphone                                                | 03 §9      | Responsável sem smartphone                                                 |
| A exclusão do _template_ biométrico é requisito deste PRD, não do PRD-01                                           | 03 §3.3    | Exclusão do _template_ biométrico                                          |
| Aviso da exclusão do _template_ na App 07, com a data                                                              | 03 §9      | Aviso da exclusão do _template_ biométrico                                 |
| Divergência sem acordo mantém a autorização suspensa, com alternativa                                              | 05 §4      | Desfecho da divergência entre responsáveis                                 |
| Solicitação da divergência entra como `esclarecimento`, em nome de quem recusou, uma só em aberto por Guerreiro(a) | PRD-13 §9  | Tipo da solicitação que a suspensão por divergência abre na fila da App 03 |
| Fim do vínculo do Guerreiro(a) por ato de Admin e por varredura dos 12 meses sem atividade                         | 03 §12.2   | Marco do fim do vínculo do Guerreiro(a)                                    |
| Comando de manutenção do núcleo cumpre os prazos de guarda — encerra vínculos e apaga _templates_                  | 03 §12.2   | Execução dos prazos de guarda                                              |
| Recusa da biometria pelo responsável marca o apagamento do _template_ em 5 dias                                    | 03 §3.3    | Apagamento do _template_ biométrico por recusa                             |
| Os três registros que contam como atividade nos 12 meses: presença, resultado e coleta                             | 03 §12.2   | O que conta como atividade na varredura dos 12 meses                       |
| A marca de apagamento não se cancela nem se adia por gatilho posterior                                             | 03 §12.2   | A marca de apagamento é definitiva                                         |
| Execução da despersonalização do registro de território (`RN-13-12`) adiada para o Ciclo 02                        | 09 §1      | Execução da despersonalização do dado de território                        |

As três primeiras decisões fecharam a pendência do **consentimento da captação da produção** e a
**[Proposta]** de consentimento por divulgação de vídeos e fotos de eventos, que deixou de
existir como termo à parte. O `Consentimento` do PRD-01 ganhou os atributos **origem** e **quem
operou**, e a `SolicitacaoDoResponsavel` teve seus atributos detalhados no mesmo PRD. O
documento 08 perdeu a questão em aberto do responsável sem smartphone.

## 14. Pendências que permanecem

- **Estado da reparação da ocorrência de conduta** (`RF-13-09`): falta o requisito que registre
  a reparação — quem a lança e se ela devolve os pontos debitados. Sem ele, a evolução exibe a
  ocorrência com motivo e data, e nunca o estado da reparação. Decisão do fundador,
  2026-08-31 (documento 09 §1).
- **Redação do termo quanto à entrega de dados**: a regra, a licença CC BY-SA e o critério de
  aprovação do Admin estão decididos; falta o **texto** que declara isso ao responsável.
  **Trava o `RF-13-34` no texto, não no desenho.**
- **Metas numéricas de H2** (documento 10): quantas autorizações caracterizam a hipótese
  confirmada. Sem elas, a métrica existe e o critério de sucesso não.
- **Tela da App 03 que encerra o vínculo do Guerreiro(a)**: o ato de Admin nasceu no núcleo
  nesta fatia (`POST /v1/guerreiros/{id}/fim-de-vinculo`); a tela da gestão que o alcança é do
  PRD-02, e entra no cronograma dele. Até lá, o ato só é alcançável pela API.
- **Volta do Guerreiro(a) que teve o vínculo encerrado**: nenhum requisito descreve o que
  acontece quando ele retorna ao projeto — a decisão do fundador de 2026-09-01 só fixa que a
  volta exige nova captura biométrica, com novo termo (documento 09 §1).
  Duas saíram desta lista, decididas e gravadas na §13: o **desfecho da divergência**, em que a
  autorização permanece suspensa e vale a alternativa equivalente, e o **aviso da exclusão do
  _template_**, que a App 07 exibe com a data. A **reidentificação em comunidade com poucos
  coletores** também saiu: a agregação mínima tem piso de três coletores (documento 02 §1). O
  **marco do fim do vínculo**, o **comando de manutenção** e a **execução da despersonalização
  do território** também saíram, gravados na §13.

## 15. Rastreabilidade

| Requisito               | Origem                                                          |
| ----------------------- | --------------------------------------------------------------- |
| `RF-13-01` a `RF-13-06` | 03 §1.1 (autenticação por persona) e 02 §1 (cadastro e vínculo) |
| `RF-13-07` a `RF-13-12` | 03 §9 (evolução do Guerreiro(a)) e 11 §6 (nível como percurso)  |
| `RF-13-13` a `RF-13-21` | 03 §§9, 12 (autorização única) e 02 §1 (quem exerce)            |
| `RF-13-22` a `RF-13-28` | 03 §§9, 12.1 (solicitações, recusa e limite da exclusão)        |
| `RF-13-43` e `RF-13-44` | 03 §§3.3, 12.2 (exclusão do _template_ e prazos)                |
| `RF-13-29` a `RF-13-34` | 03 §§9, 12.2 (transparência e prazos), 12.3 (entrega de dados)  |
| `RF-13-35` a `RF-13-38` | 03 §9 (atendimento assistido e termo impresso)                  |
| `RF-13-39` a `RF-13-42` | 03 §§7, 9, 12 (fila única, canal fechado e aviso de coleta)     |
