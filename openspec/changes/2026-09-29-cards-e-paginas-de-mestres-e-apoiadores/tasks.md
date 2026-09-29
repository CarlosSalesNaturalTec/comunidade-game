# Tasks

## 1. As duas decisões novas, antes do código

- [ ] 1.1 Gravar no **documento 11 §8.2** as duas decisões do fundador de 2026-09-29: o
      **nome no lugar do nick** quando o adulto não tiver nick — nunca para Guerreiro(a) — e
      a **efetividade pública** do Apoiador com trilha, período e contagem de conclusões, sem
      alcançar quem concluiu. Verificar que a tabela das variantes Mestre e Apoiador passa a
      dizer as duas coisas em uma frase cada, sem repetir regra de outro documento
- [ ] 1.2 Mover as duas linhas correspondentes no **documento 09 §1** para "Já decididos",
      com a data e o documento-fonte; verificar que nenhuma pendência nova fica sem linha
- [ ] 1.3 Aplicar as duas decisões ao **PRD-03** — `RF-03-07` (identificação por nome quando
      não houver nick) e a linha do `RF-03-02` que descreve a página do Apoiador —, sem
      repetir o texto normativo do documento 11; verificar que o PRD só cita, não redefine

## 2. Leitura pública de Mestre (`leitura-publica-da-vitrine`)

- [ ] 2.1 Em `backend/src/nucleo/vitrine/publico.py`, a projeção pública do Mestre: avatar
      (com o padrão no lugar do que falte), identificação declarada como nick ou nome, áreas
      de habilidade derivadas da área do conhecimento das trilhas publicadas de autoria,
      artefatos comprobatórios com endereço e rótulo, trilhas de autoria e a contagem de
      absorções (`RF-03-02`, `RF-03-07`)
- [ ] 2.2 Em `backend/src/nucleo/vitrine/rotas.py`, `GET /vitrine/mestres` paginada e
      `GET /vitrine/mestres/{id}` por identificador, sem token de sessão e sem freio por
      origem próprio; persona que não é Mestre e identificador inexistente devolvem o mesmo
      404 (`RF-03-02`, `RF-03-07`, `RN-03-01`)

## 3. Leitura pública de Apoiador (`leitura-publica-da-vitrine`)

- [ ] 3.1 Na mesma `publico.py`, a projeção pública do Apoiador: identificação declarada,
      total em moedas por `moedas_acumuladas_de`, avatar resolvido pelo piso de 10 moedas com
      o sinal do avatar padrão, nível de sustento, selos e artefatos comprobatórios
      (`RF-03-10`, `RF-03-55`, `RF-03-56`, `RF-03-66`, `RN-03-18`)
- [ ] 3.2 Na mesma `publico.py`, a projeção pública da efetividade: desafios extras propostos
      pelo Apoiador com trilha, período de vigência e contagem de conclusões, sem nick, avatar
      ou dado de quem concluiu, e o direcionado só como "houve conclusão" (`RF-03-02`)
- [ ] 3.3 Em `rotas.py`, `GET /vitrine/apoiadores` e `GET /vitrine/apoiadores/{id}`, com o
      portão do **aporte homologado** — quem não tem fica fora da listagem e recebe o mesmo
      404 do inexistente — e ordem alfabética pela identificação, nunca por valor
      (`RF-03-57`, `RN-03-26`, `RN-14-38`)

## 4. Mestres responsáveis no catálogo de poderes

- [ ] 4.1 Em `rotas.py`, `GET /vitrine/poderes` passa a trazer, por poder, os autores das
      trilhas publicadas dele, deduplicados, cada um com identificador, avatar e identificação;
      poder sem trilha publicada sai com a lista vazia (`RF-03-02`)

## 5. Testes do núcleo

- [ ] 5.1 Em `backend/tests/test_vitrine.py`, os cenários de Mestre: listagem e leitura por
      identificador sem sessão, áreas vindas das trilhas de autoria sem repetição, ausência de
      e-mail, WhatsApp e canal de contato, e o 404 indistinto para persona de outro papel e
      identificador inexistente
- [ ] 5.2 No mesmo arquivo, os cenários de Apoiador: quem tem aporte homologado aparece, quem
      só tem declaração pendente não, o total sai em moedas sem campo algum em reais, abaixo
      do piso vale o avatar padrão, alcançado o piso vale o próprio, o direito não regride com
      ressarcimento pago, e a listagem não traz posição nem ordenação por valor
- [ ] 5.3 No mesmo arquivo, os cenários da identificação e da efetividade: adulto sem nick sai
      pelo nome declarado como nome, com nick sai pelo nick, Guerreiro(a) nunca sai por nome; e
      o desafio proposto sai com trilha, período e contagem, sem dado de quem concluiu e sem
      abrir o direcionado
