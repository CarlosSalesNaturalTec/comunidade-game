import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Campo } from "comum/react";
import { useState } from "react";
import { type LancamentoDoExtrato, lancarAjuste } from "./api";

interface Props {
  lancamento: LancamentoDoExtrato;
  onAjustado: () => void;
}

// A correção se faz por lançamento novo, que referencia o original sem
// alterá-lo — não há caminho de edição nem de remoção (`RF-02-40`,
// `RN-02-12`).
export function AjusteDeLancamento({ lancamento, onAjustado }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [aberto, definirAberto] = useState(false);
  const [quantidade, definirQuantidade] = useState("");
  const [valorEmMoedas, definirValorEmMoedas] = useState("");
  const [motivo, definirMotivo] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<{
    campo: string;
    mensagem: string;
  } | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  if (!aberto) {
    return (
      <Botao variante="secundaria" onClick={() => definirAberto(true)}>
        Ajustar
      </Botao>
    );
  }

  async function confirmar() {
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!quantidade) {
      definirErroDeCampo({ campo: "quantidade", mensagem: "Informe a quantidade do ajuste." });
      return;
    }
    if (!valorEmMoedas) {
      definirErroDeCampo({
        campo: "moedas",
        mensagem: "Informe o valor em moedas do ajuste.",
      });
      return;
    }
    if (!motivo.trim()) {
      definirErroDeCampo({ campo: "motivo", mensagem: "Informe o motivo do ajuste." });
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      await lancarAjuste(
        lancamento.id,
        { quantidade, valor_em_moedas: valorEmMoedas, motivo },
        sessao.token,
      );
      definirAberto(false);
      definirQuantidade("");
      definirValorEmMoedas("");
      definirMotivo("");
      onAjustado();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDeRecusa(
        erro instanceof ErroDaApi
          ? erro.message
          : "Não foi possível lançar o ajuste. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <div className="cg-ajuste-de-lancamento">
      <Campo
        rotulo="Quantidade do ajuste"
        tipo="number"
        valor={quantidade}
        aoAlterar={definirQuantidade}
        erro={erroDeCampo?.campo === "quantidade" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="Valor em moedas do ajuste"
        tipo="number"
        valor={valorEmMoedas}
        aoAlterar={definirValorEmMoedas}
        erro={erroDeCampo?.campo === "moedas" ? erroDeCampo.mensagem : null}
      />
      <Campo
        rotulo="Motivo"
        valor={motivo}
        aoAlterar={definirMotivo}
        erro={erroDeCampo?.campo === "motivo" ? erroDeCampo.mensagem : null}
      />

      {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

      <Botao onClick={confirmar} desabilitado={enviando}>
        Confirmar ajuste
      </Botao>
      <Botao variante="secundaria" onClick={() => definirAberto(false)}>
        Voltar
      </Botao>
    </div>
  );
}
