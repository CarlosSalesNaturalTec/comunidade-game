import { useEffect, useRef, useState } from "react";
import type { ComunidadeNoMapa, ModoDoMapa } from "./tipos";

interface Props {
  comunidades: ComunidadeNoMapa[];
  modo: ModoDoMapa;
  rotulo: string;
  irPara: (id: string) => void;
}

// O mapa das Comunidades Virtuais: na listagem, todos os contornos, cada um
// abrindo a página da comunidade; na página, o contorno dela em destaque
// (`RF-03-89` a `RF-03-91`). Complementa a lista e a representação visual
// genérica, nunca as substitui (`RN-03-46`), e sem contorno não monta: nada de
// mapa vazio nem de aviso.
//
// O motor do MapLibre chega por `import()` dinâmico (design — Decisão 4).
export function MapaDeComunidades({ comunidades, modo, rotulo, irPara }: Props) {
  const elemento = useRef<HTMLElement>(null);
  const irParaAtual = useRef(irPara);
  irParaAtual.current = irPara;
  const [falhou, definirFalhou] = useState(false);

  useEffect(() => {
    const alvo = elemento.current;
    if (!alvo || comunidades.length === 0) return;
    let desmontar: (() => void) | undefined;
    let cancelado = false;
    import("./motorDoMapa")
      .then(({ montarMapa }) => {
        if (cancelado) return;
        desmontar = montarMapa({
          elemento: alvo,
          comunidades,
          modo,
          irPara: (id) => irParaAtual.current(id),
        });
      })
      .catch(() => {
        if (!cancelado) definirFalhou(true);
      });
    return () => {
      cancelado = true;
      desmontar?.();
    };
  }, [comunidades, modo]);

  if (comunidades.length === 0) return null;

  // O crédito e a licença vêm do núcleo, iguais em todo contorno — o contorno
  // é sempre cópia do OSM (`RF-03-92`, design — Decisão 6).
  const { credito, licenca } = comunidades[0].contorno;

  return (
    <figure className={`cg-mapa cg-mapa--${modo}`}>
      {falhou ? (
        <p className="cg-mapa__indisponivel" role="status">
          O mapa não pôde ser carregado agora.
        </p>
      ) : (
        <section ref={elemento} className="cg-mapa__tela" aria-label={rotulo} />
      )}
      <figcaption className="cg-mapa__credito">
        {credito} · {licenca}
      </figcaption>
    </figure>
  );
}
