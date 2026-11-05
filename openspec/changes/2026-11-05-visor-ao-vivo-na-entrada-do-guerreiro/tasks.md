# Tasks

## 1. O visor na camada comum

- [ ] 1.1 Criar `comum/react/Visor.tsx` a partir de `apps/app-01-aula-presencial/src/captura/Visor.tsx`,
      com as frases do laço recebidas por _prop_ em vez da `FRASE_DO_LACO` interna, mantendo o
      contrato de **emprestar um lugar** — nem `MediaStream`, nem quadro, nem pixel entram no
      componente (`RF-05-95`, `RN-05-53`).
- [ ] 1.2 Mover as quatro regras `.cg-visor-moldura`, `.cg-visor-lugar:empty`, `.cg-visor` e
      `.cg-visor-estado` do `index.css` da App 01 para `comum/react/estilos.css`, preservando o
      espelhamento `scaleX(-1)` e o limite de altura, e exportar o `Visor` no
      `comum/react/indice.ts` (`RF-05-95`).
- [ ] 1.3 Apontar as duas telas de câmera da App 01 — `onboarding/TelaDeCaptura.tsx` e
      `entrada/TelaDeEntradaDoGuerreiro.tsx` — ao `Visor` comum, passando as frases de quem opera
      que elas já usam, e apagar `src/captura/Visor.tsx`. Nenhum comportamento da App 01 muda
      (`RF-04-64`).

## 2. A entrada da App 05

- [ ] 2.1 Em `apps/app-05-guerreiro/src/entrada/TelaDeEntradaDoGuerreiro.tsx`, chamar
      `prepararCaptura()` antes do laço e acoplar o espelho no lugar emprestado ao `Visor`, de
      modo que a câmera só acenda ao toque em Entrar (`RF-05-95`, `RN-05-49`).
- [ ] 2.2 Passar `definirEstadoDoLaco` como `aoMudarEstado` de `provarVivacidade()` e declarar as
      três frases de criança aprovadas no `design.md` §4 (`RF-05-95`, `RF-05-02`).
- [ ] 2.3 Dar desfecho próprio à falha de `prepararCaptura()` — frase que diz que a câmera não
      pôde ser preparada, sem interromper em vermelho, com o caminho do adulto oferecido junto —
      e remover a absorção dela pelo `definirRecusado(true)` do `catch` genérico, corrigindo a
      citação trocada de `RN-01-22` no comentário (`RN-05-48`, `RN-05-02`).
- [ ] 2.4 Acrescentar a frase fixa de orientação sobre luz e enquadramento, junto do visor
      (`RF-05-96`).
- [ ] 2.5 Acrescentar o aviso discreto do que acontece com a imagem, em linguagem de criança
      (`RF-05-57`, PRD-05 §11).
- [ ] 2.6 Encerrar a captura ao desmontar a tela, como a `TelaDeCaptura` da App 01 já faz, para
      que sair da entrada no meio do laço não deixe a câmera acesa (`RN-05-53`).

## 3. Testes

- [ ] 3.1 `comum/react/Visor.test.tsx`: o visor vazio não aparece; o lugar emprestado recebe o
      vídeo sem o componente ver quadro ou fluxo; as frases vêm de quem usa, e duas telas rendem
      redações diferentes para o mesmo estado — cenários "O visor vazio não ocupa a tela", "O
      visor não recebe a imagem" e "Duas telas, duas redações" (`RF-05-95`, `RN-05-53`).
- [ ] 3.2 `apps/app-05-guerreiro/src/entrada/entrada.test.tsx`: a tela abre sem câmera acesa e sem
      visor; o visor aparece depois do Entrar; as três frases do laço saem em linguagem de criança;
      a orientação e o aviso estão na tela; e o quadro capturado nunca é devolvido — cenários "O
      visor mostra a criança a si mesma", "A tela abre sem câmera acesa", "O quadro capturado não
      volta à tela", os três do laço, "A orientação aparece com o visor" e "O aviso acompanha a
      tela que abre a câmera" (`RF-05-95`, `RF-05-96`, `RF-05-57`, `RN-05-49`, `RN-05-53`).
- [ ] 3.3 No mesmo arquivo, cobrir a separação do preparo: `prepararCaptura()` que rejeita produz
      a frase da câmera e oferece o adulto, e NUNCA a frase do rosto; e as frases já existentes de
      recusa e de falha de camada seguem intactas — cenário "Câmera que não abre não vira rosto que
      não confere" (`RN-05-48`).
- [ ] 3.4 Confirmar que `apps/app-01-aula-presencial/src/onboarding/captura.test.tsx` e
      `src/entrada/entrada.test.tsx` seguem verdes **sem edição de asserção**: a App 01 trocou de
      onde importa o visor, não de comportamento (`RF-04-64`).

## 4. Documentação

- [ ] 4.1 Revisar o PRD-05: criar `RF-05-95` e `RF-05-96` na tabela de requisitos funcionais e
      `RN-05-53` na de regras de negócio, com origem no documento 03 §3.3 e no invariante 12;
      precisar o marcador do §11 sobre imagem real exibida, no molde do `RN-04-34`; e lançar os
      três na rastreabilidade do §15.
- [ ] 4.2 Marcar a fatia 14 como `implementado` em `openspec/cronograma-de-fatias.md` e trocar o
      recorte previsto pelo slug da change. O documento 09 **não** muda — não houve decisão nova,
      só aplicação de regra já vigente; o documento 99, o `docs/prds/index.md` e a `nav` do
      `mkdocs.yml` também não, porque nenhuma relação entre documentos mudou, a situação do PRD-05
      segue a mesma e nenhum arquivo nasceu em `docs/`.
