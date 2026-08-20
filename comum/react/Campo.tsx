import { useId } from "react";

interface Props {
  rotulo: string;
  valor: string;
  aoAlterar: (valor: string) => void;
  erro?: string | null;
  tipo?: string;
}

// Gera o próprio identificador e amarra rótulo, erro e estado inválido ao
// campo, para que quem o alcança a qualquer momento — não só quando o erro
// surge — receba a mensagem junto (documento 15 §5, requisito "O erro de um
// campo é anunciado no próprio campo").
export function Campo({ rotulo, valor, aoAlterar, erro, tipo = "text" }: Props) {
  const id = useId();
  const idDoErro = `${id}-erro`;
  const invalido = Boolean(erro);

  return (
    <div className="cg-campo">
      <label htmlFor={id}>{rotulo}</label>
      <input
        id={id}
        type={tipo}
        value={valor}
        onChange={(evento) => aoAlterar(evento.target.value)}
        aria-invalid={invalido || undefined}
        aria-describedby={invalido ? idDoErro : undefined}
      />
      {invalido && (
        <p id={idDoErro} role="alert" className="cg-campo__erro">
          {erro}
        </p>
      )}
    </div>
  );
}
