import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { useState } from "react";
import { desativarPoder } from "./api";

interface Props {
  idDoPoder: string;
  onDesativado: () => void;
}

const RECUSA_POR_PAPEL = "Só o Admin desativa poder do catálogo.";

// Confirmação em dois passos, no molde de `RevogarChave` — sem motivo, que
// `desativar_poder` não exige. Retira o poder da escolha de novas trilhas
// sem desfazer o vínculo das trilhas já criadas (`RF-02-10`, `RF-01-62`).
export function DesativarPoder({ idDoPoder, onDesativado }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [confirmando, definirConfirmando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  if (!confirmando) {
    return (
      <Botao variante="secundaria" onClick={() => definirConfirmando(true)}>
        Desativar
      </Botao>
    );
  }

  async function confirmar() {
    if (!sessao) return;

    definirErro(null);
    definirEnviando(true);
    try {
      await desativarPoder(idDoPoder, sessao.token);
      definirConfirmando(false);
      onDesativado();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === "permissao_negada") {
        definirErro(RECUSA_POR_PAPEL);
        return;
      }
      definirErro("Não foi possível desativar o poder. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <div>
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      <Botao onClick={confirmar} desabilitado={enviando}>
        Confirmar desativação
      </Botao>
      <Botao variante="secundaria" onClick={() => definirConfirmando(false)}>
        Voltar
      </Botao>
    </div>
  );
}
