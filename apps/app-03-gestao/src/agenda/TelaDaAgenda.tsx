import { Aviso, Botao, Cabecalho, CampoDeDataHora, Moldura } from "comum/react";
import { useCallback, useEffect, useId, useMemo, useState } from "react";
import { ehRecusaDeSessao } from "../api/cliente";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { type ComunidadeDaLista, listarComunidades } from "../comunidades/api";
import { listarPontosDeApoio, type PontoDeApoioDaLista } from "../pontos-de-apoio/api";
import { type AulaDaAgenda, cancelarAula, listarAgenda } from "./api";
import { FormularioDeAgendamento } from "./FormularioDeAgendamento";
import { ListaDaAgenda } from "./ListaDaAgenda";

export function TelaDaAgenda() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const idDoSeletorDeComunidade = useId();
  const [comunidades, definirComunidades] = useState<ComunidadeDaLista[]>([]);
  const [comunidadeId, definirComunidadeId] = useState("");
  const [pontosDeApoio, definirPontosDeApoio] = useState<PontoDeApoioDaLista[]>([]);
  const [periodoInicio, definirPeriodoInicio] = useState("");
  const [periodoFim, definirPeriodoFim] = useState("");
  const [aulas, definirAulas] = useState<AulaDaAgenda[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);

  // O caminho de agendamento não é oferecido a quem não é Admin (`RF-02-12`).
  const podeAgendar = sessao?.papel === "admin";
  // Admin e o Mestre da comunidade da aula cancelam — e a agenda que o
  // Mestre lê já vem filtrada pela sua própria comunidade (`RF-02-95`,
  // `RF-01-72`).
  const podeCancelar = sessao?.papel === "admin" || sessao?.papel === "mestre";

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

  useEffect(() => {
    if (!sessao || !comunidadeId) {
      definirPontosDeApoio([]);
      return;
    }
    listarPontosDeApoio(sessao.token, comunidadeId)
      .then((pagina) => definirPontosDeApoio(pagina.itens))
      .catch(() => definirPontosDeApoio([]));
  }, [sessao, comunidadeId]);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    // Admin declara a comunidade, sempre; o Mestre a tem derivada do
    // próprio vínculo (`RF-02-12`, `RF-01-18`).
    if (podeAgendar && !comunidadeId) return;

    try {
      const pagina = await listarAgenda(sessao.token, {
        comunidadeId: podeAgendar ? comunidadeId : undefined,
        periodoInicio: periodoInicio || undefined,
        periodoFim: periodoFim || undefined,
      });
      definirAulas(pagina.itens);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível carregar a agenda. Tente novamente em instantes.");
    }
  }, [sessao, podeAgendar, comunidadeId, periodoInicio, periodoFim, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  const aoAgendar = useCallback(async () => {
    definirMostrarFormulario(false);
    await carregar();
  }, [carregar]);

  const aoCancelar = useCallback(
    async (idDaAula: string, motivo: string) => {
      if (!sessao) return;
      try {
        await cancelarAula(idDaAula, motivo, sessao.token);
        await carregar();
      } catch (erroCapturado) {
        if (ehRecusaDeSessao(erroCapturado)) {
          tratarRecusaDeSessao();
          return;
        }
        definirErro("Não foi possível cancelar a aula. Tente novamente em instantes.");
      }
    },
    [sessao, carregar, tratarRecusaDeSessao],
  );

  const nomeDaComunidade = useMemo(() => {
    const porId = new Map(comunidades.map((comunidade) => [comunidade.id, comunidade.nome]));
    return (id: string) => porId.get(id) ?? id;
  }, [comunidades]);

  const nomeDoPontoDeApoio = useMemo(() => {
    const porId = new Map(
      pontosDeApoio.map((pontoDeApoio) => [pontoDeApoio.id, pontoDeApoio.nome]),
    );
    return (id: string) => porId.get(id) ?? id;
  }, [pontosDeApoio]);

  return (
    <Moldura>
      <Cabecalho titulo="Agenda de Aulas" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {podeAgendar && comunidades.length > 0 && (
        <div className="cg-campo">
          <label htmlFor={idDoSeletorDeComunidade}>Comunidade</label>
          <select
            id={idDoSeletorDeComunidade}
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

      <CampoDeDataHora
        rotulo="Início do período"
        valor={periodoInicio}
        aoAlterar={definirPeriodoInicio}
      />
      <CampoDeDataHora
        rotulo="Fim do período"
        valor={periodoFim}
        aoAlterar={definirPeriodoFim}
      />

      {podeAgendar && !mostrarFormulario && (
        <Botao onClick={() => definirMostrarFormulario(true)}>Nova aula</Botao>
      )}

      {podeAgendar && mostrarFormulario && (
        <FormularioDeAgendamento
          comunidades={comunidades}
          onAgendada={aoAgendar}
          onCancelar={() => definirMostrarFormulario(false)}
        />
      )}

      <ListaDaAgenda
        aulas={aulas}
        nomeDaComunidade={nomeDaComunidade}
        nomeDoPontoDeApoio={nomeDoPontoDeApoio}
        podeCancelar={podeCancelar}
        aoCancelar={aoCancelar}
      />
    </Moldura>
  );
}
