import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import { avaliarSolicitacaoDeDados, type SolicitacaoDeDados } from "./api";

interface Props {
  solicitacao: SolicitacaoDeDados;
  onFechar: () => void;
  onAvaliado: (solicitacao: SolicitacaoDeDados) => void;
}

// Os três critérios de aprovação aparecem antes da decisão, e o
// compromisso de não reidentificação é exigido no próprio campo — quem
// garante é a regra do núcleo, a tela só transporta (design — decisão 2,
// `RF-02-93`, `RF-02-78`). O que foi entregue só se aplica à aprovação
// (`RF-02-79`).
export function AvaliacaoDeDados({ solicitacao, onFechar, onAvaliado }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoParecer = useId();
  const idDoCompromisso = useId();
  const idDoEntregue = useId();

  const [parecer, definirParecer] = useState("");
  const [compromisso, definirCompromisso] = useState(false);
  const [entregue, definirEntregue] = useState("");
  const [erroDeParecer, definirErroDeParecer] = useState<string | null>(null);
  const [erroDeCompromisso, definirErroDeCompromisso] = useState<string | null>(null);
  const [erroDeEnvio, definirErroDeEnvio] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState<"aceita" | "recusada" | null>(null);

  const jaAvaliada = solicitacao.decidido_em !== null;

  async function avaliar(situacao: "aceita" | "recusada") {
    definirErroDeParecer(null);
    definirErroDeCompromisso(null);
    definirErroDeEnvio(null);

    if (!parecer.trim()) {
      definirErroDeParecer("Informe o parecer.");
      return;
    }
    if (situacao === "aceita" && !compromisso) {
      definirErroDeCompromisso(
        "Afirme o compromisso de não tentar reidentificar ninguém para aprovar.",
      );
      return;
    }
    if (!sessao) return;

    definirEnviando(situacao);
    try {
      const atualizada = await avaliarSolicitacaoDeDados(
        solicitacao.id,
        {
          situacao,
          parecer,
          compromisso_de_nao_reidentificar: situacao === "aceita" ? compromisso : undefined,
          entregue: situacao === "aceita" && entregue.trim() ? entregue : undefined,
        },
        sessao.token,
      );
      onAvaliado(atualizada);
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
    avaliar("aceita");
  }

  return (
    <div>
      <Botao variante="secundaria" onClick={onFechar}>
        Voltar para a fila
      </Botao>

      <dl>
        <dt>Solicitante</dt>
        <dd>{solicitacao.solicitante}</dd>
        <dt>Instituição</dt>
        <dd>{solicitacao.instituicao}</dd>
        <dt>Finalidade declarada</dt>
        <dd>{solicitacao.finalidade_declarada}</dd>
        <dt>Recorte pedido</dt>
        <dd>{solicitacao.recorte_pedido}</dd>
      </dl>

      {jaAvaliada ? (
        <dl>
          <dt>Desfecho</dt>
          <dd>{solicitacao.situacao === "aceita" ? "Aceita" : "Recusada"}</dd>
          <dt>Parecer</dt>
          <dd>{solicitacao.parecer ?? "—"}</dd>
          {solicitacao.situacao === "aceita" && solicitacao.entregue && (
            <>
              <dt>Entrega</dt>
              <dd>{solicitacao.entregue} — entrega gratuita e anonimizada.</dd>
            </>
          )}
        </dl>
      ) : (
        <form onSubmit={aoSubmeter} aria-label="Avaliar solicitação de dados">
          <h3>Critérios de aprovação</h3>
          <ul>
            <li>Solicitante identificado</li>
            <li>Finalidade declarada compatível com pesquisa ou política pública</li>
            <li>Compromisso de não tentar reidentificar ninguém</li>
          </ul>

          <div className="cg-campo">
            <label htmlFor={idDoParecer}>Parecer</label>
            <textarea
              id={idDoParecer}
              value={parecer}
              onChange={(evento) => definirParecer(evento.target.value)}
              aria-invalid={Boolean(erroDeParecer) || undefined}
            />
            {erroDeParecer && (
              <p role="alert" className="cg-campo__erro">
                {erroDeParecer}
              </p>
            )}
          </div>

          <div className="cg-campo">
            <label htmlFor={idDoCompromisso}>
              <input
                id={idDoCompromisso}
                type="checkbox"
                checked={compromisso}
                onChange={(evento) => definirCompromisso(evento.target.checked)}
              />{" "}
              Afirmo o compromisso de não tentar reidentificar ninguém
            </label>
            {erroDeCompromisso && (
              <p role="alert" className="cg-campo__erro">
                {erroDeCompromisso}
              </p>
            )}
          </div>

          <div className="cg-campo">
            <label htmlFor={idDoEntregue}>O que foi entregue e a quem (se aprovada)</label>
            <textarea
              id={idDoEntregue}
              value={entregue}
              onChange={(evento) => definirEntregue(evento.target.value)}
            />
          </div>

          {erroDeEnvio && <Aviso tipo="erro">{erroDeEnvio}</Aviso>}

          <Botao tipo="submit" desabilitado={enviando !== null}>
            Aceitar
          </Botao>
          <Botao
            variante="secundaria"
            desabilitado={enviando !== null}
            onClick={() => avaliar("recusada")}
          >
            Recusar
          </Botao>
        </form>
      )}
    </div>
  );
}
