import { MidiaDoNucleo } from "comum/react";
import { useEffect, useState } from "react";
import { type CriacaoPublica, lerArquivoDoAcervo } from "../api/leituras";

const ROTULO_DE_ABERTURA: Record<string, string> = {
  texto: "Ler a produção",
  imagem: "Ver a imagem",
  audio: "Ouvir o áudio",
  video: "Ver o vídeo",
};

const INDISPONIVEL = "A produção não está disponível agora.";

/**
 * A produção de um item do acervo, aberta **na própria linha** (`RF-03-85`).
 *
 * Sem endereço novo e sem camada sobreposta: a criação não tem página
 * individual (decisão do fundador de 2026-10-11), e são os **nicks** que
 * abrem página (`RF-03-03`). O aberto/fechado é estado **deste** componente,
 * nunca da `ListaDeRegistros`, que outras três seções usam — e por isso morre
 * ao recarregar e ao trocar de página, que é o que o `RN-03-22` exige: nada
 * da navegação do visitante é gravado no aparelho (design — decisão 6).
 *
 * Imagem, áudio e vídeo vão por `MidiaDoNucleo`, com `token` nulo — a vitrine
 * não tem sessão de persona (`RN-03-33`). Ele já busca os bytes com a chave
 * em cabeçalho, monta a URL de objeto, a revoga e trata a falha em moldura de
 * tamanho fixo; reimplementá-lo aqui é o desvio que a moldura comum veio
 * corrigir (design — decisão 7).
 *
 * O **link externo** sai como link de saída, sem embutir conteúdo de
 * terceiro, e o **arquivo**, como transferência nomeada pelo título. A falha
 * é dita em linguagem simples e **nunca** revela o motivo da recusa do
 * núcleo — que a autorização caiu, ou que o Mestre não tornou a entrega
 * publicável (`RN-03-02`).
 */
export function ProducaoDoAcervo({ item }: { item: CriacaoPublica }) {
  const [aberta, definirAberta] = useState(false);

  if (item.tipo === null) return null;

  if (item.tipo === "link_externo") {
    if (!item.producao) return null;
    return (
      <a
        className="cg-acervo__saida"
        href={item.producao}
        rel="noreferrer noopener"
        target="_blank"
      >
        Abrir a produção em outro site
      </a>
    );
  }

  if (item.tipo === "arquivo") {
    return <TransferenciaDoArquivo item={item} />;
  }

  if (!aberta) {
    return (
      <button className="cg-acervo__abrir" onClick={() => definirAberta(true)} type="button">
        {ROTULO_DE_ABERTURA[item.tipo]}
      </button>
    );
  }

  return (
    <div className="cg-acervo__producao">
      <button className="cg-acervo__fechar" onClick={() => definirAberta(false)} type="button">
        Fechar a produção
      </button>
      {item.tipo === "texto" ? (
        <p className="cg-acervo__texto">{item.producao ?? INDISPONIVEL}</p>
      ) : (
        <MidiaDoNucleo
          alt={`Produção de ${item.titulo}`}
          buscar={(id) => lerArquivoDoAcervo({ id, fonte: item.fonte })}
          id={item.id}
          textoDeErro={INDISPONIVEL}
          semSessao
          tipo={item.tipo}
          token={null}
        />
      )}
    </div>
  );
}

/** A transferência do tipo arquivo: os bytes também exigem a chave em
 * cabeçalho, então o endereço local nasce de um `Blob` e é revogado ao
 * desmontar. Nome do arquivo: o título do item (`RF-03-85`). */
function TransferenciaDoArquivo({ item }: { item: CriacaoPublica }) {
  const [estado, definirEstado] = useState<{
    endereco: string | null;
    naoAbriu: boolean;
  } | null>(null);

  useEffect(() => {
    return () => {
      if (estado?.endereco) URL.revokeObjectURL(estado.endereco);
    };
  }, [estado]);

  if (estado?.naoAbriu) {
    return <p className="cg-acervo__indisponivel">{INDISPONIVEL}</p>;
  }

  if (estado?.endereco) {
    return (
      <a className="cg-acervo__saida" download={item.titulo} href={estado.endereco}>
        Salvar a produção
      </a>
    );
  }

  return (
    <button
      className="cg-acervo__abrir"
      onClick={async () => {
        try {
          const bytes = await lerArquivoDoAcervo(item);
          definirEstado({ endereco: URL.createObjectURL(bytes), naoAbriu: false });
        } catch {
          definirEstado({ endereco: null, naoAbriu: true });
        }
      }}
      type="button"
    >
      Preparar a produção para salvar
    </button>
  );
}
