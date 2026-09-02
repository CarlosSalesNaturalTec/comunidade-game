## 1. Área detalhada de direitos e dados

- [ ] 1.1 Criar `apps/app-08-apoiador/src/direitos/ContextoDeDireitos.tsx` com o provedor e o
      `useDireitos`, no mesmo desenho das Apps 03 e 09, e verificar que o `useDireitos` fora do
      provedor lança erro (`RF-14-58`)
- [ ] 1.2 Criar `apps/app-08-apoiador/src/direitos/TelaDeDireitos.tsx` de leitura, com a tabela
      da PRD-14 §11 — dado, finalidade, base legal, retenção e quem acessa — e a declaração de
      que acesso, correção e exclusão são pedidos à gestão; a ação de sair só aparece com
      sessão; verificar que a tela não tem formulário nem ação de escrita (`RF-14-58`)
- [ ] 1.3 Criar `apps/app-08-apoiador/src/direitos/AvisoDeColeta.tsx`, com `role="status"`, que
      nomeia o dado da tela e leva à área detalhada, sem bloquear nem pedir confirmação, e
      acrescentar as classes `cg-aviso-de-coleta`, `cg-aviso-de-coleta__botao` e
      `cg-tabela-de-direitos` a `apps/app-08-apoiador/src/index.css` (`RF-14-58`)

## 2. Área de propostas de evolução

- [ ] 2.1 Criar `apps/app-08-apoiador/src/propostas/api.ts` com `registrarProposta`
      (`POST /v1/sugestoes`, `alvo_tipo: "plataforma"`) e `listarMinhasPropostas`
      (`GET /v1/sugestoes/minhas`), sem expor o parecer interno da gestão (`RF-14-56`,
      `RF-14-57`, design — decisão 1)
- [ ] 2.2 Criar `apps/app-08-apoiador/src/propostas/TelaDePropostas.tsx` com o registro em
      texto, a lista das próprias propostas com o status, o motivo do retorno quando não
      adotada e a declaração de que o retorno chega na plataforma; sem promessa de ponto,
      badge, moeda, selo ou nível, e sem destinatário ou campo de resposta (`RF-14-56`,
      `RF-14-57`, `RN-14-26`, `RN-14-27`, `RN-14-29`, `RF-14-59`)

## 3. Ligação na aplicação

- [ ] 3.1 Em `apps/app-08-apoiador/src/App.tsx`, envolver a árvore com sessão e a sem sessão no
      `ProvedorDeDireitos` e acrescentar as áreas "Propostas" e "Direitos e dados" à navegação,
      verificando pela navegação renderizada (`RF-14-56`, `RF-14-58`)
- [ ] 3.2 Acrescentar o `AvisoDeColeta`, nomeando o dado de cada tela, às nove telas que gravam
      dado: pré-cadastro, troca da senha provisória, identidade pública, comprobatórios,
      declaração de aporte, cobertura de missão, proposta de desafio extra, favorito e proposta
      de evolução (`RF-14-58`)

## 4. Testes

- [ ] 4.1 `apps/app-08-apoiador/src/direitos/direitos.test.tsx`: a área lista destino e uso de
      cada dado e declara que os direitos correm pela gestão; o aviso nomeia o dado, leva à
      área detalhada, não bloqueia a tela e não impede o envio do formulário (`RF-14-58`)
- [ ] 4.2 `apps/app-08-apoiador/src/propostas/propostas.test.tsx`: a proposta entra na fila
      única e passa a aparecer na lista; a não adotada mostra o motivo em linguagem simples; a
      tela não promete e-mail, ponto, badge nem moeda (`RF-14-56`, `RF-14-57`, `RN-14-26`,
      `RN-14-27`)
- [ ] 4.3 `apps/app-08-apoiador/src/testes/canalFechado.test.tsx`: renderiza as telas da
      aplicação e falha se aparecer campo de mensagem ou rótulo de telefone ou e-mail de
      Guerreiro(a), família ou Mestre — critério de aceite da PRD-14 §12 (`RF-14-59`,
      `RN-14-20`, `RN-14-24`)
- [ ] 4.4 `apps/app-08-apoiador/src/preCadastro/preCadastro.test.tsx`: a porta pública traz o
      aviso e alcança a área detalhada sem sessão (`RF-14-58`)

## 5. Documentação

- [ ] 5.1 Marcar a fatia 8 do PRD-14 como implementada em `openspec/cronograma-de-fatias.md`,
      com o slug da change. Nada muda em `docs/`: não houve decisão nova, o PRD-14 segue
      aprovado com a fatia 9 em aberto, nenhuma relação entre documentos mudou e nenhum arquivo
      nasceu em `docs/`
