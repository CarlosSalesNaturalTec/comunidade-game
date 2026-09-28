# Spec Delta

## ADDED Requirements

### Requirement: A seção de Guerreiros e Guerreiras apresenta cards que rotacionam a cada 5 segundos

A App 06 SHALL apresentar, no recorte sociedade civil, a seção **Guerreiros e Guerreiras** com
os cards de quem tem autorização vigente, e os cards SHALL **rotacionar a cada 5 segundos**. A
rotação SHALL parar quando o aparelho declarar `prefers-reduced-motion`, e NEVER SHALL ser a
**única via** ao conteúdo: quem não espera a rotação SHALL alcançar os mesmos Guerreiros e
Guerreiras pela navegação da própria seção. (`RF-03-02`, `RF-03-04`, documento 15 §§5, 8.1)

#### Scenario: Os cards rotacionam sozinhos

- **WHEN** o visitante abre a vitrine e permanece na seção de Guerreiros e Guerreiras
- **THEN** os cards trocam a cada 5 segundos, sem que ele acione nada

#### Scenario: Quem pede menos movimento não vê rotação

- **WHEN** o aparelho do visitante declara preferência por movimento reduzido
- **THEN** os cards não rotacionam, e todos seguem alcançáveis

#### Scenario: A rotação não é a única via ao conteúdo

- **WHEN** o visitante quer ver um card que ainda não entrou na rotação
- **THEN** ele o alcança pela navegação da seção, sem esperar a troca

### Requirement: Cada card abre a página individual, em endereço próprio

Cada card SHALL abrir a **página individual** do Guerreiro(a), em **endereço próprio**,
compartilhável e alcançável diretamente. A página SHALL detalhar a trajetória nas trilhas, os
badges e níveis por poder e o portfólio de criações originais com a autoria, na composição do
documento 11 §8.2. (`RF-03-03`, PRD-03 §5.1)

#### Scenario: O card leva à página

- **WHEN** o visitante aciona um card de Guerreiro(a)
- **THEN** a página individual daquele Guerreiro(a) abre, em endereço próprio

#### Scenario: O endereço direto resolve

- **WHEN** alguém abre diretamente o endereço da página de um Guerreiro(a) com autorização
  vigente
- **THEN** a página abre com a composição do documento 11 §8.2

### Requirement: Card e página exibem só avatar, nick, badges, poderes e desempenho

O card e a página do Guerreiro(a) SHALL exibir **avatar, nick, badges, poderes com níveis e
desempenho**, mais as criações originais que a variante do documento 11 §8.2 pede. NEVER SHALL
exibir imagem real, nome civil, rede social, canal de contato ou qualquer outro dado da criança,
em tela nenhuma da vitrine. A vitrine NEVER SHALL oferecer canal de contato com o Guerreiro(a)
ou com a família dele. (`RF-03-05`, `RF-03-06`, `RN-03-04`, `RN-03-05`, invariantes 10 e 12 do
documento 99 §6)

Faltando à leitura o que a variante exige, a carta NEVER SHALL ser apresentada pela metade: a
tela SHALL dizer em uma frase o que tem, como o documento 11 §8.2 determina.

#### Scenario: O card mostra só o que é permitido

- **WHEN** o visitante vê um card de Guerreiro(a)
- **THEN** ele vê avatar, nick, badges, poderes e desempenho, e nenhuma imagem real, nome civil,
  rede social ou contato

#### Scenario: A página não abre canal de contato

- **WHEN** o visitante percorre a página individual inteira
- **THEN** nenhuma tela oferece falar com o Guerreiro(a) ou com a família dele

#### Scenario: Carta incompleta não se apresenta

- **WHEN** a leitura não devolve o que a variante Guerreiro(a) exige
- **THEN** a carta não é apresentada, e a tela diz em uma frase o que tem

### Requirement: A busca é por nick exato, sem lista, sugestão ou completação

A App 06 SHALL oferecer busca por **nick exato**, e NEVER SHALL oferecer sugestão, completação,
lista de nicks ou contagem de resultados parecidos. Havendo autorização vigente, a busca SHALL
levar à página pública daquele Guerreiro(a). (`RF-03-11`, `RF-03-12`, `RN-03-06`, PRD-03 §5.6)

#### Scenario: Nick exato leva à página

- **WHEN** o visitante digita o nick exato de um Guerreiro(a) com autorização vigente
- **THEN** a página pública dele abre

#### Scenario: A busca não sugere nem completa

- **WHEN** o visitante digita parte de um nick
- **THEN** nenhuma sugestão, completação ou lista de nicks é apresentada

### Requirement: Nick inexistente e nick sem autorização recebem a mesma resposta

A App 06 SHALL apresentar **a mesma resposta** de "não encontrado" para nick inexistente e para
nick sem autorização de divulgação vigente, sem revelar qual dos dois casos ocorreu — na busca e
no endereço direto da página. (`RF-03-11`, `RN-03-07`, PRD-03 §§5.6, 5.7)

#### Scenario: Os dois casos respondem igual

- **WHEN** o visitante busca um nick que não existe, e depois um nick sem autorização vigente
- **THEN** as duas respostas são idênticas, e nenhuma diz qual caso ocorreu

