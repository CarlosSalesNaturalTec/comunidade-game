import { useSessao } from "comum/autenticacao";
import { Aviso, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useMemo, useState } from "react";
import { type AulaDaAgenda, listarAgenda } from "../agenda/api";
import { type ComunidadeDaLista, listarComunidades } from "../comunidades/api";
import { listarPontosDeApoio, type PontoDeApoioDaLista } from "../pontos-de-apoio/api";
import {
  type AporteRegistrado,
  listarNecessidades,
  listarTiposDeRecurso,
  type NecessidadeDeRecurso,
  type TipoDeRecurso,
} from "./api";
import { ListaDeNecessidades } from "./ListaDeNecessidades";
import { RegistroDeAporte } from "./RegistroDeAporte";

const RECUSA_POR_PAPEL = "Só o Admin acessa a área Recursos.";

// Reúne o registro do aporte e a lista das necessidades em aberto, restrita
// ao Admin (`RF-02-57`, `RF-02-58`, PRD-02 §4).
export function TelaDeRecursos() {
  const { sessao, sair } = useSessao();
  const podeAcessar = sessao?.papel === "admin";

  const [necessidades, definirNecessidades] = useState<NecessidadeDeRecurso[] | null>(null);
  const [tipos, definirTipos] = useState<TipoDeRecurso[]>([]);
  const [comunidades, definirComunidades] = useState<ComunidadeDaLista[]>([]);
  const [pontosDeApoio, definirPontosDeApoio] = useState<PontoDeApoioDaLista[]>([]);
  const [erro, definirErro] = useState<string | null>(null);
  const [ultimoAporte, definirUltimoAporte] = useState<AporteRegistrado | null>(null);
  const [aulasConfirmadas, definirAulasConfirmadas] = useState<AulaDaAgenda[]>([]);

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
  }, [podeAcessar, sessao, carregarNecessidades]);

  // Os pontos de apoio de todas as comunidades, para rotular a necessidade
  // sem exigir escolha prévia de comunidade (`RF-02-58`).
  useEffect(() => {
    if (!podeAcessar || !sessao || comunidades.length === 0) return;
    Promise.all(
      comunidades.map((comunidade) => listarPontosDeApoio(sessao.token, comunidade.id)),
    ).then((paginas) => definirPontosDeApoio(paginas.flatMap((pagina) => pagina.itens)));
  }, [podeAcessar, sessao, comunidades]);

  const aoRegistrar = useCallback(
    async (aporte: AporteRegistrado) => {
      definirUltimoAporte(aporte);
      definirAulasConfirmadas([]);
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
        <Cabecalho titulo="Recursos" acao={{ rotulo: "Sair", aoAcionar: sair }} />
        <Aviso tipo="erro">{RECUSA_POR_PAPEL}</Aviso>
      </Moldura>
    );
  }

  return (
    <Moldura>
      <Cabecalho titulo="Recursos" acao={{ rotulo: "Sair", aoAcionar: sair }} />

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

      <RegistroDeAporte onRegistrado={aoRegistrar} />

      <ListaDeNecessidades
        necessidades={necessidades}
        nomeDoTipoDeRecurso={nomeDoTipoDeRecurso}
        nomeDaComunidade={nomeDaComunidade}
        nomeDoPontoDeApoio={nomeDoPontoDeApoio}
      />
    </Moldura>
  );
}
