import { type ReactNode, useEffect, useId, useRef } from "react";
import { Botao } from "./Botao";

interface Props {
  aberto: boolean;
  titulo: string;
  aoFechar: () => void;
  children: ReactNode;
}

// Sobre o elemento `dialog` nativo, aberto por `showModal`: o navegador já
// prende o foco e fecha por `Esc`. O componente acrescenta o rótulo
// acessível, o fechamento por botão com rótulo textual — ícone nunca
// sozinho (documento 15 §5) — e devolve o foco a quem abriu (design —
// decisão 3).
export function Dialogo({ aberto, titulo, aoFechar, children }: Props) {
  const referencia = useRef<HTMLDialogElement>(null);
  const idDoTitulo = useId();
  const elementoQueAbriu = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const dialogo = referencia.current;
    if (!dialogo) return;

    if (aberto && !dialogo.open) {
      elementoQueAbriu.current = document.activeElement as HTMLElement | null;
      dialogo.showModal();
    } else if (!aberto && dialogo.open) {
      dialogo.close();
    }
  }, [aberto]);

  useEffect(() => {
    const dialogo = referencia.current;
    if (!dialogo) return;

    function aoFecharPeloNavegador() {
      aoFechar();
      elementoQueAbriu.current?.focus();
    }

    dialogo.addEventListener("close", aoFecharPeloNavegador);
    return () => dialogo.removeEventListener("close", aoFecharPeloNavegador);
  }, [aoFechar]);

  return (
    <dialog ref={referencia} className="cg-dialogo" aria-labelledby={idDoTitulo}>
      <div className="cg-dialogo__cabecalho">
        <h2 id={idDoTitulo}>{titulo}</h2>
        <Botao variante="secundaria" onClick={() => referencia.current?.close()}>
          Fechar
        </Botao>
      </div>
      <div className="cg-dialogo__corpo">{children}</div>
    </dialog>
  );
}
