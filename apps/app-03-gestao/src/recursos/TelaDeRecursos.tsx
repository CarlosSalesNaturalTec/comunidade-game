import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useMemo, useState } from "react";
import { type AulaDaAgenda, listarAgenda } from "../agenda/api";
import { type ComunidadeDaLista, listarComunidades } from "../comunidades/api";
import { listarMissoes, type MissaoDoApoiador } from "../missoes-do-apoiador/api";
import { ListaDeMissoes } from "../missoes-do-apoiador/ListaDeMissoes";
import { PublicacaoDeMissao } from "../missoes-do-apoiador/PublicacaoDeMissao";
import {
  listarPontosDeApoio,
  listarSaldosDoPontoDeApoio,
  type PontoDeApoioDaLista,
} from "../pontos-de-apoio/api";
import {
  type AporteRegistrado,
  listarNecessidades,
  listarTiposDeRecurso,
  type NecessidadeDeRecurso,
  type TipoDeRecurso,
} from "./api";
import { ListaDeNecessidades } from "./ListaDeNecessidades";
import {
  ListaDeSaldosDisponiveis,
  type SaldoDoPontoDeApoio,
} from "./ListaDeSaldosDisponiveis";
import { RegistroDeAporte } from "./RegistroDeAporte";

const RECUSA_POR_PAPEL = "Só o Admin acessa a área Recursos.";

