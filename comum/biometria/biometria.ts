// O `alias` do `vite.config.ts` resolve este especificador para o build ESM
// de navegador — sem ele, cairia no build Node, que exige
// `@tensorflow/tfjs-node` nativo.
import Human from "@vladmandic/human";

// Único módulo da App 01 que importa a Human, carrega modelo ou toca
// `getUserMedia` — a fronteira que garante o invariante 12 por construção:
// a fotografia só existe aqui dentro, e as duas funções expostas devolvem
// só `boolean` e `number[]` (`RF-04-14`, `RF-04-48`, `RN-04-08`, `RN-04-12`,
// design — decisão 5).
//
// Modelos embarcados no build, sob `/modelos-de-biometria/` — sem provedor
// externo (documento 03 §3.3) —, e carregados só ao entrar neste módulo,
// nunca na subida da aplicação (documento 03 §3.4).
const human = new Human({
  modelBasePath: "/modelos-de-biometria/",
  warmup: "none",
  face: {
    enabled: true,
    detector: { rotation: true, maxDetected: 1 },
    mesh: { enabled: true },
    description: { enabled: true },
    antispoof: { enabled: true },
    liveness: { enabled: true },
    emotion: { enabled: false },
    iris: { enabled: false },
    gear: { enabled: false },
  },
  body: { enabled: false },
  hand: { enabled: false },
  object: { enabled: false },
  gesture: { enabled: false },
  segmentation: { enabled: false },
});

// Limiar de vivacidade — parâmetro de operação, ajustável na primeira turma
// (pendência do PRD-04 §14, "peso dos modelos"); não é regra de produto.
const LIMIAR_DE_VIVACIDADE = 0.5;

// Verifica a presença de câmera sem abri-la (`RF-04-04`). Sem câmera, o
// onboarding continua pelo caminho sem imagem — só a captura fecha (design
// — decisão 6, `RN-04-03`, `RN-04-09`).
export async function existeCamera(): Promise<boolean> {
  if (!navigator.mediaDevices?.enumerateDevices) return false;
  const dispositivos = await navigator.mediaDevices.enumerateDevices();
  return dispositivos.some((dispositivo) => dispositivo.kind === "videoinput");
}

let fluxo: MediaStream | null = null;
let elementoDeVideo: HTMLVideoElement | null = null;

async function abrirCamera(): Promise<HTMLVideoElement> {
  if (elementoDeVideo) return elementoDeVideo;
  fluxo = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } });
  const video = document.createElement("video");
  video.srcObject = fluxo;
  video.muted = true;
  video.playsInline = true;
  await video.play();
  elementoDeVideo = video;
  return video;
}

// Encerra a câmera e descarta o quadro capturado — chamado ao fim de toda
// tentativa de captura, aprovada ou não (`RN-04-08`, `RN-04-12`).
export function encerrarCaptura(): void {
  for (const faixa of fluxo?.getTracks() ?? []) {
    faixa.stop();
  }
  fluxo = null;
  elementoDeVideo = null;
}

// Prova de vivacidade, sempre antes do descritor (documento 03 §3.3).
// Devolve `false` sem lançar — reprovada, a tela oferece nova tentativa
// sem enviar nada ao núcleo (`RF-04-13`, `RF-04-48`).
export async function provarVivacidade(): Promise<boolean> {
  const video = await abrirCamera();
  await human.load();
  const resultado = await human.detect(video);
  const rosto = resultado.face[0];
  if (!rosto) return false;
  const antispoofagem = rosto.real ?? 0;
  const vivacidade = rosto.live ?? 0;
  return antispoofagem >= LIMIAR_DE_VIVACIDADE && vivacidade >= LIMIAR_DE_VIVACIDADE;
}

// Só é chamada depois de `provarVivacidade` aprovar. Encerra a câmera ao
// final — a fotografia não sobrevive à geração do descritor (`RF-04-14`,
// `RN-04-08`).
export async function gerarDescritor(): Promise<number[]> {
  const video = await abrirCamera();
  const resultado = await human.detect(video);
  const rosto = resultado.face[0];
  encerrarCaptura();
  if (!rosto?.embedding) {
    throw new Error("Não foi possível gerar o descritor facial. Tente novamente.");
  }
  return Array.from(rosto.embedding);
}
