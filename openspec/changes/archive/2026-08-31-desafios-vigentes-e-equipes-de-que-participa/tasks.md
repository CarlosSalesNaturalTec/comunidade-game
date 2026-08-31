## 1. Núcleo — regra

- [x] 1.1 `RF-05-19`: acrescentar em `trilhas/regra.py` a derivação dos desafios em aberto do
      Guerreiro(a) — inscrições, missões com desbloqueio aprovado, atividades dessas missões,
      subtraídas as que já têm `Resultado` dele (design — decisão 1), sem alcançar a atividade
      avulsa (design — decisão 2). Verificar por `uv run pytest tests/test_meus_desafios.py -x`.
- [x] 1.2 `RF-05-22`, `RF-05-24`: acrescentar em `equipes/regra.py` a consulta das equipes de
      que a persona em sessão é integrante — da aula e da trilha —, com o papel dela em cada
      uma, sem nenhuma escrita (`RN-05-12`, design — decisão 4). Verificar por
      `uv run pytest tests/test_minhas_equipes.py -x`.
- [x] 1.3 `RF-05-22`: acrescentar em `equipes/regra.py` a derivação das atividades de cada
      equipe — a programação do encontro na equipe da aula, as atividades das missões da trilha
      publicada na equipe da trilha (design — decisão 5), reaproveitando
      `programacao_do_encontro` onde ela já serve.

## 2. Núcleo — rotas

- [x] 2.1 `RF-05-19`, `RN-05-21`: expor `GET /v1/eu/desafios` em `trilhas/rotas.py`, com
      modalidade, formato, produção esperada, missão e trilha de cada desafio, restrita ao
      Guerreiro(a) da sessão pelo contexto e com 403 para as demais personas.
- [x] 2.2 `RF-05-22`, `RF-05-23`, `RN-05-15`: expor `GET /v1/eu/equipes` em `equipes/rotas.py`,
      estendendo `saida_da_equipe` com o papel da persona em sessão e as atividades da equipe,
      mantendo o integrante restrito a avatar e nick (design — decisão 4).

## 3. Núcleo — testes

- [x] 3.1 `RF-05-19`: criar `tests/test_meus_desafios.py` cobrindo os cenários da spec de
      `area-do-guerreiro` — atividade de missão desbloqueada devolvida com modalidade e
      formato, missão ainda bloqueada fora, atividade com `Resultado` lançado fora, trilha não
      inscrita fora, conjunto vazio com 200 e 403 para persona que não é Guerreiro(a).
- [x] 3.2 `RF-05-22`, `RF-05-23`, `RF-05-24`: criar `tests/test_minhas_equipes.py` cobrindo os
      cenários da spec de `equipe` — equipe de aula e de trilha na mesma leitura com papel e
      atividades, corrente marcada na programação do encontro, só avatar e nick, equipe que não
      integra fora, conjunto vazio com 200 e nenhuma escrita pela leitura (`RN-05-12`,
      `RN-05-21`).

## 4. App 05 — Área do Guerreiro(a)

- [x] 4.1 `RF-05-19`, `RF-05-22`: criar `src/api/desafiosEEquipes.ts` com os dois clientes de
      leitura e os tipos das duas saídas, no molde de `src/api/trilha.ts`.
- [x] 4.2 `RF-05-19`, `RN-05-06`: criar `src/desafios/MeusDesafios.tsx` — cada desafio com
      modalidade e formato em linguagem da criança, a produção esperada e a missão e trilha de
      origem; sem desafio em aberto, a mensagem que explica, nunca lista vazia muda; nenhuma
      ação de lançar resultado, presença ou mérito.
- [x] 4.3 `RF-05-22`, `RF-05-23`, `RF-05-24`: criar `src/desafios/MinhasEquipes.tsx` — as
      equipes com papel e atividades, integrantes por avatar e nick, a mensagem de onde a
      equipe se forma quando não integra nenhuma, e nenhuma ação de formar, editar, entrar,
      sair ou homologar (`RN-05-12`, `RN-05-15`).
- [x] 4.4 `RF-05-19`, `RF-05-22`: criar `src/desafios/DesafiosEEquipes.tsx` com as duas abas, no
      molde de `Carteira.tsx`, e ligá-lo como bloco novo na navegação de `AreaDoGuerreiro.tsx`
      (design — decisão 6).
- [x] 4.5 `RF-05-19`, `RF-05-22`, `RF-05-23`, `RN-05-22`: escrever os testes dos três
      componentes (`MeusDesafios.test.tsx`, `MinhasEquipes.test.tsx`,
      `DesafiosEEquipes.test.tsx`) cobrindo os cenários das specs, inclusive a ausência de
      qualquer canal de conversa nas duas telas.

## 5. Documentação

- [x] 5.1 Marcar a fatia 6 do PRD-05 como implementada em
      `openspec/cronograma-de-fatias.md`, com o slug desta change, e trocar no recorte daquela
      linha o `RN-05-23` pelo `RN-05-12`, conforme a decisão do fundador registrada na
      proposal. Nada mais muda em `docs/`: nenhuma decisão nova de produto, nenhum arquivo
      novo, e a situação do PRD-05 em `docs/prds/index.md` segue "aprovado".
