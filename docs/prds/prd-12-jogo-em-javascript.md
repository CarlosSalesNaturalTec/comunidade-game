# PRD-12 — App 04: Jogo em JavaScript

## 1. Identificação

| Campo            | Valor                                               |
| ---------------- | --------------------------------------------------- |
| PRD              | PRD-12                                              |
| Aplicação        | App 04 — Jogo em JavaScript                         |
| Onda             | 5                                                   |
| Situação         | em revisão                                          |
| Versão e data    | v1 — 2026-08-08                                     |
| Depende de       | PRD-01, PRD-03                                      |
| Documentos-fonte | 02 §§1, 2, 4; 03 §§6, 8, 9, 12; 04 §§1, 2; 11 §§5–8 |

## 2. Contexto e objetivo

O App 04 é a recompensa lúdica do que se conquistou na vida real. O Guerreiro(a) que sustentou
uma série de coleta por três meses, desbloqueou missões e chegou à culminância vê esse esforço
virar um personagem mais forte numa arena — e vê isso em público, num jogo que qualquer pessoa
do bairro abre no celular sem se cadastrar.

Este PRD define esse jogo: como o catálogo de personagens jogáveis nasce da mesma lista de
divulgação autorizada da vitrine, como cada virtude do Guerreiro(a) vira atributo da partida,
como o duelo funciona sem rede e em dupla no mesmo aparelho, e — sobretudo — como o contrato
de **somente leitura** é sustentado por construção: não existe rota de escrita para o jogo,
então não há o que automatizar nem o que fraudar.

No Ciclo 01, entregue esta aplicação, a turma da Guerreira Zeferina tem um jogo em que os
personagens são os próprios colegas, com o código aberto que a trilha do Poder da IA e
Robótica ensina a alterar — o Guerreiro(a) deixa de ser só jogador e passa a ser um dos
construtores do jogo.

## 3. Escopo

### 3.1 Dentro do escopo

- **Catálogo público de personagens jogáveis**, sem login, formado exclusivamente pelos
  Guerreiros e Guerreiras com divulgação autorizada vigente.
- **Tela de escolha do personagem** com a ficha das virtudes conquistadas e dos atributos que
  elas produzem na partida.
- **Duelo por turnos** contra adversário conduzido pelo computador, dimensionado pelo
  personagem escolhido.
- **Duelo local**, dois jogadores no mesmo aparelho, para uso nas aulas presenciais.
- **Composição do personagem pelo mapa fixo** de virtude em atributo do documento 11.
- **Funcionamento offline**: catálogo guardado no aparelho, partida sem rede e revalidação a
  cada reconexão.
- **Instalação como aplicação do navegador** (PWA), sem loja e sem instalador.
- **Código aberto e legível**, com o balanceamento em arquivo próprio, apto a virar conteúdo
  de trilha.
- **Aviso permanente** de que nada da partida volta para a plataforma.

### 3.2 Fora do escopo

- **Multiplayer em rede** — exigiria servidor de partida e pareamento, fora do Ciclo 01.
- **Conta de jogador, placar persistente e ranking do jogo** — o ranking mede realização na
  vida real, não partida.
- **Qualquer escrita na plataforma** — é o contrato do jogo, não uma limitação de onda.
- **Mestre, Apoiador e Comunidade Virtual como personagens jogáveis** — ficam para ciclo
  futuro; no Ciclo 01 só o Guerreiro(a) é personagem.
- **Loja, moeda, item comprável ou anúncio** — o jogo não tem economia própria.
- **Áudio ou imagem real de criança** — a representação é sempre por avatar.
- **Torneio, temporada e evento com premiação** — dependem de escrita e de calendário próprio.

## 4. Personas e permissões

