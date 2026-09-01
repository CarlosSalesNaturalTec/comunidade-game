import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import { listarMeusAportes, type MeusAportesSaida } from "./api";

function formatarData(isoDeData: string): string {
  const data = new Date(isoDeData);
  return Number.isNaN(data.getTime())
    ? isoDeData
    : data.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric" });
}

// Os aportes já homologados — data, tipo e destino — e o Poder Sustentador
// como total acumulado em moedas, exatamente como o núcleo os devolve, sem
// somar nem reordenar (`RF-14-21`, `RF-14-22`, `RN-14-09`).
export function TelaDeMeusAportes() {
  const { sessao } = useSessao();
  const [saida, definirSaida] = useState<MeusAportesSaida | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    listarMeusAportes(sessao.token)
      .then(definirSaida)
      .catch(() => definirErro("Não foi possível carregar seus aportes. Tente novamente."));
  }, [sessao]);

  return (
    <Moldura>
      <Cabecalho titulo="Meus aportes" />
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {saida === null && !erro && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {saida && (
        <p>
          <strong>Poder Sustentador:</strong> {saida.poder_sustentador_em_moedas} moedas
        </p>
      )}
      {saida && saida.aportes.length === 0 && (
        <EstadoDaLista>Ainda não há aporte homologado.</EstadoDaLista>
      )}
      {saida?.aportes.map((aporte) => (
        <article key={aporte.id} className="cg-cartao-de-aporte">
          <p>
            {formatarData(aporte.data_do_aporte)} — {aporte.tipo_de_recurso_nome} —{" "}
            {aporte.ponto_de_apoio_nome}
          </p>
          <p>{aporte.valor_em_moedas} moedas</p>
        </article>
      ))}
    </Moldura>
  );
}
