## ADDED Requirements

### Requirement: A área Pontos de Apoio apresenta o limiar de comparação medido em cada espaço

A App 03 SHALL apresentar ao Admin, na área Pontos de Apoio, o **limiar de comparação vigente**
de cada ponto de apoio, com **quem mediu**, **quando** e as **duas séries de distâncias** da
medição que o produziu. (`RF-02-109`, `RF-01-73`)

A aplicação SHALL **destacar** os pontos de apoio **sem limiar medido**, dizendo em linguagem
simples o que aquilo significa no encontro: ali o reconhecimento facial não confere ninguém, e
todo Guerreiro(a) entra pela confirmação de Mestre ou Admin. (`RF-02-109`, `RN-01-56`)

A tela SHALL ser de **consulta**: ela NEVER SHALL oferecer edição do limiar. O valor nasce de
uma medição no aparelho do encontro, e medir de novo é o caminho de corrigi-lo. (`RF-02-109`,
`RF-04-66`)

#### Scenario: O limiar vigente aparece com a origem

- **WHEN** o Admin abre um ponto de apoio já medido
- **THEN** a tela apresenta o limiar vigente, quem mediu, quando e as duas séries da medição

#### Scenario: Ponto de apoio sem limiar é destacado

- **WHEN** um ponto de apoio ainda não teve limiar medido
- **THEN** a tela o destaca e explica que ali ninguém é reconhecido e a entrada é por
  confirmação humana

#### Scenario: A tela não edita o limiar

- **WHEN** o Admin procura na tela um caminho para digitar ou corrigir o limiar
- **THEN** nenhum existe, e a tela indica que corrigir é medir de novo na App 01

#### Scenario: Medição nova aparece com a anterior preservada

- **WHEN** um ponto de apoio recebe uma medição nova
- **THEN** a tela passa a apresentar o limiar novo, e a medição anterior segue consultável
