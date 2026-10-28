import { useSessao } from "comum/autenticacao";
import { Aviso, MidiaDoNucleo } from "comum/react";
import { useEffect, useState } from "react";
import { type ConteudoDaMissao, lerArquivoDoConteudo } from "./api";

// Texto e link saem do próprio conteúdo; imagem e vídeo vêm em bytes do
// núcleo, buscados por `MidiaDoNucleo` numa moldura de tamanho fixo, porque
// toda rota sob `/v1` exige a chave da aplicação em cabeçalho e `<img src>`
// não a manda (`RF-09-25`, design — decisão 3 e 4 desta fatia). Antes da
// fatia anterior, os três apareciam como a frase "Arquivo enviado.".
export function ConteudoExibido({
  conteudo,
  tituloDaMissao,
}: {
  conteudo: ConteudoDaMissao;
  tituloDaMissao: string;
}) {
  const { sessao } = useSessao();
  const token = sessao?.token ?? null;
  const temArquivo = conteudo.referencia !== null;

  if (conteudo.tipo === "texto") return <p>{conteudo.corpo}</p>;
  if (conteudo.tipo === "link_externo") {
    return <a href={conteudo.endereco ?? "#"}>{conteudo.endereco}</a>;
  }

  // Envio não concluído é dito pendente, nunca apresentado como quebrado.
  if (!temArquivo) return <p>Envio ainda não concluído.</p>;

  if (conteudo.tipo === "imagem" || conteudo.tipo === "video") {
    return (
      <MidiaDoNucleo
        id={conteudo.id}
        buscar={lerArquivoDoConteudo}
        token={token}
        tipo={conteudo.tipo}
        alt={
          conteudo.tipo === "imagem"
            ? `Conteúdo de ${tituloDaMissao}`
            : `Vídeo de ${tituloDaMissao}`
        }
        textoDeErro="Esse arquivo não abriu agora, mas segue anexado."
      />
    );
  }
  return <ArquivoDeApoio conteudo={conteudo} token={token} />;
}

// O arquivo de apoio não é mídia embutida: é link para o Mestre conferir o
// que anexou (design — decisão 4, Risks/Trade-offs, desta fatia).
function ArquivoDeApoio({
  conteudo,
  token,
}: {
  conteudo: ConteudoDaMissao;
  token: string | null;
}) {
  const [endereco, definirEndereco] = useState<string | null>(null);
  const [naoAbriu, definirNaoAbriu] = useState(false);

  useEffect(() => {
    if (!token) return;
    let local: string | null = null;
    let descartado = false;
    lerArquivoDoConteudo(conteudo.id, token)
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
  }, [conteudo.id, token]);

  if (naoAbriu) {
    return <Aviso tipo="atencao">Esse arquivo não abriu agora, mas segue anexado.</Aviso>;
  }
  if (!endereco) return <p>Carregando o arquivo…</p>;
  return <a href={endereco}>Abrir o arquivo de apoio</a>;
}
