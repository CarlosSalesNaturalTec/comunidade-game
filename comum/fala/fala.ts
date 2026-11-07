// Tipos mínimos da Web Speech API do navegador — sem pacote de tipos: só
// o que este módulo usa entra aqui (design — decisão 6).
interface ResultadoDeFala {
  transcript: string;
}

interface ListaDeResultadosDeFala {
  length: number;
  [indice: number]: { length: number; [indice: number]: ResultadoDeFala };
}

interface EventoDeResultadoDeFala extends Event {
  results: ListaDeResultadosDeFala;
}

interface EventoDeErroDeFala extends Event {
  error: string;
}

interface ReconhecimentoDeFala extends EventTarget {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  onresult: ((evento: EventoDeResultadoDeFala) => void) | null;
  onerror: ((evento: EventoDeErroDeFala) => void) | null;
  onend: (() => void) | null;
  start(): void;
  stop(): void;
}

interface ConstrutorDeReconhecimentoDeFala {
  new (): ReconhecimentoDeFala;
}

declare global {
  interface Window {
    SpeechRecognition?: ConstrutorDeReconhecimentoDeFala;
    webkitSpeechRecognition?: ConstrutorDeReconhecimentoDeFala;
  }
}

// A plataforma é de uma comunidade brasileira; nenhum documento prevê
// outro idioma (design — decisão 5).
const IDIOMA = "pt-BR";

function obterConstrutor(): ConstrutorDeReconhecimentoDeFala | undefined {
  return window.SpeechRecognition ?? window.webkitSpeechRecognition;
}

// Único módulo que toca a API de fala do navegador — a fronteira que
// garante que o áudio nunca sai do aparelho: só a transcrição atravessa
// (`RF-04-40`, `RN-04-21`). Onde o navegador não oferece a API, a tela
// mantém só o texto digitado (`RF-04-39`, design — decisão 6).
export function existeTranscricaoDeFala(): boolean {
  return obterConstrutor() !== undefined;
}

interface RetornosDaTranscricao {
  aoTranscrever: (transcricao: string) => void;
  aoFalhar: (motivo: string) => void;
  aoEncerrar: () => void;
}

// Abre o microfone e devolve o encerrador. Uma fala por abertura —
// `continuous` e `interimResults` desligados —, o que já fecha sozinho ao
// fim da fala, exatamente o que `RF-04-39` pede (design — decisão 4). O
// encerrador é seguro de chamar mais de uma vez: depois que o
// reconhecimento já terminou sozinho, ele não faz nada.
export function iniciarTranscricao(retornos: RetornosDaTranscricao): () => void {
  const Construtor = obterConstrutor();
  if (!Construtor) {
    throw new Error("Este navegador não oferece transcrição de fala.");
  }

  const reconhecimento = new Construtor();
  reconhecimento.lang = IDIOMA;
  reconhecimento.continuous = false;
  reconhecimento.interimResults = false;

  let encerrado = false;

  reconhecimento.onresult = (evento) => {
    const transcricao = evento.results[0]?.[0]?.transcript;
    if (transcricao) retornos.aoTranscrever(transcricao);
  };
  reconhecimento.onerror = (evento) => {
    retornos.aoFalhar(evento.error);
  };
  reconhecimento.onend = () => {
    encerrado = true;
    retornos.aoEncerrar();
  };

  reconhecimento.start();

  return () => {
    if (!encerrado) reconhecimento.stop();
  };
}

/**
 * Pede a permissão do microfone ao navegador e devolve se foi dada. Só a
 * permissão: as faixas abertas param na hora e nada é captado (`RN-05-54`,
 * design — decisão 3). Sem a API, ou negada, devolve `false` sem lançar.
 */
export async function pedirPermissaoDoMicrofone(): Promise<boolean> {
  const dispositivos = typeof navigator === "undefined" ? undefined : navigator.mediaDevices;
  if (!dispositivos?.getUserMedia) return false;
  try {
    const fluxo = await dispositivos.getUserMedia({ audio: true });
    for (const faixa of fluxo.getTracks()) faixa.stop();
    return true;
  } catch {
    return false;
  }
}

interface RetornosDaJanela {
  duracaoMs: number;
  /** O que foi dito até aqui, a cada resultado — também os parciais. */
  aoParcial: (transcricao: string) => void;
  /** Uma vez só, ao fim: o texto acumulado, vazio no silêncio ou no erro. */
  aoEncerrar: (transcricao: string) => void;
}

/**
 * Escuta por uma janela de tempo e fecha sozinha ao fim dela — a resposta
 * falada da sondagem (`RF-05-97`, design — decisão 2). Ao contrário de
 * `iniciarTranscricao`, liga `continuous` e `interimResults`: a tela mostra o
 * que a criança diz enquanto ela diz, e o prazo, não a pausa, encerra.
 * O navegador encerrar sozinho antes do prazo (pausa longa) não antecipa a
 * entrega: a janela dura o que a tela mostra. Devolve o encerrador, seguro
 * de chamar mais de uma vez; `descartar` fecha o microfone **sem** entregar —
 * é o toque numa alternativa durante a janela, que vale no lugar da fala.
 */
export function escutarPorJanela(retornos: RetornosDaJanela): (descartar?: boolean) => void {
  const Construtor = obterConstrutor();
  if (!Construtor) {
    throw new Error("Este navegador não oferece transcrição de fala.");
  }

  const reconhecimento = new Construtor();
  reconhecimento.lang = IDIOMA;
  reconhecimento.continuous = true;
  reconhecimento.interimResults = true;

  let transcricao = "";
  let parado = false;
  let entregue = false;

  function entregar() {
    if (entregue) return;
    entregue = true;
    clearTimeout(prazo);
    retornos.aoEncerrar(transcricao.trim());
  }

  function parar(descartar = false) {
    if (descartar) {
      entregue = true;
      clearTimeout(prazo);
    }
    if (!parado) {
      parado = true;
      try {
        reconhecimento.stop();
      } catch {
        // Já terminou sozinho.
      }
    }
    // O `onend` pode demorar ou não vir (Safari): o fim da janela é o prazo,
    // não o navegador.
    entregar();
  }

  reconhecimento.onresult = (evento) => {
    const partes: string[] = [];
    for (let indice = 0; indice < evento.results.length; indice += 1) {
      const melhor = evento.results[indice]?.[0]?.transcript;
      if (melhor) partes.push(melhor.trim());
    }
    transcricao = partes.join(" ");
    if (!entregue) retornos.aoParcial(transcricao);
  };
  // `no-speech`, `aborted` e afins: o que foi dito até ali vale, e o
  // silêncio é resposta vazia — nunca alarme (`RF-05-98`).
  reconhecimento.onerror = () => {};
  reconhecimento.onend = () => {
    parado = true;
  };

  const prazo = setTimeout(() => parar(), retornos.duracaoMs);
  reconhecimento.start();

  return parar;
}
