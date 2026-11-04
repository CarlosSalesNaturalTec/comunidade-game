# Spec Delta

## MODIFIED Requirements

### Requirement: O portfólio público exibe as criações autorizadas com trilha, data e autoria

A App 06 SHALL exibir o **portfólio** do acervo autorizado, cada item em **uma linha**, com o
**título** em destaque, a **data** em que o Mestre o aprovou e a **autoria por nick** de cada
creditado, com o **avatar** de cada um. A linha SHALL trazer também a **trilha**, exceto quando
o título já é o nome dela — a criação da culminância —, caso em que NEVER SHALL repeti-lo
(decisão do fundador, 2026-11-04). Cada **nick creditado** SHALL abrir a página individual
daquele Guerreiro(a). NEVER SHALL exibir item cujo creditado não tenha autorização vigente, nem
item sem aprovação do Mestre. A seção SHALL sair em ordem **decrescente** por data de aprovação
e SHALL manter o nome "Portfólio de criações originais". (`RF-03-08`, `RF-03-83`, `RF-03-84`,
`RN-03-02`, `RN-03-41`, `RN-03-43`)

Isto **substitui** a saída **sem título**, decidida em 2026-09-28, quando título nenhum
existia.

#### Scenario: A criação aparece com trilha, data e autoria

- **WHEN** o visitante abre o portfólio
- **THEN** cada linha traz o título em destaque, a data de aprovação, a trilha quando ela não
  é o título, e o avatar e o nick de cada autor creditado

#### Scenario: A comprovação aprovada traz o título curto e a trilha

- **WHEN** o visitante abre o portfólio e vê a linha de uma comprovação de desafio prático
  aprovada
- **THEN** a linha traz o título curto declarado pelo Mestre e, ao lado da data, a trilha da
  missão

#### Scenario: A criação da culminância não repete a trilha

- **WHEN** o visitante abre o portfólio e vê a linha de uma criação da culminância, cujo título
  é o nome da trilha
- **THEN** o nome da trilha aparece uma vez, como título, e não uma segunda vez na linha

#### Scenario: O portfólio não exibe quem não autorizou

- **WHEN** uma criação tem creditado sem autorização vigente
- **THEN** ela não aparece no portfólio

#### Scenario: A criação mais recente abre o portfólio

- **WHEN** o visitante abre o portfólio
- **THEN** a primeira linha é o item aprovado mais recentemente, de qualquer uma das
  duas fontes

#### Scenario: O nick creditado abre a página do autor

- **WHEN** o visitante aciona o nick de um autor creditado
- **THEN** a página individual daquele Guerreiro(a) abre, em endereço próprio

## ADDED Requirements

### Requirement: A linha do portfólio abre a produção na própria linha

A App 06 SHALL permitir que o visitante **abra a produção** de um item do acervo **na própria
linha**, sem sair da seção e sem endereço novo: a criação não tem página individual. Ao abrir,
SHALL exibir a **imagem**, o **áudio**, o **vídeo** ou o **texto**; o **link externo** SHALL
sair como link de saída e o **arquivo**, como transferência. Fechar SHALL devolver a linha ao
estado recolhido. (`RF-03-85`, `RF-03-03`)

#### Scenario: A imagem abre na linha

- **WHEN** o visitante abre a produção de um item do tipo imagem
- **THEN** a imagem aparece na própria linha, com texto alternativo, e a lista continua visível

#### Scenario: O áudio e o vídeo abrem com controles

- **WHEN** o visitante abre a produção de um item do tipo áudio ou vídeo
- **THEN** ela aparece na linha com controles de reproduzir e pausar, e nada toca sozinho

#### Scenario: O texto abre na linha

- **WHEN** o visitante abre a produção de um item do tipo texto
- **THEN** o corpo do texto aparece na própria linha

#### Scenario: O link externo sai como link

- **WHEN** o item é do tipo link externo
- **THEN** a linha oferece um link de saída para o endereço, e não embute conteúdo de terceiro

#### Scenario: O arquivo sai como transferência

- **WHEN** o item é do tipo arquivo
- **THEN** a linha oferece a transferência do arquivo, sem tentar exibi-lo

#### Scenario: Fechar devolve a linha ao estado recolhido

- **WHEN** o visitante abriu a produção de um item e aciona o fechar
- **THEN** a linha volta a exibir só título, data, trilha e autoria

#### Scenario: O que foi aberto não é gravado no aparelho

- **WHEN** o visitante abre a produção de um item e recarrega a página
- **THEN** todas as linhas voltam recolhidas, e nada da navegação dele foi gravado no aparelho

### Requirement: A produção que o núcleo não serve não vira linha quebrada

Quando a produção de um item não puder ser servida, a App 06 SHALL dizê-lo em **linguagem
simples** na própria linha, mantendo título, data, trilha e autoria à vista, e NEVER SHALL
revelar o motivo da recusa do núcleo — que a autorização caiu, ou que o Mestre não a tornou
publicável. (`RF-03-85`, `RN-03-02`)

#### Scenario: A mídia indisponível é dita em linguagem simples

- **WHEN** o visitante abre a produção de um item e o núcleo não a serve
- **THEN** a linha diz, em linguagem simples, que a produção não está disponível agora, e segue
  exibindo título, data, trilha e autoria
