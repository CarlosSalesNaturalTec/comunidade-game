# Tasks

> Fatia 24 do PRD-04. Fecha a primeira pendência da §14 do PRD-04 e cria `RF-04-75` e
> `RN-04-42`. Cada tarefa cita o identificador que atende.
>
> **Tarefa 0 é porta:** as duas questões da `proposal.md` precisam de resposta do fundador antes
> das tarefas 2.x. As tarefas 1.x não dependem delas e podem andar antes.

## 0. Portas

- [ ] 0.1 Confirmar com o fundador se o **indicador** entra — e com ele o `RF-04-75` — ou se a
      pré-carga é **silenciosa**, caso em que a fatia vira desenho de implementação puro e as
      tarefas 2.3 e 4.x do indicador caem (`proposal.md` — questão 1)
- [ ] 0.2 Confirmar o **momento do disparo**: ao abrir a sessão de trabalho, como esta change
      assume, ou só com a aula já escolhida (`proposal.md` — questão 2)

## 1. A pré-carga em `comum/biometria`

- [ ] 1.1 Criar `precarregarModelos()` em `comum/biometria/biometria.ts` — chama `human.load()`
      e **nunca** `abrirCamera()`. Resolve sem lançar: falha é informada pelo retorno, não por
      exceção, porque quem chama não tem o que dizer à pessoa (`RN-04-42`; `design.md` —
      decisão 2)
- [ ] 1.2 Exportá-la em `comum/biometria/indice.ts`, mantendo a fronteira: nenhuma tela importa
      a Human nem toca `modelBasePath` (`RN-04-12`, invariante 12)
- [ ] 1.3 Expor o **andamento por modelo carregado**, a partir de `human.models.loaded()` contra
      os cinco habilitados — nunca percentual contínuo (`RF-04-75`; `design.md` — decisão 4)
- [ ] 1.4 Em `comum/biometria/biometria.test.ts`: afirmar que `precarregarModelos()` **não toca
      `getUserMedia`**, que é idempotente com `prepararCaptura()` e que resolve sem lançar
      quando o carregamento falha (`RN-04-42`, `RF-04-65`)

## 2. O disparo e o indicador na App 01

- [ ] 2.1 Em `src/testes/configuracao.ts`, dublar `precarregarModelos` — sem isso a suíte
      tentaria buscar 10,22 MB em jsdom, no molde do que já se faz com `prepararCaptura` e
      `acoplarEspelho` (`design.md` — Risks)
- [ ] 2.2 Disparar a pré-carga em `AparelhoDaAula.tsx` quando houver sessão de trabalho e rede,
      com nova tentativa **quando a rede voltar**, pelo mesmo desenho do efeito que busca o
      verificador do PIN. Nunca aguardar por ela em caminho algum (`RF-04-75`; `design.md` —
      decisão 3)
- [ ] 2.3 Apresentar o indicador discreto ao lado de `AvisoDeOperacaoSemConexao`, que some ao
      concluir e não impede ação nenhuma (`RF-04-75`)
- [ ] 2.4 Conferir que falha da pré-carga **não apresenta nada** na tela, e que o caminho de erro
      de `prepararCaptura()` segue intacto (`RF-04-65`)

## 3. Testes da aplicação

- [ ] 3.1 A pré-carga começa ao abrir a sessão de trabalho com rede; não começa sem rede; e
      recomeça quando a rede volta (spec: "Os modelos de biometria se carregam antes da primeira
      captura, sem travar a aula")
- [ ] 3.2 A tela inicial e os caminhos dela aparecem e operam **com a pré-carga em andamento** —
      o teste que impede o indicador de virar portão (spec: mesmo requisito)
- [ ] 3.3 O registro de presença e a fila local operam com a pré-carga em andamento e com ela
      falhada (`RF-04-23`, documento 03 §3.4)
- [ ] 3.4 Falha da pré-carga não apresenta mensagem; o preparo da captura segue dizendo o que
      houve (spec: "A pré-carga falha em silêncio…")
- [ ] 3.5 O indicador some ao concluir e expressa modelo carregado, não percentual (spec: "O
      andamento da pré-carga é dito de forma discreta e honesta")

## 4. Documentação

- [ ] 4.1 PRD-04 §6: criar `RF-04-75` e `RN-04-42` com enunciado verificável. **Depende do PR de
      revisão do PRD-04**, que é quem cria os identificadores
- [ ] 4.2 PRD-04 §14: retirar a pendência "peso dos modelos da biblioteca Human", que esta fatia
      fecha, e registrar onde a decisão foi gravada
- [ ] 4.3 Documento 03 §3.4: registrar a pré-carga como a resposta ao requisito de poucos
      segundos, em uma frase — o documento é fonte única e não repete o desenho
- [ ] 4.4 Documento 09 §1: gravar a decisão nova em "Já decididos" — pré-carga ao fundo, sem
      portão — e abrir a pendência do **service worker / app instalável**, que esta fatia
      descartou e que é decisão das oito, do documento 03
- [ ] 4.5 `openspec/cronograma-de-fatias.md`: fechar a situação da linha da fatia 24
- [ ] 4.6 Conferir os invariantes do documento 99 §6 — em especial o 1, que fixa as oito como
      Web Apps sem app nativo, e o 12, da imagem que não fica no aparelho

## 5. Verificação

- [ ] 5.1 `vitest run` em `comum/` e em `apps/app-01-aula-presencial/`, uma vez, ao fechar as
      tarefas de código
- [ ] 5.2 `biome format --check .` e `biome check .` nas duas pastas
- [ ] 5.3 `npm run fix`, `npm run lint` e `mkdocs build --strict` — a change toca `docs/`
