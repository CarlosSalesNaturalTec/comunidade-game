## Purpose

A App 05 — a aplicação em que o Guerreiro(a) percorre a própria trilha, registra a coleta do
território e cuida do que conquistou. Nesta fatia, só a porta de entrada: a sessão no aparelho
compartilhado do ponto de apoio, que é a condição normal de uso e o pré-requisito de toda tela
do PRD-05.

## Requirements

### Requirement: O Guerreiro(a) entra na App 05 por nick e imagem

A aplicação SHALL abrir a sessão do Guerreiro(a) pedindo o **nick** e submetendo a **imagem**
à conferência biométrica do núcleo, em toda sessão. A prova de vivacidade e a extração do
descritor facial SHALL acontecer **no próprio aparelho**; ao núcleo SHALL ir apenas o
descritor, e a fotografia NEVER SHALL trafegar. (`RF-05-01`, `RN-05-01`, documento 03 §1.1)

#### Scenario: Entrada com nick e imagem conferidos

- **WHEN** um Guerreiro(a) com imagem gravada informa o nick e apresenta o rosto à câmera
- **THEN** a aplicação obtém o descritor no aparelho, o submete à conferência e abre a sessão

#### Scenario: A fotografia não sai do aparelho

- **WHEN** a aplicação submete a conferência ao núcleo
- **THEN** a chamada leva o descritor facial, e nenhuma imagem é enviada

#### Scenario: A recusa não diz o que falhou

- **WHEN** a conferência não encontra correspondência para o nick informado
- **THEN** a aplicação recusa a entrada sem revelar se o nick existe, e oferece o caminho da
  sessão assistida

### Requirement: O aparelho sem câmera recusa a entrada e explica o motivo

A aplicação SHALL recusar a entrada em aparelho sem câmera disponível e SHALL explicar a recusa
em **linguagem de criança de 6 anos**, sem termo técnico e sem código de erro exposto. A recusa
SHALL dizer o que a criança pode fazer — procurar um Mestre no ponto de apoio. (`RF-05-02`,
`RN-05-01`, PRD-05 §10)

#### Scenario: Aparelho sem câmera não entra

- **WHEN** a aplicação é aberta em aparelho sem câmera, ou com o acesso à câmera negado
- **THEN** a entrada é recusada, e a tela explica em linguagem simples o que aconteceu e o que
  fazer

#### Scenario: Nenhum código técnico chega à criança

- **WHEN** qualquer recusa de entrada é apresentada
- **THEN** a tela não exibe código de erro, nome de biblioteca nem termo técnico

### Requirement: Mestre ou Admin presente abre a sessão do Guerreiro(a)

A aplicação SHALL oferecer o caminho da **sessão assistida**, em que um Mestre ou um Admin
presente se autentica e abre a sessão do Guerreiro(a), nos dois casos previstos: quando a
conferência biométrica falha e quando o Guerreiro(a) **ainda não tem imagem gravada**. O adulto
que abre a sessão NEVER SHALL operar a aplicação em nome da criança. (`RF-05-03`, `RF-05-04`,
`RN-05-02`, PRD-05 §4)

#### Scenario: Conferência que falha abre pela sessão assistida

- **WHEN** a conferência biométrica de um Guerreiro(a) com imagem gravada não passa e um Mestre
  presente confirma a identidade dele
- **THEN** a sessão do Guerreiro(a) é aberta, e ele opera a aplicação normalmente

#### Scenario: Quem não tem imagem gravada entra pelo mesmo caminho

- **WHEN** um Guerreiro(a) que ainda não teve a imagem capturada no onboarding pede para entrar
  e um Admin presente confirma a identidade dele
- **THEN** a sessão é aberta, sem que nenhuma imagem seja capturada nesta aplicação

#### Scenario: Sem adulto presente não há sessão assistida

- **WHEN** a conferência falha e nenhum Mestre ou Admin se autentica
- **THEN** nenhuma sessão é aberta

### Requirement: A sessão encerra ao sair e por inatividade, com aviso antes

A aplicação SHALL encerrar a sessão quando o Guerreiro(a) sair e quando a sessão expirar por
inatividade, voltando em ambos os casos ao pedido de nick. **Um minuto antes** do encerramento
por inatividade a aplicação SHALL avisar, oferecendo a opção de continuar; escolhida a opção, a
contagem recomeça. A duração é a **declarada na implantação**, sem valor padrão no código.
(`RF-05-05`, `RF-05-71`, `RF-01-04`)

#### Scenario: Sair volta ao pedido de nick

- **WHEN** o Guerreiro(a) encerra a própria sessão
- **THEN** a aplicação volta ao pedido de nick, sem nenhum dado dele na tela

#### Scenario: O aviso precede o encerramento por inatividade

- **WHEN** falta um minuto para a sessão expirar por inatividade
- **THEN** a aplicação avisa e oferece a opção de continuar

#### Scenario: Continuar recomeça a contagem

- **WHEN** o Guerreiro(a) escolhe continuar diante do aviso
- **THEN** a sessão segue aberta e a contagem de inatividade recomeça

#### Scenario: Sem resposta ao aviso a sessão encerra

- **WHEN** o aviso é apresentado e o minuto passa sem resposta
- **THEN** a sessão encerra e a aplicação volta ao pedido de nick

### Requirement: O aparelho compartilhado não guarda nada de quem passou por ele

A aplicação NEVER SHALL armazenar imagem de Guerreiro(a) no aparelho compartilhado — nem a
fotografia da conferência, nem o descritor dela. Encerrada uma sessão, a tela seguinte NEVER
SHALL exibir dado do Guerreiro(a) anterior, e a troca de sessão entre duas crianças SHALL
acontecer **sem reiniciar a aplicação**. (`RF-05-06`, `RF-05-07`, PRD-05 §§10, 12)

#### Scenario: Nenhuma imagem fica no aparelho

- **WHEN** a conferência biométrica termina, tendo passado ou não
- **THEN** nenhuma imagem e nenhum descritor do Guerreiro(a) permanece armazenado no aparelho

#### Scenario: A tela seguinte não mostra a criança anterior

- **WHEN** uma sessão encerra e outro Guerreiro(a) informa o nick
- **THEN** nenhum dado do Guerreiro(a) anterior aparece em nenhuma tela

#### Scenario: Trocar de sessão não reinicia a aplicação

- **WHEN** dois Guerreiros e Guerreiras usam o mesmo aparelho, um após o outro
- **THEN** a troca acontece dentro da aplicação em execução, sem recarga nem reinício

### Requirement: A App 05 é inteiramente autenticada

A aplicação NEVER SHALL apresentar tela de conteúdo a visitante: toda tela além do pedido de
nick SHALL exigir sessão de Guerreiro(a) aberta. Uma sessão NEVER SHALL alcançar os dados de
outro Guerreiro(a). (`RF-05-01`, PRD-05 §4)

#### Scenario: Visitante não alcança tela nenhuma

- **WHEN** a aplicação é aberta sem sessão
- **THEN** a única tela apresentada é o pedido de nick

#### Scenario: A sessão alcança apenas os próprios dados

- **WHEN** a aplicação, com sessão aberta, consulta dados no núcleo
- **THEN** a resposta traz apenas dados do Guerreiro(a) daquela sessão

### Requirement: A App 05 mostra as séries do Guerreiro(a) e a próxima medição de cada uma

