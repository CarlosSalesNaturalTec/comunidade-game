import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { Protocol } from "pmtiles";
import type { ComunidadeNoMapa, ModoDoMapa } from "./tipos";

// O único ponto que conhece o MapLibre. Importado por `import()` dinâmico, para
// a página não carregar o motor antes de precisar, e substituído nos testes,
// que não têm WebGL (design — Decisão 4).

// Tudo sai da própria origem da App 06: estilo, recorte e nenhum glifo ou
// sprite (`RN-03-45`, design — Decisões 2 e 3).
export const ESTILO_DO_MAPA = "/mapa/estilo.json";

let protocoloRegistrado = false;

function registrarProtocolo() {
  if (protocoloRegistrado) return;
  const protocolo = new Protocol();
  maplibregl.addProtocol("pmtiles", protocolo.tile);
  protocoloRegistrado = true;
}

type Posicao = [number, number];

function posicoesDe(geometria: Record<string, unknown>): Posicao[] {
  const coordenadas = geometria.coordinates as unknown;
  const posicoes: Posicao[] = [];
  const percorrer = (valor: unknown) => {
    if (Array.isArray(valor) && typeof valor[0] === "number" && typeof valor[1] === "number") {
      posicoes.push([valor[0], valor[1]]);
      return;
    }
    if (Array.isArray(valor)) valor.forEach(percorrer);
  };
  percorrer(coordenadas);
  return posicoes;
}

export function envoltorio(comunidades: ComunidadeNoMapa[]): [Posicao, Posicao] {
  const posicoes = comunidades.flatMap((comunidade) =>
    posicoesDe(comunidade.contorno.geometria),
  );
  const longitudes = posicoes.map((posicao) => posicao[0]);
  const latitudes = posicoes.map((posicao) => posicao[1]);
  return [
    [Math.min(...longitudes), Math.min(...latitudes)],
    [Math.max(...longitudes), Math.max(...latitudes)],
  ];
}

export interface MontagemDoMapa {
  elemento: HTMLElement;
  comunidades: ComunidadeNoMapa[];
  modo: ModoDoMapa;
  irPara: (id: string) => void;
}

/** Monta o mapa e devolve a função que o desmonta. Desenha só o contorno e o
 * nome de cada comunidade — nunca local, ponto ou coletor (`RN-03-44`). */
export function montarMapa({ elemento, comunidades, modo, irPara }: MontagemDoMapa) {
  registrarProtocolo();
  const mapa = new maplibregl.Map({
    container: elemento,
    style: ESTILO_DO_MAPA,
    bounds: envoltorio(comunidades),
    fitBoundsOptions: { padding: 32 },
    attributionControl: { compact: false },
  });

  const contornos = {
    type: "FeatureCollection" as const,
    features: comunidades.map((comunidade) => ({
      type: "Feature" as const,
      properties: { id: comunidade.id },
      geometry: comunidade.contorno.geometria as unknown as GeoJSON.Geometry,
    })),
  };

  mapa.on("load", () => {
    mapa.addSource("contornos", { type: "geojson", data: contornos });
    mapa.addLayer({
      id: "contornos-preenchimento",
      type: "fill",
      source: "contornos",
      paint: { "fill-color": "#f25c05", "fill-opacity": modo === "destaque" ? 0.25 : 0.15 },
    });
    mapa.addLayer({
      id: "contornos-linha",
      type: "line",
      source: "contornos",
      paint: { "line-color": "#b33c00", "line-width": modo === "destaque" ? 3 : 2 },
    });
    if (modo === "listagem") {
      mapa.on("click", "contornos-preenchimento", (evento) => {
        const id = evento.features?.[0]?.properties?.id;
        if (typeof id === "string") irPara(id);
      });
    }
  });

  const marcadores = comunidades.map((comunidade) => {
    const [[oeste, sul], [leste, norte]] = envoltorio([comunidade]);
    const rotulo = document.createElement(modo === "listagem" ? "a" : "span");
    rotulo.className = "cg-mapa__nome";
    rotulo.textContent = comunidade.nome;
    if (rotulo instanceof HTMLAnchorElement) {
      rotulo.href = comunidade.destino;
      rotulo.addEventListener("click", (evento) => {
        evento.preventDefault();
        irPara(comunidade.id);
      });
    }
    return new maplibregl.Marker({ element: rotulo })
      .setLngLat([(oeste + leste) / 2, (sul + norte) / 2])
      .addTo(mapa);
  });

  return () => {
    for (const marcador of marcadores) marcador.remove();
    mapa.remove();
  };
}
