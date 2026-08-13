## MODIFIED Requirements

### Requirement: Badge é conquistado por trilha ou por poder, nunca global

O núcleo SHALL conceder **badge** sempre vinculado a uma trilha ou a um poder, nunca de forma
global (11 §7), com **uma única exceção: o badge de protagonismo**, que é global porque a
proposta de evolução que o rende é sobre a plataforma inteira e não sobre uma trilha
(`RN-01-50`). Nesta capacidade o núcleo SHALL conceder o **badge de nível** a cada nível
certificado, o **badge de valores/causas** a Resultado de atividade de natureza "valores e
temas transversais", o **badge de autoria** a **cada integrante** da equipe cuja criação
original for validada pelo Mestre autor e o **badge de protagonismo** ao autor da sugestão
adotada pela gestão, na mesma operação em que a fila de avaliação grava o desfecho. O badge de
conquista **Guardião do Acervo** não nasce de Resultado nem de Criação Original — ele depende
de encontro presencial identificável (`Aula/Agenda`) — e fica para a fatia que o entregar.
(`RF-01-21`, `RF-01-64`, `RN-01-50`, 11 §7)

#### Scenario: Badge de nível concedido ao certificar um nível

- **WHEN** o núcleo certifica um nível numa trilha
- **THEN** o núcleo concede o badge de nível correspondente àquela trilha

#### Scenario: Badge de valores/causas concedido por atividade da natureza

- **WHEN** o Guerreiro(a) tem Resultado de atividade de natureza "valores e temas transversais"
- **THEN** o núcleo concede o badge de valores/causas correspondente à trilha ou ao poder

#### Scenario: Badge de autoria concedido ao validar a criação original

- **WHEN** o Mestre autor da trilha valida a criação original entregue pela equipe da trilha
- **THEN** o núcleo concede o badge de autoria daquela trilha a cada integrante da equipe

#### Scenario: Badge de protagonismo concedido ao adotar a proposta

- **WHEN** um Admin conclui a avaliação de uma sugestão como **adotada**
- **THEN** o núcleo concede o badge de protagonismo ao autor, **sem vínculo com trilha ou
  poder**, na mesma operação em que credita os pontos extras

#### Scenario: Badge de protagonismo não se repete

- **WHEN** o desfecho **adotada** é gravado para uma sugestão cujo autor já recebeu o badge de
  protagonismo
- **THEN** o núcleo não concede o badge outra vez
