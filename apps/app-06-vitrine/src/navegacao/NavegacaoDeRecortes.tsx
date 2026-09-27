import type { ChaveDeRecorte } from "./recortes";
import { RECORTES } from "./recortes";

interface Props {
  recorteAtual: ChaveDeRecorte;
  aoSelecionarRecorte: (caminho: string) => void;
}

// A `NavegacaoDeAreas` de `comum/react` não serve aqui: ela traz a saída da
// sessão, e a vitrine não tem sessão de que sair (`RN-03-01`). O recorte
// corrente é marcado por `aria-current` e por peso e borda, nunca só por cor
// (documento 15 §5).
export function NavegacaoDeRecortes({ recorteAtual, aoSelecionarRecorte }: Props) {
  return (
    <nav className="cg-recortes" aria-label="Recortes de leitura">
      {RECORTES.map((recorte) => (
        <button
          key={recorte.chave}
          type="button"
          className="cg-recortes__item"
          aria-current={recorte.chave === recorteAtual ? "true" : undefined}
          onClick={() => aoSelecionarRecorte(recorte.caminho)}
        >
          {recorte.rotulo}
        </button>
      ))}
    </nav>
  );
}