| Persona                         | O que faz nesta aplicação                                                                        | O que não pode fazer                                                                |
| ------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| **Visitante** (qualquer pessoa) | Abre o jogo sem se identificar, escolhe personagem, duela                                        | Cadastrar-se, alterar qualquer coisa na plataforma, ver dado pessoal de criança     |
| **Guerreiro(a) autorizado**     | É personagem jogável do catálogo, com as virtudes que conquistou                                 | Escolher entrar ou sair do catálogo — quem autoriza é o responsável, na App 07      |
| **Guerreiro(a) construtor**     | Altera o código do jogo como atividade de trilha                                                 | Alterar o contrato de leitura, criar escrita ou mudar o mapa de virtude em atributo |
| **Mestre**                      | Usa o jogo na aula, inclusive no duelo local em dupla                                            | Creditar ponto pelo resultado de partida — o crédito é de atividade validada        |
| **Responsável**                 | Não usa o jogo; a autorização que ele dá na App 07 é o que põe e tira o Guerreiro(a) do catálogo | Escolher em qual aplicação a autorização vale: ela é única e vale em todas          |
| **Admin / gestão**              | Não opera o jogo                                                                                 | Configurar personagem, forçar entrada no catálogo ou ajustar atributo de alguém     |

## 5. Jornadas principais

### 5.1 Visitante escolhe um personagem e duela

1. Alguém abre o endereço do jogo pelo celular, vindo da vitrine ou de um link compartilhado.
2. O jogo carrega o **catálogo de personagens** — os Guerreiros e Guerreiras com divulgação
   autorizada — e mostra os cards, com avatar e nick.
3. O visitante abre um card e vê a **ficha do personagem**: quais poderes e badges ele
   conquistou, em que nível está, os dois saldos de pontos e **qual atributo cada virtude
   produziu** na partida.
4. Escolhido o personagem, começa o duelo contra um adversário conduzido pelo computador,
   dimensionado pelo personagem escolhido.
5. A partida corre em turnos alternados: atacar, usar habilidade (consumindo energia) ou
   defender.
6. Vitória ou derrota, a tela final mostra o resumo e diz, com todas as letras, que **nada
   disso alterou o perfil do Guerreiro(a)** — nem ponto, nem nível, nem histórico.
7. O visitante joga de novo, troca de personagem ou vai para a vitrine ver a página completa
   daquele Guerreiro(a).

**Exceção — rede fora no primeiro acesso.** Sem catálogo guardado no aparelho e sem rede, o
jogo explica que precisa de conexão uma primeira vez para conhecer os personagens, e não abre
partida com lista inventada.

### 5.2 Duelo local na aula presencial

1. O Mestre abre o jogo no aparelho da aula e escolhe o **duelo local**.
2. Cada um dos dois jogadores escolhe seu personagem no mesmo catálogo; personagens distintos.
3. O duelo corre em turnos alternados no mesmo aparelho, passando o celular de mão em mão.
4. Os atributos **não são igualados**: quem escolheu o personagem mais evoluído começa mais
   forte, e a tela mostra a diferença antes de começar — é o ponto do jogo, não um defeito.
5. Termina a partida, nada é enviado, nada é creditado. O Mestre lança pontos, quando for o
   caso, pela **atividade** que a aula previu — nunca pelo resultado do duelo.

**Exceção — só um personagem autorizado no catálogo.** O duelo local exige dois personagens
distintos; havendo apenas um, a opção fica indisponível, com a explicação em uma linha.

### 5.3 Partida com a rede fora

1. O aparelho já abriu o jogo alguma vez e tem o catálogo guardado.
2. A rede cai — ou nunca esteve disponível naquele ponto de apoio.
3. O jogo abre normalmente, avisa que está usando a **lista guardada** e **de quando ela é**, e
   deixa jogar.
4. Voltando a rede, o jogo **revalida o catálogo antes de abrir a próxima partida**: se mudou,
   baixa a lista nova; se um personagem saiu, ele desaparece da escolha.
5. A partida em andamento no momento da reconexão não é interrompida.

### 5.4 Autorização revogada durante o uso

1. O responsável revoga a autorização de divulgação na App 07.
2. Na leitura seguinte do catálogo, aquele Guerreiro(a) **não está mais lá** — nem como card,
   nem como resultado de busca por nick.
3. Um endereço direto para a ficha dele responde "não encontrado", igual ao de um nick que
   nunca existiu.
4. No aparelho que estava offline, o personagem sai assim que o catálogo é revalidado; até lá,
   a defasagem é a do catálogo guardado, e a tela sempre diz de quando ele é.
5. Nada do que aconteceu em partida precisa ser desfeito — o jogo nunca gravou nada.

