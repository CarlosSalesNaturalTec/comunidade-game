# Tasks

## 1. A projeção de carta no núcleo

- [x] 1.1 Em `backend/src/nucleo/vitrine/publico.py`, acrescentar à projeção pública a
      composição da carta — badges com família e poder, poderes com nível, desempenho (posição e
      pontos regulares) e criações creditadas com trilha e data —, montada em **consultas por
      conjunto de identificadores**, no molde de `buscar_avatares_e_nicks`, sem N+1 e sem tocar
      na projeção mínima `AvatarENickSaida` que a autoria e o contrato dos jogos usam
      (`RF-01-21`, `RF-01-33`, `RN-01-10`, `RN-01-11`, design — decisões 1, 2 e 4)
- [x] 1.2 Resolver o **nome do poder** e a **família do badge** no núcleo, a partir do vínculo
      trilha–poder que `/vitrine/poderes` já expõe, para que nível e badge saiam nomeados e não
      como `trilha_id` cru (`RF-03-05`, design — decisão 2)
- [x] 1.3 Derivar o desempenho de `pontuacao.regra.consulta_de_ranking(exigir_divulgacao=True)`,
      a mesma derivação de `/vitrine/rankings`, respeitando o filtro de comunidade da consulta
      para que posição e listagem nunca discordem (`RF-03-05`, `RF-03-09`, design — decisão 3)
- [x] 1.4 Em `backend/src/nucleo/vitrine/rotas.py`, fazer `GET /vitrine/guerreiros` e
      `GET /vitrine/guerreiros/{nick}` devolverem a **mesma** composição, mantendo a paginação, o
      filtro de comunidade, o portão da divulgação e o 404 indistinto da rota por nick
      (`RF-03-03`, `RF-03-05`, `RF-03-13`, `RN-03-02`, `RN-03-07`)
- [x] 1.5 Acrescentar a `GET /vitrine/criacoes` a **data de validação** e o **nome da trilha** de
      cada criação, sem campo de título — que o modelo não tem —, mantendo a condição de todos os
      creditados autorizados (`RF-03-08`, `RN-03-02`, decisão do fundador, 2026-09-28)

## 2. Testes do núcleo

- [x] 2.1 Em `backend/tests/test_vitrine.py`, cobrir a projeção nova com os critérios de aceite
      do PRD-03 §12: o card traz a composição inteira e a página por nick traz a mesma; uma
      página de cards sai de uma resposta só; Guerreiro(a) sem autorização não aparece em card,
      página, portfólio nem ranking, nem por endereço direto; revogada a autorização, a leitura
      seguinte já não o alcança; nick inexistente e nick sem autorização devolvem o mesmo 404; e
      nenhuma resposta traz nome civil, nascimento, contato, imagem real ou valor em reais
      (`RF-03-05`, `RF-03-13`, `RF-03-14`, `RN-03-02`, `RN-03-03`, `RN-03-04`, `RN-03-07`)
- [x] 2.2 No mesmo arquivo, cobrir que a **projeção mínima não mudou** onde ela vale — autoria
      creditada nas criações e elenco dos jogos seguem com avatar e nick — e que a criação
      pública passou a trazer data e nome da trilha, sem título (`RF-03-08`, `RN-01-11`,
      invariante 8 do documento 99 §6)

## 3. A seção de Guerreiros e Guerreiras na App 06

- [x] 3.1 Em `apps/app-06-vitrine/src/api/`, declarar as leituras da fatia sobre
      `lerDoNucleo` — cards, perfil por nick, criações, ranking e poderes —, com os tipos da
      composição nova e sem credencial de persona (`RN-03-33`)
- [x] 3.2 Implementar a seção **Guerreiros e Guerreiras** com `SequenciaPaginada` de
      `comum/react` e a posição comandada de fora: temporizador de 5 s avança, os controles do
      paginador deixam o visitante avançar sozinho, e `prefers-reduced-motion` não arma o
      temporizador — a rotação nunca é a única via ao conteúdo (`RF-03-02`, `RF-03-04`,
      documento 15 §§5, 8.1, design — decisão 5)
- [x] 3.3 Apresentar cada Guerreiro(a) pela `CartaDoPersonagem` variante `guerreiro` de
      `comum/react`, sem componente de carta novo, e **sem apresentar carta pela metade**: a tela
      diz em uma frase o que tem quando a leitura não completa a variante (`RF-03-05`,
      `RF-03-06`, `RN-03-04`, documento 11 §8.2)

## 4. A página individual, a busca e o freio legível

