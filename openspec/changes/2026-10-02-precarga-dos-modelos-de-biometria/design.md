# Design

## Context

`comum/biometria/biometria.ts` é, por desenho, o **único módulo** que importa a Human, carrega
modelo ou toca `getUserMedia` — a fronteira que garante o invariante 12 por construção. Hoje ele
expõe `prepararCaptura()`, que faz **duas** coisas em sequência: abre a câmera e carrega os
modelos. Quem chama são as três telas de câmera da App 01.

A pré-carga precisa da segunda metade sem a primeira.

## Decisão 1 — pré-carga ao fundo, e não service worker

| | **Pré-carga ao fundo** | Service worker / PWA |
| --- | --- | --- |
| Resolve o momento do download | sim | sim |
| Durabilidade do cache | **já existe** (IndexedDB da Human) | duplicaria o que já funciona |
| Shell offline, instalabilidade | não | sim — **outro problema** |
| Alcance da decisão | a App 01 | as **oito** (documento 03) |
| Modo de falha | nenhum novo | aplicação velha que não atualiza, em aparelho de sala |
| Custo | uma função e um disparo | infraestrutura, dependência de build, decisão nova |

Escolhida a **pré-carga**. A medição que decidiu: na Human 3.3.6 fixada,

```ts
/** Cache models in IndexDB on first sucessfull load
 *  default: true if indexdb is available (browsers), false if its not (nodejs)
 */
cacheModels: boolean;
```

e `biometria.ts` não declara a opção — logo, vale o padrão, e o cache em IndexedDB **já está
ligado**. O ganho estrutural que justificaria o service worker, portanto, não está em aberto.

A PWA **não fica descartada para sempre**: fica fora **desta fatia**. Ela é decisão das oito, do
documento 03, e entra no documento 09 como pendência própria, com o invariante 1 do documento 99
§6 a condicionar.

## Decisão 2 — a pré-carga carrega modelo, e nunca abre a câmera

A função nova SHALL chamar `human.load()` **sem** `abrirCamera()`. Não é economia de código: a
câmera fora do consentimento contraria `RN-04-07`, e o documento 15 §5 não admite aparelho
piscando luz de câmera sem ninguém ter pedido nada. A fronteira do módulo fica como está — a
função nova nasce **dentro** de `biometria.ts` e sai pelo `indice.ts`, nunca na tela.

```text
   prepararCaptura()            precarregarModelos()
   ├── abrirCamera()            └── human.load()
   └── human.load()                 (idempotente: acha tudo pronto
       ├── lança em falha            se a pré-carga já passou)
       └── confere models.loaded()
```

`prepararCaptura()` **não muda**, e segue sendo o caminho de erro visível (`RF-04-65`).

## Decisão 3 — o disparo segue o padrão que o arquivo já tem

`AparelhoDaAula.tsx` já resolve exatamente este formato de problema no efeito que busca o
verificador do PIN: depende de `sessao`, desiste com `if (semRede) return;` e volta a tentar
quando a rede retorna, pelas dependências `[sessao, restaurando, semRede]`. A pré-carga usa o
mesmo desenho, em vez de inventar outro:

- Dispara quando há **sessão de trabalho** e **há rede**.
- Se o aparelho abriu sem rede, tenta de novo **quando a rede voltar** — a sala com rede
  intermitente é o caso normal, não a exceção.
- Uma vez concluída, não repete.
- Falha é **silenciosa**: nada na tela, nenhum erro anunciado. `prepararCaptura()` continua
  sendo a rede de segurança, e ela é que fala com a pessoa.

O indicador fica **ao lado de `AvisoDeOperacaoSemConexao`**, dentro de `AparelhoDaAula` e acima
de `ConteudoDoAparelho` — o lugar que a aplicação já usa para estado ambiente do aparelho.

## Decisão 4 — o indicador tem 5 passos, e diz isso

A Human não expõe progresso por byte. `human.models.loaded()` devolve a lista dos carregados, e
os habilitados são cinco. O indicador, portanto, é **discreto e de 5 passos**, e NEVER promete
precisão que não tem. Uma barra percentual suave exigiria interceptar `fetch` dentro da
biblioteca — preço alto para um enfeite, num elemento que por decisão não bloqueia nada.

O indicador **some ao concluir** e nunca vira portão: nenhuma tela, nenhum caminho e nenhum botão
espera por ele.

## Risks

| Risco | Tratamento |
| --- | --- |
| A pré-carga competir com a rede da aula e atrasar a presença | É o teste 2 da tarefa 3.3: a fila de presença e a tela inicial não esperam por ela em momento nenhum. Prioridade é implícita — a pré-carga não tem prazo |
| O jsdom tentar baixar 10,22 MB na suíte | Dublê em `src/testes/configuracao.ts`, no molde do que já existe para `prepararCaptura` e `acoplarEspelho` |
| A pré-carga abrir a câmera por engano numa refatoração | Teste que afirma que `precarregarModelos()` não toca `getUserMedia` (decisão 2) |
| O indicador virar portão numa mudança futura | Cenário de spec próprio: a tela inicial aparece com a pré-carga em andamento |
| `load()` concorrente, se a câmera abrir durante a pré-carga | `human.load()` é idempotente e `prepararCaptura()` confere `models.loaded()` depois; conferir que a chamada concorrente não deixa o preparo em falso negativo |
