## MODIFIED Requirements

### Requirement: O Guerreiro(a) consulta as suas séries, com o estado e os pontos de cada uma

O núcleo SHALL devolver ao **Guerreiro(a) em sessão** a lista das **suas** séries, cada uma com
o **desafio**, o **local**, a **cadência**, o **estado** e os **pontos que a série está
rendendo** — a soma dos pontos creditados pelos registros válidos dela. A consulta NEVER SHALL
devolver série de outro Guerreiro(a), e persona de outro papel SHALL receber **403**. O estado
devolvido SHALL ser o derivado no momento da consulta.

Cada série SHALL vir acompanhada da **próxima medição** e do **tipo de coleta** que ela mede.
A próxima medição SHALL ser o início do **período de cadência seguinte** ao da última medição
válida, pela mesma régua de período civil com que a interrupção é apurada; a série que ainda
não tem medição válida SHALL declarar o **período corrente** como próxima medição. A série
**interrompida** e a **encerrada** NEVER SHALL declarar próxima medição. O tipo de coleta SHALL
sair com o **nome**, a **forma de registro** e a **unidade** quando houver — o que a aplicação
precisa para pedir a medição na forma certa. Cada série SHALL trazer também a **comunidade do
seu local** — o mesmo dado que a solicitação de local já expõe —, para que a aplicação resolva
o rótulo do local sem uma rota nova. (`RF-05-30`)

A consulta SHALL ser **paginada**, como toda listagem do núcleo: SHALL aceitar **cursor** e
**tamanho de página**, SHALL devolver os itens da página junto do **cursor seguinte** — nulo na
última página — e SHALL recusar com **422** o tamanho acima do teto e o **parâmetro que não
declara**. A ordenação SHALL ser estável, de modo que nenhuma série se repita entre páginas nem
falte a alguma delas. O núcleo SHALL apurar o estado e somar os pontos **apenas das séries da
página**. (`RF-08-17`, `RN-08-04`, `RF-01-28`, `RF-05-30`, `RN-05-10`, PRD-08 §9, PRD-05 §6.4)

#### Scenario: O Guerreiro(a) vê as suas séries com estado e pontos

- **WHEN** um Guerreiro(a) em sessão consulta as suas séries
- **THEN** o núcleo devolve cada série dele com o desafio, o local, a cadência, o estado e a
  soma dos pontos creditados pelos registros válidos daquela série

#### Scenario: A série ativa declara quando é a próxima medição

- **WHEN** um Guerreiro(a) consulta uma série ativa cuja última medição válida caiu no período
  de cadência anterior
- **THEN** o núcleo devolve como próxima medição o início do período de cadência seguinte ao
  daquela medição

#### Scenario: A série sem medição válida espera medição no período corrente

- **WHEN** um Guerreiro(a) consulta uma série ativa que ainda não recebeu nenhuma medição
  válida
- **THEN** o núcleo devolve como próxima medição o início do período de cadência corrente

#### Scenario: A série interrompida não declara próxima medição

- **WHEN** um Guerreiro(a) consulta uma série interrompida ou encerrada
- **THEN** o núcleo devolve a série sem próxima medição, com os pontos já creditados intactos

#### Scenario: A série sai com o tipo de coleta que ela mede

- **WHEN** um Guerreiro(a) consulta as suas séries
- **THEN** cada uma vem com o nome do tipo de coleta, a forma de registro que ele exige e a
  unidade, quando o tipo a declara

#### Scenario: A consulta não alcança série de outro Guerreiro(a)

- **WHEN** um Guerreiro(a) consulta as suas séries e há séries de outros coletores no mesmo
  desafio e local
- **THEN** o núcleo devolve apenas as séries do Guerreiro(a) da sessão

#### Scenario: A consulta reflete a interrupção sem depender de escrita anterior

- **WHEN** um Guerreiro(a) cuja série passou dois períodos sem registro consulta as suas séries
- **THEN** o núcleo devolve aquela série como `interrompida`, ainda que nenhuma escrita tenha
  acontecido desde a última medição

#### Scenario: Mestre não consulta pela rota do Guerreiro(a)

- **WHEN** um Mestre em sessão chama a consulta das séries do Guerreiro(a)
- **THEN** o núcleo responde 403

#### Scenario: A consulta devolve uma página com o cursor seguinte

- **WHEN** um Guerreiro(a) com mais séries do que o tamanho de página pedido consulta as suas
  séries
- **THEN** o núcleo devolve só o tamanho pedido, acompanhado do cursor da página seguinte

#### Scenario: O cursor percorre todas as séries sem repetir nenhuma

- **WHEN** o Guerreiro(a) percorre as páginas seguindo o cursor devolvido até ele vir nulo
- **THEN** o núcleo terá devolvido cada série dele uma única vez, sem repetição e sem falta

#### Scenario: Parâmetro que a rota não declara é recusado

- **WHEN** a consulta é chamada com um parâmetro fora dos que a rota declara
- **THEN** o núcleo responde 422, em vez de ignorar o parâmetro
