import { useEffect, useState } from "react";

interface Props {
  duracaoMs: number;
  /** O que a criança disse até aqui, já transcrito. */
  transcricao: string;
}

// Passo do relógio da barra: fino o bastante para a barra andar sem saltos.
const PASSO_MS = 100;

/**
 * A janela de escuta da sondagem por voz (`RF-05-97`, design — decisão 6).
 * A barra mede **o tempo** da janela — vazia ao abrir o microfone, cheia no
 * fim — e nunca a posição da pergunta no quiz: quem a monta lhe dá uma
 * `key` por pergunta, e ela recomeça vazia a cada uma. A transcrição é texto
 * da tela, alcançável por leitor de tela, e não frase só para a voz.
 */
export function JanelaDeEscuta({ duracaoMs, transcricao }: Props) {
  const [decorrido, definirDecorrido] = useState(0);

  useEffect(() => {
    const inicio = Date.now();
    const relogio = setInterval(() => {
      const agora = Math.min(Date.now() - inicio, duracaoMs);
      definirDecorrido(agora);
      if (agora >= duracaoMs) clearInterval(relogio);
    }, PASSO_MS);
    return () => clearInterval(relogio);
  }, [duracaoMs]);

  return (
    <div className="cg-trilha__escuta">
      <p>Pode falar a sua resposta.</p>
      <progress aria-label="Tempo para responder" max={duracaoMs} value={decorrido} />
      <p aria-live="polite" className="cg-trilha__escuta-transcricao">
        {transcricao ? `Você disse: ${transcricao}` : "Escutando…"}
      </p>
    </div>
  );
}
