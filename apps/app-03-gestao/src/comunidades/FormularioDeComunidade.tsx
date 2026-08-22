import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useState } from "react";
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
      <Campo
        rotulo="Nome"
        valor={nome}
        aoAlterar={definirNome}
        erro={erroDeCampo?.campo === "nome" ? erroDeCampo.mensagem : null}
      />

      <Campo
        rotulo="Localização"
        valor={localizacao}
        aoAlterar={definirLocalizacao}
        erro={erroDeCampo?.campo === "localizacao" ? erroDeCampo.mensagem : null}
      />

      <Campo
        rotulo="Granularidade máxima"
        valor={granularidadeMaxima}
        aoAlterar={definirGranularidadeMaxima}
        erro={erroDeCampo?.campo === "granularidade_maxima" ? erroDeCampo.mensagem : null}
      />

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Criar
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