### 5.5 Catálogo sem nenhum personagem autorizado

1. No começo do ciclo, ou numa comunidade em que nenhum responsável autorizou ainda, o
   catálogo volta vazio.
2. O jogo não inventa personagem, não usa exemplo fictício e não mostra criança sem
   autorização.
3. A tela explica em linguagem simples que os personagens aparecem quando as famílias
   autorizam, e oferece o caminho para a vitrine.

### 5.6 Guerreiro(a) altera o jogo como atividade de trilha

1. Uma missão da trilha do Poder da IA e Robótica propõe alterar o jogo — mudar o
   balanceamento, criar uma habilidade nova, corrigir um comportamento.
2. O Guerreiro(a) trabalha sobre o **código aberto**, com o arquivo de balanceamento separado
   e documentado.
3. A entrega é a produção da missão, avaliada pelo Mestre como qualquer outra atividade.
4. O que entra no jogo oficial passa pelo fluxo de contribuição do projeto.
5. **O crédito de pontos é da atividade validada pelo Mestre**, nunca do jogo.

## 6. Requisitos funcionais

### 6.1 Catálogo e escolha do personagem

| ID         | Requisito                                                                                            | Prioridade |
| ---------- | ---------------------------------------------------------------------------------------------------- | ---------- |
| `RF-12-01` | Carregar e exibir o catálogo de personagens sem exigir login, cadastro ou identificação do visitante | essencial  |
| `RF-12-02` | Compor o catálogo exclusivamente com Guerreiros e Guerreiras de divulgação autorizada vigente        | essencial  |
| `RF-12-03` | Exibir na ficha do personagem avatar, nick, poderes com níveis, badges e os dois saldos de pontos    | essencial  |
| `RF-12-04` | Filtrar o catálogo por nick dentro da lista já carregada, sem consultar nick que não esteja nela     | desejável  |
| `RF-12-05` | Mostrar, para cada atributo do personagem, de qual virtude ele veio                                  | essencial  |
| `RF-12-06` | Exibir o catálogo idêntico para todo visitante, sem personalização de nenhuma natureza               | essencial  |

### 6.2 Composição do personagem

| ID         | Requisito                                                                                      | Prioridade |
| ---------- | ---------------------------------------------------------------------------------------------- | ---------- |
| `RF-12-07` | Converter as virtudes em atributos pelo mapa fixo do documento 11, sem deixar virtude de fora  | essencial  |
| `RF-12-08` | Garantir monotonia: progresso maior nunca produz atributo menor                                | essencial  |
| `RF-12-09` | Dimensionar o adversário do computador pelo personagem escolhido, mantendo a partida disputada | essencial  |
| `RF-12-10` | Manter os números do balanceamento em arquivo próprio, versionado e documentado                | essencial  |

### 6.3 Partida

| ID         | Requisito                                                                                       | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------------- | ---------- |
| `RF-12-11` | Executar o duelo em turnos alternados, com as ações atacar, usar habilidade e defender          | essencial  |
| `RF-12-12` | Cobrar energia pelo uso de habilidade e impedir o uso quando a energia acabar                   | essencial  |
| `RF-12-13` | Encerrar a partida em vitória ou derrota, com resumo do que aconteceu                           | essencial  |
| `RF-12-14` | Declarar na tela final que o resultado não alterou nada no perfil do Guerreiro(a)               | essencial  |
| `RF-12-15` | Permitir abandonar a partida a qualquer momento, sem consequência e sem confirmação burocrática | desejável  |

### 6.4 Duelo local em dupla

| ID         | Requisito                                                                                         | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------------- | ---------- |
| `RF-12-16` | Permitir que dois jogadores escolham personagens distintos e duelem no mesmo aparelho, em turnos  | essencial  |
| `RF-12-17` | Exibir a diferença de atributos entre os dois personagens antes de começar o duelo local          | essencial  |
| `RF-12-18` | Operar o duelo local sem servidor, sem pareamento e sem rede                                      | essencial  |
| `RF-12-19` | Indisponibilizar o duelo local, com explicação, quando o catálogo tiver menos de dois personagens | essencial  |

### 6.5 Funcionamento sem rede

