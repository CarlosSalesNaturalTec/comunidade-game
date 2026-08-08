# PRD-10 — Batalhas e eventos presenciais

## 1. Identificação

| Campo            | Valor                                              |
| ---------------- | -------------------------------------------------- |
| PRD              | PRD-10                                             |
| Aplicação        | — (domínio operado pelas Apps 01, 03, 05, 06 e 09) |
| Onda             | 5                                                  |
| Situação         | em revisão                                         |
| Versão e data    | v1 — 2026-08-07                                    |
| Depende de       | PRD-01, PRD-09                                     |
| Documentos-fonte | 02 §§5, 6, 8; 07; 11 §§2.1, 4, 5, 8.1, 8.4         |

## 2. Contexto e objetivo

A batalha é o momento em que o que foi aprendido e construído vira disputa pública. Ela fecha o
ciclo da trilha — aprender, construir, batalhar, pontuar — e é o único ponto do Ciclo 01 em que
um artefato físico feito pelos Guerreiros e Guerreiras conversa com a plataforma.

Este PRD define esse domínio: como a batalha é cadastrada como marco de trilha, como a partida
abre com as equipes da aula, como a telemetria chega à API durante a disputa e como o resultado
vira atividade realizada, pontos, portfólio e vitrine. A Batalha de Laser (documento 07) é o
caso de referência; o modelo é agnóstico de área e serve à batalha de rima e à roda de capoeira
quando elas chegarem.

No Ciclo 01, entregue este domínio, a turma da Guerreira Zeferina disputa a Batalha de Laser em
novembro com os artefatos que ela mesma construiu, e o resultado da partida entra na plataforma
sem ninguém digitar planilha.

## 3. Escopo

### 3.1 Dentro do escopo

- Cadastro da batalha pelo Mestre autor, vinculada a uma trilha e ao marco que ela cumpre.
- Duas modalidades: **presencial com telemetria** e **de projetos e ideias**, no mesmo cadastro.
- Declaração dos papéis disputados e, em cada um, da métrica que apura o desempenho.
- Agendamento do encontro da batalha pela gestão, como qualquer aula presencial.
- Abertura da partida no Nexus, com as equipes da aula e o vínculo artefato → equipe →
  Guerreiro(a).
- **Conferência de segurança** registrada como trava de início da partida.
- Ponte Nexus → API **ao vivo**, com o Nexus como único ponto com saída para a internet.
- Apuração automática do resultado e do melhor desempenho de cada papel.
- Lançamento da atividade realizada e dos pontos da batalha, pela tabela do documento 11.
- Anulação da partida pelo Mestre, havendo contestação.
- Resultado e estatísticas alimentando portfólio, ranking e vitrine.

### 3.2 Fora do escopo

- Firmware dos artefatos e código do painel do Nexus: são conteúdo da trilha 2, não da
  plataforma.
- Culminância e criação original — são do PRD-09 e do PRD-05; a batalha só as antecede.
- Batalha entre comunidades diferentes: no Ciclo 01 há uma comunidade, e a partida é da turma.
- Transmissão ao vivo da partida para o público: nada além do painel da sala no Ciclo 01.
- Batalhas de rima e capoeira: ciclo futuro, e o modelo aqui já as comporta.
- Credencial de dispositivo para os artefatos: eles não falam com a API; quem fala é o Nexus.

## 4. Personas e permissões

| Persona      | O que faz                                                                                                 | O que não pode fazer                                                                |
| ------------ | --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Mestre autor | Cadastra a batalha na trilha, declara papéis, métricas e roteiro de segurança, conduz e encerra a partida | Alterar resultado lançado; iniciar partida sem conferência de segurança             |
| Admin        | Agenda o encontro da batalha, acompanha o painel do dia, lança resultado quando a ponte não completa      | Formar ou editar equipe; alterar a métrica declarada pelo Mestre autor              |
| Guerreiro(a) | Disputa a partida no papel que assumiu, pela equipe que formou na aula                                    | Escolher o próprio papel sem o Mestre; disputar sem presença registrada na aula     |
| Nexus        | Estação de controle: abre a partida, apura e envia a telemetria, sob a sessão do Mestre                   | Existir como persona ou credencial própria; escrever qualquer coisa fora da partida |
| Visitante    | Vê batalhas, resultados e estatísticas nas rotas públicas                                                 | Ver nick de quem não tem divulgação autorizada                                      |

