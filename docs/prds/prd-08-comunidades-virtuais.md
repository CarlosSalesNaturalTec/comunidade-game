# PRD-08 — Comunidades Virtuais e dados do território

## 1. Identificação

| Campo            | Valor                                                |
| ---------------- | ---------------------------------------------------- |
| PRD              | PRD-08                                               |
| Aplicação        | — (domínio consumido pelas Apps 02, 03, 05, 06 e 09) |
| Onda             | 1                                                    |
| Situação         | aprovado                                             |
| Versão e data    | v1 — 2026-08-02                                      |
| Depende de       | —                                                    |
| Documentos-fonte | 02 §1, 02 §2, 03 §12, 11 §4, 11 §5, 11 §7, 11 §8.3   |

## 2. Contexto e objetivo

A Comunidade Virtual é a representação digital da comunidade real em que o jogador vive, e ela
**existe na medida em que dados reais são registrados**. Este PRD define o domínio que sustenta
isso: a comunidade, o desafio de coleta, a série temporal, o registro e a pontuação recorrente
que remunera a continuidade da medição.

É o primeiro PRD da esteira porque é o que mais entidades introduz no núcleo. O ledger
(PRD-07) e o Backend API (PRD-01) são escritos depois dele e o consomem.

No Ciclo 01, entregue este domínio, um jogador da Guerreira Zeferina consegue abrir uma série
de medição do seu ponto do território, registrar por texto, voz, foto, vídeo ou sensor
construído na trilha do Robô Educa, ganhar pontos enquanto mantiver a série viva, e ver o
resultado no painel público da comunidade — que começa vazio e ganha corpo a cada registro.

## 3. Escopo

### 3.1 Dentro do escopo

- Cadastro da Comunidade Virtual por Admin, nascendo vazia, e marcação da comunidade default
  do onboarding.
- Vínculo obrigatório do jogador a exatamente uma comunidade, com histórico de transferências.
- Hierarquia de locais da comunidade: comunidade → bairro → rua → condomínio → bloco → quadra,
  cadastrada por Admin.
- Solicitação de novo local pelo jogador, aprovada pelo Mestre da trilha ou por um Admin,
  com alerta das solicitações em aberto.
- Catálogo de tipos de coleta, com forma de registro, unidade de medida e faixa esperada.
- Desafio de coleta criado pelo Mestre dentro da trilha, com cadência, vigência e quantidade
  de registros que pontuam por período.
- Série de coleta individual, com estados ativa, interrompida, retomada e encerrada.
- Registro de coleta com origem manual, por voz ou de sensor do jogador.
- Registro por **foto ou vídeo**, para o que se mede por evidência e não por número — lixo
  acumulado, buraco na via, poste apagado.
- Crédito automático de pontos recorrentes ao Poder do Território.
- Auditoria por amostragem do Mestre, com invalidação de registro e estorno dos pontos.
- Guarda permanente do registro com o coletor identificado.
- Painel público por comunidade, agregado até o nível da rua, e exportação anonimizada.

### 3.2 Fora do escopo

- Importação de fontes públicas de dados (INMET, prefeitura) — integração que não cabe no
  primeiro ciclo.
- Georreferenciamento por coordenada de GPS — a granularidade do Ciclo 01 é a hierarquia de
  locais declarada, não o ponto no mapa.
- Interface das telas de coleta — pertence ao PRD-05 (App 05) e ao PRD-06 (App 02).
- Escolha do banco de séries temporais — decisão de arquitetura do PRD-01.

## 4. Personas e permissões

| Persona     | O que faz neste domínio                                                                                                                     | O que não pode fazer                                                        |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Admin       | Cria comunidades e locais, define a default do onboarding, transfere jogador entre comunidades e avalia solicitações de novo local          | Registrar coleta no lugar do jogador                                        |
| Mestre      | Cria o desafio de coleta da sua trilha, aprova solicitações de novo local dos jogadores dela, audita registros por amostragem e os invalida | Alterar o valor registrado por um jogador                                   |
| Jogador     | Abre séries, seleciona o local, solicita novo local, registra medições e acompanha os pontos das suas séries                                | Apagar registro já gravado; criar local; abrir série fora da sua comunidade |
| Responsável | Consulta, pela App 07, o que a criança sob sua responsabilidade coletou                                                                     | Registrar, corrigir ou apagar dado do território                            |
| Visitante   | Consulta o painel público da comunidade, agregado e anonimizado                                                                             | Ver coletor, granularidade abaixo de rua ou dado bruto                      |