| ID         | Requisito                                                                                                         | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------------------------------- | ---------- |
| `RF-12-20` | Guardar o catálogo no aparelho e abrir partida com ele quando não houver rede                                     | essencial  |
| `RF-12-21` | Revalidar o catálogo a cada reconexão, antes de abrir a próxima partida                                           | essencial  |
| `RF-12-22` | Ler sempre da API quando houver rede; o catálogo guardado só serve na falta dela                                  | essencial  |
| `RF-12-23` | Informar na tela quando o catálogo em uso é o guardado, e de quando ele é                                         | essencial  |
| `RF-12-24` | Explicar, no primeiro acesso sem rede e sem catálogo, que é preciso conectar uma vez para conhecer os personagens | essencial  |
| `RF-12-25` | Permitir a instalação como aplicação do navegador, sem loja e sem instalador                                      | desejável  |

### 6.6 Código aberto e uso em trilha

| ID         | Requisito                                                                                          | Prioridade |
| ---------- | -------------------------------------------------------------------------------------------------- | ---------- |
| `RF-12-26` | Publicar o código aberto e legível, com instruções de como rodar e alterar o jogo                  | essencial  |
| `RF-12-27` | Rodar sem depender de serviço proprietário, para que a alteração feita em trilha funcione          | essencial  |
| `RF-12-28` | Isolar em arquivos próprios o que a trilha altera com mais frequência: balanceamento e habilidades | desejável  |

### 6.7 Transparência com o visitante

| ID         | Requisito                                                                    | Prioridade |
| ---------- | ---------------------------------------------------------------------------- | ---------- |
| `RF-12-29` | Manter visível o aviso de que o jogo lê a plataforma e não escreve nada nela | essencial  |
| `RF-12-30` | Informar o que o jogo guarda no aparelho e oferecer a opção de apagar isso   | essencial  |
| `RF-12-31` | Oferecer caminho para a vitrine e para o "Entrar" da plataforma              | desejável  |

## 7. Regras de negócio

| ID         | Regra                                                                                           | Invariante (doc 99 §6) | Fonte   |
| ---------- | ----------------------------------------------------------------------------------------------- | ---------------------- | ------- |
| `RN-12-01` | O jogo é público, sem login, e não escreve nada na plataforma                                   | 8                      | 11 §8.4 |
| `RN-12-02` | Não existe rota de escrita para o jogo; a tentativa devolve 404                                 | 8                      | 11 §8.4 |
| `RN-12-03` | Resultado de partida não credita, não debita e não registra histórico                           | 8                      | 03 §6   |
| `RN-12-04` | Não há saldo de pontos consumidos: ponto não se gasta em partida                                | 8                      | 11 §5   |
| `RN-12-05` | Só é personagem quem tem divulgação autorizada vigente do responsável                           | 8, 12                  | 03 §12  |
| `RN-12-06` | O catálogo é idêntico para todo visitante — sem login, o jogo não distingue quem joga           | 8                      | 03 §6   |
| `RN-12-07` | O Guerreiro(a) aparece só por avatar e nick, nunca por imagem real ou nome civil                | 12                     | 03 §12  |
| `RN-12-08` | A revogação vale para frente e tira o personagem do catálogo na leitura seguinte                | 12                     | 03 §9   |
| `RN-12-09` | Ficha inexistente e ficha sem autorização recebem a mesma resposta "não encontrado"             | 12                     | 03 §8   |
| `RN-12-10` | O mapa de virtude em atributo é fixo e nenhuma virtude fica de fora                             | 8                      | 11 §8.4 |
| `RN-12-11` | Evoluir na vida real nunca produz personagem pior em atributo nenhum                            | 8                      | 11 §8.4 |
| `RN-12-12` | O balanceamento é conteúdo do jogo, alterável em trilha, não regra de plataforma                | —                      | 11 §8.4 |
| `RN-12-13` | Jogar muito não altera ranking, nível ou badge de ninguém                                       | 8                      | 11 §8.4 |
| `RN-12-14` | O catálogo guardado só é usado sem rede e é revalidado a cada reconexão                         | —                      | 03 §6   |
| `RN-12-15` | O jogo guarda no aparelho apenas o catálogo e as preferências do próprio jogo, e não envia nada | —                      | 03 §6   |
| `RN-12-16` | O duelo local não iguala atributos: a diferença de evolução é intencional e visível             | 8                      | 03 §6   |
| `RN-12-17` | Não há canal de contato entre visitante e Guerreiro(a) ou família                               | 10                     | 02 §1   |
| `RN-12-18` | O jogo não exibe dado de localização, escola, turma ou comunidade de um Guerreiro(a)            | 12                     | 03 §12  |
| `RN-12-19` | O jogo não veicula publicidade, patrocínio, rastreador ou cookie de terceiro                    | —                      | 04 §2   |
| `RN-12-20` | Não há compra, moeda nem item pago dentro do jogo                                               | 16                     | 04 §1   |
| `RN-12-21` | O código é aberto e alterá-lo é atividade de trilha, com crédito pela atividade validada        | 19                     | 11 §8.4 |
| `RN-12-22` | Só o Guerreiro(a) é personagem jogável no Ciclo 01                                              | 13                     | 03 §6   |

