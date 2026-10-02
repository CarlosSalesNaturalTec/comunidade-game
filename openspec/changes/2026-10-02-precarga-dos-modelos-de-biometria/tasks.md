# Tasks

> Fatia 24 do PRD-04. Fecha a primeira pendência da §14 do PRD-04 e cria `RF-04-75` e
> `RN-04-42`. Cada tarefa cita o identificador que atende.
>
> **A elicitação está fechada** — todas as respostas do fundador são de 2026-10-02 e estão na
> `proposal.md`. As tarefas podem andar na ordem que convier.

## 0. O que a elicitação fechou

- [x] 0.1 **O indicador entra** — e é ele que cria o `RF-04-75`. Pré-carga silenciosa descartada
- [x] 0.2 **O disparo é ao abrir a sessão de trabalho**, não com a aula já escolhida
- [x] 0.3 **Indicador local à App 01**, texto "Carregando modelos de reconhecimento facial",
      **narrado** quando a narração das telas estiver ativada
- [x] 0.4 **A falha é dita, em vermelho** — "Não foi possível carregar os modelos de
      reconhecimento facial" —, sem deixar o indicador parado. **Reverte** a falha silenciosa
      que esta change havia desenhado
- [x] 0.5 **A falha some quando a rede volta**, e o andamento volta com ela
- [x] 0.6 **`RN-04-42` desce do `RN-04-07` e do documento 03 §3.3**
- [x] 0.7 **Fora do aviso de coleta** (`RF-04-26`): a pré-carga não coleta dado nenhum
- [x] 0.8 **`RF-04-75` na §6.1**; na §5.1, **nota do passo 1**, e o **passo 6 corrigido junto**
- [x] 0.9 **Service worker e app instalável: descartados**, não adiados
- [x] 0.10 **App 05 em fatia própria** do PRD-05; **revisão do PRD-04 em PR próprio**, fechando
      só a pendência dos modelos

## 1. A pré-carga em `comum/biometria`

- [ ] 1.1 Criar `precarregarModelos()` em `comum/biometria/biometria.ts` — chama `human.load()`
      e **nunca** `abrirCamera()`. Resolve sem lançar: falha é informada pelo retorno, não por
      exceção, porque quem chama é que decide o que dizer (`RN-04-42`; `design.md` — decisão 2)
- [ ] 1.2 Exportá-la em `comum/biometria/indice.ts`, mantendo a fronteira: nenhuma tela importa
      a Human nem toca `modelBasePath` (`RN-04-12`, invariante 12)
- [ ] 1.3 Expor o **andamento por modelo carregado**, a partir de `human.models.loaded()` contra
      os cinco habilitados — nunca percentual contínuo (`RF-04-75`; `design.md` — decisão 5)
- [ ] 1.4 Em `comum/biometria/biometria.test.ts`: afirmar que `precarregarModelos()` **não toca
      `getUserMedia`**, que é idempotente com `prepararCaptura()` e que resolve sem lançar
      quando o carregamento falha (`RN-04-42`, `RF-04-65`)

## 2. O disparo, o andamento e a falha na App 01

- [ ] 2.1 Em `src/testes/configuracao.ts`, dublar `precarregarModelos` — sem isso a suíte
      tentaria buscar 10,22 MB em jsdom, no molde do que já se faz com `prepararCaptura` e
      `acoplarEspelho` (`design.md` — Risks)
- [ ] 2.2 Disparar a pré-carga em `AparelhoDaAula.tsx` quando houver sessão de trabalho e rede,
      com nova tentativa **quando a rede voltar**, pelo mesmo desenho do efeito que busca o
      verificador do PIN. Nunca aguardar por ela em caminho algum (`RF-04-75`; `design.md` —
      decisão 3)
