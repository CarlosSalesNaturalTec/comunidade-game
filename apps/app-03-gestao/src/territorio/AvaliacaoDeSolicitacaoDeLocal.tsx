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
  onConcluido: () => void;
}

interface ErroDeCampo {
  campo: string;
  mensagem: string;
}

// Dois desfechos possíveis, cada um com o campo que exige (`RF-02-22`,
// `RF-08-23`): aprovar informando o local pai, ou recusar com motivo. A
// recusa da hierarquia devolve a solicitação à fila — este componente só
// fecha quando `avaliarSolicitacaoDeLocal` responde com sucesso.
export function AvaliacaoDeSolicitacaoDeLocal({ solicitacao, locais, onConcluido }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoPai = useId();
  const [aberto, definirAberto] = useState(false);
  const [localPaiId, definirLocalPaiId] = useState("");
  const [motivo, definirMotivo] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<ErroDeCampo | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState<"aprovada" | "recusada" | null>(null);

  if (!aberto) {
    return (
      <Botao variante="secundaria" onClick={() => definirAberto(true)}>
        Avaliar
      </Botao>
    );
  }

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
      definirAberto(false);
      definirLocalPaiId("");
      definirMotivo("");
      onConcluido();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "erro_de_validacao" && erro.campo) {
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
    <div className="avaliacao-de-solicitacao-de-local">
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
      <Botao variante="secundaria" onClick={() => definirAberto(false)}>
        Voltar
      </Botao>
    </div>
  );
}