## 5. Jornadas principais

### 5.1 Mestre cadastra a batalha na trilha

1. Na App 09, dentro da trilha, o Mestre cria a batalha e a vincula ao **marco** que ela cumpre.
2. Declara a **modalidade**: presencial com telemetria ou de projetos e ideias.
3. Na presencial com telemetria, declara os **artefatos** da partida, os **papéis** disputados e,
   em cada papel, a **métrica** que apura o desempenho — precisão do Caçador, acertos absorvidos
   sem penalidade do Defensor.
4. Declara a **condição de vitória** e o **roteiro de conferência de segurança**.
5. Declarando recompensa no marco, a trilha só publica com o lastro registrado — regra do
   PRD-09, aplicada aqui sem exceção.
6. **Exceção:** batalha com telemetria e nenhum papel com métrica declarada não é aceita — sem
   métrica não há como apurar o ponto de desempenho.

### 5.2 Gestão agenda o encontro

1. Na App 03, o Admin agenda o encontro com comunidade, data, horário inicial e final, como
   qualquer aula presencial.
2. Marca no encontro qual batalha será disputada.
3. O painel do dia passa a mostrar a batalha prevista e os artefatos que ela exige.
4. **Exceção:** sem encontro agendado não há partida — é a mesma regra que rege o App 01.

### 5.3 A turma chega e forma as equipes

1. Os Guerreiros e Guerreiras entram no App 01 por nick e imagem, e a presença é registrada.
2. As equipes são formadas por eles mesmos, no App 01, e valem para aquela aula.
3. **Exceção:** quem não teve presença registrada não é vinculado a artefato na partida.

### 5.4 Mestre abre a partida no Nexus

1. O Mestre autentica no Nexus com a **própria sessão** — o Nexus não tem credencial de
   dispositivo.
2. O Nexus se conecta à internet pelo **Wi-Fi do local**; não havendo, pelos **dados móveis do
   Admin ou do Mestre** presentes na atividade.
3. O Nexus lê as **equipes da aula em andamento** e a batalha prevista para o encontro.
4. O Mestre vincula cada **artefato** a uma equipe e ao **Guerreiro(a) que o opera**, pelo nick.
5. O Nexus apresenta o **roteiro de conferência de segurança** — classe do laser, proteção
   ocular, área de tiro delimitada, ninguém mirando o rosto — e o Mestre confirma item a item.
6. Confirmada a conferência, o Nexus a grava com quem conferiu, data e hora, e libera o "Start".
7. **Exceção:** sem conferência registrada o "Start" não é liberado, e a tela diz o que falta.

### 5.5 A partida acontece

1. O Nexus publica o comando de início; a partida corre com a lógica rodando **local em cada
   artefato**, na rede isolada.
2. O Nexus assina os tópicos da partida, exibe o painel na sala e **envia os eventos à API
   durante a disputa**.
3. A partida termina quando a **condição de vitória declarada** se cumpre.
4. **Exceção — internet fora:** a partida não para nem muda de resultado; o Nexus acumula o que
   não enviou e retoma assim que a saída volta.
5. **Exceção — artefato fora do ar:** a partida segue pelo que os demais publicam, e o papel sem
   telemetria fica sem apuração de desempenho.

### 5.6 Encerramento e pontuação

1. O Mestre aciona o encerramento no Nexus e vê o **resumo da partida** antes de qualquer
   lançamento.
