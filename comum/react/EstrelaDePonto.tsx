import { CAMINHO_DA_ESTRELA, type TamanhoDeIcone } from "./Icone";

// A **estrela cheia** da grandeza **ponto regular** (documento 15 §9).
//
// Não é glifo do `Icone`: ele fixa `fill="none"` e `stroke="currentColor"`, e o
// documento 15 §11.1 o quer assim. A §9 declara a exceção — a **ficha das
// grandezas** é peça preenchida —, e a §11.1 a repete: a exceção é ao traço,
// nunca à regra de que o tema troca o desenho junto. A cor sai dos **tokens**
// (`--cor-ponto` no preenchimento e `--cor-ponto-contorno` no contorno), e
// nenhum valor de cor entra aqui.
//
// A peça nasceu dentro do `TrioDeEstrelas` e saiu para cá quando a carta
// passou a precisar de **uma** estrela ao lado da frase de desempenho (decisão
// do fundador de 2026-10-30): o trio a compõe três vezes e a carta uma vez, e
// dois desenhos da mesma forma divergiriam na primeira correção.
//
// Ponto regular é **uma** estrela; a recompensa de marco são **três**, e é a
// contagem que separa as duas (`RF-05-45`). O **ponto extra** é a estrela
// **vazada**, que é glifo do `Icone` como os demais, porque ali o vazado é a
// regra e não a exceção.
//
// A estrela é `aria-hidden`: o documento 15 §5 proíbe que a forma carregue
// sozinha o significado, e quem lê por voz alcança a frase ao lado.

interface Props {
  tamanho?: TamanhoDeIcone;
}

export function EstrelaDePonto({ tamanho = 24 }: Props) {
  return (
    <svg
      className="cg-estrela-de-ponto"
      width={tamanho}
      height={tamanho}
      viewBox="0 0 24 24"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
    >
      <path d={CAMINHO_DA_ESTRELA} />
    </svg>
  );
}
