## 1. Leitura e desfecho no núcleo

- [ ] 1.1 `GET /solicitacoes-de-participacao` em `fila/rotas.py`: `contrato_de_listagem` **sem**
      filtro de comunidade obrigatório (design — decisão 1), envelope `PaginaDeResultado`,
      restrita a Admin no molde de `chaves/rotas.py`, ordenada do mais antigo para o mais
      recente. A saída traz identificação, pretensão, apresentação, instituição, links,
      situação, prazo e o desfecho quando houver; na pretensão de Apoiador, o aporte declarado,
      o nick pretendido e a indicação de comprovante anexado — nunca o conteúdo do arquivo
      (`RF-02-18`, `RF-02-83`, `RF-01-25`, `RF-01-28`, `RF-01-16`, `RN-01-28`).
- [ ] 1.2 Campo `em_atraso` derivado na saída da mesma rota, consumindo `esta_em_atraso` **sem
      alterá-la**, calculado no instante da consulta e nunca gravado (`RF-02-65`, `RN-01-49`,
      design — decisão 2).
- [ ] 1.3 `POST /solicitacoes-de-participacao/{id}/avaliacao` em `fila/rotas.py`, consumindo
      `avaliar_solicitacao_de_participacao` **sem alterá-la**: restrita a Admin, aceita ou
      recusada com parecer, 422 no desfecho fora do vocabulário, 404 na solicitação inexistente
      (`RF-02-19`, `RF-02-86`, `RF-01-25`, `RN-02-01`).
- [ ] 1.4 Guarda de reavaliação na rota: solicitação com `decidido_em` já gravado recebe **409**
      e o desfecho original permanece. A regra não muda (design — decisão 3). A trilha de
      auditoria vem do `MiddlewareDeAuditoria`, sem código na rota (`RN-02-21`).

## 2. Testes do núcleo

- [ ] 2.1 Em `backend/tests/test_fila_rota.py`, os cenários da leitura: Admin lê a fila; a
      solicitação de Apoiador traz aporte declarado, nick pretendido e indicação de
      comprovante; a de prazo vencido vem marcada em atraso com a situação ainda **recebida**;
      a já avaliada traz o desfecho e não vem em atraso; Mestre, Apoiador, Guerreiro(a) e
      responsável recebem 403; e o conteúdo do comprovante não sai em campo algum
      (`RF-02-18`, `RF-02-65`, `RF-02-83`, `RN-01-28`).
- [ ] 2.2 Ainda em `backend/tests/test_fila_rota.py`, os cenários do desfecho: Admin aceita e
      **nenhuma persona é criada**; Admin recusa com o motivo no parecer; desfecho fora de
      aceita ou recusada recebe 422; segundo desfecho sobre solicitação já avaliada recebe 409
      com o original intacto; Mestre recebe 403 (`RF-02-19`, `RF-02-86`, `RN-01-03`,
      `RN-02-03`).
- [ ] 2.3 Ainda em `backend/tests/test_fila_rota.py`, o cenário da auditoria: o desfecho
      aparece na trilha com autor, papel, data e hora (`RN-02-21`).

## 3. Área Filas na App 03

- [ ] 3.1 `apps/app-03-gestao/src/filas/api.ts`: cliente da leitura e do desfecho, sobre o
      cliente de API existente.
- [ ] 3.2 `apps/app-03-gestao/src/filas/TelaDeFilas.tsx` e `ListaDeFilas.tsx`: lista única com
      **filtro por natureza** — montado desde já, servindo só participação nesta fatia
      (design — decisão 5) —, cada item com natureza, quem enviou, situação e prazo, e o
      atraso anunciado por **rótulo textual**, nunca só por cor. Consome a camada de
      `comum/react/`. Quem não é Admin lê a recusa em linguagem simples (`RF-02-18`,
      `RF-02-65`, `RF-02-25`, `RN-02-01`, documento 15 §5).
- [ ] 3.3 Registro da área em `App.tsx`, como quinta área da navegação.
- [ ] 3.4 `apps/app-03-gestao/src/filas/AvaliacaoDaSolicitacao.tsx`: detalhe com identificação,
      pretensão, apresentação, instituição, links e, no pré-cadastro, aporte declarado e nick
      pretendido; desfecho de aceitar ou recusar com parecer, exigido no próprio campo antes de
      chamar o núcleo; solicitação já avaliada mostra o desfecho e não oferece reavaliação. O
      comprovante aparece como **existente e ainda não exibível**, sem silenciar sobre ele
      (`RF-02-19`, `RF-02-83`, `RF-02-86`).

## 4. Encaminhamento ao cadastro e homologação do aporte

- [ ] 4.1 A solicitação aceita oferece abrir o cadastro de Mestre ou Apoiador conforme a
      pretensão, levando os dados da solicitação como **valores iniciais editáveis** aos
      formulários de `src/personas/` — sem rota nova no núcleo e sem mudar o contrato dos
      formulários (design — decisão 4). Aceitar, por si só, não cria persona alguma
      (`RF-02-20`, `RN-02-03`, `RN-01-28`).
- [ ] 4.2 Homologação do aporte declarado sobre `POST /aportes` com
      `solicitacao_de_participacao_id`, apresentando depois o valor **em moedas** e nunca em
      reais; recusa por solicitação já homologada explicada em linguagem simples, e o caminho
      deixa de ser oferecido depois da homologação (`RF-02-84`, `RF-07-30`, `RN-02-19`,
      `RN-07-21`).

## 5. Testes da App 03

- [ ] 5.1 `apps/app-03-gestao/src/filas/filas.test.tsx`, cenários da lista e do desfecho: a
      área abre com o filtro por natureza; o atraso aparece por rótulo legível sem cor; o
      Mestre lê a recusa em linguagem simples, não um erro cru; aceitar com parecer mostra o
      desfecho registrado; recusar com parecer vazio aponta o campo sem chamar o núcleo;
      solicitação já avaliada não oferece desfecho (`RF-02-18`, `RF-02-19`, `RF-02-65`,
      `RF-02-86`, `RN-02-01`).
- [ ] 5.2 Ainda em `filas.test.tsx`, cenários do encaminhamento e da homologação: aceitar não
      cadastra ninguém; o formulário de Apoiador abre pré-preenchido e editável; o cadastro
      pré-preenchido sem artefato comprobatório é apontado e não é criado; a homologação mostra
      o valor em moedas e nenhum valor em reais; solicitação já homologada não oferece
      homologar de novo (`RF-02-20`, `RF-02-04`, `RF-02-84`, `RN-02-19`).

## 6. Documentação

- [ ] 6.1 Nenhum documento de `docs/` muda: a change não toma decisão nova, não altera
      requisito de PRD, não muda a situação de nenhum PRD, não muda relação entre documentos e
      não cria arquivo em `docs/`. A duplicidade de `RF-02-93`, decidida em 2026-08-22, é
      corrigida na change `avaliacao-de-dados-de-chave-e-de-sugestao`, que implementa o
      requisito afetado.
