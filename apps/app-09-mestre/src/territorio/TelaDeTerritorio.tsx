import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  listarMinhasTrilhas,
  listarTiposDeColeta,
  type TipoDeColeta,
  type TrilhaDoMestre,
} from "../trilhas/api";
import { AvaliacaoDeSolicitacao } from "./AvaliacaoDeSolicitacao";
import {
  type ComunidadeDaLista,
  type LocalDaLista,
  listarSolicitacoesAbertasDeTodasAsComunidades,
  listarTodosOsLocais,
  type NivelDoLocal,
  type SolicitacaoDeLocalDaLista,
} from "./api";

export const ROTULO_DO_NIVEL: Record<NivelDoLocal, string> = {
  comunidade: "Comunidade",
  bairro: "Bairro",
  rua: "Rua",
  condominio: "Condomínio",
  bloco: "Bloco",
  quadra: "Quadra",
};

interface GrupoPorComunidade {
  comunidade: ComunidadeDaLista;
  solicitacoes: SolicitacaoDeLocalDaLista[];
}

interface DesafioResumo {
  tipoNome: string;
  missaoTitulo: string;
}

interface Props {
  // Chamado a cada recarga, com o total de solicitações em aberto — o
  // alerta da navegação usa este mesmo total, para nunca divergir do que a
  // área de território mostra (`RF-09-54`).
  onContagemAtualizada?: (total: number) => void;
}

// Sem seletor de comunidade: a trilha do Mestre atravessa todas — a lista
// sai agrupada por comunidade, das mesmas consultas que alimentam o alerta
// da navegação (`RF-09-53`, `RN-01-42`, design — decisões 4 e 5). Nenhuma
// ação de cadastrar local ou criar Comunidade Virtual: as duas seguem
// privativas de Admin (PRD-09 §3.2).
export function TelaDeTerritorio({ onContagemAtualizada }: Props = {}) {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const [grupos, definirGrupos] = useState<GrupoPorComunidade[] | null>(null);
  const [locaisPorComunidade, definirLocaisPorComunidade] = useState<
    Map<string, LocalDaLista[]>
  >(new Map());
  const [trilhas, definirTrilhas] = useState<TrilhaDoMestre[]>([]);
  const [tiposDeColeta, definirTiposDeColeta] = useState<TipoDeColeta[]>([]);
  const [erro, definirErro] = useState<string | null>(null);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const [novosGrupos, minhasTrilhas, tipos] = await Promise.all([
        listarSolicitacoesAbertasDeTodasAsComunidades(sessao.token),
        listarMinhasTrilhas(sessao.token),
        listarTiposDeColeta(sessao.token),
      ]);
      definirGrupos(novosGrupos);
      definirTrilhas(minhasTrilhas);
      definirTiposDeColeta(tipos);
      onContagemAtualizada?.(
        novosGrupos.reduce((total, grupo) => total + grupo.solicitacoes.length, 0),
      );
      const paresDeLocais = await Promise.all(
        novosGrupos.map(
          async (grupo) =>
            [grupo.comunidade.id, await listarTodosOsLocais(grupo.comunidade.id)] as const,
        ),
      );
      definirLocaisPorComunidade(new Map(paresDeLocais));
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar o território. Tente novamente em instantes.");
    }
  }, [sessao, tratarRecusaDeSessao, onContagemAtualizada]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  // O desafio de origem, resolvido pelas próprias trilhas do Mestre — a
  // mesma leitura que a autoria já usa, sem rota nova.
  const desafioPorId = useMemo(() => {
    const tipoPorId = new Map(tiposDeColeta.map((tipo) => [tipo.id, tipo]));
    const mapa = new Map<string, DesafioResumo>();
    for (const trilha of trilhas) {
      for (const missao of trilha.missoes) {
        for (const desafio of missao.desafios_de_coleta ?? []) {
          const tipo = tipoPorId.get(desafio.tipo_de_coleta_id);
          mapa.set(desafio.id, {
            tipoNome: tipo?.nome ?? "Desafio de coleta",
            missaoTitulo: missao.titulo,
          });
        }
      }
    }
    return mapa;
  }, [trilhas, tiposDeColeta]);

  const totalDeSolicitacoes = (grupos ?? []).reduce(
    (total, grupo) => total + grupo.solicitacoes.length,
    0,
  );

  return (
    <Moldura>
      <Cabecalho
        titulo="Território"
        subtitulo="Solicitações de novo local dos desafios das suas trilhas"
        acao={{ rotulo: "Sair", aoAcionar: sair }}
      />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {grupos === null && (
        <EstadoDaLista>Carregando as solicitações de novo local…</EstadoDaLista>
      )}

      {grupos !== null && totalDeSolicitacoes === 0 && (
        <EstadoDaLista>Nenhuma solicitação de novo local em aberto.</EstadoDaLista>
      )}

      {grupos?.map((grupo) => (
        <section
          key={grupo.comunidade.id}
          aria-label={`Solicitações de ${grupo.comunidade.nome}`}
        >
          <h2>{grupo.comunidade.nome}</h2>
          <ul>
            {grupo.solicitacoes.map((solicitacao) => {
              const desafio = desafioPorId.get(solicitacao.desafio_de_coleta_id);
              return (
                <li key={solicitacao.id}>
                  <div>
                    <span>{ROTULO_DO_NIVEL[solicitacao.nivel_pretendido]}</span> ·{" "}
                    <span>{solicitacao.rotulo}</span>
                    {desafio && (
                      <>
                        {" "}
                        · {desafio.tipoNome} ({desafio.missaoTitulo})
                      </>
                    )}
                  </div>
                  <p>{solicitacao.justificativa}</p>
                  <AvaliacaoDeSolicitacao
                    solicitacao={solicitacao}
                    locais={locaisPorComunidade.get(grupo.comunidade.id) ?? []}
                    onConcluida={carregar}
                  />
                </li>
              );
            })}
          </ul>
        </section>
      ))}
    </Moldura>
  );
}
