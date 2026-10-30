import { EstrelaDePonto } from "./EstrelaDePonto";

// O trio de estrelas da **recompensa de marco conquistada** (`RF-05-45`,
// decisão do fundador de 2026-10-19).
//
// A estrela cheia é, no documento 15 §9, o glifo da **grandeza ponto**, e a
// §9 abre dizendo que as três grandezas "nunca podem ser confundidas na
// tela". O fundador escolheu a estrela porque é o que a criança entende como
// "ganhei", e o **trio** é o diferenciador: ponto é sempre **uma** estrela,
// recompensa de marco são **três**. A exceção está escrita na §9, não
// subentendida aqui — e nenhum ponto é creditado neste caminho, porque o
// desbloqueio não credita ponto por si.
//
// A estrela mora em `EstrelaDePonto`, que o trio compõe três vezes: desde que
// a carta passou a levar **uma** estrela ao lado da frase de desempenho
// (decisão do fundador de 2026-10-30), o desenho é de lá. É ali que estão o
// porquê de a peça ser preenchida e a origem da cor nos tokens.
//
// O trio é `aria-hidden`, como todo ícone: o documento 15 §5 proíbe que a
// forma carregue sozinha o significado, e quem lê por voz alcança o **texto**
// da recompensa, nunca a contagem das estrelas.

/** As três estrelas, nomeadas para a chave estável da lista. */
const ESTRELAS = ["uma", "duas", "tres"] as const;

export function TrioDeEstrelas() {
  return (
    <span className="cg-trio-de-estrelas" aria-hidden="true">
      {ESTRELAS.map((estrela) => (
        <EstrelaDePonto key={estrela} />
      ))}
    </span>
  );
}