## 5. Jornadas principais

### 5.1 Admin abre a comunidade

1. Admin cria a Comunidade Virtual com nome, localização e granularidade máxima permitida.
2. A comunidade nasce **vazia**: sem locais, sem séries, sem jogadores.
3. Admin cadastra os locais do território, na hierarquia — é a lista que o jogador escolhe
   depois.
4. Admin marca uma comunidade como **default do onboarding** — sem isso, o App 01 não opera.

### 5.2 Mestre cria o desafio de coleta

1. Mestre, ao montar a trilha, vincula um desafio de coleta a um ponto de trilha.
2. Declara: tipo de coleta, cadência, vigência, granularidade exigida e **quantos registros
   do mesmo período pontuam**.
3. A trilha só pode ser publicada com ao menos um desafio de coleta (regra do PRD-09).

### 5.3 Jogador abre a série e registra

1. Jogador aceita o desafio de coleta e **seleciona o local** entre os cadastrados na sua
   comunidade, na granularidade exigida.
2. Faltando o local, o jogador **solicita a inclusão**. O **Mestre da trilha** (App 09) ou um
   **Admin** (App 03) aprova, e o local passa a existir; a série só abre depois disso. Os dois
   veem alerta das solicitações em aberto.
3. O sistema abre a **série**, individual, com a cadência herdada do desafio.
4. A cada período, o jogador registra por texto, por voz (App 02), por **foto ou vídeo** ou
   pelo sensor que construiu (Robô Educa), conforme o tipo de coleta exigir.
5. O registro nasce **válido** e credita os pontos na hora, até o limite de registros que
   pontuam naquele período.
6. Registro fora da faixa esperada do tipo de coleta é aceito e gravado, mas **marcado para
   auditoria** — a medição estranha pode ser a mais valiosa da série.

Exceção — sem rede: o registro é enfileirado no dispositivo e sincronizado depois, com a
**data e hora da medição** preservadas, não a do envio.

### 5.4 A série interrompe e retoma

1. Passado um período de cadência sem registro, a série continua ativa e o jogador é avisado.
2. Passado o **segundo período seguido** sem registro, a série é marcada **interrompida** e
   deixa de render pontos.
3. Os pontos já creditados permanecem.
4. Um novo registro **retoma** a série, sem recuperar os pontos do período parado.

### 5.5 Mestre audita por amostragem

1. O Mestre recebe uma amostra de registros das séries dos seus desafios, priorizando os
   marcados fora da faixa.
2. Confirma ou **invalida** o registro, com motivo.
3. A invalidação **estorna** os pontos daquele registro e fica no histórico da série.
4. Invalidação não apaga o registro: ele permanece gravado, marcado como inválido.

### 5.6 Visitante consulta o painel

1. O visitante abre o painel da comunidade, sem login.
2. Vê as séries históricas por tipo de coleta, agregadas **até o nível da rua**.
3. Não vê nick, nome, avatar nem qualquer identificação de quem coletou.

## 6. Requisitos funcionais

