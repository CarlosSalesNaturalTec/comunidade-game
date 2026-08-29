import { ErroDaApi, ehRecusaDeSessao } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { type FormEvent, useCallback, useEffect, useId, useState } from "react";
import {
  listarMinhasPropostas,
  type PropostaDoAutor,
  registrarProposta,
  type SituacaoDaProposta,
} from "./api";

const ROTULO_DA_SITUACAO: Record<SituacaoDaProposta, string> = {
  recebida: "Recebida",
  em_avaliacao: "Em avaliação",
  adotada: "Adotada",
  nao_adotada: "Não adotada",
};

// A proposta de evolução da plataforma, na fila única da gestão — em texto,
// sem áudio, e sem ação de avaliar: a avaliação é ato de Admin, na App 03
// (`RF-09-55`, `RN-09-23`, PRD-09 §3.2). O retorno chega dentro da própria
// aplicação; nenhum e-mail é construído aqui.
export function TelaDePropostas() {
  const { sessao, sair, tratarRecusaDeSessao } = useSessao();
  const idDoTexto = useId();
  const [propostas, definirPropostas] = useState<PropostaDoAutor[] | null>(null);
  const [texto, definirTexto] = useState("");
  const [erroDeCampo, definirErroDeCampo] = useState<string | null>(null);
  const [erroDeRecusa, definirErroDeRecusa] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);

  const carregar = useCallback(async () => {
    if (!sessao) return;
    try {
      const lista = await listarMinhasPropostas(sessao.token);
      definirPropostas(lista);
    } catch (erroCapturado) {
      if (ehRecusaDeSessao(erroCapturado)) {
        tratarRecusaDeSessao();
        return;
      }
      definirErroDeRecusa("Não foi possível carregar as suas propostas. Tente novamente.");
    }
  }, [sessao, tratarRecusaDeSessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    definirErroDeCampo(null);
    definirErroDeRecusa(null);

    if (!texto.trim()) {
      definirErroDeCampo("Escreva a proposta antes de enviar.");
      return;
    }
    if (!sessao) return;

    definirEnviando(true);
    try {
      await registrarProposta(texto, sessao.token);
      definirTexto("");
      await carregar();
    } catch (erro) {
      if (ehRecusaDeSessao(erro)) {
        tratarRecusaDeSessao();
        return;
      }
      if (erro instanceof ErroDaApi) {
        definirErroDeRecusa(erro.message);
        return;
      }
      definirErroDeRecusa(
        "Não foi possível registrar a proposta. Tente novamente em instantes.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <Moldura>
      <Cabecalho titulo="Propostas de evolução" acao={{ rotulo: "Sair", aoAcionar: sair }} />

      <form onSubmit={aoSubmeter} aria-label="Nova proposta de evolução">
        <div className="cg-campo">
          <label htmlFor={idDoTexto}>Proposta</label>
          <textarea
            id={idDoTexto}
            value={texto}
            onChange={(evento) => definirTexto(evento.target.value)}
            aria-invalid={Boolean(erroDeCampo) || undefined}
          />
          {erroDeCampo && (
            <p role="alert" className="cg-campo__erro">
              {erroDeCampo}
            </p>
          )}
        </div>

        {erroDeRecusa && <Aviso tipo="erro">{erroDeRecusa}</Aviso>}

        <Botao tipo="submit" desabilitado={enviando}>
          Enviar proposta
        </Botao>
      </form>

      <h2>Minhas propostas</h2>
      {propostas === null ? (
        <EstadoDaLista>Carregando as suas propostas…</EstadoDaLista>
      ) : propostas.length === 0 ? (
        <EstadoDaLista>Nenhuma proposta registrada ainda.</EstadoDaLista>
      ) : (
        <ul aria-label="Minhas propostas">
          {propostas.map((proposta) => (
            <li key={proposta.id}>
              <p>{proposta.texto}</p>
              <p>
                {ROTULO_DA_SITUACAO[proposta.situacao]}
                {proposta.em_atraso && proposta.decidido_em === null && " · Em atraso"}
              </p>
              {proposta.situacao === "nao_adotada" && proposta.motivo_do_retorno && (
                <p>Motivo do retorno: {proposta.motivo_do_retorno}</p>
              )}
            </li>
          ))}
        </ul>
      )}
    </Moldura>
  );
}
