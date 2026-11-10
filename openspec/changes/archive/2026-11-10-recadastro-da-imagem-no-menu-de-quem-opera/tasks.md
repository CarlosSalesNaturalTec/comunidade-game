# Tasks

## 1. O glifo

- [x] 1.1 Acrescentar o glifo `recadastro` a `comum/react/Icone.tsx` — quinas de enquadramento
      com um rosto dentro, traço `currentColor` e sem preenchimento — e à lista do
      `Icone.test.tsx` (`RF-04-01`, documento 15 §11.1).

## 2. A entrada e a tela inicial

- [x] 2.1 Em `TelaDeEntradaDoGuerreiro.tsx`, acrescentar o caminho `recadastro`, que abre direto
      na confirmação pelo nick e pelo PIN de quem abriu o aparelho, com título próprio, e retirar
      o aviso `aoAbrirSessao`, que só servia ao recadastro (`RF-04-22`, `RF-04-21`, `RN-04-37`).
- [x] 2.2 Em `TelaInicial.tsx`, acrescentar o cartão "Recadastrar imagem de Guerreiro(a)" ao
      grupo de quem opera, logo depois da medição; o caminho `recadastro` abre a entrada e,
      com a sessão aberta, a `TelaDeCaptura` sem a guarda de presença; concluída a captura, a
      tela "Imagem recadastrada" volta ao início encerrando a sessão. Retirar `viaDeEntrada` e
      `mostrarRecadastro` (`RF-04-22`, `RF-04-28`, decisão do fundador de 2026-11-10).
- [x] 2.3 Em `TelaDeEquipes.tsx`, retirar o botão do recadastro e as duas props que o ligavam
      (`RF-04-22`).

## 3. Os testes

- [x] 3.1 Em `inicio.test.tsx`, substituir os dois testes do recadastro pelas equipes pelos
      cenários "O recadastro mora no grupo de quem opera", "O recadastro abre só pela
      confirmação presencial" (sem chamar a guarda de presença, com o identificador vindo da
      sessão — `RN-01-22`) e "Gravada a imagem, o atendimento termina"; atualizar a ordem do
      grupo nos cenários "As ações de quem opera fecham a lista…" e "O aparelho que não abre a
      troca…" (`RF-04-22`, `RF-04-71`, `RF-04-49`).
- [x] 3.2 Em `entrada.test.tsx`, retirar as asserções de `aoAbrirSessao` e acrescentar que o
      caminho do recadastro abre na confirmação, sem o botão "Entrar" do reconhecimento
      (`RF-04-22`, `RF-04-21`).

## 4. Documentação

- [x] 4.1 Acrescentar a fatia 32 ao bloco do PRD-04 em `openspec/cronograma-de-fatias.md`,
      marcada `implementado`. Nada muda em `docs/`: não há regra nova, o PRD-04 já diz "a partir
      da própria aplicação" e a situação dele em `docs/prds/index.md` não muda.
