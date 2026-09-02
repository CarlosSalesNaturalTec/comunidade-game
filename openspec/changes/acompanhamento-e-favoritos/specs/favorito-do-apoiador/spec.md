## Purpose

Governa o favorito do Apoiador: o alvo que ele alcança — Guerreiro(a) pelo nick exato que a
família cedeu, Mestre pela persona pública dele —, a recusa indistinta que impede descobrir
quem existe, a novidade derivada dos últimos 30 dias e as salvaguardas que mantêm o favorito
como leitura, nunca como canal com a criança.

## ADDED Requirements

### Requirement: O favorito é do Apoiador em sessão, e alcança somente os próprios

O núcleo SHALL expor rotas em que a persona de **Apoiador em sessão** lê, cria e remove os
**próprios** favoritos, sem identificador de outro Apoiador no caminho ou em parâmetro.
Persona de outro papel SHALL receber **403**. A remoção de favorito que não é do Apoiador em
sessão SHALL receber **404**, indistinto do favorito inexistente. (`RF-14-49`, `RF-14-52`,
`RF-14-55`, PRD-14 §§4, 9)

#### Scenario: O Apoiador lê apenas os favoritos que são dele

- **WHEN** um Apoiador em sessão lê os próprios favoritos, e outro Apoiador tem favoritos
  gravados
- **THEN** a resposta traz só os favoritos de quem está em sessão, sem nenhum do outro

#### Scenario: Persona de outro papel é recusada

- **WHEN** um Mestre, um responsável, um Guerreiro(a) ou um Admin chama qualquer rota de
  favorito
- **THEN** o núcleo responde 403, e nenhum favorito é criado, lido ou removido

#### Scenario: Remover favorito de outro Apoiador é indistinto de remover o inexistente

- **WHEN** um Apoiador pede a remoção de um favorito que é de outro Apoiador
- **THEN** o núcleo responde 404, na mesma resposta que daria a um favorito inexistente

### Requirement: O favorito de Guerreiro(a) se faz por nick exato, e a recusa é sempre a mesma

O núcleo SHALL aceitar o favorito de Guerreiro(a) **apenas pelo nick exato** informado pelo
Apoiador, resolvido contra o portão de divulgação da leitura pública. Nick **inexistente** e
nick de quem **não tem divulgação autorizada vigente** SHALL receber a **mesma resposta 404**,
com a mesma mensagem, sem qualquer diferença de corpo, cabeçalho ou tempo de resposta que
permita distinguir os dois casos. Nenhuma rota SHALL confirmar, direta ou indiretamente, que um
nick existe. (`RF-14-49`, `RF-14-51`, `RN-14-23`, PRD-14 §11)

#### Scenario: Nick exato de quem autorizou vira favorito

- **WHEN** o Apoiador informa o nick exato de um Guerreiro(a) com divulgação autorizada vigente
- **THEN** o favorito é gravado com o alvo, e a leitura seguinte o traz por avatar e nick

#### Scenario: Nick inexistente e nick sem autorização devolvem a mesma resposta

- **WHEN** o Apoiador informa um nick que não existe, e depois o nick de um Guerreiro(a) sem
  divulgação autorizada vigente
- **THEN** as duas respostas são 404 idênticas, e nenhuma delas revela qual dos dois casos
  ocorreu

#### Scenario: Nick aproximado não alcança ninguém

- **WHEN** o Apoiador informa um nick parecido com o de um Guerreiro(a) existente, mas não
  igual
- **THEN** o núcleo responde o mesmo 404, sem sugestão, aproximação ou correção

### Requirement: Nenhuma rota de favorito lista, sugere ou completa nick

O núcleo NEVER SHALL oferecer, em rota de favorito, listagem de nicks, busca parcial, sugestão,
autocompletar, contagem de resultados ou qualquer parâmetro que aceite fragmento de nick. O
único caminho é o nick exato, e a resposta é o favorito criado ou o 404 indistinto.
(`RF-14-50`, `RN-14-23`)

#### Scenario: Não existe rota de busca de nick

- **WHEN** se procura entre as rotas de favorito uma que devolva nicks a partir de fragmento,
  prefixo ou aproximação
- **THEN** nenhuma existe

### Requirement: O Mestre é favoritado pela persona pública dele

O núcleo SHALL aceitar o favorito de **Mestre** pela persona dele. Persona que não é Mestre,
ou que não existe, SHALL receber **404**. O Mestre SHALL aparecer na leitura do favorito por
**nome e avatar**, sem dado de contato. (`RF-14-52`, `RN-14-20`)

#### Scenario: Mestre vira favorito

- **WHEN** o Apoiador favorita um Mestre pela persona dele
- **THEN** o favorito é gravado, e a leitura seguinte traz o Mestre por nome e avatar, sem
  e-mail, telefone ou qualquer outro contato

#### Scenario: Persona que não é Mestre é recusada

- **WHEN** o Apoiador tenta favoritar como Mestre uma persona de outro papel, ou uma que não
  existe
- **THEN** o núcleo responde 404

### Requirement: A novidade do favorito é derivada e dura 30 dias

