# Tarefas — esqueleto da aula presencial e equipe da aula

## 1. A porta HTTP da equipe

- [ ] 1.1 Criar `backend/src/nucleo/equipes/rotas.py` com as quatro rotas do PRD-04 §9 —
      `GET` e `POST /v1/aulas/{id}/equipes`, `POST /v1/equipes/{id}/integrantes` e
      `DELETE /v1/equipes/{id}/integrantes/eu` —, consumindo `criar_equipe`,
      `entrar_na_equipe`, `sair_da_equipe` e `equipes_da_aula` sem alterá-las, com
      `exigir_permissao` nas operações `equipe_que_forma_na_aula` e
      `equipes_da_aula_em_andamento` e paginação por `contrato_de_listagem()` na leitura
      (`RF-04-30`, `RF-04-31`, `RF-04-32`, `RF-04-33`, `RF-04-34`, `RF-04-59`). Verificar
      pelas rotas respondendo no OpenAPI do núcleo.
- [ ] 1.2 Montar a saída da leitura restrita a **avatar e nick** de cada integrante, no
      esquema Pydantic da rota, sem projeção nova no modelo (`RF-04-34`, `RN-04-14`,
      invariante 11). Verificar que nome, nascimento e descritor não aparecem no corpo.
- [ ] 1.3 Fazer `DELETE /v1/equipes/{id}/integrantes/eu` passar a `sair_da_equipe` o
      `persona_id` da sessão, nunca identificador vindo do cliente (`RF-04-30`, invariante 15).
- [ ] 1.4 Registrar o roteador em `backend/src/nucleo/principal.py`, na ordem já usada pelos
      demais.

## 2. Testes do núcleo

- [ ] 2.1 Criar `backend/tests/test_equipe_rota.py` cobrindo, pela porta: criação com o autor
      como primeiro integrante, entrada, saída, papel declarado e papel ausente
      (`RF-04-30`, `RF-04-59`).
- [ ] 2.2 No mesmo arquivo, cobrir as recusas que a porta reexpõe — sexto integrante, segundo
      integrante de 17 anos ou mais, equipe de aula encerrada, Admin criando equipe, Mestre
      alterando composição e pedido sem credencial de persona (`RF-04-31`, `RF-04-32`,
      `RF-01-16`, `RF-01-38`), conferindo o código de resposta e que a composição não muda.
- [ ] 2.3 No mesmo arquivo, cobrir a leitura: equipes daquela aula, só avatar e nick, equipe de
      trilha fora do resultado, equipe de outra aula fora do resultado e aula sem equipe
      devolvendo conjunto vazio com 200 (`RF-04-33`, `RF-04-34`, `RN-04-14`).

## 3. Duas sessões no mesmo aparelho

- [ ] 3.1 Parametrizar a chave de armazenamento em `comum/autenticacao/armazenamentoDeSessao.ts`
      e `ContextoDeSessao.tsx`, mantendo o valor de hoje como padrão (design — decisão 1).
      Verificar que as Apps 03 e 09 seguem sem passar a propriedade e sem mudança de
      comportamento.
- [ ] 3.2 Cobrir em `comum/autenticacao` o padrão e a chave explícita, e dois provedores
      aninhados com chaves distintas convivendo sem que um derrube o outro (design — decisão 1).

## 4. A App 01

- [ ] 4.1 Criar `apps/app-01-aula-presencial/` no desenho das duas irmãs — Vite, React,
      TypeScript, workspace `apps/*`, consumindo `comum/` —, Mobile First com alto contraste e
      poucos elementos por tela (PRD-04 §10).
- [ ] 4.2 Implementar a **sessão de trabalho do aparelho**: entrada de Mestre ou Admin por login
      social, recusa de Guerreiro(a) em linguagem simples, leitura de `GET /v1/aulas/vigentes`,
      a aplicação que não abre sem aula vigente e a pergunta única da comunidade quando há mais
      de uma, guardada junto do token de trabalho (`RF-04-02`, `RF-04-03`, `RF-04-05`,
      `RN-04-01`, `RN-04-02`, design — decisões 3 e 4).
- [ ] 4.3 Encerrar a sessão de trabalho quando a aula escolhida deixa de aparecer entre as
      vigentes, relendo a rota ao abrir e a cada volta à tela inicial (`RF-04-05`, `RN-04-29`,
      design — decisão 3).
