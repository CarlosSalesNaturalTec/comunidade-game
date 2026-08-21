import { Botao, Campo } from "comum/react";
import { type FormEvent, useState } from "react";
import { ErroDaApi, ehRecusaDeSessao } from "../api/cliente";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { gravarNickDoAdulto } from "./api";

interface Props {
  personaId: string;
  onGravado: () => void;
  onCancelar: () => void;
}

// O desfecho da colisão: o Admin grava aqui o nick que a pessoa lhe passou
// por fora da plataforma. NEVER sugere nick algum — quem escolhe é sempre
// quem o usa (`RF-02-01`, `RN-01-30`, `RN-14-10`, design — decisões).
export function FormularioDeNick({ personaId, onGravado, onCancelar }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [nick, definirNick] = useState("");
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErro(null);

    if (!nick.trim()) {
      definirErro("Informe o nick que a pessoa passou.");
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      await gravarNickDoAdulto(personaId, nick, sessao.token);
      onGravado();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === "erro_de_validacao") {
        // Não revela de quem é o nick em uso (`RN-01-30`).
        definirErro("Este nick já está em uso. Peça outro à pessoa.");
        return;
      }
      definirErro("Não foi possível gravar o nick. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <form onSubmit={aoSubmeter} aria-label="Gravar nick">
      <Campo
        rotulo="Nick recebido por fora"
        valor={nick}
        aoAlterar={definirNick}
        erro={erro}
      />
      <Botao tipo="submit" desabilitado={enviando}>
        Gravar
      </Botao>
      <Botao variante="secundaria" onClick={onCancelar}>
        Cancelar
      </Botao>
    </form>
  );
}
