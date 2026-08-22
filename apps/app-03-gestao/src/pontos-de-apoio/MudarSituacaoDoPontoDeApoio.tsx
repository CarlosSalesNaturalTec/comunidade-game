import { Aviso, Botao, Campo } from "comum/react";
import { useState } from "react";
import { ErroDaApi, ehRecusaDeSessao } from "../api/cliente";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import "./MudarSituacaoDoPontoDeApoio.css";
import { desativarPontoDeApoio, reativarPontoDeApoio } from "./api";

interface Props {
  idDoPontoDeApoio: string;
  ativo: boolean;
  onConcluido: () => void;
  onIrParaTransferencia: () => void;
}

// Desativar e reativar exigem motivo, e a recusa por aula futura ou por
// saldo remanescente é traduzida em linguagem simples, com o caminho da
// transferência oferecido só na recusa por saldo (`RF-07-47`, `RN-07-01`,
// `RN-07-15`, `RN-02-21`).
export function MudarSituacaoDoPontoDeApoio({
  idDoPontoDeApoio,
  ativo,
  onConcluido,
  onIrParaTransferencia,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [aberto, definirAberto] = useState(false);
  const [motivo, definirMotivo] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<string | null>(null);
  const [recusa, definirRecusa] = useState<{
    mensagem: string;
    ofereceTransferencia: boolean;
  } | null>(null);
  const [enviando, definirEnviando] = useState(false);

  const rotuloDaAcao = ativo ? "Desativar" : "Reativar";

  if (!aberto) {
    return (
      <Botao variante="secundaria" onClick={() => definirAberto(true)}>
        {rotuloDaAcao}
      </Botao>
    );
  }

  async function confirmar() {
    if (!motivo.trim()) {
      definirErroDeCampo("Informe o motivo.");
      return;
    }
    if (!sessao) return;

    definirErroDeCampo(null);
    definirRecusa(null);
    definirEnviando(true);
    try {
      const mudar = ativo ? desativarPontoDeApoio : reativarPontoDeApoio;
      await mudar(idDoPontoDeApoio, motivo, sessao.token);
      definirAberto(false);
      definirMotivo("");
      onConcluido();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.campo === "aulas_futuras") {
        definirRecusa({ mensagem: erro.message, ofereceTransferencia: false });
        return;
      }
      if (erro instanceof ErroDaApi && erro.campo === "saldo") {
        definirRecusa({ mensagem: erro.message, ofereceTransferencia: true });
        return;
      }
      if (erro instanceof ErroDaApi && erro.campo === "motivo") {
        definirErroDeCampo(erro.message);
        return;
      }
      definirRecusa({
        mensagem: `Não foi possível ${rotuloDaAcao.toLowerCase()} o ponto de apoio. Tente novamente em instantes.`,
        ofereceTransferencia: false,
      });
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <div className="mudar-situacao-do-ponto-de-apoio">
      <Campo rotulo="Motivo" valor={motivo} aoAlterar={definirMotivo} erro={erroDeCampo} />

      {recusa && <Aviso tipo="erro">{recusa.mensagem}</Aviso>}
      {recusa?.ofereceTransferencia && (
        <Botao variante="secundaria" onClick={onIrParaTransferencia}>
          Transferir saldo para outro ponto de apoio
        </Botao>
      )}

      <Botao onClick={confirmar} desabilitado={enviando}>
        Confirmar {rotuloDaAcao.toLowerCase()}
      </Botao>
      <Botao variante="secundaria" onClick={() => definirAberto(false)}>
        Voltar
      </Botao>
    </div>
  );
}