2. O Nexus apura o resultado e o **melhor de cada papel**, pela métrica que o Mestre declarou.
3. Confirmado o encerramento, a API lança a **atividade realizada** e credita: **10** a cada
   integrante que disputou, **+10** a cada integrante da equipe vencedora e **+5** ao melhor de
   cada papel.
4. O resultado entra no portfólio de cada integrante e, havendo divulgação autorizada, na
   vitrine.
5. **Exceção — telemetria incompleta:** o +5 não é distribuído, e o Mestre lança o resultado
   pela App 09, como o documento 11 já prevê.
6. **Exceção — contestação:** o Mestre anula a partida; nada é creditado e a anulação fica
   registrada com o motivo.

### 5.7 Batalha de projetos e ideias

1. O Mestre cadastra a batalha na modalidade de projetos, sem artefato e sem papéis.
2. No encontro, as equipes apresentam e disputam; não há Nexus nem telemetria.
3. O Mestre registra as equipes que disputaram e o resultado, e a API credita os **10** e os
   **+10**. O **+5 não existe** nesta modalidade.

### 5.8 Visitante vê a batalha

1. Na vitrine, a seção de batalhas mostra a partida, as equipes e o resultado.
2. Aparecem por nick e avatar apenas os Guerreiros e Guerreiras com **divulgação autorizada**;
   os demais disputaram e pontuaram igual, e simplesmente não são nomeados.

## 6. Requisitos funcionais

### 6.1 Cadastro da batalha (App 09)

| ID         | Requisito                                                                              | Prioridade |
| ---------- | -------------------------------------------------------------------------------------- | ---------- |
| `RF-10-01` | Mestre autor cadastra a batalha vinculada a uma trilha e ao marco que ela cumpre       | essencial  |
| `RF-10-02` | Mestre declara a modalidade: presencial com telemetria ou de projetos e ideias         | essencial  |
| `RF-10-03` | Mestre declara os papéis disputados e, em cada papel, a métrica que apura o desempenho | essencial  |
| `RF-10-04` | Mestre declara os artefatos que a partida exige e o que cada um publica                | essencial  |
| `RF-10-05` | Aplicação recusa batalha com telemetria sem ao menos um papel com métrica declarada    | essencial  |
| `RF-10-06` | Mestre declara a condição de vitória da partida                                        | essencial  |
| `RF-10-07` | Mestre declara o roteiro de conferência de segurança exigido antes do início           | essencial  |
| `RF-10-08` | Mestre declara se a modalidade admite o familiar de 17 anos ou mais na equipe          | essencial  |
| `RF-10-09` | Mestre duplica uma batalha já cadastrada como ponto de partida de outra                | desejável  |

### 6.2 Agendamento (App 03)

| ID         | Requisito                                                                               | Prioridade |
| ---------- | --------------------------------------------------------------------------------------- | ---------- |
| `RF-10-10` | Admin marca, no encontro agendado, qual batalha será disputada                          | essencial  |
| `RF-10-11` | Painel do dia mostra a batalha prevista e os artefatos que ela exige                    | essencial  |
| `RF-10-12` | Batalha sem encontro agendado não abre partida                                          | essencial  |
| `RF-10-13` | Admin lança o resultado da partida cuja telemetria não completou, com motivo registrado | essencial  |

### 6.3 Abertura da partida (Nexus)

| ID         | Requisito                                                                                      | Prioridade |
| ---------- | ---------------------------------------------------------------------------------------------- | ---------- |
| `RF-10-14` | Mestre autentica no Nexus com a própria sessão, sem credencial de dispositivo                  | essencial  |
| `RF-10-15` | Nexus lê as equipes da aula em andamento e a batalha prevista para o encontro                  | essencial  |
| `RF-10-16` | Mestre vincula cada artefato a uma equipe e ao Guerreiro(a) que o opera, pelo nick             | essencial  |
| `RF-10-17` | Guerreiro(a) sem presença registrada na aula não é vinculado a artefato                        | essencial  |
| `RF-10-18` | Nexus registra a conferência de segurança com os itens confirmados, quem conferiu, data e hora | essencial  |
| `RF-10-19` | Nexus recusa iniciar a partida sem a conferência registrada, dizendo o que falta               | essencial  |
| `RF-10-20` | Nexus mostra, antes do início, quem disputa por qual equipe e em qual papel                    | essencial  |

