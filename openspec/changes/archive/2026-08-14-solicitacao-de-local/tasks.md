## 1. Refatoração que abre a segunda origem do local

- [x] 1.1 Separar, em `locais/regra.py`, o portão de autorização do núcleo de validação da
      hierarquia: `cadastrar_local` mantém assinatura e o 403 para quem não é Admin, e delega a
      uma função interna que valida comunidade, nível, rótulo e pai sem opinião sobre quem
      chama (`RF-08-04`, design — Decisions)
- [x] 1.2 Rodar os testes vigentes de `local-do-territorio` sem alterá-los — passar sem
      alteração é a prova da refatoração (`RF-08-04`)

## 2. Modelo e migração

- [x] 2.1 Criar `SolicitacaoDeLocal` em `locais/modelo.py` com os atributos do PRD-08 §8 —
      solicitante, comunidade, desafio de origem, nível pretendido, rótulo, justificativa,
      situação, avaliador e motivo da recusa — mais o local criado e a data do desfecho
      (`RF-08-22`, design — Decisions)
- [x] 2.2 Declarar a situação como enum de três valores — `recebida`, `aprovada`, `recusada` —
      sem prazo de resposta e sem campo de atraso (`RF-08-24`, `RN-08-18`)
- [x] 2.3 Escrever a migração do Alembic que cria `solicitacao_de_local`, com as chaves
      estrangeiras para persona, comunidade, desafio de coleta e local criado (design —
      Migration Plan)

## 3. Regra de solicitação

- [x] 3.1 Implementar a solicitação restrita ao Guerreiro(a), com 403 para qualquer outro papel
      (`RF-08-22`)
- [x] 3.2 Prender a solicitação à comunidade vigente do solicitante, recusando com 403 a
      solicitação apontada para outra comunidade (`RF-08-22`, `RN-08-02`)
- [x] 3.3 Exigir nível entre os seis da hierarquia, rótulo e justificativa, recusando com 422 o
      que faltar (`RF-08-22`)
- [x] 3.4 Garantir que o pedido grave a solicitação e NEVER crie local (`RN-08-18`)

## 4. Regra de avaliação

- [x] 4.1 Alcançar a trilha por desafio de origem → missão → trilha e aplicar
      `conferir_posse_da_trilha`, aceitando Admin e Mestre autor e recusando os demais com 403
      (`RF-08-23`)
- [x] 4.2 Implementar a aprovação chamando o núcleo de validação da tarefa 1.1, com o
      `local_pai_id` vindo do corpo da avaliação, e gravando o local criado na solicitação
      (`RF-08-23`, `RF-08-04`, design — Decisions)
- [x] 4.3 Validar a hierarquia antes de qualquer escrita do desfecho: pai inválido recusa com
      422 e deixa a solicitação em aberto, sem avaliador nem data gravados (`RF-08-23`,
      `RF-08-04`)
- [x] 4.4 Exigir motivo na recusa, recusando com 422 a recusa sem motivo, e gravar avaliador e
      data no desfecho (`RF-08-23`)
- [x] 4.5 Recusar com 422 a segunda avaliação de solicitação já aprovada ou recusada, sem
      alterar o desfecho gravado (`RF-08-23`)

## 5. Lista de solicitações em aberto

- [x] 5.1 Implementar a listagem com `contrato_de_listagem(filtro_comunidade_obrigatorio=True)`,
      recusando com 422 a consulta sem o filtro de comunidade (`RF-08-24`, `RF-01-18`)
- [x] 5.2 Aplicar o recorte por papel num caminho só: Admin sem recorte adicional, Mestre
      restrito às trilhas de que é autor, pela junção solicitação → desafio → missão → trilha
      (`RF-08-24`, `RF-08-23`)
- [x] 5.3 Devolver apenas as solicitações sem desfecho, e recusar com 403 persona de outro papel
      (`RF-08-24`)

## 6. Permissões e rotas

- [x] 6.1 Acrescentar a operação de solicitar local ao conjunto de escrita do Guerreiro(a) em
      `permissoes.py` e ligar `aprovacao_de_local`, já declarada para o Mestre, à rota de
      avaliação (`RF-08-22`, `RF-08-23`, `RF-01-16`)
- [x] 6.2 Expor `POST /solicitacoes-de-local`, `GET /solicitacoes-de-local/abertas` e
      `POST /solicitacoes-de-local/{id}/avaliacao`, e registrá-las em `principal.py`
      (`RF-08-22`, `RF-08-23`, `RF-08-24`, PRD-08 §9)
- [x] 6.3 Gravar autoria em toda escrita das três rotas, pelo mixin vigente (`RF-01-03`)

## 7. Testes

- [x] 7.1 Solicitação em comunidade que não é a do Guerreiro(a) recusada com 403; solicitação
      por quem não é Guerreiro(a) recusada com 403 (`RF-08-22`)
- [x] 7.2 Envio da solicitação não cria local, e a série não abre no local ainda pedido
      (`RN-08-18`, `RF-08-07`)
- [x] 7.3 Aprovação por Admin e pelo Mestre autor aceitas; Mestre de outra trilha recusado com
      403; Guerreiro(a) que tenta aprovar a própria solicitação recusado com 403 (`RF-08-23`)
- [x] 7.4 Critério de aceite do PRD-08 §12: solicitação aprovada pelo Mestre da trilha cria o
      local e **libera a abertura da série**; recusada, devolve o motivo (`RF-08-23`)
- [x] 7.5 Pai de nível ou comunidade inválidos recusados com 422, sem criar local e sem consumir
      a solicitação; recusa sem motivo recusada com 422 (`RF-08-23`, `RF-08-04`)
- [x] 7.6 Segunda avaliação recusada com 422, sem criar um segundo local e sem alterar o
      desfecho (`RF-08-23`)
- [x] 7.7 Lista sem filtro de comunidade recusada com 422; Admin vê as de outras trilhas na
      comunidade filtrada; Mestre vê só as das suas; solicitação avaliada sai da lista
      (`RF-08-24`, `RF-01-18`)
- [x] 7.8 Solicitação de local não recebe prazo nem marca de atraso, e não aparece na fila única
      das quatro naturezas (`RF-08-24`, `RN-08-18`)

## 8. Documentação e fecho

- [x] 8.1 Acrescentar **a solicitação de novo local** à linha do Guerreiro(a) na matriz de
      `docs/prds/prd-01-backend-api.md` §4 — omissão corrigida, não decisão nova (`RF-08-22`,
      proposal — Omissão corrigida)
- [x] 8.2 Conferir que nada mais em `docs/` muda: o documento 09 não recebe linha, porque não há
      decisão nova; `docs/prds/index.md` mantém o PRD-08 "aprovado"; o documento 99 não muda,
      porque nenhuma relação entre documentos foi alterada; e a `nav` do `mkdocs.yml` não muda,
      porque nenhum arquivo nasceu em `docs/`
- [x] 8.3 Rodar `ruff format --check .`, `ruff check .` e `pytest` no `backend/`
- [x] 8.4 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR
- [x] 8.5 Rodar `openspec validate --all` e `/opsx:verify` antes de arquivar a change
