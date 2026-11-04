import { useEffect, useRef, useState } from "react";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { useNarracao } from "../narracao/ProvedorDeNarracao";
import { Aviso } from "../react/Aviso";
import { Botao } from "../react/Botao";
import { Campo } from "../react/Campo";
import { MidiaDoNucleo } from "../react/MidiaDoNucleo";
import { SequenciaPaginada } from "../react/SequenciaPaginada";
import {
  abrirEnvioDaComprovacao,
  type ComprovacaoEntregue,
  confirmarEnvioDaComprovacao,
  consultarEnvioDaComprovacao,
  type DesafioDeDesbloqueio as Desafio,
  type EntregaDoPratico,
  enviarComprovacao,
  FORMAS_DE_COMPROVACAO_EM_TEXTO,
  type FormaDeComprovacao,
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
  /** O que o Guerreiro(a) já entregou neste prático, vindo do percurso: a
   * tela reapresenta a entrega em lugar de um formulário vazio ao voltar à
   * missão (`RF-05-93`). */
  comprovacaoEntregue?: ComprovacaoEntregue | null;
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

const ROTULO_DA_FORMA: Record<FormaDeComprovacao, string> = {
  texto: "um texto",
  imagem: "uma foto",
  audio: "um áudio",
  video: "um vídeo",
  arquivo: "um arquivo",
  link_externo: "um link",
};

// Os formatos que o núcleo aceita por forma, para o seletor de arquivo já
// filtrar o que seria recusado depois (`RF-05-91`).
const FORMATOS_ACEITOS: Partial<Record<FormaDeComprovacao, string>> = {
  imagem: "image/jpeg,image/png,image/webp",
  audio: "audio/mpeg",
  video: "video/mp4,video/webm",
  arquivo: "application/pdf,image/jpeg,image/png,image/webp,audio/mpeg",
};

const MENSAGEM_DE_QUEDA_DE_REDE =
  "A conexão caiu no meio do envio. Quando ela voltar, toque em Tentar novamente.";

class QuedaDeRedeDuranteEnvio extends Error {}

// O aviso de que a mídia fica guardada e pode ir à vitrine. É **requisito**,
// não texto de enfeite: é o que dá sentido ao critério de aceite que o Mestre
// escreveu, e por isso vem **antes** do controle de entrega, nunca depois do
// envio. O "Saber mais" é o acesso à área detalhada que o PRD-05 §11 exige de
// toda tela que coleta dado (`RF-05-92`, documento 03 §12).
function AvisoDaMidiaGuardada() {
  const [aberto, definirAberto] = useState(false);

  return (
    <div className="cg-trilha__aviso-da-midia">
      <p>
        O que você entregar aqui fica guardado, e o seu Mestre pode escolher mostrá-lo na
        vitrine.{" "}
        <button
          type="button"
          className="cg-trilha__aviso-da-midia-botao"
          aria-expanded={aberto}
          onClick={() => definirAberto((valor) => !valor)}
        >
          {aberto ? "Ver menos" : "Saber mais"}
        </button>
      </p>
      {aberto && (
        <p className="cg-trilha__aviso-da-midia-detalhe">
          Só o seu Mestre vê o que você enviou, para conferir se você cumpriu o desafio. Se ele
          marcar que pode ser publicado, a sua produção aparece na vitrine com o seu nick —
          nunca com o seu nome nem com a sua foto de rosto. É por isso que o combinado acima
          importa.
        </p>
      )}
    </div>
  );
}

/** A entrega da comprovação do desafio prático, na forma que o Mestre autor
 * aceitou: o critério à vista, o aviso antes do controle, o campo da forma e,
 * ao lado, a alternativa de entregar ao Mestre no encontro para quem recusa a
 * câmera, não tem aparelho que grave ou não consegue enviar (`RF-05-91`,
 * `RF-05-92`, `RF-05-93`, `RN-05-51`). */
function EntregaDoPraticoNaTela({
  desafio,
  comprovacaoEntregue,
  aoDeclarar,
  enviando,
  erro,
}: {
  desafio: Desafio;
  comprovacaoEntregue: ComprovacaoEntregue | null;
  aoDeclarar: (entrega: EntregaDoPratico, arquivo: File | null) => Promise<void>;
  enviando: boolean;
  erro: string | null;
}) {
  const [corpo, definirCorpo] = useState("");
  const [arquivo, definirArquivo] = useState<File | null>(null);
  const [progresso, definirProgresso] = useState<number | null>(null);
  const [erroDeCampo, definirErroDeCampo] = useState<string | null>(null);

  // `?? null` porque o campo chega **ausente** de quem monta a tela sem ele —
  // o prático declarado antes dos três campos, e todo chamador anterior a esta
  // fatia. `undefined` tratado como forma declarada faria o controle nascer
  // indisponível para sempre, sem campo algum a preencher (design — decisão 7).
  const forma = desafio.desafio_pratico_forma_de_comprovacao ?? null;
  const criterio = desafio.desafio_pratico_criterio_de_aceite ?? null;
  const ehTexto = forma !== null && FORMAS_DE_COMPROVACAO_EM_TEXTO.includes(forma);
  const ehMidia = forma !== null && !ehTexto;

  // O prático declarado antes dos três campos não tem forma aceita: segue
  // realizável pela declaração nua, como sempre foi (design — decisão 7).
  const semFormaDeclarada = forma === null;

  // O controle fica indisponível enquanto a comprovação não estiver
  // preenchida: o inválido se impede antes do toque, não se explica depois
  // dele — o mesmo critério que o envio do quiz já aplica.
  const faltaComprovacao = (ehTexto && !corpo.trim()) || (ehMidia && arquivo === null);

  if (comprovacaoEntregue != null) {
    return (
      <div className="cg-trilha__entrega-feita">
        <Aviso tipo="andamento">
          Você declarou que cumpriu! Agora é só esperar o Mestre conferir.
        </Aviso>
        {comprovacaoEntregue.entrega_presencial ? (
          <p>Você vai entregar a sua produção ao Mestre no encontro.</p>
        ) : (
          <>
            <h4>O que você entregou</h4>
            {comprovacaoEntregue.comprovacao !== null && (
              <p className="cg-trilha__comprovacao-entregue">
                {comprovacaoEntregue.comprovacao}
              </p>
            )}
            {comprovacaoEntregue.tem_arquivo && (
              <p>O seu arquivo foi enviado e está guardado.</p>
            )}
          </>
        )}
      </div>
    );
  }

  async function declarar(entrega: EntregaDoPratico, comArquivo: File | null) {
    definirErroDeCampo(null);
    if (comArquivo !== null) definirProgresso(0);
    try {
      await aoDeclarar(entrega, comArquivo);
    } finally {
      definirProgresso(null);
    }
  }

  return (
    <div className="cg-trilha__entrega-do-pratico">
      {criterio !== null && (
        <div className="cg-trilha__criterio">
          <h4>O que o seu Mestre combinou</h4>
          <p>{criterio}</p>
        </div>
      )}
      {forma !== null && <p>Para cumprir, entregue {ROTULO_DA_FORMA[forma]}.</p>}

      {ehMidia && <AvisoDaMidiaGuardada />}

      {ehTexto && (
        <Campo
          rotulo={
            forma === "link_externo" ? "O endereço do seu trabalho" : "Conte o que você fez"
          }
          valor={corpo}
          aoAlterar={definirCorpo}
          tipo={forma === "link_externo" ? "url" : "text"}
          erro={erroDeCampo}
        />
      )}

      {ehMidia && (
        <label className="cg-trilha__arquivo-da-comprovacao">
          Escolha o arquivo
          <input
            type="file"
            accept={FORMATOS_ACEITOS[forma]}
            onChange={(evento) => definirArquivo(evento.target.files?.[0] ?? null)}
          />
        </label>
      )}

      {progresso !== null && (
        <p className="cg-trilha__progresso" role="status">
          Enviando… {progresso}%
        </p>
      )}

      {erroDeCampo !== null && <Aviso tipo="erro">{erroDeCampo}</Aviso>}
      {erro !== null && <Aviso tipo="erro">{erro}</Aviso>}

      <Botao
        onClick={() =>
          declarar(ehTexto ? { comprovacao: corpo.trim() } : {}, ehMidia ? arquivo : null)
        }
        desabilitado={enviando || (!semFormaDeclarada && faltaComprovacao)}
      >
        {enviando ? "Enviando…" : "Já cumpri!"}
      </Botao>

      {/* A alternativa nunca é apresentada como falha, desistência ou perda
          da missão: é o caminho de quem recusa a câmera, não tem aparelho que
          grave ou não consegue enviar, e o PRD-05 §11 já o garante para a
          produção da missão (`RN-05-51`, `RF-05-78`). */}
      {ehMidia && (
        <div className="cg-trilha__entrega-no-encontro">
          <p>Não dá para enviar agora?</p>
          <Botao
            variante="secundaria"
            onClick={() => declarar({ entrega_presencial: true }, null)}
            desabilitado={enviando}
          >
            Vou entregar ao Mestre no encontro
          </Botao>
        </div>
      )}
    </div>
  );
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
  comprovacaoEntregue = null,
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
  const [entregue, definirEntregue] = useState<ComprovacaoEntregue | null>(
    comprovacaoEntregue ?? null,
  );
  // O que falta enviar depois de a rede cair: o endereço da sessão já aberta,
  // o arquivo e quantos bytes o armazenamento já tem. Com isto a retomada
  // continua de onde parou, sem recomeçar do zero (`RF-05-91`).
  const [retomada, definirRetomada] = useState<{
    endereco: string;
    arquivo: File;
    recebidos: number;
  } | null>(null);

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

  async function submeter(entrega: EntregaDoPratico = {}, arquivo: File | null = null) {
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
      const resultado = await submeterDesafioDeDesbloqueio(
        missaoId,
        respostas,
        sessao.token,
        entrega,
      );
      // Na mídia a declaração nasce sem arquivo e o recebe agora, pela sessão
      // retomável: a entrega só está completa quando o envio confirma
      // (`RF-05-91`).
      if (arquivo !== null) {
        const entregaConfirmada = await enviarArquivoDaComprovacao(arquivo, sessao.token);
        definirEntregue(entregaConfirmada ?? null);
        definirAguardandoMestre(true);
        return;
      }
      if (resultado.aprovado === true) {
        aoDesbloquear();
        return;
      }
      if (resultado.aguardando_mestre) {
        definirEntregue(resultado.comprovacao_entregue ?? null);
        definirAguardandoMestre(true);
        return;
      }
      definirPlacar({ acertos: resultado.acertos, total: resultado.total });
    } catch (erroCapturado) {
      if (erroCapturado instanceof QuedaDeRedeDuranteEnvio) {
        definirErro(MENSAGEM_DE_QUEDA_DE_REDE);
        return;
      }
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

  /** Abre a sessão, manda as partes e confirma. Caindo a rede, a posição já
   * recebida volta do armazenamento e o envio retoma de onde parou, sem
   * recomeçar do zero nem perder a declaração (`RF-05-91`). */
  async function enviarArquivoDaComprovacao(
    arquivo: File,
    token: string,
  ): Promise<ComprovacaoEntregue> {
    const endereco = await abrirEnvioDaComprovacao(
      missaoId,
      arquivo.type,
      arquivo.size,
      token,
    );
    try {
      await enviarComprovacao(endereco, arquivo, () => {});
    } catch {
      const recebidos = await consultarEnvioDaComprovacao(endereco, arquivo.size).catch(
        () => 0,
      );
      if (recebidos < arquivo.size) {
        definirRetomada({ endereco, arquivo, recebidos });
        throw new QuedaDeRedeDuranteEnvio();
      }
    }
    return confirmarEnvioDaComprovacao(missaoId, token);
  }

  async function retomarEnvio() {
    if (!sessao || retomada === null) return;
    definirEnviando(true);
    definirErro(null);
    try {
      await enviarComprovacao(
        retomada.endereco,
        retomada.arquivo,
        () => {},
        retomada.recebidos,
      );
      definirEntregue((await confirmarEnvioDaComprovacao(missaoId, sessao.token)) ?? null);
      definirRetomada(null);
      definirAguardandoMestre(true);
    } catch {
      definirErro(MENSAGEM_DE_QUEDA_DE_REDE);
    } finally {
      definirEnviando(false);
    }
  }

  if (retomada !== null) {
    return (
      <section aria-label="Desafio de desbloqueio" className="cg-trilha__desafio">
        <h3>Desafio de desbloqueio</h3>
        <Aviso tipo="atencao">{MENSAGEM_DE_QUEDA_DE_REDE}</Aviso>
        {erro !== null && <Aviso tipo="erro">{erro}</Aviso>}
        <Botao onClick={retomarEnvio} desabilitado={enviando}>
          {enviando ? "Enviando…" : "Tentar novamente"}
        </Botao>
      </section>
    );
  }

  if (aguardandoMestre || entregue !== null) {
    // Sem entrega a reapresentar — prático antigo, que não guardou
    // comprovação — o aviso nu segue sendo a resposta certa.
    if (!ehQuiz && entregue !== null) {
      return (
        <section aria-label="Desafio de desbloqueio" className="cg-trilha__desafio">
          <h3>Desafio de desbloqueio</h3>
          {desafio.enunciado && <p>{desafio.enunciado}</p>}
          <EntregaDoPraticoNaTela
            desafio={desafio}
            comprovacaoEntregue={entregue}
            aoDeclarar={submeter}
            enviando={enviando}
            erro={erro}
          />
        </section>
      );
    }
    return (
      <Aviso tipo="andamento">
        Você declarou que cumpriu! Agora é só esperar o Mestre conferir.
      </Aviso>
    );
  }

  // O envio pertence ao **conjunto** das respostas, não à pergunta da vez, e
  // por isso acompanha avançar e voltar na mesma linha (decisão do fundador de
  // 2026-10-16).
  //
  // `() => submeter()` e não `submeter`: o `onClick` passaria o evento do toque
  // como primeiro argumento, que agora é a entrega do prático — o quiz mandaria
  // um `MouseEvent` no corpo da submissão.
  const envioDoQuiz = submissaoLigada ? (
    <Botao onClick={() => submeter()} desabilitado={enviando || !todasRespondidas}>
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
          responder: o que ele pede é a comprovação na forma que o Mestre
          autor aceitou, sob o critério que ele escreveu (`RF-05-91`,
          `RF-05-92`). */}
      {!ehQuiz && submissaoLigada && (
        <EntregaDoPraticoNaTela
          desafio={desafio}
          comprovacaoEntregue={null}
          aoDeclarar={submeter}
          enviando={enviando}
          erro={erro}
        />
      )}

      {/* Desligada a submissão, o critério e a forma seguem à vista: eles não
          são segredo do Mestre, e é deles que a criança sabe o que preparar. */}
      {!ehQuiz && !submissaoLigada && !!desafio.desafio_pratico_criterio_de_aceite && (
        <div className="cg-trilha__criterio">
          <h4>O que o seu Mestre combinou</h4>
          <p>{desafio.desafio_pratico_criterio_de_aceite}</p>
        </div>
      )}

      {!submissaoLigada && (
        <Aviso tipo="andamento">
          Aqui você só lê o desafio. Para enviar, abra a sua Área do Guerreiro(a).
        </Aviso>
      )}
    </section>
  );
}
