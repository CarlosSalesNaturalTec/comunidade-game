import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import { type SolicitacaoDoResponsavel, tratarSolicitacaoDoResponsavel } from "./api";

interface Props {
  solicitacao: SolicitacaoDoResponsavel;
  onFechar: () => void;
  onTratada: (solicitacao: SolicitacaoDoResponsavel) => void;
}

const ROTULO_DO_TIPO: Record<SolicitacaoDoResponsavel["tipo"], string> = {
  acesso: "Acesso",
  correcao: "Correção",
  exclusao: "Exclusão",
  esclarecimento: "Esclarecimento",
};

function formatarData(valorComFuso: string): string {
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return valorComFuso;
  return data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

// O desfecho é só o registro do tratamento — nenhum caminho daqui apaga,
// despersonaliza ou altera dado do Guerreiro(a): a execução do pedido de
// exclusão é da App 07, fora do escopo desta tela (`RF-02-24`, `RN-13-12`,
// `RN-13-22`).
export function TratamentoDaSolicitacaoDoResponsavel({
  solicitacao,
  onFechar,
  onTratada,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoDesfecho = useId();

  const [desfecho, definirDesfecho] = useState("");
  const [erroDeDesfecho, definirErroDeDesfecho] = useState<string | null>(null);
  const [erroDeEnvio, definirErroDeEnvio] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState<"aceita" | "recusada" | null>(null);

  const jaTratada = solicitacao.tratado_em !== null;

  async function tratar(situacao: "aceita" | "recusada") {
    definirErroDeDesfecho(null);
    definirErroDeEnvio(null);

    if (!desfecho.trim()) {
      definirErroDeDesfecho("Informe o texto do que foi tratado.");
      return;
    }
    if (!sessao) return;

    definirEnviando(situacao);
    try {
      const atualizada = await tratarSolicitacaoDoResponsavel(
        solicitacao.id,
        { situacao, desfecho },
        sessao.token,
      );
      onTratada(atualizada);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "solicitacao_ja_avaliada") {
        definirErroDeEnvio("Esta solicitação já tem um desfecho gravado.");
        return;
      }
      definirErroDeEnvio(
        "Não foi possível registrar o desfecho. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(null);
    }
  }

  function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    tratar("aceita");
  }

  return (
    <div>
      <Botao variante="secundaria" onClick={onFechar}>
        Voltar para a fila
      </Botao>

      <dl>
        <dt>Tipo</dt>
        <dd>{ROTULO_DO_TIPO[solicitacao.tipo]}</dd>
        <dt>Pedido</dt>
        <dd>{solicitacao.texto}</dd>
      </dl>

      {jaTratada ? (
        <dl>
          <dt>Desfecho</dt>
          <dd>{solicitacao.situacao === "aceita" ? "Aceita" : "Recusada"}</dd>
          <dt>O que foi tratado</dt>
          <dd>{solicitacao.desfecho ?? "—"}</dd>
          <dt>Tratada por</dt>
          <dd>{solicitacao.tratado_por_id}</dd>
          <dt>Tratada em</dt>
          <dd>{solicitacao.tratado_em && formatarData(solicitacao.tratado_em)}</dd>
        </dl>
      ) : (
        <form onSubmit={aoSubmeter} aria-label="Tratar solicitação do responsável">
          <div className="cg-campo">
            <label htmlFor={idDoDesfecho}>O que foi tratado</label>
            <textarea
              id={idDoDesfecho}
              value={desfecho}
              onChange={(evento) => definirDesfecho(evento.target.value)}
              aria-invalid={Boolean(erroDeDesfecho) || undefined}
            />
            {erroDeDesfecho && (
              <p role="alert" className="cg-campo__erro">
                {erroDeDesfecho}
              </p>
            )}
          </div>

          {erroDeEnvio && <Aviso tipo="erro">{erroDeEnvio}</Aviso>}

          <Botao tipo="submit" desabilitado={enviando !== null}>
            Aceitar
          </Botao>
          <Botao
            variante="secundaria"
            desabilitado={enviando !== null}
            onClick={() => tratar("recusada")}
          >
            Recusar
          </Botao>
        </form>
      )}
    </div>
  );
}
