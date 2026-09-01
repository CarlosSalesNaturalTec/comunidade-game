import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { type FormEvent, useCallback, useEffect, useId, useState } from "react";
import type { GuerreiroVinculado } from "../vinculados/api";
import {
  abrirSolicitacao,
  listarMinhasSolicitacoes,
  type MinhaSolicitacao,
  type SituacaoDaSolicitacao,
  type TipoDeSolicitacao,
} from "./api";

interface Props {
  guerreiro: GuerreiroVinculado;
}

const ROTULO_DO_TIPO: Record<TipoDeSolicitacao, string> = {
  acesso: "Acesso aos dados",
  correcao: "Correção de dados",
  exclusao: "Exclusão de dados",
  esclarecimento: "Esclarecimento",
};

const ROTULO_DA_SITUACAO: Record<SituacaoDaSolicitacao, string> = {
  recebida: "Recebida",
  em_avaliacao: "Em avaliação",
  aceita: "Aceita",
  recusada: "Recusada",
};

const CODIGO_DE_DUPLICATA = "solicitacao_do_responsavel_duplicada";

const FORMATADOR_DE_DATA = new Intl.DateTimeFormat("pt-BR", { dateStyle: "short" });

function formatarData(momentoISO: string): string {
  return FORMATADOR_DE_DATA.format(new Date(momentoISO));
}

// Abertura nos quatro tipos sobre o vinculado escolhido, com o limite da
// exclusão declarado antes do aceite, e o acompanhamento das próprias com o
// atraso vindo do núcleo (`RF-13-22` a `RF-13-26`, `RN-13-12` a `RN-13-14`,
// `RN-13-22`).
export function TelaDeSolicitacoes({ guerreiro }: Props) {
  const { sessao } = useSessao();
  const idDoTexto = useId();
  const [tipo, definirTipo] = useState<TipoDeSolicitacao>("acesso");
  const [texto, definirTexto] = useState("");
  const [enviando, definirEnviando] = useState(false);
  const [confirmacao, definirConfirmacao] = useState<{ id: string; prazo: string } | null>(
    null,
  );
  const [erroDeEnvio, definirErroDeEnvio] = useState<string | null>(null);

  const [solicitacoes, definirSolicitacoes] = useState<MinhaSolicitacao[] | null>(null);
  const [erroDaLista, definirErroDaLista] = useState<string | null>(null);

  const carregarLista = useCallback(() => {
    if (!sessao) return;
    return listarMinhasSolicitacoes(sessao.token)
      .then(definirSolicitacoes)
      .catch(() => definirErroDaLista("Não foi possível carregar suas solicitações."));
  }, [sessao]);

  useEffect(() => {
    definirSolicitacoes(null);
    definirErroDaLista(null);
    definirConfirmacao(null);
    definirErroDeEnvio(null);
    definirTexto("");
    carregarLista();
  }, [carregarLista]);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    if (!sessao || !texto.trim()) return;

    definirEnviando(true);
    definirErroDeEnvio(null);
    definirConfirmacao(null);
    try {
      const resposta = await abrirSolicitacao(guerreiro.id, tipo, texto, sessao.token);
      definirConfirmacao({ id: resposta.id, prazo: resposta.prazo });
      definirTexto("");
      await carregarLista();
    } catch (erroCapturado) {
      if (erroCapturado instanceof ErroDaApi && erroCapturado.codigo === CODIGO_DE_DUPLICATA) {
        definirErroDeEnvio(
          `Já existe uma solicitação de ${ROTULO_DO_TIPO[tipo].toLowerCase()} em aberto ` +
            `para ${guerreiro.nick}. Acompanhe-a na lista abaixo.`,
        );
        return;
      }
      definirErroDeEnvio("Não foi possível registrar a solicitação. Tente novamente.");
    } finally {
      definirEnviando(false);
    }
  }

  const minhasDoVinculado = (solicitacoes ?? []).filter(
    (item) => item.guerreiro_id === guerreiro.id,
  );

  return (
    <section aria-label={`Solicitações de ${guerreiro.nick}`}>
      <section>
        <h2>Nova solicitação</h2>
        <form onSubmit={aoSubmeter} aria-label="Abrir solicitação">
          <div className="cg-campo">
            <label htmlFor="tipo-da-solicitacao">Tipo</label>
            <select
              id="tipo-da-solicitacao"
              value={tipo}
              onChange={(evento) => definirTipo(evento.target.value as TipoDeSolicitacao)}
            >
              <option value="acesso">{ROTULO_DO_TIPO.acesso}</option>
              <option value="correcao">{ROTULO_DO_TIPO.correcao}</option>
              <option value="exclusao">{ROTULO_DO_TIPO.exclusao}</option>
              <option value="esclarecimento">{ROTULO_DO_TIPO.esclarecimento}</option>
            </select>
          </div>

          {tipo === "exclusao" && (
            <Aviso tipo="atencao">
              O registro de dado do território é despersonalizado, não apagado: o vínculo de
              autoria é rompido e o mapeamento destruído, e a medição permanece na série sem
              apontar pessoa alguma. O <em>template</em> biométrico é a exceção — esse é
              apagado.
            </Aviso>
          )}

          <div className="cg-campo">
            <label htmlFor={idDoTexto}>Descreva o pedido</label>
            <textarea
              id={idDoTexto}
              value={texto}
              onChange={(evento) => definirTexto(evento.target.value)}
            />
          </div>

          <Botao tipo="submit" desabilitado={enviando || !texto.trim()}>
            Enviar solicitação
          </Botao>
        </form>

        {confirmacao && (
          <Aviso tipo="sucesso">
            Solicitação registrada — protocolo {confirmacao.id}, prazo de resposta em{" "}
            {formatarData(confirmacao.prazo)}.
          </Aviso>
        )}
        {erroDeEnvio && <Aviso tipo="erro">{erroDeEnvio}</Aviso>}
      </section>

      <section>
        <h2>Minhas solicitações</h2>
        {erroDaLista && <Aviso tipo="erro">{erroDaLista}</Aviso>}
        {!erroDaLista && solicitacoes === null && <EstadoDaLista>Carregando…</EstadoDaLista>}
        {!erroDaLista && solicitacoes !== null && minhasDoVinculado.length === 0 && (
          <EstadoDaLista>Nenhuma solicitação ainda para {guerreiro.nick}.</EstadoDaLista>
        )}
        {!erroDaLista && minhasDoVinculado.length > 0 && (
          <ul aria-label={`Solicitações de ${guerreiro.nick}`}>
            {minhasDoVinculado.map((item) => (
              <li key={item.id}>
                {ROTULO_DO_TIPO[item.tipo]} — protocolo {item.id} —{" "}
                {ROTULO_DA_SITUACAO[item.situacao]}
                {item.em_atraso && (
                  <>
                    {" "}
                    <strong>Em atraso</strong>
                  </>
                )}{" "}
                — prazo {formatarData(item.prazo)}
                {item.tratado_em && (
                  <>
                    {" "}
                    — desfecho em {formatarData(item.tratado_em)}: {item.desfecho}
                  </>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>
    </section>
  );
}
