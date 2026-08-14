## 1. Modelo e migração

- [ ] 1.1 Criar o módulo `backend/src/nucleo/coletas/` com `__init__.py`, `modelo.py`,
      `regra.py` e `rotas.py`, no desenho dos módulos vizinhos (design — Decisions).
- [ ] 1.2 Declarar `FormaDeRegistro` (`numero`, `foto`, `video`) e `TipoDeColeta` com nome,
      forma de registro, unidade, faixa mínima e máxima, `ativo` e autoria (`RF-08-05`).
- [ ] 1.3 Pôr no `TipoDeColeta` o `CheckConstraint` que exige unidade e faixa quando a forma é
      `numero`, as proíbe quando é `foto` ou `video`, e recusa mínimo maior que o máximo
      (`RF-08-05`, `RF-08-12`, design — Decisions).
- [ ] 1.4 Declarar `Cadencia` (`diaria`, `semanal`, `mensal`) e `DesafioDeColeta` com missão,
      tipo, cadência, início e fim da vigência, granularidade exigida e registros que pontuam
      por período, com `ComAutoria` (`RF-08-06`, `RN-08-06`).
- [ ] 1.5 Usar `NivelDoLocal` de `locais/modelo.py` na granularidade exigida, sem enum novo
      (`RN-08-25`, design — Decisions).
- [ ] 1.6 Escrever a revisão do Alembic que cria `tipo_de_coleta` e `desafio_de_coleta`, com
      `downgrade` na ordem inversa (design — Migration Plan).

## 2. Permissões e posse

- [ ] 2.1 Acrescentar `Operacao.catalogo_de_tipos_de_coleta` sem entrada na matriz de papel
      algum, no precedente do `catalogo_de_poderes`, de modo que só o Admin a alcance por
      `Operacao.tudo` (`RF-08-05`, `RF-01-16`).
- [ ] 2.2 Exigir `Operacao.suas_trilhas_e_conteudos` na escrita do desafio e conferir a posse
      com `conferir_posse_da_trilha`, alcançando a trilha por `missao.trilha_id` (`RF-08-06`,
      `RF-01-16`).

## 3. Regras do catálogo de tipos de coleta

- [ ] 3.1 Implementar cadastro, alteração e desativação de tipo de coleta, gravando autoria,
      data e hora (`RF-08-05`, `RF-01-03`).
- [ ] 3.2 Recusar com 422 tipo sem nome, forma de registro fora das três, tipo por número sem
      unidade ou sem faixa, e faixa invertida (`RF-08-05`).
- [ ] 3.3 Recusar com 403 a escrita no catálogo por qualquer papel que não seja Admin,
      inclusive o Mestre (`RF-08-05`, `RF-01-16`).

## 4. Regras do desafio de coleta

- [ ] 4.1 Implementar a criação do desafio vinculado a uma missão da trilha do Mestre autor,
      recusando com 422 missão inexistente ou de outra trilha (`RF-08-06`).
- [ ] 4.2 Recusar com 422 desafio sem tipo, cadência, vigência, granularidade ou quantidade de
      registros que pontuam, apontando o campo em falta (`RF-08-06`, `RN-08-06`).
- [ ] 4.3 Recusar com 422 cadência fora das três, vigência cujo fim precede o início e
      quantidade de registros que pontuam menor que 1 (`RF-08-06`, `RN-08-06`).
- [ ] 4.4 Aceitar qualquer um dos seis níveis como granularidade exigida sem ler
      `ComunidadeVirtual`, e recusar com 422 nível fora da hierarquia (`RN-08-25`).
- [ ] 4.5 Recusar com 422 o desafio que escolhe tipo desativado, deixando intactos os desafios
      já criados com aquele tipo (`RF-08-05`, `RF-08-06`).

## 5. Etiqueta ODS herdada

- [ ] 5.1 Implementar `resolver_etiquetas_do_desafio`, delegando a
      `ods/regra.py::resolver_etiquetas_da_missao`, sem coluna de etiqueta no desafio
      (`RF-08-25`, `RF-01-41`, design — Decisions).
- [ ] 5.2 Recusar com 422 o desafio que chega com etiqueta ODS declarada nele, porque a
      etiqueta é derivada (`RF-08-25`).
- [ ] 5.3 Garantir que a etiqueta herdada não entra em pontuação, cadência nem validade, e que
      trocá-la não reprocessa nada (`RN-08-21`).

## 6. Rotas

- [ ] 6.1 Criar `POST /v1/tipos-de-coleta`, de Admin, com o contrato de entrada e saída no
      desenho de `locais/rotas.py` (`RF-08-05`, PRD-08 §9).
- [ ] 6.2 Criar `POST /v1/desafios-de-coleta`, de Mestre (`RF-08-06`, PRD-08 §9).
- [ ] 6.3 Registrar o roteador de `coletas/` em `principal.py`, sob o prefixo `/v1`
      (`RF-01-01`).

## 7. Testes

- [ ] 7.1 Cobrir o cadastro do tipo por Admin, a recusa do Mestre com 403 e as quatro recusas
      de 422 do catálogo (`RF-08-05`).
- [ ] 7.2 Cobrir tipo por número com unidade e faixa, tipo por foto sem elas, e a recusa do
      tipo por número sem faixa (`RF-08-05`, `RF-08-12`).
- [ ] 7.3 Cobrir a criação do desafio pelo Mestre autor, a recusa do Mestre que não é autor com
      403 e a recusa da missão de outra trilha com 422 (`RF-08-06`).
- [ ] 7.4 Cobrir as recusas de 422 dos atributos do desafio, uma por cenário da spec
      (`RF-08-06`, `RN-08-06`).
- [ ] 7.5 Cobrir a granularidade mais fina que a de uma comunidade sendo aceita, e provar que
      nenhuma comunidade é lida na criação do desafio (`RN-08-25`).
- [ ] 7.6 Cobrir a herança da etiqueta pela missão, o recuo para a da trilha, o desafio sem
      etiqueta quando nenhuma existe, e a etiqueta nova aparecendo após a troca na missão
      (`RF-08-25`, `RF-01-41`).
- [ ] 7.7 Cobrir a recusa do desafio que escolhe tipo desativado e o desafio já criado que
      segue intacto após a desativação (`RF-08-05`, `RF-08-06`).
- [ ] 7.8 Cobrir que a trilha em rascunho sem desafio de coleta continua sendo aceita
      (`RN-08-14`).

## 8. Documentação e esteira

- [ ] 8.1 Conferir que `docs/` já reflete esta change: as duas decisões entraram no documento
      02 §1, no documento 09 e no PRD-08 antes do código, e nada mais mudou — o PRD-08 segue
      **aprovado** em `docs/prds/index.md`, e nenhum arquivo novo entra em `docs/` nem na `nav`
      do `mkdocs.yml`.
- [ ] 8.2 Rodar `ruff format`, `ruff check` e `pytest` em `backend/`, as três verificações que
      bloqueiam o merge.
- [ ] 8.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR.
