import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Botao, Campo } from "comum/react";
import { useState } from "react";
import { revogarChave } from "./api";

interface Props {
  idDaChave: string;
  onRevogada: () => void;
}

// Revoga a qualquer tempo, com motivo exigido no próprio campo antes de
// chamar o núcleo (`RF-02-92`), no molde de `MudarSituacaoDoPontoDeApoio`.
export function RevogarChave({ idDaChave, onRevogada }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [aberto, definirAberto] = useState(false);
  const [motivo, definirMotivo] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  if (!aberto) {
    return (
      <Botao variante="secundaria" onClick={() => definirAberto(true)}>
        Revogar
      </Botao>
    );
  }

  async function confirmar() {
    if (!motivo.trim()) {
      definirErroDeCampo("Informe o motivo da revogação.");
      return;
    }
    if (!sessao) return;

    definirErroDeCampo(null);
    definirEnviando(true);
    try {
      await revogarChave(idDaChave, motivo, sessao.token);
      definirAberto(false);
      definirMotivo("");
      onRevogada();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDeCampo("Não foi possível revogar a chave. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <div>
      <Campo rotulo="Motivo" valor={motivo} aoAlterar={definirMotivo} erro={erroDeCampo} />
      <Botao onClick={confirmar} desabilitado={enviando}>
        Confirmar revogação
      </Botao>
      <Botao variante="secundaria" onClick={() => definirAberto(false)}>
        Voltar
      </Botao>
    </div>
  );
}
