# Spec Delta

## MODIFIED Requirements

### Requirement: A linha do portfólio abre a produção na própria linha

A App 06 SHALL permitir que o visitante **abra a produção** de um item do acervo **na própria
linha**, sem sair da seção e sem endereço novo: a criação não tem página individual. Ao abrir,
SHALL exibir a **imagem**, o **áudio**, o **vídeo** ou o **texto**; o **link externo** SHALL
sair como link de saída e o **arquivo**, como transferência. Os bytes SHALL ser pedidos à rota
pública **da fonte do item** — criação original, comprovação do prático ou customização do kit.
Fechar SHALL devolver a linha ao estado recolhido. (`RF-03-85`, `RF-03-88`, `RF-03-03`)

A **imagem** aberta na linha SHALL ser um controle que, acionado por toque, clique ou teclado,
a abre **inteira, sem corte, no maior tamanho que a tela comporta**, sobre a página; fecha pelo
botão **"Fechar"**, pela tecla `Esc` e pelo toque fora dela, devolvendo o foco à imagem.
Ampliar NEVER SHALL buscar os bytes de novo, recolher a linha nem gravar coisa alguma no
aparelho, e o **vídeo** NEVER SHALL ganhar a ampliação. (`RF-03-85`, `RN-03-22`, decisão do
fundador de 2026-11-14)

#### Scenario: A imagem abre na linha

- **WHEN** o visitante abre a produção de um item do tipo imagem
- **THEN** a imagem aparece na própria linha, com texto alternativo, e a lista continua visível

#### Scenario: Tocar na imagem a abre em tela cheia

- **WHEN** o visitante toca ou clica na imagem aberta na linha de um item do acervo, de
  qualquer das três fontes
- **THEN** a imagem abre inteira, sem corte, no maior tamanho que a tela comporta, sem nova
  busca ao núcleo

#### Scenario: A imagem ampliada fecha e devolve o foco

- **WHEN** a imagem está ampliada e o visitante aciona "Fechar", tecla `Esc` ou toca fora dela
- **THEN** a imagem ampliada fecha, o foco volta à imagem na linha e a produção segue aberta

#### Scenario: O vídeo não amplia

- **WHEN** o visitante abre a produção de um item do tipo vídeo
- **THEN** o vídeo fica na moldura com os controles nativos, sem controle de ampliar

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