- [ ] 2.3 Apresentar o andamento com **`Aviso tipo="andamento"`** — "Carregando modelos de
      reconhecimento facial" —, ao lado de `AvisoDeOperacaoSemConexao`. Sai ao concluir e não
      impede ação nenhuma. **Nenhum componente novo** (`RF-04-75`; `design.md` — decisão 4)
- [ ] 2.4 Apresentar a falha com **`Aviso tipo="erro"`** — "Não foi possível carregar os modelos
      de reconhecimento facial" —, no lugar do andamento, que não fica parado no passo que
      travou. A mensagem sai quando a rede volta e o andamento retorna (`RF-04-75`)
- [ ] 2.5 Conferir que o caminho de erro de `prepararCaptura()` segue intacto e **distinto** —
      a frase da captura não se confunde com a da pré-carga (`RF-04-65`)

## 3. Testes da aplicação

- [ ] 3.1 A pré-carga começa ao abrir a sessão de trabalho com rede; não começa sem rede; e
      recomeça quando a rede volta (spec: "Os modelos de biometria se carregam antes da primeira
      captura, sem travar a aula")
- [ ] 3.2 A tela inicial e os caminhos dela aparecem e operam **com a pré-carga em andamento** —
      o teste que impede o indicador de virar portão (spec: mesmo requisito)
- [ ] 3.3 O registro de presença e a fila local operam com a pré-carga em andamento e com ela
      falhada (`RF-04-23`, documento 03 §3.4)
- [ ] 3.4 O andamento é apresentado como informação, sai ao concluir e é expresso por modelo
      carregado, nunca em percentual (spec: "O andamento da pré-carga é dito…")
- [ ] 3.5 A falha é apresentada como erro, com rótulo textual que não depende da cor; o
      andamento sai; a rede que volta limpa a mensagem (spec: "A falha da pré-carga é dita…")
- [ ] 3.6 Com a narração ativada, andamento e falha são falados como os demais avisos
      (documento 15 §5.1)

## 4. Documentação

- [ ] 4.1 **Em PR próprio de revisão do PRD-04** — padrão das fatias 20 e 21 —, criar
      `RF-04-75` na **§6.1** e `RN-04-42`, com enunciado verificável e as fontes `RN-04-07` e
      documento 03 §3.3
- [ ] 4.2 Na mesma revisão, §5.1: a pré-carga entra como **nota do passo 1**, e o **passo 6 é
      corrigido** — ele diz que a aplicação verifica a câmera ao abrir a sessão de trabalho, e
      `existeCamera()` é chamado dentro de `TelaDeEntradaDoGuerreiro` e `FluxoDeOnboarding`, não
      na abertura. Defeito preexistente, corrigido junto por decisão do fundador
- [ ] 4.3 PRD-04 §14: retirar **só** a pendência "peso dos modelos da biblioteca Human". As
      outras seis seguem abertas e não são tocadas
- [ ] 4.4 Documento 03 §3.4: registrar a pré-carga como a resposta ao requisito de poucos
      segundos, em uma frase — o documento é fonte única e não repete o desenho
- [ ] 4.5 Documento 09 §1: gravar em "Já decididos" a pré-carga ao fundo, sem portão, **e o
      descarte do service worker e do app instalável** — descartados, não adiados
- [ ] 4.6 `openspec/cronograma-de-fatias.md`: fechar a situação da linha da fatia 24, e conferir
      que a linha da fatia da App 05 está registrada no bloco do PRD-05
- [ ] 4.7 Conferir os invariantes do documento 99 §6 — em especial o 1, que fixa as oito como
      Web Apps sem app nativo, e o 12, da imagem que não fica no aparelho

## 5. Verificação

- [ ] 5.1 `vitest run` em `comum/` e em `apps/app-01-aula-presencial/`, uma vez, ao fechar as
      tarefas de código
- [ ] 5.2 `biome format --check .` e `biome check .` nas duas pastas
- [ ] 5.3 `npm run fix`, `npm run lint` e `mkdocs build --strict` — a change toca `docs/`
