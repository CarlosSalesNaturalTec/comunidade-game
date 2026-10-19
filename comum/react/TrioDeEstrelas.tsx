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
// Não é glifo do `Icone`: ele fixa `fill="none"` e `stroke="currentColor"`, e
// o documento 15 §11.1 o quer assim. A **silhueta de badge** — a outra peça
// que o documento declara preenchida — já resolveu isso com componente e SVG
// próprios, e o trio segue o mesmo caminho (design — decisão 6).
//
// A cor sai dos **tokens** (`--cor-ponto` no preenchimento e
// `--cor-ponto-contorno` no contorno, que é o degrau 700 que a §9 manda para
// toda ficha): nenhum valor de cor entra aqui, e por isso o tema troca o trio
// junto. O contorno não tem versão escura em `comum/tokens.css` — lacuna
// preexistente da família ponto inteira —, e no tema escuro o preenchimento se
// sustenta sozinho contra o fundo.
//
// O trio é `aria-hidden`, como todo ícone: o documento 15 §5 proíbe que a
// forma carregue sozinha o significado, e quem lê por voz alcança o **texto**
// da recompensa, nunca a contagem das estrelas.

/** As três estrelas, nomeadas para a chave estável da lista. */
const ESTRELAS = ["uma", "duas", "tres"] as const;

// A estrela de cinco pontas na grade de `24` px do sistema de ícone.
const CAMINHO_DA_ESTRELA =
  "M12 2.6l2.9 6.1 6.7.9-4.9 4.6 1.2 6.6L12 17.7l-5.9 3.1 1.2-6.6-4.9-4.6 6.7-.9z";

export function TrioDeEstrelas() {
  return (
    <span className="cg-trio-de-estrelas" aria-hidden="true">
      {ESTRELAS.map((estrela) => (
        <svg
          key={estrela}
          className="cg-trio-de-estrelas__estrela"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          // `aria-hidden` em cada estrela, e não só no grupo, pelo mesmo
          // motivo do `Icone`: o significado é do texto ao lado, nunca da
          // forma (documento 15 §5).
          aria-hidden="true"
          focusable="false"
        >
          <path d={CAMINHO_DA_ESTRELA} />
        </svg>
      ))}
    </span>
  );
}
