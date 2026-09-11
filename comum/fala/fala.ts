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
