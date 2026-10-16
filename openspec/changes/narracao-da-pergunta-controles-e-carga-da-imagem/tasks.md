# Tasks

A ordem dos grupos é a dependência entre os componentes (design — Migration Plan): a moldura e o
paginador antes de quem os usa.

## 1. A moldura de mídia parte do zero a cada item (`RF-05-11`, `RF-09-119`)

- [ ] 1.1 Em `comum/react/MidiaDoNucleo.tsx`, trocar `endereco` e `naoAbriu` por **um estado só**
      que guarda o `id` buscado junto do endereço e da falha (design — decisão 6); `id` da
      propriedade diferente do guardado significa carregando. Verificar que a moldura diz
      "Carregando…" nesse estado e que nem a mídia nem a falha do item anterior aparecem.
- [ ] 1.2 Na mesma, aceitar `aoMudarCarregamento?: (carregando: boolean) => void` e reportar fim
      de carga **também** na falha da busca e na limpeza da desmontagem (design — decisão 7, as
      duas quedas obrigatórias). Verificar que a desmontagem reporta `false`.
- [ ] 1.3 Em `comum/react/MidiaDoNucleo.test.tsx`, cobrir: a troca de `id` não deixa a mídia
      anterior na tela e mostra "Carregando…"; a falha de um item não acompanha o item seguinte;
      a falha reporta fim de carga; a desmontagem reporta fim de carga. Cenários "A mídia do item
      anterior não fica na tela", "O erro de um item não gruda no seguinte" e "Mídia que não abre
      libera a navegação" da spec `area-do-guerreiro`.

## 2. O paginador perde a posição e ganha ações e trava (`RF-05-11`, `RF-04-35`, `RF-05-89`, `RN-05-45`)

- [ ] 2.1 Em `comum/react/SequenciaPaginada.tsx`, remover o parágrafo da posição e a propriedade
      `nome`, que só existia para montá-lo (design — decisão 3). Verificar que nenhuma contagem
      aparece na tela nem é anunciada.
- [ ] 2.2 Na mesma, aceitar `acoes?: ReactNode` dentro de `cg-sequencia__controles` e passar a
      guarda `itens.length > 1` a valer **só** para avançar e voltar: havendo `acoes`, a linha
      renderiza com um item só (design — decisão 4). Verificar o caso de **um** item com `acoes`.
- [ ] 2.3 Na mesma, aceitar `controlesTravados?: boolean` que desabilita avançar e voltar **sem**
      travar as `acoes`, que têm condição própria (design — decisão 7).
- [ ] 2.4 Em `comum/react/estilos.css`, remover a regra `.cg-sequencia__posicao` e dar à linha de
      controles o arranjo que acomoda as ações ao lado de avançar e voltar.
- [ ] 2.5 Em `comum/react/SequenciaPaginada.test.tsx`, retirar as asserções da frase de posição e
      cobrir: nada de posição é apresentado; `acoes` aparecem na linha de controles; um item só
      com `acoes` renderiza a linha; `controlesTravados` desabilita avançar e voltar e **não** as
      ações.

## 3. O desafio fala a pergunta e condiciona o envio (documento 15 §5.1, `RF-05-89`, `RN-05-45`, `RF-09-119`)

- [ ] 3.1 Em `comum/trilha/DesafioDeDesbloqueio.tsx`, declarar o roteiro de narração da pergunta
      da vez — enunciado **e** alternativas, numa frase montada a partir do array da pergunta e
      entregue à síntese, sem entrar na tela —, disparado por `useRef` na troca de `pergunta.id`
      (design — decisões 1 e 2). Verificar que avançar e voltar falam a pergunta alcançada e que
      reapresentar o mesmo item não fala de novo.
- [ ] 3.2 Na mesma, derivar `todasRespondidas` no render e desabilitar "Enviar respostas" até que
      todas estejam respondidas, **só** para `tipo === "quiz"` — o desafio por declaração segue
      sempre disponível (design — decisão 5).
- [ ] 3.3 Na mesma, remover o estado `faltando`, o aviso "Falta responder N pergunta(s)", o salto
      até a primeira pendente e o uso da classe `cg-trilha__pergunta--falta`, que a condição do
      envio torna inalcançáveis; limpar a classe órfã de `comum/trilha/estilos.css` se ela estiver
      declarada lá.
- [ ] 3.4 Na mesma, passar o botão de enviar para `acoes` do paginador e ligar a trava: guardar o
      carregamento reportado por `MidiaDoNucleo` e repassá-lo como `controlesTravados`.
- [ ] 3.5 Em `comum/trilha/trilha.test.tsx`, retirar a asserção de "Pergunta 1 de 3" e cobrir os
      cenários da spec `area-do-guerreiro`: "Pergunta sem resposta é sinalizada", "Respondidas
      todas, enviar fica disponível", "Enviar aparece junto de avançar e voltar", "Quiz de uma
      pergunta oferece enviar", "O desafio por declaração não espera resposta", "A posição entre
      as perguntas não é declarada", "A pergunta alcançada é falada com as alternativas" e "A
      moldura diz que está carregando" no caminho do quiz.

## 4. Os demais chamadores do paginador (`RF-05-11`, `RF-04-35`)

- [ ] 4.1 Em `comum/trilha/Missao.tsx`, deixar de passar `nome` e ligar a trava de navegação ao
      carregamento da mídia do conteúdo, que tem o mesmo defeito do quiz (design — decisão 6).
- [ ] 4.2 Em `apps/app-01-aula-presencial/src/trilhas/TelaDaProgramacao.tsx`, deixar de passar
      `nome`. Verificar pela esteira de tipos que nenhum outro chamador ficou para trás.
- [ ] 4.3 Em `comum/trilha/trilha.test.tsx` e nos testes das trilhas da App 01, retirar a asserção
      de "Conteúdo 1 de 2" e cobrir os cenários "A posição na sequência não é declarada" e "A
      mídia do item anterior não fica na tela" no caminho do conteúdo da missão.

## 5. Documentação da change

- [ ] 5.1 Em `docs/15-identidade-visual.md` §6.4, registrar a decisão do fundador de 2026-10-16:
      a sequência **não declara a posição** do item, e o desafio que se envia inteiro só oferece o
      envio com tudo respondido. É a fonte única de "um conteúdo por vez" e hoje não trata nem de
      uma coisa nem de outra — sem isso a frase de posição volta por leitura futura. Conferir a
      linha de ~95 caracteres e os invariantes do documento 99 §6.
- [ ] 5.2 Em `docs/09-topicos-em-aberto-e-sugestoes.md` §1, acrescentar a linha da decisão nova,
      com as quatro partes e a data.
- [ ] 5.3 Em `openspec/cronograma-de-fatias.md`, marcar a fatia 28 do bloco PRD-04 como
      implementada. **Nada mais muda:** nenhum PRD é afetado — os enunciados alcançados não fixam
      posição em texto nem o salto até a pergunta pendente —, a situação do PRD-04 em
      `docs/prds/index.md` não muda, nenhum arquivo nasce em `docs/` (logo a `nav` do
      `mkdocs.yml` fica como está) e a relação entre documentos não muda (logo o documento 99
      também).
