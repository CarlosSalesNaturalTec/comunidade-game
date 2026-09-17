import { useEffect, useState } from "react";
import { Aviso } from "./Aviso";
import { EstadoDaLista } from "./EstadoDaLista";

interface Props {
  id: string;
  buscar: (id: string, token: string) => Promise<Blob>;
  token: string | null;
  tipo: "imagem" | "video";
  alt: string;
  textoDeErro: string;
}

// Busca a mídia do núcleo em bytes: nenhuma rota sob `/v1` aceita
// `<img src>`/`<video src>` direto, porque toda rota exige a chave da
// aplicação em cabeçalho. Monta uma URL de objeto local e a revoga ao
// desmontar, para não vazar memória em tela com muita mídia. Exibe numa
// moldura de tamanho fixo (`--largura-de-miniatura` × `--altura-de-miniatura`),
// com o conteúdo inteiro visível — nunca cortado — e sem oferecer
// ampliação (`RF-09-25`, `RF-05-11`, `RF-09-119`, decisão do fundador de
// 2026-09-17). Falhar em carregar nunca impede o resto da tela de
// funcionar: a moldura mostra o aviso de erro que o chamador escolher.
export function MidiaDoNucleo({ id, buscar, token, tipo, alt, textoDeErro }: Props) {
  const [endereco, definirEndereco] = useState<string | null>(null);
  const [naoAbriu, definirNaoAbriu] = useState(false);

  useEffect(() => {
    if (!token) return;
    let local: string | null = null;
    let descartado = false;
    buscar(id, token)
      .then((bytes) => {
        if (descartado) return;
        local = URL.createObjectURL(bytes);
        definirEndereco(local);
      })
      .catch(() => {
        if (!descartado) definirNaoAbriu(true);
      });
    return () => {
      descartado = true;
      if (local) URL.revokeObjectURL(local);
    };
  }, [id, token, buscar]);

  return (
    <div className="cg-midia-do-nucleo">
      {naoAbriu && <Aviso tipo="atencao">{textoDeErro}</Aviso>}
      {!naoAbriu && !endereco && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {!naoAbriu && endereco && tipo === "imagem" && (
        <img src={endereco} alt={alt} onError={() => definirNaoAbriu(true)} />
      )}
      {!naoAbriu && endereco && tipo === "video" && (
        // biome-ignore lint/a11y/useMediaCaption: legenda do vídeo do Mestre não é declarada no Ciclo 01 — o PRD-09 não a prevê.
        <video
          src={endereco}
          controls
          aria-label={alt}
          onError={() => definirNaoAbriu(true)}
        />
      )}
    </div>
  );
}