A aplicação SHALL listar ao Guerreiro(a) em sessão as **suas** séries de coleta, cada uma com o
que ela mede, o **local**, o **estado**, **quando é a próxima medição** e **quantos pontos ela
está rendendo**. A série **interrompida** SHALL ser sinalizada como tal, com o **histórico
preservado** e o **caminho de retomada** — registrar de novo —, e a tela SHALL dizer que os
pontos já ganhos **permanecem**. (`RF-05-30`, `RF-05-36`, `RN-05-10`, PRD-05 §5.4)

#### Scenario: A lista abre com o que medir e quando

- **WHEN** o Guerreiro(a) em sessão abre a área de coleta
- **THEN** vê as suas séries com o que cada uma mede, o local, o estado, a próxima medição e os
  pontos que está rendendo

#### Scenario: A série interrompida mostra como retomar

- **WHEN** uma das séries está interrompida
- **THEN** a tela a sinaliza, mantém o histórico visível, diz que os pontos ganhos permanecem e
  oferece o caminho de registrar de novo

#### Scenario: Nenhuma série de outra criança aparece

- **WHEN** o Guerreiro(a) abre a área de coleta
- **THEN** nenhuma série, registro ou dado de outro Guerreiro(a) é exibido

### Requirement: O Guerreiro(a) abre a série escolhendo o desafio e o local

A aplicação SHALL permitir ao Guerreiro(a) **abrir uma série** sobre um dos desafios de coleta
que ele pode assumir, escolhendo o **local** entre os **cadastrados pela gestão** — a aplicação
NEVER SHALL cadastrar local. A escolha SHALL oferecer apenas locais do **nível exigido** pelo
desafio, e a tela SHALL explicar em linguagem simples a recusa que o núcleo devolver.
(`RF-05-31`, `RN-05-11`, `RN-05-24`, PRD-05 §§3.2, 5.4)

#### Scenario: Abertura de série sobre desafio elegível

- **WHEN** o Guerreiro(a) escolhe um desafio que pode assumir e um local do nível exigido
- **THEN** a série é aberta e passa a aparecer na lista das suas séries

#### Scenario: A aplicação não oferece desafio que o núcleo recusaria

- **WHEN** um desafio está fora da vigência, exige granularidade acima do teto da comunidade ou
  já tem série do Guerreiro(a) naquele local
- **THEN** ele não é oferecido como abertura disponível

#### Scenario: A recusa da abertura é explicada sem termo técnico

- **WHEN** a abertura da série é recusada pelo núcleo
- **THEN** a tela explica o motivo em linguagem de criança, sem código de erro nem termo
  técnico

### Requirement: O Guerreiro(a) solicita o local que falta e acompanha a resposta

A aplicação SHALL permitir ao Guerreiro(a) **solicitar a inclusão de um local faltante**,
declarando rótulo, nível pretendido e justificativa, e SHALL exibir a **situação** de cada
solicitação sua até o desfecho: recebida, aprovada — com o local que passa a existir — ou
recusada, **com o motivo**. A tela SHALL deixar claro que o pedido **não cria local** e que
quem decide é o Mestre da trilha ou um Admin. (`RF-05-32`, `RN-05-11`, PRD-05 §5.4)

#### Scenario: Solicitação registrada e acompanhada

- **WHEN** o Guerreiro(a) não encontra o local e solicita a inclusão
- **THEN** a solicitação é registrada e passa a aparecer na lista das suas solicitações como
  recebida

#### Scenario: A recusa chega com o motivo

- **WHEN** uma solicitação do Guerreiro(a) é recusada
- **THEN** a tela mostra a situação recusada e o motivo declarado pelo avaliador

#### Scenario: O local aprovado fica disponível para abrir série

- **WHEN** uma solicitação do Guerreiro(a) é aprovada
- **THEN** a tela mostra o local criado, e ele passa a aparecer entre os locais escolhíveis

### Requirement: O Guerreiro(a) registra a medição por digitação, voz ou mídia

A aplicação SHALL registrar a medição na forma que o **tipo de coleta** do desafio exige:
**valor digitado** ou **ditado por voz** quando a forma é número, e **foto ou vídeo** quando a
forma é mídia. A **origem** SHALL ser gravada — `manual` para o valor digitado, `voz` para o
ditado — e a aplicação NEVER SHALL declarar a origem `sensor`, que é do aparelho com credencial
de dispositivo, não da criança. O ditado por voz SHALL ser transcrito **no próprio aparelho**, e
o áudio NEVER SHALL trafegar nem ficar guardado. (`RF-05-33`, `RN-05-32`, PRD-05 §§6.4, 11)

#### Scenario: Valor digitado grava origem manual

- **WHEN** o Guerreiro(a) digita a medição numa série cujo tipo pede número
- **THEN** o registro é enviado com o valor, a unidade do tipo e a origem `manual`

#### Scenario: Valor ditado grava origem voz e descarta o áudio

- **WHEN** o Guerreiro(a) dita a medição por voz
- **THEN** o valor transcrito no aparelho é enviado com a origem `voz`, e o áudio não trafega
  nem é guardado

#### Scenario: Tipo de mídia pede a foto ou o vídeo

- **WHEN** a série é de um tipo cuja forma de registro é foto ou vídeo
- **THEN** a tela pede a mídia como o próprio registro, e não pede valor numérico

### Requirement: A tela explica o registro a conferir sem acusar a criança

A aplicação SHALL exibir, ao gravar, se o registro **pontuou na hora** ou entrou como **"a
conferir"**. O registro a conferir SHALL ser explicado como **medição que o Mestre vai olhar**,
em linguagem acolhedora, sem acusação, sem sugerir erro e sem termo técnico; a tela SHALL dizer
que os pontos entram se o Mestre confirmar. (`RF-05-34`, `RF-05-35`, `RN-05-08`, PRD-05 §5.4)

#### Scenario: Registro dentro da faixa pontua na hora

- **WHEN** o Guerreiro(a) grava uma medição dentro da faixa esperada do tipo
- **THEN** a tela confirma que a medição valeu e mostra os pontos creditados

#### Scenario: Registro fora da faixa é explicado sem acusação

- **WHEN** o núcleo devolve o registro marcado "a conferir"
- **THEN** a tela diz que a medição foi guardada e que o Mestre vai olhá-la, sem afirmar que
  houve erro e sem código técnico

### Requirement: O Guerreiro(a) lê o histórico da própria série, com o que foi invalidado

A aplicação SHALL exibir o **histórico** da série do Guerreiro(a), com a **data** e o **valor**
de cada registro, quais pontuaram e quais estão a conferir. O registro **invalidado** pelo
Mestre SHALL aparecer com o **motivo**, e a tela SHALL deixar claro que **só ele** perdeu os
pontos e que a série continua. (`RF-05-37`, `RF-05-38`, `RN-05-09`, PRD-05 §12)

#### Scenario: O histórico mostra data e valor de cada registro

- **WHEN** o Guerreiro(a) abre o histórico de uma série sua
- **THEN** vê cada registro com data, valor, situação e pontos

#### Scenario: O registro invalidado aparece com o motivo

- **WHEN** o histórico inclui um registro invalidado pelo Mestre
- **THEN** ele aparece com o motivo, e a tela diz que apenas aquele registro perdeu os pontos

### Requirement: Sem rede, o registro é recusado e nada fica enfileirado no aparelho

A aplicação SHALL **recusar** o registro de coleta quando não houver rede, explicando o motivo
em linguagem simples e orientando a tentar de novo ao reconectar. A aplicação NEVER SHALL
manter fila local de registros pendentes, NEVER SHALL guardar a medição no aparelho e NEVER
SHALL reenviá-la sozinha depois. (`RF-05-85`, PRD-05 §§10, 13)

