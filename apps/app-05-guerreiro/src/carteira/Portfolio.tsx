import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import { type ItemDoPortfolio, obterPortfolio } from "../api/criacaoOriginal";

function formatarData(valorIso: string): string {
  return new Date(valorIso).toLocaleDateString("pt-BR");
}

// O portfólio das criações originais validadas, com a situação de
// exposição pública — a autorização de divulgação é ato do responsável na
// App 07, nunca oferecido aqui (`RF-05-43`, `RF-05-44`, `RN-05-14`).
export function Portfolio() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [itens, definirItens] = useState<ItemDoPortfolio[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    let cancelado = false;
    obterPortfolio(sessao.token)
      .then((resultado) => {
        if (!cancelado) definirItens(resultado);
      })
      .catch((erroCapturado) => {
        if (cancelado) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirErro(
          "Não foi possível carregar o portfólio agora. Tente de novo em instantes.",
        );
      });
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  return (
    <section className="cg-portfolio" aria-label="Meu portfólio">
      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {itens === null && !erro && <EstadoDaLista>Carregando o seu portfólio…</EstadoDaLista>}
      {itens !== null && itens.length === 0 && (
        <EstadoDaLista>
          Você ainda não tem nenhuma criação original validada. Continue na sua trilha!
        </EstadoDaLista>
      )}
      {itens !== null && itens.length > 0 && (
        <ul className="cg-lista-do-portfolio">
          {itens.map((item) => (
            <li key={item.id} className="cg-cartao-do-portfolio">
              <p>{item.producao ?? "Produção em mídia"}</p>
              <p>
                Autoria: {item.autores.map((autor) => autor.nick).join(", ")}
                {item.validado_em && ` — validada em ${formatarData(item.validado_em)}`}
              </p>
              {item.publica ? (
                <Aviso tipo="sucesso">Pública na vitrine.</Aviso>
              ) : (
                <Aviso tipo="andamento">
                  Ainda depende da autorização de divulgação do responsável, dada na App 07.
                </Aviso>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