### 6.4 Partida e telemetria

| ID         | Requisito                                                                                    | Prioridade |
| ---------- | -------------------------------------------------------------------------------------------- | ---------- |
| `RF-10-21` | Lógica da partida roda local em cada artefato, sem depender da rede nem da plataforma        | essencial  |
| `RF-10-22` | Nexus envia os eventos de telemetria à API durante a partida                                 | essencial  |
| `RF-10-23` | Evento reenviado não duplica o registro, pela sequência declarada na partida                 | essencial  |
| `RF-10-24` | Queda de internet não interrompe a partida nem altera o resultado                            | essencial  |
| `RF-10-25` | Nexus retoma o envio do que ficou pendente assim que a saída para a internet volta           | essencial  |
| `RF-10-26` | Painel do Nexus exibe em tempo real energia, resistência do escudo e vida da torre           | essencial  |
| `RF-10-27` | Artefato fora do ar não interrompe a partida; o papel sem telemetria fica sem apuração       | essencial  |
| `RF-10-45` | Nexus usa o Wi-Fi do local e, na falta dele, os dados móveis do Admin ou do Mestre presentes | essencial  |
| `RF-10-46` | Nexus mostra qual saída está em uso e avisa quando nenhuma das duas está disponível          | essencial  |

### 6.5 Encerramento e pontuação

| ID         | Requisito                                                                                 | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------- | ---------- |
| `RF-10-28` | Partida encerra quando a condição de vitória declarada se cumpre                          | essencial  |
| `RF-10-29` | Mestre aciona o encerramento e vê o resumo da partida antes de qualquer lançamento        | essencial  |
| `RF-10-30` | Nexus apura o melhor de cada papel pela métrica que o Mestre declarou                     | essencial  |
| `RF-10-31` | API lança a atividade realizada e credita 10 pontos a cada integrante que disputou        | essencial  |
| `RF-10-32` | API credita +10 pontos a cada integrante da equipe vencedora                              | essencial  |
| `RF-10-33` | API credita +5 pontos ao melhor de cada papel apurado na telemetria                       | essencial  |
| `RF-10-34` | Partida sem telemetria completa não distribui o +5, e o resultado é lançado pelo Mestre   | essencial  |
| `RF-10-35` | Empate declarado registra a partida sem crédito dos +10 da equipe vencedora               | essencial  |
| `RF-10-36` | Mestre anula a partida havendo contestação, com motivo registrado e sem crédito de pontos | essencial  |
| `RF-10-37` | Lançamento da partida não é editável; a correção referencia o lançamento original         | essencial  |

### 6.6 Batalha de projetos e ideias

| ID         | Requisito                                                                      | Prioridade |
| ---------- | ------------------------------------------------------------------------------ | ---------- |
| `RF-10-38` | Batalha de projetos abre sem Nexus, sem artefato e sem telemetria              | essencial  |
| `RF-10-39` | Mestre registra as equipes que disputaram e o resultado da batalha de projetos | essencial  |
| `RF-10-40` | Batalha de projetos credita os 10 e os +10, e nunca o +5 de desempenho         | essencial  |

### 6.7 Exibição do resultado

| ID         | Requisito                                                                              | Prioridade |
| ---------- | -------------------------------------------------------------------------------------- | ---------- |
| `RF-10-41` | Resultado e estatísticas da partida entram no portfólio de cada integrante             | essencial  |
| `RF-10-42` | Vitrine exibe a batalha, as equipes e o resultado, sem nomear quem não tem divulgação  | essencial  |
| `RF-10-43` | App 05 mostra ao Guerreiro(a) a sua participação, o papel e as estatísticas da partida | essencial  |
| `RF-10-44` | App 07 mostra ao responsável a participação do Guerreiro(a) sob sua responsabilidade   | essencial  |

