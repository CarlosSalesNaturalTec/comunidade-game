## 1. Aviso de coleta e área de direitos

- [x] 1.1 Criar `apps/app-03-gestao/src/direitos/AvisoDeColeta.tsx`: aviso discreto
      parametrizado pelo dado da tela, com o acesso à área Direitos e dados, sem bloquear a
      tela nem exigir confirmação; estilo em `apps/app-03-gestao/src/index.css`, sem cor como
      único sinal (`RF-02-64`).
- [x] 1.2 Criar `apps/app-03-gestao/src/direitos/TelaDeDireitos.tsx` com a tabela do PRD-02 §11
      — dado, finalidade, base legal, retenção e quem acessa — e as quatro declarações da §11:
      a gestão não vê a imagem, o responsável exerce os direitos pela App 07, o registro do
      território é despersonalizado e não apagado, e a infração fica restrita à gestão e ao
      responsável. Área de leitura, sem escrita, exclusão ou exportação (`RF-02-64`).
- [x] 1.3 Registrar a área `direitos` em `apps/app-03-gestao/src/App.tsx` — chave, rótulo
      "Direitos e dados" e navegação —, e ligar o acesso do aviso a ela (`RF-02-64`).

## 2. O aviso nas telas que gravam dado pessoal

- [x] 2.1 Pôr o aviso nos cadastros de `apps/app-03-gestao/src/personas/`:
      `FormularioDeGuerreiro`, `FormularioDeAdulto` com `FormularioDeArtefatos`,
      `FormularioDeAdmin` e `FormularioDeResponsavel`, cada um nomeando o dado da sua linha da
      §11 (`RF-02-64`).
- [x] 2.2 Pôr o aviso em `apps/app-03-gestao/src/lancamentos/`: `ConferenciaDePresencas`,
      `LancamentoDaAtividade` e `RegistroDeInfracao` — presença e resultado de atividade num
      caso, infração e pontuação negativa no outro (`RF-02-64`).
- [x] 2.3 Pôr o aviso em `apps/app-03-gestao/src/painel-do-dia/AnexoDaDigitalizacao.tsx`, sobre
      o termo assinado no encontro (`RF-02-64`).
- [x] 2.4 Pôr o aviso em `apps/app-03-gestao/src/filas/AvaliacaoDaSolicitacao.tsx` e
      `AvaliacaoDeDados.tsx`, sobre a solicitação de participação e a solicitação de dados
      (`RF-02-64`).

## 3. As guardas do consentimento e da autoria

- [x] 3.1 Conferir e assegurar em `apps/app-03-gestao/src/lancamentos/` que a lista é a do
      encontro inteiro: nenhum filtro, marcação ou ação por consentimento em
      `TelaDeLancamentos`, `ConferenciaDePresencas`, `LancamentoDaAtividade` e
      `RegistroDeInfracao` (`RN-02-23`).
- [x] 3.2 Acrescentar em `apps/app-03-gestao/src/atividades/TelaDeAtividades.tsx` a linha que
      diz que ali se cadastra atividade avulsa, fora de trilha, e que a atividade de missão é
      autoria do Mestre, na App 09; conferir que
      `apps/app-03-gestao/src/territorio/ListaDeDesafiosPublicados.tsx` segue só de leitura
      (`RN-02-24`).

## 4. Testes

- [x] 4.1 `apps/app-03-gestao/src/direitos/direitos.test.tsx`: a área apresenta o destino de
      cada dado, declara que o dado do território é despersonalizado e não apagado, e não
      oferece escrita; o acesso a partir do aviso chega nela (`RF-02-64`).
- [x] 4.2 Estender `personas.test.tsx`, `lancamentos.test.tsx`, `painel-do-dia.test.tsx` e
      `filas.test.tsx`: cada tela que grava dado pessoal exibe o aviso nomeando o dado dela, e
      o formulário se preenche e se envia sem confirmar o aviso (`RF-02-64`).
- [x] 4.3 Em `lancamentos.test.tsx`, cobrir o `RN-02-23`: Guerreiro(a) cujo responsável recusou
      a autorização aparece na lista e tem o desfecho lançado como qualquer outro, e nenhuma
      das três telas oferece filtro, marcação ou ação que o retire por consentimento
      (`RN-02-23`).
- [x] 4.4 Em `atividades.test.tsx` e `territorio.test.tsx`, cobrir o `RN-02-24`: a área
      Atividades cadastra apenas atividade avulsa e diz onde a atividade de missão se faz, e os
      desafios de coleta publicados não têm caminho de criação nem de edição (`RN-02-24`).

## 5. Documentação

- [x] 5.1 `openspec/cronograma-de-fatias.md`: o recorte já foi corrigido ao abrir a change —
      resta marcar a fatia 13 do PRD-02 como `implementado` ao arquivar.
- [x] 5.2 `docs/09-topicos-em-aberto-e-sugestoes.md`: gravar a decisão do fundador —
      **processos de auditoria ainda não implementados vão ao Ciclo 02**, com a exceção do
      `RF-13-30` (histórico de acessos do responsável), que permanece no Ciclo 01 — e registrar
      como pendência do Ciclo 02 as três consequências no que já está implementado: o registro
      de coleta "a conferir" que fica sem validação do Mestre, a despublicação de trilha sem
      tela, e a trilha de auditoria sem consumidor na gestão.
- [x] 5.3 `docs/prds/prd-02-frontend-de-gestao.md`: a §3.2 recebe a exclusão dos recortes de
      auditoria adiados, a §13 recebe a decisão com a linha do documento 09, e a §14 registra o
      que ficou pendente por causa dela. Na §14 do PRD-09, registrar o adiamento do `RF-09-35`,
      do `RN-09-21` e do `RF-09-48`. O PRD-13 não muda: o histórico de acessos fica no Ciclo 01.
- [x] 5.4 `docs/prds/index.md`: atualizar a coluna de situação do PRD-02 e do PRD-09 se a
      decisão a mudou — a coluna da tabela, nunca parágrafo novo. Nenhum arquivo novo em
      `docs/`, logo a `nav` do `mkdocs.yml` não muda; conferir os invariantes do documento 99
      §6 e atualizar o documento 99 apenas se alguma relação entre documentos mudou.
