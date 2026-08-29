import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useMemo, useState } from "react";
import { AbsorcaoDaNecessidade } from "./AbsorcaoDaNecessidade";
import {
  type AbsorcaoDoMestre,
  listarMeusPontosDeApoio,
  listarMinhasAbsorcoes,
  listarMinhasNecessidades,
  listarTiposDeRecurso,
  type NecessidadeDeRecurso,
  type PontoDeApoioDaLista,
  type TipoDeRecurso,
} from "./api";
import { ListaDeNecessidades } from "./ListaDeNecessidades";
import { MinhasAbsorcoes } from "./MinhasAbsorcoes";

// Reúne a leitura das necessidades, o ato de absorção e o acompanhamento do
// ressarcimento — a área de recursos da App 09 (`RF-09-56` a `RF-09-60`).
// Relê as duas listas depois de cada absorção confirmada, para nunca
// divergir da falta derivada (design — decisão 8).
export function TelaDeRecursos() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();

  const [necessidades, definirNecessidades] = useState<NecessidadeDeRecurso[] | null>(null);
  const [absorcoes, definirAbsorcoes] = useState<AbsorcaoDoMestre[] | null>(null);
  const [tipos, definirTipos] = useState<TipoDeRecurso[]>([]);
  const [pontosDeApoio, definirPontosDeApoio] = useState<PontoDeApoioDaLista[]>([]);
  const [erro, definirErro] = useState<string | null>(null);
  const [necessidadeEmAbsorcao, definirNecessidadeEmAbsorcao] =
    useState<NecessidadeDeRecurso | null>(null);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const [novasNecessidades, novasAbsorcoes, novosTipos, novosPontosDeApoio] =
        await Promise.all([
          listarMinhasNecessidades(sessao.token),
          listarMinhasAbsorcoes(sessao.token),
          listarTiposDeRecurso(sessao.token),
          listarMeusPontosDeApoio(sessao.token),
        ]);
      definirNecessidades(novasNecessidades);
      definirAbsorcoes(novasAbsorcoes);
      definirTipos(novosTipos);
      definirPontosDeApoio(novosPontosDeApoio);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar os recursos. Tente novamente em instantes.");
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  const nomeDoTipoDeRecurso = useMemo(() => {
    const porId = new Map(tipos.map((tipo) => [tipo.id, tipo.nome]));
    return (id: string) => porId.get(id) ?? id;
  }, [tipos]);

  const nomeDoPontoDeApoio = useMemo(() => {
    const porId = new Map(pontosDeApoio.map((ponto) => [ponto.id, ponto.nome]));
    return (id: string) => porId.get(id) ?? id;
  }, [pontosDeApoio]);

  const tipoDaNecessidadeEmAbsorcao = necessidadeEmAbsorcao
    ? (tipos.find((tipo) => tipo.id === necessidadeEmAbsorcao.tipo_de_recurso_id) ?? null)
    : null;

  return (
    <Moldura>
      <Cabecalho titulo="Recursos" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {necessidadeEmAbsorcao ? (
        <AbsorcaoDaNecessidade
          necessidade={necessidadeEmAbsorcao}
          tipo={tipoDaNecessidadeEmAbsorcao}
          nomeDoTipoDeRecurso={nomeDoTipoDeRecurso(necessidadeEmAbsorcao.tipo_de_recurso_id)}
          nomeDoPontoDeApoio={nomeDoPontoDeApoio(necessidadeEmAbsorcao.ponto_de_apoio_id)}
          onConcluida={() => {
            definirNecessidadeEmAbsorcao(null);
            carregar();
          }}
          onCancelar={() => definirNecessidadeEmAbsorcao(null)}
        />
      ) : (
        <>
          <ListaDeNecessidades
            necessidades={necessidades}
            nomeDoTipoDeRecurso={nomeDoTipoDeRecurso}
            nomeDoPontoDeApoio={nomeDoPontoDeApoio}
            aoAbsorver={definirNecessidadeEmAbsorcao}
          />
          <MinhasAbsorcoes
            absorcoes={absorcoes}
            nomeDoTipoDeRecurso={nomeDoTipoDeRecurso}
            nomeDoPontoDeApoio={nomeDoPontoDeApoio}
          />
        </>
      )}
    </Moldura>
  );
}
