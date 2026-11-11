import { useEffect, useRef, useState } from "react";
import { useSessao } from "../autenticacao/ContextoDeSessao";
import { escutarPorJanela, existeTranscricaoDeFala } from "../fala/fala";
import { useNarracao } from "../narracao/ProvedorDeNarracao";
import { Aviso } from "../react/Aviso";
import { Botao } from "../react/Botao";
import { Campo } from "../react/Campo";
import { Icone } from "../react/Icone";
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
  type JulgamentoDoPratico,
  lerImagemDaPergunta,
  submeterDesafioDeDesbloqueio,
} from "./api";
import { JanelaDeEscuta } from "./JanelaDeEscuta";
import { ligarFalaAAlternativa } from "./ligarFalaAAlternativa";

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
  /** O que o Mestre autor decidiu, vindo do mesmo percurso: `null` é "ainda
   * não julgado". Julgado, a tela diz se cumpriu, se vai à vitrine e o
   * motivo — nada do julgamento fica gravado sem ser lido por ele
   * (`RF-05-94`). */
  julgamento?: JulgamentoDoPratico | null;
  /** A **sondagem**: só ela responde por voz — com o áudio ligado, depois de
   * cada pergunta falada, o microfone abre pela janela de 5 s (`RF-05-97`,
   * `RN-05-54`) — e só ela tem retorno por pergunta, avanço sozinho e a tela
   * final com Refazer e Concluir (`RF-05-99`, `RF-05-100`). Aqui
   * `aoDesbloquear` é o **Concluir**: a trilha só recarrega quando a criança
   * sai da tela final, senão ela sumiria (design — decisão 8). */
  ehSondagem?: boolean;
}

// A janela da sondagem por voz: cinco segundos, da decisão do fundador de
// 2026-11-07 (`RF-05-97`, design — decisão 2).
export const JANELA_DA_SONDAGEM_MS = 5000;

// Quanto o símbolo de acerto ou de erro fica na tela antes de a sondagem
// seguir sozinha (`RF-05-99`, decisão do fundador de 2026-11-10).
export const RETORNO_DA_SONDAGEM_MS = 2000;

// O texto do retorno: anunciado ao leitor de tela e, com a narração ligada,
// falado. Sem palavra de aprovação ou reprovação (`RF-05-73`).
const TEXTO_DO_ACERTO = "Você acertou!";
const TEXTO_DO_ERRO = "Não foi essa.";

// A escolha por toque é o número da alternativa; a resposta falada que não
// se ligou a nenhuma segue literal (`RF-05-98`).
type Escolha = number | { falada: string };

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
// O que o Mestre decidiu, dito ao Guerreiro(a) — o motivo **na íntegra**, como
// o Mestre o escreveu, nunca resumido nem trocado por frase da aplicação. Não
// tendo cumprido, a linguagem é acolhedora e convida a entregar de novo, sem
// contagem de fracassos e sem nada que elimine ou classifique a criança: a
// mesma régua do quiz que não passa (`RF-05-94`, `RN-05-20`).
function VereditoDoMestre({ julgamento }: { julgamento: JulgamentoDoPratico }) {
  if (!julgamento.cumpriu) {
    return (
      <div className="cg-trilha__veredito">
        <Aviso tipo="atencao">
          O Mestre conferiu e pediu para você fazer mais uma vez. Dá para tentar de novo,
          quantas vezes precisar.
        </Aviso>
        {julgamento.motivo !== null && (
          <p className="cg-trilha__motivo-do-mestre">{julgamento.motivo}</p>
        )}
      </div>
    );
  }
  return (
    <div className="cg-trilha__veredito">
      <Aviso tipo="sucesso">Você cumpriu o desafio! O Mestre conferiu a sua produção.</Aviso>
      {julgamento.publicavel ? (
        <p>A sua produção pode aparecer na vitrine do projeto.</p>
      ) : (
        <>
          <p>Esta produção não vai para a vitrine.</p>
          {julgamento.motivo !== null && (
            <p className="cg-trilha__motivo-do-mestre">{julgamento.motivo}</p>
          )}
        </>
      )}
    </div>
  );
}

