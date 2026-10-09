# Tasks

> A tarefa 1.1 é a **trava**: sem os arquivos do elenco, nenhuma das demais começa. O
> manifesto do que entregar está em `comum/marca/README.md` §3, e o que o elenco precisa
> parecer, no documento 15 §13.6.
>
> O elenco são **Susy, Otávio, prof. Carlos Trenell e Robô Educa** — decisão do fundador
> de 2026-10-09. Os **Rôbróders** saíram do elenco e seguem só como submarca.
>
> A marca do projeto — logotipo, símbolo, submarcas, cabeçalho e favicon — saiu desta
> change e foi entregue por `2026-10-02-marca-do-projeto-e-silhueta-de-nivel`.

## 1. O elenco no repositório

- [x] 1.0 Tirar `comum/marca/**` do alcance do Biome, como `apps/**/public` já está: o
      Biome lê `.svg` como JSX e acusa `noSvgWithoutTitle` em arquivo de marca, onde o
      rótulo é de quem apresenta e não do arquivo. Feito **antes** dos arquivos, para o
      upload não derrubar a esteira
- [x] 1.1 Receber os quatro personagens — Susy, Otávio, Trenell e Robô Educa — em
      `comum/marca/elenco/`, conferir um a um contra o manifesto do `README.md` §3
      (formato, nome, grade e orçamento de peso) e contra o documento 15 §13.6 (contorno
      quase preto, preenchimento chapado, fundo transparente e keyline em `cal-050`).
      Arquivo que chegar sem o keyline o recebe no recorte, e o que mudou se registra,
      como o §6 do manifesto já manda para limpeza. Fechar a procedência do `README.md`
      §8. Decidir com os arquivos na mão entre **SVG** e a rota
      alternativa do §3, **AVIF com reserva em WebP** a `1024` px, e declarar qual
      personagem saiu por qual, para a implementação prever `srcset`
- [x] 1.2 Escrever `comum/marca/LICENCA.md` com a reserva do documento 03 §1 — a marca
      fora da AGPL e da CC BY-SA, e a réplica trocando-a pela sua —, ao lado dos
      arquivos, como o `OFL-archivo.txt` fica ao lado das fontes

## 2. O herói da abertura

- [x] 2.1 Montar o herói em `src/pages/index.astro` — ilustração do elenco em primeiro
      plano, a frase do projeto e as ações "Entrar" e "Quero participar", que já existem
      —, com a ilustração fora do caminho crítico; verificar que a frase e as ações
      continuam de pé sem ela e que nenhuma ação nova é oferecida (`RF-03-01`,
      `RF-03-58`, `RF-03-51`)
- [x] 2.2 Acrescentar o herói a `src/testes/TelaDaVitrine.tsx`, para a composição de
      teste não desviar do layout; verificar que a suíte da App 06 segue verde
- [x] 2.3 Escrever os casos do herói, cobrindo os cenários do delta de
      `aplicacao-da-vitrine`: o herói aparece antes da primeira seção com a frase e as
      duas ações; sobrevive à ausência da ilustração; não oferece ação que a vitrine não
      tenha; e não busca recurso de domínio de terceiro
- [x] 2.4 Acrescentar ao teste da saída do build o caso de nível 2: o herói sai no
      documento servido da abertura, e nenhuma requisição a domínio de terceiro entra com
      a ilustração

## 3. Documentação

- [x] 3.1 Gravar no documento 15 §13.6 **quais personagens são de uso público**, que é o
      que resta da linha e chega com os arquivos, e remover de lá o `A definir`
      correspondente; mover do documento 09 a parte que isso fecha. O §13.6, o §14
      estreitado, as três decisões de 2026-10-09 no documento 09 e a linha do elenco no
      documento 99 §8 **já foram escritos** — conferir, não reescrever. Verificar que as
      linhas de logotipo e de submarcas já saíram pela change da marca
- [x] 3.2 Marcar a fatia 11 como `implementado` no `openspec/cronograma-de-fatias.md`, com
      o slug da change. A linha transversal da marca já foi fechada pela change
      `2026-10-02-marca-do-projeto-e-silhueta-de-nivel`; a situação do PRD-03 em
      `docs/prds/index.md` não muda, e nenhum arquivo nasce em `docs/`
