# Tasks

> A tarefa 1.1 é a **trava**: sem os arquivos do fundador, nenhuma das demais começa. O
> manifesto do que entregar está em `comum/marca/README.md`.

## 1. A marca no repositório

- [x] 1.0 Tirar `comum/marca/**` do alcance do Biome, como `apps/**/public` já está: o
      Biome lê `.svg` como JSX e acusa `noSvgWithoutTitle` em arquivo de marca, onde o
      rótulo é de quem apresenta e não do arquivo. Feito **antes** dos arquivos, para o
      upload não derrubar a esteira
- [ ] 1.1 Receber os arquivos em `comum/marca/`, conferir um a um contra o manifesto do
      `README.md` — formato, nome, grade e orçamento de peso — e registrar a procedência
      e a data no próprio `README.md`; verificar que nenhum arquivo traz valor de cor
      fora da paleta do documento 15 §3. **Dois não são encomendados:** o
      `apple-touch-icon.png` é rasterizado do `favicon.svg` aqui, e as versões `-mono`,
      se não vierem prontas, são derivadas das coloridas trocando preenchimento por
      `currentColor`
- [x] 1.2 Escrever `comum/marca/LICENCA.md` com a reserva do documento 03 §1 — a marca
      fora da AGPL e da CC BY-SA, e a réplica trocando-a pela sua —, ao lado dos
      arquivos, como o `OFL-archivo.txt` fica ao lado das fontes
- [ ] 1.3 Declarar `./marca` em `exports` e em `files` de `comum/package.json`;
      verificar que uma aplicação importa um arquivo da marca sem caminho relativo

## 2. A marca no cabeçalho das oito aplicações

- [ ] 2.1 Apresentar a marca em `comum/react/Cabecalho.tsx`, com a versão colorida no
      claro e a monocromática no escuro e sobre foto, mantendo o **nome em texto** ao
      lado dela; verificar que o nome continua legível quando a marca não carrega e que
      o contraste é medido sobre superfície opaca (documento 15 §§3.3, 5, princípio 3)
- [ ] 2.2 Trocar o favicon das sete aplicações pelo do projeto, a partir do arquivo
      único de `comum/marca/`, copiado pela esteira; verificar que nenhuma aplicação
      serve mais o logotipo do Vite (design — decisão 4)

## 3. O herói da abertura

- [ ] 3.1 Montar o herói em `src/pages/index.astro` — ilustração em primeiro plano, a
      frase do projeto e as ações "Entrar" e "Quero participar", que já existem —, com a
      ilustração fora do caminho crítico; verificar que a frase e as ações continuam de
      pé sem ela e que nenhuma ação nova é oferecida (`RF-03-01`, `RF-03-58`,
      `RF-03-51`)
- [ ] 3.2 Acrescentar o herói a `src/testes/TelaDaVitrine.tsx`, para a composição de
      teste não desviar do layout; verificar que a suíte da App 06 segue verde

## 4. Testes

- [ ] 4.1 Escrever os casos de nível 1: o herói traz a frase e as duas ações e sobrevive
      à ausência da ilustração; o cabeçalho traz o nome em texto sem a marca; a marca
      apresentada muda com o modo
- [ ] 4.2 Acrescentar ao teste da saída do build os casos de nível 2: o herói sai no
      documento servido da abertura, o favicon é o do projeto, e nenhuma requisição a
      domínio de terceiro entra com a marca nem com a ilustração

## 5. Documentação

- [ ] 5.1 Fechar no documento 15 as três linhas do §13 que a entrega resolve — logotipo
      e marca gráfica, universo dos personagens e submarcas —, gravando no corpo do
      documento a área de proteção, o tamanho mínimo e quais personagens são de uso
      público, que chegam com os arquivos; mover as três pendências correspondentes do
      documento 09 para "Já decididos" e atualizar o documento 99 se a relação entre
      documentos mudar
- [ ] 5.2 Marcar a fatia 11 e a linha transversal da marca como `implementado` no
      `openspec/cronograma-de-fatias.md`, com o slug da change. A situação do PRD-03 em
      `docs/prds/index.md` não muda, e nenhum arquivo nasce em `docs/`
