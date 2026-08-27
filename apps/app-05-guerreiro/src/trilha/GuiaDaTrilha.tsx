import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { useCallback, useEffect, useState } from "react";
import {
  type MissaoNoPercurso,
  obterMissaoNoPercurso,
  type TrilhaComProximaMissao,
} from "../api/trilha";
import { Culminancia } from "./Culminancia";
import { Missao } from "./Missao";

interface Props {
  trilha: TrilhaComProximaMissao;
  aoAtualizarTrilhas: () => void;
  aoTrocarDeTrilha: () => void;
}

// Abre direto na próxima missão do Guerreiro(a), sem que ele precise
// procurar em menu, e mostra qual é a missão seguinte, ainda trancada, com
// o motivo (`RF-05-08`, `RF-05-10`). Alternar de trilha preserva o
// contexto de cada uma, porque a posição vem sempre do núcleo, nunca de
// estado local perdido ao trocar (`RF-05-17`).
export function GuiaDaTrilha({ trilha, aoAtualizarTrilhas, aoTrocarDeTrilha }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [missaoAtual, definirMissaoAtual] = useState<MissaoNoPercurso | null>(null);
  const [missaoSeguinte, definirMissaoSeguinte] = useState<MissaoNoPercurso | null>(null);
  const [erro, definirErro] = useState<string | null>(null);

  const tratarErro = useCallback(
    (erroCapturado: unknown) => {
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
      if (
        erroCapturado &&
        typeof erroCapturado === "object" &&
        "codigo" in erroCapturado &&
        erroCapturado.codigo === "nao_encontrado"
      ) {
        return;
      }
      definirErro("Não foi possível carregar a missão agora. Tente de novo em instantes.");
    },
    [tratarRecusaDeSessao],
  );

  const carregar = useCallback(() => {
    if (!sessao || trilha.proxima_missao_posicao === null) return;
    definirErro(null);
    obterMissaoNoPercurso(trilha.id, trilha.proxima_missao_posicao, sessao.token)
      .then(definirMissaoAtual)
      .catch(tratarErro);
    obterMissaoNoPercurso(trilha.id, trilha.proxima_missao_posicao + 1, sessao.token)
      .then(definirMissaoSeguinte)
      .catch(() => definirMissaoSeguinte(null));
  }, [sessao, trilha, tratarErro]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  function aoDesbloquear() {
    aoAtualizarTrilhas();
  }

  if (trilha.proxima_missao_posicao === null) {
    return (
      <section aria-label={`Guia de ${trilha.nome}`} className="cg-trilha__guia">
        <Aviso tipo="sucesso">
          Você já desbloqueou todas as missões desta trilha. Agora é hora da culminância!
        </Aviso>
        <Culminancia trilhaId={trilha.id} />
      </section>
    );
  }

  return (
    <section aria-label={`Guia de ${trilha.nome}`} className="cg-trilha__guia">
      <header className="cg-trilha__cabecalho-do-guia">
        <h2>{trilha.nome}</h2>
        <Botao variante="secundaria" onClick={aoTrocarDeTrilha}>
          Trocar de trilha
        </Botao>
      </header>

      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {!erro && missaoAtual === null && <EstadoDaLista>Carregando a missão…</EstadoDaLista>}

      {missaoAtual && (
        <Missao trilhaId={trilha.id} missao={missaoAtual} aoDesbloquear={aoDesbloquear} />
      )}

      {missaoSeguinte && !missaoSeguinte.desbloqueada && (
        <Aviso tipo="andamento">
          A seguir: <strong>{missaoSeguinte.titulo}</strong> —{" "}
          {missaoSeguinte.motivo_do_bloqueio}
        </Aviso>
      )}
    </section>
  );
}