## 8. Modelo de dados

A aplicação **não cria entidade nenhuma** e **não escreve no domínio** — nem uma solicitação
pública, ao contrário da vitrine. Tudo o que ela usa é projeção de leitura, e o pouco que
persiste fica **no aparelho do visitante**, nunca no servidor.

```text
LÊ da API (definidos em outro PRD)        GUARDA no aparelho (nunca no servidor)
Guerreiro(a) / Avatar / Nick   (PRD-01)   CatalogoGuardado
Ponto — regular e extra        (PRD-01)   PreferenciasDoJogo
Nivel / Badge / Poder          (PRD-01)
Consentimento (estado vigente) (PRD-01)   DERIVA em memória, a cada partida
                                          Personagem  (virtudes → atributos)
ESCREVE                                   Adversario  (dimensionado pelo Personagem)
Nada. Em lugar nenhum.                    Partida     (existe só até a tela final)
```

| Estrutura            | Atributos essenciais                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------------------- |
| `CatalogoGuardado`   | lista de personagens jogáveis, carimbo de versão do catálogo, data e hora da revalidação                      |
| `PreferenciasDoJogo` | som, dificuldade e opção de duelo local — locais, sem identificador de visitante                              |
| `Personagem`         | nick, avatar, vitalidade, energia, escalonamento, habilidades e passivas, com a virtude de origem de cada uma |
| `Adversario`         | atributos derivados do `Personagem` escolhido, sem vínculo com Guerreiro(a) algum                             |
| `Partida`            | turno atual, vitalidade e energia correntes dos dois lados, resultado — descartada ao fim                     |

Derivações e imutabilidade:

- **Nada aqui é fonte de verdade.** O `Personagem` é projeção do progresso gravado pelo PRD-01
  e deixa de existir quando a partida termina.
- A **elegibilidade** de um Guerreiro(a) é derivada do estado vigente do `Consentimento` — a
  mesma derivação que a vitrine usa (PRD-03), e não uma lista própria do jogo.
- A `Partida` **não é persistida em lugar nenhum**, nem no aparelho: não há histórico, não há
  retomada de partida antiga e não há placar acumulado.
- O `CatalogoGuardado` é **descartável**: apagá-lo não perde nada, e o visitante pode apagá-lo
  pela própria tela do jogo.

## 9. Contratos de API

A aplicação segue as convenções do PRD-01 — prefixo `/v1`, erro em corpo único — e consome
**apenas rotas públicas de leitura, sem token**. Não consome nenhuma rota autenticada e não
existe, em rota alguma, um verbo de escrita destinado ao jogo.

| Método | Rota                          | Autenticação | Descrição                                                                   |
| ------ | ----------------------------- | ------------ | --------------------------------------------------------------------------- |
| GET    | `/v1/jogo/personagens`        | pública      | Catálogo jogável: avatar, nick, poderes com níveis, badges e os dois saldos |
| GET    | `/v1/jogo/personagens/{nick}` | pública      | Ficha de um personagem, por nick exato                                      |
| GET    | `/v1/jogo/catalogo/versao`    | pública      | Carimbo de versão do catálogo, para revalidar sem baixar a lista            |

