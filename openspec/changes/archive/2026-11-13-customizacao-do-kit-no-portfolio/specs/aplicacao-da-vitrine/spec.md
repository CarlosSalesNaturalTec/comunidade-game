## MODIFIED Requirements

### Requirement: O portfólio público exibe as criações autorizadas com trilha, data e autoria

A App 06 SHALL exibir o **portfólio** do acervo autorizado, cada item em **uma linha**, com o
**título** em destaque, a **data** em que o Mestre o aprovou e a **autoria por nick** de cada
creditado, com o **avatar** de cada um. A linha SHALL trazer também a **trilha**, exceto quando
o título já é o nome dela — a criação da culminância —, caso em que NEVER SHALL repeti-lo
(decisão do fundador, 2026-11-04). Cada **nick creditado** SHALL abrir a página individual
daquele Guerreiro(a). NEVER SHALL exibir item cujo creditado não tenha autorização vigente, nem
item sem aprovação do Mestre. O acervo tem **três** fontes — a comprovação aprovada do prático,
a criação da culminância e o registro aprovado da customização do kit —, e a do registro de
customização SHALL sair com a **descrição** do Guerreiro(a) como título e a **trilha** em que o
kit foi recebido. A seção SHALL sair em ordem **decrescente** por data de aprovação e SHALL
manter o nome "Portfólio de criações originais". (`RF-03-08`, `RF-03-83`, `RF-03-84`,
`RF-03-88`, `RN-03-02`, `RN-03-41`, `RN-03-43`)

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

#### Scenario: A customização aprovada traz a descrição e a trilha do kit

- **WHEN** o visitante abre o portfólio e vê a linha de um registro de customização do kit
  aprovado
- **THEN** a linha traz a descrição do Guerreiro(a) como título e, ao lado da data, a trilha em
  que o kit foi recebido

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
  três fontes

#### Scenario: O nick creditado abre a página do autor

- **WHEN** o visitante aciona o nick de um autor creditado
- **THEN** a página individual daquele Guerreiro(a) abre, em endereço próprio

### Requirement: A linha do portfólio abre a produção na própria linha

A App 06 SHALL permitir que o visitante **abra a produção** de um item do acervo **na própria
linha**, sem sair da seção e sem endereço novo: a criação não tem página individual. Ao abrir,
SHALL exibir a **imagem**, o **áudio**, o **vídeo** ou o **texto**; o **link externo** SHALL
sair como link de saída e o **arquivo**, como transferência. Os bytes SHALL ser pedidos à rota
pública **da fonte do item** — criação original, comprovação do prático ou customização do kit.
Fechar SHALL devolver a linha ao estado recolhido. (`RF-03-85`, `RF-03-88`, `RF-03-03`)

#### Scenario: A imagem abre na linha

- **WHEN** o visitante abre a produção de um item do tipo imagem
- **THEN** a imagem aparece na própria linha, com texto alternativo, e a lista continua visível

#### Scenario: O áudio e o vídeo abrem com controles

- **WHEN** o visitante abre a produção de um item do tipo áudio ou vídeo
- **THEN** ela aparece na linha com controles de reproduzir e pausar, e nada toca sozinho

#### Scenario: A customização abre a mídia do kit

- **WHEN** o visitante abre a produção de um registro de customização do kit aprovado, do tipo
  imagem ou vídeo
- **THEN** a mídia vem da rota pública da customização e aparece na própria linha, e não pela
  rota de outra fonte

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

### Requirement: A coluna de criações originais da carta lista o acervo com título e data

Na carta do Guerreiro(a), a coluna "Criações originais" SHALL listar o **acervo público** dele —
a criação da culminância, as comprovações aprovadas do prático e os registros aprovados da
customização do kit —, um item por linha, com o **título** e a **data** de aprovação, do mais
recente ao mais antigo. O título SHALL seguir o `RN-03-43` e, na customização, SHALL ser a
descrição do Guerreiro(a). A coluna NEVER SHALL abrir a produção: é o resumo, e a produção abre
no portfólio abaixo da carta. (`RF-03-05`, `RF-03-86`, `RF-03-88`, `RN-03-43`, decisão do
fundador, 2026-11-07)

#### Scenario: A comprovação aprovada aparece na carta

- **WHEN** o visitante abre a página de um Guerreiro(a) que só tem comprovações aprovadas do
  prático
- **THEN** a coluna "Criações originais" lista cada uma pelo título curto do desafio e pela data,
  e não diz que não há criação validada

#### Scenario: A customização aprovada aparece na carta

- **WHEN** o visitante abre a página de um Guerreiro(a) que tem registro de customização do kit
  aprovado
- **THEN** a coluna "Criações originais" o lista pela descrição e pela data de aprovação

#### Scenario: A criação da culminância aparece pelo nome da trilha

- **WHEN** o Guerreiro(a) tem a criação da culminância validada
- **THEN** a coluna a lista com o nome da trilha como título e a data de validação

#### Scenario: A coluna abre pelo item mais recente

- **WHEN** a coluna lista mais de um item
- **THEN** o mais recente vem primeiro

#### Scenario: Sem item no acervo público, a coluna diz que não há

- **WHEN** o Guerreiro(a) não tem item aprovado e autorizado no acervo
- **THEN** a coluna diz em uma frase que não há criação original ainda

### Requirement: A página do Guerreiro(a) mantém o portfólio abaixo da carta, com a linha da vitrine

A página do Guerreiro(a) SHALL manter o **portfólio** abaixo da carta, com os mesmos itens da
coluna, na mesma ordem, e cada item na **linha do portfólio da vitrine**: título, data, trilha
fora da criação da culminância e autoria por nick. A linha SHALL **abrir a produção** como a
linha do portfólio da vitrine, também na customização do kit. (`RF-03-87`, `RF-03-85`,
`RF-03-88`, `RN-03-43`, decisão do fundador, 2026-11-07)

#### Scenario: O portfólio da página traz as duas fontes

- **WHEN** o visitante abre a página de um Guerreiro(a) com uma criação da culminância e uma
  comprovação aprovada
- **THEN** o portfólio abaixo da carta traz as duas, a mais recente primeiro

#### Scenario: O portfólio da página traz a customização aprovada

- **WHEN** o visitante abre a página de um Guerreiro(a) com um registro de customização do kit
  aprovado
- **THEN** o portfólio abaixo da carta o traz pela descrição, com a trilha do kit e a data, e a
  mídia abre na própria linha

#### Scenario: A linha da página abre a produção

- **WHEN** o visitante aciona a produção de uma linha do portfólio da página
- **THEN** a produção abre na própria linha, como no portfólio da vitrine

#### Scenario: A linha da página é a da vitrine

- **WHEN** um item aparece no portfólio da página e no portfólio da vitrine
- **THEN** as duas linhas trazem o mesmo título, data, trilha e autoria
