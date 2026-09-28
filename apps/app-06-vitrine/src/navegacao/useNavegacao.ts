import { useCallback, useEffect, useState } from "react";

/** Navegação por **endereço real**, sobre a History API: cada seção da vitrine
 * tem caminho próprio, o que a torna compartilhável e indexável (PRD-03 §10) e
 * o que a fatia seguinte exige para a página individual responder por endereço
 * direto. Sem biblioteca de rotas — escolha de _framework_ que os documentos
 * não decidem — e sem nada guardado no aparelho (`RF-03-51`, `RN-03-22`;
 * design — decisão 2). */
export function useNavegacao() {
  const [caminho, definirCaminho] = useState(() => window.location.pathname);

  useEffect(() => {
    function aoVoltar() {
      definirCaminho(window.location.pathname);
    }
    window.addEventListener("popstate", aoVoltar);
    return () => window.removeEventListener("popstate", aoVoltar);
  }, []);

  const irPara = useCallback((destino: string) => {
    if (destino === window.location.pathname) return;
    window.history.pushState(null, "", destino);
    definirCaminho(destino);
  }, []);

  return { caminho, irPara };
}
