import { useId } from "react";

interface Props {
  rotulo: string;
  valor: string;
  aoAlterar: (valor: string) => void;
  erro?: string | null;
  tipo?: string;
  /** Teto de caracteres do `<input>`, quando a regra o fixa. */
  maxLength?: number;
  /**
   * Declara este campo como o inicial da tela: ele recebe o foco quando a tela
   * abre. É opcional e nunca padrão — foco automático em tela que apresenta
   * conteúdo acima do campo faz quem navega por leitor de tela começar no meio
   * (documento 15 §5).
   */
  focoInicial?: boolean;
}

// Gera o próprio identificador e amarra rótulo, erro e estado inválido ao
// campo, para que quem o alcança a qualquer momento — não só quando o erro
// surge — receba a mensagem junto (documento 15 §5, requisito "O erro de um
// campo é anunciado no próprio campo").
export function Campo({
  rotulo,
  valor,
  aoAlterar,
  erro,
  tipo = "text",
  maxLength,
  focoInicial,
}: Props) {
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
        maxLength={maxLength}
        // O foco inicial é declarado pela tela, nunca assumido pelo componente, e
        // só nas telas cujo propósito é preencher aquele campo (documento 15 §5).
        // biome-ignore lint/a11y/noAutofocus: opt-in da tela, nunca padrão
        autoFocus={focoInicial}
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
