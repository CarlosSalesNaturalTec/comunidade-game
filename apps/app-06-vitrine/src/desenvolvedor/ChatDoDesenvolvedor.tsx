import { ErroDaApi } from "comum/api";
import { Aviso, Botao } from "comum/react";
import { useState } from "react";
import { type MensagemDaConversa, perguntarAoAssistente } from "../api/desenvolvedor";
import { MENSAGEM_DE_ABERTURA, OPCOES_DA_ABERTURA } from "./abertura";

/** Assistente de chat da Área do Apoiador Desenvolvedor (`RF-03-68` a
 * `RF-03-72`). A conversa vive **aqui**, no estado do componente: nada vai ao
 * `localStorage`, a cookie ou ao núcleo, e recarregar a página a perde inteira
 * (`RN-03-15`, `RN-03-22`, PRD-03 §8). */
export function ChatDoDesenvolvedor() {
  const [conversa, definirConversa] = useState<MensagemDaConversa[]>([MENSAGEM_DE_ABERTURA]);
  const [opcoes, definirOpcoes] = useState<readonly string[]>(OPCOES_DA_ABERTURA);
  const [pergunta, definirPergunta] = useState("");
  const [perguntando, definirPerguntando] = useState(false);
  const [indisponivel, definirIndisponivel] = useState<string | null>(null);

  async function perguntar(texto: string) {
    const limpo = texto.trim();
    if (!limpo || perguntando) return;

    const comAPergunta: MensagemDaConversa[] = [
      ...conversa,
      { de: "visitante", texto: limpo },
    ];
    definirConversa(comAPergunta);
    definirPergunta("");
    definirOpcoes([]);
    definirPerguntando(true);
    definirIndisponivel(null);

    try {
      const resposta = await perguntarAoAssistente(limpo, conversa);
      definirConversa([...comAPergunta, { de: "assistente", texto: resposta.resposta }]);
      definirOpcoes(resposta.opcoes);
    } catch (erro) {
      // Falha do assistente dita como o que é, nunca como recusa do domínio
      // (`RF-03-72`, documento 99 §6 invariante 25). O resto da área não
      // depende dela.
      definirIndisponivel(
        erro instanceof ErroDaApi && erro.status === 429
          ? "Você perguntou muitas vezes seguidas deste aparelho. Espere um pouco e pergunte de novo — a documentação, o repositório e o formulário de chave continuam logo abaixo."
          : "O assistente não respondeu agora e voltará. A documentação, o repositório e o formulário de chave continuam logo abaixo.",
      );
      definirOpcoes(OPCOES_DA_ABERTURA);
    } finally {
      definirPerguntando(false);
    }
  }

  return (
    <section aria-labelledby="cg-chat-do-desenvolvedor">
      <h3 id="cg-chat-do-desenvolvedor">Converse com o assistente</h3>
      <ol className="cg-conversa">
        {conversa.map((mensagem, indice) => (
          // A conversa não tem identificador — nada dela é guardado —, e a
          // posição é o que distingue um turno do outro.
          // biome-ignore lint/suspicious/noArrayIndexKey: turno não tem id
          <li key={indice} data-de={mensagem.de}>
            <strong>{mensagem.de === "assistente" ? "Assistente" : "Você"}:</strong>{" "}
            {mensagem.texto}
          </li>
        ))}
      </ol>

      {indisponivel ? <Aviso tipo="atencao">{indisponivel}</Aviso> : null}
      {perguntando ? <p>Pensando…</p> : null}

      {/* Toda mensagem termina com a pergunta de múltipla escolha do próximo
          passo — a abertura, a resposta e a recusa (`RF-03-69`). */}
      {opcoes.length > 0 ? (
        <fieldset>
          <legend>O que você quer conhecer agora?</legend>
          {opcoes.map((opcao) => (
            <Botao key={opcao} variante="secundaria" onClick={() => void perguntar(opcao)}>
              {opcao}
            </Botao>
          ))}
        </fieldset>
      ) : null}

      <form
        onSubmit={(evento) => {
          evento.preventDefault();
          void perguntar(pergunta);
        }}
      >
        <label htmlFor="cg-pergunta-do-desenvolvedor">Ou pergunte o que quiser</label>
        <input
          id="cg-pergunta-do-desenvolvedor"
          type="text"
          value={pergunta}
          onChange={(evento) => definirPergunta(evento.target.value)}
        />
        <Botao tipo="submit" desabilitado={perguntando}>
          Perguntar
        </Botao>
      </form>
      {/* `RF-03-71`: nada aqui pede nome, contato ou qualquer dado de quem
          está perguntando. */}
      <p className="cg-secao__pendente">
        O assistente responde a partir da documentação, do README e do contrato da API, e não
        pede nenhum dado seu.
      </p>
    </section>
  );
}
