import { useSessao } from "comum/autenticacao";
import { Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import { consultarMeuSustento, FAMILIAS_DE_SELO, type SustentoDoApoiador } from "./api";

const ROTULO_DA_FAMILIA: Record<string, string> = {
  frente: "De frente",
  modalidade: "De modalidade",
  ato: "De ato",
  multiplicacao: "De multiplicação",
};

function formatarData(iso: string): string {
  const data = new Date(iso);
  return Number.isNaN(data.getTime())
    ? iso
    : data.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric" });
}

// O nível de sustento alcançado, os selos conquistados agrupados por
// família e a frente que falta para o próximo nível — uma vez, sem
// insistir e sem repetição em outras telas (`RF-14-67` a `RF-14-70`,
// `RN-14-36`, `RN-14-38`).
export function TelaDeSustento() {
  const { sessao } = useSessao();
  const [sustento, definirSustento] = useState<SustentoDoApoiador | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    consultarMeuSustento(sessao.token)
      .then(definirSustento)
      .catch(() => definirErro("Não foi possível carregar o sustento. Tente novamente."));
  }, [sessao]);

  const totalDeSelos = sustento
    ? FAMILIAS_DE_SELO.reduce((total, familia) => total + sustento.selos[familia].length, 0)
    : 0;

  return (
    <Moldura>
      <Cabecalho titulo="Sustento" />
      {erro && <p role="alert">{erro}</p>}
      {sustento === null && !erro && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {sustento !== null && (
        <>
          <p>
            Nível {sustento.nivel} — {sustento.nome_do_nivel}
          </p>
          <p>Próxima frente: {sustento.frente_que_falta}</p>

          {totalDeSelos === 0 && <EstadoDaLista>Nenhum selo conquistado ainda.</EstadoDaLista>}
          {FAMILIAS_DE_SELO.filter((familia) => sustento.selos[familia].length > 0).map(
            (familia) => (
              <section key={familia} aria-label={ROTULO_DA_FAMILIA[familia]}>
                <h2>{ROTULO_DA_FAMILIA[familia]}</h2>
                <ul>
                  {sustento.selos[familia].map((selo) => (
                    <li key={`${selo.missao_do_apoiador_id}-${selo.selo_nome}`}>
                      {selo.selo_nome} — {formatarData(selo.creditado_em)}
                    </li>
                  ))}
                </ul>
              </section>
            ),
          )}
        </>
      )}
    </Moldura>
  );
}
