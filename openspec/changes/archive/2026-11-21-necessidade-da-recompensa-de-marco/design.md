# Design

## Context

A necessidade da aula já existe (`openspec/specs/necessidade-de-recurso`): derivada na leitura,
contada pela ordem do horário e servida pelas rotas pública e do Mestre. Missão do Apoiador,
absorção e declaração do Apoiador a apontam pelo par `aula_id` + `tipo_de_recurso_id`, sem
chave estrangeira para a necessidade. A fatia 13 entregou `aula_de_referencia_da_comunidade`,
que dá o ponto de apoio da entrega fora do encontro. Esta fatia acrescenta a segunda espécie e
leva o resto a aceitá-la.

## Goals / Non-Goals

**Goals:** derivar a necessidade da recompensa; servi-la nas duas rotas existentes; deixar
absorção, missão e declaração apontá-la; mostrá-la nas quatro aplicações.

**Non-Goals:** rota nova; gravar necessidade; mudar a necessidade da aula; mudar a entrega da
recompensa (fatia 13).

## Decisions

1. **Uma derivação, duas espécies.** `derivar_necessidades` devolve as da aula, como hoje, e
   depois as da recompensa, de uma função nova no mesmo módulo. `NecessidadeDeRecurso` ganha
   `especie` (`aula` | `recompensa_de_marco`), `trilha_id` e `trilha_nome`; `aula_id`,
   `inicio_em` e `fim_em` passam a opcionais. Os tipos não se disputam: pela finalidade
   (`RN-07-41`), a aula só declara consumo do encontro e a recompensa só recompensa.
   - Descartado: rota própria para a recompensa — o PRD-07 §9 serve as duas pelas mesmas rotas.

2. **Derivação da recompensa**, por comunidade:
   - ponto de apoio = `aula_de_referencia_da_comunidade(...)`; sem ela, a comunidade não gera
     nada;
   - trilhas = as de `Missao.trilha_id` das `Atividade` não removidas cuja aula é da comunidade e
     não cancelada; a data de ordem da trilha é o menor `Aula.inicio_em` entre essas atividades;
   - pedido por tipo = Σ sobre as `RecompensaDeMarco` da trilha daquele tipo de
     (vínculos vigentes − entregas da recompensa a quem tem vínculo vigente) × `quantidade`;
   - falta = pedido − disponível, atribuído por par (tipo, ponto de apoio) em ordem
     `(data de ordem, trilha_id)` — a mesma atribuição gulosa da aula, e o desempate por
     identificador dá ordem estável.

3. **Identidade da necessidade da recompensa: comunidade + trilha + tipo.** O ponto de apoio é
   função da comunidade no momento da leitura; guardá-lo na missão ou na declaração faria a
   chave envelhecer quando a comunidade tiver aula nova noutro ponto.

4. **Ordem da saída:** as da aula primeiro, por `inicio_em`, como hoje; as da recompensa
   depois, por nome da comunidade, nome da trilha e nome do tipo.

5. **Esquema.** Uma migração Alembic acrescenta `comunidade_virtual_id` e `trilha_id`, anuláveis
   e com chave estrangeira, a `aporte`, `aporte_declarado` e `missao_do_apoiador`, e torna
   `missao_do_apoiador.aula_id` anulável. Um `CheckConstraint` em `missao_do_apoiador` garante
   aula **ou** comunidade + trilha. Em `aporte` e `aporte_declarado` a regra fica no código,
   porque ali as duas podem faltar (aporte da gestão; declaração por missão ou valor livre).
   - Descartado: coluna `chave_da_necessidade` em texto — perde a chave estrangeira.

6. **Validação da absorção da recompensa.** Exige o ponto de apoio igual ao da aula anterior
   da comunidade e uma `RecompensaDeMarco` da trilha com aquele tipo; não exige que a
   necessidade esteja aberta, como a da aula não exige. Credita como qualquer absorção;
   `confirmar_aulas_pendentes` segue chamada e não acha aula, porque o tipo é recompensa.

7. **Missão e declaração** conferem a combinação contra `derivar_necessidades` com a chave da
   espécie: `(aula_id, tipo)` ou `(comunidade, trilha, tipo)`. `tem_necessidade_por_tras`
   usa a mesma chave.

8. **Aplicações.** Cada uma ganha uma função `chaveDaNecessidade` e um rótulo que mostra a
   data da aula ou "Trilha <nome>" pela `especie`. A App 09 e a App 03 enviam
   `comunidade_virtual_id` e `trilha_id` no lugar de `aula_id`; a App 08 faz o mesmo na
   declaração, e o pré-cadastro só muda o texto que descreve a escolha.

9. **Documentação.** As três regras de contagem decididas pelo fundador ao abrir a fatia
   entram no documento 04 §1, no item da recompensa, e na linha "Consumo do encontro e
   recompensa de marco" do documento 09.

## Risks / Trade-offs

- **Leitura mais cara:** a derivação percorre vínculos e entregas de toda comunidade com aula.
  No Ciclo 01 são poucas comunidades e dezenas de Guerreiros(as); fica uma consulta por
  agregação, sem cache.
- **Pedido antecipado:** conta quem ainda não alcançou o marco, como o documento 04 manda; a
  necessidade é estoque para a turma, não fila de entrega.
- **BREAKING** nos campos opcionais da saída: as quatro aplicações mudam no mesmo PR.
