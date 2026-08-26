import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, Moldura } from "comum/react";
import { useState } from "react";
import { encerrarCiclo } from "./api";

const RECUSA_POR_PAPEL = "Só o Admin encerra o ciclo.";

// O ato é irreversível — o motivo expurgado não volta —, por isso a
// confirmação enuncia os dois efeitos antes de executar e nunca oferece
// declarar o ciclo seguinte, que é declaração à parte na implantação
// (`RF-02-99`, `RF-02-100`, `RN-02-30`).
export function TelaDeEncerramentoDeCiclo() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const [confirmando, definirConfirmando] = useState(false);
  const [enviando, definirEnviando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [resultado, definirResultado] = useState<number | null>(null);

  const ehAdmin = sessao?.papel === "admin";

  async function confirmar() {
    if (!sessao) return;
    definirErro(null);
    definirEnviando(true);
    try {
      const ciclo = await encerrarCiclo(sessao.token);
      definirResultado(ciclo.ocorrencias_expurgadas);
      definirConfirmando(false);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === "permissao_negada") {
        definirErro(RECUSA_POR_PAPEL);
        return;
      }
      definirErro("Não foi possível encerrar o ciclo. Tente novamente em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <Moldura>
      <Cabecalho titulo="Encerramento do ciclo" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      {!ehAdmin && <Aviso tipo="atencao">{RECUSA_POR_PAPEL}</Aviso>}

      {ehAdmin && !confirmando && (
        <Botao variante="secundaria" onClick={() => definirConfirmando(true)}>
          Encerrar ciclo
        </Botao>
      )}

      {ehAdmin && confirmando && (
        <>
          <Aviso tipo="atencao">
            Encerrar o ciclo apaga o motivo de toda ocorrência de conduta do ciclo — só o
            valor, a data e o autor permanecem — e tira essas ocorrências do ranking público. O
            ciclo seguinte não é declarado aqui. Essa ação não pode ser desfeita.
          </Aviso>
          {erro && <Aviso tipo="erro">{erro}</Aviso>}
          <Botao onClick={confirmar} desabilitado={enviando}>
            {enviando ? "Encerrando…" : "Confirmar encerramento"}
          </Botao>
          <Botao variante="secundaria" onClick={() => definirConfirmando(false)}>
            Voltar
          </Botao>
        </>
      )}

      {resultado !== null && (
        <Aviso tipo="sucesso">
          Ciclo encerrado. {resultado}{" "}
          {resultado === 1 ? "ocorrência de conduta teve" : "ocorrências de conduta tiveram"} o
          motivo expurgado.
        </Aviso>
      )}
    </Moldura>
  );
}
