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
// O backend é **declarado**, não autosselecionado. Omitido, a Human escolhe
// `webgpu` sempre que `navigator.gpu` existir — o que é verdade em Chrome
// mesmo onde `requestAdapter()` devolve `null`, e ali o `load()` morre antes
// de buscar qualquer modelo: em produção, nenhum modelo chegou a ser baixado
// e toda captura reprovava por vivacidade (`RF-04-65`, design — decisão 1).
// `webgl` é o denominador comum dos aparelhos modestos do documento 03 §3.2.
const human = new Human({
  backend: "webgl",
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

// O laço de detecção: quadros são colhidos até a vivacidade passar ou o tempo
// se esgotar, em vez de um único quadro colhido no instante do acionamento —
// com a câmera recém-aberta e a exposição ainda se ajustando (`RF-04-64`,
// design — decisão 3).
const ESPERA_ENTRE_QUADROS_MS = 200;
const TEMPO_MAXIMO_DA_VIVACIDADE_MS = 15_000;

// Preparo que não se concluiu — câmera que não abriu ou modelos que não
// carregaram. Existe como erro próprio para que a tela diga o que aconteceu
// em vez de anunciar ausência de pessoa diante da câmera: foi essa confusão
// que escondeu por um mês um `load()` que nunca baixou modelo (`RF-04-65`,
// design — decisão 4).
export class ErroDePreparoDaCaptura extends Error {}

// O que o laço está vendo, para a tela dar retorno **abstrato** a quem opera.
// Só isto sai daqui sobre a imagem: nunca quadro, nunca pixel (`RN-04-34`,
// documento 99 §6 invariante 12).
export type EstadoDaVivacidade =
  | "procurando_rosto"
  | "rosto_encontrado"
  | "vivacidade_confirmada";

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
  video.className = "cg-visor";
  await video.play();
  elementoDeVideo = video;
  return video;
}

// Abre a câmera e carrega os modelos **antes** de qualquer julgamento de
// vivacidade. Falha aqui é falha de preparo, e lança — nunca devolve o
// mesmo `false` da vivacidade reprovada (`RF-04-65`, design — decisão 4).
export async function prepararCaptura(): Promise<void> {
  try {
    await abrirCamera();
    await human.load();
  } catch (causa) {
    throw new ErroDePreparoDaCaptura("Não foi possível preparar a câmera.", { cause: causa });
  }

  // `load()` resolve sem lançar quando nenhum modelo chega a ser buscado —
  // foi assim que o backend autosselecionado passou despercebido. Sem modelo,
  // `detect` não acha rosto nenhum, e a tela culparia a pessoa.
  if (human.models.loaded().length === 0) {
    throw new ErroDePreparoDaCaptura("Os modelos de biometria não foram carregados.");
  }
}

// Anexa o visor ao elemento que a tela forneceu. A tela **empresta um lugar**:
// nem `MediaStream`, nem quadro, nem pixel saem deste módulo, e a fronteira
// que garante o invariante 12 continua de pé por construção (`RF-04-64`,
// design — decisão 2). Sem preparo feito, não há o que acoplar.
export function acoplarEspelho(container: HTMLElement): void {
  if (elementoDeVideo === null || elementoDeVideo.parentElement === container) return;
  container.replaceChildren(elementoDeVideo);
}

// Encerra a câmera, desacopla o visor e descarta o quadro capturado — chamado
// ao fim de toda tentativa de captura, aprovada ou não (`RN-04-08`,
// `RN-04-12`).
export function encerrarCaptura(): void {
  for (const faixa of fluxo?.getTracks() ?? []) {
    faixa.stop();
  }
  elementoDeVideo?.remove();
  fluxo = null;
  elementoDeVideo = null;
}

function esperar(milissegundos: number): Promise<void> {
  return new Promise((resolver) => setTimeout(resolver, milissegundos));
}

// Prova de vivacidade, sempre antes do descritor (documento 03 §3.3), colhida
// **em laço** até passar ou o tempo se esgotar: um único quadro no instante do
// acionamento reprova quem só precisava de mais um segundo de exposição
// (`RF-04-64`, design — decisão 3). Devolve `false` sem lançar — reprovada, a
// tela oferece nova tentativa sem enviar nada ao núcleo (`RF-04-13`,
// `RF-04-48`).
//
// `aoMudarEstado` é o retorno **abstrato** a quem opera: diz o que o laço vê,
// nunca o que a câmera capturou (`RN-04-34`).
export async function provarVivacidade(
  aoMudarEstado?: (estado: EstadoDaVivacidade) => void,
): Promise<boolean> {
  const video = await abrirCamera();
  const limite = Date.now() + TEMPO_MAXIMO_DA_VIVACIDADE_MS;
  let ultimoEstado: EstadoDaVivacidade | null = null;

  const anunciar = (estado: EstadoDaVivacidade) => {
    if (estado === ultimoEstado) return;
    ultimoEstado = estado;
    aoMudarEstado?.(estado);
  };

  do {
    const resultado = await human.detect(video);
    const rosto = resultado.face[0];
    if (rosto) {
      const antispoofagem = rosto.real ?? 0;
      const vivacidade = rosto.live ?? 0;
      if (antispoofagem >= LIMIAR_DE_VIVACIDADE && vivacidade >= LIMIAR_DE_VIVACIDADE) {
        anunciar("vivacidade_confirmada");
        return true;
      }
      anunciar("rosto_encontrado");
    } else {
      anunciar("procurando_rosto");
    }
    await esperar(ESPERA_ENTRE_QUADROS_MS);
  } while (Date.now() < limite);

  return false;
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
