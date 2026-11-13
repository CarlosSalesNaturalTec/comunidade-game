## ADDED Requirements

### Requirement: O percurso do Guerreiro(a) registra a customização do kit no encontro

No caminho **Trilhas e missões** — o percurso do Guerreiro(a) no aparelho do encontro —, a App
01 SHALL mostrar cada **kit recebido com customização aberta**, identificado pelo kit e pela
trilha, com a situação e a ação da camada comum, e o registro da camada comum, sem cópia
própria e sem divergir da App 05. A leitura e as escritas vão sob a **sessão do Guerreiro(a)**.
O registro NEVER SHALL ganhar entrada nova na tela inicial. (`RF-04-80`, PRD-04 §5.13.1)

#### Scenario: Kit aberto oferece o registro no percurso

- **WHEN** o Guerreiro(a) abre Trilhas e missões e um kit recebido tem a customização aberta,
  sem registro
- **THEN** o percurso mostra aquele kit e oferece Registrar a customização

#### Scenario: Sem kit aberto, o percurso não muda

- **WHEN** nenhum bem recebido do Guerreiro(a) tem customização aberta
- **THEN** o percurso mostra as trilhas e as atividades do encontro, sem bloco de customização

#### Scenario: O registro no encontro vai à fila do Mestre da aula

- **WHEN** o Guerreiro(a) registra a customização no percurso e o envio é confirmado
- **THEN** o kit mostra que aguarda a aula, e o registro é o pendente que a fila do cuidado do
  encontro apresenta ao Mestre

#### Scenario: O pendente se cancela no encontro

- **WHEN** o kit tem registro pendente e o Guerreiro(a) toca em Cancelar
- **THEN** o registro é cancelado e o kit volta a oferecer Registrar a customização

### Requirement: A falha da customização não esconde o percurso

A falha só na leitura da customização SHALL aparecer num aviso único e NEVER SHALL esconder as
trilhas nem as atividades do encontro. (`RF-04-80`)

#### Scenario: A customização não carrega

- **WHEN** a leitura das trilhas responde e a da customização falha
- **THEN** o percurso mostra as trilhas e as atividades, com um aviso de que a customização dos
  kits não carregou
