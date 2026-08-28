import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type ChangeEvent, type FormEvent, useEffect, useId, useState } from "react";
import { type ComunidadeDaLista, listarComunidades } from "../comunidades/api";
import { type AdultoDaLista, listarApoiadores, listarMestres } from "../personas/api";
import { listarPontosDeApoio, type PontoDeApoioDaLista } from "../pontos-de-apoio/api";
import {
  type AporteRegistrado,
  listarTiposDeRecurso,
  registrarAporte,
  type TipoDeRecurso,
} from "./api";

interface Props {
  onRegistrado: (aporte: AporteRegistrado) => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const FORMAS: { valor: "financeira" | "material" | "servico"; rotulo: string }[] = [
  { valor: "financeira", rotulo: "Financeira" },
  { valor: "material", rotulo: "Material" },
  { valor: "servico", rotulo: "Serviço" },
];

const RECUSA_DE_CAUSA_PROPRIA = "Quem registra o aporte não pode ser o próprio provedor.";
const MENSAGEM_DE_FALHA = "Não foi possível registrar o aporte. Tente novamente em instantes.";

// O registro avulso — porta comum de crédito do livro-razão, ao contrário
// de `HomologacaoDoAporte`, que só fecha o que o pré-cadastro já declarou
// (`RF-02-57`, `RN-02-19`).
export function RegistroDeAporte({ onRegistrado }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoProvedor = useId();
  const idDaComunidade = useId();
  const idDoPontoDeApoio = useId();
  const idDoTipo = useId();
  const idDaForma = useId();
  const idDoComprovante = useId();

  const [adultos, definirAdultos] = useState<AdultoDaLista[]>([]);
  const [provedorId, definirProvedorId] = useState("");
  const [comunidades, definirComunidades] = useState<ComunidadeDaLista[]>([]);
  const [comunidadeId, definirComunidadeId] = useState("");
  const [pontosDeApoio, definirPontosDeApoio] = useState<PontoDeApoioDaLista[]>([]);
  const [pontoDeApoioId, definirPontoDeApoioId] = useState("");
  const [tipos, definirTipos] = useState<TipoDeRecurso[]>([]);
  const [tipoDeRecursoId, definirTipoDeRecursoId] = useState("");
  const [quantidade, definirQuantidade] = useState("");
  const [dataDoAporte, definirDataDoAporte] = useState("");
  const [forma, definirForma] = useState<(typeof FORMAS)[number]["valor"]>("financeira");
  const [comprovante, definirComprovante] = useState<File | undefined>(undefined);
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  useEffect(() => {
    if (!sessao) return;
    Promise.all([listarMestres(sessao.token), listarApoiadores(sessao.token)]).then(
      ([mestres, apoiadores]) => {
        definirAdultos([...mestres.itens, ...apoiadores.itens]);
      },
    );
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

  const tipoEscolhido = tipos.find((tipo) => tipo.id === tipoDeRecursoId) ?? null;

  function aoEscolherArquivo(evento: ChangeEvent<HTMLInputElement>) {
    definirComprovante(evento.target.files?.[0]);
  }

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!provedorId) {
      definirErroDeCampo({ campo: "provedor_id", mensagem: "Escolha o provedor." });
      return;
    }
    if (!tipoDeRecursoId) {
      definirErroDeCampo({
        campo: "tipo_de_recurso_id",
        mensagem: "Escolha o tipo de recurso.",
      });
      return;
    }
    if (!quantidade.trim() || Number(quantidade) <= 0) {
      definirErroDeCampo({
        campo: "quantidade",
        mensagem: "Informe uma quantidade maior que zero.",
      });
      return;
    }
    if (!pontoDeApoioId) {
      definirErroDeCampo({
        campo: "ponto_de_apoio_id",
        mensagem: "Escolha o ponto de apoio.",
      });
      return;
    }
    if (!dataDoAporte) {
      definirErroDeCampo({ campo: "data_do_aporte", mensagem: "Informe a data do aporte." });
      return;
    }
    // O tipo que exige comprovante bloqueia o envio sem ele, no próprio
    // campo, antes de chegar ao núcleo (`RF-02-57`).
    if (tipoEscolhido?.exige_comprovante && !comprovante) {
      definirErroDeCampo({
        campo: "comprovante",
        mensagem: "Este tipo de recurso exige o comprovante.",
      });
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      const aporte = await registrarAporte(
        {
          provedorId,
          tipoDeRecursoId,
          quantidade,
          pontoDeApoioId,
          dataDoAporte,
          forma,
          comprovante,
        },
        sessao.token,
      );
      onRegistrado(aporte);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "permissao_negada") {
        definirErroDeRecusa(RECUSA_DE_CAUSA_PROPRIA);
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa(MENSAGEM_DE_FALHA);
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Registrar aporte">
      <div className="cg-campo">
        <label htmlFor={idDoProvedor}>Provedor</label>
        <select
          id={idDoProvedor}
          value={provedorId}
          onChange={(evento) => definirProvedorId(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "provedor_id" || undefined}
        >
          <option value="">Escolha o provedor</option>
          {adultos.map((adulto) => (
            <option key={adulto.id} value={adulto.id}>
              {adulto.nome}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "provedor_id" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

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
          aria-invalid={erroDeCampo?.campo === "ponto_de_apoio_id" || undefined}
        >
          <option value="">Selecione</option>
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
          aria-invalid={erroDeCampo?.campo === "tipo_de_recurso_id" || undefined}
        >
          <option value="">Escolha um tipo</option>
          {tipos.map((tipo) => (
            <option key={tipo.id} value={tipo.id}>
              {tipo.nome}
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

      <div className="cg-campo">
        <label htmlFor={idDoComprovante}>Comprovante</label>
        <input
          id={idDoComprovante}
          type="file"
          accept="application/pdf,image/jpeg,image/png"
          onChange={aoEscolherArquivo}
          aria-invalid={erroDeCampo?.campo === "comprovante" || undefined}
        />
        {erroDeCampo?.campo === "comprovante" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Registrar aporte
      </Botao>
    </form>
  );
}
