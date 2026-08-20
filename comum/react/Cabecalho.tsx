import { Botao } from "./Botao";

interface Acao {
  rotulo: string;
  aoAcionar: () => void;
}

interface Props {
  titulo: string;
  subtitulo?: string;
  acao?: Acao;
}

export function Cabecalho({ titulo, subtitulo, acao }: Props) {
  return (
    <header className="cg-cabecalho">
      <div className="cg-cabecalho__texto">
        <h1>{titulo}</h1>
        {subtitulo && <p>{subtitulo}</p>}
      </div>
      {acao && (
        <Botao variante="secundaria" onClick={acao.aoAcionar}>
          {acao.rotulo}
        </Botao>
      )}
    </header>
  );
}
