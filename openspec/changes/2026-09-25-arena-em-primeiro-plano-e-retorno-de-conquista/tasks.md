# Tasks

## 0. Os insumos do fundador, recebidos ao iniciar a implementação

- [ ] 0.1 Receber do fundador as **imagens de comunidade** e a regra de uso delas — acervo do
      projeto, foto da comunidade registrada na plataforma ou ilustração no traço do documento 15 §2
      —, e gravar a regra no documento 15 §6 antes de usá-las. Porta da tarefa 2; não impede a 1.
- [ ] 0.2 Receber do fundador **quais fatos ganham retorno** entre missão desbloqueada, badge
      certificado, nível que subiu, ponto creditado e produção entregue, e gravar a decisão no
      documento 11 antes de implementá-la — é decisão de gamificação, e artefato do OpenSpec não a
      cria. Porta da tarefa 3; não impede a 1.
- [ ] 0.3 Conferir que a change da **carta do personagem** entrou — a tarefa 1 depende dela.

## 1. A carta domina a tela da Arena

- [ ] 1.1 Nas telas das Apps 01 e 05 que apresentam personagem, compor com a **carta como elemento
      maior** e uma decisão por tela, conforme a densidade baixa do documento 15 §6 (`RF-04-01`,
      design — decisão 4).
- [ ] 1.2 Em `apps/app-01-aula-presencial/src/index.css` e `apps/app-05-guerreiro/src/index.css`,
      acomodar a composição sem introduzir densidade da Operação e sem alterar o alvo de toque de
      `48` px.
- [ ] 1.3 Cobrir o cenário "A carta domina a tela da Arena" nos testes das duas aplicações.

## 2. Imagem de comunidade ao fundo — depende da tarefa 0.1

- [ ] 2.1 Acomodar a imagem ao fundo das telas da Arena, atrás da cor chapada, garantindo os pisos
      de contraste medidos sobre ela para texto, componente, borda que informa e estado de foco
      (design — decisão 3).
- [ ] 2.2 Garantir que nada do que a tela comunica se perca quando a imagem não carrega, e conferir
      o peso do arquivo contra o princípio 4 do documento 15 (design — decisões 3 e 5).
- [ ] 2.3 Cobrir os cenários "A imagem de fundo não come o contraste" e "A imagem de fundo não
      carrega informação".

## 3. Retorno de progresso e conquista — depende da tarefa 0.2

- [ ] 3.1 Implementar o retorno a `300` ms com `ease-in-out`, amarrado ao **fato** que o acontece —
      nunca à abertura da tela (design — decisões 1 e 2).
- [ ] 3.2 Garantir que o fato continue legível em texto, numeral ou forma sem o movimento, e que a
      preferência por menos movimento o suprima por completo (`RF-05-15`, `RF-05-16`, design —
      decisão 2).
- [ ] 3.3 Cobrir os cenários "A conquista devolve retorno, e o fato fica legível sem ele", "Menos
      movimento suprime o retorno sem esconder o fato" e "Não há retorno sem fato".

## 4. Documentação

- [ ] 4.1 Marcar a linha desta fatia como implementada em `openspec/cronograma-de-fatias.md`.
- [ ] 4.2 Conferir que as duas decisões recebidas na tarefa 0 estão gravadas no documento-fonte de
      cada uma — a imagem de comunidade no documento 15 §6, os fatos que ganham retorno no documento
      11 — e que cada uma moveu a linha dela no documento 09 §1, de pendente para decidida. Nada muda em `docs/prds/index.md`, no documento 99 nem na `nav`
      do `mkdocs.yml`, e nenhum arquivo nasce em `docs/`.
