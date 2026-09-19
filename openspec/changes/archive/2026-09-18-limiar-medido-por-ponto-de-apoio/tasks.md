## 1. A decisão nova nos documentos-fonte

A decisão nasce aqui e só então vira código — hierarquia de autoridade do `CLAUDE.md`. Nada
das seções 2 a 6 começa antes desta seção fechar.

- [x] 1.1 No documento 03 §3.3, reescrever o item **"Calibração do limiar"**: o limiar é dado
      **de cada ponto de apoio**, medido no aparelho do encontro; a medição segue guardando um
      descritor de referência por vez e descartando a comparada no ato, e o que sai do aparelho
      é o **limiar confirmado com as distâncias medidas** — descritor e imagem, nunca. Corrigir
      a frase "nada envia ao núcleo", que deixa de ser verdade. Conferir que a §3.3 não passa a
      duplicar regra que já esteja em outro documento.
- [x] 1.2 Registrar a decisão em `docs/09-topicos-em-aberto-e-sugestoes.md` §1, movendo para
      "Já decididos" a linha **"Parâmetros da entrada do Guerreiro(a)"** no que toca ao limiar:
      ele deixa de ser parâmetro de implantação e vira dado medido por ponto de apoio; ponto de
      apoio sem medição não reconhece ninguém, e a gestão mostra quem está nessa situação. A
      duração da sessão do Guerreiro(a) **continua** parâmetro de implantação e permanece na
      linha.
- [x] 1.3 Criar no PRD-01 o `RF-01-73` (limiar como dado medido do ponto de apoio, com
      histórico, e comparação que recusa sem ele) e o `RN-01-56` (a recusa por ausência de
      limiar é indistinguível das três causas do `RN-01-22`), e corrigir na rastreabilidade do
      PRD-01 a linha que hoje declara o limiar como "parâmetro declarado na implantação" — a
      duração da sessão segue como está.
- [x] 1.4 Criar no PRD-04 o `RF-04-66` (bancada em duas séries, valor proposto e gravação) e o
      `RN-04-35` (critério de conclusão: mínimos, duas pessoas no teto, folga obrigatória, ponto
      médio como valor proposto, sobreposição não grava), e ampliar `RF-04-63` e `RN-04-32` no
      que a decisão mudou.
- [x] 1.5 Criar no PRD-02 o `RF-02-109` (consulta do limiar por ponto de apoio, com origem e
      destaque de quem não tem), e registrar os cinco identificadores novos na rastreabilidade
      do documento 99 §8, sem repetir texto normativo do documento 03.

## 2. O núcleo — o limiar como dado do ponto de apoio

- [x] 2.1 Modelar a **medição do limiar** em `nucleo/biometria/modelo.py`: ponto de apoio,
      limiar, as duas séries de distâncias, quem mediu e quando; o vigente é a medição mais
      recente do ponto de apoio. Migração Alembic correspondente (`RF-01-73`, design — decisão 4).
- [x] 2.2 Em `nucleo/biometria/regra.py`, ler o limiar vigente do ponto de apoio e fazer
      `autenticar_por_nick_e_descritor` **recusar** quando não houver medição — auditando a
      comparação como recusa, como já faz nos demais casos (`RF-01-73`, `RN-01-56`, `RN-01-14`).
- [x] 2.3 Escrever a regra da **gravação** da medição: confere o critério de conclusão do
      `RN-04-35` também no núcleo — as duas séries, os mínimos e a folga —, recusa descritor no
      corpo e grava com o autor. O núcleo não confia no cálculo do aparelho (`RF-01-73`,
      `RN-04-35`, `RN-01-15`).
- [x] 2.4 Remover `biometria_limiar_de_comparacao` da `Configuracao` e a seção correspondente do
      `backend/README.md`, deixando registrado que a variável saiu e por quê (`RF-01-73`).

## 3. O núcleo — as rotas

- [x] 3.1 Rota de gravação da medição, restrita a Mestre e Admin pela matriz, recebendo a aula
      em curso — é ela que determina o ponto de apoio (`RF-01-73`, `RF-01-16`, design — decisão 3).
- [x] 3.2 Rota de leitura do limiar vigente por ponto de apoio, com a origem da medição, para a
      App 03; e a marcação de quem não tem limiar medido (`RF-02-109`).
- [x] 3.3 Em `POST /v1/sessoes/guerreiro`, receber a **aula**, conferir que ela está vigente e
      que o vínculo do Guerreiro(a) é da comunidade dela, e manter a recusa **única** para todas
      as causas — as três do `RN-01-22` mais as duas novas (`RF-01-04`, `RN-01-56`, design —
      decisão 3).

