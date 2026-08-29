import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useId, useMemo, useState } from "react";
import { type ComunidadeDaLista, listarComunidades } from "../comunidades/api";
import {
  type AdultoDaLista,
  type GuerreiroDaLista,
  listarApoiadores,
  listarGuerreiros,
  listarMestres,
} from "../personas/api";
import { listarPontosDeApoio, type PontoDeApoioDaLista } from "../pontos-de-apoio/api";
import { listarTiposDeRecurso, type TipoDeRecurso } from "../recursos/api";
import {
  type EntregaDeRecompensa,
  type ItemPatrimonialDaLista,
  listarAcervo,
  listarEntregas,
} from "./api";
import { FormularioDeTombamento } from "./FormularioDeTombamento";
import { ListaDeEntregas } from "./ListaDeEntregas";
import { ListaDoAcervo } from "./ListaDoAcervo";

export function TelaDoAcervo() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const idDoSeletor = useId();
  const [comunidades, definirComunidades] = useState<ComunidadeDaLista[]>([]);
  const [comunidadeId, definirComunidadeId] = useState("");
  const [itens, definirItens] = useState<ItemPatrimonialDaLista[] | null>(null);
  const [pontosDeApoio, definirPontosDeApoio] = useState<PontoDeApoioDaLista[]>([]);
  const [adultos, definirAdultos] = useState<AdultoDaLista[]>([]);
  const [entregas, definirEntregas] = useState<EntregaDeRecompensa[] | null>(null);
  const [tiposDeRecurso, definirTiposDeRecurso] = useState<TipoDeRecurso[]>([]);
  const [guerreiros, definirGuerreiros] = useState<GuerreiroDaLista[]>([]);
  const [erro, definirErro] = useState<string | null>(null);
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);

  // Tombar é restrito ao Admin; anotar é aberto a Admin e Mestre — a área
  // nunca oferece retirada, empréstimo, devolução nem transferência
  // (`RF-02-52`, `RF-02-55`, `RN-02-18`).
  const podeTombar = sessao?.papel === "admin";
  const podeAnotar = sessao?.papel === "admin" || sessao?.papel === "mestre";

  useEffect(() => {
    listarComunidades()
      .then((pagina) => {
        definirComunidades(pagina.itens);
        definirComunidadeId((atual) => atual || (pagina.itens[0]?.id ?? ""));
      })
      .catch(() => {
        definirErro("Não foi possível carregar as comunidades. Tente novamente em instantes.");
      });
  }, []);

  const carregar = useCallback(async () => {
    if (!sessao || !comunidadeId) return;
    try {
      const [
        itensCarregados,
        paginaDePontosDeApoio,
        paginaDeMestres,
        paginaDeApoiadores,
        entregasCarregadas,
        tiposDeRecursoCarregados,
        paginaDeGuerreiros,
      ] = await Promise.all([
        listarAcervo(comunidadeId, sessao.token),
        listarPontosDeApoio(sessao.token, comunidadeId),
        listarMestres(sessao.token),
        listarApoiadores(sessao.token),
        listarEntregas(sessao.token),
        listarTiposDeRecurso(sessao.token),
        listarGuerreiros(sessao.token),
      ]);
      definirItens(itensCarregados);
      definirPontosDeApoio(paginaDePontosDeApoio.itens);
      definirAdultos([...paginaDeMestres.itens, ...paginaDeApoiadores.itens]);
      definirEntregas(entregasCarregadas);
      definirTiposDeRecurso(tiposDeRecursoCarregados);
      definirGuerreiros(paginaDeGuerreiros.itens);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar o acervo. Tente novamente em instantes.");
    }
  }, [sessao, comunidadeId, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  // Nome do responsável e do ponto de apoio resolvidos por mapa, a partir
  // do que a área já lê — o núcleo devolve identificador, a tela nunca o
  // exibe (design — decisão 3).
  const pontoDeApoioPorId = useMemo(
    () => new Map(pontosDeApoio.map((ponto) => [ponto.id, ponto.nome])),
    [pontosDeApoio],
  );
  const nomePorId = useMemo(
    () => new Map(adultos.map((adulto) => [adulto.id, adulto.nome])),
    [adultos],
  );
  const tipoDeRecursoPorId = useMemo(
    () => new Map(tiposDeRecurso.map((tipo) => [tipo.id, tipo.nome])),
    [tiposDeRecurso],
  );
  const nickDoGuerreiroPorId = useMemo(
    () => new Map(guerreiros.map((guerreiro) => [guerreiro.id, guerreiro.nick])),
    [guerreiros],
  );

  // A releitura é do acervo inteiro da comunidade depois de tombar ou
  // anotar (design — decisão 6).
  const aoTombar = useCallback(async () => {
    definirMostrarFormulario(false);
    await carregar();
  }, [carregar]);

  return (
    <Moldura>
      <Cabecalho titulo="Acervo" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {comunidades.length > 0 && (
        <div className="cg-campo">
          <label htmlFor={idDoSeletor}>Comunidade</label>
          <select
            id={idDoSeletor}
            value={comunidadeId}
            onChange={(evento) => definirComunidadeId(evento.target.value)}
          >
            {comunidades.map((comunidade) => (
              <option key={comunidade.id} value={comunidade.id}>
                {comunidade.nome}
              </option>
            ))}
          </select>
        </div>
      )}

      {podeTombar && !mostrarFormulario && (
        <Botao onClick={() => definirMostrarFormulario(true)}>Tombar exemplar</Botao>
      )}
      {podeTombar && mostrarFormulario && (
        <FormularioDeTombamento
          pontosDeApoio={pontosDeApoio}
          onTombado={aoTombar}
          onCancelar={() => definirMostrarFormulario(false)}
        />
      )}

      <ListaDoAcervo
        itens={itens}
        pontoDeApoioPorId={pontoDeApoioPorId}
        nomePorId={nomePorId}
        podeAnotar={podeAnotar}
        onAnotado={carregar}
      />

      <ListaDeEntregas
        itens={entregas}
        tipoDeRecursoPorId={tipoDeRecursoPorId}
        pontoDeApoioPorId={pontoDeApoioPorId}
        nomeDoMestrePorId={nomePorId}
        nickDoGuerreiroPorId={nickDoGuerreiroPorId}
      />
    </Moldura>
  );
}
