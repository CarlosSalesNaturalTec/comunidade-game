// A síntese de fala do navegador — o caminho inverso de `comum/fala`, que é
// o reconhecimento. Os tipos vêm da `lib.dom`: `SpeechSynthesis`,
// `SpeechSynthesisUtterance` e `SpeechSynthesisVoice` já estão lá, ao
// contrário do reconhecimento, que o irmão precisou declarar à mão.

// A plataforma é de uma comunidade brasileira; nenhum documento prevê outro
// idioma, e voz de outro idioma lendo português não é acessibilidade, é
// ruído (documento 15 §5.1, design — decisão 5).
const IDIOMA = "pt-BR";

/**
 * O que uma tela entrega à narração — e a fronteira do dado, defendida pelo
 * **tipo** e não por recomendação: dos dados do Guerreiro(a) só o `nick`
 * tem campo aqui. Nome, nascimento, vínculo e comunidade não têm por onde
 * entrar (documento 03 §§1.12, 12, design — decisão 2).
 *
 * O `texto` é a frase declarada pela tela e pode conter o marcador
 * `{nick}`; a substituição acontece **dentro** da camada.
 */
export interface Fala {
  texto: string;
  nick?: string;
}

// Único módulo que toca a síntese de fala do navegador — a fronteira por
// onde o texto passa antes de ser falado, que pode ser voz de rede
// (documento 03 §1.12). Onde o navegador não a oferece, tudo aqui devolve
// silêncio: nenhuma tela precisa perguntar.
function motorDeFala(): SpeechSynthesis | undefined {
  if (typeof window === "undefined") return undefined;
  if (typeof window.speechSynthesis === "undefined") return undefined;
  if (typeof window.SpeechSynthesisUtterance === "undefined") return undefined;
  return window.speechSynthesis;
}

export function existeSinteseDeFala(): boolean {
  return motorDeFala() !== undefined;
}

// `pt_BR` aparece em alguns aparelhos Android no lugar de `pt-BR`.
function ehPortuguesDoBrasil(voz: SpeechSynthesisVoice): boolean {
  return voz.lang.replace("_", "-").toLowerCase() === IDIOMA.toLowerCase();
}

/**
 * A voz da narração: pt-BR, e entre as candidatas a **local** — não por
 * privacidade do texto da plataforma, que a decisão já liberou, mas porque
 * ela funciona sem rede. Não havendo pt-BR alguma, devolve `null` e a
 * camada cala (design — decisão 5).
 */
export function vozPreferida(): SpeechSynthesisVoice | null {
  const motor = motorDeFala();
  if (!motor) return null;
  const candidatas = motor.getVoices().filter(ehPortuguesDoBrasil);
  if (candidatas.length === 0) return null;
  return candidatas.find((voz) => voz.localService) ?? candidatas[0];
}

/**
 * `getVoices()` volta vazio até o navegador carregar a lista — no Chrome,
 * até o evento `voiceschanged`. Devolve o encerrador da escuta.
 */
export function observarVozes(aoMudar: () => void): () => void {
  const motor = motorDeFala();
  if (!motor) return () => {};
  motor.addEventListener("voiceschanged", aoMudar);
  return () => motor.removeEventListener("voiceschanged", aoMudar);
}

/**
 * Monta o enunciado a partir da fala declarada. É **aqui** que o `{nick}`
 * é substituído, e é por isto que nenhum outro dado do Guerreiro(a) alcança
 * a síntese: a camada lê o `texto` e o `nick`, e mais nada do que lhe
 * entregarem (design — decisão 2).
 */
export function enunciarFala(fala: Fala): string {
  return fala.texto
    .replaceAll("{nick}", fala.nick ?? "")
    .replace(/\s+/g, " ")
    .trim();
}

/**
 * Fala o enunciado, cancelando antes o que estiver em curso: uma tela fala
 * uma coisa, e a seguinte cala a anterior (documento 15 §5.1).
 */
export function falar(fala: Fala, voz: SpeechSynthesisVoice): void {
  const motor = motorDeFala();
  if (!motor || typeof window.SpeechSynthesisUtterance === "undefined") return;
  const enunciado = enunciarFala(fala);
  if (enunciado === "") return;
  motor.cancel();
  const dito = new window.SpeechSynthesisUtterance(enunciado);
  dito.lang = IDIOMA;
  dito.voice = voz;
  motor.speak(dito);
}

export function cancelar(): void {
  motorDeFala()?.cancel();
}

/**
 * O navegador não deixa falar antes de um gesto da pessoa. Um enunciado
 * vazio, falado **dentro** do próprio gesto, é o que libera o motor —
 * descartado tentar falar e detectar a falha, que o navegador não reporta
 * de forma confiável (design — decisão 6).
 */
export function armar(): void {
  const motor = motorDeFala();
  if (!motor || typeof window.SpeechSynthesisUtterance === "undefined") return;
  motor.speak(new window.SpeechSynthesisUtterance(""));
}
