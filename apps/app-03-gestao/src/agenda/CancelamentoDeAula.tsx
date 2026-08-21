import { Aviso, Botao, Campo } from "comum/react";
import { useState } from "react";

interface Props {
  onConfirmar: (motivo: string) => Promise<void>;
}

// Motivo obrigatório e aviso, antes de confirmar, de que a operação libera
// os recursos reservados e não se desfaz (`RF-02-95`, `RF-01-72`).
export function CancelamentoDeAula({ onConfirmar }: Props) {
  const [aberto, definirAberto] = useState(false);
  const [motivo, definirMotivo] = useState("");
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  if (!aberto) {
    return (
      <Botao variante="secundaria" onClick={() => definirAberto(true)}>
        Cancelar aula
      </Botao>
    );
  }

  async function confirmar() {
    if (!motivo.trim()) {
      definirErro("Informe o motivo do cancelamento.");
      return;
    }
    definirErro(null);
    definirEnviando(true);
    try {
      await onConfirmar(motivo);
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <div className="lista-da-agenda__cancelamento">
      <Aviso tipo="atencao">
        Cancelar libera os recursos reservados desta aula e não pode ser desfeito.
      </Aviso>
      <Campo
        rotulo="Motivo do cancelamento"
        valor={motivo}
        aoAlterar={definirMotivo}
        erro={erro}
      />
      <Botao onClick={confirmar} desabilitado={enviando}>
        Confirmar cancelamento
      </Botao>
      <Botao variante="secundaria" onClick={() => definirAberto(false)}>
        Voltar
      </Botao>
    </div>
  );
}
