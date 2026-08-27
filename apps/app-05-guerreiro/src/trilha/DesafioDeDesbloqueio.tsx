import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { useState } from "react";
import {
  type DesafioDeDesbloqueio as Desafio,
  submeterDesafioDeDesbloqueio,
} from "../api/trilha";

interface Props {
  missaoId: string;
  desafio: Desafio;
  aoDesbloquear: () => void;
}

// Realiza o desafio de desbloqueio. Passando, a missão seguinte abre na
// hora; não passando, convida a tentar de novo, sem contagem de fracassos
// nem punição (`RF-05-13`, `RF-05-14`, `RN-05-20`).
export function DesafioDeDesbloqueio({ missaoId, desafio, aoDesbloquear }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [enviando, definirEnviando] = useState(false);
  const [naoPassou, definirNaoPassou] = useState(false);
  const [aguardandoMestre, definirAguardandoMestre] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);

  async function submeter(alternativaEscolhida: number | null) {
    if (!sessao) return;
    definirEnviando(true);
    definirErro(null);
    definirNaoPassou(false);
    try {
      const resultado = await submeterDesafioDeDesbloqueio(
        missaoId,
        alternativaEscolhida,
        sessao.token,
      );
      if (resultado.aprovado === true) {
        aoDesbloquear();
        return;
      }
      if (resultado.aguardando_mestre) {
        definirAguardandoMestre(true);
        return;
      }
      definirNaoPassou(true);
    } catch (erroCapturado) {
      if (
        erroCapturado &&
        typeof erroCapturado === "object" &&
        "codigo" in erroCapturado &&
        (erroCapturado.codigo === "sessao_ausente" ||
          erroCapturado.codigo === "sessao_invalida")
      ) {
        tratarRecusaDeSessao();
        return;
      }
      definirErro("Não foi possível enviar agora. Tente de novo em instantes.");
    } finally {
      definirEnviando(false);
    }
  }

  if (aguardandoMestre) {
    return (
      <Aviso tipo="andamento">
        Você declarou que cumpriu! Agora é só esperar o Mestre conferir.
      </Aviso>
    );
  }

  return (
    <section aria-label="Desafio de desbloqueio" className="cg-trilha__desafio">
      <h3>Desafio de desbloqueio</h3>
      <p>{desafio.enunciado}</p>

      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {naoPassou && (
        <Aviso tipo="atencao">
          Não foi dessa vez! Você pode tentar de novo quando quiser.
        </Aviso>
      )}

      {desafio.tipo === "quiz" && desafio.alternativas && (
        <ul className="cg-trilha__alternativas">
          {desafio.alternativas.map((alternativa, indice) => (
            <li key={alternativa}>
              <Botao onClick={() => submeter(indice + 1)} desabilitado={enviando}>
                {alternativa}
              </Botao>
            </li>
          ))}
        </ul>
      )}

      {desafio.tipo === "pratico" && (
        <Botao onClick={() => submeter(null)} desabilitado={enviando}>
          {enviando ? "Enviando…" : "Já cumpri!"}
        </Botao>
      )}
    </section>
  );
}
