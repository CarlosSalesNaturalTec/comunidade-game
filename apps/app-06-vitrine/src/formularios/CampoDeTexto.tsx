import { useId } from "react";

interface Props {
  rotulo: string;
  valor: string;
  aoAlterar: (valor: string) => void;
  erro?: string | null;
  longo?: boolean;
}

/** Campo de texto livre — o `Campo` da camada comum é de uma linha só. */
export function CampoDeTexto({ rotulo, valor, aoAlterar, erro, longo }: Props) {
  const id = useId();
  const idDoErro = `${id}-erro`;
  return (
    <div className="cg-campo">
      <label htmlFor={id}>{rotulo}</label>
      {longo ? (
        <textarea
          id={id}
          rows={5}
          value={valor}
          onChange={(e) => aoAlterar(e.target.value)}
          aria-invalid={erro ? true : undefined}
          aria-describedby={erro ? idDoErro : undefined}
        />
      ) : (
        <input
          id={id}
          value={valor}
          onChange={(e) => aoAlterar(e.target.value)}
          aria-invalid={erro ? true : undefined}
          aria-describedby={erro ? idDoErro : undefined}
        />
      )}
      {erro && (
        <p id={idDoErro} role="alert" className="cg-campo__erro">
          {erro}
        </p>
      )}
    </div>
  );
}
