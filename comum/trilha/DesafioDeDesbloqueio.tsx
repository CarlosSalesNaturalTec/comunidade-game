import { useEffect, useRef, useState } from "react";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { useNarracao } from "../narracao/ProvedorDeNarracao";
import { Aviso } from "../react/Aviso";
import { Botao } from "../react/Botao";
import { MidiaDoNucleo } from "../react/MidiaDoNucleo";
import { SequenciaPaginada } from "../react/SequenciaPaginada";
import {
  type DesafioDeDesbloqueio as Desafio,
  lerImagemDaPergunta,
  submeterDesafioDeDesbloqueio,
} from "./api";

interface Props {
  missaoId: string;
  desafio: Desafio;
  aoDesbloquear: () => void;
  /** A submissão é ato de escrita, e cada aplicação liga a sua: desligada,
   * a tela apresenta o desafio e diz onde ele se submete, sem botão de
   * envio (design — decisão 3). */
  submissaoLigada?: boolean;
}

type Pergunta = NonNullable<Desafio["perguntas"]>[number];

// O que a narração fala ao se alcançar a pergunta: o enunciado **e as
// alternativas**. Só o enunciado é o recorte do Quiz ao Vivo, onde o tempo de
// resposta é curto; aqui não há cronômetro, e ouvir a pergunta sem as
// respostas possíveis deixaria quem ainda não lê sem como responder
// (documento 15 §5.1, decisão do fundador de 2026-10-16).
//
// A frase sai do **dado que a tela declara** — o enunciado e o array de
// alternativas —, nunca do documento apresentado, e vai direto à síntese: ela
// nunca entra na tela, e por isso não há nó algum a esconder de leitor de
// tela, que segue lendo o enunciado e as alternativas como a tela os
// apresenta. Nada é numerado, porque a tela não numera as alternativas:
// inventar número seria ler rótulo de interface, que o contrato da camada
// veda (design — decisão 2).
function falaDaPergunta(pergunta: Pergunta): string {
  return [pergunta.enunciado, ...pergunta.alternativas].join(". ");
}