#### Scenario: A gravação sem rede é recusada na hora

- **WHEN** o Guerreiro(a) tenta gravar uma medição com o aparelho sem rede
- **THEN** a aplicação recusa, explica que é preciso rede e orienta tentar de novo ao
  reconectar

#### Scenario: Nada da medição recusada fica no aparelho

- **WHEN** um registro é recusado por falta de rede
- **THEN** nenhuma medição, mídia ou fila permanece guardada no aparelho compartilhado

### Requirement: Toda tela que coleta dado avisa o que coleta

A aplicação SHALL exibir, em **toda tela que coleta dado**, um **aviso discreto** do que está
sendo coletado, com **acesso à área detalhada** de privacidade. O aviso SHALL estar em
linguagem de criança e NEVER SHALL bloquear a tela. (`RF-05-57`, PRD-05 §11, documento 03 §12)

#### Scenario: A tela de registro traz o aviso

- **WHEN** o Guerreiro(a) abre a tela de registrar medição
- **THEN** um aviso discreto informa o que é coletado e dá acesso à área detalhada

#### Scenario: O aviso não atrapalha o uso

- **WHEN** o aviso é exibido
- **THEN** ele não bloqueia a tela nem exige confirmação para continuar

### Requirement: A App 05 mostra as duas contas de ponto extra, separadas

A aplicação SHALL exibir ao Guerreiro(a) em sessão o **acumulado** e o **saldo disponível** de
pontos extras **separados e rotulados**, sem somá-los e sem confundi-los com o ponto regular. A
tela SHALL dizer, em linguagem simples, que o acumulado **só cresce** e que o trocável é o
**saldo disponível**. (`RF-05-82`, `RN-05-39`, `RN-05-40`, `RN-05-42`, PRD-05 §5.6)

#### Scenario: As duas contas aparecem distintas

- **WHEN** o Guerreiro(a) abre a carteira
- **THEN** vê o acumulado e o saldo disponível como dois números rotulados, nunca somados

#### Scenario: Ponto regular não entra na carteira

- **WHEN** a carteira é exibida
- **THEN** nenhum ponto regular é somado nem apresentado como trocável

#### Scenario: A carteira é só a própria

- **WHEN** o Guerreiro(a) abre a carteira
- **THEN** nenhuma conta de outra criança é exibida

### Requirement: A App 05 mostra o catálogo avulso e não troca nada

A aplicação SHALL exibir o **catálogo avulso da Comunidade Virtual** do Guerreiro(a), com o
**preço em pontos extras** e o **estoque** de cada item, e SHALL informar que a troca é feita
**presencialmente, com o Mestre, ao fim do encontro**. A aplicação NEVER SHALL oferecer troca
nem reserva de item — a execução é do App 01. (`RF-05-83`, `RF-05-86`, `RF-05-87`, PRD-05 §§3.2,
5.6)

#### Scenario: O catálogo abre com preço e estoque

- **WHEN** o Guerreiro(a) abre o catálogo avulso
- **THEN** vê os itens ativos da sua comunidade, cada um com preço em pontos extras e estoque

#### Scenario: Nenhum botão de troca ou reserva

- **WHEN** o catálogo é exibido
- **THEN** nenhuma ação de trocar ou reservar item é oferecida, e a tela explica que a troca
  acontece no encontro, com o Mestre

#### Scenario: Catálogo vazio não quebra a tela

- **WHEN** a comunidade ainda não tem item ativo cadastrado
- **THEN** a tela explica que ainda não há recompensa avulsa disponível, sem erro nem tela vazia

### Requirement: A App 05 mostra o histórico das próprias trocas

A aplicação SHALL exibir o histórico das trocas do Guerreiro(a), cada uma com o **item**, o
**preço cobrado** na data e a **data**. NEVER SHALL exibir valor em moedas nem em reais.
(`RF-05-88`, `RN-05-21`)

#### Scenario: O histórico traz item, preço e data

- **WHEN** o Guerreiro(a) abre o histórico de trocas
- **THEN** vê cada troca sua com item, preço cobrado e data

#### Scenario: O preço exibido é o cobrado na época

- **WHEN** a tabela de preços mudou depois de uma troca
- **THEN** o histórico continua mostrando o preço que foi cobrado naquela troca

#### Scenario: Nenhum custo em moedas ou reais

- **WHEN** o histórico é exibido
- **THEN** nenhum campo traz valor em moedas nem em reais

### Requirement: A App 05 avisa a recompensa conquistada e nunca a vende

A aplicação SHALL exibir as recompensas de marco que o Guerreiro(a) **conquistou**, dizendo em
linguagem simples que **a entrega é confirmada pelo Mestre** e mostrando, de cada uma, se já foi
entregue ou se aguarda. A aplicação NEVER SHALL oferecer nenhuma forma de **comprar** recompensa
de marco, com ponto de qualquer natureza. (`RF-05-45`, `RF-05-46`, `RN-05-07`, `RN-05-41`,
PRD-05 §5.6)

#### Scenario: Marco alcançado avisa a conquista

- **WHEN** o Guerreiro(a) alcança um marco que concede recompensa
- **THEN** a tela de conquistas mostra a recompensa e diz que o Mestre confirma a entrega

#### Scenario: A entrega feita aparece como feita

- **WHEN** o Mestre já confirmou a entrega
- **THEN** a mesma recompensa aparece como entregue, com a data

#### Scenario: Nenhuma tela vende recompensa de marco

- **WHEN** o Guerreiro(a) percorre carteira, catálogo e conquistas
- **THEN** em nenhuma delas há caminho de adquirir recompensa de marco com pontos

### Requirement: A App 05 mostra o estado do perfil público e não o altera

A aplicação SHALL exibir ao Guerreiro(a) o estado do **próprio perfil público** — se a
**divulgação foi autorizada** —, em linguagem simples e sem termo jurídico, dizendo que quem
decide é o responsável, na App 07. A aplicação NEVER SHALL oferecer caminho de conceder, recusar
ou revogar a autorização, e NEVER SHALL exibir qual responsável decidiu nem quando. (`RF-05-50`,
`RN-05-14`, `RN-05-21`, PRD-05 §3.2)

#### Scenario: O perfil diz se a divulgação está autorizada

- **WHEN** o Guerreiro(a) abre o próprio perfil
- **THEN** a tela diz se a divulgação foi autorizada, em linguagem de criança

#### Scenario: A criança não decide sobre a própria divulgação

- **WHEN** o perfil é exibido
- **THEN** nenhuma ação de autorizar ou revogar é oferecida, e a tela diz que quem decide é o
  responsável

#### Scenario: O perfil não expõe o ato do adulto

- **WHEN** o perfil é exibido
- **THEN** nenhum responsável, data ou motivo de decisão aparece

### Requirement: A App 05 mostra o ranking da turma com a própria posição sempre visível

A aplicação SHALL exibir o ranking da Comunidade Virtual do Guerreiro(a), **por trilha ou por
poder**, somente com **pontos regulares**, alcançando **a turma inteira** — inclusive quem não
tem divulgação autorizada. A **própria posição** SHALL estar sempre visível, ainda que fora da
faixa exibida. De cada colega a tela SHALL mostrar **apenas avatar, nick e posição**.
(`RF-05-52`, `RF-05-53`, `RF-05-84`, `RN-05-16`, `RN-05-18`, `RN-05-21`)