O catálogo é **o mesmo conjunto** que a vitrine expõe em `/v1/vitrine/guerreiros` (PRD-03),
com um recorte diferente de campos: o jogo precisa dos dois saldos de pontos e não precisa de
criações originais nem de portfólio. A elegibilidade é a mesma derivação de consentimento, e
não uma segunda lista a manter em dia.

Erros previstos:

- Nick inexistente ou sem autorização vigente: **404 idêntico nos dois casos**, sem revelar
  qual ocorreu.
- Excesso de consultas da mesma origem: 429, com o tempo de espera em linguagem simples.
- Qualquer verbo de escrita em qualquer rota do jogo: **404** — a rota não existe, e a resposta
  não sugere que exista em outro caminho.
- Catálogo indisponível: 503, tratado no cliente pela leitura do catálogo guardado.

## 10. Requisitos não funcionais

- **Web App responsivo Mobile First**, jogável em retrato, com alvos de toque grandes o
  bastante para dedo de criança em tela pequena.
- **Celular modesto**: o pacote inicial precisa ser pequeno e a partida rodar sem travar em
  aparelho antigo, que é o que existe no ponto de apoio.
- **Rede instável e ausência de rede**: o jogo abre e joga com o catálogo guardado, e a queda
  de conexão no meio da partida não a interrompe.
- **Aparelho compartilhado**: o jogo não guarda nada que identifique quem jogou antes; quem
  pega o celular em seguida encontra a mesma tela inicial.
- **Sem dependência de serviço proprietário** em tempo de execução — é condição para que a
  alteração feita em trilha funcione no aparelho do Guerreiro(a).
- **Acessibilidade e linguagem simples**: contraste alto, textos curtos, nenhuma instrução que
  dependa de saber jargão de jogo.
- **Idioma pt-BR** em toda a interface e nos nomes de domínio do código do jogo.
- **Código aberto**, com licença conforme a decisão de licenciamento do projeto, ainda
  pendente.

## 11. LGPD e proteção da criança

| Dado coletado                              | Finalidade                        | Base legal                    | Retenção                                         | Quem acessa        |
| ------------------------------------------ | --------------------------------- | ----------------------------- | ------------------------------------------------ | ------------------ |
| Nenhum dado do visitante                   | —                                 | —                             | —                                                | —                  |
| Avatar e nick do Guerreiro(a)              | Compor o personagem jogável       | Consentimento do responsável  | Enquanto a autorização vigorar                   | Qualquer visitante |
| Virtudes (pontos, poderes, níveis, badges) | Converter em atributos da partida | Consentimento do responsável  | Enquanto a autorização vigorar                   | Qualquer visitante |
| Catálogo guardado no aparelho              | Permitir a partida sem rede       | Execução da própria aplicação | Até a revalidação ou o apagamento pelo visitante | Só o aparelho      |

Complementos exigidos pelo modelo:

- **Consentimento.** O jogo **não coleta consentimento nenhum** — nem do visitante, nem da
  criança. A autorização que coloca um Guerreiro(a) no catálogo é a **autorização única de
  divulgação**, concedida e revogada pelo responsável na App 07 (PRD-13), e registrada lá.
- **Alternativa equivalente.** Quem não autoriza simplesmente **não vira personagem**, e não
  perde nada por isso: o jogo não é atividade de trilha, não pontua e não entra em avaliação.
  A recusa não exclui ninguém de atividade alguma.
- **Aviso visível.** Toda tela informa que o jogo **lê a plataforma e não escreve nela**, que
  não há cadastro e que os personagens são Guerreiros e Guerreiras cujas famílias autorizaram
  a divulgação. A tela também diz o que fica guardado no aparelho.
- **Acesso, correção e exclusão.** O jogo não é o canal desses pedidos — não tem formulário e
  não abre protocolo. O aviso encaminha à App 07, onde o pedido tem protocolo, prazo e
  resposta. O que o jogo oferece por conta própria é **apagar o que ele guardou no aparelho**.
- **Nada de contato.** Não há mensagem, comentário, compartilhamento com identificação, nem
  qualquer caminho de um visitante até um Guerreiro(a) ou sua família.