- [x] 4.1 Estender `src/navegacao/recortes.ts` para reconhecer `/guerreiros/<nick>` antes de cair
      no recorte padrão, e implementar a página individual em endereço próprio, compartilhável e
      alcançável direto (`RF-03-03`, design — decisão 6)
- [x] 4.2 Implementar a busca por **nick exato**, sem sugestão, completação ou lista, com a
      **mesma** tela de "não encontrado" para nick inexistente e nick sem autorização
      (`RF-03-11`, `RF-03-12`, `RN-03-06`, `RN-03-07`)
- [x] 4.3 Tratar o freio por origem como resposta esperada: o `tempoDeEsperaEmSegundos` de
      `comum/api` vira motivo e espera em linguagem simples, sem CAPTCHA, cadastro ou login, e
      sem gravar no aparelho marca alguma de quem foi freado (`RF-03-36`, `RF-03-37`, `RN-03-08`,
      `RN-03-34`, design — decisão 8)

## 5. Portfólio, ranking e poderes na App 06

- [x] 5.1 Implementar o **portfólio** das criações autorizadas, cada uma com trilha, data e
      autoria por nick, e sem título enquanto o modelo não o tiver (`RF-03-08`, `RN-03-02`)
- [x] 5.2 Implementar o **ranking público** só com pontos regulares e só de quem autorizou, sem
      ponto extra, moeda ou valor em reais (`RF-03-09`, `RN-03-02`, invariante 16 do documento 99
      §6)
- [x] 5.3 Implementar a seção e a página de **poderes**, cada poder com as trilhas dele e sem
      espaço vazio ou promessa de Mestres responsáveis, que chegam com a fatia 7 (`RF-03-02`,
      decisão do fundador, 2026-09-28)

## 6. Testes da App 06

- [x] 6.1 Em `apps/app-06-vitrine/src/testes/`, cobrir a seção de cards e a página individual: os
      cards rotacionam a cada 5 s; com movimento reduzido não rotacionam e todos seguem
      alcançáveis; o card abre a página em endereço próprio; card e página exibem só o que a
      variante permite; e carta incompleta não se apresenta (`RF-03-02` a `RF-03-06`)
- [x] 6.2 Cobrir a busca e o freio: nick exato leva à página; parte de nick não sugere, não
      completa e não lista; nick inexistente e nick sem autorização produzem a mesma tela; e a
      repetição freada explica motivo e espera sem pedir CAPTCHA nem cadastro (`RF-03-11`,
      `RF-03-12`, `RF-03-36`, `RF-03-37`, `RN-03-06`, `RN-03-07`, `RN-03-08`)
- [x] 6.3 Cobrir portfólio, ranking, poderes e a ausência de rastro: a criação aparece com
      trilha, data e autoria; quem não autorizou não está em card, página, portfólio nem ranking;
      o ranking é de ponto regular; a seção de poderes traz as trilhas sem prometer Mestres; e,
      percorrida a visita inteira, nada fica em `localStorage`, `sessionStorage` ou cookie
      (`RF-03-02`, `RF-03-08`, `RF-03-09`, `RF-03-13`, `RF-03-14`, `RN-03-02`, `RN-03-03`)

## 7. Documentação

- [x] 7.1 Fechar a **linha 2** do PRD-03 em `openspec/cronograma-de-fatias.md`: situação
      `implementado` e o slug da change no lugar do recorte — o recorte corrigido (a fatia leva
      núcleo, entrega a seção de poderes sem os Mestres e sai sem título no `RF-03-08`) já entrou
      na linha ao abrir a change. Ajustar a frase de fechamento do bloco, que hoje diz que só as
      fatias 5, 7 e 8 levam rota nova e só a 3 leva delta de spec
- [x] 7.2 Registrar em `docs/09-topicos-em-aberto-e-sugestoes.md` §1, em "Já decididos", as duas
      decisões do fundador de 2026-09-28 — a **projeção pública do Guerreiro(a) passa a ser a
      carta inteira nas duas rotas**, e o **portfólio sai com trilha, data e autoria, sem
      título**, porque a criação original não tem esse campo no modelo
- [x] 7.3 Registrar o **título da criação original** como pendência, na §14 do PRD-03 e na tabela
      do documento 09: nenhum documento-fonte o define, e é o que trava o `RF-03-08` por
      inteiro. `docs/prds/index.md` não muda — o PRD-03 segue `aprovado` enquanto houver fatia em
      aberto. Nenhum arquivo novo em `docs/`, nada a mudar no documento 99 nem na `nav` do
      `mkdocs.yml`
