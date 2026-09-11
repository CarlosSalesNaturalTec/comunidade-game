import { useSessao } from "comum/autenticacao";
import { Aviso, Botao } from "comum/react";
import { useEffect, useState } from "react";
import {
  type DesafioDeDesbloqueio as Desafio,
  lerImagemDaPergunta,
  type PerguntaDoDesbloqueio,
  submeterDesafioDeDesbloqueio,
} from "../api/trilha";

// A imagem da pergunta é buscada do núcleo e mostrada por URL local: a rota
// exige cabeçalho, e `<img src>` não manda nenhum (`RF-09-119`, design —
// decisão 6). Carrega **por pergunta**, e a falha em carregar nunca impede
// de responder — o teto de 1 MB existe justamente porque o quiz é lido em
// rede fraca.
function ImagemDaPergunta({
  pergunta,
  token,
}: {
  pergunta: PerguntaDoDesbloqueio;
  token: string | null;
}) {
  const [endereco, definirEndereco] = useState<string | null>(null);
  const [naoAbriu, definirNaoAbriu] = useState(false);

  useEffect(() => {
    if (!token) return;
    let local: string | null = null;
    let descartado = false;
    lerImagemDaPergunta(pergunta.id, token)
      .then((bytes) => {
        if (descartado) return;
        local = URL.createObjectURL(bytes);
        definirEndereco(local);
      })
      .catch(() => {
        if (!descartado) definirNaoAbriu(true);
      });
    return () => {
      descartado = true;
      if (local) URL.revokeObjectURL(local);
    };
  }, [pergunta.id, token]);

  if (naoAbriu) {
    return (
      <Aviso tipo="atencao">A imagem desta pergunta não abriu, mas pode responder.</Aviso>
    );
  }
  if (!endereco) return null;
  return (
    <img
      className="cg-trilha__imagem-da-pergunta"
      src={endereco}
      alt={`Imagem da pergunta: ${pergunta.enunciado}`}
      onError={() => definirNaoAbriu(true)}
    />
  );
}

interface Props {
  missaoId: string;
  desafio: Desafio;
  aoDesbloquear: () => void;
}

// Realiza o desafio de desbloqueio. No quiz, todas as perguntas aparecem
// numa tela só e vão de uma vez; passando, a missão seguinte abre na hora.
// Não passando, diz quantas ele acertou e convida a tentar de novo, sem
// contagem de fracassos nem punição. Na sondagem nada disso aparece: o
// núcleo abre a trilha ao ser respondida, e é `Sondagem` que dá o
// enquadramento (`RF-05-13`, `RF-05-14`, `RF-05-89`, `RN-05-20`,
// `RN-05-45`, `RN-05-46`).
export function DesafioDeDesbloqueio({ missaoId, desafio, aoDesbloquear }: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const [enviando, definirEnviando] = useState(false);
  const [placar, definirPlacar] = useState<{ acertos: number; total: number } | null>(null);
  const [aguardandoMestre, definirAguardandoMestre] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [escolhas, definirEscolhas] = useState<Record<string, number>>({});
  const [faltando, definirFaltando] = useState<string[]>([]);

  const perguntas = desafio.perguntas ?? [];

  async function submeter() {
    if (!sessao) return;
    let respostas = null;
    if (desafio.tipo === "quiz") {
      const semResposta = perguntas
        .filter((pergunta) => escolhas[pergunta.id] === undefined)
        .map((pergunta) => pergunta.id);
      if (semResposta.length > 0) {
        definirFaltando(semResposta);
        return;
      }
      respostas = perguntas.map((pergunta) => ({
        pergunta_id: pergunta.id,
        alternativa_escolhida: escolhas[pergunta.id],
      }));
    }
    definirFaltando([]);
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

  return (
    <section aria-label="Desafio de desbloqueio" className="cg-trilha__desafio">
      <h3>Desafio de desbloqueio</h3>
      {desafio.enunciado && <p>{desafio.enunciado}</p>}

      {erro && <Aviso tipo="erro">{erro}</Aviso>}
      {faltando.length > 0 && (
        <Aviso tipo="atencao">
          Falta responder {faltando.length} pergunta(s) antes de enviar.
        </Aviso>
      )}
      {placar && (
        <Aviso tipo="atencao">
          Não foi dessa vez! Você acertou {placar.acertos} de {placar.total}. Pode tentar de
          novo quando quiser.
        </Aviso>
      )}

      {desafio.tipo === "quiz" &&
        perguntas.map((pergunta, indice) => (
          <fieldset
            key={pergunta.id}
            className={
              faltando.includes(pergunta.id)
                ? "cg-trilha__pergunta cg-trilha__pergunta--falta"
                : "cg-trilha__pergunta"
            }
          >
            <legend>
              {indice + 1}. {pergunta.enunciado}
            </legend>
            {pergunta.imagem_referencia && (
              <ImagemDaPergunta pergunta={pergunta} token={sessao?.token ?? null} />
            )}
            <ul className="cg-trilha__alternativas">
              {pergunta.alternativas.map((alternativa, posicao) => (
                <li key={alternativa}>
                  <label>
                    <input
                      type="radio"
                      name={`pergunta-${pergunta.id}`}
                      checked={escolhas[pergunta.id] === posicao + 1}
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
        ))}

      <Botao onClick={submeter} desabilitado={enviando}>
        {enviando ? "Enviando…" : desafio.tipo === "quiz" ? "Enviar respostas" : "Já cumpri!"}
      </Botao>
    </section>
  );
}
