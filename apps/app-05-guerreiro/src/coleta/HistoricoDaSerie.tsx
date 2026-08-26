import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import {
  listarHistoricoDaSerie,
  type RegistroDoHistorico,
  type SerieDoGuerreiro,
} from "../api/coleta";

function formatarData(valorIso: string): string {
  return new Date(valorIso).toLocaleString("pt-BR");
}

interface Props {
  serie: SerieDoGuerreiro;
  aoVoltar: () => void;
}

// Histórico da série: data, valor, situação e pontos de cada registro, com
// o motivo do que foi invalidado — só aquele registro perde os pontos, a
// série continua (`RF-05-37`, `RF-05-38`, `RN-05-09`, PRD-05 §12).
export function HistoricoDaSerie({ serie, aoVoltar }: Props) {
  const { sessao } = useSessao();
  const [registros, definirRegistros] = useState<RegistroDoHistorico[] | null>(null);

  useEffect(() => {
    if (!sessao) return;
    listarHistoricoDaSerie(serie.id, sessao.token)
      .then((pagina) => definirRegistros(pagina.itens))
      .catch(() => definirRegistros([]));
  }, [sessao, serie.id]);

  return (
    <section aria-label="Histórico da série">
      <h2>Histórico — {serie.tipo_de_coleta.nome}</h2>

      {registros === null && <EstadoDaLista>Carregando o histórico…</EstadoDaLista>}
      {registros !== null && registros.length === 0 && (
        <EstadoDaLista>Ainda não há nenhum registro nessa série.</EstadoDaLista>
      )}
      {registros !== null && registros.length > 0 && (
        <ul className="cg-lista-de-registros">
          {registros.map((registro) => (
            <li key={registro.id} className="cg-cartao-de-registro">
              <p>{formatarData(registro.momento_do_fato)}</p>
              <p>
                {registro.valor !== null
                  ? `${registro.valor}${registro.unidade ? ` ${registro.unidade}` : ""}`
                  : "Mídia enviada"}
              </p>
              {registro.situacao === "invalidada" ? (
                <Aviso tipo="atencao">
                  Este registro não valeu
                  {registro.motivo_da_invalidacao
                    ? `: ${registro.motivo_da_invalidacao}`
                    : "."}{" "}
                  Só ele perdeu os pontos — a série continua.
                </Aviso>
              ) : registro.a_conferir ? (
                <p>A conferir — o Mestre ainda vai olhar.</p>
              ) : (
                <p>Pontos: {registro.pontos_creditados}</p>
              )}
            </li>
          ))}
        </ul>
      )}

      <Botao variante="secundaria" onClick={aoVoltar}>
        Voltar
      </Botao>
    </section>
  );
}
