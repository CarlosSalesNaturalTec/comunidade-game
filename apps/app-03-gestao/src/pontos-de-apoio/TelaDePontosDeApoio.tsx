import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useId, useMemo, useState } from "react";
import { type ComunidadeDaLista, listarComunidades } from "../comunidades/api";
import { type AdultoDaLista, listarApoiadores, listarMestres } from "../personas/api";
import { listarPontosDeApoio, type PontoDeApoioDaLista } from "./api";
import { ExtratoDoPontoDeApoio } from "./ExtratoDoPontoDeApoio";
import { FormularioDePontoDeApoio } from "./FormularioDePontoDeApoio";
import { ListaDePontosDeApoio } from "./ListaDePontosDeApoio";
import { TransferenciaDeSaldo } from "./TransferenciaDeSaldo";

export function TelaDePontosDeApoio() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const idDoSeletor = useId();
  const [comunidades, definirComunidades] = useState<ComunidadeDaLista[]>([]);
  const [comunidadeId, definirComunidadeId] = useState("");
  const [pontosDeApoio, definirPontosDeApoio] = useState<PontoDeApoioDaLista[] | null>(null);
  const [adultos, definirAdultos] = useState<AdultoDaLista[]>([]);
  const [erro, definirErro] = useState<string | null>(null);
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);
  const [origemDaTransferencia, definirOrigemDaTransferencia] =
    useState<PontoDeApoioDaLista | null>(null);
  const [pontoDeApoioDoExtrato, definirPontoDeApoioDoExtrato] =
    useState<PontoDeApoioDaLista | null>(null);

  // O caminho de cadastro não é oferecido a quem não é Admin (`RF-07-47`).
  const podeCadastrar = sessao?.papel === "admin";

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
    if (!sessao) return;
    // Admin declara a comunidade, sempre; o Mestre a tem derivada do
    // próprio vínculo (`RF-07-47`, `RF-01-18`).
    if (podeCadastrar && !comunidadeId) return;

    try {
      const pagina = await listarPontosDeApoio(
        sessao.token,
        podeCadastrar ? comunidadeId : undefined,
      );
      definirPontosDeApoio(pagina.itens);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro(
        "Não foi possível carregar os pontos de apoio. Tente novamente em instantes.",
      );
    }
  }, [sessao, podeCadastrar, comunidadeId, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  // Os Mestres e Apoiadores cadastrados são o universo de quem pode ser
  // designado responsável pelo acervo (`RF-07-49`, `RN-07-34`).
  useEffect(() => {
    if (!sessao) return;
    Promise.all([listarMestres(sessao.token), listarApoiadores(sessao.token)]).then(
      ([mestres, apoiadores]) => {
        definirAdultos([...mestres.itens, ...apoiadores.itens]);
      },
    );
  }, [sessao]);

  const nomePorId = useMemo(
    () => new Map(adultos.map((adulto) => [adulto.id, adulto.nome])),
    [adultos],
  );

  const aoCriar = useCallback(async () => {
    definirMostrarFormulario(false);
    await carregar();
  }, [carregar]);

  return (
    <Moldura>
      <Cabecalho titulo="Pontos de Apoio" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      {podeCadastrar && comunidades.length > 0 && (
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

      {podeCadastrar && !mostrarFormulario && (
        <Botao onClick={() => definirMostrarFormulario(true)}>Novo ponto de apoio</Botao>
      )}

      {podeCadastrar && mostrarFormulario && (
        <FormularioDePontoDeApoio
          comunidades={comunidades}
          onCriado={aoCriar}
          onCancelar={() => definirMostrarFormulario(false)}
        />
      )}

      {origemDaTransferencia && pontosDeApoio ? (
        <TransferenciaDeSaldo
          origem={origemDaTransferencia}
          pontosDeApoio={pontosDeApoio}
          onConcluida={() => {
            definirOrigemDaTransferencia(null);
            carregar();
          }}
          onCancelar={() => definirOrigemDaTransferencia(null)}
        />
      ) : pontoDeApoioDoExtrato ? (
        <ExtratoDoPontoDeApoio
          pontoDeApoio={pontoDeApoioDoExtrato}
          onVoltar={() => definirPontoDeApoioDoExtrato(null)}
        />
      ) : (
        <ListaDePontosDeApoio
          pontosDeApoio={pontosDeApoio}
          podeGerenciar={podeCadastrar}
          nomePorId={nomePorId}
          adultos={adultos}
          aoMudarSituacao={carregar}
          aoDesignar={carregar}
          aoIrParaTransferencia={definirOrigemDaTransferencia}
          aoIrParaExtrato={definirPontoDeApoioDoExtrato}
        />
      )}
    </Moldura>
  );
}
