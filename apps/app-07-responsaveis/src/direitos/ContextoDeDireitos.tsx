import { createContext, type ReactNode, useContext } from "react";

interface ContextoDeDireitosValor {
  irParaTransparencia: () => void;
}

const ContextoDeDireitos = createContext<ContextoDeDireitosValor | null>(null);

interface ProvedorDeDireitosProps extends ContextoDeDireitosValor {
  children: ReactNode;
}

// Deixa o `AvisoDeColeta`, em qualquer profundidade da árvore, levar à área
// detalhada sem prop-drilling pelas telas intermediárias — na App 07 essa
// área é a própria tela de transparência do vinculado, não uma tabela
// estática de direitos como nas Apps 03 e 09 (`RF-13-41`, design — decisão
// 4). A App.tsx decide para onde ir; este contexto só carrega o callback.
export function ProvedorDeDireitos({
  irParaTransparencia,
  children,
}: ProvedorDeDireitosProps) {
  return (
    <ContextoDeDireitos.Provider value={{ irParaTransparencia }}>
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
