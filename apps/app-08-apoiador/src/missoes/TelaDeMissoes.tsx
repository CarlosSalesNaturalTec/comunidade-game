import { Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useEffect, useState } from "react";
import {
  listarMissoesAbertas,
  type MissaoDoApoiador,
  type MissoesAgrupadas,
  NIVEIS_DE_NECESSIDADE,
} from "./api";
import { DeclaracaoPorMissao } from "./DeclaracaoPorMissao";

const ROTULO_DO_NIVEL: Record<string, string> = {
  existir: "Existir",
  acontecer: "Acontecer",
  reconhecer: "Reconhecer",
  permanecer: "Permanecer",
};

function formatarPrazo(iso: string): string {
  const data = new Date(iso);
  return Number.isNaN(data.getTime())
    ? iso
    : data.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit", year: "numeric" });
}

// As missões abertas, agrupadas pelo nível de necessidade que sustentam,
// cada uma com o que se pede, o que falta em moedas, o prazo, o selo e o
// coberto em quantidade — sem identificar quem cobriu (`RF-14-60` a
// `RF-14-62`, `RF-14-71`, `RF-14-72`). Escolher uma missão abre a
// declaração do aporte por ela, inteira ou em parte (`RF-14-63`).
export function TelaDeMissoes() {
  const [agrupadas, definirAgrupadas] = useState<MissoesAgrupadas | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [missaoEscolhida, definirMissaoEscolhida] = useState<MissaoDoApoiador | null>(null);

  const carregar = () => {
    listarMissoesAbertas()
      .then(definirAgrupadas)
      .catch(() => definirErro("Não foi possível carregar as missões. Tente novamente."));
  };

  useEffect(carregar, []);

  if (missaoEscolhida) {
    return (
      <DeclaracaoPorMissao
        missao={missaoEscolhida}
        aoVoltar={() => {
          definirMissaoEscolhida(null);
          carregar();
        }}
      />
    );
  }

  const totalDeMissoes = agrupadas
    ? NIVEIS_DE_NECESSIDADE.reduce((total, nivel) => total + agrupadas[nivel].length, 0)
    : 0;

  return (
    <Moldura>
      <Cabecalho
        titulo="Missões"
        subtitulo="Cada missão vem de uma necessidade real, publicada pela gestão."
      />
      {erro && <p role="alert">{erro}</p>}
      {agrupadas === null && !erro && <EstadoDaLista>Carregando…</EstadoDaLista>}
      {agrupadas !== null && totalDeMissoes === 0 && (
        <EstadoDaLista>Não há missão aberta no momento.</EstadoDaLista>
      )}
      {agrupadas !== null &&
        NIVEIS_DE_NECESSIDADE.filter((nivel) => agrupadas[nivel].length > 0).map((nivel) => (
          <section key={nivel} aria-label={ROTULO_DO_NIVEL[nivel]}>
            <h2>{ROTULO_DO_NIVEL[nivel]}</h2>
            {agrupadas[nivel].map((missao) => (
              <article key={missao.id}>
                <h3>{missao.titulo}</h3>
                <p>{missao.o_que_se_pede}</p>
                <p>
                  Falta {missao.falta} moedas — já coberto: {missao.coberto} — prazo{" "}
                  {formatarPrazo(missao.prazo)}
                </p>
                <p>Selo: {missao.selo_nome}</p>
                <Botao variante="secundaria" onClick={() => definirMissaoEscolhida(missao)}>
                  Cobrir esta missão
                </Botao>
              </article>
            ))}
          </section>
        ))}
    </Moldura>
  );
}
