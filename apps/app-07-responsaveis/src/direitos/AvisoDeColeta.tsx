import { useDireitos } from "./ContextoDeDireitos";

interface Props {
  dado: string;
}

// Aviso discreto em toda tela da App 07 que grava dado — nomeia o dado
// daquela tela e dá acesso à área detalhada (a transparência do vinculado);
// nunca bloqueia a tela nem exige confirmação para continuar (`RF-13-41`,
// PRD-13 §11, documento 03 §12).
export function AvisoDeColeta({ dado }: Props) {
  const { irParaTransparencia } = useDireitos();

  return (
    <p role="status" className="cg-aviso-de-coleta">
      Esta tela coleta {dado}.{" "}
      <button
        type="button"
        className="cg-aviso-de-coleta__botao"
        onClick={irParaTransparencia}
      >
        Ver na transparência
      </button>
    </p>
  );
}