## 4. A bancada da App 01

- [x] 4.1 Em `TelaDeMedicaoDoLimiar`, declarar a **série** de cada captura — piso ou teto —, com
      as duas listas separadas na tela e o maior piso e o menor teto em destaque (`RF-04-66`).
- [x] 4.2 Implementar o **critério de conclusão** e o valor proposto: mínimos por série, duas
      pessoas no teto, folga obrigatória e ponto médio entre maior piso e menor teto. Séries que
      se sobrepõem não oferecem gravação e dizem que não há limiar viável (`RN-04-35`, design —
      decisões 6 e 7).
- [x] 4.3 Gravar o limiar confirmado, dizendo antes qual ponto de apoio o receberá e
      apresentando o desfecho a quem confirmou. A tela passa a precisar do token de trabalho e
      da aula, que a `TelaInicial` e o `FluxoDeOnboarding` já têm (`RF-04-66`).
- [x] 4.4 Conferir que a fronteira do aparelho segue de pé: um descritor de referência por vez,
      comparada descartada no ato, e nenhum descritor ou imagem no corpo da gravação
      (`RN-04-32`, `RN-04-34`).
- [x] 4.5 Atualizar o aviso de coleta e a área detalhada de direitos: a medição passa a enviar
      ao núcleo o limiar e as distâncias, e segue sem enviar descritor ou imagem (`RF-04-26`).

## 5. A consulta na App 03

- [x] 5.1 Na área Pontos de Apoio, apresentar o limiar vigente de cada espaço com quem mediu,
      quando e as duas séries, e **destacar** os pontos de apoio sem limiar medido, dizendo o
      que aquilo significa no encontro. Sem caminho de edição (`RF-02-109`, `RN-01-56`, design —
      decisão 2).

## 6. Testes

- [x] 6.1 No backend, cobrir a regra da comparação: limiar vigente lido do ponto de apoio da
      aula, pontos de apoio com limiares diferentes aplicando cada um o seu, ausência de medição
      recusando, e a auditoria da recusa (`RF-01-73`, `RN-01-56`, `RN-01-14`).
- [x] 6.2 No backend, cobrir a gravação: critério conferido no núcleo, sobreposição recusada,
      descritor no corpo recusado, medição nova substituindo a vigente sem apagar a anterior, e
      a permissão restrita a Mestre e Admin (`RF-01-73`, `RN-04-35`, `RF-01-16`, `RN-01-15`).
- [x] 6.3 No backend, cobrir a rota de sessão: pedido sem aula recusado com 422, aula de outra
      comunidade e aula não vigente recusadas com a **mesma** resposta das três causas do
      `RN-01-22` (`RF-01-04`, `RN-01-56`).
- [x] 6.4 Em `bancada.test.tsx`, cobrir as duas séries separadas, os mínimos, o teto com uma
      pessoa só, a sobreposição que não grava, o ponto médio proposto e a gravação só após
      confirmação (`RF-04-66`, `RN-04-35`).
- [x] 6.5 Na App 03, cobrir a consulta: limiar com a origem, ponto de apoio sem limiar destacado
      e ausência de caminho de edição (`RF-02-109`).

## 7. Documentação

- [x] 7.1 Acrescentar ao bloco do PRD-04 do `openspec/cronograma-de-fatias.md` a **fatia 15**
      com o slug desta change, e ao bloco do PRD-02 a linha sem número que registra a consulta
      do `RF-02-109`. Marcar como **superada** a tarefa em aberto da fatia 14 — trocar o segredo
      pelo valor medido —, porque o segredo deixa de existir. A situação dos PRDs em
      `docs/prds/index.md` não muda, e nenhum arquivo novo entra em `docs/`, então a `nav` do
      `mkdocs.yml` segue como está.

## 8. Implantação e primeira medição

- [ ] 8.1 Remover `CG_BIOMETRIA_LIMIAR_DE_COMPARACAO` do segredo `GCP_SECRETOS_CG` **depois** do
      _merge_ em `main` — antes dele, a revisão em produção ainda exige a variável.
- [ ] 8.2 **EM ABERTO — só existe depois do _deploy_.** Fazer a primeira medição no aparelho do
      encontro, pelo caminho do diagnóstico, com **dois ou mais adultos**: série do piso, série
      do teto, e o limiar gravado no ponto de apoio. É o ato que finalmente liga o
      reconhecimento facial em produção.
