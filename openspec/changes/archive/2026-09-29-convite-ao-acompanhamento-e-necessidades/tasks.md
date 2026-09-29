# Tasks

## 1. Leitura das necessidades

- [x] 1.1 Acrescentar em `apps/app-06-vitrine/src/api/leituras.ts` o tipo e a leitura de
      `GET /v1/vitrine/necessidades`, com tipo de recurso, quantidade faltante, valor em moedas
      (`null` possível), comunidade, ponto de apoio e início e fim da aula (`RF-03-47`)
- [x] 1.2 Criar `necessidades/useNecessidades.ts` com a memorização em memória por carga, no
      padrão de `useConteudoInstitucional`, compartilhada pela porta e por "Como apoiar"
      (`RF-03-47`, design — decisão 5)
- [x] 1.3 Criar `necessidades/ListaDeNecessidades.tsx`: item por necessidade com rótulo e valor,
      data e horário da aula formatados, valor em moedas com duas casas e a linha sem moedas
      quando o núcleo não manda valor; nenhum campo em reais, nenhuma pessoa, e a frase de lista
      vazia (`RF-03-47`, `RF-03-10`, `RN-03-18`, design — decisão 6)

## 2. A porta do convite

- [x] 2.1 Criar `convite/PortaDoConvite.tsx` em `/quero-participar`, sem propriedade de origem:
      o que é ser Apoiador — aportar, propor desafios extras, acompanhar favoritos —, a
      declaração de que nada ali cria cadastro nem acesso, que um Admin avalia e que o prazo é de
      7 dias (`RF-03-42`, `RN-03-17`, design — decisões 1 e 3)
- [x] 2.2 Entregar o garfo `convite/modalidades.ts` e a pergunta na abertura da porta: as sete
      respostas do documento 14 §10, cada uma com o comprobatório nomeado, encaminhando dinheiro
      ao pré-cadastro da App 08 e as demais a `/participar`, sem guardar a escolha (`RF-03-42`,
      design — decisão 2)
- [x] 2.3 Entregar na porta os dois caminhos sem cadastro: a chave PIX, pela leitura institucional
      já memorizada de "Como apoiar", e a lista de necessidades em aberto (`RF-03-43`, `RF-03-46`,
      `RF-03-47`)
- [x] 2.4 Entregar a saída da recusa: `voltar()` em `navegacao/useNavegacao.ts`, com
      `history.back()` quando esta carga já empilhou endereço e `irPara("/")` quando a porta foi
      aberta direto, sem nada guardado no aparelho (`RF-03-44`, `RF-03-38`, `RN-03-15`,
      design — decisão 4)

## 3. A chamada nas páginas individuais

- [x] 3.1 Criar `convite/ChamadaDeParticipacao.tsx` — a chamada "Quero participar" e a ação de
      acompanhar, as duas levando a `/quero-participar` sem passar nick, identificador ou nome, e
      o texto do convite do projeto, que não vincula apoio a quem está na tela (`RF-03-39`,
      `RF-03-40`, `RF-03-41`, `RN-03-25`)
- [x] 3.2 Montar a chamada em `guerreiros/PaginaDoGuerreiro.tsx` e em
      `territorio/PaginaDaComunidade.tsx`, que passa a receber `irPara` (`RF-03-39`,
      design — decisão 7)

## 4. Ligação das telas

- [x] 4.1 Ligar o caminho `/quero-participar` em `navegacao/caminhos.ts` e em `App.tsx`, no padrão
      das demais telas de endereço próprio (`RF-03-42`)
- [x] 4.2 Trocar em `institucional/SecoesInstitucionais.tsx` a frase pendente de "Como apoiar"
      pelo bloco de necessidades em aberto (`RF-03-47`, design — decisão 8)

## 5. Testes

- [x] 5.1 Em `apps/app-06-vitrine/src/testes/convite.test.tsx`: a chamada e a ação de acompanhar
      nas páginas do Guerreiro(a) e da comunidade levando à mesma porta; a porta sem citar quem
      estava sendo visto e com endereço sem parâmetro; o papel do Apoiador, a declaração de que
      nada cria cadastro nem acesso e o prazo de 7 dias; a saída devolvendo à navegação
      (`RF-03-39` a `RF-03-44`, `RN-03-17`, `RN-03-25`)
- [x] 5.2 Em `apps/app-06-vitrine/src/testes/garfoDeModalidade.test.tsx`: dinheiro encaminhando ao
      pré-cadastro da App 08 com o comprovante nomeado, cada uma das outras seis modalidades
      encaminhando a `/participar` com o comprobatório dela, e a escolha esquecida na recarga
      (`RF-03-42`)
- [x] 5.3 Em `apps/app-06-vitrine/src/testes/necessidadesEmAberto.test.tsx`: a necessidade com os
      sete campos na porta e em "Como apoiar", nenhuma linha com reais nem pessoa, tipo sem
      vigência sem valor em moedas, e a frase de nenhuma necessidade em aberto (`RF-03-47`,
      `RF-03-10`, `RN-03-18`)
- [x] 5.4 Estender `apps/app-06-vitrine/src/testes/semRastro.test.tsx`: acompanhar, escolher
      modalidade e recusar o convite deixam `localStorage`, `sessionStorage` e cookie vazios, e a
      vitrine recarregada fica idêntica à primeira visita (`RF-03-38`, `RN-03-15`, `RN-03-16`)

## 6. Documentação

- [x] 6.1 Acrescentar ao PRD-03 §6.4 o requisito do garfo de modalidade na porta, aplicando a
      decisão já registrada nos documentos 02 §1, 14 §§10 e 11 e 09 §1 ("Já decididos"), com a
      linha correspondente na rastreabilidade da §15 (`RF-03-42`)
- [x] 6.2 Marcar a fatia 6 do PRD-03 como implementada em `openspec/cronograma-de-fatias.md`, com
      o slug da change, o `RF-03-39` declaradamente parcial — Mestre e Apoiador na fatia 7, poder
      sem página individual — e as decisões do fundador de 2026-09-29. `docs/prds/index.md`, o
      documento 09, o documento 99 e a `nav` do `mkdocs.yml` não mudam: nenhum arquivo nasce em
      `docs/`, nenhuma decisão nova foi tomada e nenhuma relação entre documentos muda
