import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useCallback, useEffect, useId, useState } from "react";
import { ehRecusaDeSessao } from "../api/cliente";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { type ComunidadeDaLista, listarComunidades } from "../comunidades/api";
import { listarPontosDeApoio, type PontoDeApoioDaLista } from "./api";
import { FormularioDePontoDeApoio } from "./FormularioDePontoDeApoio";
import { ListaDePontosDeApoio } from "./ListaDePontosDeApoio";

export function TelaDePontosDeApoio() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const idDoSeletor = useId();
  const [comunidades, definirComunidades] = useState<ComunidadeDaLista[]>([]);
  const [comunidadeId, definirComunidadeId] = useState("");
  const [pontosDeApoio, definirPontosDeApoio] = useState<PontoDeApoioDaLista[] | null>(null);
  const [erro, definirErro] = useState<string | null>(null);
  const [mostrarFormulario, definirMostrarFormulario] = useState(false);

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

      <ListaDePontosDeApoio pontosDeApoio={pontosDeApoio} />
    </Moldura>
  );
}