function EntregaDoPraticoNaTela({
  desafio,
  comprovacaoEntregue,
  julgamento,
  aoDeclarar,
  aoEnviarArquivo,
  enviando,
  erro,
}: {
  desafio: Desafio;
  comprovacaoEntregue: ComprovacaoEntregue | null;
  julgamento: JulgamentoDoPratico | null;
  aoDeclarar: (entrega: EntregaDoPratico, arquivo: File | null) => Promise<void>;
  aoEnviarArquivo: (arquivo: File) => Promise<void>;
  enviando: boolean;
  erro: string | null;
}) {
  const [corpo, definirCorpo] = useState("");
  const [arquivo, definirArquivo] = useState<File | null>(null);
  const [progresso, definirProgresso] = useState<number | null>(null);
  const [erroDeCampo, definirErroDeCampo] = useState<string | null>(null);

  // Nulos no prático declarado antes dos três campos, que segue realizável
  // pela declaração nua (`RN-09-50`).
  const forma = desafio.forma_de_comprovacao ?? null;
  const criterio = desafio.criterio_de_aceite ?? null;
  const ehTexto = forma !== null && FORMAS_DE_COMPROVACAO_EM_TEXTO.includes(forma);
  const ehMidia = forma !== null && !ehTexto;

  // O prático declarado antes dos três campos não tem forma aceita: segue
  // realizável pela declaração nua, como sempre foi (design — decisão 7).
  const semFormaDeclarada = forma === null;

  // O controle fica indisponível enquanto a comprovação não estiver
  // preenchida: o inválido se impede antes do toque, não se explica depois
  // dele — o mesmo critério que o envio do quiz já aplica.
  const faltaComprovacao = (ehTexto && !corpo.trim()) || (ehMidia && arquivo === null);

  // O que já foi entregue, sempre à vista. O julgamento decide se a entrega
  // está **encerrada** (cumpriu) ou **reaberta** (não cumpriu): recusado, o
  // Guerreiro(a) entrega outra em cima da anterior, sem limite (`RN-09-54`).
  const recusado = julgamento !== null && !julgamento.cumpriu;
  if (comprovacaoEntregue != null) {
    const oQueEntregou = (
      <>
        {comprovacaoEntregue.entrega_presencial ? (
          <p>Você vai entregar a sua produção ao Mestre no encontro.</p>
        ) : (
          <>
            {/* O título só com o que apresentar embaixo dele (`RF-05-93`). */}
            {(comprovacaoEntregue.comprovacao !== null || comprovacaoEntregue.tem_arquivo) && (
              <h4>O que você entregou</h4>
            )}
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
      </>
    );

    // Declaração em mídia, ainda não julgada, cujo arquivo não chegou: a
    // mesma declaração recebe o arquivo agora, como retomada do envio, sem
    // declarar de novo (`RF-05-91`, `RF-05-93`).
    const arquivoFaltando =
      julgamento === null &&
      ehMidia &&
      !comprovacaoEntregue.entrega_presencial &&
      !comprovacaoEntregue.tem_arquivo;
    if (arquivoFaltando && forma !== null) {
      return (
        <div className="cg-trilha__entrega-feita">
          <Aviso tipo="andamento">
            Você declarou que cumpriu, mas o arquivo não chegou. Envie {ROTULO_DA_FORMA[forma]}{" "}
            para o Mestre conferir.
          </Aviso>
          {criterio !== null && (
            <div className="cg-trilha__criterio">
              <h4>O que o seu Mestre combinou</h4>
              <p>{criterio}</p>
            </div>
          )}
          <AvisoDaMidiaGuardada />
          <label className="cg-trilha__arquivo-da-comprovacao">
            Escolha o arquivo
            <input
              type="file"
              accept={FORMATOS_ACEITOS[forma]}
              onChange={(evento) => definirArquivo(evento.target.files?.[0] ?? null)}
            />
          </label>
          {erro !== null && <Aviso tipo="erro">{erro}</Aviso>}
          <Botao
            onClick={() => arquivo !== null && aoEnviarArquivo(arquivo)}
            desabilitado={enviando || arquivo === null}
          >
            {enviando ? "Enviando…" : "Enviar o arquivo"}
          </Botao>
        </div>
      );
    }
    if (julgamento === null) {
      return (
        <div className="cg-trilha__entrega-feita">
          <Aviso tipo="andamento">
            Você declarou que cumpriu! Agora é só esperar o Mestre conferir.
          </Aviso>
          {oQueEntregou}
        </div>
      );
    }
    if (!recusado) {
      return (
        <div className="cg-trilha__entrega-feita">
          <VereditoDoMestre julgamento={julgamento} />
          {oQueEntregou}
        </div>
      );
    }
    // Recusado: o veredito e o motivo acima, o que ele entregou à vista, e o
    // formulário aberto de novo — cai para o corpo da função.
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
      {/* Recusado, o veredito e o motivo vêm **antes** do formulário, e o que
          ele entregou segue à vista: ele vê por que não passou e o que
          mandou, e entrega outra em cima (`RF-05-94`, `RN-09-54`). */}
      {recusado && julgamento !== null && <VereditoDoMestre julgamento={julgamento} />}
      {recusado && comprovacaoEntregue?.comprovacao != null && (
        <div className="cg-trilha__entrega-anterior">
          <h4>O que você entregou antes</h4>
          <p className="cg-trilha__comprovacao-entregue">{comprovacaoEntregue.comprovacao}</p>
        </div>
      )}
      {recusado && comprovacaoEntregue?.tem_arquivo && (
        <p>O arquivo que você mandou antes está guardado.</p>
      )}

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
  julgamento = null,
  ehSondagem = false,
}: Props) {
  const { sessao, tratarRecusaDeSessao } = useSessao();
  const { narrar, microfonePermitido } = useNarracao();
  const [enviando, definirEnviando] = useState(false);
  const [placar, definirPlacar] = useState<{ acertos: number; total: number } | null>(null);
  const [aguardandoMestre, definirAguardandoMestre] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [escolhas, definirEscolhasNoEstado] = useState<Record<string, Escolha>>({});
  // A resposta falada chega por retorno do navegador, fora do render: a
  // referência é o que ela lê para não marcar sobre escolhas velhas.
  const escolhasAtuais = useRef<Record<string, Escolha>>({});
  function definirEscolhas(novas: Record<string, Escolha>) {
    escolhasAtuais.current = novas;
    definirEscolhasNoEstado(novas);
  }
  const [escuta, definirEscuta] = useState<{ perguntaId: string; transcricao: string } | null>(
    null,
  );
  const encerrarEscuta = useRef<((descartar?: boolean) => void) | null>(null);
  const [indiceDaPergunta, definirIndiceDaPergunta] = useState(0);
  // O retorno da pergunta respondida, enquanto o símbolo está na tela, e o
  // placar que o núcleo devolveu ao fim — só na sondagem (`RF-05-99`,
  // `RF-05-100`).
  const [retorno, definirRetorno] = useState<{ perguntaId: string; acertou: boolean } | null>(
    null,
  );
  const [resultadoDaSondagem, definirResultadoDaSondagem] = useState<{
    acertos: number;
    total: number;
  } | null>(null);
  const temporizadorDoRetorno = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [midiaCarregando, definirMidiaCarregando] = useState(false);
  const [entregue, definirEntregue] = useState<ComprovacaoEntregue | null>(
    comprovacaoEntregue ?? null,
  );
  // O veredito do Mestre, vindo do percurso. Entregar de novo o **limpa**,
  // porque a entrega nova reabre a declaração no núcleo e o julgamento
  // anterior não vale mais para ela (`RN-09-54`).
  const [vereditoDoMestre, definirVereditoDoMestre] = useState<JulgamentoDoPratico | null>(
    julgamento ?? null,
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
  const escutaPossivel =
    ehSondagem && ehQuiz && submissaoLigada && microfonePermitido && existeTranscricaoDeFala();

  // A fala entra na **mudança do `id`** da pergunta, guardada em referência, e
  // não num efeito sobre o objeto dela: o objeto é novo a cada render de quem
  // monta, e um efeito por identidade falaria em laço — o mesmo cuidado que o
  // Quiz ao Vivo tem com a sondagem de 2 s (design — decisão 1).
  // A referência guarda o `narrar` junto do `id`, e não o `id` sozinho: ele
  // cala quando a narração está desligada ou quando a voz do aparelho ainda
  // não chegou, e um `id` já marcado faria a pergunta nunca falar depois — o
  // laço de `useNarrarAoEntrar`, que refala quando o `narrar` muda de
  // identidade, sem o `id` só porque não precisa dele.
  // `escuta` entra na marca porque a permissão do microfone chega depois do
  // toque que liga: a pergunta no ar é falada de novo, agora com a janela.
  const perguntaFalada = useRef<{
    id: string;
    narrar: typeof narrar;
    escuta: boolean;
  } | null>(null);
  // O que a janela faz ao fechar mora numa referência renovada a cada render:
  // o retorno do navegador chega depois, e precisa da tela de agora.
  const aoFimDaEscuta = useRef<(pergunta: Pergunta, transcricao: string) => void>(() => {});
  aoFimDaEscuta.current = (pergunta, transcricao) => {
    encerrarEscuta.current = null;
    definirEscuta(null);
    const ligada = ligarFalaAAlternativa(transcricao, pergunta.alternativas);
    const escolha: Escolha = ligada ?? { falada: transcricao };
    // A resposta falada passa pelo mesmo retorno do toque antes de seguir;
    // na última, a sondagem se submete sozinha (`RF-05-97`, `RF-05-99`).
    responderNaSondagem.current(pergunta, escolha);
  };

  // Responder uma pergunta da sondagem: grava a escolha, mostra o retorno —
  // conferido contra a alternativa correta que só a sondagem traz — e, passados
  // os 2 s, avança ou, na última, submete. Resposta falada sem alternativa é
  // erro (`RN-05-55`). Em referência pelo mesmo motivo do fim da escuta: o
  // temporizador dispara fora do render.
  const responderNaSondagem = useRef<(pergunta: Pergunta, escolha: Escolha) => void>(() => {});
  responderNaSondagem.current = (pergunta, escolha) => {
    const novas = { ...escolhasAtuais.current, [pergunta.id]: escolha };
    definirEscolhas(novas);
    const acertou = typeof escolha === "number" && escolha === pergunta.alternativa_correta;
    definirRetorno({ perguntaId: pergunta.id, acertou });
    narrar({ texto: acertou ? TEXTO_DO_ACERTO : TEXTO_DO_ERRO });
    const posicao = perguntas.findIndex((cada) => cada.id === pergunta.id);
    if (temporizadorDoRetorno.current) clearTimeout(temporizadorDoRetorno.current);
    temporizadorDoRetorno.current = setTimeout(() => {
      temporizadorDoRetorno.current = null;
      definirRetorno(null);
      if (posicao < perguntas.length - 1) {
        definirIndiceDaPergunta(posicao + 1);
        return;
      }
      void submeter({}, null, novas);
    }, RETORNO_DA_SONDAGEM_MS);
  };

  // A tela que sai leva o temporizador junto: sondagem largada no meio não
  // submete nada (design — decisão 5).
  useEffect(
    () => () => {
      if (temporizadorDoRetorno.current) clearTimeout(temporizadorDoRetorno.current);
    },
    [],
  );

  function refazerASondagem() {
    definirEscolhas({});
    definirRetorno(null);
    definirResultadoDaSondagem(null);
    definirErro(null);
    // A primeira pergunta volta a ser falada, ainda que seja a mesma.
    perguntaFalada.current = null;
    definirIndiceDaPergunta(0);
  }

  const abrirEscuta = useRef<(pergunta: Pergunta) => void>(() => {});
  abrirEscuta.current = (pergunta) => {
    if (!escutaPossivel || encerrarEscuta.current) return;
    try {
      definirEscuta({ perguntaId: pergunta.id, transcricao: "" });
      encerrarEscuta.current = escutarPorJanela({
        duracaoMs: JANELA_DA_SONDAGEM_MS,
        aoParcial: (transcricao) =>
          definirEscuta((atual) =>
            atual?.perguntaId === pergunta.id ? { ...atual, transcricao } : atual,
          ),
        aoEncerrar: (transcricao) => aoFimDaEscuta.current(pergunta, transcricao),
      });
    } catch {
      // Sem reconhecimento, a sondagem segue por toque, sem alarme.
      encerrarEscuta.current = null;
      definirEscuta(null);
    }
  };

  // Trocar de pergunta ou sair da tela fecha o microfone **sem** entregar: a
  // janela é da pergunta que estava no ar (`RN-05-54`).
  const idDaPerguntaDaVez = perguntaDaVez?.id;
  useEffect(() => {
    if (!idDaPerguntaDaVez) return;
    return () => {
      encerrarEscuta.current?.(true);
      encerrarEscuta.current = null;
      definirEscuta(null);
    };
  }, [idDaPerguntaDaVez]);

  useEffect(() => {
    if (!ehQuiz || !perguntaDaVez) return;
    const falada = perguntaFalada.current;
    if (
      falada?.id === perguntaDaVez.id &&
      falada.narrar === narrar &&
      falada.escuta === escutaPossivel
    ) {
      return;
    }
    perguntaFalada.current = { id: perguntaDaVez.id, narrar, escuta: escutaPossivel };
    const pergunta = perguntaDaVez;
    // Só depois de a pergunta ser **dita até o fim** o microfone abre; fala
    // cancelada não avisa o fim, e nada escuta (`RF-05-97`).
    narrar(
      { texto: falaDaPergunta(pergunta) },
      escutaPossivel ? { aoTerminar: () => abrirEscuta.current(pergunta) } : undefined,
    );
  }, [ehQuiz, perguntaDaVez, narrar, escutaPossivel]);

  async function submeter(
    entrega: EntregaDoPratico = {},
    arquivo: File | null = null,
    escolhasDoEnvio: Record<string, Escolha> = escolhas,
  ) {
    if (!sessao) return;
    let respostas = null;
    if (ehQuiz) {
      // O envio não fica disponível antes disto; a guarda é a rede de
      // segurança de quem chamar por outro caminho.
      if (!perguntas.every((pergunta) => escolhasDoEnvio[pergunta.id] !== undefined)) return;
      respostas = perguntas.map((pergunta) => {
        const escolha = escolhasDoEnvio[pergunta.id];
        return typeof escolha === "number"
          ? { pergunta_id: pergunta.id, alternativa_escolhida: escolha }
          : { pergunta_id: pergunta.id, resposta_falada: escolha.falada };
      });
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
      if (ehSondagem) {
        definirResultadoDaSondagem({ acertos: resultado.acertos, total: resultado.total });
        return;
      }
      if (resultado.aprovado === true) {
        aoDesbloquear();
        return;
      }
      if (resultado.aguardando_mestre) {
        definirEntregue(resultado.comprovacao_entregue ?? null);
        // A entrega nova reabre a declaração no núcleo: o veredito anterior
        // não vale mais para ela, e deixá-lo na tela diria à criança que ela
        // foi recusada de novo, sem ninguém ter julgado (`RN-09-54`).
        definirVereditoDoMestre(null);
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

  /** Envia o arquivo de uma declaração em mídia que ficou sem ele, sem
   * declarar de novo: a sessão de envio aceita a declaração pendente
   * (`RF-05-91`, `RF-05-93`). */
  async function enviarArquivoPendente(arquivo: File) {
    if (!sessao) return;
    definirEnviando(true);
    definirErro(null);
    try {
      definirEntregue(await enviarArquivoDaComprovacao(arquivo, sessao.token));
    } catch (erroCapturado) {
      if (erroCapturado instanceof QuedaDeRedeDuranteEnvio) {
        definirErro(MENSAGEM_DE_QUEDA_DE_REDE);
        return;
      }
      definirErro("Não foi possível enviar agora. Tente de novo em instantes.");
    } finally {
      definirEnviando(false);
    }
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
            julgamento={vereditoDoMestre}
            aoDeclarar={submeter}
            aoEnviarArquivo={enviarArquivoPendente}
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
  const envioDoQuiz =
    submissaoLigada && !ehSondagem ? (
      <Botao onClick={() => submeter()} desabilitado={enviando || !todasRespondidas}>
        {enviando ? "Enviando…" : "Enviar respostas"}
      </Botao>
    ) : undefined;

  // A pergunta como a tela a apresenta, no paginador do desafio ou sozinha na
  // sondagem. Na sondagem, enquanto o retorno está na tela, as alternativas
  // ficam travadas e a resposta dada não se troca (`RF-05-99`).
  const travadaPeloRetorno = ehSondagem && (retorno !== null || enviando);
  function perguntaNaTela(pergunta: Pergunta) {
    return (
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
            ampliavel
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
                  disabled={!submissaoLigada || travadaPeloRetorno}
                  onChange={() => {
                    // O toque vence a voz: fecha o microfone sem
                    // entregar a fala, e vale a alternativa (`RN-05-54`).
                    encerrarEscuta.current?.(true);
                    encerrarEscuta.current = null;
                    definirEscuta(null);
                    if (ehSondagem) {
                      responderNaSondagem.current(pergunta, posicao + 1);
                      return;
                    }
                    definirEscolhas({ ...escolhas, [pergunta.id]: posicao + 1 });
                  }}
                />
                {alternativa}
              </label>
            </li>
          ))}
        </ul>
        {escuta?.perguntaId === pergunta.id && (
          <JanelaDeEscuta
            key={pergunta.id}
            duracaoMs={JANELA_DA_SONDAGEM_MS}
            transcricao={escuta.transcricao}
          />
        )}
        {/* O retorno: forma distinta e texto anunciado, nunca só a cor. A
              região é fixa para o leitor de tela anunciar o que entra nela. */}
        {ehSondagem && (
          <div role="status" className="cg-trilha__retorno-da-sondagem">
            {retorno?.perguntaId === pergunta.id && (
              <span
                className={
                  retorno.acertou
                    ? "cg-trilha__retorno cg-trilha__retorno--acerto"
                    : "cg-trilha__retorno cg-trilha__retorno--erro"
                }
              >
                <Icone glifo={retorno.acertou ? "acerto" : "erro"} tamanho={48} />
                <span className="cg-trilha__oculto">
                  {retorno.acertou ? TEXTO_DO_ACERTO : TEXTO_DO_ERRO}
                </span>
              </span>
            )}
          </div>
        )}
      </fieldset>
    );
  }

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

      {ehQuiz && !ehSondagem && (
        <SequenciaPaginada
          itens={perguntas}
          rotuloDeAvancar="Próxima pergunta"
          rotuloDeVoltar="Pergunta anterior"
          indice={indiceDaPergunta}
          aoIrPara={definirIndiceDaPergunta}
          acoes={envioDoQuiz}
          controlesTravados={midiaCarregando}
        >
          {(pergunta) => perguntaNaTela(pergunta)}
        </SequenciaPaginada>
      )}

      {/* A sondagem não pagina: a pergunta da vez sozinha, sem avançar, sem
          voltar e sem enviar — ela segue e se submete sozinha (`RF-05-99`). */}
      {ehQuiz && ehSondagem && resultadoDaSondagem === null && perguntaDaVez && (
        <>
          {perguntaNaTela(perguntaDaVez)}
          {enviando && <p>Enviando…</p>}
          {erro !== null && !enviando && submissaoLigada && (
            <Botao onClick={() => submeter()}>Tentar de novo</Botao>
          )}
        </>
      )}

      {ehSondagem && resultadoDaSondagem !== null && (
        <div className="cg-trilha__fim-da-sondagem">
          <p>
            Você acertou {resultadoDaSondagem.acertos} e errou{" "}
            {resultadoDaSondagem.total - resultadoDaSondagem.acertos}.
          </p>
          <div className="cg-trilha__acoes-da-sondagem">
            <Botao variante="secundaria" onClick={refazerASondagem}>
              Refazer
            </Botao>
            <Botao onClick={() => aoDesbloquear()}>Concluir</Botao>
          </div>
        </div>
      )}

      {/* O desafio que se cumpre por **declaração** não tem pergunta a
          responder: o que ele pede é a comprovação na forma que o Mestre
          autor aceitou, sob o critério que ele escreveu (`RF-05-91`,
          `RF-05-92`). */}
      {!ehQuiz && submissaoLigada && (
        <EntregaDoPraticoNaTela
          desafio={desafio}
          comprovacaoEntregue={null}
          julgamento={null}
          aoDeclarar={submeter}
          aoEnviarArquivo={enviarArquivoPendente}
          enviando={enviando}
          erro={erro}
        />
      )}

      {/* Desligada a submissão, o critério e a forma seguem à vista: eles não
          são segredo do Mestre, e é deles que a criança sabe o que preparar. */}
      {!ehQuiz && !submissaoLigada && !!desafio.criterio_de_aceite && (
        <div className="cg-trilha__criterio">
          <h4>O que o seu Mestre combinou</h4>
          <p>{desafio.criterio_de_aceite}</p>
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
