import { Icone, type NomeDeGlifo, type TamanhoDeIcone } from "./Icone";

// O glifo de poder do documento 15 §8.4: desenhado no sistema de ícone da
// §11.1 — a mesma grade de `24` px, o mesmo traço de `2` px, `currentColor` —,
// sempre **ao lado do nome do poder**, nunca no lugar dele.
//
// A cobertura é de **um glifo por poder do catálogo** do documento 02 §2, e o
// catálogo é dado da gestão: quem cadastra um poder novo não passa por aqui, e
// por isso poder sem glifo cai no **genérico** em vez de quebrar a tela.
//
// A escolha é pelo **nome**, não por identificador: o `poder_id` é gerado pelo
// banco de cada instalação e não serve de chave de desenho. O nome chega
// normalizado — sem acento, em minúsculas — e basta uma palavra distintiva
// dele para resolver o glifo, de modo que "Poder do Território", "Território"
// e "Poder do territorio" cheguem ao mesmo desenho.

/** O glifo do poder sem glifo próprio (documento 15 §8.4). */
export const GLIFO_GENERICO_DE_PODER: NomeDeGlifo = "poder";

const GLIFO_POR_PALAVRA: [palavra: string, glifo: NomeDeGlifo][] = [
  ["robotica", "poder-ia-e-robotica"],
  ["territorio", "poder-do-territorio"],
  ["sustentador", "poder-sustentador"],
  ["sustento", "poder-sustentador"],
  ["rima", "poder-da-rima"],
  ["redes", "poder-das-redes"],
  ["capoeira", "poder-da-capoeira"],
];

function normalizar(nome: string): string {
  return nome.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
}

/** O glifo do poder pelo nome dele, caindo no genérico quando não houver um
 * desenhado (documento 15 §8.4). */
export function glifoDoPoder(poder: string): NomeDeGlifo {
  const nome = normalizar(poder);
  for (const [palavra, glifo] of GLIFO_POR_PALAVRA) {
    if (nome.includes(palavra)) return glifo;
  }
  return GLIFO_GENERICO_DE_PODER;
}

interface Props {
  /** O nome do poder, como o catálogo da gestão o escreve. */
  poder: string;
  tamanho?: TamanhoDeIcone;
}

// O poder **não tem cor própria** (documento 15 §§8.4, 9): o glifo herda a cor
// do texto que acompanha, como todo ícone da §11.1, e cor fica reservada à
// grandeza e ao estado.
export function GlifoDePoder({ poder, tamanho = 24 }: Props) {
  return (
    <span className="cg-glifo-de-poder">
      <Icone glifo={glifoDoPoder(poder)} tamanho={tamanho} />
      <span className="cg-glifo-de-poder__nome">{poder}</span>
    </span>
  );
}
