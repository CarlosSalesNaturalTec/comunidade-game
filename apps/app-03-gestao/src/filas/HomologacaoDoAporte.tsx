import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useEffect, useId, useState } from "react";
import { ErroDaApi, ehRecusaDeSessao } from "../api/cliente";
import { type AporteHomologado, homologarAporte } from "../aportes/api";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { type ComunidadeDaLista, listarComunidades } from "../comunidades/api";
import { listarPontosDeApoio, type PontoDeApoioDaLista } from "../pontos-de-apoio/api";
import { listarTiposDeRecurso, type TipoDeRecurso } from "../recursos/api";

interface Props {
  provedorId: string;
  solicitacaoDeParticipacaoId: string;
  aporteDeclarado: string | null;
  onHomologado: (aporte: AporteHomologado) => void;
}

const FORMAS: { valor: "financeira" | "material" | "servico"; rotulo: string }[] = [
  { valor: "financeira", rotulo: "Financeira" },
  { valor: "material", rotulo: "Material" },
  { valor: "servico", rotulo: "Serviço" },
];

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

// Registra pela mesma rota `POST /aportes` que a gestão avulsa já usa,
// apontando a solicitação de origem (`RF-02-84`, `RF-07-30`, `RN-07-21`).
// Nenhuma rota nova de escrita — só a leitura do catálogo entrou fora da
// proposal (design — decisão 6).
export function HomologacaoDoAporte({
  provedorId,
  solicitacaoDeParticipacaoId,
  aporteDeclarado,
  onHomologado,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDaComunidade = useId();
  const idDoPontoDeApoio = useId();
  const idDoTipo = useId();
  const idDaForma = useId();

  const [comunidades, definirComunidades] = useState<ComunidadeDaLista[]>([]);
  const [comunidadeId, definirComunidadeId] = useState("");
  const [pontosDeApoio, definirPontosDeApoio] = useState<PontoDeApoioDaLista[]>([]);
  const [pontoDeApoioId, definirPontoDeApoioId] = useState("");
  const [tipos, definirTipos] = useState<TipoDeRecurso[]>([]);
  const [tipoDeRecursoId, definirTipoDeRecursoId] = useState("");
  const [quantidade, definirQuantidade] = useState("");
  const [dataDoAporte, definirDataDoAporte] = useState("");
  const [forma, definirForma] = useState<(typeof FORMAS)[number]["valor"]>("financeira");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [jaHomologado, definirJaHomologado] = useState(false);
  const [enviando, definirEnviando] = useState(false);

  useEffect(() => {
    if (!sessao) return;
    listarComunidades().then((pagina) => {
      definirComunidades(pagina.itens);
      definirComunidadeId((atual) => atual || (pagina.itens[0]?.id ?? ""));
    });
    listarTiposDeRecurso(sessao.token).then(definirTipos);
  }, [sessao]);

  useEffect(() => {
    if (!sessao || !comunidadeId) return;
    listarPontosDeApoio(sessao.token, comunidadeId).then((pagina) => {
      definirPontosDeApoio(pagina.itens);
      definirPontoDeApoioId((atual) =>
        pagina.itens.some((item) => item.id === atual) ? atual : (pagina.itens[0]?.id ?? ""),
      );
    });
  }, [sessao, comunidadeId]);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!pontoDeApoioId) {
      definirErroDeCampo({
        campo: "ponto_de_apoio_id",
        mensagem: "Escolha o ponto de apoio.",
      });
      return;
    }
    if (!tipoDeRecursoId) {
      definirErroDeCampo({
        campo: "tipo_de_recurso_id",
        mensagem: "Escolha o tipo de recurso.",
      });
      return;
    }
    if (!quantidade.trim()) {
      definirErroDeCampo({ campo: "quantidade", mensagem: "Informe a quantidade." });
      return;
    }
    if (!dataDoAporte) {
      definirErroDeCampo({ campo: "data_do_aporte", mensagem: "Informe a data do aporte." });
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      const aporte = await homologarAporte(
        {
          provedorId,
          tipoDeRecursoId,
          quantidade,
          pontoDeApoioId,
          dataDoAporte,
          forma,
          solicitacaoDeParticipacaoId,
        },
        sessao.token,
      );
      onHomologado(aporte);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.campo === "solicitacao_de_participacao_id") {
        definirJaHomologado(true);
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa(
        "Não foi possível homologar o aporte. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  if (jaHomologado) {
    return <Aviso tipo="sucesso">O aporte desta solicitação já foi homologado.</Aviso>;
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Homologar aporte declarado">
      {aporteDeclarado && <p>Declarado no pré-cadastro: {aporteDeclarado}</p>}

      <div className="cg-campo">
        <label htmlFor={idDaComunidade}>Comunidade</label>
        <select
          id={idDaComunidade}
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

      <div className="cg-campo">
        <label htmlFor={idDoPontoDeApoio}>Ponto de apoio</label>
        <select
          id={idDoPontoDeApoio}
          value={pontoDeApoioId}
          onChange={(evento) => definirPontoDeApoioId(evento.target.value)}
        >
          {pontosDeApoio.map((ponto) => (
            <option key={ponto.id} value={ponto.id}>
              {ponto.nome}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "ponto_de_apoio_id" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <div className="cg-campo">
        <label htmlFor={idDoTipo}>Tipo de recurso</label>
        <select
          id={idDoTipo}
          value={tipoDeRecursoId}
          onChange={(evento) => definirTipoDeRecursoId(evento.target.value)}
        >
          <option value="">Escolha um tipo</option>
          {tipos.map((tipo) => (
            <option key={tipo.id} value={tipo.id}>
              {tipo.nome} — {tipo.valor_em_moedas} moedas/{tipo.unidade}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "tipo_de_recurso_id" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      <Campo
        rotulo="Quantidade"
        valor={quantidade}
        aoAlterar={definirQuantidade}
        erro={erroDeCampo?.campo === "quantidade" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="Data do aporte"
        tipo="date"
        valor={dataDoAporte}
        aoAlterar={definirDataDoAporte}
        erro={erroDeCampo?.campo === "data_do_aporte" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDaForma}>Forma</label>
        <select
          id={idDaForma}
          value={forma}
          onChange={(evento) => definirForma(evento.target.value as typeof forma)}
        >
          {FORMAS.map((item) => (
            <option key={item.valor} value={item.valor}>
              {item.rotulo}
            </option>
          ))}
        </select>
      </div>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Homologar aporte
      </Botao>
    </form>
  );
}
