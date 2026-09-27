import type { ReactNode } from "react";
import type { Fala } from "../narracao/narracao";
import { useNarrarAoEntrar } from "../narracao/ProvedorDeNarracao";

export type TipoDeAviso = "erro" | "atencao" | "sucesso" | "andamento";

interface Props {
  tipo: TipoDeAviso;
  children: ReactNode;
  /** O que este aviso **fala** ao entrar na tela. Omitida, fala o rótulo e o
   * texto do aviso quando o conteúdo é texto simples — a propriedade
   * declarada por quem montou a tela, não o documento apresentado. `null`
   * cala este aviso (documento 15 §5.1, design — decisão 4). */
  narracao?: Fala | null;
}

const ROTULO: Record<TipoDeAviso, string> = {
  erro: "Erro:",
  atencao: "Atenção:",
  sucesso: "Sucesso:",
  andamento: "Em andamento:",
};

// Erro e recusa interrompem (`role="alert"`); andamento e sucesso apenas
// informam (`role="status"`) — cada aviso leva rótulo textual que o
// identifica sem depender da cor (documento 15 §5, requisitos "Nenhum
// estado se comunica apenas por cor").
const PAPEL: Record<TipoDeAviso, "alert" | "status"> = {
  erro: "alert",
  atencao: "alert",
  sucesso: "status",
  andamento: "status",
};

// O rótulo entra na fala porque é o que o aviso diz por escrito: quem ouve
// recebe o mesmo aviso que quem lê. Conteúdo que não é texto simples — nós
// de React montados pela tela — só fala com `narracao` declarada: adivinhar
// o texto de dentro deles seria extrair do documento apresentado, que o
// documento 15 §5.1 veda.
function falaDoAviso(tipo: TipoDeAviso, children: ReactNode): Fala | null {
  if (typeof children !== "string") return null;
  return { texto: `${ROTULO[tipo]} ${children}` };
}

export function Aviso({ tipo, children, narracao }: Props) {
  const fala = narracao === undefined ? falaDoAviso(tipo, children) : narracao;
  useNarrarAoEntrar(fala === null ? null : fala.texto, fala?.nick);

  return (
    <p role={PAPEL[tipo]} className={`cg-aviso cg-aviso--${tipo}`}>
      <span className="cg-aviso__rotulo">{ROTULO[tipo]}</span> {children}
    </p>
  );
}
