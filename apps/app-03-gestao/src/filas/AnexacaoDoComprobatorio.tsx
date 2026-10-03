import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { useState } from "react";
import { anexarComprobatorio, type ComprobatorioPendente } from "../personas/api";

interface Props {
  pendente: ComprobatorioPendente;
  onAnexado: () => void;
}

// O ato do Admin aqui é anexar, e nada mais: a fila NUNCA oferece edição do
// endereço nem do rótulo que o Apoiador declarou — isso é da tela de
// artefatos do cadastro (`RF-02-101`, design — Non-Goals).
export function AnexacaoDoComprobatorio({ pendente, onAnexado }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  async function anexar() {
    if (!sessao) return;
    definirErro(null);
    definirEnviando(true);
    try {
      await anexarComprobatorio(pendente.apoiador_id, pendente.artefato_id, sessao.token);
      onAnexado();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      // A recusa que o núcleo declarou vira a frase do domínio, como ela
      // chegou no corpo único de erro; falha de camada aparece como o que é
      // (invariante 25 do documento 99 §6, `RF-14-19`).
      if (erroCapturado instanceof ErroDaApi) {
        definirErro(erroCapturado.message);
        return;
      }
      definirErro("Não foi possível anexar o documento. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <div>
      <p>
        {pendente.apoiador} — {pendente.rotulo}
      </p>
      <p>
        <a href={pendente.endereco} target="_blank" rel="noreferrer">
          {pendente.endereco}
        </a>
      </p>

      {erro && <Aviso tipo="erro">{erro}</Aviso>}

      <Botao onClick={anexar} desabilitado={enviando}>
        Anexar ao cadastro
      </Botao>
    </div>
  );
}