| ID         | Requisito                                                                                         | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------------- | ---------- |
| `RF-08-01` | Admin cria Comunidade Virtual com nome, localização e granularidade máxima                        | essencial  |
| `RF-08-02` | Admin marca exatamente uma comunidade como default do onboarding                                  | essencial  |
| `RF-08-03` | Admin transfere jogador entre comunidades, preservando a data da mudança                          | essencial  |
| `RF-08-04` | Admin cadastra locais na hierarquia comunidade → bairro → rua → condomínio → bloco → quadra       | essencial  |
| `RF-08-05` | Sistema mantém catálogo de tipos de coleta, com unidade e faixa esperada                          | essencial  |
| `RF-08-06` | Mestre cria desafio de coleta com tipo, cadência, vigência, granularidade e registros que pontuam | essencial  |
| `RF-08-07` | Jogador abre série individual selecionando um desafio e um local cadastrado da sua comunidade     | essencial  |
| `RF-08-08` | Jogador registra medição com valor, data e hora da medição e origem                               | essencial  |
| `RF-08-09` | Sistema credita, por registro válido, o valor do documento 11 §5 ao Poder do Território           | essencial  |
| `RF-08-10` | Sistema marca a série como interrompida após dois períodos de cadência seguidos sem registro      | essencial  |
| `RF-08-11` | Sistema retoma a série ao receber novo registro, sem recompor o período parado                    | essencial  |
| `RF-08-12` | Sistema marca para auditoria registro fora da faixa esperada do tipo de coleta                    | essencial  |
| `RF-08-13` | Mestre invalida registro com motivo, estornando os pontos e mantendo o registro gravado           | essencial  |
| `RF-08-14` | Sistema aceita registro vindo de sensor do jogador, identificando o dispositivo de origem         | essencial  |
| `RF-08-15` | Sistema enfileira registro feito sem rede e sincroniza depois, preservando a hora da medição      | essencial  |
| `RF-08-16` | Rota pública devolve a série histórica da comunidade agregada até rua, sem identificar coletor    | essencial  |
| `RF-08-17` | Jogador consulta suas séries, a situação de cada uma e os pontos que estão rendendo               | essencial  |
| `RF-08-18` | Responsável consulta, pela App 07, as séries da criança sob sua responsabilidade                  | desejável  |
| `RF-08-19` | Exportação de dados agregados e anonimizados por comunidade e período                             | desejável  |
| `RF-08-20` | Painel reflete visualmente o crescimento da comunidade conforme o documento 11 §8.3               | desejável  |
| `RF-08-21` | Sistema aceita foto ou vídeo como o próprio registro, quando o tipo de coleta assim o define      | essencial  |
| `RF-08-22` | Jogador solicita a inclusão de local ausente, e a solicitação entra na fila de aprovação          | essencial  |
| `RF-08-23` | Mestre da trilha ou Admin aprova ou recusa a solicitação, com motivo na recusa                    | essencial  |
| `RF-08-24` | Mestre e Admin veem alerta das solicitações de local em aberto nas suas aplicações                | essencial  |

## 7. Regras de negócio

| ID         | Regra                                                                                                                         | Invariante | Fonte   |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------- | ------- |
| `RN-08-01` | Comunidade Virtual é criada apenas por Admin e nasce vazia                                                                    | 4          | 02 §1   |
| `RN-08-02` | Todo jogador tem vínculo obrigatório a exatamente uma comunidade, atribuído pela default                                      | 4          | 02 §1   |
| `RN-08-03` | O registro pertence à comunidade vigente do jogador na data da medição                                                        | —          | 02 §1   |
| `RN-08-04` | A série é individual: um coletor por série                                                                                    | —          | 02 §1   |
| `RN-08-05` | Registro válido rende valor único, igual para todo tipo de coleta, sem teto por período                                       | 6          | 11 §5   |
| `RN-08-06` | Quantos registros de um mesmo período de cadência pontuam é declarado no desafio                                              | 6          | 11 §5   |
| `RN-08-07` | Dois períodos de cadência seguidos sem registro interrompem a série                                                           | 6          | 02 §1   |
| `RN-08-08` | Série interrompida cessa o cômputo; os pontos já creditados permanecem                                                        | 6          | 02 §1   |
| `RN-08-09` | Registro nasce válido; o Mestre audita por amostragem e pode invalidar, estornando os pontos                                  | —          | 02 §1   |
| `RN-08-10` | Registro nunca é apagado nem editado: correção se faz por invalidação e novo registro                                         | 7          | 02 §1   |
| `RN-08-11` | O vínculo entre registro e jogador coletor é permanente, inclusive após a saída dele do projeto                               | 7          | 02 §1   |
| `RN-08-12` | Anonimização se aplica na saída — painéis, exportações e pesquisas —, nunca no armazenamento                                  | 7          | 02 §1   |
| `RN-08-13` | A saída pública agrega até o nível da rua; abaixo disso, só uso interno ou entrega com acordo                                 | 7          | 02 §1   |
| `RN-08-14` | Toda trilha tem ao menos um desafio de coleta                                                                                 | 5          | 02 §3   |
| `RN-08-15` | Pontos da coleta creditam o Poder do Território, não o poder da trilha em que o desafio nasceu                                | —          | 02 §2   |
| `RN-08-16` | Registro em foto ou vídeo que contenha pessoa identificável é invalidado na auditoria                                         | 12         | 03 §12  |
| `RN-08-17` | O jogo nunca credita pontos de coleta; o crédito vem do registro validado                                                     | 8          | 11 §8.4 |
| `RN-08-18` | Local nasce de cadastro do Admin ou de solicitação aprovada por Admin ou pelo Mestre da trilha; o pedido em si não cria local | 4          | 02 §1   |

