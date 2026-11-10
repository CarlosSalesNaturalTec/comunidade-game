# Tasks

## 1. Núcleo

- [x] 1.1 `backend/src/nucleo/personas/regra.py`: `definir_avatar_do_guerreiro`, opaca, no molde
      de `definir_avatar_do_mestre` (`RF-05-51`).
- [x] 1.2 `backend/src/nucleo/personas/rotas.py`: `PATCH /v1/eu/avatar`, entrada `{avatar}` com
      `min_length=1` e `extra="forbid"`, saída `{avatar}`, 403 a todo papel que não seja
      Guerreiro(a), sem identificador de persona na rota (`RF-05-51`, `RN-05-21`, PRD-05 §9).
- [x] 1.3 Testes da rota em `backend/tests/test_avatar_do_guerreiro.py`: troca grava e
      `GET /v1/eu` devolve o novo; segunda troca grava; Mestre, Apoiador, Admin e responsável
      recebem 403; outro Guerreiro(a) não muda; vazio dá 422; sem sessão é recusado
      (`RF-05-51`, `RN-05-21`, `RF-01-76`).

## 2. Camada comum

- [x] 2.1 `comum/avatar/objeto.ts`: `regravarAvatar(textoVigente, avatarNovo)`, que troca só o
      objeto do §7.2 dentro do envelope e preserva as demais chaves; exportada por `indice.ts`
      (`RF-05-51`, documento 15 §7).
- [x] 2.2 `comum/avatar/MontagemDoAvatar.tsx`: componente controlado extraído da
      `TelaDeCadastro`, com as regras `.cg-escolha-de-avatar*` movidas do `index.css` da App 01
      para `comum/avatar/estilos.css`; exportado por `indice.ts` (`RF-04-07`, `RF-05-51`).
- [x] 2.3 Testes em `comum/avatar/avatar.test.tsx`: as nove camadas na ordem com nomes
      dizíveis; parte do avatar recebido; escolher traço redesenha sem chamar `fetch`;
      `regravarAvatar` preserva a forma de tratamento, grava o objeto sozinho quando o vigente é
      objeto, texto livre ou ausente (`RF-04-07`, `RF-05-51`, documento 15 §7).

## 3. App 01

- [x] 3.1 `TelaDeCadastro.tsx` passa a consumir `MontagemDoAvatar`, mantendo o fundo de partida
      `acao-100`; a suíte do onboarding segue verde sem editar asserção (`RF-04-07`).

## 4. App 05

- [x] 4.1 `src/api/carteira.ts`: `alterarMeuAvatar(token, avatar)` sobre `PATCH /v1/eu/avatar`
      (`RF-05-51`).
- [x] 4.2 `src/carteira/AlterarMeuAvatar.tsx`: lê `GET /v1/eu`, abre a montagem em
      `lerAvatar`, grava por `regravarAvatar` + `alterarMeuAvatar`, "Voltar sem salvar" não
      grava, recusa de sessão por `tratarRecusaDeSessao`, falha dita com a frase do design
      mantendo os traços escolhidos (`RF-05-51`, `RN-05-48`, `RN-05-15`).
- [x] 4.3 `src/carteira/MinhaCarteira.tsx`: botão "Mudar o meu avatar" no apoio do palco, troca
      para a `AlterarMeuAvatar` e, salvo, volta com a `MinhaCarta` remontada (`RF-05-51`,
      `RF-05-50`).
- [x] 4.4 Testes em `src/carteira/AlterarMeuAvatar.test.tsx` e `MinhaCarteira.test.tsx`: abre no
      avatar vigente; sem avatar abre no padrão; salvar grava e a carta relê a sessão; voltar
      sem salvar não chama a rota; a forma de tratamento sobrevive; falha mantém a montagem
      com o escolhido; recusa de sessão encerra a sessão (`RF-05-51`, `RN-05-48`).

## 5. Documentação

- [x] 5.1 `openspec/cronograma-de-fatias.md`: linha da fatia 16 do PRD-05 com o slug desta
      change, marcada implementada ao fechar; `docs/09-topicos-em-aberto-e-sugestoes.md` §1:
      pendência nova **Regravação da facial pelo próprio Guerreiro(a)** — hoje só Mestre ou
      Admin recadastra (`RF-01-08`), e decidir exige pesar consentimento do responsável e a
      sessão aberta sem rosto conferido. PRD-05, `docs/prds/index.md`, documento 99 e `nav` não
      mudam: o `RF-05-51` e a rota já estão no PRD.
