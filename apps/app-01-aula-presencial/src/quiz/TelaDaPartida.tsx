import { ErroDaApi } from "comum/api";
import { useNarracao } from "comum/narracao";
import { Aviso, Botao, Cabecalho, EstadoDaLista, Moldura } from "comum/react";
import { useCallback, useEffect, useRef, useState } from "react";
import {
  enviarResposta,
  lerPerguntaDaPartida,
  listarPartidasDaAula,
  type PerguntaParaEquipe,
} from "../api/quiz";

// Estado do próprio aparelho — nunca a verdade, sempre relido do núcleo a
// cada abertura do caminho do quiz (design — decisão 4, Risks). Apagada ao
// voltar ao início, junto das demais chaves da sessão de trabalho
// (`TelaInicial.tsx`).
export const CHAVE_DA_PARTIDA_DE_QUIZ = "app-01:quiz:partida";

const INTERVALO_DE_SONDAGEM_EM_MS = 2000;

const MENSAGEM_DE_PERDA_DE_CONTATO =
  "Perdemos contato com o núcleo. A tela segue com a última pergunta conhecida e volta a atualizar sozinha assim que a rede voltar.";

const MENSAGEM_DE_JA_RESPONDEU = "Esta equipe já respondeu a esta pergunta.";

const MENSAGEM_DE_RESPOSTA_INDISPONIVEL =
  "A resposta está indisponível sem rede. Assim que a rede voltar, você pode responder.";

const MENSAGEM_SEM_PARTIDA =
  "Não há partida de Quiz ao Vivo para esta equipe agora. Peça a um Mestre para verificar.";

interface Props {
  aulaId: string;
  tokenDoGuerreiro: string;
  aoVoltar: () => void;
}

