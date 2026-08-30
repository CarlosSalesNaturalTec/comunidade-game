import { ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { useState } from "react";
import { duplicarTrilha, type TrilhaDaLista } from "./api";

interface Props {
  idDaTrilha: string;
  onDuplicada: (copia: TrilhaDaLista) => void;
}

// Confirmação em dois passos, no molde de `DesativarPoder`: a cópia nasce
// em rascunho, traz missões e atividades da origem e não traz percurso de
// Guerreiro(a) algum — a origem nunca é alterada (`RF-09-13`, `RN-09-05`).
export function DuplicarTrilha({ idDaTrilha, onDuplicada }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [confirmando, definirConfirmando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  if (!confirmando) {
    return (
      <Botao variante="secundaria" onClick={() => definirConfirmando(true)}>
        Duplicar
      </Botao>
    );
  }

  async function confirmar() {
    if (!sessao) return;
    definirErro(null);
    definirEnviando(true);
    try {
      const copia = await duplicarTrilha(idDaTrilha, sessao.token);
      definirConfirmando(false);
      onDuplicada(copia);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível duplicar a trilha. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <div>
      <Aviso tipo="atencao">
        A cópia nasce em rascunho, sob a sua autoria, trazendo as missões e as atividades da
        origem. Ela não traz inscrição, desbloqueio, resultado nem recompensa de nenhum
        Guerreiro(a). A trilha de origem não é alterada.
      </Aviso>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <Botao onClick={confirmar} desabilitado={enviando}>
        Confirmar duplicação
      </Botao>
      <Botao variante="secundaria" onClick={() => definirConfirmando(false)}>
        Voltar
      </Botao>
    </div>
  );
}
