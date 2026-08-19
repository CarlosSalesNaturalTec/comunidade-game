## Context

As peças da troca já existem e estão consolidadas: `catalogo-avulso` (item, estoque, lastro,
ativo, ponto de apoio), `ponto-extra` (duas contas, com a trava de não-negativo em
`CheckConstraint` e gatilho), `livro-razao` (`lancar_debito`, cujo `aula_id` já nasceu anulável
citando "a baixa da troca do catálogo avulso") e `catalogo-de-tipos-de-recurso` (as duas réguas
de vigência). Esta fatia não inventa mecanismo: liga os quatro numa operação só.

Ver `proposal.md` — Why, e `specs/` para os requisitos.

## Goals / Non-Goals

**Goals:**

- Uma operação atômica, sem estado intermediário, que respeite `RN-07-27`.
- Recusa antes de qualquer escrita, com a condição nomeada na resposta.
- Preço congelado no registro; nenhuma saída da troca em moedas ou reais.

**Non-Goals:**

- Desfazer troca. O PRD-07 §6 não tem requisito para isso — ver Open Questions.
- Verificar estado da aula, presença ou janela de troca: garantia da App 01 (decisão 1).

## Decisions

**1. Módulo próprio `backend/src/nucleo/trocas/`, com `rotas.py` seu.** A `Troca` depende de
`aulas`, `catalogo_avulso`, `ponto_extra` e `livro_razao`, e nenhum deles depende dela — a seta
não fecha ciclo. _Alternativa descartada:_ pôr `POST /aulas/{id}/trocas` em `aulas/rotas.py`,
como `/aulas/{id}/reservas` está; ela deixaria a leitura do histórico órfã do módulo.

**2. Rotas: `POST /v1/aulas/{id}/trocas` e `GET /v1/trocas`.** A escrita fica sob a aula porque
o encontro é onde a entrega acontece (decisão 2 da proposta); a leitura fica em primeiro nível
porque o Guerreiro(a) lê o histórico dele inteiro, não o de uma aula. O filtro por persona segue
o padrão de `GET /catalogo-avulso`. _Alternativa descartada:_ `GET /minhas-trocas`, que exigiria
uma segunda rota para o Mestre e o Admin.

**3. As quatro recusas correm antes de qualquer escrita, na ordem do spec.** Item/lastro,
estoque, comunidade, saldo. Uma função de validação que devolve a condição que recusou, para a
resposta 422 nomeá-la. _Alternativa descartada:_ deixar as travas de banco (`CheckConstraint` do
saldo não-negativo) recusarem — daria 500 em vez de 422 e não diria o motivo.

**4. O lastro é reverificado com `saldo_de`, não lido de `item.ativo`.** `ativo` é marca gravada
na ativação; o saldo cai por outras baixas depois dela. O spec exige a reverificação no ato.

**5. `preco_cobrado` é coluna da `Troca`, não junção.** É o histórico que `RF-07-46` exige, e a
tabela de referência muda por vigência. Mesma escolha que `Aporte.valor_em_moedas` já fez.

**6. O débito usa `lancar_debito(..., aula_id=None)`** — quantidade 1, ponto de apoio do item,
moedas pela vigência do valor de referência na data, no mesmo mecanismo de
`reservas.regra._valorar_debito`. Não há reserva a consumir: a troca é entrega imediata.

**7. Tudo numa transação só, no padrão das demais escritas do núcleo.** O `flush` de cada peça
e um `commit` na rota; qualquer exceção desfaz as quatro escritas.

## Risks / Trade-offs

- **Duas trocas simultâneas do último item podem passar as duas pela verificação de estoque.** →
  Trava a linha do item (`SELECT ... FOR UPDATE`) antes de verificar estoque e lastro. O
  `CheckConstraint` do saldo de pontos extras cobre o mesmo risco do lado do Guerreiro(a).
- **Item ativo com estoque zero fica visível no catálogo.** → É a decisão do spec: o Mestre
  repõe o estoque sem recadastrar. A recusa por estoque protege a troca; a App 01 decide se
  exibe ou esconde.
- **Troca gravada é definitiva nesta fatia.** → O livro-razão tem ajuste, mas o ponto extra não
  tem caminho de volta. Ver Open Questions.

## Open Questions

- **Como se desfaz uma troca registrada por engano?** O PRD-07 §6 não tem requisito de
  cancelamento ou estorno de troca, e criá-lo aqui seria regra nascida num artefato do OpenSpec.
  A fatia entrega sem ele; a pergunta vai ao fundador e, se virar decisão, entra no documento 02
  §8.2 e no PRD-07 antes de virar código.