#### Scenario: A turma inteira aparece

- **WHEN** o Guerreiro(a) abre o ranking
- **THEN** vê os colegas da sua comunidade, inclusive os sem divulgação autorizada

#### Scenario: A própria posição nunca some

- **WHEN** o Guerreiro(a) está fora das primeiras posições exibidas
- **THEN** a tela mostra assim mesmo em que posição ele está

#### Scenario: A alternância entre trilha e poder mantém a leitura

- **WHEN** o Guerreiro(a) troca o recorte entre trilha e poder
- **THEN** o ranking é reordenado pelo ponto regular daquele recorte

#### Scenario: Nenhum dado pessoal de colega na tela

- **WHEN** o ranking é exibido
- **THEN** cada colega aparece só por avatar, nick e posição, sem imagem real nem nome civil

#### Scenario: Ponto extra não aparece no ranking

- **WHEN** o ranking é exibido
- **THEN** nenhuma posição considera ou mostra ponto extra

### Requirement: A App 05 abre na próxima missão do Guerreiro(a)

A aplicação SHALL abrir o bloco da trilha na **próxima missão** do Guerreiro(a) em sessão,
dizendo **o que fazer** e **o que ela desbloqueia**, sem que a criança precise procurar em
menu. O Guerreiro(a) inscrito em **mais de uma trilha** SHALL alternar entre elas **preservando
o contexto** de cada uma — a missão aberta numa trilha continua aberta ao voltar a ela. Sem
nenhuma inscrição, a tela SHALL levar à escolha do poder, nunca a uma tela vazia sem saída.
(`RF-05-08`, `RF-05-17`, PRD-05 §5.2)

#### Scenario: A tela inicial já mostra o que fazer agora

- **WHEN** o Guerreiro(a) inscrito abre o bloco da trilha
- **THEN** vê a próxima missão, o que precisa ser feito nela e o que ela desbloqueia

#### Scenario: Alternar de trilha não perde o contexto

- **WHEN** o Guerreiro(a) inscrito em duas trilhas alterna para a outra e volta
- **THEN** cada trilha reabre no ponto em que ele a deixou

#### Scenario: Sem inscrição, a tela oferece o caminho

- **WHEN** um Guerreiro(a) sem nenhuma inscrição abre o bloco da trilha
- **THEN** a tela o leva à escolha do poder, em vez de mostrar tela vazia

### Requirement: O Guerreiro(a) escolhe o poder e inscreve-se nas trilhas dele

A aplicação SHALL exibir os **poderes do catálogo do ciclo** e, escolhido um, as **trilhas
publicadas** dele, permitindo ao Guerreiro(a) **inscrever-se**. A escolha do poder NEVER SHALL
ser teto: ele SHALL poder inscrever-se em **quantas trilhas quiser**, de um ou de vários
poderes. A tela NEVER SHALL oferecer desinscrição, porque a inscrição não se desfaz.
(`RF-05-09`, `RN-05-43`, `RN-05-44`)

#### Scenario: Escolher o poder leva às trilhas dele

- **WHEN** o Guerreiro(a) escolhe um poder do catálogo
- **THEN** vê as trilhas publicadas daquele poder, com o caminho de se inscrever em cada uma

#### Scenario: Inscrição confirmada abre o percurso

- **WHEN** o Guerreiro(a) se inscreve numa trilha
- **THEN** a trilha passa a constar entre as dele e o percurso abre na missão de sondagem

#### Scenario: Nenhuma tela oferece desinscrever

- **WHEN** o Guerreiro(a) abre uma trilha em que está inscrito
- **THEN** nenhuma ação de sair, cancelar ou desfazer a inscrição é oferecida

### Requirement: A missão bloqueada diz o motivo, nunca é cadeado mudo

A aplicação SHALL exibir a missão **bloqueada** com o **motivo do bloqueio** e **o que falta
para abri-la**, em linguagem que a faixa de 6 a 16 anos entenda. NEVER SHALL exibir bloqueio
sem explicação. A missão **opcional** SHALL vir **marcada como tal**, com a tela dizendo que
ela **não conta** no que falta para o próximo nível. (`RF-05-10`, `RF-05-81`, `RN-05-20`,
`RN-05-33`)

#### Scenario: O bloqueio nomeia o que falta

- **WHEN** o Guerreiro(a) vê uma missão que ainda não pode abrir
- **THEN** a tela diz qual missão falta desbloquear, em linguagem simples

#### Scenario: A opcional aparece marcada e fora da conta

- **WHEN** o percurso traz uma missão opcional
- **THEN** ela aparece marcada como opcional, e a tela diz que ela não conta para o próximo
  nível

### Requirement: O Guerreiro(a) percorre o conteúdo e a bibliografia da missão

A aplicação SHALL exibir o **conteúdo da missão** — texto, imagens, vídeo e arquivos — na ordem
em que o Mestre autor o dispôs, com o **crédito ao autor** e a **licença** que a trilha
publicada declara. A **bibliografia** SHALL indicar **título** e **capítulo** e, quando o
Guerreiro(a) tiver ponto de apoio, **se há exemplar disponível nele**; sem essa informação, a
disponibilidade SHALL ficar **indeterminada**, nunca afirmada nem negada por suposição.
(`RF-05-11`, `RF-05-12`)

#### Scenario: O conteúdo abre na ordem do autor

- **WHEN** o Guerreiro(a) abre uma missão desbloqueada
- **THEN** percorre o conteúdo dela na ordem declarada, com crédito ao Mestre autor e a licença

#### Scenario: A bibliografia diz onde encontrar o livro

- **WHEN** a missão traz bibliografia vinculada a exemplar do ponto de apoio do Guerreiro(a)
- **THEN** a tela indica título, capítulo e se há exemplar disponível nele

#### Scenario: Sem vínculo, a disponibilidade não é afirmada

- **WHEN** a bibliografia da missão não está vinculada a exemplar tombado
- **THEN** a tela mostra título e capítulo e nada afirma sobre disponibilidade

### Requirement: O Guerreiro(a) responde à sondagem que abre a trilha

A aplicação SHALL apresentar a **missão de sondagem** como o primeiro passo da trilha recém
inscrita, e a tela SHALL dizer, em linguagem simples, que ela serve para **o Mestre ajustar** o
que vem pela frente e que o resultado dela **não muda o nível** de ninguém. NEVER SHALL
apresentar a sondagem como prova nem exibir acerto e erro como nota. (`RF-05-72`, `RF-05-73`,
`RN-05-34`)

#### Scenario: A sondagem abre a trilha

- **WHEN** o Guerreiro(a) abre uma trilha em que acabou de se inscrever
- **THEN** a missão de sondagem é o primeiro passo apresentado

#### Scenario: A tela explica para que serve a sondagem

- **WHEN** o Guerreiro(a) está respondendo a sondagem
- **THEN** a tela diz que ela serve para o Mestre ajustar e que não muda o nível dele

### Requirement: O Guerreiro(a) faz o desafio de desbloqueio e repete sem ser punido

A aplicação SHALL permitir ao Guerreiro(a) **realizar o desafio de desbloqueio** da missão.
**Passando**, a missão seguinte SHALL abrir **na hora**, sem recarregar a aplicação nem esperar
ato de terceiro. **Não passando**, a tela SHALL oferecer **tentar de novo** em linguagem
acolhedora, sem contagem de fracassos, sem punição e sem qualquer mensagem que elimine ou
classifique a criança. (`RF-05-13`, `RF-05-14`, `RN-05-20`)

