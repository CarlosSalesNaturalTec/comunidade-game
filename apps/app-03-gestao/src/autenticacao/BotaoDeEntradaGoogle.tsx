import { useEffect, useRef } from "react";
import { GOOGLE_CLIENT_ID } from "../api/configuracao";

const URL_DO_SCRIPT = "https://accounts.google.com/gsi/client";

interface Props {
  aoReceberIdToken: (idToken: string) => void;
}

// O `id_token` vem do Google Identity Services, carregado do próprio Google
// — a única dependência externa em tempo de execução da aplicação (design —
// Decisions).
export function BotaoDeEntradaGoogle({ aoReceberIdToken }: Props) {
  const referenciaDoContainer = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!GOOGLE_CLIENT_ID) return;

    function inicializar() {
      const container = referenciaDoContainer.current;
      if (!window.google || !container) return;
      window.google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: (resposta) => aoReceberIdToken(resposta.credential),
      });
      window.google.accounts.id.renderButton(container, { theme: "outline", size: "large" });
    }

    if (window.google) {
      inicializar();
      return;
    }

    const script = document.createElement("script");
    script.src = URL_DO_SCRIPT;
    script.async = true;
    script.defer = true;
    script.addEventListener("load", inicializar);
    document.body.appendChild(script);

    return () => {
      script.removeEventListener("load", inicializar);
      script.remove();
    };
  }, [aoReceberIdToken]);

  return <div ref={referenciaDoContainer} data-testid="botao-de-entrada-google" />;
}
