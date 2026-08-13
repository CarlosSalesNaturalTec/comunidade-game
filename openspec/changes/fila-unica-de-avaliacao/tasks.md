## 1. Ciclo comum e modelo

- [ ] 1.1 Criar `backend/src/nucleo/fila/modelo.py` com o _mixin_ `EmAvaliacao` — situação,
      prazo, quem avaliou, parecer e data do desfecho — no idioma do `ComAutoria` já existente
      (`RF-01-25`, design — Decisions)
- [ ] 1.2 Declarar `SituacaoDaSolicitacao` (recebida, em avaliação, aceita, recusada) e
      `SituacaoDaSugestao` (recebida, em avaliação, adotada, não adotada), preservando o
      vocabulário do PRD-05 §5.8 (`RF-01-25`)
- [ ] 1.3 Declarar a constante do prazo de 7 dias em `fila/regra.py`, gravada na linha no
      registro e nunca calculada na leitura (`RN-01-49`, 02 §1, 03 §§7, 12.3)
- [ ] 1.4 Modelar `SolicitacaoDeParticipacao` com os campos do PRD-01 §8, incluindo pretensão,
      aporte declarado e a referência do comprovante (`RF-01-25`, `RN-01-28`)
- [ ] 1.5 Modelar `SolicitacaoDeDados` com solicitante, instituição, e-mail, finalidade
      declarada, recorte pedido e o que foi entregue (`RF-01-46`)
- [ ] 1.6 Modelar `SolicitacaoDeChave` com solicitante, contato, instituição opcional e o que
      pretende construir (`RF-01-49`)
- [ ] 1.7 Modelar `SugestaoOuProposta` com autor e persona, alvo, texto, motivo do retorno e a
      marca de crédito já concedido (`RF-01-25`, 03 §§7, 12.2)
- [ ] 1.8 Gerar a migração do Alembic com as quatro tabelas e os dois tipos enumerados, com
      `downgrade` que as remove (design — Migration Plan)

## 2. Porta de armazenamento do comprovante

- [ ] 2.1 Criar `backend/src/nucleo/armazenamento/` com a interface mínima — gravar, ler e
      remover — sem versionamento nem ciclo de vida (design — Decisions)
- [ ] 2.2 Implementar o adaptador de disco, padrão em desenvolvimento e na esteira
      (design — Migration Plan)
- [ ] 2.3 Implementar o adaptador de Cloud Storage e a escolha por `Configuracao`, sem
      credencial obrigatória fora de produção (03 §1)
- [ ] 2.4 Gravar no registro apenas referência, nome original, tipo e tamanho — nunca os bytes
      (`RN-01-28`, design — Decisions)

## 3. Rotas públicas de envio

- [ ] 3.1 Criar `fila/rotas.py` e registrar o roteador por `incluir_roteador_de_dados`, que já
      exige chave de aplicação e cota (`RF-01-48`, `RF-01-55`)
- [ ] 3.2 Implementar `POST /v1/solicitacoes-de-participacao`, aceitando pretensão de Mestre ou
      Apoiador e, para Apoiador, aporte declarado e comprovante (`RF-01-25`, `RN-01-28`)
- [ ] 3.3 Recusar a solicitação de participação que traga CPF, CNPJ ou documento de identidade
      (`RN-01-29`)
- [ ] 3.4 Implementar `POST /v1/solicitacoes-de-dados`, exigindo finalidade declarada
      (`RF-01-46`)
- [ ] 3.5 Implementar `POST /v1/solicitacoes-de-chave`, que registra e **não** emite chave
      (`RF-01-49`, `RN-01-37`)
- [ ] 3.6 Declarar a superfície do freio nas rotas de participação e de dados pela _dependency_
      `exigir_freio_por_origem`, e **não** declará-la na de chave (`RF-01-65`, `RN-01-46`)
- [ ] 3.7 Garantir que as três devolvam apenas registro e prazo — nunca dado, arquivo, chave ou
      acesso (`RN-01-03`, `RN-01-25`, `RN-01-37`)

## 4. Sugestão e proposta por rota autenticada

- [ ] 4.1 Acrescentar a operação de proposta do Mestre a `Operacao` e à
      `MATRIZ_DE_PERMISSOES`, aplicando a correção do PRD-01 §4 (`RF-01-16`, 03 §11)
- [ ] 4.2 Implementar `POST /v1/sugestoes` autenticada, aceitando **texto apenas**, com autor,
      persona e alvo gravados (`RF-01-25`, 03 §§7, 12.2)
