/// <reference path="./google-identity-services.d.ts" />
import { useEffect, useRef } from "react";

const URL_DO_SCRIPT = "https://accounts.google.com/gsi/client";

interface Props {
  clientId: string;
  aoReceberIdToken: (idToken: string) => void;
}

// O `id_token` vem do Google Identity Services, carregado do próprio Google
// — a única dependência externa em tempo de execução da aplicação (design —
// Decisions). O `clientId` chega por parâmetro, e não por variável de
// ambiente lida aqui dentro: cada aplicação declara o próprio, como a chave
// de aplicação e a URL do núcleo (design — decisão 6).
export function BotaoDeEntradaGoogle({ clientId, aoReceberIdToken }: Props) {
  const referenciaDoContainer = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!clientId) return;

    function inicializar() {
      const container = referenciaDoContainer.current;
      if (!window.google || !container) return;
      window.google.accounts.id.initialize({
        client_id: clientId,
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
  }, [clientId, aoReceberIdToken]);

  return <div ref={referenciaDoContainer} data-testid="botao-de-entrada-google" />;
}
