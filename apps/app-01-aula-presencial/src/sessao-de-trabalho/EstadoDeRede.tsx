import { createContext, type ReactNode, useCallback, useContext, useEffect, useState } from "react";

interface EstadoDeRedeValor {
  semRede: boolean;
  marcarFalhaDeRede: () => void;
  marcarSucessoDeRede: () => void;
}

const PADRAO: EstadoDeRedeValor = {
  semRede: false,
  marcarFalhaDeRede: () => {},
  marcarSucessoDeRede: () => {},
};

const ContextoDeRede = createContext<EstadoDeRedeValor | null>(null);

// O estado "sem rede" do aparelho inteiro, elevado de cada tela para cá
// (`RF-04-23`, `RF-04-24`, design — decisão 9): quem chama o núcleo marca a
// falha ou o sucesso, e o aviso aparece em toda tela enquanto durar. O
// evento `offline` do navegador só adianta o aviso — a verdade continua
// sendo a chamada ao núcleo que falha ou que conclui (`navigator.onLine`
// nunca decide sozinho, só dispara nova tentativa em quem sincroniza).
export function ProvedorDeEstadoDeRede({ children }: { children: ReactNode }) {
  const [semRede, definirSemRede] = useState(false);

  const marcarFalhaDeRede = useCallback(() => definirSemRede(true), []);
  const marcarSucessoDeRede = useCallback(() => definirSemRede(false), []);

  useEffect(() => {
    window.addEventListener("offline", marcarFalhaDeRede);
    return () => window.removeEventListener("offline", marcarFalhaDeRede);
  }, [marcarFalhaDeRede]);

  return (
    <ContextoDeRede.Provider value={{ semRede, marcarFalhaDeRede, marcarSucessoDeRede }}>
      {children}
    </ContextoDeRede.Provider>
  );
}

// Fora do provedor (telas testadas isoladamente, sem o aparelho inteiro),
// devolve o padrão sem rede fora do ar — nunca lança, ao contrário de
// `useSessao`: aqui a ausência de provedor é cenário de teste legítimo, não
// erro de composição.
export function useEstadoDeRede(): EstadoDeRedeValor {
  const contexto = useContext(ContextoDeRede);
  return contexto ?? PADRAO;
}
