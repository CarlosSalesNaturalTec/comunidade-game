import { Aviso, Botao } from "comum/react";
import { type FormEvent, useId, useState } from "react";
import { ErroDaApi, ehRecusaDeSessao } from "../api/cliente";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { emitirChave } from "../chaves/api";
import { avaliarSolicitacaoDeChave, type SolicitacaoDeChave } from "./api";

interface Props {
  solicitacao: SolicitacaoDeChave;
  onFechar: () => void;
  onAvaliado: (solicitacao: SolicitacaoDeChave) => void;
}

// Dois atos: primeiro o desfecho, depois — sobre a solicitação aceita — a
// emissão, nunca no mesmo passo (design — decisão 1, `RF-02-88`,
// `RF-02-89`). O segredo vive só na memória deste componente, nunca em
// `sessionStorage` (design — decisão 5, `RN-02-28`); sair da tela ou trocar
// de solicitação o descarta.
export function AvaliacaoDeChave({ solicitacao, onFechar, onAvaliado }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const idDoParecer = useId();

  const [parecer, definirParecer] = useState("");
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState<"aceita" | "recusada" | null>(null);
  const [emitindo, definirEmitindo] = useState(false);
  const [erroDeEmissao, definirErroDeEmissao] = useState<string | null>(null);
  const [chaveEmitida, definirChaveEmitida] = useState<{ id: string; segredo: string } | null>(
    null,
  );

  const jaAvaliada = solicitacao.decidido_em !== null;

  async function avaliar(situacao: "aceita" | "recusada") {
    definirErroDeRecusa(null);
    if (!sessao) return;

    definirEnviando(situacao);
    try {
      const atualizada = await avaliarSolicitacaoDeChave(
        solicitacao.id,
        { situacao, parecer: parecer || undefined },
        sessao.token,
      );
      onAvaliado(atualizada);
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi && erro.codigo === "solicitacao_ja_avaliada") {
        definirErroDeRecusa("Esta solicitação já tem um desfecho gravado.");
        return;
      }
      definirErroDeRecusa(
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

  async function emitir() {
    if (!sessao) return;
    definirErroDeEmissao(null);
    definirEmitindo(true);
    try {
      const emitida = await emitirChave(solicitacao.id, sessao.token);
      definirChaveEmitida(emitida);
      onAvaliado({ ...solicitacao, chave_emitida: true });
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDeEmissao("Não foi possível emitir a chave. Tente novamente em instantes.");
    } finally {
      definirEmitindo(false);
    }
  }

  const podeEmitir = solicitacao.situacao === "aceita" && !solicitacao.chave_emitida;

  return (
    <div>
      <Botao variante="secundaria" onClick={onFechar}>
        Voltar para a fila
      </Botao>

      <dl>
        <dt>Solicitante</dt>
        <dd>{solicitacao.solicitante}</dd>
        <dt>Contato</dt>
        <dd>{solicitacao.contato}</dd>
        {solicitacao.instituicao && (
          <>
            <dt>Instituição</dt>
            <dd>{solicitacao.instituicao}</dd>
          </>
        )}
        <dt>O que pretende construir</dt>
        <dd>{solicitacao.o_que_pretende_construir}</dd>
      </dl>

      {jaAvaliada ? (
        <dl>
          <dt>Desfecho</dt>
          <dd>{solicitacao.situacao === "aceita" ? "Aceita" : "Recusada"}</dd>
          <dt>Parecer</dt>
          <dd>{solicitacao.parecer ?? "—"}</dd>
        </dl>
      ) : (
        <form onSubmit={aoSubmeter} aria-label="Avaliar solicitação de chave">
          <div className="cg-campo">
            <label htmlFor={idDoParecer}>Parecer</label>
            <textarea
              id={idDoParecer}
              value={parecer}
              onChange={(evento) => definirParecer(evento.target.value)}
            />
          </div>

          {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

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

      {podeEmitir && !chaveEmitida && (
        <div>
          <Botao onClick={emitir} desabilitado={emitindo}>
            Emitir chave
          </Botao>
          {erroDeEmissao && <Aviso tipo="erro">{erroDeEmissao}</Aviso>}
        </div>
      )}

      {solicitacao.chave_emitida && !chaveEmitida && (
        <Aviso tipo="sucesso">Chave já emitida para esta solicitação.</Aviso>
      )}

      {chaveEmitida && (
        <Aviso tipo="atencao">
          Identificador: {chaveEmitida.id}. Segredo: {chaveEmitida.segredo}. Este segredo não
          será mostrado de novo — copie agora.
        </Aviso>
      )}
    </div>
  );
}
