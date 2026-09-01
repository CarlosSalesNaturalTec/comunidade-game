## MODIFIED Requirements

### Requirement: O Apoiador lê os próprios aportes e o próprio Poder Sustentador, sem escrita

O núcleo SHALL responder `GET /meus-aportes` à persona **Apoiador** em sessão, devolvendo os
aportes dela e o Poder Sustentador dela. A rota SHALL alcançar **somente** os aportes da
persona em sessão. Cada aporte SHALL sair com a **data**, o **nome do tipo de recurso**, o
**destino** e o valor **em moedas**, e o Poder Sustentador SHALL sair como **total acumulado em
moedas**. A declaração ainda pendente NÃO SHALL aparecer nesta rota: enquanto não homologada
ela não é aporte, e é lida na rota da situação das declarações. A leitura SHALL ser somente de
consulta: esta capacidade NÃO SHALL expor rota de escrita sobre aporte algum. O valor de origem
em **reais** SHALL ficar fora da resposta — o acesso a ele é da gestão (PRD-07 §11).
(`RF-07-17`, `RN-07-05`, `RF-01-16`, `RF-14-21`, `RF-14-22`, `RF-14-23`, `RN-14-09`, PRD-07
§§9, 11, PRD-14 §6.3)

#### Scenario: O Apoiador vê os aportes dele

- **WHEN** um Apoiador em sessão consulta os próprios aportes
- **THEN** o núcleo devolve os aportes dele, cada um com data, nome do tipo de recurso, destino
  e valor em moedas, e o Poder Sustentador dele como total acumulado em moedas

#### Scenario: O aporte alheio fica de fora

- **WHEN** um Apoiador em sessão consulta os próprios aportes e outro Apoiador também tem
  aportes registrados
- **THEN** a resposta traz apenas os aportes da persona em sessão

#### Scenario: A declaração pendente não aparece como aporte

- **WHEN** um Apoiador em sessão consulta os próprios aportes e tem uma declaração pendente
- **THEN** a resposta não a traz, e o Poder Sustentador dele não a soma

#### Scenario: Sem sessão de persona a rota não responde

- **WHEN** a consulta chega com chave de aplicação válida e sem token de sessão
- **THEN** o núcleo recusa, porque a rota exige a credencial da persona

#### Scenario: A leitura não abre edição

- **WHEN** um Apoiador tenta alterar um aporte próprio por esta capacidade
- **THEN** não há rota que o faça: a capacidade é somente de leitura

#### Scenario: Nenhum campo traz reais

- **WHEN** a lista de "Meus aportes" é lida
- **THEN** nenhum campo da resposta traz o valor de origem em reais