## 12. Critérios de aceite e métricas

Critérios verificáveis, um por requisito essencial:

- O jogo abre e chega à escolha de personagem **sem nenhuma tela de login ou cadastro**
  (`RF-12-01`).
- Um Guerreiro(a) sem autorização vigente **não aparece** no catálogo, nem pela busca por nick,
  e o endereço direto da ficha dele responde 404 (`RF-12-02`, `RN-12-05`, `RN-12-09`).
- A ficha do personagem exibe avatar, nick, poderes com níveis, badges e os dois saldos, e
  indica **de qual virtude veio cada atributo** (`RF-12-03`, `RF-12-05`).
- Dois visitantes diferentes, em aparelhos diferentes, veem **o mesmo catálogo** (`RF-12-06`).
- Um personagem com mais pontos, mais poderes ou nível maior tem atributos **maiores ou iguais**
  aos de um personagem com menos — nunca menores (`RF-12-08`).
- O adversário do computador acompanha o personagem escolhido: a partida não termina em um
  turno nem se arrasta sem fim, seja qual for o personagem (`RF-12-09`).
- Habilidade sem energia suficiente **não executa**, e a interface diz por quê (`RF-12-12`).
- A tela final declara explicitamente que **nada foi alterado no perfil**, e uma consulta ao
  progresso do Guerreiro(a) antes e depois de dez partidas devolve **exatamente o mesmo**
  (`RF-12-14`, `RN-12-03`, `RN-12-13`).
- Qualquer tentativa de `POST`, `PUT`, `PATCH` ou `DELETE` nas rotas do jogo devolve **404**
  (`RN-12-02`).
- No duelo local, dois personagens distintos duelam no mesmo aparelho **com o modo avião
  ligado** (`RF-12-16`, `RF-12-18`).
- Com um único personagem no catálogo, o duelo local aparece **indisponível com explicação**,
  e não quebrado (`RF-12-19`).
- Com o modo avião ligado depois de um primeiro acesso, o jogo abre, avisa que a lista é a
  guardada, diz de quando ela é e **deixa jogar** (`RF-12-20`, `RF-12-23`).
- Revogada uma autorização enquanto o aparelho estava offline, o personagem **desaparece na
  primeira revalidação após a reconexão** (`RF-12-21`, `RN-12-08`, `RN-12-14`).
- No primeiro acesso sem rede e sem catálogo, o jogo **explica e não abre partida** com lista
  inventada (`RF-12-24`).
- O repositório roda com as instruções publicadas, **sem chave de serviço proprietário**, e o
  balanceamento está em arquivo próprio e documentado (`RF-12-10`, `RF-12-26`, `RF-12-27`).
- A tela informa o que o jogo guardou no aparelho e a opção de apagar **funciona**, deixando o
  jogo no estado de primeiro acesso (`RF-12-30`).
- Uma varredura da aplicação não encontra cookie de terceiro, rastreador, anúncio nem chamada
  a domínio que não seja o da própria API (`RN-12-19`).

**Hipótese do Ciclo 01.** Este PRD **não sustenta hipótese nenhuma** do documento 10 e não
passa a medir nada — pela mesma razão que o torna seguro: o jogo não registra partida, não
guarda identificador de visitante e não produz série. O interesse que ele desperta só aparece
onde vira cadastro, e a **H1** é medida no App 01 (PRD-04), nunca aqui.

## 13. Decisões tomadas neste PRD

| Decisão                                                                        | Gravada em         | Linha do doc 09                          |
| ------------------------------------------------------------------------------ | ------------------ | ---------------------------------------- |
| Gênero e mecânica: arena de duelo por turnos contra adversário do computador   | doc 03 §6 e doc 08 | Mecânica do jogo (App 04) — Já decididos |
| Engine **Phaser.js** confirmada, de sugestão para definição vigente            | doc 03 §6 e doc 08 | Mecânica do jogo (App 04) — Já decididos |
| Mapa fixo de virtude em atributo, com monotonia e transparência                | doc 11 §8.4        | Mecânica do jogo (App 04) — Já decididos |
| Balanceamento é conteúdo do jogo, alterável em trilha, não regra de plataforma | doc 11 §8.4        | Mecânica do jogo (App 04) — Já decididos |
| O jogo funciona offline, com catálogo guardado e revalidação a cada reconexão  | doc 03 §6 e doc 08 | Mecânica do jogo (App 04) — Já decididos |
| Duelo local com dois jogadores no mesmo aparelho, sem igualar atributos        | doc 03 §6 e doc 08 | Mecânica do jogo (App 04) — Já decididos |
| No Ciclo 01, só o Guerreiro(a) é personagem jogável                            | doc 03 §6          | Mecânica do jogo (App 04) — Já decididos |

