import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import {
  type Local,
  listarLocaisDaComunidade,
  listarMinhasSeries,
  type SerieDoGuerreiro,
} from "../api/coleta";

const ROTULO_DO_ESTADO: Record<SerieDoGuerreiro["estado"], string> = {
  ativa: "Em dia",
  interrompida: "Parada — retome quando puder",
  encerrada: "Encerrada",
};

function formatarData(valorIso: string | null): string {
  if (!valorIso) return "";
  return new Date(valorIso).toLocaleDateString("pt-BR");
}

interface Props {
  aoAbrirNovaSerie: () => void;
  aoVerSolicitacoes: () => void;
  aoRegistrarNaSerie: (serie: SerieDoGuerreiro) => void;
  aoVerHistorico: (serie: SerieDoGuerreiro) => void;
}

// A lista das próprias séries: o que cada uma mede, o local, o estado, a
// próxima medição e os pontos que está rendendo (`RF-05-30`, `RF-05-36`,
// PRD-05 §5.4). Quem usa força uma releitura — depois de abrir série ou
// gravar um registro, por exemplo — remontando este componente com uma
// `key` nova.
export function ListaDeSeries({
  aoAbrirNovaSerie,
  aoVerSolicitacoes,
  aoRegistrarNaSerie,
  aoVerHistorico,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [series, definirSeries] = useState<SerieDoGuerreiro[] | null>(null);
  const [locais, definirLocais] = useState<Record<string, Local>>({});
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    const token = sessao.token;
    let cancelado = false;

    async function carregar() {
      definirErro(null);
      try {
        const pagina = await listarMinhasSeries(token);
        if (cancelado) return;
        definirSeries(pagina.itens);

        const comunidadeId = pagina.itens[0]?.comunidade_virtual_id;
        if (comunidadeId) {
          const paginaDeLocais = await listarLocaisDaComunidade(comunidadeId);
          if (cancelado) return;
          const mapa: Record<string, Local> = {};
          for (const local of paginaDeLocais.itens) mapa[local.id] = local;
          definirLocais(mapa);
        }
      } catch (erroCapturado) {
        if (cancelado) return;
        if (
          erroCapturado &&
          typeof erroCapturado === "object" &&
          "codigo" in erroCapturado &&
          (erroCapturado.codigo === "sessao_ausente" ||
            erroCapturado.codigo === "sessao_invalida")
        ) {
          tratarRecusaDeSessao();
          return;
        }
        definirErro(
          "Não foi possível carregar as suas séries agora. Tente de novo em instantes.",
        );
      }
    }

    carregar();
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  return (
    <section className="cg-coleta-secao" aria-label="Coleta do território">
      <div className="cg-coleta-secao__acoes">
        <Botao onClick={aoAbrirNovaSerie}>Abrir nova série</Botao>
        <Botao variante="secundaria" onClick={aoVerSolicitacoes}>
          Meus pedidos de local
        </Botao>
      </div>

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {series === null && !erro && <EstadoDaLista>Carregando as suas séries…</EstadoDaLista>}
      {series !== null && series.length === 0 && (
        <EstadoDaLista>Você ainda não abriu nenhuma série de coleta.</EstadoDaLista>
      )}

      {series !== null && series.length > 0 && (
        <ul className="cg-lista-de-series">
          {series.map((serie) => {
            const local = locais[serie.local_id];
            const interrompida = serie.estado === "interrompida";
            return (
              <li key={serie.id} className="cg-cartao-de-serie">
                <p className="cg-cartao-de-serie__titulo">
                  {serie.tipo_de_coleta.nome}
                  {serie.tipo_de_coleta.unidade ? ` (${serie.tipo_de_coleta.unidade})` : ""}
                </p>
                <p>Local: {local ? local.rotulo : "—"}</p>
                <p>Estado: {ROTULO_DO_ESTADO[serie.estado]}</p>
                {serie.proxima_medicao && (
                  <p>Próxima medição: {formatarData(serie.proxima_medicao)}</p>
                )}
                <p>Pontos rendidos: {serie.pontos}</p>
                {interrompida && (
                  <Aviso tipo="atencao">
                    Essa série está parada, mas os pontos que você já ganhou continuam valendo.
                    Registre de novo para retomar.
                  </Aviso>
                )}
                {serie.estado !== "encerrada" && (
                  <Botao onClick={() => aoRegistrarNaSerie(serie)}>
                    {interrompida ? "Registrar de novo" : "Registrar medição"}
                  </Botao>
                )}
                <Botao variante="secundaria" onClick={() => aoVerHistorico(serie)}>
                  Ver histórico
                </Botao>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