#### Scenario: Passar abre a seguinte na hora

- **WHEN** o Guerreiro(a) realiza o desafio de desbloqueio e passa
- **THEN** a missão seguinte aparece aberta imediatamente no percurso dele

#### Scenario: Não passar convida a tentar de novo

- **WHEN** o Guerreiro(a) realiza o desafio e não passa
- **THEN** a tela o convida a tentar de novo, sem punição e sem exibir contagem de fracassos

### Requirement: O progresso mostra o nível e o que falta, nunca saldo de pontos

A aplicação SHALL exibir, por trilha ou poder, o **nível** do Guerreiro(a) e **quantas missões
obrigatórias faltam** para o próximo — nível é **percurso**, não saldo. SHALL exibir também os
**pontos, badges e recompensas conquistadas** por trilha ou poder, nunca de forma global, e
NEVER SHALL apresentar o nível como decorrência do total de pontos. Resultado ainda **não
lançado pelo Mestre** SHALL aparecer como **"aguardando lançamento"**, e a aplicação NEVER
SHALL lançar resultado, presença ou mérito. (`RF-05-15`, `RF-05-16`, `RF-05-18`, `RN-05-03`,
`RN-05-04`, `RN-05-06`)

#### Scenario: O progresso diz quantas faltam

- **WHEN** o Guerreiro(a) abre o progresso de uma trilha
- **THEN** vê o nível atual e quantas missões obrigatórias faltam para o próximo

#### Scenario: Nada sobe de nível por acúmulo de pontos

- **WHEN** o Guerreiro(a) acumula pontos sem desbloquear missão obrigatória
- **THEN** o nível exibido não muda

#### Scenario: O que o Mestre ainda não lançou aparece como tal

- **WHEN** o Guerreiro(a) cumpriu uma atividade cujo Resultado o Mestre ainda não lançou
- **THEN** a tela mostra "aguardando lançamento", sem creditar ponto nem avançar o nível

#### Scenario: Nenhuma tela lança resultado

- **WHEN** o Guerreiro(a) percorre qualquer tela do bloco da trilha
- **THEN** nenhuma ação de lançar resultado, presença ou mérito é oferecida


### Requirement: A App 05 mostra o que a criação da culminância precisa ser

Concluído o percurso da trilha, a App 05 SHALL apresentar ao Guerreiro(a) a **culminância**
daquela trilha com a **descrição** do que a criação original precisa ser, o **critério de
validação** e a **modalidade** — individual ou de equipe —, todos escritos pelo Mestre autor.
A tela NEVER SHALL reescrever nem resumir o texto do Mestre. Trilha sem culminância declarada
SHALL exibir que ela ainda não foi declarada, em linguagem simples, e NEVER SHALL oferecer a
entrega. (`RF-05-39`, `RF-09-29`, `RF-09-30`)

#### Scenario: A culminância traz descrição, critério e modalidade

- **WHEN** o Guerreiro(a) abre a culminância da trilha em que está inscrito
- **THEN** a tela mostra o que a criação precisa ser, o critério de validação e se é individual
  ou de equipe

#### Scenario: Trilha sem culminância declarada não oferece entrega

- **WHEN** a trilha ainda não tem culminância declarada pelo Mestre autor
- **THEN** a tela diz isso em linguagem simples e não apresenta o caminho de entrega

### Requirement: O Guerreiro(a) entrega a criação original da culminância

A App 05 SHALL permitir ao Guerreiro(a) entregar a criação original em **texto, imagem, vídeo,
arquivo ou link**, na modalidade que a culminância declara. Na modalidade **de equipe**, a tela
SHALL apresentar os integrantes da equipe da trilha e registrar o **papel de cada um** na
entrega; a formação da equipe NEVER SHALL acontecer aqui — ela é do App 01 e a App 05 apenas a
consulta. Enviada mídia, a tela SHALL exibir o progresso do envio até concluir. Entregue, a
tela SHALL informar que o **Mestre autor** ainda validará, e NEVER SHALL exibir ponto, nível ou
badge como já creditados. (`RF-05-40`, `RF-05-41`, `RN-05-12`)

#### Scenario: Entrega em texto ou link

- **WHEN** o Guerreiro(a) entrega a criação escrevendo o texto ou informando o link
- **THEN** a App 05 registra a entrega e mostra que o Mestre autor ainda validará

#### Scenario: Entrega em mídia mostra o progresso do envio

- **WHEN** o Guerreiro(a) entrega a criação enviando imagem, vídeo ou arquivo
- **THEN** a tela mostra o progresso do envio até concluir

#### Scenario: Entrega de equipe registra o papel de cada integrante

- **WHEN** a culminância é de equipe e o Guerreiro(a) entrega pela equipe da trilha
- **THEN** a tela apresenta os integrantes e registra o papel de cada um na entrega

#### Scenario: A App 05 não forma nem edita equipe

- **WHEN** o Guerreiro(a) abre a entrega de uma culminância de equipe
- **THEN** a tela apenas consulta a equipe homologada, sem oferecer formar nem editar

### Requirement: A criação devolvida diz o motivo e aceita o reenvio

A App 05 SHALL exibir a criação original **devolvida** com o **motivo escrito pelo Mestre**, em
linguagem simples, e SHALL apresentar o caminho de reenvio da produção ajustada. A tela NEVER
SHALL apresentar a devolução como punição nem como perda: a **autoria permanece** e SHALL
continuar visível ao Guerreiro(a) depois da devolução. (`RF-05-42`, `RN-05-13`)

#### Scenario: Devolução traz o motivo e a autoria intacta

- **WHEN** o Mestre autor devolve a criação original do Guerreiro(a)
- **THEN** a tela mostra o motivo em linguagem simples e a autoria segue creditada a ele

#### Scenario: Criação devolvida pode ser reenviada

- **WHEN** o Guerreiro(a) ajusta a produção de uma criação devolvida
- **THEN** a tela permite reenviá-la, e a criação volta a aguardar a decisão do Mestre autor

### Requirement: O portfólio reúne as criações validadas e diz quais são públicas

A App 05 SHALL apresentar o **portfólio** do Guerreiro(a) com as criações originais
**validadas** de que ele é creditado, cada uma com a **trilha**, a **data** e a **autoria**. Cada
criação SHALL indicar se está **pública** ou se **depende de autorização do responsável**, e a
tela SHALL dizer, em linguagem simples, que a autorização é ato do responsável na App 07.
Criação validada sem autorização SHALL aparecer no portfólio do Guerreiro(a). A App 05 NEVER
SHALL oferecer alterar a autorização de divulgação nem exibir criação de outro Guerreiro(a).
(`RF-05-43`, `RF-05-44`, `RN-05-14`, `RN-05-21`)

#### Scenario: Portfólio traz trilha, data e autoria de cada criação validada

- **WHEN** o Guerreiro(a) abre o portfólio
- **THEN** a tela mostra cada criação validada com a trilha, a data e a autoria creditada

#### Scenario: Criação sem autorização aparece como dependente de autorização

- **WHEN** uma criação validada do Guerreiro(a) não tem autorização de divulgação vigente de
  todos os creditados
- **THEN** ela aparece no portfólio marcada como dependente de autorização do responsável

#### Scenario: A App 05 não altera a autorização de divulgação

- **WHEN** o Guerreiro(a) vê uma criação dependente de autorização
- **THEN** a tela explica que a autorização é ato do responsável e não oferece alterá-la

