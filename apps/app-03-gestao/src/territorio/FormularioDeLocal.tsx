import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import { cadastrarLocal, type LocalDaLista, NIVEIS_DO_LOCAL, type NivelDoLocal } from "./api";

interface Props {
  comunidadeId: string;
  locais: LocalDaLista[];
  onCriado: (local: LocalDaLista) => void;
  onCancelar: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

export const ROTULO_DO_NIVEL: Record<NivelDoLocal, string> = {
  comunidade: "Comunidade",
  bairro: "Bairro",
  rua: "Rua",
  condominio: "Condomínio",
  bloco: "Bloco",
  quadra: "Quadra",
};

// O nível `comunidade` é o único que dispensa pai; os demais exigem um
// local já cadastrado da comunidade (`RF-02-16`, `RN-08-18`).
export function FormularioDeLocal({ comunidadeId, locais, onCriado, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoNivel = useId();
  const idDoPai = useId();
  const [nivel, definirNivel] = useState<NivelDoLocal>("bairro");
  const [rotulo, definirRotulo] = useState("");
  const [localPaiId, definirLocalPaiId] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  const exigePai = nivel !== "comunidade";

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!rotulo.trim()) {
      definirErroDeCampo({ campo: "rotulo", mensagem: "Informe o rótulo do local." });
      return;
    }
    if (exigePai && !localPaiId) {
      definirErroDeCampo({ campo: "local_pai_id", mensagem: "Escolha o local pai." });
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      const local = await cadastrarLocal(
        {
          comunidade_id: comunidadeId,
          nivel,
          rotulo,
          local_pai_id: exigePai ? localPaiId : undefined,
        },
        sessao.token,
      );
      definirRotulo("");
      definirLocalPaiId("");
      onCriado(local);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa("Não foi possível cadastrar o local. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Novo local">
      <div className="cg-campo">
        <label htmlFor={idDoNivel}>Nível</label>
        <select
          id={idDoNivel}
          value={nivel}
          onChange={(evento) => {
            definirNivel(evento.target.value as NivelDoLocal);
            definirLocalPaiId("");
          }}
        >
          {NIVEIS_DO_LOCAL.map((valor) => (
            <option key={valor} value={valor}>
              {ROTULO_DO_NIVEL[valor]}
            </option>
          ))}
        </select>
      </div>

      <Campo
        rotulo="Rótulo"
        valor={rotulo}
        aoAlterar={definirRotulo}
        erro={erroDeCampo?.campo === "rotulo" ? erroDeCampo.mensagem : null}
      />

      {exigePai && (
        <div className="cg-campo">
          <label htmlFor={idDoPai}>Local pai</label>
          <select
            id={idDoPai}
            value={localPaiId}
            onChange={(evento) => definirLocalPaiId(evento.target.value)}
            aria-invalid={erroDeCampo?.campo === "local_pai_id" || undefined}
          >
            <option value="">Selecione</option>
            {locais.map((local) => (
              <option key={local.id} value={local.id}>
                {local.rotulo}
              </option>
            ))}
          </select>
          {erroDeCampo?.campo === "local_pai_id" && (
            <p role="alert" className="cg-campo__erro">
              {erroDeCampo.mensagem}
            </p>
          )}
        </div>
      )}

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
