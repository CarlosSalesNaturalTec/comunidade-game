import { chamarNucleo } from "comum/api";

export interface VerificadorDoPin {
  algoritmo: string;
  iteracoes: number;
  sal: string;
  resumo: string;
}

interface EstadoDoPin {
  personaId: string;
  verificador: VerificadorDoPin | null;
  erros: number;
  bloqueado: boolean;
}

// Mesma chave-mãe da sessão de trabalho: o verificador vive só enquanto ela
// dura e sai junto com ela. O PIN nunca é gravado — só o verificador de quem
// abriu a sessão, o contador de erros seguidos e a marca de bloqueio, para
// que recarregar a página não os zere (`RN-04-38`, design — decisão 7).
const CHAVE_DO_ESTADO_DO_PIN = "app-01:sessao-trabalho:pin";

// Cinco erros seguidos bloqueiam o PIN neste aparelho até novo login
// Google, com ou sem rede (`RN-04-38`, documento 03 §1.1).
export const ERROS_ATE_O_BLOQUEIO = 5;

export const FORMATO_DO_PIN = /^[0-9]{4}$/;

export function buscarVerificadorDoPin(tokenDeTrabalho: string): Promise<VerificadorDoPin> {
  return chamarNucleo<VerificadorDoPin>("/v1/eu/pin-de-confirmacao/verificador", {
    token: tokenDeTrabalho,
  });
}

function lerEstado(): EstadoDoPin | null {
  try {
    const bruto = sessionStorage.getItem(CHAVE_DO_ESTADO_DO_PIN);
    return bruto ? (JSON.parse(bruto) as EstadoDoPin) : null;
  } catch {
    return null;
  }
}

function gravarEstado(estado: EstadoDoPin): void {
  sessionStorage.setItem(CHAVE_DO_ESTADO_DO_PIN, JSON.stringify(estado));
}

export function estadoDoPinDe(personaId: string): EstadoDoPin | null {
  const estado = lerEstado();
  return estado?.personaId === personaId ? estado : null;
}

export function guardarVerificadorDoPin(
  personaId: string,
  verificador: VerificadorDoPin | null,
): void {
  const anterior = estadoDoPinDe(personaId);
  gravarEstado({
    personaId,
    verificador,
    erros: anterior?.erros ?? 0,
    bloqueado: anterior?.bloqueado ?? false,
  });
}

export function apagarEstadoDoPin(): void {
  sessionStorage.removeItem(CHAVE_DO_ESTADO_DO_PIN);
}

export function verificadorGuardado(): VerificadorDoPin | null {
  return lerEstado()?.verificador ?? null;
}

export function pinBloqueadoNoAparelho(): boolean {
  return lerEstado()?.bloqueado ?? false;
}

export function marcarPinBloqueado(): void {
  const estado = lerEstado();
  if (estado) gravarEstado({ ...estado, bloqueado: true });
}

/** Conta um erro seguido e diz se ele bloqueou o PIN. */
export function registrarErroDePin(): boolean {
  const estado = lerEstado();
  if (!estado) return false;
  const erros = estado.erros + 1;
  const bloqueado = erros >= ERROS_ATE_O_BLOQUEIO;
  gravarEstado({ ...estado, erros, bloqueado });
  return bloqueado;
}

export function zerarErrosDePin(): void {
  const estado = lerEstado();
  if (estado && estado.erros !== 0) gravarEstado({ ...estado, erros: 0 });
}

function deBase64(texto: string): Uint8Array<ArrayBuffer> {
  return Uint8Array.from(atob(texto), (caractere) => caractere.charCodeAt(0));
}

// A mesma derivação do núcleo — PBKDF2-HMAC-SHA256 com o sal e as iterações
// do próprio verificador —, pelo `SubtleCrypto` do navegador, sem biblioteca
// nova (design — decisão 1).
export async function pinConfereNoAparelho(
  pin: string,
  verificador: VerificadorDoPin,
): Promise<boolean> {
  const material = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(pin),
    "PBKDF2",
    false,
    ["deriveBits"],
  );
  const esperado = deBase64(verificador.resumo);
  const bits = await crypto.subtle.deriveBits(
    {
      name: "PBKDF2",
      hash: "SHA-256",
      salt: deBase64(verificador.sal),
      iterations: verificador.iteracoes,
    },
    material,
    esperado.length * 8,
  );
  const calculado = new Uint8Array(bits);
  if (calculado.length !== esperado.length) return false;
  let diferenca = 0;
  for (let indice = 0; indice < calculado.length; indice += 1) {
    diferenca |= calculado[indice] ^ esperado[indice];
  }
  return diferenca === 0;
}
