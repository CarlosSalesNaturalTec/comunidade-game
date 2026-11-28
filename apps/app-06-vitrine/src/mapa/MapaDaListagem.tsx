import { useMemo } from "react";
import { listarTodasAsComunidades } from "../api/leituras";
import { useLeitura } from "../leitura/useLeitura";
import { navegarPara } from "../navegacao/navegar";
import { caminhoDaComunidade } from "../navegacao/recortes";
import { MapaDeComunidades } from "./MapaDeComunidades";
import type { ComunidadeNoMapa } from "./tipos";

interface Props {
  irPara?: (destino: string) => void;
}

// O mapa da listagem: só quem tem contorno entra, e cada contorno abre a
// página da comunidade (`RF-03-89`, `RF-03-90`). Enquanto carrega, falha ou
// não há contorno algum, nada se desenha — a lista abaixo segue sendo a
// leitura das comunidades.
export function MapaDaListagem({ irPara = navegarPara }: Props) {
  const leitura = useLeitura(listarTodasAsComunidades, "comunidades/mapa");
  const comunidades = useMemo<ComunidadeNoMapa[]>(() => {
    if (leitura.situacao !== "pronta") return [];
    return leitura.dado.flatMap((comunidade) =>
      comunidade.contorno
        ? [
            {
              id: comunidade.id,
              nome: comunidade.nome,
              destino: caminhoDaComunidade(comunidade.id),
              contorno: comunidade.contorno,
            },
          ]
        : [],
    );
  }, [leitura]);

  return (
    <MapaDeComunidades
      modo="listagem"
      rotulo="Mapa das Comunidades Virtuais"
      comunidades={comunidades}
      irPara={(id) => irPara(caminhoDaComunidade(id))}
    />
  );
}
