## ADDED Requirements

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