## 14. Pendências que permanecem

| Pendência                              | O que trava                                                                                                                                           | Quando precisa de resposta                            |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Validade do catálogo offline**       | O prazo máximo em que o catálogo guardado ainda serve sem nenhuma reconexão, e o que a tela mostra ao vencer — é o teto da defasagem de uma revogação | Antes de implementar `RF-12-20`                       |
| **Acesso das aplicações de terceiros** | Se aplicação de terceiro se identifica por chave para consumir a mesma leitura pública, quem a emite e o que acontece na revogação                    | Só quando houver jogo de terceiro; não trava o App 04 |
| **Licenças do código**                 | A licença sob a qual o jogo é publicado, e portanto sob a qual a alteração feita em trilha é redistribuída                                            | Antes da primeira publicação do repositório           |

As três já constam da tabela de decisões pendentes do documento 09.

## 15. Rastreabilidade

| Requisito                           | Origem                                                           |
| ----------------------------------- | ---------------------------------------------------------------- |
| `RF-12-01`, `RF-12-06`              | 03 §6 (jogo público, sem login, lista idêntica)                  |
| `RF-12-02`                          | 03 §§6, 12 e 11 §8.4 (divulgação autorizada)                     |
| `RF-12-03`, `RF-12-05`              | 11 §§8.2, 8.4 (composição do card e transparência do mapa)       |
| `RF-12-04`                          | 03 §8 (consulta por nick exato)                                  |
| `RF-12-07`, `RF-12-08`, `RF-12-10`  | 11 §8.4 (mapa de virtude em atributo)                            |
| `RF-12-09`                          | 03 §6 (adversário dimensionado pelo personagem)                  |
| `RF-12-11` a `RF-12-13`             | 03 §6 (arena de duelo por turnos)                                |
| `RF-12-14`                          | 11 §8.4 e 03 §6 (a partida não volta para a plataforma)          |
| `RF-12-15`                          | 03 §6 (partida sem consequência)                                 |
| `RF-12-16` a `RF-12-19`             | 03 §6 (duelo local em dupla nas aulas presenciais)               |
| `RF-12-20` a `RF-12-25`             | 03 §6 (catálogo guardado, revalidação e Mobile First)            |
| `RF-12-26` a `RF-12-28`             | 11 §8.4 e 02 §2 (código aberto, alterá-lo é atividade de trilha) |
| `RF-12-29`, `RF-12-30`              | 03 §12 (aviso do que se coleta e do que se guarda)               |
| `RF-12-31`                          | 03 §8 (vitrine e "Entrar")                                       |
| `RN-12-01` a `RN-12-04`, `RN-12-13` | 11 §§5, 8.4 (contrato dos jogos)                                 |
| `RN-12-05` a `RN-12-09`, `RN-12-18` | 03 §§9, 12 (autorização, revogação e exibição pública)           |
| `RN-12-10` a `RN-12-12`             | 11 §8.4 (mapa fixo, monotonia e balanceamento como conteúdo)     |
| `RN-12-14`, `RN-12-15`              | 03 §6 (funcionamento offline)                                    |
| `RN-12-16`                          | 03 §6 (duelo local não iguala atributos)                         |
| `RN-12-17`                          | 02 §1 (nenhum contato direto com Guerreiro(a) ou família)        |
| `RN-12-19`, `RN-12-20`              | 04 §§1, 2 (sem publicidade, sem economia própria no jogo)        |
| `RN-12-21`                          | 11 §8.4 e 02 §4 (crédito é da atividade validada)                |
| `RN-12-22`                          | 03 §6 e 99 §6 nº 13 (escopo do Ciclo 01)                         |