- [ ] 5.4 No mesmo arquivo, os cenários dos poderes: poder com duas trilhas publicadas de
      Mestres diferentes traz os dois sem repetição, e poder sem trilha publicada traz a lista
      vazia

## 6. As duas variantes da carta (`camada-visual-comum`)

- [ ] 6.1 Em `comum/react/CartaDoPersonagem.tsx`, a variante **Mestre**, com os seis campos do
      documento 11 §8.2, o nome quando não houver nick — apresentado como nome —, o avatar
      padrão no lugar do que falte, a prova como link com rótulo, e `cartaEstaCompleta`
      estendida à variante (`RF-03-02`, `RF-03-07`)
- [ ] 6.2 No mesmo arquivo, a variante **Apoiador**, na moldura comum com avatar centralizado
      em proporção fixa, nick ou nome abaixo, total de moedas em destaque, avatar padrão
      abaixo do piso sem nenhuma outra marca de diferença, e nunca valor em reais (`RF-03-10`,
      `RF-03-55`, `RF-03-56`, `RF-03-66`, `RN-03-18`)
- [ ] 6.3 Em `comum/react/carta.test.tsx`, os cenários das duas variantes: os campos de cada
      uma, nome no lugar do nick ausente, avatar padrão por falta e por piso, moldura igual
      para logomarcas de proporções diferentes, ausência de reais, a efetividade sem quem
      concluiu, e a carta pela metade caindo em outra forma

## 7. Seções e páginas na App 06 (`aplicacao-da-vitrine`)

- [ ] 7.1 Em `apps/app-06-vitrine/src/`, o cliente das quatro rotas novas e a seção
      **Mestres**, com um card por Mestre e o card abrindo a página individual em endereço
      próprio (`RF-03-02`, `RF-03-03`)
- [ ] 7.2 A **página individual do Mestre**: habilidades, trilhas de autoria, a prova pública
      como link com rótulo e quantas vezes sustentou atividade sem recurso, sem ação alguma de
      edição (`RF-03-07`)
- [ ] 7.3 A seção **Apoiadores** e a **página individual do Apoiador**: aportes em moedas,
      nível de sustento, selos, desafios propostos com trilha, período e contagem, e a prova do
      apoio; ordem alfabética e nenhum Apoiador sem aporte homologado (`RF-03-02`, `RF-03-03`,
      `RF-03-07`, `RF-03-57`)
- [ ] 7.4 A chamada **"Quero participar"** e a ação de acompanhar nas duas páginas novas,
      levando à mesma porta `/quero-participar` que as duas já publicadas usam — fecha o
      `RF-03-39`, que saiu parcial da fatia 6, e o `RF-14-52`, cuja página pública do Mestre é
      esta (`RF-03-39`, `RF-03-40`)
- [ ] 7.5 Em `apps/app-06-vitrine/src/poderes/SecaoDePoderes.tsx`, os Mestres responsáveis de
      cada poder, cada um com link para a página individual dele, e nenhum espaço vazio no
      poder que não tem trilha publicada (`RF-03-02`)

## 8. Testes da App 06

- [ ] 8.1 Um arquivo de teste novo em `apps/app-06-vitrine/src/testes/` para as duas seções e
      as duas páginas: card abre a página em endereço próprio e o endereço aberto direto leva à
      mesma página, a prova sai como link com rótulo, a vitrine não oferece edição, Apoiador
      sem aporte homologado não aparece, a seção não é pódio, e a efetividade sai sem quem
      concluiu
- [ ] 8.2 Em `portfolioRankingEPoderes.test.tsx`, os Mestres responsáveis na seção de poderes,
      com link, e a ausência de espaço vazio no poder sem trilha publicada
- [ ] 8.3 Em `convite.test.tsx`, a chamada "Quero participar" e a ação de acompanhar nas
      páginas de Mestre e de Apoiador, chegando à mesma porta

## 9. Documentação

- [ ] 9.1 Marcar a **fatia 7 do PRD-03** como implementada em
      `openspec/cronograma-de-fatias.md`, com o slug da change e o que ela entregou de
      diferente do previsto; corrigir na mesma passada a linha da fatia 2 (Mestres
      responsáveis) e a da fatia 6 (`RF-03-39` deixa de ser parcial), e a nota do PRD-14 sobre
      a página pública do Mestre. `docs/prds/index.md` só muda se a situação do PRD-03 mudar —
      a coluna da tabela, nunca parágrafo novo. Sem arquivo novo em `docs/`, a `nav` do
      `mkdocs.yml` não muda; o documento 99 só muda se a relação entre documentos mudar
