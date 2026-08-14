## Purpose

O App 04 monta o personagem a partir do progresso real do Guerreiro(a) e não devolve nada ao
núcleo. Esta capacidade fixa esse contrato como fronteira verificável: o que o jogo lê, o
elenco que ele alcança e — sobretudo — a **ausência** de qualquer rota pela qual um jogo
pudesse creditar, debitar ou registrar resultado de partida.

## Requirements

### Requirement: O jogo lê o progresso do Guerreiro(a) para montar o personagem

O núcleo SHALL expor em leitura, mediante chave de aplicação e **sem credencial de persona**, o
progresso que o jogo usa para montar o personagem: **pontos regulares**, **acumulado de pontos
extras**, **poderes**, **badges** e **níveis**. A leitura SHALL responder pela mesma projeção
pública da vitrine — avatar e nick —, sem nome, contato, imagem ou valor em reais.
(`RF-01-22`, `RF-01-02`, `RN-01-10`, `RN-01-11`, invariante 8 do documento 99 §6)

#### Scenario: O jogo lê o progresso para montar o personagem

- **WHEN** o App 04 consulta o progresso de um Guerreiro(a) do elenco, com chave válida
- **THEN** o núcleo devolve pontos regulares, acumulado de pontos extras, poderes, badges e
  níveis, com avatar e nick

#### Scenario: A leitura do jogo dispensa credencial de persona

- **WHEN** a consulta do jogo chega sem token de sessão
- **THEN** o núcleo responde normalmente, porque ninguém se identifica para jogar

#### Scenario: Sem chave o jogo não lê

- **WHEN** a consulta do jogo chega sem chave de aplicação válida
- **THEN** o núcleo responde 401

### Requirement: O elenco do jogo é o mesmo público da vitrine

O núcleo SHALL montar o elenco alcançável pelo jogo **estritamente** com os Guerreiros e
Guerreiras que têm autorização de divulgação vigente — o mesmo portão da vitrine. Guerreiro(a)
sem autorização NEVER SHALL ser alcançável por rota de jogo, nem por consulta direta ao
progresso dele. (`RN-01-10`, invariantes 8 e 12 do documento 99 §6)

#### Scenario: Elenco traz só quem autorizou

- **WHEN** o jogo pede o elenco disponível
- **THEN** a resposta traz apenas Guerreiros e Guerreiras com autorização de divulgação vigente

#### Scenario: Progresso de quem não autorizou não é alcançável

- **WHEN** o jogo consulta o progresso de um Guerreiro(a) sem autorização vigente
- **THEN** o núcleo responde 404, com corpo idêntico ao do Guerreiro(a) inexistente

#### Scenario: Revogar tira do elenco

- **WHEN** o responsável revoga a autorização de divulgação de um Guerreiro(a)
- **THEN** a consulta seguinte do jogo já não o alcança

### Requirement: Do ponto extra o jogo lê o acumulado, e o saldo disponível nunca sai

O núcleo SHALL expor ao jogo **apenas o acumulado** de pontos extras, que só cresce. O **saldo
disponível** NEVER SHALL aparecer em nenhuma resposta de rota de jogo, em nenhum campo,
agregado ou derivado do qual se possa reconstituí-lo. Trocar ponto extra por recompensa avulsa
NEVER SHALL enfraquecer o personagem. (`RF-01-59`, `RN-01-41`, `RN-01-39`, invariantes 8 e 23
do documento 99 §6)

#### Scenario: O jogo lê o acumulado

- **WHEN** o jogo consulta o progresso de um Guerreiro(a) que tem pontos extras
- **THEN** a resposta traz o acumulado de pontos extras

#### Scenario: Nenhuma resposta de jogo traz o saldo disponível

- **WHEN** qualquer rota de jogo responde
- **THEN** nenhum campo da resposta é o saldo disponível nem permite deduzi-lo

#### Scenario: Trocar não enfraquece o personagem

- **WHEN** um Guerreiro(a) troca ponto extra por recompensa avulsa e o jogo consulta o
  progresso dele em seguida
- **THEN** o acumulado lido pelo jogo é o mesmo de antes da troca

### Requirement: Não existe rota de escrita para jogos

O núcleo NEVER SHALL oferecer a um jogo rota que credite ponto, debite ponto, conceda badge,
altere nível ou registre resultado de partida. A tentativa SHALL responder **404**, porque a
rota não existe — não 403, que admitiria a existência de uma rota sem permissão. Ponto SHALL
vir apenas de realização registrada pelas rotas de domínio. (`RF-01-22`, `RN-01-06`,
invariante 8 do documento 99 §6, PRD-01 §12)

#### Scenario: Não há rota de crédito para jogo

- **WHEN** se procura no núcleo uma rota pela qual um jogo credite pontos
- **THEN** nenhuma existe

#### Scenario: Tentativa de crédito pelo jogo devolve 404

- **WHEN** uma chamada tenta creditar ponto por um caminho de jogo
- **THEN** o núcleo responde 404

#### Scenario: Não há registro de resultado de partida vindo do jogo

- **WHEN** se procura no núcleo uma rota pela qual um jogo registre o resultado de uma partida
- **THEN** nenhuma existe, e o progresso do Guerreiro(a) permanece como as rotas de domínio o
  deixaram