// Realiza o desafio de desbloqueio. No quiz, a tela apresenta **uma
// pergunta por vez**, com retorno à anterior para trocar a resposta, e a
// submissão continua sendo **uma só, com todas as respostas**: o critério
// de aprovação é do conjunto (`RN-05-45`), e submeter por pergunta o
// tornaria incalculável. O envio **só fica disponível com todas as perguntas
// respondidas**: o inválido se impede antes do toque, não se explica depois
// dele (decisão do fundador de 2026-10-16). Passando, a missão seguinte abre
// na hora.
// Não passando, diz quantas ele acertou e convida a tentar de novo, sem
// contagem de fracassos nem punição. Na sondagem nada disso aparece: o
// núcleo abre a trilha ao ser respondida, e é `Sondagem` que dá o
// enquadramento (`RF-05-13`, `RF-05-14`, `RF-05-89`, `RN-05-20`,
// `RN-05-45`, `RN-05-46`).
export function DesafioDeDesbloqueio({
  missaoId,
  desafio,
  aoDesbloquear,
  submissaoLigada = false,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const { narrar } = useNarracao();
  const [enviando, definirEnviando] = useState(false);
  const [placar, definirPlacar] = useState<{ acertos: number; total: number } | null>(null);
  const [aguardandoMestre, definirAguardandoMestre] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [escolhas, definirEscolhas] = useState<Record<string, number>>({});
  const [indiceDaPergunta, definirIndiceDaPergunta] = useState(0);
  const [midiaCarregando, definirMidiaCarregando] = useState(false);

  const perguntas = desafio.perguntas ?? [];
  const ehQuiz = desafio.tipo === "quiz";
  const perguntaDaVez = perguntas[Math.min(indiceDaPergunta, perguntas.length - 1)];
  const todasRespondidas = perguntas.every((pergunta) => escolhas[pergunta.id] !== undefined);

  // A fala entra na **mudança do `id`** da pergunta, guardada em referência, e
  // não num efeito sobre o objeto dela: o objeto é novo a cada render de quem
  // monta, e um efeito por identidade falaria em laço — o mesmo cuidado que o
  // Quiz ao Vivo tem com a sondagem de 2 s (design — decisão 1).
  // A referência guarda o `narrar` junto do `id`, e não o `id` sozinho: ele
  // cala quando a narração está desligada ou quando a voz do aparelho ainda
  // não chegou, e um `id` já marcado faria a pergunta nunca falar depois — o
  // laço de `useNarrarAoEntrar`, que refala quando o `narrar` muda de
  // identidade, sem o `id` só porque não precisa dele.
  const perguntaFalada = useRef<{ id: string; narrar: typeof narrar } | null>(null);
  useEffect(() => {
    if (!ehQuiz || !perguntaDaVez) return;
    const falada = perguntaFalada.current;
    if (falada?.id === perguntaDaVez.id && falada.narrar === narrar) return;
    perguntaFalada.current = { id: perguntaDaVez.id, narrar };
    narrar({ texto: falaDaPergunta(perguntaDaVez) });
  }, [ehQuiz, perguntaDaVez, narrar]);

  async function submeter() {
    if (!sessao) return;
    let respostas = null;
    if (ehQuiz) {
      // O envio não fica disponível antes disto; a guarda é a rede de
      // segurança de quem chamar por outro caminho.
      if (!todasRespondidas) return;
      respostas = perguntas.map((pergunta) => ({
        pergunta_id: pergunta.id,
        alternativa_escolhida: escolhas[pergunta.id],
      }));
    }
    definirEnviando(true);
    definirErro(null);
    definirPlacar(null);
    try {
      const resultado = await submeterDesafioDeDesbloqueio(missaoId, respostas, sessao.token);
      if (resultado.aprovado === true) {
        aoDesbloquear();
        return;
      }
      if (resultado.aguardando_mestre) {
        definirAguardandoMestre(true);
        return;
      }
      definirPlacar({ acertos: resultado.acertos, total: resultado.total });
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

  // O envio pertence ao **conjunto** das respostas, não à pergunta da vez, e
  // por isso acompanha avançar e voltar na mesma linha (decisão do fundador de
  // 2026-10-16).
  const envioDoQuiz = submissaoLigada ? (
    <Botao onClick={submeter} desabilitado={enviando || !todasRespondidas}>
      {enviando ? "Enviando…" : "Enviar respostas"}
    </Botao>
  ) : undefined;

  return (
    <section aria-label="Desafio de desbloqueio" className="cg-trilha__desafio">
      <h3>Desafio de desbloqueio</h3>
      {desafio.enunciado && <p>{desafio.enunciado}</p>}

      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {placar && (
        <Aviso tipo="atencao">
          Não foi dessa vez! Você acertou {placar.acertos} de {placar.total}. Pode tentar de
          novo quando quiser.
        </Aviso>
      )}

      {ehQuiz && (
        <SequenciaPaginada
          itens={perguntas}
          rotuloDeAvancar="Próxima pergunta"
          rotuloDeVoltar="Pergunta anterior"
          indice={indiceDaPergunta}
          aoIrPara={definirIndiceDaPergunta}
          acoes={envioDoQuiz}
          controlesTravados={midiaCarregando}
        >
          {(pergunta) => (
            <fieldset className="cg-trilha__pergunta">
              <legend>{pergunta.enunciado}</legend>
              {pergunta.imagem_referencia && (
                <MidiaDoNucleo
                  id={pergunta.id}
                  buscar={lerImagemDaPergunta}
                  token={sessao?.token ?? null}
                  tipo="imagem"
                  alt={`Imagem da pergunta: ${pergunta.enunciado}`}
                  textoDeErro="A imagem desta pergunta não abriu, mas pode responder."
                  aoMudarCarregamento={definirMidiaCarregando}
                />
              )}
              <ul className="cg-trilha__alternativas">
                {pergunta.alternativas.map((alternativa, posicao) => (
                  <li key={alternativa}>
                    <label>
                      <input
                        type="radio"
                        name={`pergunta-${pergunta.id}`}
                        checked={escolhas[pergunta.id] === posicao + 1}
                        disabled={!submissaoLigada}
                        onChange={() =>
                          definirEscolhas({ ...escolhas, [pergunta.id]: posicao + 1 })
                        }
                      />
                      {alternativa}
                    </label>
                  </li>
                ))}
              </ul>
            </fieldset>
          )}
        </SequenciaPaginada>
      )}

      {/* O desafio que se cumpre por **declaração** não tem pergunta a
          responder, e o controle dele segue sempre disponível. */}
      {!ehQuiz && submissaoLigada && (
        <Botao onClick={submeter} desabilitado={enviando}>
          {enviando ? "Enviando…" : "Já cumpri!"}
        </Botao>
      )}

      {!submissaoLigada && (
        <Aviso tipo="andamento">
          Aqui você só lê o desafio. Para enviar, abra a sua Área do Guerreiro(a).
        </Aviso>
      )}
    </section>
  );
}
