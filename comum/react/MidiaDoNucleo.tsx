import { useEffect, useRef, useState } from "react";
import { Aviso } from "./Aviso";
import { EstadoDaLista } from "./EstadoDaLista";

interface Props {
  id: string;
  buscar: (id: string, token: string) => Promise<Blob>;
  token: string | null;
  tipo: "imagem" | "video";
  alt: string;
  textoDeErro: string;
  /** Diz a quem monta se a mídia **da vez** está sendo buscada, para que a
   * sequência possa travar avançar e voltar enquanto ela não chega. Reporta
   * `false` também na **falha** e na **desmontagem**: sem as duas quedas, a
   * mídia que não abre — ou o item seguinte que não tem mídia alguma —
   * deixaria a trava armada para sempre (design — decisão 7). */
  aoMudarCarregamento?: (carregando: boolean) => void;
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
//
// O resultado é guardado **junto do `id` que o produziu**, e não solto: numa
// sequência paginada o React reaproveita esta instância entre itens, e estado
// que não acompanha o `id` deixava a mídia do item **anterior** na tela sob o
// item novo — informação errada apresentada como se fosse a correta, com o
// "Carregando…" nunca aparecendo porque havia endereço, a URL já revogada
// ainda referenciada e a falha de um item grudando em todos os seguintes.
// `id` diferente do guardado **é** o estado de carga (design — decisão 6).
export function MidiaDoNucleo({
  id,
  buscar,
  token,
  tipo,
  alt,
  textoDeErro,
  aoMudarCarregamento,
}: Props) {
  const [resultado, definirResultado] = useState<{
    id: string;
    endereco: string | null;
    naoAbriu: boolean;
  } | null>(null);

  // O aviso é lido no efeito e na limpeza, e trocá-lo não deve refazer a
  // busca — daí a referência, e não a dependência.
  const avisar = useRef(aoMudarCarregamento);
  avisar.current = aoMudarCarregamento;

  useEffect(() => {
    if (!token) return;
    let local: string | null = null;
    let descartado = false;
    avisar.current?.(true);
    buscar(id, token)
      .then((bytes) => {
        if (descartado) return;
        local = URL.createObjectURL(bytes);
        definirResultado({ id, endereco: local, naoAbriu: false });
        avisar.current?.(false);
      })
      .catch(() => {
        if (descartado) return;
        definirResultado({ id, endereco: null, naoAbriu: true });
        avisar.current?.(false);
      });
    return () => {
      descartado = true;
      // Sem isto, ir para um item **sem** mídia desmonta esta instância com
      // a trava armada e prende a navegação (design — decisão 7).
      avisar.current?.(false);
      if (local) URL.revokeObjectURL(local);
    };
  }, [id, token, buscar]);

  // Resultado de outro `id` não vale para este item: nem a mídia, nem a falha.
  const daVez = resultado?.id === id ? resultado : null;
  const carregando = daVez === null;

  return (
    <div className="cg-midia-do-nucleo">
      {daVez?.naoAbriu && <Aviso tipo="atencao">{textoDeErro}</Aviso>}
      {carregando && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {daVez?.endereco && tipo === "imagem" && (
        <img
          src={daVez.endereco}
          alt={alt}
          onError={() => definirResultado({ id, endereco: null, naoAbriu: true })}
        />
      )}
      {daVez?.endereco && tipo === "video" && (
        // biome-ignore lint/a11y/useMediaCaption: legenda do vídeo do Mestre não é declarada no Ciclo 01 — o PRD-09 não a prevê.
        <video
          src={daVez.endereco}
          controls
          aria-label={alt}
          onError={() => definirResultado({ id, endereco: null, naoAbriu: true })}
        />
      )}
    </div>
  );
}