### Requirement: O Guerreiro(a) lê os próprios desafios em aberto

O núcleo SHALL servir, em `GET /v1/eu/desafios`, o que o Guerreiro(a) **em sessão** tem em
aberto, em **dois conjuntos apartados**: os **semanais** e os **extras**.

Os **semanais** SHALL ser as **atividades em aberto** dele: as das missões que ele já
**desbloqueou**, nas trilhas em que está **inscrito**, e para as quais o Mestre ainda **não
lançou Resultado** para ele. Cada atividade SHALL trazer **modalidade** e **formato**, além do
título, da descrição, da produção esperada e da missão e trilha a que pertence.

Os **extras** SHALL ser os desafios extras publicados, vigentes e elegíveis a ele, na forma da
capacidade `desafio-extra`.

A leitura SHALL alcançar apenas o Guerreiro(a) da sessão, identificado pelo contexto e nunca
por identificador vindo do cliente, e NEVER SHALL devolver atividade de trilha em que ele não
está inscrito, de missão que ele ainda não desbloqueou nem atividade cujo Resultado já foi
lançado para ele. Guerreiro(a) sem nada em aberto SHALL receber **200** com os **dois conjuntos
vazios**, nunca erro. Persona que não é Guerreiro(a) SHALL receber **403**. (`RF-05-19`,
`RF-05-20`, `RN-05-21`, `RN-05-06`)

#### Scenario: As atividades das missões desbloqueadas são devolvidas

- **WHEN** um Guerreiro(a) em sessão consulta os próprios desafios e tem missões desbloqueadas
  com atividades sem Resultado lançado
- **THEN** o núcleo devolve essas atividades no conjunto dos semanais, cada uma com modalidade
  e formato

#### Scenario: Atividade de missão ainda bloqueada não aparece

- **WHEN** existe atividade numa missão que o Guerreiro(a) ainda não desbloqueou
- **THEN** essa atividade não entra na leitura

#### Scenario: Atividade já lançada pelo Mestre sai da lista

- **WHEN** o Mestre lança o Resultado do Guerreiro(a) numa atividade que estava em aberto
- **THEN** a leitura seguinte não a devolve mais

#### Scenario: Atividade de trilha em que não se inscreveu não aparece

- **WHEN** existe atividade em trilha na qual o Guerreiro(a) não está inscrito
- **THEN** essa atividade não entra na leitura

#### Scenario: Os dois conjuntos vêm apartados na mesma resposta

- **WHEN** o Guerreiro(a) em sessão tem atividade em aberto e desafio extra elegível
- **THEN** a resposta traz a atividade entre os semanais e o desafio extra entre os extras, sem
  misturar os dois conjuntos

#### Scenario: Sem nada em aberto a resposta é conjunto vazio

- **WHEN** o Guerreiro(a) em sessão não tem nenhuma atividade em aberto nem desafio extra
  elegível
- **THEN** o núcleo responde 200 com os dois conjuntos vazios, nunca erro

#### Scenario: Persona que não é Guerreiro(a) não lê

- **WHEN** um Mestre, Admin, Apoiador ou responsável em sessão consulta a rota
- **THEN** o núcleo responde 403 e nada é devolvido

### Requirement: A App 05 mostra os desafios extras vigentes, apartados dos semanais

A App 05 SHALL apresentar ao Guerreiro(a), no bloco dos desafios e **apartados dos semanais**,
os **desafios extras vigentes** que lhe são elegíveis, cada um com a **recompensa oferecida**,
a **quantidade disponível**, o **período de vigência**, o **critério** para conquistá-la, o
**formato** — presencial ou on-line — e a trilha (e a missão, quando houver) a que se prende,
em linguagem da criança. O desafio **direcionado** SHALL ser apresentado como dirigido a ela,
sem nomear terceiro. Guerreiro(a) sem desafio extra elegível SHALL ver uma mensagem que diz
isso, e NEVER SHALL receber lista vazia sem explicação.

A tela SHALL dizer que os pontos do desafio extra são **extras** e não contam para o nível, e
NEVER SHALL oferecer concluir, disputar, comprar ou trocar o desafio: no Ciclo 01 a conclusão é
lançada fora desta aplicação. (`RF-05-20`, `RF-05-21`, `RN-05-18`, `RN-05-06`)

#### Scenario: Cada desafio extra diz recompensa, quantidade e vigência

- **WHEN** o Guerreiro(a) abre o bloco dos desafios e tem desafio extra elegível
- **THEN** vê cada um com a recompensa oferecida, a quantidade disponível, o período de
  vigência e o critério para conquistá-la

#### Scenario: Os extras não se misturam aos semanais

- **WHEN** o Guerreiro(a) tem desafio semanal e desafio extra ao mesmo tempo
- **THEN** a tela mostra os dois em blocos distintos, cada um identificado como o que é

#### Scenario: O esgotado continua visível, dizendo que acabou

- **WHEN** um desafio extra vigente já teve todas as recompensas entregues
- **THEN** ele continua na tela, marcado como esgotado, em vez de desaparecer sem explicação

#### Scenario: Sem desafio extra a tela explica

- **WHEN** o Guerreiro(a) não tem nenhum desafio extra elegível
- **THEN** a tela diz isso em linguagem simples, sem lista vazia muda

#### Scenario: A tela diz que o ponto extra não sobe nível

- **WHEN** o Guerreiro(a) vê os pontos que um desafio extra vale
- **THEN** a tela informa que são pontos extras e que não contam para o nível da trilha

#### Scenario: Nenhuma ação de concluir ou trocar é oferecida

- **WHEN** o Guerreiro(a) percorre os desafios extras
- **THEN** nenhuma ação de concluir, disputar, comprar ou trocar aparece

### Requirement: A App 05 mostra os desafios em aberto, com modalidade e formato

A App 05 SHALL apresentar ao Guerreiro(a) os **desafios em aberto** dele, cada um com a
**modalidade** — individual, em equipe ou em equipe com familiar — e o **formato** —
presencial ou on-line —, em linguagem da criança, junto do que se espera que ele produza e da
missão e trilha a que o desafio pertence. Guerreiro(a) sem desafio em aberto SHALL ver uma
mensagem que diz isso, e NEVER SHALL receber lista vazia sem explicação.

A tela NEVER SHALL oferecer lançar resultado, presença ou mérito, e NEVER SHALL apresentar o
desafio como comprável ou trocável. (`RF-05-19`, `RN-05-06`)

#### Scenario: Cada desafio diz a modalidade e o formato

- **WHEN** o Guerreiro(a) abre o bloco dos desafios com atividades em aberto
- **THEN** vê cada desafio com a modalidade e o formato dele, e o que precisa produzir

#### Scenario: Sem desafio em aberto a tela explica

- **WHEN** o Guerreiro(a) não tem nenhum desafio em aberto
- **THEN** a tela diz isso em linguagem simples, sem lista vazia muda

#### Scenario: Nenhuma tela do bloco lança resultado

- **WHEN** o Guerreiro(a) percorre o bloco dos desafios
- **THEN** nenhuma ação de lançar resultado, presença ou mérito é oferecida

### Requirement: A App 05 mostra as equipes de que o Guerreiro(a) participa

A App 05 SHALL apresentar ao Guerreiro(a) as **equipes de que ele participa** — as da aula e as
da trilha —, o **papel** dele em cada uma e as **atividades** de cada equipe. Cada colega SHALL
aparecer **apenas por avatar e nick**, e a tela NEVER SHALL exibir imagem real, nome civil,
data de nascimento nem qualquer outro dado pessoal de outra criança.