## 7. Regras de negócio

| ID         | Regra                                                                                                | Invariante | Fonte   |
| ---------- | ---------------------------------------------------------------------------------------------------- | ---------- | ------- |
| `RN-10-01` | A batalha é marco de trilha declarado pelo Mestre autor, nunca evento avulso da gestão               | —          | 02 §6   |
| `RN-10-02` | A partida acontece em encontro agendado pela gestão, e sem ele não abre                              | 4          | 02 §6   |
| `RN-10-03` | As equipes que disputam são as da aula, formadas pelos próprios Guerreiros e Guerreiras no App 01    | 15         | 02 §5   |
| `RN-10-04` | A equipe tem até 5 integrantes e, quando a batalha admitir, no máximo 1 familiar de 17 anos ou mais  | 15         | 02 §5   |
| `RN-10-05` | Sem a conferência de segurança registrada, a partida não inicia                                      | —          | 07      |
| `RN-10-06` | Toda a lógica da partida roda local no artefato; a rede do jogo é exclusivamente telemetria          | —          | 07      |
| `RN-10-07` | O Nexus é o único ponto com saída para a internet, e a rede dos artefatos segue isolada              | —          | 07      |
| `RN-10-08` | O Nexus opera sob a sessão do Mestre que conduz a partida, sem credencial de dispositivo             | —          | 07      |
| `RN-10-09` | A batalha credita 10 por disputar, +10 à equipe vencedora e +5 ao melhor desempenho de cada papel    | —          | 11 §5   |
| `RN-10-10` | O +5 sai por papel, pela métrica declarada no cadastro; batalha sem telemetria não o distribui       | —          | 11 §5   |
| `RN-10-11` | Os pontos da batalha são regulares: alimentam nível e ranking                                        | —          | 11 §5   |
| `RN-10-12` | O crédito é da atividade validada, não do jogo: a partida lança atividade realizada                  | 8          | 11 §8.4 |
| `RN-10-13` | Lançamento de partida não é editável; a correção referencia o original                               | —          | 11 §5.1 |
| `RN-10-14` | A batalha só acontece com lastro dos recursos que ela exige, artefatos inclusive                     | 9          | 02 §4   |
| `RN-10-15` | Recompensa prometida no marco batalha exige lastro registrado antes da publicação da trilha          | 9          | 02 §8   |
| `RN-10-16` | Guerreiro(a) sem divulgação autorizada disputa e pontua igual, e não é nomeado em lugar público      | 12         | 03 §8   |
| `RN-10-17` | Nenhuma imagem real do Guerreiro(a) entra no registro da partida, na vitrine ou no portfólio         | 12         | 03 §12  |
| `RN-10-18` | Recusar o papel de risco não exclui o Guerreiro(a) da batalha: há papel equivalente na mesma partida | 11         | 03 §12  |
| `RN-10-19` | A batalha é marco de trilha de qualquer área, e o modelo não pressupõe poder técnico                 | —          | 02 §6   |
| `RN-10-20` | A saída do Nexus é o Wi-Fi do local e, na falta dele, os dados móveis do Admin ou Mestre presentes   | —          | 07      |
| `RN-10-21` | O consumo de dados móveis na batalha é aporte por absorção de quem o proveu                          | —          | 04 §1   |

## 8. Modelo de dados

A `Batalha` já constava do bloco de operação do PRD-01. Este PRD lhe dá atributos e acrescenta
as quatro entidades da partida. `Equipe`, `Presenca`, `Aula/Agenda` e `Atividade` são do núcleo
e aqui apenas referenciadas.

```text
BATALHA (PRD-10)                    NÚCLEO (PRD-01)
Batalha                             Trilha / Missao / Atividade
ArtefatoDeBatalha                   Aula/Agenda
PartidaDeBatalha                    Equipe / Presenca
ParticipacaoNaPartida               Guerreiro(a)
EventoDeTelemetria                  Ponto / Nivel / Badge
ConferenciaDeSeguranca              RecompensaDeMarco (PRD-09)
```

