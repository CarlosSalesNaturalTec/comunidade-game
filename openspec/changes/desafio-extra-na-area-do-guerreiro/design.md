## Context

A `desafio-extra` já está consolidada em `openspec/specs/desafio-extra/spec.md`: entidade,
situações, lastro, reserva na publicação, encerramento e quantidade restante. Esta fatia não
mexe em nada disso — só acrescenta **uma consulta de leitura** e a tela que a exibe. O
`GET /v1/eu/desafios` já existe desde a fatia 6, com a derivação em
`trilhas.regra.desafios_em_aberto_do_guerreiro`.

Duas coisas que a leitura precisa e o código já tem: `Nick`, tabela própria com índice único
sobre `lower(valor)`, e `InscricaoNaTrilha`, lida por
`trilhas.regra.consultar_inscricoes_do_guerreiro`. O `encerrado` não é situação: é
`encerrado_em` preenchido sobre um desafio que segue em `publicado`.

## Goals / Non-Goals

**Goals:**

- Servir ao Guerreiro(a) em sessão os desafios extras publicados, vigentes e elegíveis, na
  mesma rota que a §9 do PRD-05 declara para eles.
- Exibi-los na App 05 com o que o `RF-05-21` manda, apartados dos semanais.

**Non-Goals:**

- Concluir o desafio, entregar a recompensa ou creditar o ponto extra — a `ConclusaoDeDesafioExtra`
  já existe e o ato de gravá-la é de fatia futura do PRD-09.
- Qualquer escrita a partir da App 05: a fatia é leitura de ponta a ponta.
- Mexer na proposta, na validação, na aprovação, na publicação ou no encerramento.

## Decisions

1. **Um objeto com `semanais` e `extras` em `GET /v1/eu/desafios`**, no lugar da lista de
   atividades. É o que a §9 do PRD-05 declara para a rota; a fatia 6 entregou metade do
   contrato. Descartado: rota nova `GET /v1/eu/desafios-extras/vigentes` — divergiria da §9 sem
   decisão do fundador, e `GET /v1/eu/desafios-extras` já é a leitura do proponente.
   **Quebra o contrato** para o único consumidor, a App 05, atualizada nesta change.
2. **A derivação mora em `desafios_extras.regra`**, não em `trilhas.regra`: é regra do desafio
   extra, e a rota apenas a compõe com a que já tem. Descartado: pôr tudo em `trilhas.regra` —
   arrastaria o agregado do desafio extra para dentro do de trilhas.
3. **Elegibilidade em uma consulta só**, com a inscrição exigida nas duas modalidades:
   `situacao = publicado`, `encerrado_em IS NULL`, `vigencia_inicio <= hoje <= vigencia_fim`,
   `trilha_id` entre as inscrições do Guerreiro(a), e `modalidade = aberto OR
   lower(nick_do_destinatario) = lower(nick dele)`. Exigir a inscrição também no direcionado é
   decisão do fundador de 2026-09-02: o desafio se prende a uma trilha (e às vezes a uma
   missão), e quem não está nela não teria como cumpri-lo.
4. **O esgotado permanece na leitura**, com `quantidade_restante = 0` — decisão do fundador de
   2026-09-02, coerente com a §5.2 do PRD-05, que proíbe o que já não dá para fazer sumir sem
   motivo. O filtro é de situação e vigência, nunca de disponibilidade.
5. **Saída própria e enxuta, não a `DesafioExtraSaida`**: a saída do proponente carrega
   `nick_do_destinatario`, `justificativa_do_vinculo`, `parecer_do_mestre`,
   `motivo_da_recusa`, `custeio`, `aporte_id` e `lastro_*`, que `RN-05-21` e `RN-14-20` mandam
   não entregar ao Guerreiro(a). A saída dele traz o que o `RF-05-21` pede mais o que a criança
   precisa para agir, com **nome** do tipo de recurso, do ponto de apoio, da trilha e da missão
   no lugar dos identificadores crus — o mesmo que a `DesafioSaida` dos semanais já faz.
6. **A tela é um terceiro bloco dentro da aba Desafios**, não uma aba nova: o
   `DesafiosEEquipes` já divide Desafios e Minhas equipes, e o `RF-05-20` é desafio. O
   `MeusDesafios` passa a montar os dois blocos a partir da mesma resposta, sem segunda
   chamada.
7. **Ponto extra em nenhum lugar vira nível**: nada nesta fatia escreve pontuação, e a tela diz
   à criança que o extra não conta para o nível (`RN-05-18`). Sem custo de operação, nada entra
   no livro-razão; sem dado de território, nenhuma série nasce aqui.

## Risks / Trade-offs

- **A quebra do contrato de `GET /v1/eu/desafios`** exige que backend e App 05 mudem juntos.
  Mitigação: consumidor único, mudança no mesmo PR, e os testes da rota cobrem o formato novo.
- **`quantidade_restante` é calculada por desafio**, com uma consulta cada. A lista do
  Guerreiro(a) é curta — os desafios vigentes das trilhas dele —, e a alternativa (agregar em
  bloco) só se paga se a lista crescer; fica para quando crescer.
- **A comparação de nick por `lower()`** repete o critério de unicidade da tabela `nick`. Se
  esse critério mudar, esta consulta muda junto — está anotado na regra.
