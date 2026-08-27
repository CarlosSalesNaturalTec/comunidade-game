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
