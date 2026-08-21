import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import { ErroDaApi, ehRecusaDeSessao } from "../api/cliente";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import type { ComunidadeDaLista } from "../comunidades/api";
import { cadastrarPontoDeApoio } from "./api";

interface Props {
  comunidades: ComunidadeDaLista[];
  onCriado: () => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

const RECUSA_POR_PAPEL = "Só o Admin cadastra ponto de apoio.";

export function FormularioDePontoDeApoio({ comunidades, onCriado, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoCampoDeComunidade = useId();
  const [nome, definirNome] = useState("");
  const [comunidadeId, definirComunidadeId] = useState(comunidades[0]?.id ?? "");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    // Campo obrigatório em falta é apontado no campo, sem chamar o núcleo
    // e sem criar nada (`RF-07-47`).
    if (!nome.trim()) {
      definirErroDeCampo({ campo: "nome", mensagem: "Informe o nome do ponto de apoio." });
      return;
    }
    if (!comunidadeId) {
      definirErroDeCampo({ campo: "comunidade_id", mensagem: "Escolha a comunidade." });
      return;
    }

    if (!sessao) return;

    definirEnviando(true);
    try {
      await cadastrarPontoDeApoio({ nome, comunidade_id: comunidadeId }, sessao.token);
      onCriado();
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
        "Não foi possível cadastrar o ponto de apoio. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Novo Ponto de Apoio">
      <Campo
        rotulo="Nome"
        valor={nome}
        aoAlterar={definirNome}
        erro={erroDeCampo?.campo === "nome" ? erroDeCampo.mensagem : null}
      />

      <div className="cg-campo">
        <label htmlFor={idDoCampoDeComunidade}>Comunidade</label>
        <select
          id={idDoCampoDeComunidade}
          value={comunidadeId}
          onChange={(evento) => definirComunidadeId(evento.target.value)}
          aria-invalid={erroDeCampo?.campo === "comunidade_id" || undefined}
        >
          <option value="">Selecione</option>
          {comunidades.map((comunidade) => (
            <option key={comunidade.id} value={comunidade.id}>
              {comunidade.nome}
            </option>
          ))}
        </select>
        {erroDeCampo?.campo === "comunidade_id" && (
          <p role="alert" className="cg-campo__erro">
            {erroDeCampo.mensagem}
          </p>
        )}
      </div>

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao tipo="submit" desabilitado={enviando}>
        Cadastrar
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
