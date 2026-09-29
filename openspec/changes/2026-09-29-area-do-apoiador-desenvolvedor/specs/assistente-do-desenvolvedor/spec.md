# Spec Delta

## Purpose

A consulta pública ao assistente da Área do Apoiador Desenvolvedor — a conversa de quem quer
construir sobre a API, respondida só a partir da documentação, do README e do contrato OpenAPI
do próprio projeto, sem login, sem dado do visitante e sem guarda nenhuma da conversa.

## ADDED Requirements

### Requirement: A consulta ao assistente do Desenvolvedor é pública e não se identifica

O núcleo SHALL aceitar a consulta ao assistente do Desenvolvedor **sem credencial de persona**,
como as demais superfícies públicas da vitrine: quem chama é a aplicação, pela chave dela, e o
visitante segue anônimo (`RN-03-29`, `RN-03-33`).

A consulta NEVER SHALL pedir, aceitar ou devolver dado pessoal do visitante — nome, contato,
identificador ou qualquer campo que o descreva. Campo dessa natureza no envio SHALL ser
recusado (`RF-03-71`).

#### Scenario: A pergunta chega sem credencial de persona

- **WHEN** um visitante anônimo envia a pergunta pela Área do Apoiador Desenvolvedor
- **THEN** o núcleo responde, e nenhuma credencial de persona é exigida

#### Scenario: O envio com dado do visitante é recusado

- **WHEN** chega uma consulta com campo de nome, contato ou identificador do visitante
- **THEN** o núcleo a recusa e nada é respondido nem gravado

### Requirement: Nada da conversa é guardado

A consulta ao assistente do Desenvolvedor NEVER SHALL gravar linha nenhuma — nem a pergunta,
nem a resposta, nem a origem, nem o momento. Ela NEVER SHALL criar consulta ao assistente, que
é da equipe e do Guerreiro(a). A conversa vive apenas no aparelho do visitante enquanto a
página estiver aberta (PRD-03 §8, `RN-03-15`).

#### Scenario: Recarregar a página perde a conversa

- **WHEN** o visitante conversa com o assistente e recarrega a página
- **THEN** a conversa recomeça do zero, e nada dela foi guardado em lugar nenhum

#### Scenario: Nenhuma tabela recebe a consulta do Desenvolvedor

- **WHEN** o núcleo responde a uma consulta do assistente do Desenvolvedor
- **THEN** nenhuma linha é gravada, e a consulta ao assistente da equipe e do Guerreiro(a)
  permanece intocada

### Requirement: O corpus é fechado na documentação, no README e no contrato OpenAPI

O assistente do Desenvolvedor SHALL responder **apenas a partir do corpus fechado** formado
pela documentação de `docs/`, pelo `README.md` da raiz e pelo contrato OpenAPI do núcleo,
montado **pela esteira a cada implantação** — nenhuma requisição a terceiro acontece no momento
da resposta (documento 03 §8, decisão do fundador de 2026-09-26).

O assistente NEVER SHALL responder de conhecimento próprio nem de fora do corpus (`RF-03-70`,
`RN-03-30`).

O corpus SHALL chegar ao modelo **em recorte por pergunta, com teto declarado**: o núcleo
escolhe, entre os blocos do artefato montado pela esteira, os que atendem à pergunta, até o
teto de caracteres (decisão do fundador de 2026-09-29). O recorte NEVER SHALL trazer texto que
não esteja no artefato.

#### Scenario: A pergunta sobre a arquitetura é respondida pelo corpus

- **WHEN** o visitante pergunta como a plataforma está montada, e a resposta está na
  documentação, no README ou no contrato OpenAPI
- **THEN** o assistente responde a partir daquele material

#### Scenario: O recorte não passa do teto

- **WHEN** a pergunta casa com mais blocos do corpus do que cabe no teto declarado
- **THEN** o que vai ao modelo para no teto, e nenhum texto de fora do artefato entra

#### Scenario: Nenhuma requisição a terceiro monta o corpus na hora da resposta

- **WHEN** o núcleo monta o recorte para responder
- **THEN** ele lê o artefato que a esteira produziu na implantação, e não busca documentação
  em lugar nenhum

### Requirement: Fora do corpus, o assistente diz que não sabe e aponta a documentação

Pergunta cujo assunto não está no corpus SHALL receber a declaração de que o assistente não
sabe, com o caminho da documentação — nunca uma resposta inventada (`RF-03-70`, `RN-03-30`).

#### Scenario: A pergunta fora do corpus recebe "não sei"

- **WHEN** o visitante pergunta sobre assunto que não está na documentação, no README nem no
  contrato OpenAPI
- **THEN** o assistente declara que não sabe e aponta a documentação, sem inventar resposta

### Requirement: Toda mensagem termina com uma pergunta de múltipla escolha

Toda resposta do assistente do Desenvolvedor SHALL terminar com uma **pergunta de múltipla
escolha** sobre o próximo passo a conhecer, com as opções apuradas — inclusive a resposta de
fora do corpus e a última de uma conversa longa (`RF-03-69`, PRD-03 §12).

Resposta do modelo que chegue **sem** as opções SHALL receber o conjunto fixo declarado pelo
núcleo, e nunca sair sem pergunta.

#### Scenario: A resposta traz a pergunta do próximo passo

- **WHEN** o assistente responde qualquer pergunta do visitante
- **THEN** a mensagem termina com uma pergunta de múltipla escolha sobre o que conhecer em
  seguida

#### Scenario: A recusa fora do corpus também termina com a escolha

- **WHEN** o assistente declara que não sabe
- **THEN** a mensagem ainda assim termina com a pergunta de múltipla escolha

#### Scenario: O modelo sem opções não derruba a regra

- **WHEN** o modelo devolve a resposta sem as opções do próximo passo
- **THEN** o núcleo completa com o conjunto fixo, e a mensagem sai com a pergunta

### Requirement: A indisponibilidade do assistente é desfecho declarado, não falha da área

Falha, demora ou resposta fora do formato esperado do modelo SHALL ser devolvida como
**indisponibilidade declarada**, com a causa dita como o que é — nunca disfarçada de recusa do
domínio nem de resposta vazia (`RF-03-72`, documento 99 §6 invariante 25).

Nenhuma consulta SHALL ser gravada por conta da indisponibilidade, porque nenhuma consulta é
gravada em caso nenhum.

#### Scenario: O modelo fora do ar devolve a indisponibilidade

- **WHEN** o modelo falha, demora além do limite ou responde fora do formato esperado
- **THEN** o núcleo devolve a indisponibilidade declarada, e não uma resposta inventada nem uma
  recusa de corpus