## 8. Modelo de dados

```text
ComunidadeVirtual 1 ──── N Local            (hierarquia: parent opcional)
ComunidadeVirtual 1 ──── N SolicitacaoDeLocal (do jogador; vira Local se aprovada)
ComunidadeVirtual 1 ──── N VinculoJogador   (histórico; um vínculo vigente por jogador)
Trilha            1 ──── N DesafioDeColeta
DesafioDeColeta   1 ──── N SerieDeColeta    (uma por jogador que aceita o desafio)
SerieDeColeta     1 ──── N RegistroDeColeta
RegistroDeColeta  0..1 ── 1 Invalidacao
RegistroDeColeta  0..1 ── 1 Dispositivo     (quando a origem é sensor)
TipoDeColeta      1 ──── N DesafioDeColeta
```

| Entidade             | Atributos essenciais                                                                                                                                 |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ComunidadeVirtual`  | nome, localização, granularidade máxima, é_default, admin criador, data de criação                                                                   |
| `Local`              | comunidade, nível (comunidade, bairro, rua, condomínio, bloco, quadra), rótulo, local pai                                                            |
| `VinculoJogador`     | jogador, comunidade, data de início, data de fim, admin responsável pela transferência                                                               |
| `TipoDeColeta`       | nome, forma de registro (número, foto ou vídeo), unidade de medida, faixa esperada (mínimo e máximo)                                                 |
| `DesafioDeColeta`    | trilha, ponto de trilha, mestre autor, tipo, cadência, vigência, granularidade exigida, registros que pontuam por período                            |
| `SerieDeColeta`      | desafio, jogador coletor, local, cadência, estado, data de abertura, data da última medição válida                                                   |
| `RegistroDeColeta`   | série, valor, unidade, data e hora da medição, data e hora do registro, origem, dispositivo, mídia, situação, pontos creditados                      |
| `SolicitacaoDeLocal` | jogador solicitante, comunidade, desafio de origem, nível pretendido, rótulo, justificativa, situação, avaliador (Admin ou Mestre), motivo da recusa |
| `Invalidacao`        | registro, mestre, motivo, data e hora                                                                                                                |
| `Dispositivo`        | jogador dono, identificação, trilha em que foi construído, situação                                                                                  |

Imutabilidade: `RegistroDeColeta` é **somente inserção**. Valor, data da medição e coletor
nunca mudam depois de gravados; a situação (válido, invalidado, em auditoria) é o único campo
que evolui. `SerieDeColeta.estado` é derivado da última medição válida e da cadência, e é
recalculado, não editado à mão.

Estados da série: `ativa` → `interrompida` (dois períodos sem registro) → `ativa` (retomada) e
`encerrada` (fim da vigência do desafio).

## 9. Contratos de API

Rotas de consulta são **públicas e sem autenticação**; escrita é autenticada.

| Método | Rota                                    | Autenticação    | Descrição                                                 |
| ------ | --------------------------------------- | --------------- | --------------------------------------------------------- |
| GET    | `/comunidades`                          | pública         | Lista comunidades com indicadores agregados               |
| GET    | `/comunidades/{id}`                     | pública         | Comunidade, locais até rua e tipos de coleta ativos       |
| GET    | `/comunidades/{id}/series`              | pública         | Séries históricas agregadas, sem coletor                  |
| GET    | `/comunidades/{id}/exportacao`          | pública         | Exportação agregada e anonimizada por período             |
| POST   | `/comunidades/{id}/locais`              | Admin           | Cadastra local na hierarquia da comunidade                |
| POST   | `/solicitacoes-de-local`                | Jogador         | Solicita a inclusão de local ausente                      |
| GET    | `/solicitacoes-de-local/abertas`        | Mestre ou Admin | Solicitações em aberto que alimentam o alerta             |
| POST   | `/solicitacoes-de-local/{id}/avaliacao` | Mestre ou Admin | Aprova, criando o local, ou recusa com motivo             |
| POST   | `/comunidades`                          | Admin           | Cria comunidade vazia                                     |
| PATCH  | `/comunidades/{id}/default`             | Admin           | Marca a comunidade default do onboarding                  |
| POST   | `/jogadores/{id}/transferencia`         | Admin           | Transfere jogador de comunidade, preservando o histórico  |
| POST   | `/desafios-de-coleta`                   | Mestre          | Cria desafio de coleta vinculado a um ponto de trilha     |
| POST   | `/series`                               | Jogador         | Abre série individual para um desafio e um local          |
| GET    | `/series/minhas`                        | Jogador         | Séries do jogador, estado e pontos que rendem             |
| POST   | `/series/{id}/registros`                | Jogador         | Grava medição; aceita lote da fila offline                |
| POST   | `/series/{id}/registros`                | Dispositivo     | Mesma rota, credencial de dispositivo — ver pendência §14 |
| GET    | `/auditoria/amostra`                    | Mestre          | Amostra de registros a auditar, priorizando fora de faixa |
| POST   | `/registros/{id}/invalidacao`           | Mestre          | Invalida registro com motivo e estorna os pontos          |

Erros previstos: série aberta fora da comunidade do jogador (403); registro fora da vigência
do desafio (422); registro além da quantidade que pontua no período (201 com `pontuou: false`);
invalidação por Mestre que não é autor do desafio (403).

## 10. Requisitos não funcionais

- Registro por celular modesto, em Web App responsivo Mobile First.
- Operação com rede instável: fila local e sincronização posterior, preservando a hora da
  medição — requisito que vale igualmente para o App 05 e o App 02.
- Uso em aparelho compartilhado do ponto de apoio: a série é do jogador autenticado na sessão,
  nunca do aparelho.
- Envio de foto ou vídeo tolera rede instável: upload retomável, com o registro pendente
  visível ao jogador até concluir.
- Consulta pública de série histórica responde sem autenticação e é cacheável.
- Linguagem simples em toda mensagem ao jogador, incluindo o aviso de série prestes a
  interromper.
- Código aberto, em pt-BR.

## 11. LGPD e proteção da criança

| Dado coletado                  | Finalidade                                | Base legal        | Retenção   | Quem acessa                            |
| ------------------------------ | ----------------------------------------- | ----------------- | ---------- | -------------------------------------- |
| Valor medido e data da medição | Construir a série do território           | interesse público | permanente | público, agregado                      |
| Local até rua                  | Situar a medição                          | interesse público | permanente | público, agregado                      |
| Local abaixo de rua            | Precisão interna da série                 | interesse público | permanente | gestão e Mestre da trilha              |
| Identificação do coletor       | Procedência da série e crédito ao jogador | a definir (§14)   | permanente | gestão, Mestre, o próprio, responsável |
| Foto ou vídeo do território    | Registro visual do território             | consentimento     | permanente | público, após auditoria                |

- O vínculo coletor ↔ registro **não é anonimizado no armazenamento**; a anonimização ocorre
  na saída.
- Pedido de exclusão do responsável **não apaga** o registro do território. A tela e o termo
  precisam dizer isso antes do aceite — requisito detalhado no PRD-13.
- A aplicação que registra a coleta indica, de forma discreta e permanente, o que está sendo
  coletado e para onde vai.
- A coleta não capta dado pessoal da criança além da autoria do registro: a foto do território
  é de lugar, nunca de pessoa.

## 12. Critérios de aceite e métricas

Critérios de aceite, um por requisito essencial, verificáveis por quem não escreveu o PRD:

- Comunidade recém-criada aparece na API sem nenhum local, série ou jogador.
- Jogador cadastrado no onboarding aparece vinculado à comunidade default, sem tê-la informado.
- Registro válido credita ao Poder do Território exatamente o valor do documento 11 §5; o
  segundo registro do mesmo período credita zero quando o desafio declara que só um pontua.
- Série sem registro por dois períodos de cadência aparece como `interrompida` e para de
  creditar; o registro seguinte a devolve para `ativa`.
- Invalidação de um registro reduz o saldo do jogador no valor exato creditado, e o registro
  continua consultável, marcado como inválido.
- Registro feito sem rede e sincronizado uma hora depois grava a hora da medição, não a do
  envio.
- Solicitação de local aprovada pelo Mestre da trilha cria o local e libera a abertura da
  série; recusada, devolve o motivo ao jogador.
- Registro em foto ou vídeo, sem valor numérico, é aceito e credita pontos como qualquer
  outro registro válido do mesmo desafio.
- Consulta pública de uma série não devolve nick, nome, avatar nem local abaixo de rua.

Este PRD não sustenta diretamente nenhuma das hipóteses H1 a H4 do Ciclo 01, que tratam de
adesão, autorização, lastro e faixa etária. Os indicadores que ele passa a produzir —
séries abertas, séries ativas ao fim do ciclo, registros válidos e taxa de continuidade — são
a base da avaliação do Poder do Território e entram no conjunto de indicadores de impacto.

## 13. Decisões tomadas neste PRD

| Decisão                                                               | Gravada em | Doc 09       |
| --------------------------------------------------------------------- | ---------- | ------------ |
| Valor único por registro válido, igual para todo tipo de coleta       | 11 §5      | Já decididos |
| Sem teto de pontos por período                                        | 11 §5      | Já decididos |
| Quantos registros do período pontuam é declarado no desafio           | 11 §5      | Já decididos |
| Dois períodos de cadência seguidos sem registro interrompem a série   | 02 §1      | Já decididos |
| Registro nasce válido; Mestre audita por amostragem e pode invalidar  | 02 §1      | Já decididos |
| Série individual, uma por jogador                                     | 02 §1      | Já decididos |
| Origem do registro: manual, por voz ou sensor construído pelo jogador | 02 §1      | Já decididos |
| Saída pública agregada até o nível da rua                             | 02 §1      | Já decididos |

## 14. Pendências que permanecem

- **Autenticação do sensor do jogador**: como o dispositivo se credencia na API, o que fazer
  com valor fora de faixa vindo de sensor e quem responde por sensor descalibrado. Trava a
  implementação do `RF-08-14`, não a modelagem.
- **Inferência de endereço pela série de rua**: falta a mitigação para rua com um único
  coletor, em que a série diária indica a casa da criança.
- **Base legal da guarda permanente e nominal** de dado produzido por criança, e o que
  exatamente se responde a um pedido de exclusão. Trava o termo da App 07, não este domínio.
- **Faixas de pontos dos níveis 1 a 5**, inclusive do Poder do Território: o documento 11 §6
  define os critérios em palavras, sem números.
- **Tecnologia de armazenamento das séries temporais**: decisão de arquitetura do PRD-01.

## 15. Rastreabilidade

| Requisito               | Origem                                        |
| ----------------------- | --------------------------------------------- |
| `RF-08-01` a `RF-08-04` | 02 §1 (Comunidades Virtuais)                  |
| `RF-08-05` a `RF-08-08` | 02 §1 (registro temporal), 11 §4              |
| `RF-08-09` a `RF-08-11` | 11 §5 (motor de pontuação)                    |
| `RF-08-12` e `RF-08-13` | 02 §1 (veracidade do dado)                    |
| `RF-08-14` e `RF-08-15` | 02 §1 (origem do registro), 03 §1             |
| `RF-08-16` e `RF-08-19` | 02 §1 (anonimização na saída), 03 §12         |
| `RF-08-17` e `RF-08-18` | 08 (PRD-05 e PRD-13)                          |
| `RF-08-20`              | 11 §8.3                                       |
| `RF-08-21`              | 02 §1 (registro por foto ou vídeo)            |
| `RF-08-22` a `RF-08-24` | 02 §1 (solicitação de novo local), 03 §§5, 11 |
