import { type ReactNode, useEffect, useId, useRef } from "react";
import { Botao } from "./Botao";

interface Props {
  aberto: boolean;
  titulo: string;
  aoFechar: () => void;
  children: ReactNode;
  /** Ocupa a janela inteira — é a imagem ampliada da moldura fixa
   * (`MidiaDoNucleo`, decisão do fundador de 2026-11-11). */
  telaCheia?: boolean;
  /** Toque no fundo, fora do corpo e do cabeçalho, fecha o diálogo. */
  fecharAoTocarFora?: boolean;
}

// Sobre o elemento `dialog` nativo, aberto por `showModal`: o navegador já
// prende o foco e fecha por `Esc`. O componente acrescenta o rótulo
// acessível, o fechamento por botão com rótulo textual — ícone nunca
// sozinho (documento 15 §5) — e devolve o foco a quem abriu (design —
// decisão 3).
export function Dialogo({
  aberto,
  titulo,
  aoFechar,
  children,
  telaCheia = false,
  fecharAoTocarFora = false,
}: Props) {
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
    // O teclado já fecha por `Esc`, nativo do `dialog`: o toque no fundo é
    // atalho de ponteiro, não o único caminho de saída.
    // biome-ignore lint/a11y/useKeyWithClickEvents: `Esc` e o botão "Fechar" são o caminho do teclado.
    <dialog
      ref={referencia}
      className={telaCheia ? "cg-dialogo cg-dialogo--tela-cheia" : "cg-dialogo"}
      aria-labelledby={idDoTitulo}
      onClick={
        fecharAoTocarFora
          ? (evento) => {
              // O fundo é o próprio `dialog`: clique no corpo ou no
              // cabeçalho tem outro alvo e não fecha.
              if (evento.target === evento.currentTarget) referencia.current?.close();
            }
          : undefined
      }
    >
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
