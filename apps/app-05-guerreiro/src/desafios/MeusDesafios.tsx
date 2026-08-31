import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { useEffect, useState } from "react";
import { type Desafio, listarMeusDesafios } from "../api/desafiosEEquipes";

const ROTULO_DA_MODALIDADE: Record<string, string> = {
  individual: "Sozinho(a)",
  em_equipe: "Em equipe",
  em_equipe_com_familiar: "Em equipe com a família",
};

const ROTULO_DO_FORMATO: Record<string, string> = {
  presencial: "Presencial",
  on_line_assincrona: "On-line",
};

// Os desafios em aberto do Guerreiro(a) — modalidade, formato e o que ele
// precisa produzir, em linguagem da criança. Leitura apenas: nenhuma ação
// de lançar resultado, presença ou mérito aparece aqui (`RF-05-19`,
// `RN-05-06`).
export function MeusDesafios() {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [desafios, definirDesafios] = useState<Desafio[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  useEffect(() => {
    if (!sessao) return;
    const token = sessao.token;
    let cancelado = false;

    async function carregar() {
      definirErro(null);
      try {
        const resultado = await listarMeusDesafios(token);
        if (cancelado) return;
        definirDesafios(resultado);
      } catch (erroCapturado) {
        if (cancelado) return;
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirErro(
          "Não foi possível carregar os seus desafios agora. Tente de novo em instantes.",
        );
      }
    }

    carregar();
    return () => {
      cancelado = true;
    };
  }, [sessao, tratarRecusaDeSessao]);

  return (
    <section className="cg-meus-desafios" aria-label="Meus desafios">
      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {desafios === null && !erro && (
        <EstadoDaLista>Carregando os seus desafios…</EstadoDaLista>
      )}
      {desafios !== null && desafios.length === 0 && (
        <EstadoDaLista>
          Você não tem nenhum desafio em aberto agora. Continue na sua trilha!
        </EstadoDaLista>
      )}
      {desafios !== null && desafios.length > 0 && (
        <ul className="cg-lista-de-desafios">
          {desafios.map((desafio) => (
            <li key={desafio.atividade.id} className="cg-cartao-de-desafio">
              <h3>{desafio.atividade.titulo}</h3>
              <p className="cg-cartao-de-desafio__origem">
                {desafio.trilha_titulo} — {desafio.missao_titulo}
              </p>
              <p>
                <strong>Como fazer:</strong>{" "}
                {ROTULO_DA_MODALIDADE[desafio.atividade.modalidade] ??
                  desafio.atividade.modalidade}
                {", "}
                {ROTULO_DO_FORMATO[desafio.atividade.formato] ?? desafio.atividade.formato}
              </p>
              <p>
                <strong>O que produzir:</strong> {desafio.atividade.producao_esperada}
              </p>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
