import { ErroDaApi } from "comum/api";
import { useSessao } from "comum/autenticacao";
import { Aviso, Botao, EstadoDaLista } from "comum/react";
import { type FormEvent, useCallback, useEffect, useId, useState } from "react";
import { AvisoDeColeta } from "../direitos/AvisoDeColeta";
import { listarMinhasPropostas, type PropostaDoAutor, registrarProposta } from "./api";

const ROTULO_DA_SITUACAO: Record<PropostaDoAutor["situacao"], string> = {
  recebida: "Recebida",
  em_avaliacao: "Em avaliação",
  adotada: "Adotada",
  nao_adotada: "Não adotada",
};

// A proposta de evolução da plataforma, na fila única da gestão — em
// texto, com o status até o retorno e o motivo em linguagem simples
// quando não adotada; nunca promete e-mail, ponto ou badge, porque a
// pontuação é da criança (`RF-13-39`, `RF-13-40`, `RN-13-15`, `RN-13-18`).
export function TelaDePropostas() {
  const { sessao } = useSessao();
  const idDoTexto = useId();
  const [propostas, definirPropostas] = useState<PropostaDoAutor[] | null>(null);
  const [texto, definirTexto] = useState("");
  const [enviando, definirEnviando] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);

  const carregar = useCallback(() => {
    if (!sessao) return;
    return listarMinhasPropostas(sessao.token)
      .then(definirPropostas)
      .catch(() => definirErro("Não foi possível carregar as suas propostas."));
  }, [sessao]);

  useEffect(() => {
    carregar();
  }, [carregar]);

  async function aoSubmeter(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    if (!sessao || !texto.trim()) return;

    definirEnviando(true);
    definirErro(null);
    try {
      await registrarProposta(texto, sessao.token);
      definirTexto("");
      await carregar();
    } catch (erroCapturado) {
      definirErro(
        erroCapturado instanceof ErroDaApi
          ? erroCapturado.message
          : "Não foi possível registrar a proposta. Tente novamente.",
      );
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <section aria-label="Propostas de evolução">
      <AvisoDeColeta dado="o texto da sua proposta de evolução da plataforma" />

      <section>
        <h2>Nova proposta</h2>
        <form onSubmit={aoSubmeter} aria-label="Registrar proposta">
          <div className="cg-campo">
            <label htmlFor={idDoTexto}>Proposta</label>
            <textarea
              id={idDoTexto}
              value={texto}
              onChange={(evento) => definirTexto(evento.target.value)}
            />
          </div>
          <Botao tipo="submit" desabilitado={enviando || !texto.trim()}>
            Enviar proposta
          </Botao>
        </form>
        {erro && <Aviso tipo="erro">{erro}</Aviso>}
      </section>

      <section>
        <h2>Minhas propostas</h2>
        {propostas === null && <EstadoDaLista>Carregando…</EstadoDaLista>}
        {propostas !== null && propostas.length === 0 && (
          <EstadoDaLista>Nenhuma proposta registrada ainda.</EstadoDaLista>
        )}
        {propostas !== null && propostas.length > 0 && (
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
      </section>
    </section>
  );
}
