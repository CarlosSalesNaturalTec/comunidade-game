import { useSessao } from "comum/autenticacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import { listarMinhasRecompensas, type RecompensaConquistada } from "../api/carteira";

function formatarData(valorIso: string): string {
  return new Date(valorIso).toLocaleDateString("pt-BR");
}

// As recompensas de marco conquistadas — o Mestre confirma a entrega, e
// nenhuma tela oferece comprá-las com pontos de qualquer natureza
// (`RF-05-45`, `RF-05-46`, `RN-05-07`, `RN-05-41`).
export function Conquistas() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [recompensas, definirRecompensas] = useState<RecompensaConquistada[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    const token = sessao.token;
    let cancelado = false;

    async function carregar() {
      definirErro(null);
      try {
        const resultado = await listarMinhasRecompensas(token);
        if (cancelado) return;
        definirRecompensas(resultado);
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
          "Não foi possível carregar as suas conquistas agora. Tente de novo em instantes.",
        );
      }
    }

    carregar();
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  return (
    <section className="cg-conquistas" aria-label="Minhas conquistas">
      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {recompensas === null && !erro && (
        <EstadoDaLista>Carregando as suas conquistas…</EstadoDaLista>
      )}
      {recompensas !== null && recompensas.length === 0 && (
        <EstadoDaLista>
          Você ainda não conquistou nenhuma recompensa de marco. Continue na sua trilha!
        </EstadoDaLista>
      )}
      {recompensas !== null && recompensas.length > 0 && (
        <ul className="cg-lista-de-conquistas">
          {recompensas.map((recompensa) => (
            <li key={recompensa.recompensa_de_marco_id} className="cg-cartao-de-conquista">
              <p>Quantidade conquistada: {recompensa.quantidade}</p>
              {recompensa.entregue ? (
                <Aviso tipo="sucesso">
                  Entregue em{" "}
                  {recompensa.entregue_em ? formatarData(recompensa.entregue_em) : ""}
                </Aviso>
              ) : (
                <Aviso tipo="andamento">Aguardando o Mestre confirmar a entrega.</Aviso>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