- [ ] 4.4 Implementar a **tela inicial** com os dois caminhos, o do onboarding desabilitado com
      o motivo em uma linha, a volta ao início ao fim de cada atendimento com a sessão do
      Guerreiro(a) limpa, e o encaminhamento de quem escolhe trilhas sem sessão à entrada do
      Guerreiro(a), nunca ao cadastro (`RF-04-01`, `RF-04-28`, design — decisão 2).
- [ ] 4.5 Implementar a **entrada do Guerreiro(a)** por `POST /v1/sessoes/guerreiro/confirmacao`,
      com o nick informado e a confirmação de Mestre ou Admin presente (`RF-04-29`, `RF-04-15`,
      `RN-04-09`), sem qualquer superfície de câmera ou mídia (`RN-04-12`).
- [ ] 4.6 Implementar a **área de equipes**: lista das equipes da aula por avatar e nick, criar,
      entrar com papel declarado e sair, com as recusas do núcleo apresentadas em linguagem
      simples (`RF-04-30`, `RF-04-31`, `RF-04-33`, `RF-04-34`, `RF-04-59`, `RN-04-16`), sem
      oferecer formação de equipe à sessão de trabalho nem homologação de equipe da trilha
      (`RN-04-18`, `RF-01-63`).

## 5. Testes da App 01

- [ ] 5.1 Cobrir a sessão de trabalho: sem aula vigente a aplicação não abre e explica em uma
      frase; uma aula dispensa a pergunta; duas aulas perguntam uma única vez e não repetem no
      restante da sessão; Guerreiro(a) é recusado na abertura; a aula que sai das vigentes
      encerra a sessão (`RF-04-02`, `RF-04-03`, `RF-04-05`, PRD-04 §12).
- [ ] 5.2 Cobrir a tela inicial e a entrada do Guerreiro(a): os dois caminhos aparecem; trilhas
      sem sessão leva à entrada e não ao cadastro; o atendimento seguinte começa sem dado do
      anterior; a confirmação do Mestre abre a sessão do Guerreiro(a) (`RF-04-01`, `RF-04-28`,
      `RF-04-29`, PRD-04 §12).
- [ ] 5.3 Cobrir a área de equipes: equipe criada aparece na lista; a sexta pessoa lê a recusa
      em linguagem simples, e o segundo integrante de 17 anos ou mais também; saída por conta
      própria; a lista mostra só avatar e nick (`RF-04-30`, `RF-04-31`, `RF-04-34`, PRD-04 §12).

## 6. Esteira de publicação

- [ ] 6.1 Acrescentar o alvo `aula` em `.firebaserc` e criar
      `.github/workflows/app-01-deploy.yml`, espelho do `app-09-deploy.yml`, com
      `VITE_CHAVE_DE_APLICACAO` própria (design — decisão 7). Verificar que o workflow dispara
      só pelos caminhos da App 01 e de `comum/`.

## 7. Documentação

- [ ] 7.1 Gravar as três decisões do fundador de 2026-08-24 em `docs/09-topicos-em-aberto-e-sugestoes.md`,
      em "Já decididos": a entrada sem câmera na primeira fatia, o cadastro de Guerreiro(a) por
      Mestre e Admin, e a conferência de nick do onboarding atrás da sessão de trabalho do
      aparelho.
- [ ] 7.2 Aplicar as decisões nos documentos afetados: a matriz do documento 02 §1 e do PRD-01
      §4 ganha o cadastro de Guerreiro(a) pelo Mestre (decisão 2); o PRD-04 §9 deixa de declarar
      a conferência de nick como pública (decisão 3) e a §14 perde as pendências decididas.
- [ ] 7.3 Alinhar `docs/prds/prd-09-area-do-mestre.md` §6.8: o `RF-09-61` — empréstimo e
      devolução de exemplar do acervo — fica para o ciclo seguinte, como o documento 09 já
      decidiu na estratégia de conservação do acervo. Não é decisão nova: é o PRD alcançando a
      fonte.
- [ ] 7.4 Atualizar `docs/prds/index.md` com a situação do PRD-04 e a narrativa desta fatia, e o
      documento 99 §8 se a relação entre documentos mudou. Nenhum arquivo novo em `docs/`, logo
      a `nav` do `mkdocs.yml` não muda.
