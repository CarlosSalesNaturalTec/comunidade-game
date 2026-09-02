import { createContext, type ReactNode, useContext } from "react";

interface ContextoDeDireitosValor {
  irParaDireitos: () => void;
}

const ContextoDeDireitos = createContext<ContextoDeDireitosValor | null>(null);

interface ProvedorDeDireitosProps extends ContextoDeDireitosValor {
  children: ReactNode;
}

// Deixa o `AvisoDeColeta`, em qualquer profundidade da árvore, levar à área
// Direitos e dados sem prop-drilling pelas telas intermediárias — é a
// App.tsx quem decide a área, este contexto só carrega o callback até quem
// precisa dele. Mesmo desenho das Apps 03 e 09 (`RF-14-58`). Na App 08 o
// provedor envolve também a árvore sem sessão, porque a porta pública já
// coleta dado antes de haver Apoiador (design — decisão 4).
export function ProvedorDeDireitos({ irParaDireitos, children }: ProvedorDeDireitosProps) {
  return (
    <ContextoDeDireitos.Provider value={{ irParaDireitos }}>
      {children}
    </ContextoDeDireitos.Provider>
  );
}

export function useDireitos(): ContextoDeDireitosValor {
  const contexto = useContext(ContextoDeDireitos);
  if (!contexto) {
    throw new Error("useDireitos precisa de um ProvedorDeDireitos.");
  }
  return contexto;
}