O núcleo SHALL devolver, junto de cada favorito, as **novidades dos últimos 30 dias**, contados
da **data do fato**. A novidade SHALL ser **derivada** das entidades que produzem o fato, nunca
armazenada como registro próprio. Os fatos SHALL ser, do Guerreiro(a) favoritado: **criação
original publicada**, **badge novo** e **nível novo**; e do Mestre favoritado: **trilha nova
publicada**. Fato com mais de 30 dias SHALL sair do destaque sem apagar nada.

O quinto fato do `RF-14-53` — **resultado de batalha** — depende do PRD-10, que não tem
entidade no núcleo; ele entra com o PRD-10 (decisão do fundador, 2026-09-02). (`RF-14-53`,
`RN-14-25`, PRD-14 §8)

#### Scenario: Criação original publicada aparece em destaque

- **WHEN** um Guerreiro(a) favoritado tem criação original publicada há menos de 30 dias
- **THEN** a leitura do favorito traz o fato em destaque, com a data dele

#### Scenario: Badge e nível novos aparecem em destaque

- **WHEN** um Guerreiro(a) favoritado recebe badge novo e nível novo dentro dos últimos 30 dias
- **THEN** a leitura do favorito traz os dois fatos, cada um com a sua data

#### Scenario: Trilha publicada pelo Mestre aparece em destaque

- **WHEN** um Mestre favoritado publica trilha nova há menos de 30 dias
- **THEN** a leitura do favorito traz o fato, e a trilha de outro Mestre não aparece

#### Scenario: O fato antigo sai do destaque

- **WHEN** o fato de um favorito completa mais de 30 dias
- **THEN** ele deixa de aparecer na leitura do favorito, e nada é apagado das entidades que o
  produziram

#### Scenario: A novidade não é registro próprio

- **WHEN** se procura tabela, rota ou campo que grave a novidade do favorito
- **THEN** nenhum existe: a novidade sai das entidades que datam o fato

### Requirement: Favoritar é leitura, e nunca amplia o que o Apoiador enxerga

Favoritar NEVER SHALL abrir canal de contato, avisar o Guerreiro(a) ou a família, gerar
notificação por e-mail ou por qualquer meio fora da aplicação, nem dar ao Apoiador acesso a
dado que ele já não veria em público. A saída de Guerreiro(a) na leitura do favorito SHALL ser
**avatar e nick**, e nada além. Nenhuma rota de favorito SHALL devolver nome real, endereço,
foto, contato ou vínculo familiar. (`RF-14-54`, `RN-14-20`, `RN-14-24`, `RN-14-27`, invariantes
9 e 10 do documento 99 §6)

#### Scenario: Favoritar não produz aviso nem canal

- **WHEN** um Apoiador favorita um Guerreiro(a)
- **THEN** nenhum aviso é gerado para o Guerreiro(a) ou para a família, nenhuma mensagem sai da
  plataforma, e nenhuma rota de contato passa a existir

#### Scenario: A saída do favorito é avatar e nick

- **WHEN** a leitura do favorito devolve um Guerreiro(a)
- **THEN** ela traz avatar e nick, e nenhum outro dado pessoal

#### Scenario: O favorito não amplia o alcance do Apoiador

- **WHEN** se compara o que a leitura do favorito devolve com o que a leitura pública já
  devolve do mesmo Guerreiro(a)
- **THEN** não há nenhum dado a mais no favorito

### Requirement: O favorito de quem saiu do público desaparece da leitura

O núcleo SHALL omitir da leitura do favorito o Guerreiro(a) cuja autorização de divulgação
**deixou de ser vigente**, sem lacuna, contagem ou marca que denuncie a omissão, do mesmo modo
que a leitura pública já omite. O registro do favorito SHALL permanecer, e o Guerreiro(a) SHALL
voltar à leitura se a autorização voltar a vigorar. (`RF-14-48`, `RN-14-24`, `RN-01-10`,
invariante 8 do documento 99 §6)

#### Scenario: Revogar a autorização tira o favoritado da leitura

- **WHEN** um Guerreiro(a) favoritado tem a autorização de divulgação revogada
- **THEN** ele deixa de aparecer na leitura do favorito, sem posição vazia, contagem ou aviso
  de que algo foi omitido

#### Scenario: A autorização de volta traz o favoritado de volta

- **WHEN** a autorização de divulgação do Guerreiro(a) favoritado volta a vigorar
- **THEN** ele reaparece na leitura do favorito, com o mesmo registro de antes

### Requirement: O Apoiador remove o favorito a qualquer tempo

O núcleo SHALL remover o favorito por ato do Apoiador em sessão, a qualquer tempo, sem prazo,
sem carência e sem aprovação de ninguém. A remoção NEVER SHALL gerar aviso ao Guerreiro(a), à
família ou ao Mestre. Favoritar de novo o mesmo alvo SHALL ser aceito. (`RF-14-55`, `RN-14-24`)

#### Scenario: Remover é imediato e silencioso

- **WHEN** o Apoiador remove um favorito
- **THEN** ele some da leitura seguinte, e nenhum aviso é gerado para o alvo

#### Scenario: Favoritar duas vezes o mesmo alvo não duplica

- **WHEN** o Apoiador favorita o mesmo alvo que já favoritou
- **THEN** continua existindo um só favorito daquele alvo, e a resposta não revela nada além
  disso
