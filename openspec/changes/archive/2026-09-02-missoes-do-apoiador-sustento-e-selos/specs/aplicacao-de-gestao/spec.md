## ADDED Requirements

### Requirement: A App 03 publica a missão do Apoiador a partir de uma necessidade em aberto

A aplicação SHALL oferecer ao Admin, na área Recursos, a publicação da missão do Apoiador
escolhendo uma **necessidade de recurso em aberto** e declarando o **nível de necessidade**, o
**título**, **o que se pede**, a **quantidade**, o **prazo** e o **selo que rende**. Recusada a
publicação pelo núcleo por faltar necessidade por trás, a tela SHALL apresentar a recusa em
linguagem simples, sem erro cru. A aplicação NEVER SHALL oferecer publicação de missão a quem
não é Admin. (`RF-02-102`, `RF-02-103`, `RN-02-31`)

#### Scenario: O Admin publica a missão pela tela

- **WHEN** o Admin escolhe uma necessidade em aberto e preenche nível, título, o que se pede,
  quantidade, prazo e selo
- **THEN** a missão é publicada e passa a aparecer entre as abertas

#### Scenario: A recusa aparece em linguagem simples

- **WHEN** o núcleo recusa a publicação por faltar necessidade publicada por trás
- **THEN** a tela apresenta o motivo em linguagem simples e mantém o que foi preenchido

#### Scenario: Quem não é Admin não alcança a publicação

- **WHEN** um Mestre abre a área Recursos
- **THEN** a aplicação não oferece o caminho de publicar missão

### Requirement: A gestão acompanha as missões publicadas e despublica a errada

A aplicação SHALL listar ao Admin as missões publicadas em **qualquer situação** — aberta,
concluída ou vencida —, cada uma com **o que já foi coberto**, **o que falta** e a situação, e
SHALL oferecer a **despublicação** da que foi publicada por engano. A tela SHALL declarar que
despublicar não estorna aporte já homologado. Recusada a despublicação por a missão já estar
concluída, a tela SHALL apresentar a recusa. A lista NEVER SHALL identificar quem cobriu cada
missão. (`RF-02-104`, `RF-02-105`, `RN-14-34`)

#### Scenario: A lista mostra o coberto, o que falta e a situação

- **WHEN** o Admin abre a lista das missões publicadas
- **THEN** cada missão aparece com o coberto, o que falta e a situação, e nenhum nick de quem
  cobriu

#### Scenario: A despublicação avisa que nada é estornado

- **WHEN** o Admin escolhe despublicar uma missão que já recebeu aporte homologado
- **THEN** a tela declara que o aporte homologado permanece, e a missão sai das listas

#### Scenario: A missão concluída não se despublica

- **WHEN** o Admin tenta despublicar uma missão já concluída
- **THEN** a tela apresenta a recusa e a missão segue concluída