Guerreiro(a) que não integra nenhuma equipe SHALL ver uma mensagem que diz isso e onde a equipe
se forma. (`RF-05-22`, `RF-05-23`, `RN-05-15`, `RN-05-21`)

#### Scenario: As equipes vêm com papel e atividades

- **WHEN** o Guerreiro(a) abre o bloco das equipes e integra equipes de aula e de trilha
- **THEN** vê cada equipe, o papel dele nela e as atividades daquela equipe

#### Scenario: Colega aparece só por avatar e nick

- **WHEN** a tela exibe os integrantes de uma equipe
- **THEN** cada integrante aparece por avatar e nick, e nenhum dado pessoal é exibido

#### Scenario: Sem equipe a tela explica onde ela se forma

- **WHEN** o Guerreiro(a) não integra nenhuma equipe
- **THEN** a tela diz isso e informa que a equipe se forma no encontro, no App 01

### Requirement: A App 05 não forma nem edita equipe e não tem canal de conversa

A App 05 NEVER SHALL oferecer **formar, editar, entrar em, sair de nem homologar** equipe: a
formação acontece no App 01, a cada aula, e a homologação da equipe da trilha é do Mestre. A
tela de equipes SHALL dizer, em linguagem simples, onde a equipe se forma.

Nenhuma tela desta aplicação SHALL oferecer **canal de conversa** entre pessoas — nem mensagem
a colega, nem comentário em equipe, nem contato com Mestre, responsável ou Apoiador.
(`RF-05-24`, `RN-05-12`, `RN-05-22`)

#### Scenario: Nenhuma ação de formar ou editar equipe é oferecida

- **WHEN** o Guerreiro(a) percorre o bloco das equipes
- **THEN** nenhuma ação de criar, editar, entrar, sair ou homologar equipe aparece

#### Scenario: A tela diz onde a equipe se forma

- **WHEN** o Guerreiro(a) abre o bloco das equipes
- **THEN** a tela informa que a formação acontece no encontro, no App 01

#### Scenario: Nenhum canal de conversa em nenhuma tela

- **WHEN** o Guerreiro(a) percorre os blocos dos desafios e das equipes
- **THEN** nenhuma caixa de mensagem, comentário ou contato entre pessoas é oferecida

### Requirement: As retomadas em aberto nascem da cadência do Mestre e do desbloqueio do Guerreiro(a)

O núcleo SHALL derivar as **retomadas em aberto** de um Guerreiro(a) da **cadência de retomada**
que o Mestre autor declarou na missão e do **momento em que ele a desbloqueou**: cada dia da
cadência é um **agendamento**, com prazo contado do desbloqueio. Nenhum estado de retomada
SHALL ser persistido — a lista nasce na leitura, como o percurso já nasce.

Um agendamento SHALL estar **em aberto** quando o prazo dele já **venceu** e o Guerreiro(a)
ainda **não entregou produção** daquela missão a partir daquele prazo. Missão **sem cadência
declarada** NEVER SHALL gerar retomada, e missão que ele ainda **não desbloqueou** também não —
não há de onde contar o prazo. Desbloqueio prático ainda **não julgado** pelo Mestre NEVER SHALL
abrir agendamento. (`RF-05-79`, `RF-09-83`, `RF-09-101`, documento 11 §2.2)

#### Scenario: A cadência declarada vira agendamentos contados do desbloqueio

- **WHEN** o Guerreiro(a) desbloqueou uma missão cuja cadência de retomada é de 2, 7 e 21 dias
- **THEN** ele tem três agendamentos, com prazos de 2, 7 e 21 dias contados do desbloqueio dele

#### Scenario: Só o agendamento vencido aparece em aberto

- **WHEN** passaram 3 dias do desbloqueio de uma missão com cadência de 2, 7 e 21 dias, e ele
  não entregou produção alguma
- **THEN** a retomada de 2 dias está em aberto, e as de 7 e 21 dias ainda não

#### Scenario: Missão sem cadência declarada não gera retomada

- **WHEN** o Guerreiro(a) desbloqueia uma missão que o Mestre deixou sem cadência de retomada
- **THEN** nenhuma retomada dela aparece para ele

#### Scenario: Missão não desbloqueada não gera retomada

- **WHEN** uma missão com cadência declarada ainda não foi desbloqueada pelo Guerreiro(a)
- **THEN** nenhuma retomada dela aparece para ele

#### Scenario: Desbloqueio prático ainda não julgado não abre agendamento

- **WHEN** o Guerreiro(a) declarou ter cumprido o desafio prático e o Mestre autor ainda não
  julgou
- **THEN** nenhuma retomada daquela missão aparece para ele

#### Scenario: A retomada é de cada Guerreiro(a), pelo desbloqueio dele

- **WHEN** dois Guerreiros desbloqueiam a mesma missão em dias diferentes
- **THEN** os prazos das retomadas de cada um são contados do desbloqueio dele, e não do colega

### Requirement: A retomada vale uma vez por agendamento, e refazer por conta própria não a reabre

A produção entregue pelo Guerreiro(a) **a partir do prazo** de um agendamento SHALL **fechá-lo**,
e o agendamento fechado NEVER SHALL voltar à lista de retomadas em aberto. Entregar de novo na
mesma missão NEVER SHALL reabrir agendamento algum nem criar agendamento novo: a cadência
declarada pelo Mestre é a única fonte dos agendamentos.

A produção entregue **antes** do prazo do próximo agendamento — refazer por conta própria —
SHALL ser gravada e receber devolutiva como qualquer outra, e NEVER SHALL fechar, antecipar nem
consumir agendamento algum. Nem a retomada nem o refazer creditam ponto: quem lança o resultado
segue sendo o Mestre. (`RF-05-80`, `RN-05-38`, `RN-05-05`, documento 11 §§2.2, 5)

#### Scenario: A produção entregue fecha o agendamento vencido

- **WHEN** o Guerreiro(a) entrega a produção de uma missão cuja retomada de 2 dias está em
  aberto
- **THEN** aquele agendamento sai da lista de retomadas em aberto

#### Scenario: Entregar duas vezes não reabre nem duplica o agendamento

- **WHEN** ele entrega uma segunda produção da mesma missão, ainda antes do próximo prazo
- **THEN** nenhum agendamento volta à lista e nenhum agendamento novo é criado

#### Scenario: Refazer por conta própria não consome agendamento

- **WHEN** o Guerreiro(a) entrega a produção de uma missão no dia seguinte ao desbloqueio, antes
  de qualquer prazo vencer
- **THEN** a produção é gravada com devolutiva, e a retomada de 2 dias aparece em aberto quando
  o prazo dela vencer

#### Scenario: O agendamento seguinte vence normalmente

- **WHEN** o Guerreiro(a) fechou a retomada de 2 dias e chega o 8º dia
- **THEN** a retomada de 7 dias aparece em aberto

#### Scenario: A retomada não credita ponto

- **WHEN** um agendamento é fechado pela produção entregue
- **THEN** nenhum ponto é creditado, nenhum Resultado é gravado e o percurso segue igual

### Requirement: As retomadas em aberto são alcançáveis por HTTP pelo Guerreiro(a) em sessão

