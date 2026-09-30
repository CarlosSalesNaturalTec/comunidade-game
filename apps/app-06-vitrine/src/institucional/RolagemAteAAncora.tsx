import { useEffect } from "react";

/**
 * Leva a nota de transparência, que o texto reescrito por IA aponta pela
 * âncora do endereço, ao foco assim que a tela está montada (`RF-03-48`).
 *
 * Vive sozinha, e não dentro da seção, porque a seção passou a ser renderizada
 * no build: `window` não existe ali. Aqui é ilha, roda no aparelho, e não
 * apresenta nada — só move o foco para onde o endereço pediu.
 */
export function RolagemAteAAncora() {
  useEffect(() => {
    const id = decodeURIComponent(window.location.hash.slice(1));
    if (id === "") return;
    const alvo = document.getElementById(id);
    if (alvo === null) return;
    alvo.scrollIntoView?.();
    alvo.focus();
  }, []);

  return null;
}
