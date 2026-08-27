import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, EstadoDaLista } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import { type CriacaoOriginal, obterMinhaCriacaoDaTrilha } from "../api/criacaoOriginal";
import { obterTrilhaPublica, type TrilhaPublicaComMissoes } from "../api/trilha";
import { EntregaDeCriacao } from "./EntregaDeCriacao";

interface Props {
  trilhaId: string;
}

const ROTULO_DA_MODALIDADE: Record<string, string> = {
  individual: "individual",
  em_equipe: "em equipe",
};

// Concluído o percurso, a culminância mostra o que a criação original
// precisa ser, com o critério de validação e a modalidade escritos pelo
// Mestre autor — sem entrega enquanto ela não for declarada (`RF-05-39`).
export function Culminancia({ trilhaId }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [trilhaPublica, definirTrilhaPublica] = useState<TrilhaPublicaComMissoes | null>(null);
  const [criacao, definirCriacao] = useState<CriacaoOriginal | null>(null);
  const [carregando, definirCarregando] = useState(true);
  const [erro, definirErro] = useState<string | null>(null);

  const carregar = useCallback(() => {
    if (!sessao) return;
    definirErro(null);
    definirCarregando(true);
    Promise.all([
      obterTrilhaPublica(trilhaId),
      obterMinhaCriacaoDaTrilha(trilhaId, sessao.token),
    ])
      .then(([trilha, minhaCriacao]) => {
        definirTrilhaPublica(trilha);
        definirCriacao(minhaCriacao);
      })
      .catch((erroCapturado) => {
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirErro(
          "Não foi possível carregar a culminância agora. Tente de novo em instantes.",
        );
      })
      .finally(() => definirCarregando(false));
  }, [sessao, trilhaId, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  if (erro) return <Aviso tipo="erro">{erro}</Aviso>;
  if (carregando || trilhaPublica === null) {
    return <EstadoDaLista>Carregando a culminância…</EstadoDaLista>;
  }

  const { culminancia } = trilhaPublica;

  if (culminancia === null) {
    return (
      <Aviso tipo="atencao">
        O Mestre ainda não declarou o que a criação original desta trilha precisa ser.
      </Aviso>
    );
  }

  return (
    <section aria-label="Culminância da trilha" className="cg-culminancia">
      <h2>Culminância</h2>
      <p>{culminancia.descricao}</p>
      <p>
        <strong>Critério de validação:</strong> {culminancia.criterio_de_validacao}
      </p>
      <p>
        <strong>Modalidade:</strong> {ROTULO_DA_MODALIDADE[culminancia.modalidade]}
      </p>

      {criacao?.situacao === "validada" && (
        <Aviso tipo="sucesso">Sua criação foi validada! Confira no seu portfólio.</Aviso>
      )}

      {criacao?.situacao === "entregue" && (
        <Aviso tipo="andamento">
          Você já entregou a criação. Agora é só esperar o Mestre autor validar.
        </Aviso>
      )}

      {(criacao === null || criacao.situacao === "devolvida") && (
        <EntregaDeCriacao
          trilhaId={trilhaId}
          culminancia={culminancia}
          criacaoDevolvida={criacao?.situacao === "devolvida" ? criacao : null}
          aoEntregar={carregar}
        />
      )}
    </section>
  );
}