// Reúne o registro do aporte e a lista das necessidades em aberto, restrita
// ao Admin (`RF-02-57`, `RF-02-58`, PRD-02 §4).
export function TelaDeRecursos() {
  const { sessao } = useSessao();
  const podeAcessar = sessao?.papel === "admin";

  const [necessidades, definirNecessidades] = useState<NecessidadeDeRecurso[] | null>(null);
  const [tipos, definirTipos] = useState<TipoDeRecurso[]>([]);
  const [comunidades, definirComunidades] = useState<ComunidadeDaLista[]>([]);
  const [pontosDeApoio, definirPontosDeApoio] = useState<PontoDeApoioDaLista[]>([]);
  const [gruposDeSaldo, definirGruposDeSaldo] = useState<SaldoDoPontoDeApoio[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [ultimoAporte, definirUltimoAporte] = useState<AporteRegistrado | null>(null);
  const [aulasConfirmadas, definirAulasConfirmadas] = useState<AulaDaAgenda[]>([]);
  const [missoes, definirMissoes] = useState<MissaoDoApoiador[] | null>(null);
  const [mostrarFormularioDeAporte, definirMostrarFormularioDeAporte] = useState(false);
  const [mostrarFormularioDeMissao, definirMostrarFormularioDeMissao] = useState(false);

  const carregarNecessidades = useCallback(async () => {
    try {
      return await listarNecessidades();
    } catch {
      definirErro("Não foi possível carregar as necessidades. Tente novamente em instantes.");
      return null;
    }
  }, []);

  useEffect(() => {
    if (!podeAcessar || !sessao) return;
    carregarNecessidades().then((itens) => {
      if (itens) definirNecessidades(itens);
    });
    listarTiposDeRecurso(sessao.token).then(definirTipos);
    listarComunidades().then((pagina) => definirComunidades(pagina.itens));
    listarMissoes(sessao.token).then(definirMissoes);
  }, [podeAcessar, sessao, carregarNecessidades]);

  // Os pontos de apoio de todas as comunidades, para rotular a necessidade
  // sem exigir escolha prévia de comunidade (`RF-02-58`).
  useEffect(() => {
    if (!podeAcessar || !sessao || comunidades.length === 0) return;
    Promise.all(
      comunidades.map((comunidade) => listarPontosDeApoio(sessao.token, comunidade.id)),
    ).then((paginas) => definirPontosDeApoio(paginas.flatMap((pagina) => pagina.itens)));
  }, [podeAcessar, sessao, comunidades]);

  // O saldo disponível é apurado por ponto de apoio, no mesmo molde já usado
  // em Pontos de Apoio — a tela nunca soma entre pontos (`RF-02-45`,
  // `RF-02-97`).
  useEffect(() => {
    if (!podeAcessar || !sessao || pontosDeApoio.length === 0) return;
    Promise.all(
      pontosDeApoio.map(async (pontoDeApoio) => ({
        pontoDeApoio,
        saldos: await listarSaldosDoPontoDeApoio(pontoDeApoio.id, sessao.token),
      })),
    ).then(definirGruposDeSaldo);
  }, [podeAcessar, sessao, pontosDeApoio]);

  const aoRegistrar = useCallback(
    async (aporte: AporteRegistrado) => {
      definirUltimoAporte(aporte);
      definirAulasConfirmadas([]);
      definirMostrarFormularioDeAporte(false);
      const antes = necessidades ?? [];
      // Releitura, nunca estado local: a aula que a falta fechava é
      // derivada relendo o núcleo, não marcada como confirmada por conta
      // própria (`RF-02-67`, design — decisão 6).
      const depois = await carregarNecessidades();
      if (!depois || !sessao) return;
      definirNecessidades(depois);

      const idsDepois = new Set(depois.map((item) => item.aula_id));
      const resolvidas = antes.filter((item) => !idsDepois.has(item.aula_id));
      if (resolvidas.length === 0) return;

      const porComunidade = new Map(
        resolvidas.map((item) => [item.comunidade_virtual_id, item]),
      );
      const paginas = await Promise.all(
        [...porComunidade.keys()].map((comunidadeId) =>
          listarAgenda(sessao.token, { comunidadeId }).catch(() => ({
            itens: [] as AulaDaAgenda[],
            proximo_cursor: null,
          })),
        ),
      );
      const idsResolvidos = new Set(resolvidas.map((item) => item.aula_id));
      const aulas = paginas
        .flatMap((pagina) => pagina.itens)
        .filter((aula) => idsResolvidos.has(aula.id));
      definirAulasConfirmadas(aulas);
    },
    [carregarNecessidades, necessidades, sessao],
  );

  const nomeDoTipoDeRecurso = useMemo(() => {
    const porId = new Map(tipos.map((tipo) => [tipo.id, tipo.nome]));
    return (id: string) => porId.get(id) ?? id;
  }, [tipos]);

  const nomeDaComunidade = useMemo(() => {
    const porId = new Map(comunidades.map((comunidade) => [comunidade.id, comunidade.nome]));
    return (id: string) => porId.get(id) ?? id;
  }, [comunidades]);

  const nomeDoPontoDeApoio = useMemo(() => {
    const porId = new Map(pontosDeApoio.map((ponto) => [ponto.id, ponto.nome]));
    return (id: string) => porId.get(id) ?? id;
  }, [pontosDeApoio]);

  if (!podeAcessar) {
    return (
      <Moldura>
        <Cabecalho titulo="Recursos" />
        <Aviso tipo="erro">{RECUSA_POR_PAPEL}</Aviso>
      </Moldura>
    );
  }

  return (
    <Moldura>
      <Cabecalho titulo="Recursos" />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {ultimoAporte && (
        <Aviso tipo="sucesso">
          Aporte registrado — {ultimoAporte.valor_em_moedas} moedas.
        </Aviso>
      )}

      {aulasConfirmadas.length > 0 && (
        <ul aria-label="Aulas confirmadas pelo aporte">
          {aulasConfirmadas.map((aula) => (
            <li key={aula.id}>
              Aula confirmada, com a reserva efetivada —{" "}
              {nomeDaComunidade(aula.comunidade_virtual_id)},{" "}
              {nomeDoPontoDeApoio(aula.ponto_de_apoio_id)}.
            </li>
          ))}
        </ul>
      )}

      {!mostrarFormularioDeAporte && (
        <Botao onClick={() => definirMostrarFormularioDeAporte(true)}>Novo aporte</Botao>
      )}
      {mostrarFormularioDeAporte && <RegistroDeAporte onRegistrado={aoRegistrar} />}

      <ListaDeNecessidades
        necessidades={necessidades}
        nomeDoTipoDeRecurso={nomeDoTipoDeRecurso}
        nomeDaComunidade={nomeDaComunidade}
        nomeDoPontoDeApoio={nomeDoPontoDeApoio}
      />

      <ListaDeSaldosDisponiveis gruposDeSaldo={gruposDeSaldo} />

      <h2>Missões do Apoiador</h2>
      {!mostrarFormularioDeMissao && (
        <Botao onClick={() => definirMostrarFormularioDeMissao(true)}>Nova missão</Botao>
      )}
      {mostrarFormularioDeMissao && (
        <PublicacaoDeMissao
          necessidades={necessidades ?? []}
          nomeDoTipoDeRecurso={nomeDoTipoDeRecurso}
          onPublicada={(missao) => {
            definirMissoes((atual) => [missao, ...(atual ?? [])]);
            definirMostrarFormularioDeMissao(false);
          }}
        />
      )}
      {sessao && (
        <ListaDeMissoes
          missoes={missoes}
          token={sessao.token}
          aoDespublicada={(atualizada) =>
            definirMissoes((atual) =>
              (atual ?? []).map((item) => (item.id === atualizada.id ? atualizada : item)),
            )
          }
        />
      )}
    </Moldura>
  );
}
