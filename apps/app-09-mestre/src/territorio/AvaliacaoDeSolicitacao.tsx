import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { useId, useState } from "react";
import {
  avaliarSolicitacaoDeLocal,
  type LocalDaLista,
  type SolicitacaoDeLocalDaLista,
} from "./api";

interface Props {
  solicitacao: SolicitacaoDeLocalDaLista;
  locais: LocalDaLista[];
  onConcluida: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

// Dois desfechos possíveis, cada um com o campo que exige (`RF-09-53`): a
// aprovação exige o local pai dentro da hierarquia da comunidade da
// solicitação, e a recusa exige o motivo. Recusada pelo núcleo — hierarquia
// inválida, recusa sem motivo, ou solicitação já avaliada —, a solicitação
// continua na fila (`RN-09-16`).
export function AvaliacaoDeSolicitacao({ solicitacao, locais, onConcluida }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoPai = useId();
  const [localPaiId, definirLocalPaiId] = useState("");
  const [motivo, definirMotivo] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState<"aprovada" | "recusada" | null>(null);

  async function avaliar(situacao: "aprovada" | "recusada") {
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (situacao === "aprovada" && !localPaiId) {
      definirErroDeCampo({ campo: "local_pai_id", mensagem: "Escolha o local pai." });
      return;
    }
    if (situacao === "recusada" && !motivo.trim()) {
      definirErroDeCampo({ campo: "motivo", mensagem: "Informe o motivo da recusa." });
      return;
    }
    if (!sessao) return;

    definirEnviando(situacao);
    try {
      await avaliarSolicitacaoDeLocal(
        solicitacao.id,
        situacao === "aprovada"
          ? { situacao, local_pai_id: localPaiId }
          : { situacao, motivo },
        sessao.token,
      );
      definirLocalPaiId("");
      definirMotivo("");
      onConcluida();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.campo) {
        definirErroDeCampo({ campo: erro.campo, mensagem: erro.message });
        return;
      }
      definirErroDeRecusa(
        "Não foi possível registrar o desfecho. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(null);
    }
  }

  return (
    <div className="avaliacao-de-solicitacao">
      <div className="cg-campo">
        <label htmlFor={idDoPai}>Local pai (para aprovar)</label>
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

      <Campo
        rotulo="Motivo da recusa"
        valor={motivo}
        aoAlterar={definirMotivo}
        erro={erroDeCampo?.campo === "motivo" ? erroDeCampo.mensagem : null}
      />

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao desabilitado={enviando !== null} onClick={() => avaliar("aprovada")}>
        Aprovar
      </Botao>
      <Botao
        variante="secundaria"
        desabilitado={enviando !== null}
        onClick={() => avaliar("recusada")}
      >
        Recusar
      </Botao>
    </div>
  );
}
