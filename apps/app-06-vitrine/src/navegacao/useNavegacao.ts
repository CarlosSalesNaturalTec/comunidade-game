import { useCallback, useEffect, useRef, useState } from "react";

/** Navegação por **endereço real**, sobre a History API: cada seção da vitrine
 * tem caminho próprio, o que a torna compartilhável e indexável (PRD-03 §10) e
 * o que a fatia seguinte exige para a página individual responder por endereço
 * direto. Sem biblioteca de rotas — escolha de _framework_ que os documentos
 * não decidem — e sem nada guardado no aparelho (`RF-03-51`, `RN-03-22`;
 * design — decisão 2). */
export function useNavegacao() {
  const [caminho, definirCaminho] = useState(() => window.location.pathname);
  // Quantos endereços esta carga empilhou. Vive só em memória e morre na
  // recarga: é o que faz o voltar da recusa devolver o visitante à página que
  // ele estava lendo sem guardar histórico em lugar nenhum (`RF-03-38`,
  // `RN-03-15`; design — decisão 4).
  const empilhados = useRef(0);

  useEffect(() => {
    function aoVoltar() {
      if (empilhados.current > 0) empilhados.current -= 1;
      definirCaminho(window.location.pathname);
    }
    window.addEventListener("popstate", aoVoltar);
    return () => window.removeEventListener("popstate", aoVoltar);
  }, []);

  const irPara = useCallback((destino: string) => {
    if (destino === window.location.pathname) return;
    window.history.pushState(null, "", destino);
    empilhados.current += 1;
    definirCaminho(destino);
  }, []);

  /** Devolve o visitante à navegação de onde ele veio. Aberta a tela por
   * endereço direto — sem nada empilhado nesta carga —, não há para onde voltar
   * e a saída é a raiz (`RF-03-44`). */
  const voltar = useCallback(() => {
    if (empilhados.current > 0) {
      window.history.back();
      return;
    }
    window.history.pushState(null, "", "/");
    definirCaminho("/");
  }, []);

  return { caminho, irPara, voltar };
}
