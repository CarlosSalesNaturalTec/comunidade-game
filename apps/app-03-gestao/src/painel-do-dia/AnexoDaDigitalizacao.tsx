import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso } from "comum/react";
import { type ChangeEvent, useId, useState } from "react";
import { anexarDigitalizacaoDoTermo } from "./api";

interface Props {
  consentimentoId: string;
  token: string;
  aoAnexar: () => void;
}

const MENSAGEM_DE_FORMATO_RECUSADO = "Envie a digitalização em PDF, JPG ou PNG.";

const MENSAGEM_DE_FALHA = "Não foi possível anexar a digitalização. Tente novamente.";

// O caminho de anexar a partir da pendência, restrito ao Admin pelo pai
// (`RF-02-68`, `RN-02-20`): a recusa de formato aparece em linguagem
// simples, sem jargão de TI.
export function AnexoDaDigitalizacao({ consentimentoId, token, aoAnexar }: Props) {
  const { tratarRecusaDeSessao } = useSessao();
  const idDoCampo = useId();
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [anexado, definirAnexado] = useState(false);

  async function aoEscolherArquivo(evento: ChangeEvent<HTMLInputElement>) {
    const arquivo = evento.target.files?.[0];
    evento.target.value = "";
    if (!arquivo) return;

    definirErro(null);
    definirEnviando(true);
    try {
      await anexarDigitalizacaoDoTermo(consentimentoId, arquivo, token);
      definirAnexado(true);
      aoAnexar();
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === "erro_de_validacao") {
        definirErro(MENSAGEM_DE_FORMATO_RECUSADO);
      } else {
        definirErro(MENSAGEM_DE_FALHA);
      }
    } finally {
      definirEnviando(false);
    }
  }

  if (anexado) {
    return <Aviso tipo="sucesso">Digitalização anexada.</Aviso>;
  }

  return (
    <div className="cg-campo">
      <label htmlFor={idDoCampo}>Anexar digitalização do termo</label>
      <input
        id={idDoCampo}
        type="file"
        accept="application/pdf,image/jpeg,image/png"
        onChange={aoEscolherArquivo}
        disabled={enviando}
      />
      {enviando && <p role="status">Enviando…</p>}
      {erro && <Aviso tipo="erro">{erro}</Aviso>}
    </div>
  );
}