O núcleo SHALL expor as retomadas em aberto por `GET /v1/eu/retomadas`, sob a **sessão do
Guerreiro(a)**, devolvendo, para cada agendamento em aberto, a **missão**, a **trilha** e o
**prazo** dele. A leitura SHALL alcançar **apenas** o Guerreiro(a) em sessão: retomada de
terceiro NEVER SHALL aparecer. Persona que não é Guerreiro(a) SHALL receber **403**, e chamada
sem persona em sessão SHALL ser recusada. (`RF-05-79`, `RN-05-21`, PRD-05 §9)

#### Scenario: O Guerreiro(a) lê as próprias retomadas

- **WHEN** o Guerreiro(a) em sessão consulta as retomadas
- **THEN** o núcleo responde com os agendamentos em aberto dele, cada um com missão, trilha e
  prazo

#### Scenario: Sem retomada em aberto a lista vem vazia

- **WHEN** ele consulta as retomadas e nenhum agendamento venceu sem produção
- **THEN** o núcleo responde com a lista vazia, sem erro

#### Scenario: A retomada de terceiro não aparece

- **WHEN** ele consulta as retomadas
- **THEN** nenhum agendamento de outro Guerreiro(a) aparece na resposta

#### Scenario: A gestão não lê retomadas por esta porta

- **WHEN** um Mestre ou um Admin em sessão consulta a rota
- **THEN** o núcleo responde 403

### Requirement: A App 05 entrega a produção da missão nas três formas, avisando o que descarta

A App 05 SHALL oferecer, na missão desbloqueada, a **entrega da produção** nas três formas —
escrever, gravar a fala ou fotografar o que fez à mão (`RF-05-74`) —, com as três apresentadas
lado a lado e nenhuma como padrão obrigatório.

Antes de enviar em áudio ou em foto, a tela SHALL dizer, em linguagem da criança, que a
gravação e a fotografia são **descartadas na leitura** e que ficam guardadas apenas a
transcrição e a devolutiva (`RF-05-76`, `RN-05-36`). A App 05 NEVER SHALL guardar a foto nem o
áudio no aparelho depois do envio. (`RF-05-74`, `RF-05-76`, documento 03 §12.2)

#### Scenario: As três formas aparecem na missão

- **WHEN** o Guerreiro(a) abre uma missão que ele desbloqueou
- **THEN** a tela oferece escrever, gravar a fala e fotografar o que fez à mão

#### Scenario: A tela avisa o descarte antes de enviar

- **WHEN** ele escolhe gravar a fala ou fotografar o manuscrito
- **THEN** a tela diz que a gravação e a foto são descartadas na leitura e que ficam só a
  transcrição e a devolutiva

#### Scenario: O aparelho não fica com a mídia

- **WHEN** o envio termina
- **THEN** a foto e o áudio não permanecem no aparelho

### Requirement: A App 05 mostra a devolutiva como próximo passo e diz que ela não vale ponto

A App 05 SHALL exibir a **devolutiva** da produção como **retorno construtivo** — o que está
bom e qual o próximo passo —, nunca como nota, acerto, erro ou correção (`RF-05-75`).

Na mesma tela, a App 05 SHALL dizer que a devolutiva **não credita ponto** e que o resultado da
atividade fica **"aguardando lançamento"** até o Mestre lançá-lo (`RF-05-77`, `RN-05-05`). A
App 05 NEVER SHALL exibir ponto, nível ou badge como consequência da entrega.

Não vindo a devolutiva, a tela SHALL confirmar que a produção **foi guardada** e dizer que o
retorno não veio agora — nunca deixar a criança sem saber se o que escreveu se perdeu.
(`RF-05-75`, `RF-05-77`, `RN-05-35`)

#### Scenario: A devolutiva aponta o próximo passo

- **WHEN** a produção é entregue e a devolutiva volta
- **THEN** a tela a exibe como o que está bom e qual o próximo passo

#### Scenario: A tela diz que a devolutiva não vale ponto

- **WHEN** a devolutiva é exibida
- **THEN** a tela diz, na mesma altura, que ela não vale ponto e que o resultado aguarda o
  lançamento do Mestre

#### Scenario: Nenhum ponto aparece por causa da entrega

- **WHEN** a entrega termina
- **THEN** nenhum ponto, nível ou badge novo é exibido como consequência dela

#### Scenario: Devolutiva que não veio não deixa dúvida

- **WHEN** a produção é guardada e a devolutiva não vem
- **THEN** a tela confirma que a produção foi guardada e diz que o retorno não veio agora

### Requirement: A App 05 não obriga foto nem áudio e mostra o caminho do encontro

A App 05 SHALL apresentar, junto às três formas de entrega, o caminho **"entrego ao Mestre no
encontro"**, com o mesmo destaque das demais — nunca como opção escondida, secundária ou de
exceção.

A tela SHALL dizer que quem não quer ser fotografado nem gravado **não perde a missão**, e a
App 05 NEVER SHALL bloquear a missão, esconder o conteúdo dela nem sinalizar pendência por
falta de produção entregue. (`RF-05-78`, `RN-05-37`, documento 03 §3.3)

#### Scenario: O caminho do encontro aparece com as outras formas

- **WHEN** o Guerreiro(a) abre a entrega da produção
- **THEN** "entrego ao Mestre no encontro" aparece com o mesmo destaque de escrever, gravar e
  fotografar

#### Scenario: A tela diz que ninguém perde a missão

- **WHEN** ele escolhe entregar ao Mestre no encontro
- **THEN** a tela diz que ele não perde a missão e nada é bloqueado

#### Scenario: Missão sem produção não vira pendência acusatória

- **WHEN** uma missão desbloqueada segue sem produção entregue
- **THEN** a tela não a marca como pendência nem esconde o conteúdo dela

### Requirement: A App 05 mostra as retomadas e explica que rever fixa

A App 05 SHALL mostrar, ao Guerreiro(a), as **retomadas em aberto** — a missão, a trilha e o
prazo de cada uma —, com a explicação, em linguagem da criança, de que **rever o que já foi
feito fixa o aprendizado** (`RF-05-79`). Sem retomada em aberto, a tela SHALL dizer isso — nunca
lista vazia muda.

Entregue a produção da retomada, ela SHALL sair da lista. A App 05 SHALL manter o caminho de
refazer a missão por conta própria pela tela dela, e SHALL dizer que refazer assim **não rende
ponto novo** (`RF-05-80`, `RN-05-38`). A App 05 NEVER SHALL apresentar a retomada como punição,
atraso ou dívida.

#### Scenario: As retomadas aparecem com missão, trilha e prazo

- **WHEN** o Guerreiro(a) abre o bloco das retomadas com agendamentos em aberto
- **THEN** cada retomada aparece com a missão, a trilha e o prazo dela

#### Scenario: A tela explica para que serve a retomada

- **WHEN** a lista de retomadas é exibida
- **THEN** a tela diz que rever o que já foi feito fixa o aprendizado

#### Scenario: Sem retomada, a tela diz que não há

- **WHEN** nenhum agendamento está em aberto
- **THEN** a tela diz que não há retomada agora, em vez de mostrar lista vazia muda

#### Scenario: A retomada entregue sai da lista

- **WHEN** ele entrega a produção de uma retomada em aberto
- **THEN** ela deixa de aparecer na lista

#### Scenario: A tela diz que refazer por conta própria não rende ponto novo

- **WHEN** ele abre uma missão já cumprida para refazer fora de agendamento
- **THEN** a tela diz que refazer por conta própria não rende ponto novo

#### Scenario: A retomada não é apresentada como castigo

- **WHEN** uma retomada é exibida
- **THEN** nenhuma palavra de atraso, dívida ou punição aparece
