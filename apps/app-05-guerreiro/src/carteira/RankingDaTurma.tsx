import { useSessao } from "comum/autenticacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import {
  listarPoderesPublicos,
  listarRankingDaTurma,
  type PoderPublico,
  type RankingDaTurma as RankingDaTurmaResposta,
} from "../api/carteira";
import { listarMinhasSeries } from "../api/coleta";

type Recorte =
  | { tipo: "geral" }
  | { tipo: "trilha"; id: string }
  | { tipo: "poder"; id: string };

function ehRecusaDeSessao(erro: unknown): boolean {
  return (
    !!erro &&
    typeof erro === "object" &&
    "codigo" in erro &&
    (erro.codigo === "sessao_ausente" || erro.codigo === "sessao_invalida")
  );
}

// O ranking logado da turma: alcança a comunidade inteira, inclusive quem
// não autorizou divulgação, e traz sempre a própria posição — a exceção
// declarada porque a tela é logada (`RF-05-52`, `RF-05-53`, `RF-05-84`,
// `RN-05-16`, `RN-05-21`). A comunidade do Guerreiro(a) não vem de nenhuma
// leitura própria: é derivada das suas séries de coleta abertas, o mesmo
// caminho que a tela da coleta já usa.
export function RankingDaTurma() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [comunidadeId, definirComunidadeId] = useState<string | null | undefined>(undefined);
  const [poderes, definirPoderes] = useState<PoderPublico[]>([]);
  const [recorte, definirRecorte] = useState<Recorte>({ tipo: "geral" });
  const [ranking, definirRanking] = useState<RankingDaTurmaResposta | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    const token = sessao.token;
    let cancelado = false;

    async function resolverComunidade() {
      try {
        const [pagina, poderesPublicos] = await Promise.all([
          listarMinhasSeries(token),
          listarPoderesPublicos(),
        ]);
        if (cancelado) return;
        definirComunidadeId(pagina.itens[0]?.comunidade_virtual_id ?? null);
        definirPoderes(poderesPublicos);
      } catch (erroCapturado) {
        if (cancelado) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirComunidadeId(null);
      }
    }

    resolverComunidade();
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    if (!sessao || !comunidadeId) return;
    const token = sessao.token;
    const comunidade = comunidadeId;
    let cancelado = false;

    async function carregarRanking() {
      definirErro(null);
      try {
        const resultado = await listarRankingDaTurma(comunidade, token, {
          trilhaId: recorte.tipo === "trilha" ? recorte.id : undefined,
          poderId: recorte.tipo === "poder" ? recorte.id : undefined,
        });
        if (cancelado) return;
        definirRanking(resultado);
      } catch (erroCapturado) {
        if (cancelado) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirErro("Não foi possível carregar o ranking agora. Tente de novo em instantes.");
      }
    }

    carregarRanking();
    return () => {
      cancelado = true;
    };
  }, [sessao, comunidadeId, recorte, tratarRecusaDeSessao]);

  if (comunidadeId === undefined) {
    return <EstadoDaLista>Carregando o ranking…</EstadoDaLista>;
  }

  if (comunidadeId === null) {
    return (
      <EstadoDaLista>
        Abra uma série de coleta na sua trilha para ver o ranking da sua turma.
      </EstadoDaLista>
    );
  }

  return (
    <section className="cg-ranking-da-turma" aria-label="Ranking da turma">
      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      <label className="cg-ranking-da-turma__recorte">
        Recorte
        <select
          value={recorte.tipo === "geral" ? "geral" : `${recorte.tipo}:${recorte.id}`}
          onChange={(evento) => {
            const valor = evento.target.value;
            if (valor === "geral") {
              definirRecorte({ tipo: "geral" });
              return;
            }
            const [tipo, id] = valor.split(":");
            definirRecorte(tipo === "trilha" ? { tipo: "trilha", id } : { tipo: "poder", id });
          }}
        >
          <option value="geral">Toda a comunidade</option>
          {poderes.map((poder) => (
            <optgroup key={poder.id} label={poder.nome}>
              <option value={`poder:${poder.id}`}>{poder.nome} (poder inteiro)</option>
              {poder.trilhas.map((trilha) => (
                <option key={trilha.id} value={`trilha:${trilha.id}`}>
                  {trilha.nome}
                </option>
              ))}
            </optgroup>
          ))}
        </select>
      </label>

      {ranking === null && !erro && <EstadoDaLista>Carregando o ranking…</EstadoDaLista>}

      {ranking !== null && (
        <>
          <p className="cg-ranking-da-turma__minha-posicao">
            Sua posição: <strong>{ranking.minha_posicao.posicao}º</strong> com{" "}
            {ranking.minha_posicao.pontos_regulares} pontos
          </p>
          <ol className="cg-lista-do-ranking">
            {ranking.itens.map((item) => (
              <li key={item.posicao} className="cg-cartao-do-ranking">
                {item.posicao}º — {item.nick} — {item.pontos_regulares} pontos
              </li>
            ))}
          </ol>
        </>
      )}
    </section>
  );
}
