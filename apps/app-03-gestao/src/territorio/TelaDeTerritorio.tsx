import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useId, useMemo, useState } from "react";
import { type ComunidadeDaLista, listarComunidades } from "../comunidades/api";
import { listarGuerreiros } from "../personas/api";
import {
  type DesafioPublicadoDaLista,
  type LocalDaLista,
  listarDesafiosDeColetaPublicados,
  listarSolicitacoesDeLocalAbertas,
  listarTodosOsLocais,
  type SolicitacaoDeLocalDaLista,
} from "./api";
import { FilaDeSolicitacoesDeLocal } from "./FilaDeSolicitacoesDeLocal";
import { FormularioDeLocal } from "./FormularioDeLocal";
import { HierarquiaDeLocais } from "./HierarquiaDeLocais";
import { ListaDeDesafiosPublicados } from "./ListaDeDesafiosPublicados";

export function TelaDeTerritorio() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const idDoSeletor = useId();
  const [comunidades, definirComunidades] = useState<ComunidadeDaLista[]>([]);
  const [comunidadeId, definirComunidadeId] = useState("");
  const [locais, definirLocais] = useState<LocalDaLista[] | null>(null);
  const [solicitacoes, definirSolicitacoes] = useState<SolicitacaoDeLocalDaLista[] | null>(
    null,
  );
  const [desafios, definirDesafios] = useState<DesafioPublicadoDaLista[] | null>(null);
  const [guerreiroPorId, definirGuerreiroPorId] = useState<Map<string, { nick: string }>>(
    new Map(),
  );
  const [erro, definirErro] = useState<string | null>(null);
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);

  // Cadastro de local e desfecho de solicitação são restritos ao Admin
  // (`RF-02-16`, `RF-02-22`); a fila e a hierarquia são leitura de
  // qualquer adulto em sessão que abra a área.
  const podeAdministrar = sessao?.papel === "admin";

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
      const [locaisCarregados, paginaDeSolicitacoes, paginaDeDesafios] = await Promise.all([
        listarTodosOsLocais(comunidadeId),
        listarSolicitacoesDeLocalAbertas(comunidadeId, sessao.token),
        listarDesafiosDeColetaPublicados(sessao.token),
      ]);
      definirLocais(locaisCarregados);
      definirSolicitacoes(paginaDeSolicitacoes.itens);
      definirDesafios(paginaDeDesafios.itens);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar o território. Tente novamente em instantes.");
    }
  }, [sessao, comunidadeId, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  useEffect(() => {
    if (!sessao) return;
    listarGuerreiros(sessao.token)
      .then((pagina) => {
        definirGuerreiroPorId(
          new Map(pagina.itens.map((guerreiro) => [guerreiro.id, { nick: guerreiro.nick }])),
        );
      })
      .catch(() => {
        // A ausência do nick não impede a fila de aparecer — só empobrece a
        // apresentação do solicitante.
      });
  }, [sessao]);

  const desafioPorId = useMemo(
    () => new Map((desafios ?? []).map((desafio) => [desafio.id, desafio])),
    [desafios],
  );

  const aoCadastrarLocal = useCallback(async () => {
    definirMostrarFormulario(false);
    await carregar();
  }, [carregar]);

  return (
    <Moldura>
      <Cabecalho titulo="Território" acao={{ rotulo: "Sair", aoAcionar: sair }} />

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

      <h2>Locais</h2>
      {podeAdministrar && !mostrarFormulario && (
        <Botao onClick={() => definirMostrarFormulario(true)}>Novo local</Botao>
      )}
      {podeAdministrar && mostrarFormulario && (
        <FormularioDeLocal
          comunidadeId={comunidadeId}
          locais={locais ?? []}
          onCriado={aoCadastrarLocal}
          onCancelar={() => definirMostrarFormulario(false)}
        />
      )}
      <HierarquiaDeLocais locais={locais} />

      <h2>Solicitações de novo local</h2>
      <FilaDeSolicitacoesDeLocal
        solicitacoes={solicitacoes}
        locais={locais ?? []}
        guerreiroPorId={guerreiroPorId}
        desafioPorId={desafioPorId}
        podeAvaliar={podeAdministrar}
        onAvaliada={carregar}
      />

      <h2>Desafios de coleta publicados</h2>
      <ListaDeDesafiosPublicados desafios={desafios} />
    </Moldura>
  );
}
