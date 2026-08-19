import { type FormEvent, useState } from "react";
import { ErroDaApi, ehRecusaDeSessao } from "../api/cliente";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { criarComunidade } from "./api";

interface Props {
  onCriada: () => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const RECUSA_POR_PAPEL = "Só o Admin cria Comunidade Virtual.";

export function FormularioDeComunidade({ onCriada, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [nome, definirNome] = useState("");
  const [localizacao, definirLocalizacao] = useState("");
  const [granularidadeMaxima, definirGranularidadeMaxima] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    // Campo obrigatório em falta é apontado no campo, sem chamar o núcleo
    // e sem criar nada (`RN-02-04`, PRD-02 §4).
    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome da comunidade." });
      return;
    }
    if (!localizacao.trim()) {
      definirErroDeCampo({ campo: "localizacao", mensagem: "Informe a localização." });
      return;
    }
    if (!granularidadeMaxima.trim()) {
      definirErroDeCampo({
        campo: "granularidade_maxima",
        mensagem: "Informe a granularidade máxima.",
      });
      return;
    }

    if (!sessao) return;

    definirEnviando(true);
    try {
      await criarComunidade(
        { nome, localizacao, granularidade_maxima: granularidadeMaxima },
        sessao.token,
      );
      onCriada();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "permissao_negada") {
        definirErroDeRecusa(RECUSA_POR_PAPEL);
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa(
        "Não foi possível criar a comunidade. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Nova Comunidade Virtual">
      <label htmlFor="campo-nome">Nome</label>
      <input id="campo-nome" value={nome} onChange={(e) => definirNome(e.target.value)} />
      {erroDeCampo?.campo === "nome" && <p role="alert">{erroDeCampo.mensagem}</p>}

      <label htmlFor="campo-localizacao">Localização</label>
      <input
        id="campo-localizacao"
        value={localizacao}
        onChange={(e) => definirLocalizacao(e.target.value)}
      />
      {erroDeCampo?.campo === "localizacao" && <p role="alert">{erroDeCampo.mensagem}</p>}

      <label htmlFor="campo-granularidade">Granularidade máxima</label>
      <input
        id="campo-granularidade"
        value={granularidadeMaxima}
        onChange={(e) => definirGranularidadeMaxima(e.target.value)}
      />
      {erroDeCampo?.campo === "granularidade_maxima" && (
        <p role="alert">{erroDeCampo.mensagem}</p>
      )}

      {erroDeRecusa && <p role="alert">{erroDeRecusa}</p>}

      <button type="submit" disabled={enviando}>
        Criar
      </button>
      <button type="button" onClick={onCancelar}>
        Cancelar
      </button>
    </form>
  );
}
