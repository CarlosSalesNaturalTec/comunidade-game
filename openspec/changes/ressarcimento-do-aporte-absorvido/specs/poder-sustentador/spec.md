## ADDED Requirements

### Requirement: O ressarcimento pago derruba o Poder Sustentador e não o selo

O Poder Sustentador do provedor SHALL **cair** quando um aporte por absorção dele é ressarcido,
voltando ao valor anterior àquele aporte — pela cadeia de ajuste que esta capacidade já deriva,
sem caminho novo de cálculo. A **contagem de absorções** daquele provedor NÃO SHALL mudar com o
ressarcimento: o reconhecimento é por ter sustentado a atividade quando faltou recurso, não pelo
valor.

O Poder Sustentador de quem **doa com destinação ressarcimento** SHALL subir pelas moedas da
doação, como o de qualquer provedor — a destinação separa o que vira lastro do que não vira, não
o que é reconhecido do que não é. (`RF-07-25`, `RF-07-23`, `RN-07-18`, `RN-07-19`, `RN-07-38`,
PRD-07 §12)

#### Scenario: O Poder Sustentador volta ao anterior e o selo permanece

- **WHEN** a única absorção de um Mestre, de 5 moedas, é ressarcida
- **THEN** o Poder Sustentador dele volta ao que era antes daquele aporte e a contagem de
  absorções segue em 1

#### Scenario: A doação destinada a ressarcir credita quem doou

- **WHEN** um Apoiador registra um aporte de destinação ressarcimento de 20 moedas
- **THEN** o Poder Sustentador dele sobe 20

#### Scenario: A prestação de contas pública lê o mesmo número

- **WHEN** uma absorção é ressarcida e a prestação de contas pública é consultada
- **THEN** o movimentado por aquele provedor reflete a queda, sem divergir da leitura por
  provedor
