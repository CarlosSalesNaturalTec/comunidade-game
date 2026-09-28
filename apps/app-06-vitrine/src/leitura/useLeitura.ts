import { useEffect, useState } from "react";

// A leitura pública de uma tela, em três estados. Nada do que volta é
// guardado no aparelho: a vitrine relê a cada visita, e é isso que faz a
// revogação da autorização valer na leitura seguinte (`RF-03-14`,
// `RN-03-03`, `RN-03-22`, design — decisão 7).

export type EstadoDaLeitura<Dado> =
  | { situacao: "carregando" }
  | { situacao: "pronta"; dado: Dado }
  | { situacao: "falhou"; erro: unknown };

export function useLeitura<Dado>(
  ler: () => Promise<Dado>,
  chave: string,
): EstadoDaLeitura<Dado> {
  const [estado, definirEstado] = useState<EstadoDaLeitura<Dado>>({ situacao: "carregando" });

  // A **chave** declara o que refaz a leitura; a função de ler muda a cada
  // render e não serve de dependência.
  // biome-ignore lint/correctness/useExhaustiveDependencies: a chave é a dependência declarada.
  useEffect(() => {
    let vigente = true;
    definirEstado({ situacao: "carregando" });
    ler()
      .then((dado) => {
        if (vigente) definirEstado({ situacao: "pronta", dado });
      })
      .catch((erro) => {
        if (vigente) definirEstado({ situacao: "falhou", erro });
      });
    return () => {
      vigente = false;
    };
  }, [chave]);

  return estado;
}
