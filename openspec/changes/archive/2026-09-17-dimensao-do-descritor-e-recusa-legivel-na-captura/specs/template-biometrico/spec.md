## MODIFIED Requirements

### Requirement: Ao núcleo chega descritor, nunca imagem

O núcleo SHALL aceitar apenas o **descritor** gerado no aparelho e SHALL NOT aceitar fotografia
em nenhuma rota. O descritor SHALL ser recusado com 422 quando não tiver o formato esperado. O
_template_ SHALL servir exclusivamente para identificar o Guerreiro(a) — presença e autenticação
—, e nenhuma rota SHALL usá-lo para outra finalidade. (`RF-01-05`, `RN-01-15`, PRD-01 §§3.2, 11)

A **dimensão esperada** do descritor é a da biblioteca de reconhecimento facial decidida no
documento 03 §3.3, e SHALL ser fixa no núcleo, com a origem declarada junto dela. Ela NEVER
SHALL ser parâmetro de implantação: não admite calibração — ou casa com o que a aplicação gera,
ou nenhuma captura é aceita. O ambiente NEVER SHALL poder declará-la, e trocá-la é trocar de
biblioteca. (`RF-01-05`, documento 03 §3.3, decisão do fundador, 2026-09-17)

O **limiar de comparação** segue no caminho oposto, e permanece parâmetro de implantação
calibrado no encontro real (documento 09, "Parâmetros da entrada do Guerreiro(a)").

#### Scenario: Envio de imagem é recusado

- **WHEN** chega uma requisição com fotografia de Guerreiro(a) em qualquer rota do núcleo
- **THEN** o núcleo a recusa e nada é gravado

#### Scenario: Descritor malformado é recusado

- **WHEN** chega um descritor fora do formato esperado
- **THEN** o núcleo responde 422 indicando o campo em falta e nenhum _template_ é gravado

#### Scenario: O descritor que a aplicação gera é aceito

- **WHEN** chega o descritor gerado pela biblioteca do documento 03 §3.3, na dimensão dela
- **THEN** o núcleo o aceita, e a dimensão conferida é a mesma em todo ambiente

#### Scenario: A dimensão não se declara no ambiente

- **WHEN** se procura uma variável de ambiente que fixe a dimensão do descritor
- **THEN** nenhuma existe, e o valor conferido vem do próprio núcleo
