import { useDireitos } from "./ContextoDeDireitos";

interface Props {
  dado: string;
}

// Aviso discreto em toda tela da gestão que grava dado pessoal — nomeia o
// dado daquela tela e dá acesso à área Direitos e dados; nunca bloqueia a
// tela nem exige confirmação para continuar (`RF-02-64`, PRD-02 §11).
export function AvisoDeColeta({ dado }: Props) {
  const { irParaDireitos } = useDireitos();

  return (
    <p role="status" className="cg-aviso-de-coleta">
      Esta tela coleta {dado}.{" "}
      <button type="button" className="cg-aviso-de-coleta__botao" onClick={irParaDireitos}>
        Ver em Direitos e dados
      </button>
    </p>
  );
}