#### Scenario: O endereço direto também não distingue

- **WHEN** alguém abre o endereço da página de um nick sem autorização vigente
- **THEN** a tela responde "não encontrado", como responderia a um nick inexistente

### Requirement: Quem não tem autorização vigente não aparece, e a revogação o retira na leitura seguinte

A App 06 NEVER SHALL exibir em card, página, portfólio ou ranking um Guerreiro(a) sem
autorização de divulgação vigente. Revogada a autorização, ele SHALL desaparecer das quatro
superfícies **na leitura seguinte**, e o endereço direto da página dele SHALL responder "não
encontrado". A vitrine NEVER SHALL guardar em cache no aparelho o que leu de um Guerreiro(a), de
modo que a revogação não sobreviva à leitura seguinte. (`RF-03-13`, `RF-03-14`, `RN-03-02`,
`RN-03-03`, `RN-03-22`, PRD-03 §5.7)

#### Scenario: Sem autorização, não aparece em lugar nenhum

- **WHEN** um Guerreiro(a) não tem autorização vigente
- **THEN** ele não está em card, página, portfólio nem ranking, nem por endereço direto

#### Scenario: A revogação vale na leitura seguinte

- **WHEN** o responsável revoga a autorização e o visitante recarrega a vitrine
- **THEN** o Guerreiro(a) já não aparece em nenhuma das quatro superfícies

#### Scenario: A criação em equipe permanece com os demais autores

- **WHEN** um dos creditados de uma criação em equipe tem a autorização revogada
- **THEN** a vitrine apresenta o que o núcleo devolver, sem citar o revogado

### Requirement: A repetição da busca encontra espera crescente explicada, sem CAPTCHA nem cadastro

Freada a origem pela repetição da busca por nick, a App 06 SHALL explicar em **linguagem
simples** o motivo e **quanto tempo falta esperar**, com o tempo que o núcleo devolveu. NEVER
SHALL pedir CAPTCHA, cadastro ou login para seguir, e NEVER SHALL guardar no aparelho qualquer
marca de quem foi freado. (`RF-03-36`, `RF-03-37`, `RN-03-08`, `RN-03-34`, PRD-03 §§5.6, 12)

#### Scenario: A espera é explicada

- **WHEN** o visitante repete a busca por nick até ser freado
- **THEN** a tela diz por que houve a espera e quanto tempo falta, em linguagem simples

#### Scenario: A espera não pede nada do visitante

- **WHEN** o visitante está esperando o freio passar
- **THEN** nenhuma tela pede CAPTCHA, cadastro ou login

### Requirement: O portfólio público exibe as criações autorizadas com trilha, data e autoria

A App 06 SHALL exibir o **portfólio** das criações originais autorizadas, cada uma com a
**trilha** de que nasceu, a **data** em que foi validada e a **autoria por nick** de cada
creditado. NEVER SHALL exibir criação cujo creditado não tenha autorização vigente. O portfólio
SHALL sair **sem título** enquanto a criação original não tiver esse campo no modelo. (`RF-03-08`,
`RN-03-02`, decisão do fundador, 2026-09-28)

#### Scenario: A criação aparece com trilha, data e autoria

- **WHEN** o visitante abre o portfólio
- **THEN** cada criação traz a trilha, a data de validação e o nick de cada autor creditado

#### Scenario: O portfólio não exibe quem não autorizou

- **WHEN** uma criação tem creditado sem autorização vigente
- **THEN** ela não aparece no portfólio

### Requirement: O ranking público exibe só pontos regulares e só quem autorizou

A App 06 SHALL exibir o ranking público com **apenas pontos regulares** e **apenas** Guerreiros
e Guerreiras com autorização de divulgação vigente. NEVER SHALL exibir ponto extra, saldo de
moedas ou valor em reais no ranking. (`RF-03-09`, `RN-03-02`, invariante 16 do documento 99 §6)

#### Scenario: O ranking é de ponto regular

- **WHEN** o visitante abre o ranking
- **THEN** a pontuação exibida é a de pontos regulares, e nenhuma outra

#### Scenario: Quem não autorizou não está no ranking

- **WHEN** um Guerreiro(a) sem autorização vigente teria posição no ranking
- **THEN** ele não aparece, e a numeração exibida não deixa buraco

### Requirement: A seção de poderes apresenta cada poder com as trilhas dele

A App 06 SHALL apresentar a seção **poderes**, com cada poder e as **trilhas** vinculadas a ele,
e a página do poder com as mesmas trilhas. Os **Mestres responsáveis** do documento 11 §8.2
NEVER SHALL ser prometidos nem apresentados vazios enquanto a rota de Mestres não existir: a
seção sai sem eles. (`RF-03-02`, decisão do fundador, 2026-09-28)

#### Scenario: O poder aparece com as trilhas

- **WHEN** o visitante abre a seção de poderes
- **THEN** cada poder aparece com as trilhas vinculadas a ele

#### Scenario: A seção não promete o que ainda não tem

- **WHEN** o visitante abre a página de um poder
- **THEN** nenhum espaço vazio ou promessa de Mestres responsáveis é apresentado
