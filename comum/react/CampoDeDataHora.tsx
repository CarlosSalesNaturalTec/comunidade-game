import { useId } from "react";

interface Props {
  rotulo: string;
  valor: string;
  aoAlterar: (valor: string) => void;
  erro?: string | null;
}

function paraExibicao(valorComFuso: string): string {
  if (!valorComFuso) return "";
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return "";
  const preencher = (numero: number) => String(numero).padStart(2, "0");
  return (
    `${data.getFullYear()}-${preencher(data.getMonth() + 1)}-${preencher(data.getDate())}` +
    `T${preencher(data.getHours())}:${preencher(data.getMinutes())}`
  );
}

function paraFuso(valorLocal: string): string {
  if (!valorLocal) return "";
  const data = new Date(valorLocal);
  if (Number.isNaN(data.getTime())) return "";
  const desvioEmMinutos = -data.getTimezoneOffset();
  const sinal = desvioEmMinutos >= 0 ? "+" : "-";
  const preencher = (numero: number) => String(Math.abs(numero)).padStart(2, "0");
  const offsetHoras = preencher(Math.trunc(desvioEmMinutos / 60));
  const offsetMinutos = preencher(desvioEmMinutos % 60);
  return `${valorLocal}:00${sinal}${offsetHoras}:${offsetMinutos}`;
}

// O único campo de data e hora da plataforma (design — decisão 4, documento
// 15 §12): o navegador coleta a hora local pelo input nativo, e o fuso é
// anexado aqui, uma única vez, antes de sair para quem usa o campo — este
// campo NUNCA devolve um horário sem fuso.
export function CampoDeDataHora({ rotulo, valor, aoAlterar, erro }: Props) {
  const id = useId();
  const idDoErro = `${id}-erro`;
  const invalido = Boolean(erro);

  return (
    <div className="cg-campo">
      <label htmlFor={id}>{rotulo}</label>
      <input
        id={id}
        type="datetime-local"
        value={paraExibicao(valor)}
        onChange={(evento) => aoAlterar(paraFuso(evento.target.value))}
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