| Entidade                 | Atributos essenciais                                                                                                                                                                                        |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Batalha`                | trilha, marco que cumpre, nome, modalidade (presencial com telemetria ou de projetos), condição de vitória, papéis disputados com a métrica de cada um, roteiro de segurança, admite familiar, Mestre autor |
| `ArtefatoDeBatalha`      | batalha, nome, papel a que serve, o que publica (tópico e grandeza), obrigatório ou opcional na partida                                                                                                     |
| `PartidaDeBatalha`       | batalha, encontro agendado, comunidade, Mestre que conduziu, início, fim, situação (aberta, encerrada, anulada), equipe vencedora ou empate, motivo da anulação                                             |
| `ParticipacaoNaPartida`  | partida, equipe, Guerreiro(a), papel, artefato operado, desempenho apurado na métrica do papel, melhor do papel                                                                                             |
| `EventoDeTelemetria`     | partida, artefato, sequência, momento, grandeza e valor publicados                                                                                                                                          |
| `ConferenciaDeSeguranca` | partida, itens confirmados, quem conferiu, data e hora                                                                                                                                                      |

O que é imutável: `EventoDeTelemetria` e `ConferenciaDeSeguranca` são **somente inserção**. A
`PartidaDeBatalha` encerrada não volta a abrir — a anulação é uma mudança de situação com
motivo, e a correção do lançamento referencia o original, nunca o substitui.

A `ParticipacaoNaPartida` é o que preserva o **crédito individual** dentro da realização
coletiva: a equipe vence, e o registro guarda o papel de cada integrante.

## 9. Contratos de API

| Método | Rota                             | Autenticação    | Descrição                                                                  |
| ------ | -------------------------------- | --------------- | -------------------------------------------------------------------------- |
| POST   | `/v1/batalhas`                   | Mestre autor    | Cadastra a batalha na trilha, com modalidade, papéis, métricas e segurança |
| GET    | `/v1/batalhas/{id}`              | autenticada     | Devolve a batalha cadastrada, com artefatos e papéis                       |
| GET    | `/v1/aulas/{id}/equipes`         | Mestre ou Admin | Equipes formadas na aula em andamento, para a abertura da partida          |
| POST   | `/v1/batalhas/{id}/partidas`     | Mestre          | Abre a partida com equipes, papéis, artefatos e a conferência de segurança |
| POST   | `/v1/partidas/{id}/telemetria`   | Mestre          | Recebe o lote de eventos da partida, idempotente pela sequência            |
| POST   | `/v1/partidas/{id}/encerramento` | Mestre          | Encerra, apura o resultado e o melhor de cada papel, e lança os pontos     |
| POST   | `/v1/partidas/{id}/resultado`    | Mestre ou Admin | Lança o resultado quando a telemetria não completou, com motivo            |
| POST   | `/v1/partidas/{id}/anulacao`     | Mestre          | Anula a partida com motivo, sem crédito de pontos                          |
| GET    | `/v1/guerreiros/{id}/batalhas`   | autenticada     | Participações do Guerreiro(a), com papel e estatísticas                    |
| GET    | `/v1/vitrine/batalhas`           | pública         | Batalhas, resultados e estatísticas, já definida no PRD-03                 |

Erros previstos: abertura de partida sem encontro agendado (422); abertura sem conferência de
segurança confirmada (422, dizendo qual item falta); vínculo de Guerreiro(a) sem presença
registrada na aula (422); cadastro de batalha com telemetria e nenhum papel com métrica (422);
telemetria de partida já encerrada (409); reenvio de sequência já recebida (200, sem duplicar);
encerramento por quem não conduziu a partida (403); tentativa de editar lançamento de partida
(405, com a rota de correção na mensagem).

## 10. Requisitos não funcionais

- **A partida nunca depende da plataforma.** Nem a rede, nem a API, nem o envio da telemetria
  são condição para a disputa acontecer ou terminar.
- **Rede do jogo isolada**, com o Nexus como único ponto conectado — é o que garante a
  estabilidade da partida independentemente do ambiente do evento.
- **Saída de internet do Nexus, em ordem:** Wi-Fi do local e, na falta dele, dados móveis do
  Admin ou do Mestre presentes — a premissa é que ao menos um chegue com dados disponíveis.
- Envio de telemetria tolerante a rede instável: em lote, com sequência, sem duplicar em
  reenvio.
- Painel do Nexus legível a distância, na sala, para quem assiste à partida.
- Telas de cadastro e de resultado responsivas, Mobile First, em pt-BR e linguagem simples.
- O roteiro de segurança é escrito para ser lido em voz alta antes da partida.
- Código aberto, como o restante da plataforma, e o do artefato é conteúdo de trilha.

## 11. LGPD e proteção da criança

| Dado coletado                     | Finalidade                                | Base legal        | Retenção                 | Quem acessa                             |
| --------------------------------- | ----------------------------------------- | ----------------- | ------------------------ | --------------------------------------- |
| Nick e equipe na partida          | Registrar quem disputou e por qual equipe | consentimento     | enquanto durar o vínculo | gestão, Mestre, responsável e o próprio |
| Papel e desempenho apurado        | Creditar os pontos da batalha             | consentimento     | enquanto durar o vínculo | gestão, Mestre, responsável e o próprio |
| Eventos de telemetria do artefato | Apurar resultado e desempenho             | consentimento     | enquanto durar o vínculo | gestão e Mestre                         |
| Conferência de segurança          | Provar que a partida iniciou conferida    | interesse público | permanente               | gestão                                  |
| Resultado exposto na vitrine      | Reconhecimento público da realização      | consentimento     | enquanto durar o vínculo | qualquer visitante                      |

- **A telemetria é dado de artefato, não de pessoa** — tiros, energia, acertos. Ela só toca a
  criança pelo vínculo com o nick, feito na abertura da partida; nenhum evento carrega nome,
  imagem ou contato.
- **Exposição pública só com divulgação autorizada.** Sem ela, o Guerreiro(a) disputa, pontua e
  aparece no seu próprio histórico e no do responsável — e não é nomeado em lugar público.
- **Recusar o papel de risco não exclui ninguém.** Quem não quiser ou não puder operar o laser
  disputa em outro papel da mesma partida, com o mesmo crédito de participação.
- A **conferência de segurança** é guardada permanentemente por ser prova de cuidado em
  atividade com criança, e não contém dado de Guerreiro(a): registra itens, quem conferiu e
  quando.
- Pedido de acesso, correção ou exclusão segue a fila da App 07, como todo o restante.

## 12. Critérios de aceite e métricas

- Batalha cadastrada com telemetria e sem métrica em nenhum papel é recusada, com a mensagem
  dizendo o que falta.
- Partida não inicia sem conferência de segurança registrada, e a tela nomeia o item pendente.
- Guerreiro(a) sem presença na aula não consegue ser vinculado a artefato.
- Desligada a internet no meio da partida, a disputa termina normalmente e o resultado é o
  mesmo; religada, os eventos pendentes chegam sem duplicar nenhum registro.
- Encerrada a partida, cada integrante que disputou tem 10 pontos, cada integrante da equipe
  vencedora tem +10, e o melhor de cada papel tem +5 — conferíveis um a um no extrato.
- Partida com telemetria incompleta não credita o +5, e o resultado lançado pelo Mestre carrega
  o motivo.
- Partida anulada não credita ponto algum e mantém o motivo consultável.
- Tentativa de editar o lançamento de uma partida é recusada, e a correção referencia o
  original.
- Visitante vê o resultado da batalha sem nenhum nick de quem não tem divulgação autorizada.

**Hipótese que sustenta:** a batalha é o marco da trilha 2 no calendário de novembro do
Ciclo 01 (documento 10) e alimenta a **H5** com um dado que o quiz não dá — o desempenho
medido em artefato construído pelo próprio Guerreiro(a). Ela não substitui a comparação
sondagem × desbloqueio, que segue sendo o instrumento da hipótese.

## 13. Decisões tomadas neste PRD

| Decisão                                                                                      | Gravada em | Linha do doc 09                        |
| -------------------------------------------------------------------------------------------- | ---------- | -------------------------------------- |
| A classe do Atacante passa a se chamar **Caçador**                                           | 07         | Nome da classe do Atacante na trilha 2 |
| Ponte Nexus → API ao vivo, sob a sessão do Mestre, com o Nexus único conectado               | 07         | Ponte Nexus → API                      |
| Conferência de segurança do laser como trava de início da partida                            | 07         | Segurança do laser na batalha          |
| O +5 da batalha sai por papel, pela métrica declarada no cadastro                            | 11 §5      | Critério do +5 da batalha              |
| Batalha é marco declarado na trilha, em encontro agendado, com as equipes da aula            | 02 §6      | Como a batalha entra na plataforma     |
| Saída de internet do Nexus: Wi-Fi do local e, na falta dele, dados móveis do Admin ou Mestre | 07         | Saída de internet do Nexus             |

A decisão da ponte fechou a proposta que estava aberta no documento 07 desde a primeira
redação. Ela dispensa credencial de dispositivo — o Nexus fala pela sessão do Mestre —, e por
isso **não depende** da pendência de acesso das aplicações de terceiros nem da autenticação do
sensor do Guerreiro(a), ambas ainda abertas no documento 09.

As entidades `ArtefatoDeBatalha`, `PartidaDeBatalha`, `ParticipacaoNaPartida`,
`EventoDeTelemetria` e `ConferenciaDeSeguranca` foram acrescentadas ao modelo do PRD-01, e a
`Batalha`, que já constava dele sem atributos, passou a tê-los aqui.

## 14. Pendências que permanecem

- **Catálogo de recompensas por marco** (documento 09): o que a batalha entrega como recompensa
  no Ciclo 01 continua indefinido. A trilha só publica com lastro, então a lacuna trava a
  publicação, não este domínio.
- **Autenticação do sensor do Guerreiro(a)** (documento 09): segue aberta e fora deste PRD — o
  sensor da coleta fala com a API, o artefato da batalha não.
- **Acesso das aplicações de terceiros** (documento 09): segue aberta. Enquanto não houver
  chave de aplicação, nenhum Nexus de terceiro conduz partida na plataforma.
- **Segurança física das demais atividades** (documento 09): eletrônica e ferramentas de
  oficina seguem sem norma escrita; só o laser da batalha ficou decidido.
- **Batalhas de outras áreas**: rima e capoeira são ciclo futuro. O modelo já as comporta, e
  cada uma precisará declarar os seus papéis e métricas quando entrar.

## 15. Rastreabilidade

| Requisito               | Origem                                                         |
| ----------------------- | -------------------------------------------------------------- |
| `RF-10-01` a `RF-10-09` | 02 §6 (batalha como marco de trilha) e 07 (papéis e segurança) |
| `RF-10-10` a `RF-10-13` | 02 §6 e 02 §1 (encontro agendado pela gestão)                  |
| `RF-10-14` a `RF-10-20` | 07 (Nexus, artefatos e conferência de segurança)               |
| `RF-10-21` a `RF-10-27` | 07 (lógica local e rede como telemetria)                       |
| `RF-10-45` e `RF-10-46` | 07 (saída de internet do Nexus)                                |
| `RF-10-28` a `RF-10-37` | 11 §5 (motor de pontuação) e 11 §5.1 (integridade dos pontos)  |
| `RF-10-38` a `RF-10-40` | 02 §6 (batalha de projetos e ideias)                           |
| `RF-10-41` a `RF-10-44` | 11 §8.1 (vitrine) e 11 §8.2 (páginas individuais)              |
