import { useSessao } from "comum/autenticacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import { listarMinhasRetomadas, type RetomadaEmAberto } from "../api/trilha";

function formatarData(valorIso: string): string {
  return new Date(valorIso).toLocaleDateString("pt-BR");
}

// As retomadas em aberto — missão, trilha e prazo de cada uma, com a
// explicação de que rever fixa o aprendizado; entregue a produção, a
// retomada some da lista, e refazer por conta própria segue possível pela
// tela da missão, sem render ponto novo (`RF-05-79`, `RF-05-80`,
// `RN-05-38`). Nunca palavra de atraso, dívida ou punição.
export function Retomadas() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [retomadas, definirRetomadas] = useState<RetomadaEmAberto[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    let cancelado = false;
    listarMinhasRetomadas(sessao.token)
      .then((resultado) => {
        if (!cancelado) definirRetomadas(resultado);
      })
      .catch((erroCapturado) => {
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
          "Não foi possível carregar as suas retomadas agora. Tente de novo em instantes.",
        );
      });
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  if (erro) return <Aviso tipo="erro">{erro}</Aviso>;
  if (retomadas === null) return <EstadoDaLista>Carregando as suas retomadas…</EstadoDaLista>;

  return (
    <section aria-label="Retomadas">
      <h2>Retomadas</h2>
      <Aviso tipo="andamento">
        Rever o que você já fez ajuda a fixar o que aprendeu — por isso essas missões voltam de
        vez em quando.
      </Aviso>

      {retomadas.length === 0 ? (
        <EstadoDaLista>Você não tem nenhuma retomada agora.</EstadoDaLista>
      ) : (
        <ul className="cg-trilha__retomadas">
          {retomadas.map((retomada) => (
            <li
              key={`${retomada.missao_id}-${retomada.prazo}`}
              className="cg-trilha__retomadas-item"
            >
              <h3>{retomada.missao_titulo}</h3>
              <p>Trilha: {retomada.trilha_titulo}</p>
              <p>Prazo: {formatarData(retomada.prazo)}</p>
            </li>
          ))}
        </ul>
      )}

      <p className="cg-trilha__retomadas-aviso">
        Você também pode refazer qualquer missão já feita pela tela dela quando quiser — só que
        isso não rende ponto novo.
      </p>
    </section>
  );
}