// O aparelho da equipe: descobre a partida e a equipe já derivadas pelo
// núcleo, acompanha a pergunta no ar por sondagem e envia a resposta da
// equipe — nunca do aparelho (`RF-04-41` a `RF-04-44`, `RF-04-58`,
// documento 05 §5).
export function TelaDaPartida({ aulaId, tokenDoGuerreiro, aoVoltar }: Props) {
  const [descobrindo, definirDescobrindo] = useState(true);
  const [partidaId, definirPartidaId] = useState<string | null>(null);
  const [equipeId, definirEquipeId] = useState<string | null>(null);
  const [pergunta, definirPergunta] = useState<PerguntaParaEquipe | null>(null);
  const [semRede, definirSemRede] = useState(false);
  const [minhaResposta, definirMinhaResposta] = useState<number | null>(null);
  const [jaRespondida, definirJaRespondida] = useState(false);
  const [enviando, definirEnviando] = useState(false);
  const perguntaIdConhecidaRef = useRef<string | null>(null);
  const { narrar } = useNarracao();

  // Descoberta: relida a cada entrada nesta tela, nunca confiada ao que o
  // `sessionStorage` guardou de um atendimento anterior (design — decisão
  // 1, Risks). A equipe já vem derivada; o aparelho não escolhe.
  useEffect(() => {
    let cancelado = false;
    definirDescobrindo(true);
    listarPartidasDaAula(aulaId, tokenDoGuerreiro)
      .then((partidas) => {
        if (cancelado) return;
        const daEquipe = partidas.find(
          (partida) => partida.situacao === "aberta" && partida.equipe_id !== null,
        );
        if (daEquipe?.equipe_id) {
          sessionStorage.setItem(
            CHAVE_DA_PARTIDA_DE_QUIZ,
            JSON.stringify({ partidaId: daEquipe.id, equipeId: daEquipe.equipe_id }),
          );
          definirPartidaId(daEquipe.id);
          definirEquipeId(daEquipe.equipe_id);
        }
      })
      .finally(() => {
        if (!cancelado) definirDescobrindo(false);
      });
    return () => {
      cancelado = true;
    };
  }, [aulaId, tokenDoGuerreiro]);

  const sondar = useCallback(async () => {
    if (!partidaId) return;
    try {
      const proxima = await lerPerguntaDaPartida(partidaId, tokenDoGuerreiro);
      definirPergunta(proxima);
      definirSemRede(false);
      if (proxima.id !== perguntaIdConhecidaRef.current) {
        perguntaIdConhecidaRef.current = proxima.id ?? null;
        definirMinhaResposta(null);
        definirJaRespondida(false);
        // A fala entra **neste** ponto, e não num efeito sobre o objeto da
        // pergunta: a sondagem devolve objeto novo a cada 2 s, e um efeito
        // por identidade falaria trinta vezes por minuto. Só o enunciado —
        // as alternativas, o resultado e os avisos de rede não são falados,
        // porque o tempo em que a equipe responde é curto (documento 15
        // §5.1, design — decisão 7).
        if (proxima.enunciado) narrar({ texto: proxima.enunciado });
      }
    } catch {
      definirSemRede(true);
    }
  }, [partidaId, tokenDoGuerreiro, narrar]);

  useEffect(() => {
    if (!partidaId) return;
    sondar();
    const intervalo = setInterval(sondar, INTERVALO_DE_SONDAGEM_EM_MS);
    return () => clearInterval(intervalo);
  }, [partidaId, sondar]);

  async function responder(alternativa: number) {
    if (!partidaId || !equipeId || !pergunta?.id) return;
    if (minhaResposta !== null || jaRespondida) return;
    if (semRede) return;
    definirEnviando(true);
    try {
      await enviarResposta(partidaId, pergunta.id, equipeId, alternativa, tokenDoGuerreiro);
      definirMinhaResposta(alternativa);
    } catch (erroCapturado) {
      if (erroCapturado instanceof ErroDaApi) {
        // Outro aparelho da mesma equipe já respondeu — a mesma mensagem
        // do bloqueio local, nunca tela de erro (`RF-04-43`, design —
        // decisão 6).
        definirJaRespondida(true);
      } else {
        definirSemRede(true);
      }
    } finally {
      definirEnviando(false);
    }
  }

  if (descobrindo) {
    return (
      <Moldura>
        <Cabecalho
          titulo="Quiz ao Vivo"
          acao={{ rotulo: "Voltar ao início", aoAcionar: aoVoltar }}
        />
        <EstadoDaLista>Procurando a partida desta aula…</EstadoDaLista>
      </Moldura>
    );
  }

  if (!partidaId || !equipeId) {
    return (
      <Moldura>
        <Cabecalho
          titulo="Quiz ao Vivo"
          acao={{ rotulo: "Voltar ao início", aoAcionar: aoVoltar }}
        />
        <Aviso tipo="atencao">{MENSAGEM_SEM_PARTIDA}</Aviso>
      </Moldura>
    );
  }

  const respondida = minhaResposta !== null || jaRespondida;
  const resultadoLiberado = pergunta?.resultado_liberado === true;

  return (
    <Moldura>
      {/* O cabeçalho desta tela cala: o que a partida tem a dizer é o
          enunciado da pergunta no ar, e falar o título antes dele só o
          cortaria — a camada não enfileira falas (design — decisão 7). */}
      <Cabecalho
        titulo="Quiz ao Vivo"
        narracao={null}
        acao={{ rotulo: "Voltar ao início", aoAcionar: aoVoltar }}
      />

      {/* Os avisos da partida e o resultado NUNCA são falados: o recorte da
          decisão é o enunciado, e o tempo em que a equipe responde é curto
          (documento 15 §5.1). Eles seguem em tela, com o `role` que o leitor
          de tela anuncia. */}
      {semRede && (
        <Aviso tipo="atencao" narracao={null}>
          {MENSAGEM_DE_PERDA_DE_CONTATO}
        </Aviso>
      )}

      {!pergunta?.id && (
        <EstadoDaLista>A próxima pergunta ainda não entrou no ar. Aguarde.</EstadoDaLista>
      )}

      {pergunta?.id && pergunta.enunciado && pergunta.alternativas && (
        <section aria-label="Pergunta no ar">
          <h2>{pergunta.enunciado}</h2>
          <ul className="cg-alternativas-de-quiz">
            {pergunta.alternativas.map((alternativa, indice) => {
              const numero = indice + 1;
              const escolhida = minhaResposta === numero;
              return (
                <li key={alternativa}>
                  <Botao
                    variante={escolhida ? "primaria" : "secundaria"}
                    onClick={() => responder(numero)}
                    desabilitado={enviando || respondida || semRede || resultadoLiberado}
                  >
                    {numero}. {alternativa}
                  </Botao>
                </li>
              );
            })}
          </ul>

          {jaRespondida && !resultadoLiberado && (
            <Aviso tipo="atencao" narracao={null}>
              {MENSAGEM_DE_JA_RESPONDEU}
            </Aviso>
          )}

          {semRede && !respondida && !resultadoLiberado && (
            <Aviso tipo="atencao" narracao={null}>
              {MENSAGEM_DE_RESPOSTA_INDISPONIVEL}
            </Aviso>
          )}

          {resultadoLiberado && (
            <Aviso tipo="sucesso" narracao={null}>
              A alternativa correta é a {pergunta.alternativa_correta}. Sua equipe{" "}
              {pergunta.acertou ? "acertou" : "não acertou"}.{" "}
              {pergunta.primeira_equipe_a_acertar &&
                (pergunta.primeira_equipe_a_acertar === equipeId
                  ? "Sua equipe chegou primeiro!"
                  : "Outra equipe chegou primeiro.")}
            </Aviso>
          )}
        </section>
      )}
    </Moldura>
  );
}