- [ ] 4.3 Recusar com 401 a chamada sem credencial de persona (`RF-01-03`)
- [ ] 4.4 Calcular e gravar a data de descarte da transcrição não adotada, 90 dias após o
      retorno, e marcar a adotada como permanente com autoria (03 §12.2)

## 5. Avaliação e desfecho

- [ ] 5.1 Implementar o desfecho de Admin nas quatro naturezas, gravando situação, parecer,
      autor e data (`RF-01-25`, `RF-01-46`, `RF-01-49`)
- [ ] 5.2 Exigir na aprovação da solicitação de dados o solicitante identificado, a finalidade
      declarada e o compromisso de não reidentificação, e registrar o motivo da recusa nas
      mesmas frentes (`RN-01-48`)
- [ ] 5.3 Recusar a liberação de conjunto de dados sem aprovação de Admin registrada
      (`RF-01-47`, `RN-01-25`)
- [ ] 5.4 Garantir que nenhum desfecho crie cadastro, persona ou credencial (`RN-01-03`,
      `RN-01-28`, `RN-01-37`)
- [ ] 5.5 Derivar "em atraso" de `prazo < agora` sem desfecho, sem estado gravado
      (`RN-01-49`, design — Decisions)

## 6. Crédito da proposta adotada

- [ ] 6.1 Acrescentar a constante de 20 extras a `ponto_extra/regra.py`, no precedente das
      fontes já existentes (`RF-01-56`, 11 §5)
- [ ] 6.2 Creditar, na mesma transação do desfecho "adotada", 20 ao acumulado e ao saldo
      disponível de ponto extra, sem creditar ponto regular (`RF-01-56`, `RF-01-57`)
- [ ] 6.3 Conceder o badge de protagonismo ao autor, sem vínculo com trilha ou poder
      (`RF-01-21`, `RN-01-50`)
- [ ] 6.4 Tornar crédito e badge idempotentes pela linha da sugestão (`RF-01-56`, design —
      Decisions)

## 7. Testes

- [ ] 7.1 Testar que envio de formulário público devolve protocolo e prazo e não cria persona
      nem credencial, e que a autenticação com os dados informados é recusada (`RN-01-03`,
      `RN-01-25`, `RN-01-37`)
- [ ] 7.2 Testar que a aprovação da solicitação de participação não cria persona (`RN-01-03`)
- [ ] 7.3 Testar a recusa de CPF, CNPJ e documento de identidade (`RN-01-29`)
- [ ] 7.4 Testar que a solicitação de dados sem finalidade é recusada e que o conjunto não sai
      sem aprovação registrada (`RF-01-46`, `RF-01-47`)
- [ ] 7.5 Testar que o envio da solicitação de chave não emite chave e que a repetição da mesma
      origem **não** encontra atraso (`RF-01-49`, `RN-01-46`)
- [ ] 7.6 Testar que o formulário de participação repetido encontra 429 e que cada formulário
      conta em separado (`RF-01-65`, `RN-01-27`)
- [ ] 7.7 Testar que a rota de sugestão recusa áudio, recusa chamada anônima e grava autor,
      persona e alvo (`RF-01-25`)
- [ ] 7.8 Testar que a proposta adotada credita 20 extras e o badge sem ponto regular, que a
      não adotada não credita nada, que registrar não pontua e que regravar o desfecho não
      credita duas vezes (`RF-01-56`, `RF-01-57`, `RN-01-50`)
- [ ] 7.9 Testar o prazo de 7 dias gravado no registro e a derivação de "em atraso"
      (`RN-01-49`)
- [ ] 7.10 Testar que o comprovante vai à porta de armazenamento e que a linha guarda apenas a
      referência (`RN-01-28`)

## 8. Documentação e esteira

- [ ] 8.1 Conferir que `docs/` já reflete esta change: as decisões da entrega de dados, do
      prazo, dos atributos de `SugestaoOuProposta`, do badge de protagonismo e da proposta do
      Mestre entraram nos documentos 03, 09 e 11 e nos PRD-01, PRD-02 e PRD-03 nos commits que
      antecedem a implementação — nada novo a escrever, nada em `docs/prds/index.md`, no
      documento 99 nem na `nav` do `mkdocs.yml`
- [ ] 8.2 Rodar `ruff format --check .`, `ruff check .` e `pytest` no `backend/`
- [ ] 8.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR
